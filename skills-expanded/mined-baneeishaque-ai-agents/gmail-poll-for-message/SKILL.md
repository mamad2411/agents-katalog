---
name: gmail-poll-for-message
description: >-
  Gmail preset: poll a Gmail mailbox until a matching email arrives, fixing the
  Gmail IMAP endpoint (imap.gmail.com:993) and the app-password credential
  convention on top of email-poll-for-message. Gmail API / MCP noted as
  alternatives.
category: Email
---

# Gmail Poll For Message Skill (v1)

> **Skill ID:** `gmail-poll-for-message`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Composer (per [`skill-factory` §2.0 Layering Decision](../../skill-factory/SKILL.md))

## Description

A Gmail preset over
[`email-poll-for-message`](../email-poll-for-message/SKILL.md): the IMAP
endpoint is fixed to `imap.gmail.com:993` and the credential convention to the
`GMAIL_APP_PASSWORD` environment variable. Criteria and polling knobs pass
through unchanged. The Gmail API and Google Workspace MCP tools are documented
as alternatives when OAuth-based access is available.

## Composition Rationale

Gmail is the concrete provider behind the generic IMAP composite: every step
(endpoint, credential name, prerequisites) is a fixed choice, not new logic.
Keeping the preset thin means the base composite carries all behavior, and
other providers (Outlook/Microsoft 365, Fastmail, …) can be added as sibling
presets with the same shape.

## Related Skills

- [`gmail-event-email-to-ics`](../../calendar/gmail-event-email-to-ics/SKILL.md)
  — turns event-invitation emails into calendar files (complementary Gmail
  workflow).
- [`google-workspace-mcp-account-switch`](../../mcp/google-workspace-mcp-account-switch/SKILL.md)
  — switches the Google Workspace MCP account when the API/MCP route is chosen
  instead of IMAP.

## 1. When to Apply

Use this skill when the mailbox to watch is Gmail:

- Wait for a Gmail-delivered confirmation email (e.g., a repository-transfer
  confirmation sent to a Gmail address).
- Wait for verification codes or notification mails from automated workflows.
- Test mailbox-waiting logic offline with `--source-file` (fixture passthrough).

**Anti-trigger:** For non-Gmail mailboxes, use the base
[`email-poll-for-message`](../email-poll-for-message/SKILL.md) directly. Sending
email is out of scope.

## 2. Why the IMAP Preset (vs Gmail API / MCP)

| Option | Verdict | Reason |
| --- | --- | --- |
| Gmail API / Google Workspace MCP | ⚠️ | richer (labels, search syntax) but requires OAuth setup and an MCP/API session; documented alternative |
| Base IMAP composite without preset | ⚠️ | works, but every caller must remember Gmail's endpoint and credential conventions |
| This Gmail preset | ✅ | zero provider SDKs; app password only; same bounded engine and JSONL records as every other waiter |

Gmail prerequisites: IMAP must be enabled in Gmail settings and an **app
password** must be created (regular account passwords are rejected for IMAP).

Language tier: **Python 3 (Tier 1)** per
[`scripting-language-selection-rules.md` §2](../../../../ai-agent-rules/scripting-language-selection-rules.md).

## 3. Required Inputs & Environment

| Requirement | Minimum | Notes |
| --- | --- | --- |
| Gmail address | `--username <address>` | the mailbox to search |
| App password | `GMAIL_APP_PASSWORD` env var (override name via `--password-env`) | created in Gmail account settings; **never** passed as a CLI argument |
| Match criteria | optional | `--subject-contains`, `--from-contains`, `--unseen`, `--since-days` |
| Python | 3.12+ | pure stdlib; no pip dependencies |

## 4. Operational Logic

### 4.1 Script catalogue

| Script | Role | Exit codes |
| --- | --- | --- |
| `scripts/poll-gmail-message.py` | preset driver — shells the `email-poll-for-message` driver with Gmail endpoint + credential conventions | `0` arrived · `1` exhausted · `2` config error |

### 4.2 CLI contract

```bash
python3 scripts/poll-gmail-message.py --username <gmail-address> \
    [--subject-contains <text>] [--interval 30] [--attempts 20]
```

| Option | Default | Purpose |
| --- | --- | --- |
| `--username <address>` | required (unless `--source-file`) | Gmail address |
| `--password-env <name>` | `GMAIL_APP_PASSWORD` | environment variable holding the app password |
| `--mailbox` / `--limit` | `INBOX` / `20` | passthrough |
| `--subject-contains` / `--from-contains` / `--unseen` / `--since-days` | — | criteria passthrough |
| `--interval` / `--attempts` | `30` / `20` | base-engine budget passthrough |
| `--source-file <jsonl>` | — | offline fixture mode passthrough |

### 4.3 Output contract

Identical to the base composite: per-attempt JSONL plus a verdict line
(`{"verdict": "arrived", "label": "email"}`); match records carry
`uid`/`subject`/`from`/`date`. Exit `0` = a matching message arrived.

### 4.4 End-to-end example

```bash
SCRIPTS=.agents/skills/email/gmail-poll-for-message/scripts

GMAIL_APP_PASSWORD='<app-password>' python3 "$SCRIPTS"/poll-gmail-message.py \
    --username <gmail-address> --subject-contains 'transfer' \
    --interval 30 --attempts 20
```

## 5. Composition by Higher-Level Skills

None yet — higher-level workflows (e.g., transfer acceptance waits) may layer
on this preset; they would shell out to `poll-gmail-message.py` and consume the
`arrived` verdict.

## 6. Composition by This Skill

| Base | Invoked As | Supplied | Consumed Back |
| --- | --- | --- | --- |
| [`email-poll-for-message`](../email-poll-for-message/SKILL.md) | its `poll-email-message.py` driver with `--imap-host imap.gmail.com --imap-port 993` fixed | Gmail endpoint + credential conventions; criteria and knobs passed through | per-attempt JSONL (streamed through) + final exit code |

## 7. Prohibited Behaviors

- Re-implementing polling or IMAP logic — shell out to the base driver (§6).
- Passing app passwords as command-line arguments — environment variables only.
- Using a regular Gmail account password for IMAP — app passwords only.

## 8. Change History

| Timestamp | Summary of Changes | Rationale |
| --- | --- | --- |
| [2026-09-30 16:05] | Initial skill v1 created | The layered email stack needed the provider preset over the provider-agnostic IMAP composite |

## 9. Traceability

See [`TRACEABILITY.md`](TRACEABILITY.md) for session logs and provenance.

## 10. Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release history.
