import base64
import mimetypes
import os
from msgraph.generated.models.message import Message
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.recipient import Recipient
from msgraph.generated.models.email_address import EmailAddress
from msgraph.generated.models.attachment import Attachment
from msgraph.generated.models.file_attachment import FileAttachment
from outlook_auth import authenticate_outlook

def create_outlook_message(sender, to, subject, message_html, message_text):
    """Create a Microsoft Graph message object"""
    message = Message()
    
    # Set sender and recipient
    message.from_ = Recipient()
    message.from_.email_address = EmailAddress()
    message.from_.email_address.address = sender
    
    message.to_recipients = []
    recipient = Recipient()
    recipient.email_address = EmailAddress()
    recipient.email_address.address = to
    message.to_recipients.append(recipient)
    
    # Set subject
    message.subject = subject
    
    # Set body (prefer HTML if available, fallback to text)
    message.body = ItemBody()
    if message_html:
        message.body.content_type = BodyType.Html
        message.body.content = message_html
    else:
        message.body.content_type = BodyType.Text
        message.body.content = message_text
    
    return message

def add_attachments_to_message(message, attachments):
    """Add file attachments to the message"""
    if not attachments:
        return message
    
    message.attachments = []
    
    for file_path in attachments:
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                file_content = file.read()
            
            attachment = FileAttachment()
            attachment.name = os.path.basename(file_path)
            attachment.content_bytes = base64.b64encode(file_content).decode()
            
            # Guess content type
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type:
                attachment.content_type = content_type
            else:
                attachment.content_type = 'application/octet-stream'
            
            message.attachments.append(attachment)
    
    return message

import asyncio

def send_outlook_email(sender, to, subject, message_html, message_text, attachments=None):
    """Send email using Microsoft Graph API"""
    return asyncio.run(send_outlook_email_async(sender, to, subject, message_html, message_text, attachments))

async def send_outlook_email_async(sender, to, subject, message_html, message_text, attachments=None):
    """Send email using Microsoft Graph API (async)"""
    try:
        # Authenticate and get Graph client
        graph_client = authenticate_outlook()
        
        # Create message
        message = create_outlook_message(sender, to, subject, message_html, message_text)
        
        # Add attachments if provided
        if attachments:
            message = add_attachments_to_message(message, attachments)
        
        # Create the send mail request body
        from msgraph.generated.users.item.send_mail.send_mail_post_request_body import SendMailPostRequestBody
        
        request_body = SendMailPostRequestBody()
        request_body.message = message
        request_body.save_to_sent_items = True
        
        # Send the message (properly await the async call)
        result = await graph_client.me.send_mail.post(request_body)
        
        return {'id': 'outlook_sent', 'status': 'sent'}
        
    except Exception as error:
        print(f'An error occurred sending via Outlook: {error}')
        import traceback
        traceback.print_exc()
        return None