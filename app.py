import streamlit as st
import pandas as pd
from datetime import datetime, time
import os
from pathlib import Path

# Import services
from services.image_generator import ImageGenerator
from services.email_sender import EmailSender
from services.scheduler import EmailScheduler
from config.settings import Settings

# Initialize settings
settings = Settings()

# Page config
st.set_page_config(
    page_title="SmartMailer",
    page_icon="📧",
    layout="wide"
)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'generated_images' not in st.session_state:
    st.session_state.generated_images = {}
if 'scheduler' not in st.session_state:
    st.session_state.scheduler = EmailScheduler()

# Title
st.title("📧 SmartMailer")
st.markdown("---")

# Sidebar - Email Configuration
with st.sidebar:
    st.header("⚙️ Email Configuration")
    
    sender_email = st.text_input("Sender Email", value=settings.SENDER_EMAIL)
    sender_password = st.text_input("Email Password", type="password", value=settings.SENDER_PASSWORD)
    smtp_server = st.text_input("SMTP Server", value=settings.SMTP_SERVER)
    smtp_port = st.number_input("SMTP Port", value=settings.SMTP_PORT, min_value=1, max_value=65535)
    
    st.markdown("---")
    st.header("🎨 Image Settings")
    
    send_mode = st.radio(
        "Send Mode",
        ["Combine Days", "Separate Days"],
        help="Combine: One image with all dates. Separate: Individual images per date."
    )
    
    if st.button("Save Configuration"):
        settings.update_config(sender_email, sender_password, smtp_server, smtp_port)
        st.success("Configuration saved!")

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📁 Import Data", "🖼️ Generate Images", "📤 Send Emails", "📊 Scheduled Emails"])

# Tab 1: Import Excel File
with tab1:
    st.header("Import Excel File")
    st.markdown("Upload an Excel file with columns: **Name**, **Email**, **Date** (format: DD/MM/YYYY)")
    
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])
    
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            
            # Validate columns
            required_cols = ['Name', 'Email', 'Date']
            if all(col in df.columns for col in required_cols):
                # Convert Date column to datetime
                df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
                
                # Save to data/uploads
                upload_path = Path("data/uploads") / uploaded_file.name
                upload_path.parent.mkdir(parents=True, exist_ok=True)
                df.to_excel(upload_path, index=False)
                
                st.session_state.df = df
                
                st.success(f"✅ Loaded {len(df)} records successfully!")
                st.dataframe(df)
                
                # Statistics
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Recipients", len(df))
                col2.metric("Unique Dates", df['Date'].nunique())
                col3.metric("Valid Emails", df['Email'].notna().sum())
                
            else:
                st.error(f"❌ Excel file must contain columns: {', '.join(required_cols)}")
        
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

# Tab 2: Generate Images
with tab2:
    st.header("Generate Personalized Images")
    
    if st.session_state.df is not None:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Upload Template Image")
            template_file = st.file_uploader("Choose template image (PNG/JPEG)", type=['png', 'jpg', 'jpeg'])
            
            if template_file:
                # Save template
                template_path = Path("assets/templates") / template_file.name
                template_path.parent.mkdir(parents=True, exist_ok=True)
                with open(template_path, 'wb') as f:
                    f.write(template_file.getbuffer())
                
                st.image(template_file, caption="Template Image", width=None)
        
        with col2:
            st.subheader("Text Settings")
            font_size = st.slider("Font Size", 20, 100, 40)
            text_color = st.color_picker("Text Color", "#000000")
            name_x = st.slider("Name X Position", 0, 1000, 100)
            name_y = st.slider("Name Y Position", 0, 1000, 100)
            date_x = st.slider("Date X Position", 0, 1000, 100)
            date_y = st.slider("Date Y Position", 0, 1000, 200)
        
        if st.button("🎨 Generate All Images", type="primary"):
            if template_file:
                with st.spinner("Generating images..."):
                    generator = ImageGenerator(str(template_path))
                    
                    if send_mode == "Combine Days":
                        # Group by email and combine dates
                        grouped = st.session_state.df.groupby(['Name', 'Email'])['Date'].apply(list).reset_index()
                        
                        for idx, row in grouped.iterrows():
                            dates_str = ", ".join([d.strftime('%d/%m/%Y') for d in row['Date']])
                            output_path = generator.generate_image(
                                row['Name'],
                                dates_str,
                                font_size,
                                text_color,
                                (name_x, name_y),
                                (date_x, date_y)
                            )
                            st.session_state.generated_images[row['Email']] = output_path
                    else:
                        # Generate separate images for each row
                        for idx, row in st.session_state.df.iterrows():
                            date_str = row['Date'].strftime('%d/%m/%Y')
                            output_path = generator.generate_image(
                                row['Name'],
                                date_str,
                                font_size,
                                text_color,
                                (name_x, name_y),
                                (date_x, date_y)
                            )
                            key = f"{row['Email']}_{idx}"
                            st.session_state.generated_images[key] = output_path
                    
                    st.success(f"✅ Generated {len(st.session_state.generated_images)} images!")
            else:
                st.warning("⚠️ Please upload a template image first.")
        
        # Display generated images
        if st.session_state.generated_images:
            st.subheader("Generated Images Preview")
            cols = st.columns(3)
            for idx, (key, img_path) in enumerate(list(st.session_state.generated_images.items())[:6]):
                with cols[idx % 3]:
                    st.image(img_path, caption=key, width=None)
    else:
        st.info("👆 Please import an Excel file first in the 'Import Data' tab.")

