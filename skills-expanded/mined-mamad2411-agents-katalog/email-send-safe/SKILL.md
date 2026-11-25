---
name: email-send-safe
description: Securely send emails via SMTP with mandatory confirmation step, content sanitization, and attachment size limits. Prevents accidental mass-mailing and sensitive data leakage through strict guardrails.
---

# Safe Email Sending SOP

Securely send emails via SMTP with mandatory confirmation step, content sanitization, and attachment size limits. Prevents accidental mass-mailing and sensitive data leakage through strict guardrails.

## When to Use

- User wants to send email
- User wants to email send
- User wants to compose email
- Keywords: email, smtp, send, safe, communication

## Required Parameters

- **to** (string): Recipient email address (single address only for safety)
- **subject** (string): Email subject line
- **body** (string): Email body content (plain text)
- **smtp_host** (string): SMTP server hostname
- **smtp_user** (string): SMTP authentication username
- **smtp_pass** (string): SMTP authentication password

## Optional Parameters

- **smtp_port** (number): SMTP server port (default: 587)
- **from_name** (string): Sender display name
- **attachment_path** (string): Optional file path for a single attachment
- **require_confirmation** (boolean): Whether to require human confirmation before sending (default: True)

## Output

- **sent** (boolean): Whether the email was successfully sent
- **message_id** (string): SMTP message ID if sent
- **sanitized_fields** (array): List of fields that were sanitized

## Security

- Sandbox level: strict
- Max execution time: 30000ms
- Network whitelist: smtp.gmail.com, smtp.qq.com, smtp.163.com, smtp.outlook.com, smtp.office365.com, smtp.mail.yahoo.com
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `validate_recipient` -> 16 steps -> Exit: `return_success`, `abort_invalid_email`, `abort_multi_recipient`, `abort_attachment_too_large`, `abort_not_confirmed`
