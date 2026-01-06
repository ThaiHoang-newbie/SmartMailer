import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path

class EmailSender:
    def __init__(self, sender_email, password, smtp_server, smtp_port):
        self.sender_email = sender_email
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    
    def send_email(self, recipient, subject, body, image_path=None):
        """
        Send email with optional image attachment
        
        Args:
            recipient: Recipient email address
            subject: Email subject
            body: Email body text
            image_path: Path to image attachment (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            
            # Attach body
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach image if provided
            if image_path and Path(image_path).exists():
                with open(image_path, 'rb') as f:
                    img_data = f.read()
                    image = MIMEImage(img_data, name=Path(image_path).name)
                    msg.attach(image)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.send_message(msg)
            
            print(f"✅ Email sent to {recipient}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email to {recipient}: {str(e)}")
            return False