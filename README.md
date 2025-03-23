# PDF Text Extraction Tool

A Python utility for extracting text from scanned PDF documents using OCR technology.

## Description

This tool uses Tesseract OCR to extract text from PDF files, saving each page as a separate text file. It can also combine all extracted pages into a single document.

Key features:
- Converts PDF pages to images
- Applies image preprocessing to improve OCR accuracy
- Extracts text using Tesseract OCR
- Combines extracted text files into a single document (optional)
- Automatically sets up a virtual environment with required dependencies

## Installation

This script is designed to be run directly and is not installable as a package. It automatically creates a dedicated virtual environment with all required Python dependencies (pdf2image, pytesseract, pillow) the first time it runs.

## Requirements

- Python 3.6+
- Tesseract OCR must be installed on your system
  - Ubuntu/Debian: `sudo apt install tesseract-ocr`
  - macOS: `brew install tesseract`
  - Windows: Download installer from https://github.com/UB-Mannheim/tesseract/wiki

## Usage

```
python pdf_text_extraction.py --pdf_path <path_to_pdf> --output_dir <output_directory> [--combine] [--skip-extraction]
```

### Arguments

- `--pdf_path`: Path to the PDF file to process
- `--output_dir`: Directory to save extracted text files
- `--combine`: (Optional) Combine all extracted text files into a single document
- `--skip-extraction`: (Optional) Skip extraction and only combine existing text files

### Examples

Extract text from a PDF:
```
python pdf_text_extraction.py --pdf_path document.pdf --output_dir ./extracted_text
```

Extract text and combine into a single document:
```
python pdf_text_extraction.py --pdf_path document.pdf --output_dir ./extracted_text --combine
```

Only combine existing text files:
```
python pdf_text_extraction.py --output_dir ./extracted_text --combine --skip-extraction
```

## Created by

This tool was vibe coded by Erika Rice Scherpelz using Claude Code.
