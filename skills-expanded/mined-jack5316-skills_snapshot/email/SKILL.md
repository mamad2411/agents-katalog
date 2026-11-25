---
name: email
description: Email digest skill (placeholder - configure IMAP or email API). Use when user asks for email processing or /email.
---

# Email Skill (Placeholder)

Placeholder for email digest functionality.

## Configuration

To implement, choose one:

**Option 1: Gmail IMAP**
1. Enable IMAP in Gmail settings
2. Enable 2FA and create App Password
3. Add to .env:
   ```
   GMAIL_USER=your-email@gmail.com
   GMAIL_APP_PASSWORD=your-app-password
   ```

**Option 2: Email API Service**
- SendGrid, Mailgun, etc.

## Output

Future: `Sources/Email Digest - YYYY-MM-DD.md`
