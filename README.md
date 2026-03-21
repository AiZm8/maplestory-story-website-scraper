# MapleStory Story Website Scraper

**Why:**

Formerly, this process was done completely manually by the website owner to help convert their content into PDF form for others (copy pasting, formatting, image adding). This script aims to alleviate a good chunk of that effort as specified by them so they have less obstacles as they continue to update the story in the future with their awesome content <img width="1107" height="647" alt="image" src="https://github.com/user-attachments/assets/499c8395-f238-4911-99fb-506737ba74b0" />

**Functionality:**

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
