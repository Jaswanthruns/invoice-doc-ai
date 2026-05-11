import os
import json
import pandas as pd
from datetime import datetime

OUTPUT_DIR = "data/extracted"
CSV_PATH = "data/extracted/invoice_history.csv"


def save_invoice_result(summary, line_items):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    record = {
        "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "vendor_name": summary.get("vendor_name"),
        "invoice_number": summary.get("invoice_number"),
        "invoice_date": summary.get("invoice_date"),
        "due_date": summary.get("due_date"),
        "total_amount": summary.get("total_amount"),
        "tax_amount": summary.get("tax_amount"),
        "line_item_count": len(line_items),
    }

    json_record = record.copy()
    json_record["line_items"] = line_items

    json_path = f"{OUTPUT_DIR}/invoice_{timestamp}.json"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_record, f, indent=4)

    new_df = pd.DataFrame([record])

    if os.path.exists(CSV_PATH):
        old_df = pd.read_csv(CSV_PATH)
        combined_df = pd.concat([old_df, new_df], ignore_index=True)
        combined_df.to_csv(CSV_PATH, index=False)
    else:
        new_df.to_csv(CSV_PATH, index=False)

    return json_path


def load_invoice_history():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    return pd.DataFrame()