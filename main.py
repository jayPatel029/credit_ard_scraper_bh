# #link 1:  https://www.paisabazaar.com/credit-card/best-credit-cards-online-shopping/
# #link 2: https://cardinsider.com/best-credit-cards-in-india/


import os
import logging
from scrapper.reader_llm import scrape_with_ai, scrape_pdf_with_ai

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def isUrl(source: str) -> bool:
    return source.startswith("http://") or source.startswith("https://")

def run_scraper(source: str):
    if isUrl(source):
        logger.info(f"Scraping URL: {source}")
        cards = scrape_with_ai(source)
    elif os.path.isfile(source):
        logger.info(f"Scraping PDF: {source}")
        cards = scrape_pdf_with_ai(source)
    else:
        logger.error(f"Invalid source: {source}")
        return
    
    if not cards:
        logger.info("No cards found.")
        return

    logger.info(f"Found {len(cards)} cards.")

def main():
    source = input("Enter URL or PDF path to scrape: ").strip()
    run_scraper(source)

if __name__ == "__main__":
    main()
