#!/usr/bin/env python3

import email
import quopri
import base64
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

# Parse message.eml
try:
    html_content, text_content = parse_eml_file('message.eml')
    
    if html_content:
        with open('message.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("Extracted HTML content -> message.html")
        print(f"HTML content preview (first 500 chars):\n{html_content[:500]}...")
    else:
        print("No HTML content found in the EML file")
    
    if text_content:
        with open('message.txt', 'w', encoding='utf-8') as f:
            f.write(text_content)
        print("\nExtracted text content -> message.txt")
        print(f"Text content:\n{text_content}")
    else:
        print("No text content found in the EML file")
        
except FileNotFoundError:
    print("Error: message.eml file not found")
except Exception as e:
    print(f"Error parsing EML file: {e}")