---
name: imap
description: "Mailbox search via `app.run` for `imap`. Use when searching email messages in IMAP mailboxes and resolving the needed credential profile."
aliases:
  - imap-search
  - email-search
  - mail
  - email
  - почта
triggers:
  - imap
  - через imap
  - search email
  - find email
  - search mailbox
  - list emails
  - list mail
  - get emails
  - inbox
  - найди письмо
  - поиск писем
  - список писем
  - получи письма
  - письма с почты
  - список писем с почты
tool_names:
  - credentials.list
  - credentials.request
  - app.run
app_names:
  - imap
preferred_tool_order:
  - credentials.list
  - credentials.request
  - app.run
requires_env:
  - AFKBOT_CREDENTIALS_MASTER_KEYS
---
# imap

Use this skill for mailbox search via unified tool `app.run`.

Tool methods:
- `app.run`
- `credentials.list`
- `credentials.request`

Supported actions (`app_name=imap`):
- `search_messages`

Credential set (per `profile_name`):
- required: `imap_host`, `imap_port`, `imap_username`, `imap_password`
- optional: `imap_use_ssl` (default `true`)

Runtime params for `app.run`:
- `app_name=imap`
- `action=search_messages`
- `profile_name=<credential profile>` (optional; runtime auto-picks default or the only available profile)
- `params={query?, mailbox?, limit?}`
- use top-level key `params`

Action payload contract:
- `search_messages`
  - required: none
  - optional: `query`, `mailbox`, `limit`, `host_credential_name`, `port_credential_name`, `username_credential_name`, `password_credential_name`, `use_ssl_credential_name`

Preferred example:
```json
{
  "app_name": "imap",
  "action": "search_messages",
  "profile_name": "default",
  "params": {
    "query": "UNSEEN",
    "mailbox": "INBOX",
    "limit": 10
  }
}
```

Workflow:
1. Resolve credential profile:
   - explicit user choice -> use it;
   - otherwise let runtime auto-pick a single/default profile;
   - if multiple active profiles exist without one default, use `credentials.list` and ask user to choose.
2. Verify required IMAP credentials in selected profile.
3. For missing values, call `credentials.request` without `value` and let runtime switch to secure input.
4. Execute `app.run` action `search_messages`.
5. Do not ask the user to paste IMAP secrets into normal chat text. Use the secure credential flow instead.
6. For mailbox-listing requests, prefer the deterministic sequence:
   - `credentials.list`
   - `credentials.request` for missing bindings
   - `app.run(app_name=imap, action=search_messages, params={mailbox: "INBOX", limit: <small number>})`

Error handling:
- `credentials_missing` -> secure collection + retry.
- `credential_binding_conflict` -> ask for exact profile.
- `profile_policy_violation` -> blocked host by policy.
- `app_run_invalid` -> inspect missing/unexpected params and retry with corrected `params`.

Safety:
- Never print IMAP password in plain output.
- Do not ask for IMAP host/user/password in normal chat when `credentials.request` can collect them securely.
- Runtime routes the correct skill automatically from `app_name`.
