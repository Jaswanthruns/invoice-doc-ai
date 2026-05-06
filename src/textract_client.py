# import boto3
# import os
# from dotenv import load_dotenv

# load_dotenv()

# def get_textract_client():
#     return boto3.client(
#         "textract",
#         region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
#         aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
#         aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
#     )

# def analyze_invoice(file_bytes):
#     client = get_textract_client()
#     return client.analyze_expense(Document={"Bytes": file_bytes})

import boto3
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

def get_textract_client():
    return boto3.client(
        "textract",
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

def analyze_invoice(file_bytes):
    client = get_textract_client()
    return client.analyze_expense(Document={"Bytes": file_bytes})

# import boto3
# import os
# import streamlit as st
# from dotenv import load_dotenv

# load_dotenv(dotenv_path=".env")

# def get_textract_client():
#     try:
#         aws_access_key = st.secrets.get("AWS_ACCESS_KEY_ID")
#         aws_secret_key = st.secrets.get("AWS_SECRET_ACCESS_KEY")
#         region = st.secrets.get("AWS_DEFAULT_REGION", "us-east-1")
#     except Exception:
#         aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
#         aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
#         region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

#     return boto3.client(
#         "textract",
#         region_name=region,
#         aws_access_key_id=aws_access_key,
#         aws_secret_access_key=aws_secret_key
#     )

# def analyze_invoice(file_bytes):
#     client = get_textract_client()
#     return client.analyze_expense(Document={"Bytes": file_bytes})