
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains

def setup_driver():
    """Sets up the Firefox WebDriver."""
    options = webdriver.FirefoxOptions()
    # options.add_argument("--headless") # Uncomment for headless mode
    try:
        driver = webdriver.Firefox(options=options)
        return driver
    except WebDriverException as e:
        print(f"Error setting up WebDriver: {e}")
        print("Please ensure geckodriver is in the same directory as the script and is executable.")
        return None

def handle_ads_and_load(driver, url, wait_time=10, retries=3):
    """Navigates to a URL and handles potential ads by refreshing, with retries."""
    for attempt in range(retries):
        print(f"Navigating to {url} (Attempt {attempt + 1}/{retries})")
        driver.get(url)
        time.sleep(2) # Initial wait for page to start loading
        try:
            # Wait for the main accordion element to be present on the archive page
            WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.ID, "accordion"))
            )
            # Check for common ad indicators and refresh if found
            if "google-auto-placed" in driver.page_source or "adsbygoogle" in driver.page_source:
                print("Ad detected, refreshing page...")
                driver.refresh()
                WebDriverWait(driver, wait_time).until(
                    EC.presence_of_element_located((By.ID, "accordion"))
                )
            return True # Page loaded successfully
        except TimeoutException:
            print(f"Page load timed out for {url}. Retrying...")
        except Exception as e:
            print(f"An unexpected error occurred while loading {url}: {e}")
    print(f"Failed to load {url} after {retries} attempts.")
    return False

def main():
    driver = setup_driver()
    if not driver:
        return

    base_url = "https://www.dailymetalprice.com"
    archive_url = f"{base_url}/datearchive.php"
    output_excel_file = "date_links.xlsx"

    date_links = []

    try:
        if not handle_ads_and_load(driver, archive_url):
            print("Failed to load archive page. Exiting.")
            driver.quit()
            return

        print("Successfully loaded archive page.")

        # Extract date links for the years 2011 to 2025
        for year in range(2011, 2026): # Iterate from 2011 to 2025
            print(f"Processing year: {year}")
            try:
                # Locate the year link using a more robust XPath that includes text
                year_link_xpath = f"//div[@id=\'heading{year}\']/h4/a[contains(@href, \'#collapse{year}\')]"
                
                # Wait until the element is present
                year_link = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, year_link_xpath))
                )
                
                # Scroll element into view
                driver.execute_script("arguments[0].scrollIntoView(true);", year_link)
                time.sleep(0.5) # Small wait after scrolling

                # Wait until the element is visible
                WebDriverWait(driver, 10).until(
                    EC.visibility_of(year_link)
                )

                # Check if the year section is collapsed and click to expand if necessary
                collapse_id = f"collapse{year}"
                collapse_div = driver.find_element(By.ID, collapse_id)
                
                # If the collapse div is not visible, click the year link using JavaScript
                if not collapse_div.is_displayed():
                    print(f"  Expanding year {year} section...")
                    driver.execute_script("arguments[0].click();", year_link)
                    time.sleep(1) # Give time for the section to expand
                    # Wait until the collapse div is visible after clicking
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of(collapse_div)
                    )

                # Extract date links for the current year from the now visible panel-body
                date_elements = collapse_div.find_elements(By.TAG_NAME, "a")

                found_links_for_year = 0
                for date_elem in date_elements:
                    href = date_elem.get_attribute("href")
                    if href and "/metaltables.php?d=" in href:
                        date_links.append(href)
                        found_links_for_year += 1
                print(f"Found {found_links_for_year} date links for {year}.")

            except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
                print(f"Could not process year {year} (Error: {e}). Skipping to next year.")
                continue # Continue to the next year if elements are not found or click fails
            except Exception as e:
                print(f"An unexpected error occurred while processing year {year}: {e}")
                continue
        
        print(f"Total date links collected: {len(date_links)}")

        # Save date links to Excel
        df_date_links = pd.DataFrame({"Date_Link": date_links})
        df_date_links.to_excel(output_excel_file, index=False)
        print(f"Date links saved to {output_excel_file}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()


