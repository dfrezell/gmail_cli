#!/usr/bin/env python3

import argparse
from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter
import re

def format_html_file(file_path, indent_size=2):
    """Format HTML file with consistent indentation"""
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    # Format with consistent indentation
    formatted_html = soup.prettify(formatter=HTMLFormatter(indent=indent_size))
    
    # Clean up some common formatting issues
    # Remove extra blank lines
    formatted_html = re.sub(r'\n\s*\n\s*\n', '\n\n', formatted_html)
    
    # Fix self-closing tags to be more consistent
    formatted_html = re.sub(r'<(br|img|input|meta|link)([^>]*?)>', r'<\1\2>', formatted_html)
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(formatted_html)
    
    print(f"Formatted {file_path} with {indent_size} spaces indentation.")

def main():
    parser = argparse.ArgumentParser(description='Format HTML files with consistent indentation')
    parser.add_argument('files', nargs='+', help='HTML files to format')
    parser.add_argument('--indent', type=int, default=2, help='Number of spaces for indentation (default: 2)')
    
    args = parser.parse_args()
    
    for file_path in args.files:
        try:
            format_html_file(file_path, args.indent)
        except Exception as e:
            print(f"Error formatting {file_path}: {e}")

if __name__ == '__main__':
    main()