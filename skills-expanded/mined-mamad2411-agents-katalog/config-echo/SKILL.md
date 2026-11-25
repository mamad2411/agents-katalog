---
name: config-echo
description: Verifies bluetemberg config (rules, agents, skills) is loaded in the session by recalling from context and cross-referencing disk. Use after `bluetemberg sync` or when a rule seems ignored.
---

# config-echo

Use this skill to confirm what bluetemberg configuration the LLM has in its active session context, and to verify it matches what is on disk.

## Triggers

- After running `bluetemberg sync` to confirm the LLM picked up the changes
- When a rule does not seem to be taking effect
- Onboarding a new team member — confirms their setup is complete end-to-end
- Debugging "why is the LLM ignoring X?" questions

## Required behavior

Steps MUST be executed in order. The LLM MUST NOT read any files before completing step 1.

### Step 1 — Recall from session memory (no file reads)

The LLM MUST enumerate every bluetemberg item it can identify in its current session context without opening any files. For each item the LLM MUST state:

- Its **name** (the rule slug, agent filename, or skill name)
- Its **category** (rule / agent / skill)
- One sentence describing what it governs or does

This is the actual test. An item loaded into the session at startup will be recallable here. If it cannot be named, it either was not present when the session started or did not register in context.

### Step 2 — Scan disk

The LLM MUST detect the active platform by checking which output directory exists:

- Claude Code: `.claude/rules/`, `.claude/agents/`, `.claude/skills/`
- Cursor: `.cursor/rules/`, `.cursor/agents/`, `.cursor/skills/`
- Copilot: `.github/instructions/`, `.github/agents/`, `.github/skills/`

For each directory that exists, the LLM MUST list every file (or subdirectory for skills) and extract the `name` and `description` from frontmatter where present.

### Step 3 — Cross-reference

The LLM MUST produce one table per category. Entries MUST be matched by name, stripping file extensions for comparison.

| Name | On disk | In context |
|------|---------|------------|
| coding-standards | ✓ | ✓ |
| git-workflow | ✓ | ✗ |

### Step 4 — Report

The LLM MUST state totals for each category:

- **Rules**: N on disk, M recalled, K matching
- **Agents**: N on disk, M recalled, K matching
- **Skills**: N on disk, M recalled, K matching

For any item on disk but not recalled, the LLM MUST note that it may have been added by a sync that ran after this session started — a fresh session will load it.

For any item recalled but not on disk, the LLM MUST note that it may have been deleted or pruned since this session started — a fresh session will not load it.

If all counts match across all categories, the LLM MUST report: `Configuration fully loaded — all N items on disk match context.`

## What this does NOT test

- Whether the LLM is correctly *applying* a rule — only whether it was loaded
- Correctness of rule content or frontmatter
- Drift between source (`llm/`) and synced outputs — run `bluetemberg sync --check` for that

## Completion checklist

- [ ] Recalled config from session context BEFORE reading any file (step 1)
- [ ] Listed the rules, agents, and skills actually present in context (step 1)
- [ ] Cross-referenced the recalled items against disk (steps 2-3)
- [ ] Flagged on-disk-not-recalled items (added by a later sync; fresh session loads them)
- [ ] Flagged recalled-not-on-disk items (deleted or pruned; fresh session drops them)
- [ ] Reported the per-category totals and the pass/fail status string (step 4)

## When NOT to use

- As a substitute for `bluetemberg sync --check` (that tests disk drift, not LLM context)
- On every task — this is a diagnostic tool, not a workflow step
