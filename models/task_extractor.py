import re

# Expand this list as needed
COMMON_VERBS = {
    "advises", "manages", "supports", "coaches", "leads", "performs",
    "conducts", "analyses", "analyzes", "develops", "coordinates",
    "monitors", "reviews", "prepares", "maintains", "implements",
    "improves", "executes", "delivers", "ensures", "validates",
    "oversees", "facilitates", "drives", "optimises", "optimizes",
    "plans", "organises", "organizes", "evaluates"
}


def extract_tasks(text):
    if not text:
        return []

    # Split on commas and "and"
    chunks = re.split(r",| and ", text, flags=re.IGNORECASE)

    tasks = []

    for chunk in chunks:
        chunk = chunk.strip()
        if len(chunk) < 5:
            continue

        # Get first word
        first_word = chunk.split()[0].lower()

        # Keep only if it starts with a known verb
        if first_word not in COMMON_VERBS:
            continue

        # Clean punctuation
        clean = chunk.rstrip(".;:").strip()

        # Capitalise
        clean = clean[0].upper() + clean[1:]

        tasks.append(clean)

    # Deduplicate while preserving order
    seen = set()
    clean_tasks = []
    for t in tasks:
        if t not in seen:
            seen.add(t)
            clean_tasks.append(t)

    return clean_tasks
