#!/usr/bin/env python3

import argparse
import sys
from gmail_sender import send_email
from outlook_sender import send_outlook_email

def detect_provider(email_address):
    """Detect email provider based on email address domain"""
    domain = email_address.split('@')[1].lower()
    
    outlook_domains = ['outlook.com', 'hotmail.com', 'live.com', 'msn.com']
    gmail_domains = ['gmail.com', 'googlemail.com']
    
    if domain in outlook_domains:
        return 'outlook'
    elif domain in gmail_domains:
        return 'gmail'
    else:
        # Default to Gmail for unknown domains
        return 'gmail'

def main():
    parser = argparse.ArgumentParser(description='Send emails via Gmail or Outlook API')
    parser.add_argument('--to', required=True, help='Recipient email address')
    parser.add_argument('--from', dest='sender', required=True, help='Sender email address')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--html', required=True, help='HTML file to use as email body')
    parser.add_argument('--text', help='Text file to use as email body')
    parser.add_argument('--provider', choices=['gmail', 'outlook'], 
                       help='Force specific email provider (auto-detected from sender address if not specified)')
    parser.add_argument('--attachments', nargs='*', help='File paths to attach')

    args = parser.parse_args()

    # Determine provider
    if args.provider:
        provider = args.provider
    else:
        provider = detect_provider(args.sender)
    
    print(f"Sending email to: {args.to}")
    print(f"From: {args.sender}")
    print(f"Subject: {args.subject}")
    print(f"Provider: {provider}")

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

    # Send email using appropriate provider
    if provider == 'outlook':
        result = send_outlook_email(
            sender=args.sender,
            to=args.to,
            subject=args.subject,
            message_html=html_body,
            message_text=text_body,
            attachments=args.attachments
        )
    else:  # Gmail
        result = send_email(
            sender=args.sender,
            to=args.to,
            subject=args.subject,
            message_html=html_body,
            message_text=text_body,
            attachments=args.attachments
        )

    if result:
        print(f"Email sent successfully! Message ID: {result.get('id')}")
    else:
        print("Failed to send email.")
        sys.exit(1)

if __name__ == '__main__':
    main()
