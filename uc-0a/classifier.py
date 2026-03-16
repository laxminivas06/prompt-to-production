"""
UC-0A — Complaint Classifier
Simple rule-based implementation so the script runs on test_[city].csv without crashing.
"""

import argparse
import csv

SEVERITY_KEYWORDS = ["injury", "hospital", "child", "school"]

CATEGORY_KEYWORDS = {
    "roads": ["pothole", "road", "street", "asphalt"],
    "water": ["water", "pipe", "leak", "sewage"],
    "electricity": ["power", "electric", "wire", "transformer"],
    "garbage": ["garbage", "trash", "waste", "dump"],
}


def detect_category(text: str):
    text_lower = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for k in keywords:
            if k in text_lower:
                return category, f"keyword '{k}' detected"
    return "other", "no category keyword matched"


def detect_priority(text: str):
    text_lower = text.lower()
    for k in SEVERITY_KEYWORDS:
        if k in text_lower:
            return "Urgent", f"severity keyword '{k}' detected"
    return "Normal", "no severity signal"


def classify_complaint(row: dict) -> dict:
    """
    Classify a single complaint row.
    Returns: dict with keys: complaint_id, category, priority, reason, flag
    """

    complaint_id = row.get("complaint_id") or row.get("id") or "UNKNOWN"
    text = row.get("complaint") or row.get("description") or ""

    if text is None or text.strip() == "":
        return {
            "complaint_id": complaint_id,
            "category": "unknown",
            "priority": "unknown",
            "reason": "empty complaint text",
            "flag": "NULL_TEXT",
        }

    category, cat_reason = detect_category(text)
    priority, pri_reason = detect_priority(text)

    return {
        "complaint_id": complaint_id,
        "category": category,
        "priority": priority,
        "reason": f"{cat_reason}; {pri_reason}",
        "flag": "",
    }


def batch_classify(input_path: str, output_path: str):
    """
    Read input CSV, classify each row, write results CSV.
    Flags bad rows but does not crash.
    """

    results = []

    try:
        with open(input_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    result = classify_complaint(row)
                    results.append(result)
                except Exception as e:
                    results.append(
                        {
                            "complaint_id": row.get("complaint_id", "UNKNOWN"),
                            "category": "error",
                            "priority": "error",
                            "reason": str(e),
                            "flag": "ROW_ERROR",
                        }
                    )

    except FileNotFoundError:
        print("Input file not found.")
        return

    fieldnames = ["complaint_id", "category", "priority", "reason", "flag"]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UC-0A Complaint Classifier")
    parser.add_argument("--input", required=True, help="Path to test_[city].csv")
    parser.add_argument("--output", required=True, help="Path to write results CSV")

    args = parser.parse_args()

    batch_classify(args.input, args.output)

    print(f"Done. Results written to {args.output}")
