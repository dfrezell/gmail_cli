import base64
import mimetypes
import os
from email.message import EmailMessage
from gmail_auth import authenticate_gmail

def create_message(sender, to, subject, message_html, message_text, attachments=None):
    message = EmailMessage()
    message['From'] = sender
    message['To'] = to
    message['Subject'] = subject
    message.set_content(message_text, subtype='plain')
    message.add_alternative(message_html, subtype='html')
    
    if attachments:
        for file_path in attachments:
            if os.path.isfile(file_path):
                content_type, encoding = mimetypes.guess_type(file_path)
                if content_type is None or encoding is not None:
                    content_type = 'application/octet-stream'
                
                main_type, sub_type = content_type.split('/', 1)
                
                with open(file_path, 'rb') as fp:
                    message.add_attachment(
                        fp.read(),
                        maintype=main_type,
                        subtype=sub_type,
                        filename=os.path.basename(file_path)
                    )
    
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