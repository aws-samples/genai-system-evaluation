#!/usr/bin/env python3

import os
import boto3
import re
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from concurrent.futures import ProcessPoolExecutor
from functools import partial

def normalize_filename(filename):
    """Normalize filename: lowercase, remove spaces/dashes/underscores"""
    return re.sub(r'[-_\s]+', '', filename.lower())

def split_pdf(pdf_path, output_dir):
    """Split PDF into individual pages"""
    reader = PdfReader(pdf_path)
    
    # Handle encrypted PDFs
    if reader.is_encrypted:
        reader.decrypt("")
    
    pdf_name = normalize_filename(Path(pdf_path).stem)
    
    page_files = []
    for page_num, page in enumerate(reader.pages, 1):
        writer = PdfWriter()
        writer.add_page(page)
        
        output_file = output_dir / f"{pdf_name}_page{page_num}.pdf"
        with open(output_file, 'wb') as f:
            writer.write(f)
        page_files.append(output_file)
    
    return page_files

def pdf_to_markdown(pdf_path):
    """Convert PDF to markdown using Bedrock"""
    bedrock = boto3.client('bedrock-runtime')
    
    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()
    
    response = bedrock.converse(
        modelId='us.anthropic.claude-haiku-4-5-20251001-v1:0',
        messages=[{
            'role': 'user',
            'content': [{
                'document': {
                    'format': 'pdf',
                    'name': 'document',
                    'source': {'bytes': pdf_bytes}
                }
            }, {
                'text': 'Convert this PDF page to clean markdown format. Preserve structure and formatting.'
            }]
        }]
    )
    
    return response['output']['message']['content'][0]['text']

def process_page(page_file, markdown_dir):
    """Process a single page - for parallel execution"""
    try:
        print(f"Converting {page_file.name} to markdown...")
        markdown_content = pdf_to_markdown(page_file)
        
        # Save markdown file
        markdown_file = markdown_dir / f"{page_file.stem}.md"
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"Created {markdown_file}")
        return str(markdown_file)
    except Exception as e:
        print(f"Error processing {page_file}: {e}")
        return None

def main():
    doc_dir = Path('doc')
    stage_dir = Path('stage')
    markdown_dir = Path('markdownfiles')
    
    # Create directories
    stage_dir.mkdir(exist_ok=True)
    markdown_dir.mkdir(exist_ok=True)
    
    # Process all PDFs in doc/
    all_page_files = []
    for pdf_file in doc_dir.glob('*.pdf'):
        print(f"Processing {pdf_file.name}...")
        page_files = split_pdf(pdf_file, stage_dir)
        all_page_files.extend(page_files)
    
    print(f"Converting {len(all_page_files)} pages to markdown using 3 parallel processes...")
    
    # Process pages in parallel
    process_func = partial(process_page, markdown_dir=markdown_dir)
    with ProcessPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(process_func, all_page_files))
    
    successful = [r for r in results if r is not None]
    print(f"Successfully converted {len(successful)} pages to markdown")

if __name__ == "__main__":
    main()
