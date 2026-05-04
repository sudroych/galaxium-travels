"""
Tests for email service functionality.
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import smtplib

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.email import EmailService, email_service
from models import User, Flight, Booking


class TestEmailService:
    """Test email service functions."""

    def test_email_service_initialization(self):
        """Test email service initializes with correct defaults."""
        service = EmailService()
        assert service.smtp_host == "smtp.gmail.com"
        assert service.smtp_port == 587
        assert service.from_email == "noreply@galaxiumtravels.com"
        assert service.enabled == False  # Default is false

    def test_console_mode_email(self, capsys):
        """Test email logging to console in development mode."""
        service = EmailService()
        service.enabled = False  # Ensure console mode
        
        result = service.send_booking_confirmation(
            to_email="test@example.com",
            user_name="Test User",
            booking_id=123,
            flight_origin="Earth",
            flight_destination="Mars",
            departure_time="2099-01-01T09:00:00Z",
            arrival_time="2099-01-01T17:00:00Z",
            price=1000000.00,
            booking_time="2099-01-01T08:00:00Z"
        )
        
        # Check result
        assert result["success"] == True
        assert result["method"] == "console"
        assert "test@example.com" in result["message"]
        
        # Check console output
        captured = capsys.readouterr()
        assert "📧 EMAIL NOTIFICATION" in captured.out
        assert "test@example.com" in captured.out
        assert "Test User" in captured.out
        assert "#123" in captured.out
        assert "Earth → Mars" in captured.out

    def test_html_email_template_generation(self):
        """Test HTML email template contains all required information."""
        service = EmailService()
        
        html = service._create_booking_email_html(
            user_name="John Doe",
            booking_id=456,
            flight_origin="Earth",
            flight_destination="Mars",
            departure_time="2099-01-01T09:00:00Z",
            arrival_time="2099-01-01T17:00:00Z",
            price=1500000.50,
            booking_time="2099-01-01T08:00:00Z"
        )
        
        # Check all required elements are present
        assert "John Doe" in html
        assert "#456" in html
        assert "Earth" in html
        assert "Mars" in html
        assert "2099-01-01T09:00:00Z" in html
        assert "2099-01-01T17:00:00Z" in html
        assert "$1,500,000.50" in html
        assert "<!DOCTYPE html>" in html
        assert "Booking Confirmed" in html

    def test_text_email_template_generation(self):
        """Test plain text email template contains all required information."""
        service = EmailService()
        
        text = service._create_booking_email_text(
            user_name="Jane Smith",
            booking_id=789,
            flight_origin="Mars",
            flight_destination="Jupiter",
            departure_time="2099-02-01T10:00:00Z",
            arrival_time="2099-02-01T20:00:00Z",
            price=2500000.75,
            booking_time="2099-02-01T09:00:00Z"
        )
        
        # Check all required elements are present
        assert "Jane Smith" in text
        assert "#789" in text
        assert "Mars" in text
        assert "Jupiter" in text
        assert "2099-02-01T10:00:00Z" in text
        assert "2099-02-01T20:00:00Z" in text
        assert "$2,500,000.75" in text
        assert "GALAXIUM TRAVELS" in text

    @patch('smtplib.SMTP')
    def test_smtp_email_success(self, mock_smtp):
        """Test successful email sending via SMTP."""
        # Setup mock
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Create service with SMTP enabled
        service = EmailService()
        service.enabled = True
        service.smtp_user = "test@gmail.com"
        service.smtp_password = "test_password"
        
        result = service.send_booking_confirmation(
            to_email="customer@example.com",
            user_name="Test Customer",
            booking_id=999,
            flight_origin="Earth",
            flight_destination="Venus",
            departure_time="2099-03-01T11:00:00Z",
            arrival_time="2099-03-01T15:00:00Z",
            price=800000.00,
            booking_time="2099-03-01T10:00:00Z"
        )
        
        # Verify result
        assert result["success"] == True
        assert result["method"] == "smtp"
        assert "customer@example.com" in result["message"]
        
        # Verify SMTP calls
        mock_smtp.assert_called_once_with("smtp.gmail.com", 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("test@gmail.com", "test_password")
        mock_server.send_message.assert_called_once()

    @patch('smtplib.SMTP')
    def test_smtp_email_failure(self, mock_smtp):
        """Test email sending failure handling."""
        # Setup mock to raise exception
        mock_smtp.return_value.__enter__.side_effect = smtplib.SMTPException("Connection failed")
        
        # Create service with SMTP enabled
        service = EmailService()
        service.enabled = True
        service.smtp_user = "test@gmail.com"
        service.smtp_password = "test_password"
        
        result = service.send_booking_confirmation(
            to_email="customer@example.com",
            user_name="Test Customer",
            booking_id=999,
            flight_origin="Earth",
            flight_destination="Venus",
            departure_time="2099-03-01T11:00:00Z",
            arrival_time="2099-03-01T15:00:00Z",
            price=800000.00,
            booking_time="2099-03-01T10:00:00Z"
        )
        
        # Verify failure is handled gracefully
        assert result["success"] == False
        assert result["method"] == "smtp"
        assert "Failed to send email" in result["message"]

    def test_singleton_instance(self):
        """Test that email_service is a singleton instance."""
        from services.email import email_service
        assert isinstance(email_service, EmailService)


class TestEmailIntegration:
    """Test email integration with booking system."""

    def test_booking_triggers_email(self, db_session, capsys):
        """Test that creating a booking triggers email sending."""
        from services.booking import book_flight
        
        # Setup test data
        db_session.add(User(name="Email Test User", email="emailtest@example.com"))
        db_session.add(Flight(
            origin="Earth",
            destination="Mars",
            departure_time="2099-01-01T09:00:00Z",
            arrival_time="2099-01-01T17:00:00Z",
            price=1000000,
            seats_available=5
        ))
        db_session.commit()
        
        user_obj = db_session.query(User).first()
        flight_obj = db_session.query(Flight).first()
        
        # Book flight
        result = book_flight(db_session, user_obj.user_id, "Email Test User", flight_obj.flight_id)
        
        # Verify booking succeeded
        assert result.status == "booked"
        
        # Verify email was logged to console (default mode)
        captured = capsys.readouterr()
        assert "📧 EMAIL NOTIFICATION" in captured.out
        assert "emailtest@example.com" in captured.out
        assert "Email Test User" in captured.out

    @patch('services.email.email_service.send_booking_confirmation')
    def test_booking_continues_on_email_failure(self, mock_send_email, db_session):
        """Test that booking succeeds even if email sending fails."""
        from services.booking import book_flight
        
        # Setup mock to raise exception
        mock_send_email.side_effect = Exception("Email service unavailable")
        
        # Setup test data
        db_session.add(User(name="Test User", email="test@example.com"))
        db_session.add(Flight(
            origin="Earth",
            destination="Mars",
            departure_time="2099-01-01T09:00:00Z",
            arrival_time="2099-01-01T17:00:00Z",
            price=1000000,
            seats_available=5
        ))
        db_session.commit()
        
        user_obj = db_session.query(User).first()
        flight_obj = db_session.query(Flight).first()
        
        # Book flight - should succeed despite email failure
        result = book_flight(db_session, user_obj.user_id, "Test User", flight_obj.flight_id)
        
        # Verify booking succeeded
        assert result.status == "booked"
        assert result.user_id == user_obj.user_id
        
        # Verify email was attempted
        mock_send_email.assert_called_once()


class TestMCPEmailTool:
    """Test MCP tool for sending booking confirmation emails."""

    def test_send_booking_confirmation_email_tool(self, db_session):
        """Test the MCP tool for sending booking confirmation emails."""
        from server import send_booking_confirmation_email
        
        # Setup test data
        db_session.add(User(name="MCP Test User", email="mcptest@example.com"))
        db_session.add(Flight(
            origin="Earth",
            destination="Mars",
            departure_time="2099-01-01T09:00:00Z",
            arrival_time="2099-01-01T17:00:00Z",
            price=1000000,
            seats_available=5
        ))
        db_session.commit()
        
        user_obj = db_session.query(User).first()
        flight_obj = db_session.query(Flight).first()
        
        # Create booking
        db_session.add(Booking(
            user_id=user_obj.user_id,
            flight_id=flight_obj.flight_id,
            status="booked",
            booking_time="2099-01-01T10:00:00Z"
        ))
        db_session.commit()
        
        booking_obj = db_session.query(Booking).first()
        
        # Send email via MCP tool
        result = send_booking_confirmation_email(booking_obj.booking_id)
        
        # Verify result
        assert result["success"] == True
        assert "method" in result

    def test_send_email_for_nonexistent_booking(self):
        """Test sending email for non-existent booking raises error."""
        from server import send_booking_confirmation_email
        
        with pytest.raises(Exception) as exc_info:
            send_booking_confirmation_email(99999)
        
        assert "not found" in str(exc_info.value).lower()

# Made with Bob
