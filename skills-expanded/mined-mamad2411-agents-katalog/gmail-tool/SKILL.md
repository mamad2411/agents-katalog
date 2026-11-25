---
name: gmail-tool
description: >-
  Gmail integration tool. Performs unread check, body retrieval, and draft creation via Gmail API using OAuth2.
  Use when: Use when: you need to check received emails, read email bodies, create drafts, search the inbox, or work with labeled emails.
tags: [communication, gmail, email, external]
---


# Gmail Tool

An external tool that directly operates on Gmail emails using OAuth2.

## How to Invoke

**Bash**: Run with `animaworks-tool gmail <サブコマンド> [引数]`

## Available Actions

### unread — List unread emails
```bash
animaworks-tool gmail unread [-n 20]
```

### read_body — Read email body
```bash
animaworks-tool gmail read MESSAGE_ID
```

### draft — Create draft
```bash
animaworks-tool gmail draft --to ADDR --subject SUBJ --body BODY [--thread-id TID]
```

## CLI Usage

```bash
animaworks-tool gmail unread [-n 20]
animaworks-tool gmail read MESSAGE_ID
animaworks-tool gmail draft --to ADDR --subject SUBJ --body BODY [--thread-id TID]
```

## Notes

- OAuth2 authentication flow is required on first use
- credentials.json and token.json must be placed in ~/.animaworks/
