import json
from pathlib import Path

class Settings:
    def __init__(self):
        self.config_file = Path("config/config.json")
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Default settings
        self.SENDER_EMAIL = ""
        self.SENDER_PASSWORD = ""
        self.SMTP_SERVER = "smtp.gmail.com"
        self.SMTP_PORT = 587
        
        # Load existing config if available
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.SENDER_EMAIL = config.get('sender_email', '')
                    self.SENDER_PASSWORD = config.get('sender_password', '')
                    self.SMTP_SERVER = config.get('smtp_server', 'smtp.gmail.com')
                    self.SMTP_PORT = config.get('smtp_port', 587)
            except Exception as e:
                print(f"Error loading config: {str(e)}")
    
    def update_config(self, sender_email, sender_password, smtp_server, smtp_port):
        """Update and save configuration"""
        self.SENDER_EMAIL = sender_email
        self.SENDER_PASSWORD = sender_password
        self.SMTP_SERVER = smtp_server
        self.SMTP_PORT = smtp_port
        
        config = {
            'sender_email': sender_email,
            'sender_password': sender_password,
            'smtp_server': smtp_server,
            'smtp_port': smtp_port
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)