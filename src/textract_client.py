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
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

def get_textract_client():
    print("KEY FOUND:", os.getenv("AWS_ACCESS_KEY_ID") is not None)
    print("REGION:", os.getenv("AWS_DEFAULT_REGION"))

    return boto3.client(
        "textract",
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

def analyze_invoice(file_bytes):
    client = get_textract_client()
    return client.analyze_expense(Document={"Bytes": file_bytes})