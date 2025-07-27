#!/usr/bin/env python3

import email
import quopri
import base64
import argparse
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def decode_content(content, encoding):
    """Decode content based on encoding type"""
    if encoding == 'quoted-printable':
        return quopri.decodestring(content.encode()).decode('utf-8')
    elif encoding == 'base64':
        return base64.b64decode(content.encode()).decode('utf-8')
    else:
        return content

def parse_eml_file(eml_file):
    """Parse EML file and extract HTML and text parts"""
    with open(eml_file, 'r', encoding='utf-8') as f:
        msg = email.message_from_file(f)
    
    html_content = None
    text_content = None
    
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_encoding = part.get('Content-Transfer-Encoding', '').lower()
            
            if content_type == 'text/plain':
                content = part.get_payload()
                text_content = decode_content(content, content_encoding)
            elif content_type == 'text/html':
                content = part.get_payload()
                html_content = decode_content(content, content_encoding)
    else:
        # Single part message
        content_type = msg.get_content_type()
        content_encoding = msg.get('Content-Transfer-Encoding', '').lower()
        content = msg.get_payload()
        
        if content_type == 'text/plain':
            text_content = decode_content(content, content_encoding)
        elif content_type == 'text/html':
            html_content = decode_content(content, content_encoding)
    
    return html_content, text_content

def main():
    parser = argparse.ArgumentParser(description='Parse EML files and extract HTML/text content')
    parser.add_argument('eml_file', help='Path to the EML file to parse')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.eml_file):
        print(f"Error: EML file '{args.eml_file}' not found")
        return
    
    # Get the directory and base filename
    eml_dir = os.path.dirname(args.eml_file)
    eml_basename = os.path.splitext(os.path.basename(args.eml_file))[0]
    
    # If no directory specified, use current directory
    if not eml_dir:
        eml_dir = '.'
    
    # Create output filenames
    html_output = os.path.join(eml_dir, f"{eml_basename}.html")
    text_output = os.path.join(eml_dir, f"{eml_basename}.txt")
    
    try:
        print(f"Parsing EML file: {args.eml_file}")
        html_content, text_content = parse_eml_file(args.eml_file)
        
        if html_content:
            with open(html_output, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Extracted HTML content -> {html_output}")
            print(f"HTML content preview (first 500 chars):\n{html_content[:500]}...")
        else:
            print("No HTML content found in the EML file")
        
        if text_content:
            with open(text_output, 'w', encoding='utf-8') as f:
                f.write(text_content)
            print(f"\nExtracted text content -> {text_output}")
            print(f"Text content preview (first 500 chars):\n{text_content[:500]}...")
        else:
            print("No text content found in the EML file")
            
    except Exception as e:
        print(f"Error parsing EML file: {e}")

if __name__ == '__main__':
    main()