from playwright.sync_api import sync_playwright
import time

GOOGLE_MAP_BASE_URL = "https://www.google.com/maps"

def scrape_all_info(search_query:str)->None:
    """
    Scrape all info and save it as html
    """
    with sync_playwright() as playwright:
        with playwright.chromium.launch(headless=False) as browser:
            context = browser.new_context(java_script_enabled=True)
            page = context.new_page()
            page.goto(GOOGLE_MAP_BASE_URL, wait_until="load")

            page.wait_for_selector('//input[@id="searchboxinput"]', timeout=5000)
            page.locator('//input[@id="searchboxinput"]').fill(search_query)
            page.keyboard.press("Enter")

            x_path_search_result_element = '//div[@role="feed"]'
            page.wait_for_selector(x_path_search_result_element, timeout=5000)
            results_container = page.query_selector(x_path_search_result_element)
            results_container.scroll_into_view_if_needed()

            keep_scolling = True
            while keep_scolling:
                results_container.press('Space')
                time.sleep(2.5)

                if results_container.query_selector('//span[text()="You\'ve reached the end of the list."]'):
                    results_container.press('Space')
                    keep_scolling = False

                    html_filename = f'notebooks/htmls/{search_query.replace(" ", "_")}.html'
                    with open(html_filename, "w", encoding="utf-8") as file:
                        file.write(results_container.inner_html())
    
    return None

if __name__ == "__main__":

    search_query = "food spots in cherunniyoor"
    scrape_all_info(search_query)

