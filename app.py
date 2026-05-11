import streamlit as st
import pandas as pd
import re

from src.textract_client import analyze_invoice
from src.parser import parse_summary_fields, parse_line_items
from src.storage import save_invoice_result, load_invoice_history



# PAGE CONFIG

st.set_page_config(
    page_title="Invoice Processing AI",
    layout="wide"
)



# HELPER FUNCTIONS
def clean_money(value):
    """
    Convert currency-like text such as '$1,234.50' into float.
    Returns None if conversion fails.
    """
    if value is None:
        return None

    cleaned = re.sub(r"[^0-9.]", "", str(value))

    try:
        return float(cleaned)
    except ValueError:
        return None


def show_invoice_summary(summary):
    """
    Display extracted invoice summary fields in a clean metric layout.
    """
    st.subheader("Extracted Invoice Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Vendor", summary.get("vendor_name") or "N/A")
    col2.metric("Invoice Number", summary.get("invoice_number") or "N/A")
    col3.metric("Invoice Date", summary.get("invoice_date") or "N/A")

    col4, col5, col6 = st.columns(3)
    col4.metric("Due Date", summary.get("due_date") or "N/A")
    col5.metric("Total", summary.get("total_amount") or "N/A")
    col6.metric("Tax", summary.get("tax_amount") or "N/A")


def show_line_items(line_items):
    """
    Display extracted line items clearly.
    """
    st.subheader("Extracted Line Items")

    if not line_items:
        st.info("No line items detected for this invoice.")
        return

    line_df = pd.DataFrame(line_items)

    preferred_columns = [
        "raw_description",
        "clean_description",
        "quantity",
        "unit_price",
        "amount",
    ]

    available_columns = [col for col in preferred_columns if col in line_df.columns]
    remaining_columns = [col for col in line_df.columns if col not in available_columns]

    line_df = line_df[available_columns + remaining_columns]

    st.dataframe(line_df, use_container_width=True)


def show_history_dashboard():
    """
    Display saved invoice analytics and history only inside the History tab.
    """
    history_df = load_invoice_history()

    if history_df.empty:
        st.info("No saved invoices yet. Process an invoice and click 'Save Result' to build history.")
        return

    history_df["numeric_total"] = history_df["total_amount"].apply(clean_money)

    st.subheader("Analytics Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Invoices Saved", len(history_df))
    col2.metric("Unique Vendors", history_df["vendor_name"].nunique(dropna=True))
    col3.metric("Total Invoice Value", f"${history_df['numeric_total'].sum():,.2f}")
    col4.metric("Average Invoice Value", f"${history_df['numeric_total'].mean():,.2f}")

    st.divider()

    st.subheader("Saved Invoice History")

    display_columns = [
        "processed_at",
        "vendor_name",
        "invoice_number",
        "invoice_date",
        "due_date",
        "total_amount",
        "tax_amount",
        "line_item_count",
    ]

    available_columns = [col for col in display_columns if col in history_df.columns]

    st.dataframe(
        history_df[available_columns],
        use_container_width=True,
        hide_index=True
    )

    csv_data = history_df[available_columns].to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Invoice History as CSV",
        data=csv_data,
        file_name="invoice_history.csv",
        mime="text/csv"
    )



# HEADER
st.title("Invoice Processing AI")
st.write(
    "Upload an invoice and extract structured fields using AWS Textract. "
    "The app converts invoice PDFs/images into structured data for review and analytics."
)

st.divider()


# TABS
tab_process, tab_history, tab_about = st.tabs(
    ["Process Invoice", "History", "About The App"]
)



# TAB 1: PROCESS INVOICE
with tab_process:
    st.header("Process a New Invoice")

    uploaded_file = st.file_uploader(
        "Upload Invoice",
        type=["pdf", "png", "jpg", "jpeg"],
        help="Upload a PDF or image invoice to extract structured fields."
    )

    if uploaded_file is None:
        st.info("Upload an invoice to begin extraction.")
    else:
        st.write(f"Selected file: **{uploaded_file.name}**")

        process_button = st.button("Proceed", type="primary")

        if process_button:
            file_bytes = uploaded_file.read()

            try:
                with st.spinner("Processing invoice with AWS Textract..."):
                    response = analyze_invoice(file_bytes)
                    summary = parse_summary_fields(response)
                    line_items = parse_line_items(response)

                st.success("Invoice processed successfully.")

                show_invoice_summary(summary)

                st.divider()

                show_line_items(line_items)

                st.divider()

                st.subheader("Save Current Result")

                st.warning(
                    "This result is not saved yet. Click the button below if you want "
                    "to add it to the invoice history and analytics dashboard."
                )

                if st.button("Save Result to History"):
                    saved_path = save_invoice_result(summary, line_items)
                    st.success(f"Saved successfully: {saved_path}")

            except Exception as e:
                st.error("Something went wrong while processing the invoice.")
                st.code(str(e))



# TAB 2: HISTORY & ANALYTICS
with tab_history:
    st.header("Saved Invoice History & Analytics")
    st.write(
        "This section only shows invoices that were saved after processing. "
        "Freshly uploaded invoices will not appear here unless you click 'Save Result to History'."
    )

    show_history_dashboard()



# TAB 3: ABOUT PROJECT
with tab_about:
    st.header("Application Overview")

    st.markdown(
        """
        This project demonstrates an end-to-end Document AI workflow:

        1. Upload invoice PDF/image  
        2. Send document to AWS Textract  
        3. Extract summary fields and line items  
        4. Clean and structure noisy OCR output  
        5. Save processed results  
        6. Display invoice history and analytics  

        **Tech stack:** Python, AWS Textract, Boto3, Streamlit, Pandas, GitHub, Streamlit Cloud.
        """
    )

    st.subheader("Why this project matters")

    st.write(
        "Manual invoice entry is repetitive and error-prone. This app shows how document AI "
        "can automate invoice extraction and convert unstructured documents into structured, "
        "analytics-ready data."
    )