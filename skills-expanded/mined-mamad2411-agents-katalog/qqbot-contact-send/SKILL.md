---
name: qqbot-contact-send
description: Resolve a QQBot recipient from the local known-targets registry, distinguish between similarly named contacts, and send text or files to the intended QQ user with the correct target. Use whenever the user says things like “发给这个 QQ 联系人”, “把这个文件发给某个 QQ 用户”, “看看 known-targets.json 里是谁”, “确认发送对象”, or when you need to map a human-readable QQ contact name to a concrete `user:<openid>` target before sending. Prefer this skill over guessing from the current chat when multiple QQ users exist.
---

# qqbot-contact-send

Use this skill when the user wants to send something to a QQ contact identified by display name or nickname rather than by raw target id.

## What this skill is for

This skill helps avoid sending to the wrong QQ user when:
- the current chat user is not the intended recipient
- multiple QQ contacts exist in `known-targets.json`
- display names are similar or duplicated
- different users may use multiple agents with the same display name
- the user asks to inspect the local QQBot target registry before sending

## Data source

Read this file first when resolving a recipient:

- `~/.openclaw/qqbot/data/known-targets.json`

It contains entries like:
- `accountId`
- `kind`
- `target`
- `displayName`
- `lastSeenAt`

## Default workflow

1. Read `~/.openclaw/qqbot/data/known-targets.json`.
2. Default to the current session's `accountId` as the lookup scope unless the user explicitly asks to send across another agent/account.
3. Prefer the bundled helper script for deterministic lookup:
   - `python3 {baseDir}/scripts/resolve_known_target.py "<name-or-target>" --account-id "<current-accountId>"`
4. Match the requested human name against `displayName` first.
5. If more than one candidate is plausible, show the candidates briefly and ask which one to use.
6. If exactly one match is clear, use that entry's `target` and `accountId`.
7. Optionally run the bundled send-prep helper:
   - `python3 {baseDir}/scripts/prepare_send.py "<recipient>" --account-id "<current-accountId>" --file <path> [--caption <text>]`
   - or `--text <message>`
8. Send via the `message` tool using:
   - `channel: "qqbot"`
   - `target: <resolved target>`
   - `accountId: <resolved accountId>`
9. If sending a file, pass the local path directly.
10. If upload fails, report the real error plainly. Offer retry or text fallback if appropriate.

## Matching rules

Prefer in this order:
1. exact `displayName` match
2. exact user-provided target id if given
3. recent active contact with a highly similar name

Do not assume the current inbound sender is the destination when the user explicitly names another person.

## Ambiguity handling

Ask a short follow-up if:
- multiple entries share the same or similar name
- no clear `displayName` match exists
- the user says only “发给他/她” without context

Good follow-up style:
- `我查到两个候选：A（user:...）和 B（user:...），你要发给哪一个？`

## Output style

When reporting the resolved recipient, be brief and concrete:
- who it maps to
- which target will be used
- whether send succeeded or failed

## Important caveat

QQ file messages sent through the generic `message` tool may not automatically enter the qqbot plugin's `ref-index`, so later quote recovery can be incomplete. This does not block sending, but it may affect future reply-context restoration.

## Example prompts this skill should trigger on

- `把这个文件发给这个 QQ 联系人`
- `看 known-targets.json，确认发送对象`
- `发给这个备注名联系人，不是当前这个人`
- `把这份 md 发给另一个 QQ 用户`
- `先查联系人再发，别发错人`

## Helper scripts

Bundled helpers:
- `scripts/resolve_known_target.py` → resolve recipient candidates
- `scripts/prepare_send.py` → resolve recipient and generate a ready-to-use `message` tool payload

Examples:

```bash
python3 {baseDir}/scripts/resolve_known_target.py "<contact-name>" --account-id "<current-accountId>"
```

```bash
python3 {baseDir}/scripts/prepare_send.py "<contact-name>" --account-id "<current-accountId>" --file <path> --caption "<optional-caption>"
```

The scripts use:
- exact `displayName`
- exact `target`
- substring match
- `lastSeenAt` recency as tie-breaker
- current session `accountId` as the default scope filter

`prepare_send.py` does not send by itself; it emits a verified payload for the `message` tool so the agent can deliver without hand-building target fields.
