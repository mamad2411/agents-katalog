---
name: client-feedback
description: >-
  Deterministic feedback processor. Fetches client feedback emails from Gmail, 
  downloads attachments (screenshots), and prepares a structured report for 
  triaging into GitHub issues.
version: 2.0.0
---

# Client Feedback Processor

Transform client feedback emails into tracked, investigated, and resolved GitHub issues with professional response emails.

This workflow uses a **Script-First** approach: a deterministic Python script handles the "labor" of fetching and parsing emails, leaving the agent to handle the "judgment" of triaging and fixing issues.

## Usage

When the user asks to "process feedback", "check emails from [domain]", or "turn feedback into issues":

1. **Run the processor script:**
   ```bash
   python3 ~/.agents/skills/client-feedback/scripts/process_feedback.py \
     --domain "<client-domain>" \
     --days 7 \
     --out "./feedback-batch-$(date +%F)"
   ```

2. **Read the report:**
   Load the generated `report.json` and the full body text files to understand the feedback.

3. **Triage to GitHub:**
   For each distinct piece of feedback in the report, create a GitHub issue or update an existing one.

## Phase 1: Intake (Script-Driven)

The `process_feedback.py` script performs these tasks in seconds:
- Searches Gmail for emails from the specified domain/sender.
- Fetches full message payloads.
- **Downloads attachments automatically** to a local directory.
- Extracts plain-text bodies to individual files for easy reading.
- Generates a `report.json` summarizing threads, participants, and snippets.

## Phase 2: Triage — GitHub issues

GitHub issues are the primary work board. One issue per item, not one per email.

### Issue body template

```markdown
## Reported by
[Person name] — [date] "[email subject]" (thread [threadId])

## Issue
[Verbatim quote if short, paraphrase if long]

## Status
[Open / awaiting client / in progress]
```

Apply labels based on category: `feedback` (always), `bug`, `content`, `design`, `provider-data`, `question`.

## Phase 3: Investigate & Fix

Verify the feedback against the actual codebase. **Grep globally** for subjects of claims to ensure full removal or update.

## Phase 4: Respond

Draft professional responses organized by email thread.

**Key Rule:** ALWAYS show the draft body text in chat before sending. 

### Signature policy
Keep signatures simple and professional. Avoid disclosing AI co-authorship unless the client relationship explicitly welcomes it.

## Reference: Gmail multipart upload
If you need to draft a reply with inline images (e.g. before/after proofs), use the `gws` multipart upload flow documented in the script comments or `process_feedback.py` logic.

```