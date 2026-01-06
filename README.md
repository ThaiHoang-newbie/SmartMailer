# SmartMailer 📧

A powerful Streamlit application for automated personalized email campaigns with image generation.

## Features

✨ **Import Excel Data** - Load recipient lists with names, emails, and dates
🎨 **Image Generation** - Create personalized images with names and dates
📤 **Email Automation** - Send emails with attachments
⏰ **Email Scheduling** - Schedule emails for future delivery
🔧 **Flexible Modes** - Combine or separate days per recipient

## Project Structure

```
SmartMailer/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── assets/
│   ├── fonts/                  # Custom fonts (optional)
│   ├── images/
│   │   └── generated/          # Generated personalized images
│   └── templates/              # Template images
├── config/
│   ├── settings.py             # Configuration management
│   └── config.json             # Saved configuration
├── data/
│   ├── processed/              # Processed data
│   └── uploads/                # Uploaded Excel files
├── services/
│   ├── image_generator.py      # Image generation service
│   ├── email_sender.py         # Email sending service
│   └── scheduler.py            # Email scheduling service
├── tests/                      # Unit tests
├── ui/                         # UI components (if needed)
└── utils/                      # Utility functions
```

## Installation

1. **Clone or create the project directory:**
```bash
mkdir SmartMailer
cd SmartMailer
```

2. **Create virtual environment:**
```bash
python -m venv venv
```

3. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Excel File Format

Your Excel file should have these columns:

| Name | Email | Date |
|------|-------|------|
| John Doe | john@example.com | 15/03/2024 |
| Jane Smith | jane@example.com | 20/03/2024 |

- **Name**: Recipient's name
- **Email**: Recipient's email address
- **Date**: Date in DD/MM/YYYY format

## Usage

1. **Start the application:**
```bash
streamlit run app.py
```

2. **Configure Email Settings (Sidebar):**
   - Enter your sender email
   - Enter your email password (App password for Gmail)
   - Set SMTP server (default: smtp.gmail.com)
   - Set SMTP port (default: 587)

3. **Import Data:**
   - Go to "Import Data" tab
   - Upload your Excel file
   - Verify the data loaded correctly

4. **Generate Images:**
   - Go to "Generate Images" tab
   - Upload a template image (PNG/JPEG)
   - Adjust text positions and styling
   - Click "Generate All Images"

5. **Send Emails:**
   - Go to "Send Emails" tab
   - Customize email subject and body
   - Choose "Send Now" or "Schedule"
   - Click "Send/Schedule Emails"

## Send Modes

### Combine Days
- One email per person
- All dates combined in a single image
- Example: "Date: 15/03/2024, 20/03/2024, 25/03/2024"

### Separate Days
- Separate email for each date
- Individual image per date
- Better for event-specific reminders

## Gmail Setup

To use Gmail as SMTP:

1. Enable 2-Factor Authentication
2. Generate App Password:
   - Go to Google Account → Security
   - Select "App passwords"
   - Generate password for "Mail"
3. Use the generated password in SmartMailer

## Tips

- Use high-quality template images (PNG recommended)
- Test with a small list first
- Check spam folder if emails not received
- For Gmail, use App Passwords instead of regular password
- Adjust text positions based on your template image

## Troubleshooting

**Images not generating:**
- Verify template image is uploaded
- Check image format (PNG/JPEG only)

**Emails not sending:**
- Verify SMTP settings
- Check email credentials
- Ensure internet connection
- For Gmail, use App Password

**Excel import errors:**
- Verify column names match exactly
- Check date format (DD/MM/YYYY)
- Ensure no empty rows

## Security Notes

- Never commit config.json with credentials
- Use environment variables for production
- Use App Passwords for email accounts
- Keep your venv directory private

## License

MIT License - Feel free to use and modify!

## Support

For issues or questions, please check the documentation or create an issue in the repository.