---
name: sbdc-ai-coworking-post-session-capture
description: Weekly post-session capture packet for the {{ORG}} AI Co-Working Hour
---

> **Schedule:** Weekly post-session capture packet
> **Needs:** Gmail, Google Calendar, Drive
> **Helper scripts (yours, not included):** none

# SBDC AI Co-Working Hour Post-Session Capture

## Objective

Create a post-session capture packet after the Monday {{ORG}} AI Co-Working Hour and AI Overflow block. The packet should turn the session into follow-up bullets, backlog items, artifact links, and wiki/Claromentis candidates.

This workflow is draft-only. Do not send the recap or edit shared records automatically.

## Account And Data Boundaries

- Use University of Maryland / SBDC Google Calendar, Gmail, and Drive context.
- Use local SBDC wiki/runbook context.
- Do not send emails, upload files, edit Drive docs, or modify wiki files automatically.
- Keep client examples anonymized unless they are explicitly approved internal training examples.

## Inputs To Review

Search for same-day and recent evidence:

- Calendar event details for the Monday AI Co-Working Hour and AI Overflow block
- Gmail thread/chat recap if available
- Drive artifacts modified or shared today in the AICOWORKING folder, AI Videos folder, Skills Library, or related SBDC AI folders
- Notes/transcripts/recordings if available
- Local agenda packet from `sbdc-advising/outputs/` if present
- `sbdc-advising/wiki/ai-coworking-hour.md`

## Output Format

Use this exact structure.

```
# AI Co-Working Hour Capture - YYYY-MM-DD

## Executive Snapshot
- Main topic:
- Decisions made:
- Artifacts shared:
- Blockers raised:
- Follow-ups needing {{USER}}:

## 3-Bullet Recap Draft

[Draft text {{USER}} can paste into the shared thread.]

## Decisions And Agreements

| Decision | Owner | Due / next check | Evidence |
|----------|-------|------------------|----------|

## Artifact Log

| Artifact | Owner | Location | Needs upload/archive? |
|----------|-------|----------|-----------------------|

## AI Overflow Backlog

| Item | Owner | Status | Recommended next step |
|------|-------|--------|-----------------------|

## Wiki / Claromentis Candidates

| Candidate | Destination | Why it matters | Source |
|-----------|-------------|----------------|--------|

## Follow-Up Drafts

### [Recipient / Group]
Subject:

[Draft follow-up]

## Questions For {{USER}}
- [Question] - why it matters
```

## Capture Rules

- If no transcript or notes are available, build from Calendar/Gmail/Drive signals and clearly say what was not available.
- Distinguish decisions from discussion.
- Turn blockers into owner + next-step language.
- Keep the 3-bullet recap short enough to paste into an email or chat thread.

## Portability Notes

When installing in another ChatGPT Enterprise instance:

- Connect UMD/SBDC Calendar, Gmail, and Drive.
- Ensure the task can access co-working artifacts or recordings if those live in a shared Drive.
- Schedule after the Monday 9:00-11:00 AM ET co-working + overflow window.
