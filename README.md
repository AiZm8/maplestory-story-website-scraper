# MapleStory Story Website Scraper

**Why:**

Formerly, this process was done completely manually by the website owner to help convert their content into PDF form for others (copy pasting, formatting, image adding) for under 3000 pages which is insane. This script automates the text migration and formatting part of that process. Discussed with them on what would be helpful <img width="1107" height="647" alt="image" src="https://github.com/user-attachments/assets/499c8395-f238-4911-99fb-506737ba74b0" />

Thanks maplehero9 for everything you put into this website as an OG maple fan (post bb though..)

**Functionality:**

Scrapes all chapters from [The Story of Maple](https://thestoryofmaple.squarespace.com/main-story-table-of-contents) and outputs a formatted Word document (`.docx`).


**What gets preserved:**
- Document structure (Parts → Chapters → Subheadings)
- Text colors (blue author notes, red key terms)
- Bold formatting

---

## Option 1: Google Colab (no setup required)

Click the button below, then click **Runtime → Run All**. The file will automatically download to your computer when done (~15 minutes).

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://githubtocolab.com/AiZm8/maplestory-story-website-scraper/blob/main/story_of_maple_scraper.ipynb)

---

## Option 2: Run locally

**Requirements:** Python 3.8+

**Install dependencies:**
```bash
pip install playwright python-docx beautifulsoup4
playwright install chromium
```

**Run:**
```bash
python scrape_maple.py
```

Output will be saved as `story_of_maple.docx` in the same folder.


## How it works

1. Loads the table of contents and collects each part and chapter link, skipping pages that aren't part of the main story
2. Opens each chapter in headless Chromium with Playwright, since the Squarespace content is rendered with JavaScript and a plain HTTP request wouldn't return the text
3. Parses each content block with BeautifulSoup, carrying text color and bold through nested tags
4. Writes everything to a Word document with python-docx, with parts, chapters and subheadings as real headings

## Design decisions

- **Built for this one site.** The URL and skipped pages are hardcoded because the goal was the owner's workflow, not a general-purpose scraper.
- **Colab notebook.** The owner can run it from a browser without installing Python or using a terminal.
- **2-second delay between pages** to avoid putting load on the site, which is part of why a full run takes about 15 minutes.
- **Failures don't stop the run.** A page that can't be fetched gets a visible placeholder in the document so it can be filled in by hand.

## Limitations

- Images aren't included and still need to be added manually
- Failed pages aren't retried
