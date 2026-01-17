#!/usr/bin/env python3
"""
Booli.se Property Listing Scraper
Searches for homes for sale in a specified town and saves results to markdown
"""

from playwright.sync_api import sync_playwright
import sys
from datetime import datetime
from pathlib import Path


def scrape_booli_listings(town_name):
    """
    Scrape property listings from booli.se for a given town

    Args:
        town_name: Name of the town/city to search for
    """
    # Create data directory if it doesn't exist
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)

    # Create filename from town name and timestamp
    safe_town = town_name.replace(' ', '_').lower()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = data_dir / f'booli_listings_{safe_town}_{timestamp}.md'

    print("=" * 60)
    print("Booli.se Property Listing Scraper")
    print("=" * 60)
    print(f"Town: {town_name}")
    print(f"Output file: {output_file}")
    print()

    with sync_playwright() as p:
        # Launch browser
        print("Launching browser...")
        browser = p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )

        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        page.set_default_timeout(60000)

        try:
            # Navigate to booli.se
            print("Navigating to booli.se...")
            page.goto('https://www.booli.se', wait_until='domcontentloaded', timeout=60000)
            page.wait_for_timeout(2000)

            # Handle cookie consent
            print("Handling cookie consent...")
            try:
                cookie_button = page.get_by_role('button', name='Acceptera nödvändiga')
                if cookie_button.is_visible(timeout=3000):
                    cookie_button.click()
                    page.wait_for_timeout(1500)
                    print("✓ Cookie consent accepted")
            except:
                print("✓ No cookie dialog (already accepted)")

            # Search for the town
            print(f"\nSearching for '{town_name}'...")
            search_field = page.locator('#area-search-field')
            search_field.click()
            search_field.fill(town_name)
            page.wait_for_timeout(2500)  # Wait for autocomplete suggestions

            # Click first suggestion to select it
            print("Selecting first suggestion...")
            suggestions = page.locator('#search-suggestions a, #search-suggestions button')
            if suggestions.count() > 0:
                suggestions.first.click()
                page.wait_for_timeout(1500)
            else:
                print("✗ No suggestions found for this town")
                browser.close()
                return

            # Click the search button
            print("Clicking 'Hitta bostäder' button...")
            search_button = page.get_by_role('button', name='Hitta bostäder')
            search_button.click()
            page.wait_for_timeout(5000)  # Wait for results to load

            current_url = page.url
            print(f"✓ Navigated to: {current_url}")

            # Extract all listings
            print("\nExtracting property listings...")
            listings = page.locator('a[href*="/annons/"]').all()

            if len(listings) == 0:
                print("✗ No listings found")
                browser.close()
                return

            print(f"✓ Found {len(listings)} listings")

            # Collect all listing data
            all_listings = []
            for i, listing in enumerate(listings):
                try:
                    text = listing.inner_text()
                    href = listing.get_attribute('href')
                    url = f"https://www.booli.se{href}"

                    all_listings.append({
                        'text': text,
                        'url': url
                    })
                    print(f"  Extracted listing {i+1}/{len(listings)}")
                except Exception as e:
                    print(f"  Warning: Could not extract listing {i+1}: {e}")

            # Generate markdown content
            print(f"\nGenerating markdown file...")
            markdown = generate_markdown(town_name, current_url, all_listings)

            # Save to file
            output_file.write_text(markdown, encoding='utf-8')

            print(f"✓ Saved {len(all_listings)} listings to {output_file}")
            print()

        except Exception as e:
            print(f"\n✗ Error occurred: {e}")
            browser.close()
            sys.exit(1)

        finally:
            browser.close()
            print("Browser closed")

    print()
    print("=" * 60)
    print("Scraping completed successfully!")
    print("=" * 60)
    print()


def generate_markdown(town_name, search_url, listings):
    """Generate markdown content from listings"""

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    md = f"""# Booli.se Property Listings - {town_name}

**Search Date:** {timestamp}
**Source URL:** [{search_url}]({search_url})
**Total Listings:** {len(listings)}

---

"""

    for i, listing in enumerate(listings, 1):
        text = listing['text']
        url = listing['url']

        # Parse the listing text to extract components
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        # Try to identify address (usually appears early and repeated)
        address = "Unknown"
        property_type = ""
        price = ""
        details = []

        for line in lines:
            if line.startswith('Spara '):
                # Address often follows "Spara"
                address = line.replace('Spara ', '')
            elif ' kr' in line and 'kr/mån' not in line:
                price = line
            elif '·' in line:
                # Property type line (e.g., "Lägenhet · Dragarbrunn · Uppsala")
                property_type = line
            elif line not in [address, price, property_type] and not line.startswith('Sön') and not line.startswith('Snart'):
                # Other details
                details.append(line)

        # Build the markdown entry
        md += f"## {i}. {address}\n\n"

        if property_type:
            md += f"**Type:** {property_type}  \n"

        if price:
            md += f"**Price:** {price}  \n"

        if details:
            md += f"**Details:** {' • '.join(details)}  \n"

        md += f"**URL:** [{url}]({url})  \n"
        md += "\n---\n\n"

    return md


if __name__ == "__main__":
    # Get town name from command line or prompt
    if len(sys.argv) > 1:
        town = sys.argv[1]
    else:
        town = input("Enter town/city name to search: ").strip()
        if not town:
            print("Error: Town name is required")
            sys.exit(1)

    scrape_booli_listings(town)
