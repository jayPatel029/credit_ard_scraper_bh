import requests
import textwrap
from groq import Groq
from typing import List, Dict
from dotenv import load_dotenv
import os
from scrapper.utils import save_to_json
from scrapper.utils import extract_text_from_pdf
import logging
from datetime import datetime
from scrapper.card_parser import normalize_card_data, extract_fields


logger = logging.getLogger(__name__)

load_dotenv()
client = Groq(api_key=os.getenv("groc_api_key"))

def chunk_text(text, max_chars=3000) -> List[str]:
    return textwrap.wrap(text, max_chars)


def scrape_with_ai(url: str, progress = None) -> List[Dict]:
    reader_url = f"https://r.jina.ai/{url}"

    try:
        response = requests.get(reader_url)
        if response.status_code != 200:
            logger.error("Reader API failed.")
            return []

        raw_text = response.text
        chunks = chunk_text(raw_text)
        all_cards = []
        
        for i, chunk in enumerate(chunks):
            logger.info(f"Scraping {i+1}/{len(chunks)}")
            progress(i+1,len(chunks)) if progress else None
            cards = call_groq(chunk=chunk, context_url=url)
            all_cards.extend(cards)
            
        if all_cards:
            all_cards = normalize_card_data(all_cards)
            json_name = f"urlCards{datetime.now().strftime('%d_%H%M')}"
            save_to_json(all_cards, f"outputs/{json_name}.json")
            logger.info(f"Saved JSON file at outputs/{json_name}.json")
        else:
            logger.info("No valid cards found.")
        return all_cards

    except Exception as e:
        logger.exception(f"scraping error: {e}")
        return []



def scrape_pdf_with_ai(pdf_path: str, progress = None) -> List[Dict]:
    try:
        raw_text = extract_text_from_pdf(pdf_path)
        if not raw_text:
            logger.info("No text extracted from PDF.")
            return []

        chunks = chunk_text(raw_text)
        all_cards = []
        url_source = f"file://{os.path.basename(pdf_path)}"


        for i, chunk in enumerate(chunks):
            logger.info(f"Scraping {i+1}/{len(chunks)}")
            progress(i+1, len(chunks)) if progress else None
            cards = call_groq(chunk=chunk, context_url=url_source)
            all_cards.extend(cards)

        if all_cards:
            all_cards = normalize_card_data(all_cards)
            json_name = f"pdfCards_{datetime.now().strftime('%d_%H%M')}"
            save_to_json(all_cards, f"outputs/{json_name}.json")
            logger.info(f"Saved JSON file at outputs/{json_name}.json")
        else:
            logger.info("No valid cards found in pdf")
        return all_cards

    except Exception as e:
        logger.exception(f"PDF processing error: {e}")
        return []


def call_groq(chunk:str, context_url:str) -> List[Dict[str,str]]:
    try:
        chat_completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Source: {context_url}\n\n{chunk}"}
            ],
            temperature=0.3,
            max_completion_tokens=1024,
            response_format={"type": "text"}
        )
        content = chat_completion.choices[0].message.content.strip()
        return [extract_fields(block, context_url) for block in content.split("\n\n")]

    except Exception as e:
        logger.exception(f"groq call failed for chunk: {e}")
        return []


system_prompt = """
You are a credit card data extraction assistant.

Extract credit card details from the following text and return each card using this format:

Card Name: ...
Bank: ...
Joining Fee: ...
Annual Fee: ...
Rewards: ...
Cashback: ...
Other Features: ...

Use 'N/A' if any detail is missing. Don't return explanations. Just list cards, each as a block of key-value lines.
"""
