# Bolitha

A Python web scraper for the Swedish website booli.se, built with Playwright.

## Features

- Playwright-based web scraping with headless browser support
- Automatic EU cookie consent handling (Swedish patterns)
- Session/cookie persistence for faster subsequent runs
- Screenshot capture for verification
- Clean OOP architecture for easy extension

## Prerequisites

- Python 3.8 or higher
- macOS, Linux, or Windows

## Quick Start

### 1. Initialize the toolchain

Run the setup script to create a virtual environment and install dependencies:

```bash
./init_toolchain.sh
```

This will:
- Create a Python virtual environment in `venv/`
- Install all required packages from `requirements.txt`
- Download Playwright browser binaries (Chromium)

### 2. Activate the virtual environment

```bash
source venv/bin/activate
```

### 3. Run the test scraper

Verify everything works:

```bash
python test_scraper.py
```

This will open booli.se in a browser window, take a screenshot, and display basic page info.

### 4. Run the main scraper

```bash
python booli_scraper.py
```

This will:
- Open booli.se
- Handle the cookie consent dialog automatically
- Extract sample data (headings by default)
- Take a full-page screenshot
- Save session cookies for future runs

## Project Structure

```
bolitha/
├── init_toolchain.sh       # Setup script
├── requirements.txt        # Python dependencies
├── test_scraper.py         # Basic test to verify setup
├── booli_scraper.py         # Main scraper with cookie handling
├── booli_cookies.json       # Saved session (auto-generated)
└── *.png                   # Screenshots (auto-generated)
```

## Customizing the Scraper

### Extract Different Data

Edit the `scrape_homepage()` method in `booli_scraper.py`:

```python
# Example: Extract all links
links = self.page.locator('a').all()
for link in links:
    print(link.get_attribute('href'))
```

### Scrape Different Pages

Use the `scrape_custom()` method:

```python
scraper.scrape_custom('https://www.booli.se/some-page')
```

### Find the Right Selectors

Use Playwright's code generator to explore the site interactively:

```bash
playwright codegen https://www.booli.se
```

This opens a browser with inspector tools that generate code as you click elements.

## Configuration Options

In `booli_scraper.py`, you can configure:

```python
scraper = BoliScraper(
    headless=True,      # Hide browser window (False to see it)
    save_cookies=True   # Save session for reuse
)
```

## Tips

1. **First run**: Keep `headless=False` to see what's happening
2. **Cookie handling**: The scraper tries multiple Swedish patterns automatically
3. **Session reuse**: Cookies are saved to avoid accepting consent every time
4. **Debugging**: Use browser DevTools (F12) to inspect page structure
5. **Rate limiting**: Add delays between requests to be respectful

## Deactivating

When done, deactivate the virtual environment:

```bash
deactivate
```

## Dependencies

- `playwright` - Browser automation
- `beautifulsoup4` - HTML parsing (optional)
- `requests` - HTTP library (optional)
- `python-dotenv` - Environment variable management

See `requirements.txt` for versions.

## Legal Notice

This tool is for educational purposes. Always:
- Check the website's `robots.txt` file
- Review their terms of service
- Respect rate limits
- Use responsibly

## License

See LICENSE file for details.
