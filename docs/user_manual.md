# Boolitha User Manual

A web scraper for extracting property listings from booli.se and saving them as structured markdown documents.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Running the Scraper](#running-the-scraper)
4. [Output Format](#output-format)
5. [Troubleshooting](#troubleshooting)
6. [Technical Details](#technical-details)

---

## Quick Start

For first-time users:

```bash
# 1. Set up the environment (one time only)
./init_toolchain.sh

# 2. Run the test scraper to verify everything works
./run_test.sh

# 3. Scrape property listings for a town
./run_scraper.sh Uppsala
```

---

## Installation

### Prerequisites

- **Python 3.8 or higher** - Check with `python3 --version`
- **macOS or Linux** - The scripts use bash
- **Internet connection** - Required for scraping booli.se

### Setup Steps

1. **Initialize the environment:**
   ```bash
   ./init_toolchain.sh
   ```

   This script will:
   - Create a Python virtual environment in `venv/`
   - Install all required packages (Playwright, BeautifulSoup, etc.)
   - Download the Chromium browser for Playwright
   - Verify the installation

2. **Verify installation:**
   ```bash
   ./run_test.sh
   ```

   If successful, you'll see:
   - A browser window open briefly
   - Message "✓ Test completed successfully!"
   - A screenshot saved as `booli_test_screenshot.png`

---

## Running the Scraper

### Method 1: Using the Helper Script (Recommended)

The easiest way to run the scraper:

```bash
./run_scraper.sh <town_name>
```

**Examples:**

```bash
# Scrape Uppsala
./run_scraper.sh Uppsala

# Scrape Stockholm
./run_scraper.sh Stockholm

# Towns with Swedish characters
./run_scraper.sh Göteborg
./run_scraper.sh Malmö

# Multi-word town names (use quotes)
./run_scraper.sh "Västerås"
```

### Method 2: Manual Execution

If you prefer to run Python directly:

```bash
# 1. Activate the virtual environment
source venv/bin/activate

# 2. Run the scraper
python booli_scraper.py Uppsala

# 3. Deactivate when done (optional)
deactivate
```

### What Happens During Scraping

1. **Browser Launch** - A Chromium browser window opens
2. **Cookie Consent** - Automatically accepts the cookie dialog
3. **Search** - Enters the town name and selects the first suggestion
4. **Navigation** - Clicks "Hitta bostäder" to show results
5. **Extraction** - Scrapes all visible property listings
6. **Save** - Generates and saves a markdown file in `data/`
7. **Cleanup** - Closes the browser

The entire process typically takes 15-30 seconds.

---

## Output Format

### File Location

All scraped data is saved to the `data/` folder:

```
data/
├── booli_listings_uppsala_20260117_160446.md
├── booli_listings_stockholm_20260117_160910.md
└── booli_listings_göteborg_20260117_161203.md
```

**File naming format:** `booli_listings_{town}_{timestamp}.md`

- `{town}` - Town name in lowercase with underscores
- `{timestamp}` - Format: `YYYYMMDD_HHMMSS`

### Markdown Structure

Each output file contains:

#### Header Section
```markdown
# Booli.se Property Listings - Uppsala

**Search Date:** 2026-01-17 15:52:39
**Source URL:** [https://www.booli.se/sok/till-salu?areaIds=419](...)
**Total Listings:** 11
```

#### Individual Listings

Each property listing includes:

```markdown
## 1. Dragarbrunnsgatan 62

**Type:** Lägenhet · Dragarbrunn · Uppsala
**Details:** 3 495 000 kr • 90,5 m² • 4 rum • vån 4 • 5 582 kr/mån • Hiss • Balkong • Inkommet idag
**URL:** [https://www.booli.se/annons/5964839](https://www.booli.se/annons/5964839)
```

**Details include:**
- **Address** - Street address or property name
- **Type** - Property type (Lägenhet/Villa/Radhus), area, and city
- **Price** - Asking price in SEK (if available)
- **Size** - Living area in m²
- **Rooms** - Number of rooms
- **Floor** - Floor level (for apartments)
- **Monthly fee** - Monthly costs (avgift)
- **Amenities** - Hiss (elevator), Balkong (balcony), etc.
- **URL** - Direct link to the full listing on booli.se

### Expected Output Size

Typical scraping results:
- **Small towns:** 5-20 listings
- **Medium cities:** 10-50 listings
- **Large cities (Stockholm, Göteborg):** 10-20 listings per page

**Note:** The scraper currently extracts only the first page of results.

---

## Troubleshooting

### Common Issues

#### 1. "No module named 'playwright'"

**Problem:** Virtual environment not activated

**Solution:**
```bash
source venv/bin/activate
python booli_scraper.py Uppsala
```

Or use the helper script:
```bash
./run_scraper.sh Uppsala
```

---

#### 2. "No suggestions found for this town"

**Problem:** Town name not recognized by booli.se

**Solutions:**
- Check spelling of the town name
- Try using the Swedish spelling (e.g., "Göteborg" instead of "Gothenburg")
- Try the municipality name (e.g., "Uppsala kommun")
- Verify the town exists on booli.se by searching manually first

---

#### 3. Browser doesn't close / hangs

**Problem:** Script interrupted or error occurred

**Solution:**
- Press `Ctrl+C` to stop the script
- Manually close any open Chromium windows
- Run the script again

---

#### 4. "Permission denied" when running scripts

**Problem:** Scripts not executable

**Solution:**
```bash
chmod +x init_toolchain.sh
chmod +x run_test.sh
chmod +x run_scraper.sh
```

---

#### 5. Cookie dialog appears but isn't clicked

**Problem:** Page structure changed or timing issue

**Solution:**
- Wait a few seconds and try again
- The script may still work - the cookie dialog usually doesn't block functionality
- Report the issue if it persists

---

### Browser Window Behavior

**Normal Behavior:**
- The browser window opens and is visible during scraping
- This is intentional - it helps you see what's happening
- The window automatically closes when done

**To run in headless mode (invisible browser):**

Edit `booli_scraper.py` line 37:
```python
# Change this:
headless=False,

# To this:
headless=True,
```

---

## Technical Details

### Technologies Used

- **Python 3.8+** - Main programming language
- **Playwright** - Browser automation for web scraping
- **Chromium** - Headless browser for rendering JavaScript

### Data Privacy

- **No login required** - Only scrapes publicly available listings
- **No personal data** - Only property information is collected
- **Local storage** - All data stays on your computer
- **Cookies** - Session cookies are used but not saved between runs

### Limitations

1. **First page only** - Currently scrapes only the first page of results
2. **No pagination** - Multiple pages are not followed
3. **No images** - Only text data is extracted (images are not downloaded)
4. **Rate limiting** - If scraping multiple cities, wait a few seconds between requests
5. **Dynamic content** - Some listings may not appear if they load asynchronously

### File Management

The `data/` folder and its contents are ignored by git (see `.gitignore`):
- Scraped markdown files won't be committed to version control
- Safe to delete old scraping results without affecting the repository
- The folder is automatically created if it doesn't exist

### Browser Requirements

- Approximately **500 MB** of disk space for Chromium browser
- Installed automatically by `init_toolchain.sh`
- Located in: `~/Library/Caches/ms-playwright/` (macOS)

---

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Verify your Python version: `python3 --version`
3. Re-run setup: `./init_toolchain.sh`
4. Check for updates to the scripts

---

## Examples

### Scraping Multiple Cities

```bash
# Scrape several cities in sequence
./run_scraper.sh Uppsala
./run_scraper.sh Stockholm
./run_scraper.sh Göteborg
./run_scraper.sh Malmö
```

### Checking Results

```bash
# List all scraped files
ls -lh data/

# View a specific file
cat data/booli_listings_uppsala_20260117_160446.md

# Count total listings
grep "^## " data/booli_listings_uppsala_20260117_160446.md | wc -l
```

### Cleaning Up

```bash
# Remove all scraped data
rm -rf data/

# Remove test screenshots
rm -f *.png

# The data folder will be recreated automatically on next run
```

---

**Version:** 1.0
**Last Updated:** 2026-01-17
