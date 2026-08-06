import re


def clean_text(text):
    """
    Clean extracted syllabus text.
    """

    if not text:
        return ""

    # Remove repeated whitespace
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize line breaks
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove strange characters
    text = re.sub(
        r"[^\x00-\x7F]+",
        " ",
        text
    )

    return text.strip()


def chunk_text(
    text,
    chunk_size=1000,
    overlap=150
):
    """
    Split syllabus into overlapping chunks.
    """

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start += chunk_size - overlap

    return chunks