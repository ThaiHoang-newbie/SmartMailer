import schedule
import threading
import time
from datetime import datetime
from services.email_sender import EmailSender
import uuid

class EmailScheduler:
    def __init__(self):
        self.jobs = {}
        self.running = False
        self.thread = None
        
    def schedule_email(self, send_time, recipient, subject, body, image_path, 
                      sender_email, password, smtp_server, smtp_port):
        """
        Schedule an email to be sent at a specific time
        
        Args:
            send_time: datetime object for when to send
            recipient: Recipient email
            subject: Email subject
            body: Email body
            image_path: Path to image attachment
            sender_email: Sender's email
            password: Sender's password
            smtp_server: SMTP server
            smtp_port: SMTP port
        """
        job_id = str(uuid.uuid4())
        
        # Create job function
        def send_job():
            sender = EmailSender(sender_email, password, smtp_server, smtp_port)
            success = sender.send_email(recipient, subject, body, image_path)
            
            if success:
                self.jobs[job_id]['status'] = 'Sent'
            else:
                self.jobs[job_id]['status'] = 'Failed'
        
        # Calculate time until send
        now = datetime.now()
        if send_time > now:
            # Schedule the job
            schedule_time_str = send_time.strftime('%H:%M')
            schedule.every().day.at(schedule_time_str).do(send_job).tag(job_id)
            
            # Store job info
            self.jobs[job_id] = {
                'id': job_id,
                'time': send_time,
                'recipient': recipient,
                'subject': subject,
                'status': 'Scheduled'
            }
            
            # Start scheduler if not running
            if not self.running:
                self._start_scheduler()
            
            return job_id
        else:
            # Send immediately if time has passed
            sender = EmailSender(sender_email, password, smtp_server, smtp_port)
            sender.send_email(recipient, subject, body, image_path)
            return None
    
    def cancel_email(self, job_id):
        """Cancel a scheduled email"""
        if job_id in self.jobs:
            schedule.clear(job_id)
            self.jobs[job_id]['status'] = 'Cancelled'
            return True
        return False
    
    def get_scheduled_emails(self):
        """Get list of all scheduled emails"""
        return [job for job in self.jobs.values() if job['status'] == 'Scheduled']
    
    def _start_scheduler(self):
        """Start the background scheduler thread"""
        self.running = True
        
        def run_scheduler():
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        
        self.thread = threading.Thread(target=run_scheduler, daemon=True)
        self.thread.start()
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.running = False
        if self.thread:
            self.thread.join()