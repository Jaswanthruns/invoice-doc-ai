def parse_summary_fields(response):
    result = {
        "vendor_name": None,
        "invoice_number": None,
        "invoice_date": None,
        "due_date": None,
        "total_amount": None,
        "tax_amount": None,
    }

    expense_docs = response.get("ExpenseDocuments", [])
    if not expense_docs:
        return result

    fields = expense_docs[0].get("SummaryFields", [])

    for field in fields:
        field_type = field.get("Type", {}).get("Text")
        field_value = field.get("ValueDetection", {}).get("Text")

        if field_type == "VENDOR_NAME":
            result["vendor_name"] = field_value
        elif field_type == "INVOICE_RECEIPT_ID":
            result["invoice_number"] = field_value
        elif field_type == "INVOICE_RECEIPT_DATE":
            result["invoice_date"] = field_value
        elif field_type == "DUE_DATE":
            result["due_date"] = field_value
        elif field_type == "TOTAL":
            result["total_amount"] = field_value
        elif field_type == "TAX":
            result["tax_amount"] = field_value

    return result


def parse_line_items(response):
    items = []

    expense_docs = response.get("ExpenseDocuments", [])
    if not expense_docs:
        return items

    line_groups = expense_docs[0].get("LineItemGroups", [])

    for group in line_groups:
        for line_item in group.get("LineItems", []):
            item_data = {
                "description": None,
                "quantity": None,
                "price": None,
            }

            for field in line_item.get("LineItemExpenseFields", []):
                field_type = field.get("Type", {}).get("Text")
                field_value = field.get("ValueDetection", {}).get("Text")

                if field_type in ["ITEM", "EXPENSE_ROW"]:
                    item_data["description"] = field_value
                elif field_type == "QUANTITY":
                    item_data["quantity"] = field_value
                elif field_type == "PRICE":
                    item_data["price"] = field_value

            items.append(item_data)

    return items