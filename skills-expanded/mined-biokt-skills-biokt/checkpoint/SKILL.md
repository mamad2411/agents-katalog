---
name: checkpoint
description: Save or load session context via CHECKPOINT.md. Use to checkpoint before /clear, or restore context at the start of a new session.
allowed-tools: Read, Write, Bash, Glob
---

Manage session context. Parse the argument (if any) to determine the action:

- `/checkpoint save` — summarize and save the current conversation to CHECKPOINT.md
- `/checkpoint load` — read CHECKPOINT.md and restore context into the session
- `/checkpoint` (no argument) — default to **load**

---

## SAVE

Summarize this conversation and save it to CHECKPOINT.md in the current working directory.

Structure the file with these sections:

### Current Goal
One or two sentences maximum — what we are working on and why.

### Work Done
**Last session only** (dated header, e.g. `### Session YYYY-MM-DD`). Bullet points, max 10 items. Each bullet: one line. Drop detail that is already visible in the code or git log.

### Current State
A small table or 3–6 bullet points covering what is running/done/broken. No prose.

### Next Steps
Max 5 bullets. Ordered by priority.

### Key Files
Max 8 entries. Path + one-line role only.

Rules:
- Write to CHECKPOINT.md in the **current working directory** (the project root).
- **Hard limit: keep the file under 60 lines / ~3 KB.** If it would exceed this, cut "Work Done" first, then "Key Files".
- Do not carry forward old "Work Done" sections — each save replaces the previous one entirely.
- Do not include conversation pleasantries or meta-commentary.
- Overwrite any existing CHECKPOINT.md (it is a checkpoint, not a log).
- After saving, confirm the file was written and tell the user they can now run /clear to start a fresh session.

---

## LOAD

Read CHECKPOINT.md from the current working directory and restore the session context.

Steps:
1. Check if CHECKPOINT.md exists in the current working directory. If not, say so and stop.
2. Read the file.
3. Scan companion files (recency-gated, partial reads only). For each file below, first check whether it was modified in the last 7 days using `find . -maxdepth 1 -name "<file>" -mtime -7`. Skip any file that returns empty and note it as stale. For files that pass:
   - `LABNOTEBOOK.md` — extract the most recent entry only (first entry in the file, since entries are prepended). Use: `awk 'NR==1{print; next} /^## /{exit} {print}' LABNOTEBOOK.md`
   - `TODO.md` — read lines 1–40.
   - `JOBS.md` — read lines 1–30.
4. Summarize the restored context: current goal, current state, and next steps — in that order. If companion files were found and recent, append a brief note: the date and one-line summary of the last lab notebook entry, and any TODOs or jobs directly relevant to the current goal. Do not quote files verbatim — distill only what adds context beyond CHECKPOINT.md.
5. Tell the user the context has been restored and they can continue where they left off.
