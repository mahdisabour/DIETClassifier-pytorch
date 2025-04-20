import requests
import pandas as pd
import numpy as np
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

BASE_URL = "http://localhost:8000/detect?input="


def to_persian_digits(text):
    persian_digits = {
        '0': '۰',
        '1': '۱',
        '2': '۲',
        '3': '۳',
        '4': '۴',
        '5': '۵',
        '6': '۶',
        '7': '۷',
        '8': '۸',
        '9': '۹'
    }
    
    return re.sub(r'[0-9]', lambda m: persian_digits[m.group()], text)
    

def get_entities_from_api(text: str):
    try:
        response = requests.get(BASE_URL + f'"{text}"')
        if response.status_code != 200:
            logging.warning(f"API call failed for: {text}")
            return [], "unknown"

        result = response.json()
        entities = [e["text"] for e in result.get("entities", [])]
        intent = result.get("intent", "unknown")
        return entities, intent
    except Exception as e:
        logging.error(f"Error during API call or response parsing: {e}")
        return [], "unknown"

def test_quality():
    df = pd.read_csv("./tests/quality/test_data.csv")

    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for idx, row in df.iterrows():
        text = row["text"]
        true_entity = row["entity"] if pd.notna(row["entity"]) else None
        true_entity = to_persian_digits(true_entity).strip() if true_entity else None

        predicted_entities, intent = get_entities_from_api(text)
        predicted_entities = [to_persian_digits(e).strip() for e in predicted_entities]

        if intent == "normal":
            if true_entity is None and not predicted_entities:
                # Correctly predicted normal text — count as true positive
                true_positives += 1
            elif true_entity is not None:
                # Missed entity (should have been anonymizing)
                print("false negetive")
                print(f"{text=}", f"{true_entity=}", f"{predicted_entities=}")
                print("=====================================")
                false_negatives += 1
            else:
                # False positive: predicted intent normal but entity was found
                print("false positive")
                print(f"{text=}", f"{true_entity=}", f"{predicted_entities=}")
                print("=====================================")
                false_positives += len(predicted_entities)
        else:  # intent is anonymizing
            if true_entity:
                if [True for _pred in predicted_entities if true_entity in _pred]:
                    true_positives += 1
                else:
                    print("false negative")
                    print(f"{text=}", f"{true_entity=}", f"{predicted_entities=}")
                    print("=====================================")
                    false_negatives += 1
            else:
                # No entity expected, but got predictions
                false_positives += len(predicted_entities)
                print("false positive")
                print(f"{text=}", f"{true_entity=}", f"{predicted_entities=}")
                print("=====================================")

    # Final metrics
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) else 0

    print(f"\n✅ Evaluation Complete:")
    print(f"True Positives: {true_positives}")
    print(f"False Positives: {false_positives}")
    print(f"False Negatives: {false_negatives}")
    print(f"\nPrecision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1-score: {f1:.2f}")