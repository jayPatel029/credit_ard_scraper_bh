from scrapper.utils import normalize_name, clean_fee, safe_get
from typing import List, Dict
from fuzzywuzzy import fuzz


def normalize_card_data(cards: List[Dict[str, str]], similarity_threshold=90) -> List[Dict[str, str]]:
    
    cleaned_cards = []

    # check: if all empty ignore the card
    fields_to_check = [
        "joining_fee", "annual_fee", "rewards", "cashback", "other_features"
    ]

    for card in cards:
        card_name = normalize_name(safe_get(card, "card_name"))
        bank = normalize_name(safe_get(card, "bank"))

        # no card_name ignore the card
        if not card_name or card_name == "n/a" or card_name == "N/A":
            continue

        
        empty_fields = sum(1 for field in fields_to_check if safe_get(card, field) in ["N/A", "n/a","", None])

        
        if empty_fields >= 5:
            continue

        # check for dupliate cards 
        found_similar = False
        for existing_card in cleaned_cards:
            existing_card_name = normalize_name(safe_get(existing_card, "card_name"))
            similarity_score = fuzz.ratio(card_name.lower(), existing_card_name.lower())
            if similarity_score >= similarity_threshold:
                found_similar = True
                break

        if not found_similar:
            cleaned_cards.append(card)

    return cleaned_cards



def extract_fields(content: str, url: str) -> Dict[str, str]:
    expected_fields = {
        "card_name": "Card Name",
        "bank": "Bank",
        "joining_fee": "Joining Fee",
        "annual_fee": "Annual Fee",
        "rewards": "Rewards",
        "cashback": "Cashback",
        "other_features": "Other Features",
        "source_url": "Source URL",
    }

    extracted = {key: "N/A" for key in expected_fields}
    extracted["source_url"] = url

    extras = {}

    for line in content.splitlines():
        if ": " in line:
            key_part, value = line.split(": ", 1)
            key_part_clean = key_part.strip().lower()
            value = value.strip()

            matched = False
            for internal_key, expected_label in expected_fields.items():
                if key_part_clean.startswith(expected_label.lower()):
                    extracted[internal_key] = value or "N/A"
                    matched = True
                    break

            if not matched:
                extras[key_part.strip()] = value


    extracted["joining_fee"] = clean_fee(extracted.get("joining_fee", "N/A"))
    extracted["annual_fee"] = clean_fee(extracted.get("annual_fee", "N/A"))
    extracted["card_name"] = safe_get(extracted, "card_name")
    extracted["bank"] = safe_get(extracted, "bank")

    if extras:
        extracted["extras"] = extras

    return extracted
