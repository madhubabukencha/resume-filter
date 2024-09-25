"""
This file contains all the function required for
parsing the text
"""
import fitz
import pdfplumber
import pandas as pd


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


def extract_tables(pdf_path: str) -> str:
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
