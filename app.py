import streamlit as st
import pandas as pd

from src.textract_client import analyze_invoice
from src.parser import parse_summary_fields, parse_line_items

st.set_page_config(page_title="Invoice AI", layout="wide")

st.title("Invoice Processing AI")
st.write("Upload an invoice and extract structured data using AWS Textract")

uploaded_file = st.file_uploader("Upload Invoice", type=["pdf", "png", "jpg", "jpeg", "tiff", "tif"])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()

    with st.spinner("Processing invoice..."):
        response = analyze_invoice(file_bytes)

        summary = parse_summary_fields(response)
        line_items = parse_line_items(response)

    st.subheader("Invoice Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Vendor", summary.get("vendor_name") or "N/A")
    col2.metric("Invoice Number", summary.get("invoice_number") or "N/A")
    col3.metric("Invoice Date", summary.get("invoice_date") or "N/A")

    col4, col5, col6 = st.columns(3)
    col4.metric("Due Date", summary.get("due_date") or "N/A")
    col5.metric("Total", summary.get("total_amount") or "N/A")
    col6.metric("Tax", summary.get("tax_amount") or "N/A")

    st.subheader("Line Items")

    if line_items:
        df = pd.DataFrame(line_items)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No line items found")