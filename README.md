# MapleStory Story Website Scraper

Scrapes all chapters from [The Story of Maple](https://thestoryofmaple.squarespace.com/main-story-table-of-contents) and outputs a formatted Word document with text colors and bold preserved.

## Usage

**Option 1 — Google Colab (no setup required)**
Click the link below, then click Runtime → Run All. The output will save to your Google Drive.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://githubtocolab.com/AiZm8/maplestory-story-website-scraper/blob/main/story_of_maple_scraper.ipynb)

**Option 2 — Run locally**
```bash
pip install playwright python-docx beautifulsoup4
playwright install chromium
python scrape_maple.py
```
