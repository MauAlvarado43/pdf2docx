import os
import uuid
import tempfile
from io import BytesIO
from playwright.sync_api import sync_playwright
from pdf2docx import parse

def convert_html_to_pdf(html):

    buffer = BytesIO()

    with sync_playwright() as p:
        browser = p.chromium.launch(args=['--no-sandbox'])
        page = browser.new_page()
        page.set_content(html)
        page.wait_for_selector('body')
        pdf_bytes = page.pdf(format='A4', margin={'top': '30px', 'bottom': '30px'})
        buffer.write(pdf_bytes)
        buffer.seek(0)
        browser.close()

    return buffer

def convert_pdf_to_docx(pdf_buffer):

    temp_pdf = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.pdf")
    with open(temp_pdf, 'wb') as f:
        f.write(pdf_buffer.read())

    docx_path = temp_pdf.replace('.pdf', '.docx')
    parse(temp_pdf, docx_path, start=0, end=None)

    with open(docx_path, 'rb') as f:
        docx_buffer = BytesIO(f.read())
        docx_buffer.seek(0)

    os.remove(temp_pdf)
    os.remove(docx_path)

    return docx_buffer

html = "<html><body><h1>Hello, World!</h1><p>This is a test HTML to PDF to DOCX conversion.</p></body></html>"
pdf_buffer = convert_html_to_pdf(html)
docx_buffer = convert_pdf_to_docx(pdf_buffer)

if docx_buffer.getbuffer().nbytes > 0:
    print("Conversion successful!")