import time
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import os
from urllib.parse import urlparse, parse_qs

def setup_driver():
    """Sets up the Firefox WebDriver with improved settings."""
    options = webdriver.FirefoxOptions()
    # options.add_argument("--headless")  # Uncomment for headless mode
    options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    try:
        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(45)
        driver.set_script_timeout(30)
        return driver
    except WebDriverException as e:
        print(f"Error setting up WebDriver: {e}")
        print("Please ensure geckodriver is in the same directory as the script and is executable.")
        return None

def handle_ads_and_load(driver, url, retries=3):
    """Navigates to a URL with robust ad handling and timeout management."""
    for attempt in range(retries):
        print(f"Loading URL (Attempt {attempt+1}/{retries}): {url}")
        try:
            driver.get(url)
            # Wait for either the table or currency dropdown to appear
            WebDriverWait(driver, 30).until(
                lambda d: d.find_element(By.CSS_SELECTOR, "table.table-striped") or 
                d.find_element(By.ID, "x")
            )
            return True
        except TimeoutException:
            print("Page load timed out. Refreshing...")
            driver.refresh()
        except Exception as e:
            print(f"Error loading page: {e}")
            if attempt < retries - 1:
                print("Refreshing and retrying...")
                driver.refresh()
                time.sleep(3)
    
    print(f"Failed to load {url} after {retries} attempts")
    return False

def extract_table_data(driver, date_str, currency):
    """Extracts data from the metal prices table with improved reliability."""
    data = []
    try:
        # Wait for table to be present
        table = WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "table.table-striped"))
        )
        
        # Wait for data rows to appear
        WebDriverWait(driver, 15).until(
            lambda d: len(table.find_elements(By.TAG_NAME, "tr")) > 1
        )
        
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows[1:]:  # Skip header row
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 4:
                continue
                
            commodity = cols[0].text.strip()
            price_text = cols[1].text.strip()
            unit = cols[2].text.strip()
            
            # Clean price text - remove any non-numeric except decimal point
            price_clean = re.sub(r'[^\d.]', '', price_text)
            try:
                price = float(price_clean) if price_clean else None
            except ValueError:
                price = None
            
            data.append({
                "Date": date_str,
                "Currency": currency,
                "Commodity": commodity,
                "Price": price,
                "Unit": unit
            })
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Table extraction error: {e}")
    except Exception as e:
        print(f"Unexpected error during extraction: {e}")
    return data

def save_to_excel(dataframe, filename="metal_prices_data.xlsx"):
    """Saves the DataFrame to an Excel file."""
    try:
        if not dataframe.empty:
            if os.path.exists(filename):
                existing_df = pd.read_excel(filename)
                combined_df = pd.concat([existing_df, dataframe], ignore_index=True)
                combined_df.to_excel(filename, index=False)
                print(f"Appended {len(dataframe)} records to {filename}")
            else:
                dataframe.to_excel(filename, index=False)
                print(f"Created new file with {len(dataframe)} records: {filename}")
        else:
            print("No data to save")
    except Exception as e:
        print(f"Error saving to Excel: {e}")

def change_currency(driver, currency):
    """Changes the currency selection with robust waiting and verification."""
    try:
        # Wait for dropdown to be interactive
        dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "x"))
        )
        select = Select(dropdown)
        
        # Get current selection
        current_currency = select.first_selected_option.get_attribute('value')
        
        if current_currency == currency:
            print(f"  {currency} already selected")
            return True
            
        print(f"  Changing to {currency}")
        select.select_by_value(currency)
        
        # Wait for changes to take effect - use multiple strategies
        time.sleep(2)  # Brief pause for JavaScript execution
        
        # Wait for spinner to disappear if present
        try:
            WebDriverWait(driver, 15).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "spinner")))
        except:
            pass
        
        # Verify currency changed by checking dropdown value
        WebDriverWait(driver, 15).until(
            lambda d: Select(d.find_element(By.ID, "x")).first_selected_option.get_attribute('value') == currency
        )
        
        print(f"  Currency changed to {currency}")
        return True
        
    except TimeoutException:
        print(f"  Timeout changing to {currency}")
    except NoSuchElementException:
        print("  Currency dropdown not found")
    except Exception as e:
        print(f"  Error changing currency: {e}")
    
    return False

def main():
    driver = setup_driver()
    if not driver:
        return

    date_links_file = "date_links.xlsx"
    output_data_file = "metal_prices_data.xlsx"
    currencies_to_scrape = ["USD", "GBP", "AUD", "CNY", "BTC", "EUR"]
    
    if not os.path.exists(date_links_file):
        print(f"Error: {date_links_file} not found. Run script1_extract_date_links.py first.")
        driver.quit()
        return

    df_links = pd.read_excel(date_links_file)
    date_links = df_links["Date_Link"].tolist()
    print(f"Loaded {len(date_links)} date links")

    # Create new Excel file if doesn't exist
    if not os.path.exists(output_data_file):
        pd.DataFrame().to_excel(output_data_file, index=False)

    for i, date_link in enumerate(date_links):
        print(f"\nProcessing URL {i+1}/{len(date_links)}: {date_link}")
        date_data = []  # Store all data for this date
        
        if not handle_ads_and_load(driver, date_link):
            print(f"Skipping {date_link}")
            continue
        
        # Extract date from URL
        parsed_url = urlparse(date_link)
        query_params = parse_qs(parsed_url.query)
        date_str = query_params.get('d', [''])[0] or parsed_url.path.split('/')[-1]
        
        for currency in currencies_to_scrape:
            print(f"  Processing currency: {currency}")
            
            # Try to change currency (will skip if already selected)
            if not change_currency(driver, currency):
                print(f"  Failed to select {currency}, skipping")
                continue
                
            # Add brief pause before extraction
            time.sleep(1.5)
            
            # Extract data for this currency
            currency_data = extract_table_data(driver, date_str, currency)
            if currency_data:
                date_data.extend(currency_data)
                print(f"    Extracted {len(currency_data)} records for {currency}")
            else:
                print(f"    No data found for {currency}")
        
        # Save all currency data for this date to Excel
        if date_data:
            df = pd.DataFrame(date_data)
            save_to_excel(df, output_data_file)
        else:
            print("  No data extracted for this date")
    
    driver.quit()
    print("\nScraping completed successfully!")

if __name__ == "__main__":
    main()