---
name: grill-session-record
description: Grill sub-skill. Persist only completed grill sessions as final raw agent-question/user-answer transcripts. In completed preflight runs, write .agent-runs/<id>/grill.md; otherwise fall back to harness/grill/sessions/<timestamp>.md. Activate only when ending a grill session.
---

# Grill: Session Record

Grill decisions are not durable in conversation memory. Persist the raw exchange only when the grill is ending.

## Hard timing rule

Only write a grill transcript after the grill session is complete and the agent is about to end the grill.

Do not create, pre-fill, append to, or update any grill transcript while a grill is still active.

Do not write research notes, planning notes, recommendations, assistant answers, summaries, decisions, or open questions into the transcript. The transcript is only the completed raw Q&A.

## Primary path during preflight

When ending a completed preflight grill for the current numeric run id, write:

```text
.agent-runs/<id>/grill.md
```

This is the Step 1 handoff artifact for `intent.md` and `harness.md`.

Do not allocate a numeric run id in this skill.

Do not write `.agent-runs/<id>/grill.md` for prototype-only work, ordinary design discussion, or any non-preflight grill.

## Fallback path outside preflight

When ending a completed non-preflight grill with no current numeric preflight run id, write:

```text
harness/grill/sessions/<YYYYMMDD-HHMMSS>.md
```

## Format

Keep the transcript pure Q&A:

```md
# Grill <id-or-timestamp>

## Q1: <question text>
A: <user answer>

## Q2: <question text>
A: <user answer>
```

Do not summarize, interpret, annotate, add decisions, or add open-branch sections. The user's words are the source; interpretation belongs in `intent.md`, `harness.md`, or later grill sessions.

`Q` is always the agent's question to the user.

`A` is always the user's answer to that question.

Never record user questions to the agent as `Q` entries, and never record assistant explanations as `A` entries.
