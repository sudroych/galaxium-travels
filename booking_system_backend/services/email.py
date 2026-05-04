"""
Email service for sending booking confirmation emails.
Supports both SMTP and console logging for development.
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class EmailService:
    """Service for sending emails via SMTP or console logging."""
    
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@galaxiumtravels.com")
        self.enabled = os.getenv("EMAIL_ENABLED", "false").lower() == "true"
    
    def send_booking_confirmation(
        self,
        to_email: str,
        user_name: str,
        booking_id: int,
        flight_origin: str,
        flight_destination: str,
        departure_time: str,
        arrival_time: str,
        price: float,
        booking_time: str
    ) -> dict:
        """
        Send a booking confirmation email.
        
        Args:
            to_email: Recipient email address
            user_name: Name of the user who made the booking
            booking_id: Unique booking ID
            flight_origin: Flight origin location
            flight_destination: Flight destination location
            departure_time: Flight departure time
            arrival_time: Flight arrival time
            price: Ticket price
            booking_time: Time when booking was made
            
        Returns:
            dict: Status of email sending operation
        """
        subject = f"🚀 Galaxium Travels - Booking Confirmation #{booking_id}"
        
        # Create HTML email body
        html_body = self._create_booking_email_html(
            user_name=user_name,
            booking_id=booking_id,
            flight_origin=flight_origin,
            flight_destination=flight_destination,
            departure_time=departure_time,
            arrival_time=arrival_time,
            price=price,
            booking_time=booking_time
        )
        
        # Create plain text version
        text_body = self._create_booking_email_text(
            user_name=user_name,
            booking_id=booking_id,
            flight_origin=flight_origin,
            flight_destination=flight_destination,
            departure_time=departure_time,
            arrival_time=arrival_time,
            price=price,
            booking_time=booking_time
        )
        
        if self.enabled and self.smtp_user and self.smtp_password:
            return self._send_smtp_email(to_email, subject, html_body, text_body)
        else:
            return self._log_email_to_console(to_email, subject, text_body)
    
    def _send_smtp_email(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: str
    ) -> dict:
        """Send email via SMTP."""
        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.from_email
            msg["To"] = to_email
            
            # Attach both plain text and HTML versions
            part1 = MIMEText(text_body, "plain")
            part2 = MIMEText(html_body, "html")
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            return {
                "success": True,
                "message": f"Email sent successfully to {to_email}",
                "method": "smtp"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to send email: {str(e)}",
                "method": "smtp"
            }
    
    def _log_email_to_console(
        self,
        to_email: str,
        subject: str,
        text_body: str
    ) -> dict:
        """Log email to console (for development/testing)."""
        print("\n" + "="*80)
        print("📧 EMAIL NOTIFICATION (Console Mode)")
        print("="*80)
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print("-"*80)
        print(text_body)
        print("="*80 + "\n")
        
        return {
            "success": True,
            "message": f"Email logged to console for {to_email}",
            "method": "console"
        }
    
    def _create_booking_email_html(
        self,
        user_name: str,
        booking_id: int,
        flight_origin: str,
        flight_destination: str,
        departure_time: str,
        arrival_time: str,
        price: float,
        booking_time: str
    ) -> str:
        """Create HTML email body for booking confirmation."""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #6366F1 0%, #EC4899 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }}
        .booking-details {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .detail-row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #e5e7eb; }}
        .detail-label {{ font-weight: bold; color: #6366F1; }}
        .footer {{ text-align: center; padding: 20px; color: #6b7280; font-size: 12px; }}
        .button {{ background: #6366F1; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; display: inline-block; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Booking Confirmed!</h1>
            <p>Your interplanetary journey awaits</p>
        </div>
        <div class="content">
            <h2>Hello {user_name},</h2>
            <p>Thank you for choosing Galaxium Travels! Your booking has been confirmed.</p>
            
            <div class="booking-details">
                <h3>Booking Details</h3>
                <div class="detail-row">
                    <span class="detail-label">Booking ID:</span>
                    <span>#{booking_id}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Route:</span>
                    <span>{flight_origin} → {flight_destination}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Departure:</span>
                    <span>{departure_time}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Arrival:</span>
                    <span>{arrival_time}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Price:</span>
                    <span>${price:,.2f}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Booked On:</span>
                    <span>{booking_time}</span>
                </div>
            </div>
            
            <p><strong>Important:</strong> Please arrive at the spaceport at least 2 hours before departure for security checks and boarding procedures.</p>
            
            <center>
                <a href="http://localhost:5173/my-bookings" class="button">View My Bookings</a>
            </center>
        </div>
        <div class="footer">
            <p>Galaxium Travels - Explore the cosmos, one booking at a time!</p>
            <p>This is an automated message. Please do not reply to this email.</p>
        </div>
    </div>
</body>
</html>
"""
    
    def _create_booking_email_text(
        self,
        user_name: str,
        booking_id: int,
        flight_origin: str,
        flight_destination: str,
        departure_time: str,
        arrival_time: str,
        price: float,
        booking_time: str
    ) -> str:
        """Create plain text email body for booking confirmation."""
        return f"""
🚀 GALAXIUM TRAVELS - BOOKING CONFIRMATION
{'='*60}

Hello {user_name},

Thank you for choosing Galaxium Travels! Your booking has been confirmed.

BOOKING DETAILS
{'='*60}
Booking ID:     #{booking_id}
Route:          {flight_origin} → {flight_destination}
Departure:      {departure_time}
Arrival:        {arrival_time}
Price:          ${price:,.2f}
Booked On:      {booking_time}
{'='*60}

IMPORTANT: Please arrive at the spaceport at least 2 hours before 
departure for security checks and boarding procedures.

View your bookings at: http://localhost:5173/my-bookings

{'='*60}
Galaxium Travels - Explore the cosmos, one booking at a time!
This is an automated message. Please do not reply to this email.
"""


# Singleton instance
email_service = EmailService()

# Made with Bob
