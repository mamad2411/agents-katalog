---
name: handover
description: Handover system — cross-device, cross-agent, cross-account work continuation. Generate a structured handover note at session end (markdown in a cloud-synced folder, SQLite indexed locally) and resume on any machine or agent. When the user says "handover", "hand over", "save progress", "switching devices/accounts", "switching to Gemini", or "that's enough for today", use it to hand over; when they say "take over", "where did I leave off", "continue yesterday's work", "resume", or want context at a new session start, use it to load. Also use for listing or searching past notes (e.g., "what methods have I tried before").
---

# Handover Notes

Markdown files are the single source of truth (stored in a cloud-synced folder—Google Drive, Dropbox, iCloud, etc.—so notes follow you across devices); SQLite is just a local index that any script can rebuild. All scripts live in the `scripts/` folder within this skill. Script paths contain spaces—always quote them.

## Handing Over (before session end)

1. **Determine session_type**: `sdd` (design-driven development) / `debug` / `discussion` / `admin`. Ask the user once if unsure.
2. **Write a draft** to a temp directory (e.g., `draft.md`), using the format below.
3. **Save**: `"<skill-dir>/scripts/save.sh" --file draft.md`
4. Report the id and suggest `/clear` to the user (clean context is better than bloated context with rot).

### Draft Format

```markdown
---
project: gmail-billing-scan
session_type: debug
account: personal
test_status: 3 failing in parser_test
---

# One sentence: what does this note do

## Done
What was accomplished (specific to files and functions).

## Decisions
What decisions were made and why. For discussion sessions, record "argument → consensus/disagreement".

## Blocked
Where you're stuck (omit if none).

## Next steps
Each item must be executable as-is, with file paths. No vague "keep debugging".

## Attempted approaches
Record as "approach → result → why it was ruled out". Mandatory for debug type; most valuable field.

## Lessons learned
Long-term applicable lessons (omit if none).
```

Frontmatter: only fill in `project`, `session_type`, and `account` (if known); other fields (created_at, device, branch, working_dir, status, agent) are auto-filled by save.sh. **Never write tokens, passwords, or credentials**—handover notes get pasted into other agents' prompts.

### Summary Depth by Session Type

- **sdd**: Record progress and "decisions that deviate from design docs". Design details → reference doc paths, don't repeat.
- **debug**: Attempted approaches is the main focus; write liberally. The final solution is secondary.
- **discussion**: Record arguments, consensus, disagreement. Skip the conversation itself.
- **admin**: Just Next steps and Decisions.

### Quality Rules (most handover failures violate these two)

- Write for **someone who never saw this conversation**: avoid pronouns and local shorthand; give full names and paths on first mention.
- Each next step must be actionable without asking the author.

## Taking Over (new session start)

1. `"<skill-dir>/scripts/load.sh" --project <name>` (newest open note; use `--id` for a specific one).
2. **Validate before acting**: the note is a snapshot from when it was written. Check if the branch still exists/merged, if mentioned files have changed; trust current state if there's a mismatch, and tell the user.
3. After starting work, mark the taken-over note: `"<skill-dir>/scripts/mark.sh" <id> superseded` (if you'll save a new note later) or `done` (work is complete). **Stale open notes are more dangerous than no notes.**

### Handing Over to Another Agent (Gemini, etc.)

`load.sh --project <name> --layer1-only` outputs only the generic layer (strips environment metadata from frontmatter). Paste the output directly to the other agent.

## Listing and Searching

- `"<skill-dir>/scripts/list.sh"`: open notes from last 30 days; `--all` shows all; `--project` filters.
- `"<skill-dir>/scripts/search.sh" "keyword"`: FTS5 full-text search—great for "what methods have I tried".

## Boundary with Long-Term Memory

Handover records **state** (expires), memory/CLAUDE.md records **facts and preferences** (long-lived). When taking over, if you find long-term-applicable lessons in Lessons learned, suggest upgrading them to memory; mark the note done.
