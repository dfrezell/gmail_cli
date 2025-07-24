import base64
import mimetypes
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from gmail_auth import authenticate_gmail

def create_message(sender, to, subject, message_html, message_text, attachments=None):
    message = MIMEMultipart("mixed" if attachments else "alternative")
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    
    message.attach(MIMEText(message_text, 'plain'))
    message.attach(MIMEText(message_html, 'html'))
    
    if attachments:
        for file_path in attachments:
            if os.path.isfile(file_path):
                content_type, encoding = mimetypes.guess_type(file_path)
                if content_type is None or encoding is not None:
                    content_type = 'application/octet-stream'
                
                main_type, sub_type = content_type.split('/', 1)
                
                with open(file_path, 'rb') as fp:
                    attachment = MIMEBase(main_type, sub_type)
                    attachment.set_payload(fp.read())
                    encoders.encode_base64(attachment)
                    attachment.add_header(
                        'Content-Disposition',
                        f'attachment; filename="{os.path.basename(file_path)}"'
                    )
                    message.attach(attachment)
    
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_email(sender, to, subject, message_html, message_text, attachments=None):
    try:
        service = authenticate_gmail()
        message = create_message(sender, to, subject, message_html, message_text, attachments)
        
        sent_message = service.users().messages().send(
            userId='me', body=message
        ).execute()
        
        return sent_message
    except Exception as error:
        print(f'An error occurred: {error}')
        return None