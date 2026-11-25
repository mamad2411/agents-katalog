---
name: llm-triggers
description: "Trigger subsystem for the kb suite (design phase): condition vocabulary, trigger banks, per-runtime interpreters. Successor to llm-must-read-kb. Agent MUST load when authoring or repairing a trigger -- a (condition, directive) pair -- in any bank, or when deciding whether a directive needs a condition of its own."
---

# llm-triggers

The kb suite's trigger subsystem. The `triggers:` field is specified in
`design.kb/040-design.kb/triggers-field.md`; bank conventions remain
`Skill(llm-must-read-kb)`. The rest of `design.kb/` is design-phase.

## Tools

`llm-triggers/bin/llm-triggers-lint [PATH]` -- run by path. Checks frontmatter
triggers under PATH (default `.`), skipping what `.gitignore` excludes. Run it
after editing any trigger; exit 0 clean, 2 on error.

Errors: a bare directive in an unconditional carrier; any `requires:` or
`depends:` -- `triggers:` is the only field. Warnings: a `triggers:` entry with
no `read:`; a `read:` that does not resolve.
