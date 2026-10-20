# ScholarAIO — Cline Rules

This wrapper is intentionally light. Full shared project instructions are in `AGENTS.md` at the repository root. **Read `AGENTS.md` before proceeding with any task.**

## Quick Reference

- Shared entry doc: `AGENTS.md`
- Deep reference: `docs/guide/agent-reference.md`
- CLI entry point: `scholaraio --help`
- Skills: `.claude/skills/*/SKILL.md` (Cline reads these natively)
- Fresh runtime defaults: `data/libraries/`, `data/spool/`, `workspace/`
- User output: write to `workspace/`, not the repo root or `scholaraio/`
- Tests: `python -m pytest -q -p no:cacheprovider`
