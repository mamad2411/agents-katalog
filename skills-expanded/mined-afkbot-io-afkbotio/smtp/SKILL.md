---
name: smtp
description: "Outbound email via `app.run` for `smtp`. Use when sending email and resolving SMTP credential profiles securely."
aliases:
  - smtp-send
  - email-send
triggers:
  - smtp
  - send email
  - send an email
  - email to
  - отправь письмо
  - отправь email
tool_names:
  - credentials.list
  - credentials.request
  - app.run
app_names:
  - smtp
preferred_tool_order:
  - credentials.list
  - credentials.request
  - app.run
requires_env:
  - AFKBOT_CREDENTIALS_MASTER_KEYS
---
# smtp

Use this skill for outbound email through unified tool `app.run`.

Tool methods:
- `app.run`
- `credentials.list`
- `credentials.request`

Supported actions (`app_name=smtp`):
- `send_email`

Credential set (per `profile_name`):
- required: `smtp_host`, `smtp_port`, `smtp_username`, `smtp_password`, `smtp_from_email`
- optional: `smtp_use_tls` (default `true`), `smtp_use_ssl` (default `false`)

Runtime params for `app.run`:
- `app_name=smtp`
- `action=send_email`
- `profile_name=<credential profile>` (optional; runtime auto-picks default or the only available profile)
- `params={to_email, subject, body, content_type?}`
- use top-level key `params`

Action payload contract:
- `send_email`
  - required: `to_email`, `subject`, `body`
  - optional: `content_type`, `host_credential_name`, `port_credential_name`, `username_credential_name`, `password_credential_name`, `from_email_credential_name`, `use_tls_credential_name`, `use_ssl_credential_name`

Preferred example:
```json
{
  "app_name": "smtp",
  "action": "send_email",
  "profile_name": "default",
  "params": {
    "to_email": "user@example.com",
    "subject": "Status update",
    "body": "Done",
    "content_type": "plain"
  }
}
```

Workflow:
1. Resolve `profile_name`:
   - explicit user choice -> use it;
   - otherwise let runtime auto-pick a single/default profile;
   - if multiple active profiles exist without one default, call `credentials.list` and ask user to choose.
2. Validate required credentials in selected profile.
3. For missing values, call `credentials.request` without `value` and let runtime switch to secure input.
4. Call `app.run` with action `send_email`.

Error handling:
- `credentials_missing` -> secure collection + retry.
- `credential_binding_conflict` -> ask user for explicit profile.
- `profile_policy_violation` -> host blocked by policy allowlist.
- `app_run_invalid` -> inspect missing/unexpected params and retry with corrected `params`.

Safety:
- SMTP password is always secret.
- Do not echo secret values in chat output.
- Runtime routes the correct skill automatically from `app_name`.
