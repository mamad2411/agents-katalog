---
name: devkinsta-email-testing
description: Instructions for using DevKinsta's local email testing inbox.
---

# DevKinsta Email Testing

DevKinsta includes a built-in local email testing tool (powered by MailHog/Mailpit behind the scenes) that intercepts all outgoing emails from your local WordPress sites. This allows you to test email functionality safely without spamming real email addresses.

## How to Access the Email Inbox
1. Open DevKinsta.
2. Navigate to the left sidebar and click on the **Email Inbox** icon (the envelope).
3. The inbox will display a list of all emails sent by any local site managed by DevKinsta.

## Testing Outgoing Emails
1. Trigger an email from your local WordPress site (e.g., password reset, contact form submission, WooCommerce order receipt).
2. The email will *not* be routed to the actual recipient. Instead, it is caught by DevKinsta's internal SMTP server.
3. Switch back to the **Email Inbox** in DevKinsta.
4. Click on the captured email to view its details, including the sender, recipient, subject, headers, and the HTML/plain text body.

## Troubleshooting
- If emails are not appearing, ensure that your WordPress site is not using a custom SMTP plugin configured to send emails via an external API (like SendGrid or Mailgun). DevKinsta's inbox only catches emails sent via the default PHP `mail()` function or internal SMTP.
