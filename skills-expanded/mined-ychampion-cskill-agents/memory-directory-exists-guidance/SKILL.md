---
name: memory-directory-exists-guidance
description: "Ensure memory directories exist once and surface consistent guidance so agents skip redundant mkdir calls."
metadata:
  author: ychampion
---

# SKILL: Memory Directory Exists Guidance
**Domain:** context-management  
**Trigger:** Use whenever you plan to write memory files so the agent can assume the directory exists instead of repeatedly running `mkdir -p`.
**Source Pattern:** Distilled from reviewed context, compaction, and memory-governance patterns.

## Core Method
Guarantee the auto-memory directory exists with a single idempotent `mkdir` (handled once per session) and prepend every guidance response with the standard instructions (`DIR_EXISTS_GUIDANCE` and `DIRS_EXIST_GUIDANCE`) so Claude knows not to rerun filesystem commands that are already satisfied. Log any mkdir failure asynchronously for telemetry but let the tool write operation report the real error to keep the workflow moving.

## Key Rules
- Call `ensureMemoryDirExists` before prompting the agent to write memory files so the path is settled; the helper already swallows `EEXIST` and warns only on genuine failures.
- Always echo either `DIR_EXISTS_GUIDANCE` or `DIRS_EXIST_GUIDANCE` when summarizing the directory state to the assistant so it stops issuing mkdir commands.
- Keep the mkdir call outside the main agent loop (e.g., in init or once-per-session code) so repeated turns do not spawn redundant filesystem operations.

## Example Application
When saving a new memory from within the CLI, run `ensureMemoryDirExists(memoryDir)` at session start, mention `DIR_EXISTS_GUIDANCE`, and proceed to open the target file without extra mkdirs; this keeps the assistant focused on writing content instead of housekeeping.

## Anti-Patterns (What NOT to do)
- Don’t rerun `mkdir -p` right before every write; the persistent guidance plus singleton helper avoids redundant logs and permission stumbling blocks.
- Don’t treat the guidance text as optional; skipping it results in the CLI repeatedly prompting for directory creation even though the path already exists.
