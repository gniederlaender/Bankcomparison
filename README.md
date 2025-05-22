# Austrian Bank Interest Rate Scraper

A Python-based scraper that collects and compares interest rates from major Austrian banks.

## Features

- Scrapes interest rates from multiple Austrian banks:
  - Erste Bank
  - Raiffeisen
  - BAWAG
  - Bank99
- Stores data in SQLite database
- Exports data to Excel
- Generates HTML comparison table
- Configurable scraping for each bank

## Requirements

- Python 3.8+
- Chrome/Chromium browser

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gniederlaender/Bankcomparison.git
cd Bankcomparison
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the scraper:
```bash
python scraper.py
```

The script will:
1. Scrape interest rates from enabled banks
2. Store the data in `austrian_banks.db`
3. Export data to `austrian_banks_data.xlsx`
4. Generate a comparison table in `bank_comparison.html`

## Configuration

You can enable/disable scraping for specific banks by modifying the `enable_scraping` dictionary in `scraper.py`:

```python
self.enable_scraping = {
    'raiffeisen': True,
    'bawag': True,
    'bank99': True,
    'erste': True
}
```

## Output Files

- `austrian_banks.db`: SQLite database with all scraped data
- `austrian_banks_data.xlsx`: Excel file with the latest data
- `bank_comparison.html`: HTML table comparing rates from all banks
- `scraper.log`: Log file with scraping operations

## Data Structure

The scraper stores data in three main tables:

1. `interest_rates`:
   - Bank name
   - Product name
   - Interest rate
   - Currency
   - Date scraped
   - Source URL

2. `fees`:
   - Bank name
   - Service name
   - Fee amount
   - Currency
   - Date scraped
   - Source URL

3. `offers`:
   - Bank name
   - Offer name
   - Description
   - Valid until date
   - Date scraped
   - Source URL

## Customization

To add more banks or modify existing ones, edit the `banks` dictionary in `scraper.py`. Each bank entry should include:
- Main URL
- Interest rates URL
- Fees URL
- Offers URL

## Legal Notice

Before using this scraper, please ensure you:
1. Review and comply with each bank's terms of service
2. Check robots.txt files
3. Implement appropriate delays between requests
4. Consider reaching out to banks for official API access

## Contributing

Feel free to submit issues and enhancement requests! 