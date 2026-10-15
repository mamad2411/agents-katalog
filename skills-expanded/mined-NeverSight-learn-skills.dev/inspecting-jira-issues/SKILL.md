---
name: inspecting-jira-issues
description: Use when starting work on a Jira ticket and you need full context — not just summary, but attachments (screenshots, mockups), comments (where repros usually live), linked issues, and custom fields. Use when `acli jira workitem view` returns a description that's just a media reference like `image-20260427-021811.png` and you can't see what the bug is. Use when an AI agent is about to guess at a bug from the summary or about to ask the user to paste a screenshot it could fetch itself. Use when authenticated curl against the Jira REST API returns 401, 403, or 406.
---

# Inspecting Jira Issues for AI Agents

## Overview

A Jira summary is the worst way to understand a bug. The actual repro almost always lives in **attachments**, **comments**, or **linked issues** — three places `acli jira workitem view` does not show by default. An AI agent that "works from the summary" guesses at half the problem.

This skill is the standard recipe for reading a Jira ticket completely from the command line, and for downloading attachment bytes that the agent can actually view (the non-obvious part — `acli` has no `attachment download` subcommand).

## When to Use

- You just opened a Jira URL and are about to start fixing
- The description is `image-20260427-021811.png` with no text
- An agent says "I'll work from the summary" or "can you paste the screenshot"
- `curl` returns 401/403/406 against the Jira REST API

**Don't use** for sparse tickets with no attachments and no linked issues — `acli jira workitem view KEY` is enough.

## Inspection workflow

The fast path is one command. **Use the absolute path** — the skill ships to `~/.claude/skills/inspecting-jira-issues/` and is not on `PATH` by default:

```bash
JIRA_SITE=https://your-site.atlassian.net \
  ~/.claude/skills/inspecting-jira-issues/jira-to-markdown.py KGM-3320
# → /tmp/jira/KGM-3320/ticket.md
# → /tmp/jira/KGM-3320/attachments/*
```

(Once you've symlinked it into `~/bin/` per the README, the bare `jira-to-markdown.py KGM-3320` form also works.)

`jira-to-markdown.py` writes a self-contained directory: one `ticket.md`
with **every populated field** rendered — header table covers all scalar
fields (standard + custom, labels resolved via `?expand=names`), and every
ADF-doc field gets its own `## Section` (Description, Environment, plus any
ADF custom fields). Attachments, linked issues, sub-tasks, and comments
follow. Every attachment is downloaded under `attachments/` and referenced
inline as `![alt](attachments/foo.png)`.

Why exhaustive: the actual repro on TPT bug tickets often lives in
`fields.environment` (発生工程, 再現手順, プラットフォーム, etc.), which
neither the description nor `acli workitem view` shows by default. Same
goes for custom fields like Severity, Urgency, Epic Link. Curating fields
ahead of time means rediscovering missing ones one ticket at a time.

The script handles the non-obvious bits — keychain-stored OAuth token,
ADF→Markdown conversion (paragraphs, lists, headings, code, links, marks,
mentions, panels, tables, media), filename-collision disambiguation, and
the `Accept: */*` quirk that bypasses `406 Not Acceptable`.

If you only need one piece, the lower-level commands still work:

```bash
KEY=KGM-3320

acli jira workitem view "$KEY" --fields '*all' --json     # full JSON
acli jira workitem attachment list --key "$KEY" --json    # attachment IDs
~/.claude/skills/inspecting-jira-issues/download-jira-attachment.sh 188469 /tmp/$KEY.png
acli jira workitem comment list --key "$KEY"              # comments alone
```

## Where things hide

| You want | It is actually in |
|----------|-------------------|
| Bug repro steps | A comment, not the description |
| The screenshot showing the bug | An attachment |
| Why this ticket matters / customer impact | Custom fields (criticality, urgency) — fetch with `--fields '*all'` |
| Whether the fix already shipped elsewhere | A comment on the parent epic, or a linked "is duplicated by" |
| The actual symptom | The screenshot, never the summary |

## Downloading attachments — the non-obvious parts

`acli` has no `attachment download`. Naive `curl` against `*.atlassian.net/rest/api/3/attachment/content/<id>` returns **403**. The four pitfalls every agent hits:

| Pitfall | Workaround |
|---------|-----------|
| Where's the OAuth token? | macOS Keychain (`security find-generic-password -s acli`), **not** `~/.config/acli/`. Stored as `go-keyring-base64:<base64(gzip(JSON))>`. |
| Which URL do I hit? | `https://api.atlassian.com/ex/jira/<cloudId>/rest/api/3/attachment/content/<id>` — the OAuth proxy. The site URL rejects acli's tokens. |
| Where's the cloudId? | The keychain account name is literally `oauth:<cloudId>:<userId>`. No need to call `getAccessibleAtlassianResources`. |
| Why does my request 406? | `Accept: image/png` triggers 406 ("Acceptable representations: [application/json]"). Use `Accept: */*` (or omit `Accept`). |

Both `jira-to-markdown.py` (full ticket dump) and `download-jira-attachment.sh` (one attachment) in this skill's directory bundle all four. Copy them to `$PATH` (e.g. `~/bin/`).

## Prerequisites

```bash
brew tap atlassian/homebrew-acli
brew install acli
acli auth login        # one-time OAuth dance — also re-run if you change sites
```

The first `acli auth login` is what plants the OAuth token in the macOS keychain. Both scripts in this skill read from there.

## Token expiry

Access tokens last ~1 hour. The scripts call `acli auth status` at startup to trigger a silent refresh, so the first run after a long break works without intervention. If `acli auth status` itself reports the refresh token has expired, re-run `acli auth login`.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Start fixing from the summary alone | The summary is a label, not the bug. Always fetch JSON + attachments first. |
| Skip attachments because "the description has text" | If the description references an image, the image *is* the description. Download it. |
| Ignore comments | Repro steps, decisions, and "this was actually fixed in PR #123" live here. |
| Skip linked issues | "is duplicated by" often points to the ticket with the actual fix plan. |
| Use the site URL for OAuth requests | Use `api.atlassian.com/ex/jira/<cloudId>/...`. |
| Use `Accept: image/png` | 406. Use `Accept: */*`. |
| Search `~/.config/acli` for the token | Token is in macOS Keychain. Config files only have metadata. |
| Treat the keychain blob as a raw token | It is `go-keyring-base64:<base64(gzip(JSON))>`. Decode; extract `access_token`. |
| Give up because `acli` has no download command | The keychain bypass is exactly why this skill exists. |
| Ask the user to paste the screenshot | Don't bother the user when the API is right there. |

## Red flags — stop and re-inspect

If you find yourself thinking any of these, you have not read the ticket completely:

- "Based on the summary, I'll…"
- "Can you share the screenshot?"
- "I'll assume the bug is…"
- "The description doesn't say much, so…"
- "There's an attachment but I don't have access to images"

All of these mean: run the inspection workflow above. Then think.

## Iron law

**If a Jira ticket mentions a screenshot, attachment, comment, or linked issue and you have not read it, you do not understand the bug yet.**

Read the whole ticket. Then think.
