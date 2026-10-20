---
name: ses
description: Amazon SES standards for sending email, templates, DKIM/SPF/DMARC setup, bounce/complaint handling, and sandbox mode
user-invocable: false
stack: email/ses
paths:
  - "**/ses.*"
  - "**/ses-*"
  - "**/sesClient*"
  - "**/*-ses*"
  - "**/*Ses*"
  - "**/*email*"
  - "**/*mailer*"
  - "**/cdk/**"
---

Full standards in [ses.md](ses.md). Always-on summary:

**Setup:**
- Instantiate with `new SESClient({ credentials: fromEnv() })` — credentials come from IAM role env vars, never hardcoded access keys

**Sending:**
- Send with `new SendEmailCommand({ Source: 'noreply@yourdomain.com', Destination: ..., Message: { Body: { Text: { Data: ... }, Html: { Data: ... } }, Subject: ... } })`
- Always send from a verified identity in `Source:`; never send from unverified addresses
- Use `SendEmail` for simple messages, `SendTemplatedEmail` for parametrized content, `SendBulkTemplatedEmail` for campaigns
- Set `ReplyToAddresses` to a monitored mailbox — never set it to a no-reply-only address

**Authentication (DKIM / SPF / DMARC):**
- Enable DKIM Easy DKIM via SES console or CDK — use 2048-bit keys
- Publish SPF TXT record: `v=spf1 include:amazonses.com ~all`
- Publish DMARC TXT record: `v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com`
- Use a custom MAIL FROM domain to align SPF with your domain

**Bounces and complaints:**
- Configure an SNS topic for bounce and complaint notifications — never ignore them
- Hard bounces: immediately remove address from your send list
- Complaints: immediately unsubscribe; never re-send to complainants
- Keep bounce rate < 5% and complaint rate < 0.1% to stay out of Review

**Sandbox:**
- New accounts start in sandbox — verify destination addresses before moving to production
- Request production access via AWS Support before any bulk sends

**Never:**
- Never send marketing email to users who haven't opted in — CAN-SPAM / GDPR
- Never suppress bounce/complaint handling — your account will be suspended
- Never log email body or PII in CloudWatch

**Related skills:** logging-standards, security-principles, cdk
