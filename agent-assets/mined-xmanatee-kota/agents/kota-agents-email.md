# Email Module

Outbound email notification channel for KOTA using SMTP (nodemailer).

- Subscribes to workflow and module bus events and sends formatted emails.
- Contributes an `email-alerts` ChannelDef that verifies SMTP on startup.
- Disabled gracefully when `smtp.host`, `from`, or `to` is absent in config.
- Credentials (`smtp.auth`) may be `$SMTP_USER` / `$SMTP_PASS` secret
  references; resolved values are never logged.
- Keep formatting behavior in `format.ts` and cover payload contracts with
  focused formatter tests.
- Optional channel filters must not suppress urgent owner/approval escalation
  notifications.
