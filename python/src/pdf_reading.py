from pypdf import PdfReader


def read_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = []
    for page in reader.pages:
        text.append(page.extract_text())

    return "\n\n".join(text)
