---
description: First-run topic setup wizard + scaffold/repair the wiki file tree.
when_to_use: Run first after cloning the template — the wizard captures your topic conversationally and writes it into CLAUDE.md. Re-run any time the directory structure looks broken or inconsistent (missing subdirectory, missing _index.md, missing template). Safe to re-run — the topic step is skipped once CLAUDE.md is filled in, and the scaffold step only creates what's absent. Also triggered by phrases like "set up the wiki", "first-time setup", "repair the structure", "scaffold the vault".
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Wiki Init

Two jobs: (1) first-run topic setup, (2) directory/template verification. Both safe to re-run — neither overwrites existing content.

## Step 1 — Topic setup (first-run only)

Read `CLAUDE.md` lines 1–10. Check whether the Overview section contains the placeholder `<!-- REPLACE THIS LINE`.

**If the placeholder is present** (fresh clone):

1. Ask the user conversationally about their topic. Good prompts:
   - "What's the knowledge base going to be about? Think of it as the one-paragraph answer you'd give a friend asking 'what's this vault for?'"
   - "Any specific domains in scope? Anything explicitly out of scope?"
   - "Is this a single-topic vault or a generalist one? If generalist, what ties the domains together?"
2. Wait for the user's response. Iterate if the answer is vague — the goal is a concrete, specific description that will actually anchor future ingests.
3. Once the user is happy, rewrite the entire placeholder `<!-- ... -->` block in `CLAUDE.md` with the user's one-paragraph topic description in plain prose. Preserve the rest of the Overview section (the "You (Claude) are the maintainer…" paragraph).
4. Also update the first line of `README.md` if the user wants a matching one-line summary there — ask.
5. Report what was written, and show the diff.

**If the placeholder is absent** (already-initialized vault): skip step 1 silently. Proceed to step 2.

## Step 2 — Directory / template verification (always)

Verify the full directory tree exists:

- `raw/{articles,papers,transcripts,assets}/`
- `wiki/{sources,concepts,entities,syntheses,outputs,views,canvases,attachments/images}/`
- `templates/`
- `docs/`

For any missing directory, create it with a `.gitkeep` file.
For any missing `_index.md`, create it using the existing ones as a shape reference.
For any missing template in `templates/` (expected: `source-summary.md`, `paper-summary.md`, `concept.md`, `entity.md`, `synthesis.md`, `output.md`, `stub.md`), tell the user — do not invent one.

Do not touch `.obsidian/`, `.git/`, or `.claude/`.

## Report

- Topic setup: completed / skipped (already configured) / abandoned
- Directories created: N (list)
- Index files created: N (list)
- Templates missing (flag for the user): list
