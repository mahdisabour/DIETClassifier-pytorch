

def convert_diet_result(data: dict) -> dict:
    entity_map = {}
    anon_text = data["text"]
    entities = sorted(data["entities"], key=lambda e: e["start"], reverse=True)

    counters = {}
    for entity in entities:
        name = entity["entity_name"]
        text = entity["text"]

        # Keep count for same entity types
        counters[name] = counters.get(name, 0) + 1
        key = f"{name}_{counters[name]}"

        # Store in entity_map
        entity_map[key] = text

        # Replace the original text with the key in the anonymized text
        anon_text = anon_text[:entity["start"]] + key + anon_text[entity["end"]:]

    return {
        "intent": data["intent"],
        "text": data["text"],
        "anonymized_text": anon_text,
        "entity_mapping": entity_map
    }
