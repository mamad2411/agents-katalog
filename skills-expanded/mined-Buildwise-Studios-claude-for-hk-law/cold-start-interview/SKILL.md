---
name: cold-start-interview
description: >
  Run the cold-start interview to configure your Hong Kong immigration practice profile.
  Use on first install, when the practice profile is missing or has [PLACEHOLDER] markers,
  or when the user says "set up the plugin" or "configure hk-immigration".
argument-hint: "[--redo to re-run]"
---

# /cold-start-interview

Writes `~/.claude/plugins/config/claude-for-hk-law/hk-immigration/CLAUDE.md`.

## Instructions

1. Read `~/.claude/plugins/config/claude-for-hk-law/hk-immigration/CLAUDE.md`. If populated and `--redo` not passed, confirm before overwriting.
2. Read `~/.claude/plugins/config/claude-for-hk-law/company-profile.md` if it exists.
3. Ask (quick start ~2 min): practice setting (firm / in-house / solo), role (lawyer / non-lawyer with solicitor access), primary work types, escalation contact, and **language** (English only / bilingual client letters / Traditional Chinese client-facing).
4. Optional: paths to seed templates, house style guides, or prior work product.
5. Write the practice profile with sections: Who we are, Who's using this, Language, Escalation, Seed documents, Outputs (reviewer note format per plugin CLAUDE.md).
6. For language rules, read `references/language-output.md` at repo root if present in context, or apply defaults from plugin template.

Doctrine reference: the shipped `CLAUDE.md` in this plugin contains Hong Kong legal knowledge; the config file captures **your** playbook and preferences.
