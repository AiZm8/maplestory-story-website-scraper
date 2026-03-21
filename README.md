# MapleStory Story Website Scraper

Scrapes all chapters from [The Story of Maple](https://thestoryofmaple.squarespace.com/main-story-table-of-contents) and outputs a formatted Word document (`.docx`).

**What gets preserved:**
- Document structure (Parts → Chapters → Subheadings)
- Text colors (blue author notes, red key terms)
- Bold formatting

---

## Option 1 — Google Colab (no setup required)

Click the button below, then click **Runtime → Run All**. The file will automatically download to your computer when done (~15 minutes).

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://githubtocolab.com/AiZm8/maplestory-story-website-scraper/blob/main/story_of_maple_scraper.ipynb)

---

## Option 2 — Run locally

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
