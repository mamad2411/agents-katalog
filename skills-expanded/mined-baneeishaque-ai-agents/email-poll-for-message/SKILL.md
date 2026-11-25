---
name: email-poll-for-message
description: >-
  Poll an IMAP mailbox until a matching email arrives (subject/from/unseen
  criteria) using the poll-until base engine with a one-shot IMAP search as the
  check command. Provider-agnostic; Gmail and other providers layer presets on
  top. Includes an offline fixture mode.
category: Email
---

# Email Poll For Message Skill (v1)

> **Skill ID:** `email-poll-for-message`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Composer (per [`skill-factory` §2.0 Layering Decision](../../skill-factory/SKILL.md))

## Description

Polls an IMAP mailbox until a matching email arrives. A one-shot search script
(`search-messages.py`) is used as the check command of the
[`poll-until`](../../general/polling/poll-until/SKILL.md) base engine, so the wait
is bounded and every attempt is recorded as JSONL. Matching messages are
emitted with `uid`, `subject`, `from`, and `date`. Provider presets (e.g. the
[`gmail-poll-for-message`](../gmail-poll-for-message/SKILL.md) preset) fix the
IMAP endpoint and credential conventions.

## Composition Rationale

The bounded retry loop, attempt budget, and JSONL timeline belong to the base
engine; this skill contributes the mailbox-specific check — an IMAP search with
subject/from/unseen filters — plus the credential convention (password via
environment variable only). IMAP is the provider-agnostic layer: it works for
any mailbox host with zero provider SDKs, and provider-specific conveniences
become thin presets over this skill.

## Related Skills

- [`gmail-event-email-to-ics`](../../calendar/gmail-event-email-to-ics/SKILL.md)
  — turns event-invitation emails into calendar files; complementary mailbox
  workflow.
- [`github-api-poll-until`](../../github/github-api-poll-until/SKILL.md) — the API
  analogue of this composite (same base engine).

## 1. When to Apply

Use this skill whenever an incoming email is the signal that an asynchronous
external process has progressed:

- Wait for a repository-transfer confirmation email (the acceptance step is
  email-based).
- Wait for a sign-up / verification / 2FA message during automation.
- Wait for any human-triggered confirmation mail with a known subject fragment.

**Anti-trigger:** Sending email, parsing attachments, or managing mailbox
folders are out of scope. If the mailbox is Gmail, prefer the
[`gmail-poll-for-message`](../gmail-poll-for-message/SKILL.md) preset.

## 2. Why IMAP Polling (Not a Provider API)

| Option | Verdict | Reason |
| --- | --- | --- |
| Manual inbox refresh | ❌ | not automatable; no verdict record |
| Provider API (Gmail API, Microsoft Graph) | ⚠️ | capable but per-provider auth/setup; overkill for "wait for one email" |
| IMAP + this composite | ✅ | provider-agnostic (stdlib `imaplib`); bounded budget; JSONL match records; presets layer on top |

Language tier: **Python 3 (Tier 1)** per
[`scripting-language-selection-rules.md` §2](../../../../ai-agent-rules/scripting-language-selection-rules.md).

## 3. Required Inputs & Environment

| Requirement | Minimum | Notes |
| --- | --- | --- |
| IMAP endpoint | host + port | port `993` (SSL) by default; `--no-ssl` for plain/STARTTLS hosts |
| Mailbox username | `--username` | the mailbox login (may differ from the address) |
| Password | environment variable | name given by `--password-env` (default `EMAIL_PASSWORD`); **never** passed as a CLI argument |
| Match criteria | optional | `--subject-contains`, `--from-contains`, `--unseen`, `--since-days` |
| Python | 3.12+ | pure stdlib (`imaplib`, `email`); no pip dependencies |

Gmail note: Gmail requires an app password for IMAP; see the
[`gmail-poll-for-message`](../gmail-poll-for-message/SKILL.md) preset for the
exact conventions.

## 4. Operational Logic

