#!/usr/bin/env python3
"""
PDF Text Extraction Tool

This script extracts text from scanned PDFs using OCR and saves it to text files.
It requires Tesseract OCR to be installed on your system.
"""

import argparse
import os
import sys
import subprocess
import venv
from pathlib import Path


def setup_virtual_environment():
    """Set up a virtual environment for the required packages."""
    venv_dir = Path.home() / ".pdf_extractor_venv"
    
    # Create virtual environment if it doesn't exist
    if not venv_dir.exists():
        print(f"Creating virtual environment at {venv_dir}...")
        venv.create(venv_dir, with_pip=True)
    
    # Determine paths
    if sys.platform == 'win32':
        pip_path = venv_dir / 'Scripts' / 'pip.exe'
        python_path = venv_dir / 'Scripts' / 'python.exe'
    else:
        pip_path = venv_dir / 'bin' / 'pip'
        python_path = venv_dir / 'bin' / 'python'
    
    # Required packages
    packages = ["pdf2image", "pytesseract", "pillow"]
    
    print(f"Installing required packages in virtual environment: {', '.join(packages)}")
    
    try:
        subprocess.check_call([str(pip_path), "install"] + packages)
        print("Required packages installed successfully.")
    except Exception as e:
        print(f"Error installing packages: {e}")
        print("Please install them manually in the virtual environment.")
        sys.exit(1)
    
    return python_path


def check_tesseract():
    """Check if Tesseract OCR is installed."""
    try:
        result = subprocess.run(["tesseract", "--version"], 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE, 
                             text=True)
        print(f"Tesseract version: {result.stdout.split()[1] if result.stdout else 'Unknown'}")
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Tesseract OCR is not installed. Please install it:")
        print("  Ubuntu/Debian: sudo apt install tesseract-ocr")
        print("  macOS: brew install tesseract")
        print("  Windows: download installer from https://github.com/UB-Mannheim/tesseract/wiki")
        return False


def extract_text_from_pdf(pdf_path, output_dir):
    """Extract text from PDF using OCR.
    
    This function requires the following packages:
    - pdf2image: For converting PDF to images
    - pytesseract: Python wrapper for Tesseract OCR
    - pillow: For image processing
    
    These packages should be installed in the virtual environment.
    """
    # Import here to ensure these are imported from virtual environment
    from pdf2image import convert_from_path
    import pytesseract
    from PIL import Image, ImageEnhance, ImageFilter
    
    print(f"Converting PDF to images: {pdf_path}")
    # Convert PDF to images
    images = convert_from_path(pdf_path)
    
    # Create output directory if it doesn't exist
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    print(f"Extracting text from {len(images)} pages...")
    for i, image in enumerate(images):
        page_num = i + 1
        print(f"Processing page {page_num}/{len(images)}")
        
        # Preprocess the image to improve OCR quality
        # Convert to grayscale
        gray_image = image.convert('L')
        
        # Increase contrast
        enhancer = ImageEnhance.Contrast(gray_image)
        enhanced_image = enhancer.enhance(2)
        
        # Apply threshold to make text more distinct
        threshold = 150
        thresholded_image = enhanced_image.point(lambda p: p > threshold and 255)
        
        # Extract text using OCR
        text = pytesseract.image_to_string(thresholded_image)
        
        # Save text to file
        output_file = output_dir / f"page_{page_num:03d}.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        
        print(f"Saved text from page {page_num} to {output_file}")
    
    print(f"Complete! Extracted text from {len(images)} pages to {output_dir}")


def combine_text_files(output_dir, output_file="combined_text.txt"):
    """Combine all extracted text files into a single document."""
    output_dir = Path(output_dir)
    if not output_dir.exists() or not output_dir.is_dir():
        print(f"Error: Output directory {output_dir} does not exist.")
        return False
    
    # Get all text files and sort them by page number
    text_files = sorted(output_dir.glob("page_*.txt"), 
                        key=lambda x: int(x.stem.split('_')[1]))
    
    if not text_files:
        print(f"No text files found in {output_dir}")
        return False
    
    # Combine all text files
    combined_content = ""
    for file_path in text_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                
                # Add page break marker for Word/Google Docs
                combined_content += content + "\n\n" + "-" * 80 + "\n\n"
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    # Write combined content to file
    combined_path = output_dir / output_file
    try:
        with open(combined_path, "w", encoding="utf-8") as f:
            f.write(combined_content)
        print(f"Combined text saved to {combined_path}")
        return True
    except Exception as e:
        print(f"Error writing combined file: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Extract text from scanned PDFs using OCR")
    parser.add_argument('--pdf_path', dest='pdf_path', help='Path to the PDF file')
    parser.add_argument('--output_dir', dest='output_dir', help='Directory to save extracted text files')
    parser.add_argument('--combine', action='store_true',
                      help='Combine extracted text files into a single document')
    parser.add_argument('--skip-extraction', action='store_true',
                      help='Skip extraction and only combine existing text files')
    args = parser.parse_args()
    
    # Validate arguments
    if args.skip_extraction and args.combine:
        if not args.output_dir:
            print("Error: --output_dir is required when using --skip-extraction and --combine")
            return
        print(f"Combining existing text files from {args.output_dir}...")
        combine_text_files(args.output_dir)
        return
    
    # Check if required arguments are provided
    if not args.pdf_path or not args.output_dir:
        print("Error: Both --pdf_path and --output_dir are required for extraction")
        return
    
    # Validate the PDF path
    pdf_path = Path(args.pdf_path).resolve()
    if not pdf_path.exists():
        print(f"Error: The file {pdf_path} does not exist.")
        return
    
    # Check if Tesseract is installed
    if not check_tesseract():
        return
    
    # Setup virtual environment
    setup_virtual_environment()
    
    try:
        # Import module-level dependencies if needed
        sys.path.insert(0, str(Path.home() / ".pdf_extractor_venv" / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"))
        
        # Extract text from PDF
        output_dir = args.output_dir
        print(f"Starting extraction process...")
        extract_text_from_pdf(str(pdf_path), output_dir)
        
        # Combine text files if requested
        if args.combine:
            print(f"Combining extracted text files...")
            combine_text_files(output_dir)
    except Exception as e:
        print(f"Error during extraction: {e}")


if __name__ == '__main__':
    main()