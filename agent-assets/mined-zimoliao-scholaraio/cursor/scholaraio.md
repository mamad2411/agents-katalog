---
description: ScholarAIO project instructions and research workflow router
alwaysApply: true
---

# ScholarAIO Cursor Entry

Use this Project Rule as the Cursor-native entry point. This rule was checked
against Cursor's official rules documentation on 2026-04-10. Full shared
project instructions live in `AGENTS.md`; do not duplicate them here.

Before ScholarAIO work:

- Read `AGENTS.md` at the repository root.
- For deeper repo, runtime, or skill organization details, read `docs/guide/agent-reference.md`.
- For paper search, reading, ingest, export, writing, or scientific-runtime
  tasks, read the matching workflow in `.claude/skills/*/SKILL.md`.
- Use `scholaraio --help` and the specific skill instructions before running
  ScholarAIO CLI commands.
- Write user-facing drafts, reports, exports, and analysis outputs under
  `workspace/`, not the repository root or `scholaraio/`.
- Keep Cursor integration on native Project Rules plus the ScholarAIO CLI.
