"""
This file contains all the function required for
parsing the text
"""
import fitz
import pdfplumber
import pandas as pd
# from django.core.mail import send_mail
# from django.conf import settings


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