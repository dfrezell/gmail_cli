#!/usr/bin/env python3

import argparse
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
from gmail_sender import send_email

def main():
    parser = argparse.ArgumentParser(description='Send emails via Gmail API')
    parser.add_argument('--to', required=True, help='Recipient email address')
    parser.add_argument('--from', dest='sender', required=True, help='Sender email address')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--html', required=True, help='HTML file to use as email body')
    parser.add_argument('--text', help='Text file to use as email body')

    args = parser.parse_args()

    print(f"Sending email to: {args.to}")
    print(f"From: {args.sender}")
    print(f"Subject: {args.subject}")

    # Read HTML body
    try:
        with open(args.html, 'r', encoding='utf-8') as html_file:
            html_body = html_file.read()
    except FileNotFoundError:
        print(f"Error: HTML file '{args.html}' not found.")
        sys.exit(1)

    # Read text body if provided
    if args.text:
        try:
            with open(args.text, 'r', encoding='utf-8') as text_file:
                text_body = text_file.read()
        except FileNotFoundError:
            print(f"Error: Text file '{args.text}' not found.")
            sys.exit(1)
    else:
        text_body = ""

    result = send_email(
        sender=args.sender,
        to=args.to,
        subject=args.subject,
        message_html=html_body,
        message_text=text_body,
        attachments=None  # Attachments can be added later if needed
    )

    if result:
        print(f"Email sent successfully! Message ID: {result.get('id')}")
    else:
        print("Failed to send email.")
        sys.exit(1)

if __name__ == '__main__':
    main()
