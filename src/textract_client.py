
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
