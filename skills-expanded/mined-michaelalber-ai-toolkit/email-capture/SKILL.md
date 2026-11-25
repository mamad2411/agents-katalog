---
name: email-capture
audience: team
description: Converts email threads, SOWs, change requests, and pasted documents into structured capture documents for spec-driven development. Extracts requirements, decisions, commitments, and open questions with source attribution to sender and message date. Use when given an email thread, SOW, change request, or pasted document that needs to be converted into structured requirements with per-message source attribution.
---

# Email Capture

> "The difference between a requirement and a preference is whether anyone will know
> if you ship without it."
> -- Adapted from Karl Wiegers, "Software Requirements"

> "Every email thread is a negotiation. Requirements hide in the agreement,
> not the conversation."

## Core Philosophy

Email threads are lower-noise than meeting transcripts but structurally messier. Requirements are embedded in reply chains, buried under greetings and signatures, split across multiple messages, and sometimes contradicted in later replies. A change request buried in a forwarded attachment is still a requirement.

This skill reads email threads and documents methodically — parsing by sender authority, chronological order, and message type — to extract requirements, decisions, commitments, and open questions with source attribution. Email content is often more decisive ("we need X by date Y") but also more fragmented (the final agreed version is in message 12 of a 15-message thread, not in message 1).

**What this skill does:** Accepts pasted email thread text or a file path. Parses the thread to identify senders, dates, and message sequence. Extracts requirements, decisions, commitments, and open questions with source attribution. Flags contradictions between earlier and later messages. Produces a structured capture markdown with provisional `DRAFT-NNN` IDs.

**What this skill does NOT do:** Access email accounts or inboxes (input is manual paste or file), synthesize requirements from ambiguous phrasing, resolve contradictions autonomously, or push to Confluence without explicit PM instruction.

**Non-Negotiable Constraints:**
1. **Read in chronological order** — the final agreed version may be message 12 of 15; a later message can supersede an earlier one
2. **Every item is attributed** — sender and message date on each requirement, decision, commitment, and open question
3. **Contradictions are surfaced, not resolved** — flag the earlier and later statements for the PM
4. **No requirements from ambiguous phrasing** — unclear wording becomes an open question, not a requirement
5. **IDs are provisional** — `DRAFT-NNN` only; canonical numbering belongs to `capture-consolidate`
6. **No Confluence push without explicit PM instruction**

The seven domain principles (chronology, sender authority, attachments-first-class, contradictions-surfaced-not-resolved, commitments-as-requirements, provisional IDs, logged trimming), the knowledge-base lookups, the AI discipline rules, anti-patterns, and error-recovery procedures live in `references/capture-discipline.md`.

## Workflow

The INTAKE → PARSE → EXTRACT → OUTPUT loop. Every phase template (intake, parse log, extraction guide + log, capture document, session opening) is in `references/email-capture-templates.md`. Parsing depth — thread structure, authority map, document types, contradiction patterns, boilerplate, attachment handling — is in `references/thread-parsing.md`.

### Phase 1: INTAKE — Gather PM Context

1. Ask the PM to provide the email thread — paste text or give file path
2. Collect context with the Intake Template (five fields: project/client, thread description, authoritative senders, in-scope topics, out-of-scope topics)
3. Confirm understanding of authoritative senders and document scope
4. Only then → PARSE

**Do not proceed without all five context fields.**

### Phase 2: PARSE — Structure the Thread

1. Identify all messages (sender, date, subject if available)
2. Detect forwarded chains, inline replies, and attachment references
3. Build a chronological message map; identify the authoritative senders from intake
4. Flag any referenced attachment not present as `[ATTACHMENT NOT PROVIDED: filename]`
5. Log the Parse Summary before extraction

Treat a single document (SOW, change request, spec) as one high-authority block. Inline replies are attributed to the replying sender. (Full parse rules: `references/email-capture-templates.md`.)

### Phase 3: EXTRACT — Requirements, Decisions, Commitments, Open Questions

1. Call `search_knowledge("requirements extraction stakeholder communication written")` to calibrate (KB lookups: `references/capture-discipline.md`)
2. Work through the thread chronologically, extracting signal by message using the Extraction Signal Guide
3. Assign provisional `DRAFT-NNN` IDs to each item
4. Mark the most recent position on each topic; tag earlier ones `[SUPERSEDED by DRAFT-NNN]` — keep for audit, never delete
5. Produce the Extraction Log before OUTPUT

### Phase 4: OUTPUT — Produce Capture Document

1. Call `search_knowledge("acceptance criteria given when then format")` to confirm format
2. Organize extracted content by signal type
3. Produce the capture markdown using the Output Template (below)
4. If Confluence publish is requested: ask for target space and parent page before publishing

Default output path: `captures/[YYYY-MM-DD]-[thread-slug].md`

## State Block

```
<email-capture-state>
phase: intake | parse | extract | output
project: [project or client name]
thread: [thread description and date range]
messages_parsed: N
authoritative_senders: [list]
requirements_found: N
decisions_found: N
commitments_found: N
open_questions_found: N
contradictions_found: N
attachments_missing: [list or "none"]
output_path: [file path, or "pending"]
last_action: [what was just done]
next_action: [what should happen next]
</email-capture-state>
```

## Output Template

`# [Thread Title] — [Date Range] — [Project / Client]`

Sections: Participants (Name / Role / authority level) | Summary (2–3 sentences) | Key Decisions (statement + Source: sender, date) | Requirements Extracted (DRAFT-NNN + statement + source, with `[SUPERSEDED by DRAFT-NNN]` or `⚠ [UNCERTAIN]` tags) | Commitments (DRAFT-NNN + statement + source) | Open Questions (question + source + status: Unanswered / Answered in msg N) | Contradictions Flagged (table: Item / Earlier Position / Later Position / Source-Earlier / Source-Later / PM Resolution) | Action Items (owner + due date) | Missing Attachments (filename + who referenced it) | Thread Trim Log (table: Excluded / Reason).

**Session Opening:** Explain the 4-phase process (intake → parse → extract → output). State that nothing is silently excluded. Ask: where is the thread/document, what project does it feed into, and who has decision authority. Emit initial `<email-capture-state>` with `phase: intake`.

Full capture-document template and all phase templates: `references/email-capture-templates.md`.

## Integration with Other Skills

- **`transcript-capture`** — Use when the intake source is a meeting transcript rather than an email or document. Both skills produce the same `DRAFT-NNN` capture format. Use `capture-consolidate` to merge outputs.
- **`capture-consolidate`** — Run after one or more capture sessions to assign canonical `REQ-XXX` IDs, deduplicate overlapping requirements, and surface contradictions.
- **`confluence-guide-writer`** — If the final capture document should be published to Confluence, use this skill to format and publish after PM approval.
