# 📧 Email Setup Guide for Galaxium Travels

## Current Status
Your booking was successful, but the email was **logged to the console** instead of being sent to your inbox because the system is in **development mode** by default.

## Why You Didn't Receive the Email

The email feature has two modes:

1. **Console Mode (Default)** - Emails are printed to the terminal/console
2. **SMTP Mode** - Emails are sent via Gmail SMTP to actual email addresses

Currently, your booking confirmation email for **sudroych@in.ibm.com** was logged to the backend server console where the application is running.

## How to Enable Real Email Sending

### Option 1: Quick Setup with Gmail (Recommended)

1. **Create/Use a Gmail Account** for sending emails

2. **Enable 2-Factor Authentication**
   - Go to: https://myaccount.google.com/security
   - Enable 2-Step Verification

3. **Generate App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer" (or Other)
   - Copy the 16-character password

4. **Update `.env` File**
   
   Edit `galaxium-travels/booking_system_backend/.env`:
   ```env
   EMAIL_ENABLED=true
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-gmail@gmail.com
   SMTP_PASSWORD=your-16-char-app-password
   FROM_EMAIL=noreply@galaxiumtravels.com
   ```

5. **Restart the Backend Server**
   - Stop the current server (Ctrl+C)
   - Run: `cd galaxium-travels && start.bat` (Windows) or `./start.sh` (Linux/Mac)

### Option 2: Use Other SMTP Providers

You can use other email providers by updating the SMTP settings:

**Outlook/Hotmail:**
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=your-email@outlook.com
SMTP_PASSWORD=your-password
```

**Yahoo:**
```env
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USER=your-email@yahoo.com
SMTP_PASSWORD=your-app-password
```

**Custom SMTP Server:**
```env
SMTP_HOST=your-smtp-server.com
SMTP_PORT=587
SMTP_USER=your-username
SMTP_PASSWORD=your-password
```

## Testing Email Functionality

### Method 1: Make a New Booking
1. Ensure `.env` is configured with EMAIL_ENABLED=true
2. Restart the backend server
3. Make a new booking through the frontend
4. Check your email inbox (and spam folder)

### Method 2: Use the MCP Tool (Manual Email Sending)
If you want to resend the confirmation email for your existing booking:

1. Find your booking ID from the "My Bookings" page
2. Use the MCP tool `send_booking_confirmation_email(booking_id)`
3. Check your email inbox

### Method 3: Check Console Logs (Current Mode)
If you want to see the email that was sent to console:

1. Look at the terminal/console where the backend server is running
2. You should see output like:
   ```
   ================================================================================
   📧 EMAIL NOTIFICATION (Console Mode)
   ================================================================================
   To: sudroych@in.ibm.com
   Subject: 🚀 Galaxium Travels - Booking Confirmation #[ID]
   --------------------------------------------------------------------------------
   [Email content with your booking details]
   ================================================================================
   ```

## Troubleshooting

### Email Not Sending After Configuration

1. **Check `.env` file exists** in `booking_system_backend/` directory
2. **Verify EMAIL_ENABLED=true** (not "True" or "TRUE")
3. **Restart the server** after changing `.env`
4. **Check SMTP credentials** are correct
5. **Check spam/junk folder** in your email
6. **For Gmail**: Ensure you're using an App Password, not your regular password
7. **Check server logs** for error messages

### Common Errors

**"Authentication failed"**
- Wrong username or password
- For Gmail: Use App Password, not regular password
- For Gmail: Enable 2FA first

**"Connection refused"**
- Wrong SMTP host or port
- Firewall blocking outgoing SMTP connections
- Check if port 587 is open

**"Email logged to console"**
- EMAIL_ENABLED is not set to "true"
- SMTP_USER or SMTP_PASSWORD is empty
- Server needs restart after .env changes

## Security Notes

⚠️ **Important:**
- Never commit `.env` file to version control (it's in `.gitignore`)
- Use App Passwords, not your main email password
- Keep SMTP credentials secure
- The `.env.example` file is safe to commit (contains no real credentials)

## Email Template Preview

Your booking confirmation email includes:
- ✅ Booking ID
- ✅ Flight route (Origin → Destination)
- ✅ Departure and arrival times
- ✅ Price
- ✅ Booking timestamp
- ✅ Link to view bookings
- ✅ Professional HTML formatting

## Need Help?

If you continue to have issues:
1. Check the backend server console for error messages
2. Verify all environment variables are set correctly
3. Test with a simple booking first
4. Check your email provider's SMTP documentation