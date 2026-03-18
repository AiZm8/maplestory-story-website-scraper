"""
scrape_maple.py

Scrapes all chapters from The Story of Maple website and outputs a .docx file.
Uses Playwright to handle JavaScript-rendered Squarespace content.
Preserves text color and bold formatting.

Setup:
    pip install playwright python-docx beautifulsoup4
    playwright install chromium

Usage:
    python scrape_maple.py
"""

import time
import re
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup, NavigableString, Tag
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

BASE_URL = "https://thestoryofmaple.squarespace.com"
TOC_URL = f"{BASE_URL}/main-story-table-of-contents"

REQUEST_DELAY = 2.0

SKIP_SLUGS = {
    "main-story-table-of-contents",
    "main-story-abridged-table-of-contents",
    "gms-verse-table-of-contents",
    "lore-changes",
    "grandis-plot-points",
    "storyline-order-and-playthroughs",
    "about",
    "contact-me",
    "lore-pre-destiny",
}


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def parse_color(style: str) -> RGBColor | None:
    """Extract an RGBColor from an inline style string like 'color: #FD0000'."""
    match = re.search(r'color:\s*#([0-9a-fA-F]{6})', style)
    if match:
        hex_color = match.group(1)
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return RGBColor(r, g, b)
    return None


def add_formatted_runs(paragraph, element, inherited_color=None, inherited_bold=False):
    """
    Recursively walk an HTML element and add formatted runs to a docx paragraph.
    Carries color and bold formatting down through nested tags.
    """
    for child in element.children:
        if isinstance(child, NavigableString):
            text = str(child)
            if not text:
                continue
            run = paragraph.add_run(text)
            if inherited_color:
                run.font.color.rgb = inherited_color
            if inherited_bold:
                run.bold = True

        elif isinstance(child, Tag):
            # Determine formatting for this tag
            color = inherited_color
            bold = inherited_bold

            # Check for inline color style
            style = child.get("style", "")
            if style:
                parsed = parse_color(style)
                if parsed:
                    color = parsed

            # Check for bold
            if child.name in ("strong", "b"):
                bold = True

            # Recurse into children
            add_formatted_runs(paragraph, child, inherited_color=color, inherited_bold=bold)


# ---------------------------------------------------------------------------
# TOC parsing
# ---------------------------------------------------------------------------

def parse_toc(page) -> list:
    page.goto(TOC_URL, wait_until="networkidle")

    entries = []
    elements = page.query_selector_all("strong, ol li a, ul li a")

    for el in elements:
        tag = el.evaluate("el => el.tagName.toLowerCase()")
        text = el.inner_text().strip()
        if not text:
            continue

        if tag == "strong" and text.startswith("PART"):
            entries.append({"type": "part", "title": text})

        elif tag == "a":
            href = el.get_attribute("href") or ""
            if href.startswith("/"):
                href = BASE_URL + href
            if BASE_URL in href:
                slug = href.rstrip("/").split("/")[-1]
                if slug not in SKIP_SLUGS:
                    entries.append({"type": "chapter", "title": text, "url": href})

    # Deduplicate while preserving order
    seen_urls = set()
    deduped = []
    for entry in entries:
        if entry["type"] == "part":
            deduped.append(entry)
        elif entry["url"] not in seen_urls:
            seen_urls.add(entry["url"])
            deduped.append(entry)

    return deduped


# ---------------------------------------------------------------------------
# Chapter content extraction
# ---------------------------------------------------------------------------

def extract_chapter_content(page, url: str) -> list:
    """
    Load a chapter page and return a list of content blocks.
    Each block is either:
      {"type": "heading", "level": int, "text": str}
      {"type": "paragraph", "element": BeautifulSoup Tag}
    """
    page.goto(url, wait_until="networkidle")

    blocks = []

    # Get the raw HTML of all sqs-html-content blocks
    content_handles = page.query_selector_all(".sqs-html-content")
    if not content_handles:
        return blocks

    for handle in content_handles:
        html = handle.inner_html()
        soup = BeautifulSoup(html, "html.parser")

        for el in soup.find_all(["h1", "h2", "h3", "h4", "p", "blockquote"]):
            text = el.get_text(strip=True)
            if not text:
                continue

            if el.name in ("h1", "h2", "h3", "h4"):
                blocks.append({"type": "heading", "level": int(el.name[1]), "text": text})
            else:
                # Pass the full element so we can extract formatting later
                blocks.append({"type": "paragraph", "element": el})

    return blocks


# ---------------------------------------------------------------------------
# Document building
# ---------------------------------------------------------------------------

def build_document(page, toc_entries: list) -> Document:
    doc = Document()

    total_chapters = sum(1 for e in toc_entries if e["type"] == "chapter")
    chapter_count = 0

    # Cover title
    title_para = doc.add_heading("The Story of Maple", level=0)
    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph("")

    for entry in toc_entries:
        if entry["type"] == "part":
            doc.add_page_break()
            doc.add_heading(entry["title"], level=1)
            print(f"\n{'='*60}\n  {entry['title']}\n{'='*60}")

        elif entry["type"] == "chapter":
            chapter_count += 1
            print(f"  [{chapter_count}/{total_chapters}] {entry['title']} ...", end=" ", flush=True)

            doc.add_heading(entry["title"], level=2)

            try:
                blocks = extract_chapter_content(page, entry["url"])
            except Exception as e:
                print(f"ERROR: {e}")
                doc.add_paragraph("[Content could not be fetched]")
                continue

            if not blocks:
                doc.add_paragraph("[No content extracted — check this page manually]")
                print("WARNING: no content found")
            else:
                for block in blocks:
                    if block["type"] == "heading":
                        doc.add_heading(block["text"], level=min(block["level"] + 1, 4))
                    else:
                        para = doc.add_paragraph()
                        add_formatted_runs(para, block["element"])

                print(f"OK ({len(blocks)} blocks)")

            time.sleep(REQUEST_DELAY)

    return doc


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    output_file = "story_of_maple.docx"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Fetching table of contents...")
        toc_entries = parse_toc(page)

        chapter_count = sum(1 for e in toc_entries if e["type"] == "chapter")
        part_count = sum(1 for e in toc_entries if e["type"] == "part")
        print(f"Found {part_count} parts and {chapter_count} chapters.\n")

        doc = build_document(page, toc_entries)
        browser.close()

    doc.save(output_file)
    print(f"\nDone! Saved to: {output_file}")


if __name__ == "__main__":
    main()
