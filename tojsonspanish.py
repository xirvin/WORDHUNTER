import json

def clean_word(word):
    word = word.strip().lower()
    return word if word.isalpha() else None

def generate_json(input_txt, output_json):
    with open(input_txt, "r", encoding="utf-8") as f:
        text = f.read()

    # Split on commas instead of newlines
    raw_words = text.split(',')

    words_clean = set()
    for word in raw_words:
        cleaned = clean_word(word)
        if cleaned:
            words_clean.add(cleaned)

    # Group words by their length
    words_by_length = {}
    for word in words_clean:
        length = len(word)
        if length not in words_by_length:
            words_by_length[length] = []
        words_by_length[length].append(word)

    # Sort words alphabetically in each group
    for length in words_by_length:
        words_by_length[length].sort()

    # Save to JSON file
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(words_by_length, f, indent=2, ensure_ascii=False)

    print(f"✅ Processed {len(words_clean)} unique words.")
    print(f"📁 JSON saved to: {output_json}")

if __name__ == "__main__":
    generate_json("Spanish.txt", "spanish_words.json")
