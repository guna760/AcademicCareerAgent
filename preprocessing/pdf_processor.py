import fitz


def extract_text_from_pdf(pdf_file):
    """
    Extract text from uploaded PDF.

    pdf_file can be:
    - Streamlit UploadedFile
    - file-like object
    """

    pdf_bytes = pdf_file.read()

    document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    pages = []

    for page in document:
        text = page.get_text()

        if text.strip():
            pages.append(text)

    document.close()

    return "\n".join(pages)