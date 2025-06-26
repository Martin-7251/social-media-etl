import re
import json
import argparse

def clean_mongo_extended_json(raw_text):
    # Replace MongoDB-specific wrappers
    raw_text = re.sub(r'ObjectId\("([^"]+)"\)', r'"\1"', raw_text)
    raw_text = re.sub(r'NumberInt\((\d+)\)', r'\1', raw_text)
    raw_text = re.sub(r'NumberLong\((\d+)\)', r'\1', raw_text)

    # Quote unquoted field names
    raw_text = re.sub(r'(?<=\{|,)\s*([a-zA-Z_][\w]*)\s*:', r'"\1":', raw_text)

    # Extract all JSON-like objects
    objects = re.findall(r'\{[\s\S]*?\}(?=\s*\{|\s*$)', raw_text)
    return objects

def main(input_path, output_path):
    print(f"📂 Reading: {input_path}")
    with open(input_path, "r", encoding="utf-8") as infile:
        raw = infile.read()

    objects = clean_mongo_extended_json(raw)
    print(f"🔍 Found {len(objects)} top-level JSON objects.")

    valid_objects = []
    skipped = 0

    for i, obj in enumerate(objects):
        try:
            parsed = json.loads(obj)
            valid_objects.append(parsed)
        except json.JSONDecodeError as e:
            print(f"⚠️ Skipped object {i+1}: {e}")
            skipped += 1

    if valid_objects:
        with open(output_path, "w", encoding="utf-8") as outfile:
            json.dump(valid_objects, outfile, indent=2)
        print(f"✅ Saved {len(valid_objects)} clean records to: {output_path}")
        print(f"🚫 Skipped {skipped} invalid records")
    else:
        print("❌ No valid records found. Nothing was written.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean Mongo shell-style JSON to valid JSON array.")
    parser.add_argument("input", help="Path to input JSON file")
    parser.add_argument("output", help="Path to output cleaned JSON file")
    args = parser.parse_args()
    main(args.input, args.output)
