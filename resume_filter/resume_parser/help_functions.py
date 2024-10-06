"""
This file contains all the function required for
parsing the text
"""
import os
import fitz
import pdfplumber
import pandas as pd
# from django.core.mail import send_mail
# from django.conf import settings
import yaml
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
with open("resume_parser/prompts.yaml", "r", encoding="utf-8") as file:
    data = yaml.safe_load(file)


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Function which extract text from PDF resume
    :param pdf_path : Path of the PDF document
    :type  pdf_path : str
    """
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text("text")
    doc.close()
    return text


def extract_tables_from_pdf(pdf_path: str) -> str:
    """
    Function which extract tables from the given PDF resume
    :param pdf_path : Path of the PDF document
    :type  pdf_path : str
    """
    tables_list = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract tables from each page
            tables = page.extract_tables()
            for table in tables:
                df = pd.DataFrame(table)
                tables_list.append(df)

    tables_text = ""
    if tables_list:
        for index, table in enumerate(tables_list):
            tables_text += f"############# TABLE-{index + 1} #############\n"
            tables_text += table.to_csv(index=None)
    return tables_text


# def send_processing_email(user_email, processed_files):
#     """
#     Send email notification about the processed files.
#     """
#     subject = f'{processed_files} have been processed'
#     message = f"""
# Dear Customer,

# Your document {processed_files} is successfully processed.
# Please visit our "Resume Filter" Website to see the results

# Regards,
# Resume Filter Team
#     """
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [user_email]
#     send_mail(subject, message, email_from, recipient_list)


def get_completion(messages: list, model="gpt-4o-mini-2024-07-18"):
    """
    Takes input and generates the output using ChatGPT API
    :param messages: system and user messages
    :type  messages: List
    :param model: model version
    :type  model: str
    """
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        # temperature: A higher value, such as 0.8,
        # makes the answers more diverse,while a lower value,
        #  like 0.2, makes them more focused and deterministic.
        temperature=0.2,
    )
    return completion.choices[0].message.content


def extract_entities_with_chatgpt(text: str, tables: str) -> dict:
    """
    Function which creates a dictiory with extracted summaries

    :param text: Extracted Text from Resume
    :type  text: str
    :param tables: Extracted Tables from Resume
    :type  table: str

    :returns: returns a list of extracted summaries and entities
    :rtype: dict
    """
    entities = {}
    for key in data.keys():
        prompt = data[key]["prompt"].replace(
                 "{TEXT}", text).replace("{TABLES}", tables)
        messages = [{'role': 'system', 'content': data[key]["system-message"]},
                    {'role': 'user', 'content': prompt}]
        entities[key] = get_completion(messages)
    return entities
