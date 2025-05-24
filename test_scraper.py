import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
import os
import re

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def setup_selenium():
    """Set up Selenium WebDriver with appropriate options"""
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Try to use Chrome if available
    chromium_paths = [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',  # Default Chrome path
        r'C:\Users\gabor\AppData\Local\Chromium\Application\chrome.exe',  # Primary path
        r'C:\Program Files\Chromium\Application\chromium.exe',
        r'C:\Program Files (x86)\Chromium\Application\chromium.exe',
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
    ]
    for path in chromium_paths:
        if os.path.exists(path):
            options.binary_location = path
            logger.info(f"Using Chrome binary at: {path}")
            break
    else:
        logger.info("Using default Chrome binary.")

    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    return driver, wait

def parse_erstebank_text(text):
    """Parse the Erste Bank representative calculation text for relevant fields."""
    mapping = {
        'sollzinssatz': r'Sollzinsen:\s*</p></dt><dd[^>]*><strong[^>]*>([\d,]+)\s*%\s*\(Fix-Zinssatz\)',
        'effektiver_jahreszins': r'Effektiver Zinssatz:\s*</p></dt><dd[^>]*><strong[^>]*>([\d,]+)\s*%\s*pro Jahr',
        'nettokreditbetrag': r'Auszahlungsbetrag:\s*</p></dt><dd[^>]*><span[^>]*><span[^>]*>([\d,.]+)\s*EUR',
        'vertragslaufzeit': r'Laufzeit:\s*</p></dt><dd[^>]*><strong[^>]*>(\d+)\s*Monate',
        'gesamtbetrag': r'Kreditbetrag und Gesamtkosten:\s*</p></dt><dd[^>]*><span[^>]*><span[^>]*>([\d,.]+)\s*EUR',
        'monatliche_rate': r'Monatliche Kreditrate:\s*</p></dt><dd[^>]*><span[^>]*><span[^>]*>([\d,.]+)\s*EUR'
    }
    
    result = {}
    for field, pattern in mapping.items():
        match = re.search(pattern, text)
        result[field] = match.group(1) if match else None
    
    return result

def scrape_page(url):
    """Scrape the entire HTML content of the given URL using Selenium"""
    driver, wait = setup_selenium()
    try:
        logger.info(f"Accessing URL: {url}")
        driver.get(url)
        
        # Wait for the page to load
        # time.sleep(2)  # Add a delay to let the page load completely
        
        # Handle cookie consent if present
        try:
            cookie_selectors = [
                (By.CSS_SELECTOR, "button#onetrust-accept-btn-handler"),
                (By.CSS_SELECTOR, "button.cookie-consent-accept"),
                (By.CSS_SELECTOR, "button[aria-label='Alle akzeptieren']"),
                (By.CSS_SELECTOR, "button[data-testid='uc-accept-all-button']"),
                (By.CSS_SELECTOR, "button.cookie-banner__accept-all"),
                (By.XPATH, "//button[contains(text(), 'Ich bin einverstanden')]")
            ]
            for by, selector in cookie_selectors:
                try:
                    cookie_button = wait.until(EC.element_to_be_clickable((by, selector)))
                    cookie_button.click()
                    logger.info("Cookie consent handled")
                    time.sleep(5)
                    break
                except:
                    continue
                    time.sleep(10)
        except Exception as e:
            logger.warning(f"Cookie consent handling failed: {str(e)}")
        
        # Get the entire page HTML
        content = driver.page_source
        
        # Save screenshot for debugging
        driver.save_screenshot('test_page.png')
        logger.info("Screenshot saved as test_page.png")
        
        return content
    except Exception as e:
        logger.error(f"Error scraping {url}: {str(e)}")
        try:
            driver.save_screenshot('error_page.png')
            logger.info("Error screenshot saved as error_page.png")
        except:
            pass
        return None
    finally:
        driver.quit()

def main():
    url = 'https://www.sparkasse.at/erstebank/privatkunden/wohnen-finanzieren/konsumfinanzierung/konsumkredit'
    content = scrape_page(url)
    
    if content:
        print("\n--- Raw Extracted HTML ---\n")
        print(content)
        # Write the HTML content to test.txt
        with open('test.txt', 'w', encoding='utf-8') as f:
            f.write(content)
        print("\nHTML content written to test.txt\n")
    else:
        logger.error("No content to write")

if __name__ == "__main__":
    main() 