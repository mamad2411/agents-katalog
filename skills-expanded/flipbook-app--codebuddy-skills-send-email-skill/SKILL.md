---
name: send-email
description: Use when the user wants to send an email, deliver a notification/report by email, or email a file's contents. Sends via SMTP using credentials from environment variables (SMTP_HOST/PORT/USER/TOKEN). Defaults to the 163 mailbox configured in this environment.
---

# send-email

Send email via SMTP. Credentials come from environment variables, never hardcoded.

## Credentials (environment variables)

| Var | Meaning | Example |
|-----|---------|---------|
| `SMTP_HOST` | SMTP server | `smtp.163.com` |
| `SMTP_PORT` | port — `465` = SSL, `587` = STARTTLS | `465` |
| `SMTP_USER` | login user / default From | `imcuttle@163.com` |
| `SMTP_TOKEN` | authorization code / app password (NOT login password for 163/QQ) | — |
| `SMTP_FROM` | optional, overrides From | — |

## Usage

```bash
python3 ./scripts/send_email.py \
  --to imcuttle@163.com \
  --subject "主题" \
  --body "正文文本"
```

Other body sources and options:
- `--body-file /path/to/body.txt` — read body from a file
- piped stdin: `echo "正文" | ... send_email.py --to a@x.com --subject "Hi"`
- `--html` — treat body as HTML
- `--to` / `--cc` / `--bcc` — repeatable for multiple recipients
- `--from` — override the From address

Run `python3 ./scripts/send_email.py --help` for the full list.

## Notes

- Port 465 → SSL (`SMTP_SSL`); any other port → plain SMTP + STARTTLS.
- Prints `OK: sent from ... to ... via host:port` on success; exits non-zero with an `ERROR:` line if a credential env var is missing.
- Never echo `SMTP_TOKEN`; only read it from the environment.
