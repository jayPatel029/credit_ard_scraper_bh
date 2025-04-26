import os
import logging
import streamlit as st
from scrapper.reader_llm import scrape_with_ai, scrape_pdf_with_ai

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def isUrl(source: str) -> bool:
    return source.startswith("http://") or source.startswith("https://")

def run_scraper_from_text(source: str, progress = None):
    
    def show_progress(curr, total):
        if progress:
            progress.text(f"Scraping {curr}/{total}...")
    if isUrl(source):
        logger.info(f"Scraping URL: {source}")
        return scrape_with_ai(source, progress=show_progress)
    elif os.path.isfile(source):
        logger.info(f"Scraping PDF file path: {source}")
        return scrape_pdf_with_ai(source)
    else:
        logger.error(f"Invalid source: {source}")
        return None

def run_scraper_from_pdf_file(uploaded_file, progress = None):
    
    def show_progress(curr, total):
        if progress:
            progress.text(f"Scraping {curr}/{total}...")
    
    if uploaded_file is not None:
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        logger.info(f"Scraping uploaded PDF: {temp_path}")
        cards = scrape_pdf_with_ai(temp_path, progress=show_progress)

        os.remove(temp_path)
        return cards

def main():
    st.title("Credit Card Scraper App")

    st.header("Option 1: Enter URL or Local PDF Path")
    source = st.text_input("Enter URL or file path:")

    if source:
        progress_text = st.empty()
        with st.spinner("Scraping in progress... please wait"):
            cards = run_scraper_from_text(source, progress=progress_text)

        if cards:
            st.success(f"Found {len(cards)} cards.")
            st.json(cards)
        else:
            st.warning("No cards found or invalid source.")

    st.markdown("----")
    st.header("Option 2: Upload PDF file")
    uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_pdf is not None:
        progress_text = st.empty()
        with st.spinner("Reading and scraping uploaded PDF... please wait"):
            cards = run_scraper_from_pdf_file(uploaded_pdf, progress=progress_text)

        if cards:
            st.success(f"Found {len(cards)} cards from uploaded PDF.")
            st.json(cards)
        else:
            st.warning("No cards found in uploaded PDF.")

if __name__ == "__main__":
    main()
