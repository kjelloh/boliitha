#!/usr/bin/env python3
"""
Test Scraper - Verify Playwright setup and basic access to booli.se
This script opens booli.se, takes a screenshot, and prints basic page info.
"""

from playwright.sync_api import sync_playwright
import sys


def test_boli_access():
    """Test basic access to booli.se"""
    print("=" * 50)
    print("Bolitha - Test Scraper")
    print("=" * 50)
    print()

    try:
        with sync_playwright() as p:
            print("Launching browser...")
            # Launch browser with anti-detection settings
            browser = p.chromium.launch(
                headless=False,
                args=['--disable-blink-features=AutomationControlled']
            )

            print("Creating new page...")
            # Create context with realistic settings
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
            )
            page = context.new_page()
            page.set_default_timeout(60000)

            print("Navigating to booli.se...")
            # Use 'domcontentloaded' which is less strict than 'networkidle'
            page.goto('https://www.booli.se', wait_until='domcontentloaded', timeout=60000)

            # Get page title
            title = page.title()
            print(f"✓ Page loaded successfully!")
            print(f"  Title: {title}")
            print(f"  URL: {page.url}")

            # Take screenshot
            screenshot_path = 'booli_test_screenshot.png'
            page.screenshot(path=screenshot_path)
            print(f"✓ Screenshot saved to: {screenshot_path}")

            # Wait a bit so you can see the page
            print("\nBrowser will close in 3 seconds...")
            page.wait_for_timeout(3000)

            browser.close()
            print("\n✓ Test completed successfully!")
            print()
            print("Next step: Run 'python booli_scraper.py' to start scraping")
            print()

    except Exception as e:
        print(f"\n✗ Error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    test_boli_access()