### 4.1 Script catalogue

| Script | Role | Exit codes |
| --- | --- | --- |
| `scripts/search-messages.py` | one-shot IMAP search (the check command); `--source-file` runs the same filters over a JSONL fixture offline | `0` match · `1` no match · `2` config/connection error |
| `scripts/poll-email-message.py` | composite driver — shells `poll-until.py` with the search as check | `0` arrived · `1` exhausted · `2` config error |

### 4.2 CLI contract (driver)

```bash
python3 scripts/poll-email-message.py --imap-host <host> --username <user> \
    [--subject-contains <text>] [--from-contains <text>] [--unseen] \
    [--interval 30] [--attempts 20] [--password-env EMAIL_PASSWORD]
```

| Option | Default | Purpose |
| --- | --- | --- |
| `--imap-host` / `--imap-port` | port `993` | IMAP endpoint |
| `--username` | required | mailbox login |
| `--password-env <name>` | `EMAIL_PASSWORD` | environment variable holding the password |
| `--mailbox <name>` | `INBOX` | mailbox to search |
| `--subject-contains` / `--from-contains` | — | case-insensitive substring filters |
| `--unseen` | off | only unseen messages |
| `--since-days <n>` | — | server-side SINCE prefilter |
| `--interval` / `--attempts` | `30` / `20` | base-engine budget |
| `--source-file <jsonl>` | — | offline fixture mode (no IMAP) |
| `--ssl` / `--no-ssl` | `--ssl` | transport selection |

### 4.3 Output contract

The search script emits one JSON object per match; the driver streams the base
engine's per-attempt JSONL and ends with a summary line. Exit `0` = a matching
message arrived.

```json
{"uid": "4821", "subject": "Repository transfer", "from": "<sender>", "date": "Wed, 30 Sep 2026 12:35:00 +0000", "source": "imap"}
{"verdict": "arrived", "attempts": 2, "label": "email"}
```

### 4.4 End-to-end examples

```bash
SCRIPTS=.agents/skills/email/email-poll-for-message/scripts

EMAIL_PASSWORD='<app-password>' python3 "$SCRIPTS"/poll-email-message.py \
    --imap-host <imap-host> --username <mailbox-user> \
    --subject-contains 'transfer' --interval 30 --attempts 20

# Offline fixture mode (no network):
python3 "$SCRIPTS"/poll-email-message.py --source-file fixtures.jsonl \
    --subject-contains transfer --interval 1 --attempts 1
```

## 5. Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`gmail-poll-for-message`](../gmail-poll-for-message/SKILL.md) | Shells out to `poll-email-message.py` with the Gmail IMAP endpoint (`imap.gmail.com:993`) and the Gmail credential convention (`GMAIL_APP_PASSWORD`); passes criteria and polling knobs through unchanged. |

## 6. Composition by This Skill

| Base | Invoked As | Supplied | Consumed Back |
| --- | --- | --- | --- |
| [`poll-until`](../../general/polling/poll-until/SKILL.md) | `poll-until.py --interval … --attempts … -- <check>` | `search-messages.py` (this skill's own check script) with the mailbox criteria | per-attempt JSONL (streamed through) + final exit code |

## 7. Prohibited Behaviors

- Passing passwords as command-line arguments — environment variables only.
- Re-implementing the polling loop — shell out to `poll-until.py` (see §6).
- Storing or logging credentials — the password is read from the environment at
  call time and never persisted.
- Marking messages as read — searches run read-only (`readonly=True` select,
  `BODY.PEEK`).

## 8. Change History

| Timestamp | Summary of Changes | Rationale |
| --- | --- | --- |
| [2026-09-30 15:55] | Initial skill v1 created | Transfer confirmations are email-based; a provider-agnostic IMAP waiter was needed, with the Gmail preset layered on top |

## 9. Traceability

See [`TRACEABILITY.md`](TRACEABILITY.md) for session logs and provenance.

## 10. Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release history.
