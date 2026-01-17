#!/usr/bin/env python3
"""
Booli.se Web Scraper
A Playwright-based scraper for extracting data from booli.se
Handles cookie consent and saves session state for reuse.
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import json
import sys
from pathlib import Path
from datetime import datetime


class BoliScraper:
    """Web scraper for booli.se with cookie handling"""

    def __init__(self, headless=False, save_cookies=True):
        """
        Initialize the scraper

        Args:
            headless: Run browser in headless mode (default: False for debugging)
            save_cookies: Save and reuse cookies (default: True)
        """
        self.headless = headless
        self.save_cookies = save_cookies
        self.cookies_file = Path("booli_cookies.json")
        self.browser = None
        self.context = None
        self.page = None

    def start_browser(self, playwright):
        """Launch browser and create context"""
        print("Launching browser...")
        self.browser = playwright.chromium.launch(headless=self.headless)

        # Load saved cookies if they exist
        if self.save_cookies and self.cookies_file.exists():
            print(f"Loading saved cookies from {self.cookies_file}")
            self.context = self.browser.new_context(
                storage_state=str(self.cookies_file)
            )
        else:
            print("Creating new browser context...")
            self.context = self.browser.new_context(
                # Use realistic browser settings
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )

        self.page = self.context.new_page()

    def handle_cookie_consent(self):
        """
        Handle the EU cookie consent dialog
        Tries multiple common Swedish cookie button patterns
        """
        print("Checking for cookie consent dialog...")

        # Common Swedish cookie consent button patterns
        cookie_selectors = [
            'button:has-text("Acceptera")',
            'button:has-text("Godkänn")',
            'button:has-text("Acceptera alla")',
            'button:has-text("Godkänn alla")',
            'button:has-text("Jag förstår")',
            'button:has-text("OK")',
            '[id*="cookie-accept"]',
            '[class*="cookie-accept"]',
            '.cookie-banner button',
            '#cookie-consent button',
        ]

        for selector in cookie_selectors:
            try:
                # Wait max 2 seconds for each selector
                if self.page.locator(selector).is_visible(timeout=2000):
                    print(f"Found cookie button with selector: {selector}")
                    self.page.click(selector)
                    print("✓ Cookie consent accepted")
                    self.page.wait_for_timeout(1000)  # Wait for dialog to close
                    return True
            except PlaywrightTimeoutError:
                continue
            except Exception as e:
                print(f"  Selector '{selector}' failed: {e}")
                continue

        print("No cookie consent dialog found (may have been accepted previously)")
        return False

    def save_session(self):
        """Save cookies and session state for future use"""
        if self.save_cookies and self.context:
            print(f"Saving session to {self.cookies_file}")
            self.context.storage_state(path=str(self.cookies_file))
            print("✓ Session saved")

    def scrape_homepage(self):
        """
        Example: Scrape data from booli.se homepage
        Modify this method to extract the specific data you need
        """
        print("\n" + "=" * 50)
        print("Scraping booli.se homepage")
        print("=" * 50)

        # Navigate to booli.se
        print("Navigating to https://www.booli.se...")
        self.page.goto('https://www.booli.se', wait_until='domcontentloaded', timeout=60000)

        # Handle cookie consent
        self.handle_cookie_consent()

        # Get basic page info
        title = self.page.title()
        url = self.page.url
        print(f"\nPage Title: {title}")
        print(f"URL: {url}")

        # Example: Extract headings (modify based on what you want to scrape)
        print("\n--- Example Data Extraction ---")
        try:
            # This is just an example - you'll need to inspect booli.se
            # and update selectors for actual data you want
            headings = self.page.locator('h1, h2, h3').all_text_contents()
            print(f"Found {len(headings)} headings:")
            for i, heading in enumerate(headings[:5], 1):  # Show first 5
                print(f"  {i}. {heading.strip()}")

        except Exception as e:
            print(f"Error extracting data: {e}")

        # Take screenshot for verification
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"booli_scrape_{timestamp}.png"
        self.page.screenshot(path=screenshot_path, full_page=True)
        print(f"\n✓ Screenshot saved: {screenshot_path}")

        # Save session for next time
        self.save_session()

    def scrape_custom(self, url, extract_function=None):
        """
        Scrape a custom URL with an optional extraction function

        Args:
            url: The URL to scrape
            extract_function: Optional function(page) that extracts data
        """
        print(f"\nNavigating to {url}...")
        self.page.goto(url, wait_until='networkidle')
        self.handle_cookie_consent()

        if extract_function:
            return extract_function(self.page)

    def close(self):
        """Clean up and close browser"""
        if self.browser:
            self.browser.close()
            print("\n✓ Browser closed")


def main():
    """Main entry point"""
    print("=" * 50)
    print("Bolitha - Booli.se Web Scraper")
    print("=" * 50)
    print()

    try:
        scraper = BoliScraper(
            headless=False,  # Set to True to hide browser window
            save_cookies=True
        )

        with sync_playwright() as playwright:
            scraper.start_browser(playwright)

            # Run the homepage scraper
            scraper.scrape_homepage()

            # Keep browser open for a bit so you can inspect
            print("\nBrowser will close in 5 seconds...")
            scraper.page.wait_for_timeout(5000)

            scraper.close()

        print("\n" + "=" * 50)
        print("Scraping completed successfully!")
        print("=" * 50)
        print()
        print("Next steps:")
        print("1. Inspect the screenshots to see what was captured")
        print("2. Modify scrape_homepage() to extract your desired data")
        print("3. Use browser DevTools (F12) to find the right selectors")
        print()

    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
