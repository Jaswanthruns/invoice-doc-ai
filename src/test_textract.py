from textract_client import analyze_invoice
from parser import parse_summary_fields, parse_line_items

file_path = "samples/invoices/sample1.pdf"

with open(file_path, "rb") as f:
    file_bytes = f.read()

response = analyze_invoice(file_bytes)

summary = parse_summary_fields(response)
line_items = parse_line_items(response)

print("\n===== INVOICE SUMMARY =====")
print(summary)

print("\n===== LINE ITEMS =====")
for item in line_items:
    print(item)