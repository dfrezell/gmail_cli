#!/usr/bin/env python3

import argparse
import sys
from gmail_sender import send_email

def main():
    parser = argparse.ArgumentParser(description='Send emails via Gmail API')
    parser.add_argument('--to', required=True, help='Recipient email address')
    parser.add_argument('--from', dest='sender', required=True, help='Sender email address')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--message', required=True, help='Email message body')
    parser.add_argument('--attachments', nargs='*', help='File paths to attach')
    
    args = parser.parse_args()
    
    print(f"Sending email to: {args.to}")
    print(f"From: {args.sender}")
    print(f"Subject: {args.subject}")
    
    result = send_email(
        sender=args.sender,
        to=args.to,
        subject=args.subject,
        message_text=args.message,
        attachments=args.attachments
    )
    
    if result:
        print(f"Email sent successfully! Message ID: {result.get('id')}")
    else:
        print("Failed to send email.")
        sys.exit(1)

if __name__ == '__main__':
    main()