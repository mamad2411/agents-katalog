---
name: sender-authentication
description: Use this skill when the user is setting up or configuring SendGrid Sender Authentication (Domain Authentication, Link Branding).
---

# SendGrid Sender Authentication

This skill provides guidelines for configuring Sender Authentication in SendGrid.

## Overview
Sender Authentication proves to mailbox providers (like Gmail, Yahoo) that SendGrid is authorized to send emails on behalf of your domain. This is critical for deliverability.

## Key Concepts
1. **Domain Authentication**: Involves adding CNAME records to your DNS settings. This configures SPF and DKIM for your domain.
2. **Link Branding**: Replaces the default `sendgrid.net` click-tracking links with your own custom domain (e.g., `click.yourdomain.com`).
3. **Reverse DNS (Dedicated IP)**: Maps your dedicated IP address to your domain.

## Best Practices
- **Automated Security**: SendGrid handles DKIM rotation automatically if you use their automated security CNAME records.
- **DNS Propagation**: DNS changes can take up to 48 hours to propagate. If validation fails initially in the SendGrid UI, instruct the user to wait and retry.
- **DMARC Compliance**: Domain authentication is required for your emails to pass DMARC alignment checks, which is mandatory for sending to many major inbox providers as of 2024.

## Troubleshooting
- Ensure no conflicting SPF records exist. Only one TXT record starting with `v=spf1` should exist at the root of the domain.
- Verify CNAME records using standard CLI tools like `dig` or `nslookup`.
