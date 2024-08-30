from playwright.sync_api import sync_playwright

def scrape_hotel_links(search_text):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.google.com/maps", timeout=60000)

        page.wait_for_selector('//input[@id="searchboxinput"]', timeout=10000)
        page.locator('//input[@id="searchboxinput"]').fill(search_text)
        page.keyboard.press("Enter")

        page.wait_for_selector('//h1[text()="Results"]', timeout=10000)
        result_element = page.locator('//h1[text()="Results"]')
        pre_div = result_element.locator("..").locator('..').locator('..')
        for _ in range(10):
            next_div = pre_div.evaluate_handle(
                "el => el.nextElementSibling"
            )
            details =  page.evaluate('''
                (element) => {
                    const links = [];
                    element.querySelectorAll('div div a').forEach(a => {
                        links.push({
                            ariaLabel: a.getAttribute('aria-label'),
                        });
                    });
                    return links;
                }
            ''', next_div)
            print(details)
            pre_div = next_div

        page.wait_for_timeout(10000)
        browser.close()

        return None

# Example usage:
search_text = "food spots in Palachira"
hotels = scrape_hotel_links(search_text)

