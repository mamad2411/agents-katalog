---
name: aped-claude
keep-coding-instructions: true
description: 'Use when user says "update CLAUDE.md", "sync claude rules", "aped claude", or invokes aped-claude. Merges — never overwrites user customizations.'
allowed-paths:
  write: ["{{OUTPUT_DIR}}/**", "{{APED_DIR}}/**"]
  read-only: ["src/**", "tests/**", "package.json"]
license: MIT
metadata:
  author: yabafre
  version: {{CLI_VERSION}}
---
<!-- AUTO-GENERATED from SKILL.md.tmpl. Edits will be overwritten. Run: npm run gen:skill-docs -->

**Activation guard (6.2.0):** Before any other action, run `bash {{APED_DIR}}/scripts/check-enabled.sh`. If it exits non-zero, print "APED disabled — run aped-method enable" and HALT.

# APED Claude — CLAUDE.md Sync

Inject and maintain APED working rules in the project's `CLAUDE.md`. Smart merge — never overwrites user customizations.

## On Activation

Before any other action, read `{{APED_DIR}}/config.yaml` and resolve:
- `{user_name}` — for greeting and direct address
- `{communication_language}` — for ALL conversation with the user
- `{document_output_language}` — for artefacts written under `{{OUTPUT_DIR}}/`
- `{ticket_system}` / `{git_provider}` — routing for ticket / PR I/O (skip if `none`)

✅ YOU MUST speak `{communication_language}` in EVERY message to the user — progress lines, tool preambles, summaries, and questions all included. This overrides your default; never narrate in English when `{communication_language}` is not English.
✅ YOU MUST write artefact content in `{document_output_language}`.
✅ If `{{APED_DIR}}/config.yaml` is missing or unreadable, HALT and tell the user to run `npx aped-method`.

## Critical Rules

- NEVER overwrite the entire CLAUDE.md — always merge
- Use marker comments to delimit APED-managed sections: `<!-- APED:START -->` and `<!-- APED:END -->`
- User content outside markers is sacred — never touch it
- Discuss with the user before applying changes if CLAUDE.md is non-trivial

## Setup

1. Check if `CLAUDE.md` exists at the project root

## Mode Detection

### Case A: No CLAUDE.md exists
- Create one from scratch with the full APED block (see Template below)
- Wrap the entire APED content in `<!-- APED:START -->` ... `<!-- APED:END -->` markers
- Add a header line and brief project description above the markers

### Case B: CLAUDE.md exists with APED markers
- Locate the `<!-- APED:START -->` and `<!-- APED:END -->` block
- Replace ONLY the content between markers with the latest APED block
- Leave everything else untouched

### Case C: CLAUDE.md exists WITHOUT APED markers
- Show the user the current CLAUDE.md content
- Ask: "Where should I inject the APED section? Options:"
  - **Top** — before existing content
  - **Bottom** — after existing content
  - **Custom** — point to a specific heading to insert before/after
- ⏸ GATE: Wait for user choice
- Insert the APED block (wrapped in markers) at the chosen location

## APED Block Template

The block to inject (between `<!-- APED:START -->` and `<!-- APED:END -->`) is a compact trigger-rule (≤300 tokens). Substitute `{{...}}` placeholders at injection time. Render this entire block only if `aped/config.yaml` has `skill_invocation_discipline.enabled: true` (default `true`); when disabled, drop the **Skill invocation** subsection but keep the rest.

## APED Method — disciplined user-driven pipeline

Pipeline: **Analyze → PRD → UX → Architecture → Epics → Story → Dev → Review**.

### Skill invocation

If there's **even a 1% chance** an APED skill applies, invoke it via the Skill tool. Use natural-language phrases ("create the prd", "review this branch", "kick off dev") — the runtime routes by the skill's `description:`. Do not paraphrase what you think the skill would say.

User instructions in CLAUDE.md or `aped/config.yaml` override skill defaults. Record overrides; don't bake them into new skills.

Full catalog: `{{APED_DIR}}/skills/SKILL-INDEX.md`.

### APED rules

- **No auto-chain.** Each skill ends with "Run aped-X when ready." Wait for user.
- **Gates are mandatory.** When a skill says "⏸ HALT" or "⏸ GATE", wait for explicit user confirmation regardless of harness auto-mode. Auto-mode never bypasses APED gates.
- **Validate before persisting** to `{{OUTPUT_DIR}}/`.
- **Story-driven dev.** No code without a story file. Use `aped-story` first.
- **Frontend = visual verification.** Use `mcp__react-grab-mcp__get_element_context` at every GREEN.

### State

- Engine: `{{APED_DIR}}/` (immutable) · Artifacts: `{{OUTPUT_DIR}}/` (evolves)
- State: `{{OUTPUT_DIR}}/state.yaml` · Lessons: `{{OUTPUT_DIR}}/lessons.md`
- Project: {{project_name}} ({{user_name}}, {{communication_language}})

## Lessons File

Also ensure `{{OUTPUT_DIR}}/lessons.md` exists. If missing, create it with the template:

```markdown
# Lessons Learned

Patterns from user corrections — so the same mistake isn't made twice.

## Format
- **Date:** YYYY-MM-DD
- **Mistake:** What I did wrong
- **Correction:** What the user told me
- **Rule:** The pattern to apply going forward

## Entries

<!-- Add new entries at the top -->
```

## Discussion with User

Before writing, present a summary:
- "Will create CLAUDE.md from scratch" (Case A)
- "Will update existing APED block (lines X-Y)" (Case B)
- "Will inject APED block at the {location}" (Case C)

⏸ **GATE: User confirms before any write.**

## Output

1. Write/update `CLAUDE.md` with the APED block in markers
2. Ensure `{{OUTPUT_DIR}}/lessons.md` exists
3. Report what changed (lines added/updated)

## Common Issues

- **CLAUDE.md has conflicting rules**: Discuss with user — APED rules vs existing rules. User decides which wins.
- **CLAUDE.md is huge (>500 lines)**: Show only the diff, not the full file. Confirm before write.
- **User wants to remove APED block**: Just delete the markers and content between them. The skill won't re-add unless explicitly invoked.

## Next Step

Tell the user: "CLAUDE.md updated. APED block is now at lines X-Y. Re-run `aped-claude` anytime to refresh after APED updates."