# Tab 3: Send Emails
with tab3:
    st.header("Send Emails")
    
    if st.session_state.df is not None and st.session_state.generated_images:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            email_subject = st.text_input("Email Subject", "Your Personalized Image")
            email_body = st.text_area(
                "Email Body",
                "Dear {name},\n\nPlease find your personalized image attached.\n\nBest regards,\nSmartMailer Team",
                height=150
            )
        
        with col2:
            st.subheader("Schedule Options")
            schedule_type = st.radio("Send Type", ["Send Now", "Schedule"])
            
            if schedule_type == "Schedule":
                schedule_date = st.date_input("Schedule Date", datetime.now())
                schedule_time = st.time_input("Schedule Time", time(9, 0))
        
        if st.button("📤 Send/Schedule Emails", type="primary"):
            email_sender = EmailSender(sender_email, sender_password, smtp_server, smtp_port)
            
            if schedule_type == "Send Now":
                with st.spinner("Sending emails..."):
                    success_count = 0
                    
                    if send_mode == "Combine Days":
                        grouped = st.session_state.df.groupby(['Name', 'Email']).first().reset_index()
                        for idx, row in grouped.iterrows():
                            if row['Email'] in st.session_state.generated_images:
                                body = email_body.replace('{name}', row['Name'])
                                if email_sender.send_email(
                                    row['Email'],
                                    email_subject,
                                    body,
                                    st.session_state.generated_images[row['Email']]
                                ):
                                    success_count += 1
                    else:
                        for idx, row in st.session_state.df.iterrows():
                            key = f"{row['Email']}_{idx}"
                            if key in st.session_state.generated_images:
                                body = email_body.replace('{name}', row['Name'])
                                if email_sender.send_email(
                                    row['Email'],
                                    email_subject,
                                    body,
                                    st.session_state.generated_images[key]
                                ):
                                    success_count += 1
                    
                    st.success(f"✅ Successfully sent {success_count} emails!")
            else:
                # Schedule emails
                schedule_datetime = datetime.combine(schedule_date, schedule_time)
                
                if send_mode == "Combine Days":
                    grouped = st.session_state.df.groupby(['Name', 'Email']).first().reset_index()
                    for idx, row in grouped.iterrows():
                        if row['Email'] in st.session_state.generated_images:
                            body = email_body.replace('{name}', row['Name'])
                            st.session_state.scheduler.schedule_email(
                                schedule_datetime,
                                row['Email'],
                                email_subject,
                                body,
                                st.session_state.generated_images[row['Email']],
                                sender_email,
                                sender_password,
                                smtp_server,
                                smtp_port
                            )
                else:
                    for idx, row in st.session_state.df.iterrows():
                        key = f"{row['Email']}_{idx}"
                        if key in st.session_state.generated_images:
                            body = email_body.replace('{name}', row['Name'])
                            st.session_state.scheduler.schedule_email(
                                schedule_datetime,
                                row['Email'],
                                email_subject,
                                body,
                                st.session_state.generated_images[key],
                                sender_email,
                                sender_password,
                                smtp_server,
                                smtp_port
                            )
                
                st.success(f"✅ Scheduled emails for {schedule_datetime.strftime('%Y-%m-%d %H:%M')}")
    else:
        st.info("👆 Please import data and generate images first.")

# Tab 4: Scheduled Emails
with tab4:
    st.header("Scheduled Emails")
    
    scheduled = st.session_state.scheduler.get_scheduled_emails()
    
    if scheduled:
        st.write(f"Total scheduled: {len(scheduled)}")
        
        for job in scheduled:
            with st.expander(f"📅 {job['time']} - {job['recipient']}"):
                st.write(f"**Subject:** {job['subject']}")
                st.write(f"**Status:** {job['status']}")
                
                if st.button(f"Cancel", key=f"cancel_{job['id']}"):
                    st.session_state.scheduler.cancel_email(job['id'])
                    st.success("Email cancelled!")
                    st.rerun()
    else:
        st.info("No scheduled emails.")