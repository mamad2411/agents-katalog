---
name: email-header-injection-defenses
description: >
  Defend mail-sending paths against CRLF/email header injection by rejecting
  control characters, using structured mail APIs, and never concatenating
  untrusted data into raw SMTP or MIME headers. Use when hardening Subject, To,
  From, Cc, Bcc, Reply-To, or custom headers; contact forms; invite mailers —
  authorized org-owned systems only.
---

# Email Header Injection Defenses

## Scope And Authorization

- **In scope:** Application mailers and SMTP gateways you own; authorized security tests against those systems.
- **Out of scope:** Using injection to spam third parties or abuse shared ESP accounts without permission.
- Prefer staging with mail catchers (Mailhog, Mailpit, SES sandbox).
- Redact recipient addresses and message bodies in tickets.
- Pair with `email-otp-rate-limits` for abuse volume and `code-quality-standards` for code fixes.

## When To Use

- Contact forms, invite flows, or notifications that put user input into headers.
- Findings titled “email/CRLF header injection” or “SMTP header injection.”
- Raw string-built MIME messages vs SDK (`SendEmail` APIs).
- Custom headers (`X-Request-Id`, `Reply-To`) fed from clients.
- Reviewing legacy PHP `mail()` or shell-outs to `sendmail`.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| DMARC/SPF/DKIM operations | `email-dmarc-reporting-ops` |
| OTP send/verify rate limits | `email-otp-rate-limits` |
| Generic XSS/SQLi | respective injection skills |
| EML parser issues | `eml-header-injection-defense` if parsing inbound EML |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Dangerous chars | CR (`\r`), LF (`\n`), NUL; sometimes Unicode line separators |
| Headers | Never concatenate untrusted strings into header blocks |
| Libraries | Use address objects / SDK fields, not raw MIME assembly |
| Subject | Strip control chars; length-limit; encode via library |
| Recipients | Validate email syntax; allowlist domains if business requires |
| Transport | Authenticated SMTP/API; no open relay |

## Workflow

### 1. Confirm scope and success criteria

1. List all code paths that send email (grep mail SDKs, SMTP clients).
2. Success: injected CRLF cannot add `Bcc:`/`Cc:`/`Subject:` lines; tests cover payloads.

### 2. Inventory mail construction

```bash
rg -n "sendmail|SendEmail|nodemailer|smtp|mime|Subject:|Reply-To" --glob '!node_modules' -i
rg -n "mail\\(|Message\\(|MailMessage" --glob '!vendor' 
```

1. Flag string templates that build raw headers.
2. Note any shell invocation with user-controlled subject/body.

### 3. Baseline attack patterns (authorized lab)

| Payload idea | Goal |
| --- | --- |
| `test@ex.com\nBcc: victim@ex.com` | Extra recipients |
| `Hello\r\nSubject: pwned` | Override subject |
| Subject with nested headers | Duplicate header confusion |

1. Reproduce only against catcher/staging.
2. Capture resulting raw MIME from the catcher as evidence.

### 4. Apply defenses

```python
# Python sketch — validate before SDK
import re
CONTROL = re.compile(r"[\r\n\x00]")

def sanitize_header_value(value: str, max_len: int = 200) -> str:
    if CONTROL.search(value):
        raise ValueError("invalid header characters")
    value = value.strip()
    if len(value) > max_len:
        raise ValueError("header too long")
    return value

# Prefer structured API:
# client.send_email(Source=..., Destination={"ToAddresses":[to]}, Message={...})
# never: raw = f"To: {user_input}\r\nSubject: ..."
```

```js
// nodemailer — pass fields, do not build raw headers from users
await transporter.sendMail({
  to: validatedEmail,
  subject: sanitize(subject),
  replyTo: validatedReplyTo, // optional
  text: body,
});
```

1. Reject on validation error (400)—do not silently strip if silent strip still allows clever encodings; prefer reject.
2. Encode subjects via library (RFC 2047) rather than manual UTF-8 glue.
3. Disallow user-controlled arbitrary custom header **names**.
4. For `Reply-To`, validate as email; do not accept multi-line.

### 5. Framework-specific notes

| Stack | Tip |
| --- | --- |
| Java `MimeMessage` | Use `InternetAddress` + `setSubject(s, charset)` |
| .NET `MailMessage` | Set properties; avoid raw `Headers.Add` with user names |
| PHP | Avoid `mail()` header concatenation; use maintained MIME libs |
| Go | `net/mail` Address parsing; `mime.QEncoding` |

### 6. Verify with evidence

```bash
# Unit tests with payloads containing \r\n in subject/to
# Integration: assert catcher message has single Subject and expected recipients only
```

1. Regression tests for each mailer entrypoint.
2. SAST/semgrep rules for raw header concatenation if available.
3. Confirm ESP side does not re-enable injection via custom X-headers API misuse.

### 7. Hand off

1. Code owners for notification service.
2. Logging: never log full raw MIME with PII by default.
3. Link rate limits to stop abuse even when injection is fixed.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Construction | SDK fields + validators | `headers = "To: " + user` |
| CRLF | Reject | Strip partially / allow `\n` |
| Reply-To | Validated single address | Free-text from client |
| Custom headers | Server-defined names only | Client picks header keys |
| Tests | CRLF fixtures in CI | Manual “looks fine” |

## Output Checklist

- [ ] All outbound mail paths inventoried
- [ ] No raw header concatenation from untrusted input
- [ ] Control-character validation in place
- [ ] Lab evidence of blocked injection
- [ ] Automated regression tests
- [ ] Custom header policy documented
- [ ] Residual risk (ESP features) noted

## Rules

- Authorized testing only; no real-world spam proofs.
- Prefer structured mail APIs over string MIME.
- Fail closed on invalid header content.
- Inbound EML parsing is a separate concern (`eml-header-injection-defense`).
- Redact recipients in evidence.
