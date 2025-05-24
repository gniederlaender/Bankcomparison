from scraper import AustrianBankScraper

def main():
    # Create an instance of the scraper
    scraper = AustrianBankScraper()
    
    # Generate the comparison HTML using existing data
    scraper.generate_comparison_html()
    
    print("Bank comparison HTML file has been generated successfully!")

if __name__ == "__main__":
    main() 