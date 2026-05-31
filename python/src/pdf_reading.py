from pypdf import PdfReader
import os


def read_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)

    text = []

    for page in reader.pages:
        text.append(page.extract_text())

    return "\n\n".join(text)


def check_file_size(path: str, max_mb: int = 15):
    size_mb = os.path.getsize(path) / (1024 * 1024)

    if size_mb > max_mb:
        raise ValueError(
            f"PDF too large: {size_mb:.2f} MB (limit {max_mb} MB)"
            )
