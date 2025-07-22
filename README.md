# global-commodity-price-scraper-python
"Automated Python web scraper using Selenium to extract 983K+ global commodity price records from 𝐝𝐚𝐢𝐥𝐲𝐦𝐞𝐭𝐚𝐥𝐩𝐫𝐢𝐜𝐞.𝐜𝐨𝐦 (2011-2025). Deployed on Azure for monthly automated data updates across multiple currencies."
<br>


## 3. README.md File Content:

```markdown
# Global Commodity Price Data Scraper

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Selenium](https://img.shields.io/badge/Selenium-4.x-red.svg)
![Azure](https://img.shields.io/badge/Azure-Cloud-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-1.x-lightgrey.svg)

## Project Overview

This repository contains a robust and automated web scraping solution developed in Python to extract comprehensive global commodity price data from `dailymetalprice.com`. The system is designed to efficiently collect over 983,176 price records spanning from 2011 to 2025, covering multiple commodities across various currencies (USD, GBP, AUD, CNY, BTC, EUR).

## Key Features

-   **High-Volume Data Extraction:** Successfully scraped 983K+ records from 2011-2025.
-   **Multi-Currency Support:** Extracts prices in USD, GBP, AUD, CNY, BTC, and EUR.
-   **Selenium-Powered Navigation:** Utilizes Selenium for robust browser automation, handling JavaScript-heavy pages and dynamic content.
-   **Azure Cloud Deployment:** Deployed on Microsoft Azure for automated monthly data updates.
-   **Comprehensive Data Fields:** Extracts Date, Commodity, Price, Currency, and Unit information.
-   **Structured Data Output:** Delivers clean, organized data in Excel format, ready for analysis.
-   **Automated Scheduling:** Runs monthly without manual intervention to ensure data freshness.

## Technologies Used

-   **Python 3.x**
-   **Selenium 4.x**
-   **Pandas** (for data processing and structuring)
-   **Microsoft Azure** (for cloud deployment and automation)
-   **GeckoDriver** (for Firefox automation)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/hajra-wajid/global-commodity-price-scraper-python.git
    cd global-commodity-price-scraper-python
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

    _Note: A `requirements.txt` file will be provided in the actual repository containing `selenium`, `pandas`, and other required packages._

4.  **Download GeckoDriver:**
    Ensure you have `geckodriver.exe` (or appropriate for your OS) in your system PATH or specify its location in the script. This is required for Selenium to control Firefox.

## Usage

### Step 1: Extract Date Links
First, run the date link extraction script to collect all available date URLs:
```bash
python extract_date_links.py
```

### Step 2: Extract Commodity Price Data
Then, run the main scraper to extract price data for all currencies:
```bash
python extract_commodity_prices.py
```

## Data Output

The extracted data will be saved in `metal_prices_data.xlsx` with the following columns:

-   `Date` - The date of the price record
-   `Currency` - Currency code (USD, GBP, AUD, CNY, BTC, EUR)
-   `Commodity` - Name of the commodity (Gold, Silver, Copper, etc.)
-   `Price` - Price value in the specified currency
-   `Unit` - Unit of measurement (lb, oz, etc.)

## Azure Deployment

This system is deployed on Microsoft Azure and configured to run automatically on a monthly basis, ensuring continuous data updates without manual intervention.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## Contact

For any questions or collaborations, feel free to reach out:

-   **Upwork Profile:** [https://www.upwork.com/freelancers/hajrawajid?mp_source=share](https://www.upwork.com/freelancers/hajrawajid?mp_source=share)
-   **GitHub Profile:** [https://github.com/hajra-wajid](https://github.com/hajra-wajid)

```
