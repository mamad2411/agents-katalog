---
name: daily-log
description: >
  Use this skill when the user wants to log today's AI activity to a shared daily log file.
  Triggers: "log this", "save to daily log", "record today's work", "/daily-log", "/log".
  Codex appends only to its own [Codex] section. Other AI sections are read-only.
---

# daily-log

Use this skill to append Codex activity to today's shared daily log.

## Core Goal

```text
identify date -> locate or create log file -> append to [Codex] section only -> verify
```

## Routing

This skill is always `simple` tier. It does one focused append and verifies it.

Escalate to `medium` only if the log file is corrupted or the directory does not exist and needs repair.

## Workflow

1. Identify today's date (YYYY-MM-DD).
2. Resolve the log file path: `<vault>/logs/YYYY/MM/YYYY-MM-DD-daily.md`. Replace `<vault>` with your configured vault root.
3. Check whether the file exists.
   - **File absent** → create it with the standard structure (see below). Create any missing `YYYY/MM/` folders first.
   - **File present** → open it and append only to the `[Codex]` section. Do not modify any other section.
4. Locate the `## [Codex]` section.
5. Append the new entry below the last existing entry in that section.
6. Verify the file was written and only the `[Codex]` section changed.

## Log File Structure (New File)

```markdown
# Daily Log | YYYY-MM-DD

> Shared daily log. Each AI appends to its own section only. Contract: LOG_CONTRACT.md

## [Claude]
*(no activity yet)*

## [Codex]
### HH:MM - HH:MM / topic-slug
- entry

## [Gemini]
*(no activity yet)*

## [Copilot]
*(no activity yet)*

## [Manual]
*(user entries)*
```

## Entry Format

```markdown
### HH:MM - HH:MM / topic-slug
- what was done
- what was verified or found
- what is still open (if any)
```

Use 24-hour time. `topic-slug` is kebab-case: `api-refactor`, `test-repair`, `data-scan`.

## Rules

- Append only. Never rewrite the full file.
- Write only to `[Codex]`. Read other sections for context only.
- Do not touch `[Claude]`, `[Gemini]`, `[Copilot]`, or `[Manual]` sections.
- If the `[Codex]` placeholder line reads `*(no activity yet)*`, replace it with the first entry block.

## Evidence

```text
Current Goal:
Tier: simple
Work Done:
Evidence: <file path> — [Codex] section appended, N bullets
Verification: file exists, size increased, other sections unchanged
Unresolved Risks:
Next Action:
Close Decision:
```

Do not treat a chat response as completion. Confirm the file on disk.
