"""Document parsing utilities for CVs and job descriptions."""

import json
from pathlib import Path

import docx
from pypdf import PdfReader


def parse_pdf(file_path: str | Path) -> str:
    """
    Extract text from a PDF file.

    Args:
        file_path: Path to the PDF file

    Returns:
        Extracted text content
    """
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()


def parse_docx(file_path: str | Path) -> str:
    """
    Extract text from a DOCX file.

    Args:
        file_path: Path to the DOCX file

    Returns:
        Extracted text content
    """
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text.strip()


def parse_txt(file_path: str | Path) -> str:
    """
    Read text from a plain text file.

    Args:
        file_path: Path to the text file

    Returns:
        File content
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def parse_document(file_path: str | Path) -> str:
    """
    Parse a document and extract text based on file extension.

    Args:
        file_path: Path to the document

    Returns:
        Extracted text content

    Raises:
        ValueError: If file format is not supported
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = path.suffix.lower()

    if extension == ".pdf":
        return parse_pdf(path)
    elif extension == ".docx":
        return parse_docx(path)
    elif extension in [".txt", ".md"]:
        return parse_txt(path)
    elif extension == ".json":
        # For structured job descriptions
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return json.dumps(data, indent=2)
    else:
        raise ValueError(f"Unsupported file format: {extension}")
