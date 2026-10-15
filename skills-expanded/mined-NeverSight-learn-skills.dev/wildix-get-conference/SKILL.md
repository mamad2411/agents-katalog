---
name: wildix-get-conference
description: Fetch details for one or more x-bees/Wildix conferences by ID from wda.wildix.com. Use when you have a conferenceId and need participant list, duration, transcription status, recording availability.
license: MIT
metadata:
  author: Wildix
allowed-tools: >-
  Bash, Glob, Skill
---

# Wildix Get Conference

Fetches conference details from `wda.wildix.com` for one or more conference IDs.

## Peer Skills

Before running, check if `wildix-auth` is installed:
```bash
Glob ~/.claude/skills/wildix-auth/SKILL.md
# If missing: npx skills add Wildix/agent-skills --s wildix-auth -y
```

See [`peers.yaml`](peers.yaml) for full peer manifest.

## Input

Conference IDs can be passed as bare IDs or as full x-bees URLs:
- `340a8cf1-8268-4f5d-a065-585016bc-11_1778230879698`
- `https://app.x-bees.com/insights/conferences/340a8cf1-8268-4f5d-a065-585016bc-11_1778230879698`

Extract the ID from the URL: everything after the last `/`.

## Flow

1. **Get IdToken** via `wildix-auth` skill (if not already available)
2. **Extract conferenceId(s)** from input (strip URL prefix if needed)
3. **Run the script** with the conference ID(s)
4. **Display results**

## Script

```bash
bash <BASE_DIR>/scripts/get-conference.sh "$ID_TOKEN" <conferenceId> [conferenceId2 ...]
```

Fetches all IDs in parallel. Returns a JSON array of conference objects sorted by start time.

## Output fields

| Field | Description |
|-------|-------------|
| `id` | Conference ID |
| `subject` | Channel/topic name |
| `startTime` | Unix ms timestamp |
| `durationMs` | Duration in milliseconds |
| `status` | `COMPLETED`, `IN_PROGRESS`, etc. |
| `participants[].name` | Participant display name (deduplicated) |
| `participants[].email` | Participant email |
| `participants[].xbsId` | x-bees user ID (matches Stream user ID) |
| `participants[].speakDurationMs` | Speaking time in ms |
| `transcriptionStatus` | `AVAILABLE`, `PENDING`, `NONE` |
| `transcriptionLanguage` | e.g. `ru-RU` |
| `hasRecording` | `true` / `false` |
| `insights.brief.title` | AI-generated meeting title |
| `insights.brief.shortSummary` | Short summary of the conversation |
| `insights.highlights_internal.topics` | List of topics discussed |
| `insights.highlights_internal.decisions` | Decisions made |
| `insights.highlights_internal.progress` | Progress / what was done |
| `insights.highlights_internal.issues` | Issues identified |

Insights are only present if `status: "SUCCEEDED"` and fields are non-empty.

## Display format

For each conference with insights:
```
### HH:MM — "Title from insights or subject" (Xm)
Participants: Name1, Name2, ...
🎙 Transcription: AVAILABLE | 🎬 Recording: yes/no

**Summary:** <shortSummary>

**Topics:** bullet list
**Decisions:** bullet list
**Issues:** bullet list (if non-empty)
```

For conferences without insights: show just time, subject, duration, participants.

## Obsidian save format

When saving a conference to Obsidian, use YAML frontmatter followed by metadata and sections:

```markdown
---
title: <insights.brief.title or subject — strip any colons>
source: https://app.x-bees.com/insights/conferences/<conferenceId>
ticket: https://wildix.atlassian.net/browse/<TICKET>  # only if subject contains a Jira ticket like WMS-1234; omit if none
channel: <subject — strip any colons>
created: <YYYY-MM-DDTHH:MM>
description: <insights.brief.shortSummary — one sentence>
language: <transcriptionLanguage>
duration: <duration in minutes>
members:
  - <participants[0].name>
tags:
  - <tag1 from topics>
---

## Short summary
<shortSummary>

---

## Topics
- topic1

---

## Progress
- progress1

---

## Issues
- issue1

---

## Decisions
- decision1
```

File path: `wildix meetings/YYYY-MM/<YYYY-MM-DD> <title>.md`

Tags: extract 3–6 keywords from `highlights_internal.topics`. Tags must not contain spaces — replace spaces with hyphens.

**Ticket extraction:** scan `subject` for Jira-style ticket IDs using pattern `[A-Z]+-\d+`. If found, add `ticket` field. Omit entirely if no ticket found.

**YAML values must not contain colons** — strip or replace any `:` in scalar fields before writing.
