---
name: leaddocket-email-config
description: >
  Configure email settings in LeadDocket — sender domain setup, email tracking,
  auto-reply rules for opportunities, and connecting email accounts. Use when
  setting up a new LeadDocket instance's email capabilities or troubleshooting
  email delivery. For sending emails programmatically via API see
  leaddocket-messages; for email templates see leaddocket-templates.
---

# LeadDocket — Email Configuration

LeadDocket's email system allows the firm to send tracked, logged emails to leads directly from the platform. Configuration happens in the admin UI.

> Support section: [Email](https://support.leaddocket.com/hc/en-us/sections/360009388032-Email)

---

## Email Setup (Admin, in the LeadDocket UI)

Navigate to **Settings → Email**

### Sender Domain Configuration

1. Add your firm's email domain (e.g., `@lawfirm.com`)
2. Add the required DNS records to your DNS provider:
   - **SPF record**: Authorizes LeadDocket to send on your domain
   - **DKIM record**: Cryptographically signs outgoing emails
   - **DMARC record**: (Recommended) Policy for unauthorized sends
3. Verify DNS records in the LeadDocket settings panel
4. Once verified, users can send as `name@lawfirm.com`

### Connecting Individual Email Accounts

Each user can connect their personal firm email account:

1. Navigate to **My Profile → Email Settings**
2. Click **Connect Email Account**
3. Authorize via OAuth (Google Workspace or Microsoft 365)
4. Sent emails from LeadDocket appear in the user's Sent folder

---

## Auto-Reply Configuration for Opportunities

LeadDocket can automatically send an email when a new opportunity is received.

1. Navigate to **Settings → Opportunities → Auto-Reply**
2. Enable auto-reply
3. Select a template (from `leaddocket-templates`)
4. Set sender name and address
5. Save

The auto-reply sends as soon as an opportunity is created, before any human reviews it.

---

## Email Tracking

LeadDocket tracks opens and clicks on emails sent through the platform:

| Metric | Where to view |
|--------|--------------|
| **Open tracking** | Lead's message feed (shows "Opened" status) |
| **Click tracking** | Individual message detail |
| **Delivery status** | Bounced/failed emails flagged in the message |

---

## Common Email Issues

| Issue | Resolution |
|-------|-----------|
| Emails going to spam | Verify SPF, DKIM, and DMARC records are set correctly |
| Sender shows as LeadDocket, not firm | Domain verification incomplete — add DNS records |
| Auto-reply not firing | Check that auto-reply is enabled and template is selected |
| Email bouncing | Check that the contact's email address is valid |

---

## Best Practices

- **Verify domain before going live**: Without domain verification, emails send from a LeadDocket address, which hurts deliverability and client trust.
- **Set up DMARC**: Even a permissive `p=none` DMARC policy improves deliverability and provides reporting on unauthorized sends.
- **Use templates for auto-reply**: The auto-reply should feel professional — use a designed template, not a plain text message.
- **Separate intake and attorney emails**: Configure separate auto-reply templates for opportunities vs. follow-ups to avoid sending retainer-stage emails at the inquiry stage.
