---
name: brag-me
description: Turn your real contributions to a project into resume-ready bullets, pulled from git history, merged PRs, and quality-gate metric trends so every claim is evidence-backed. Use when the user wants a brag document, resume/CV bullets, a work log of what they shipped, help describing a job's impact, or to remember what they did on a project before they forget.
---

# Brag Me

## Quick start

Facts first, prose second. The script gathers verifiable evidence; you distill it — never invent a number the evidence doesn't support.

1. **Collect** — run [scripts/brag-me.mjs](scripts/brag-me.mjs) `collect --author=<your git name/email>` in the repo. It writes `brag-facts.json`: your commits (by type), diff totals, merged PRs, and the coverage/duplication trend from any committed `baseline.json`.
2. **Interview** — for impact git can't see (business outcome, scale, latency, team size), ask the user. Mark those as self-reported.
3. **Write two files** — `brag.md` (private log, every bullet linked to a commit/PR/number) and `resume.md` (distilled, XYZ format, sanitized).

Formats, interview questions, sanitization rules, and templates: [REFERENCE.md](REFERENCE.md).

## Honesty rules (non-negotiable)

- **Every claim traces to evidence** — a commit, a PR, or a measured metric delta. No evidence → the bullet is qualitative, not a fabricated number.
- **Measured vs self-reported** — numbers from git/PRs/baseline are measured. Numbers from the interview are labeled self-reported. Never blur the two.
- **Attribute honestly** — `--author` filters to *your* commits. Don't claim a team's work as yours.
- **No inflation** — "modularized a module" does not become "architected a world-class scalable system". Describe what the diff shows.

## Sanitized by default

`resume.md` ships generic: no employer name, client name, internal system name, or confidential data — "a payments gateway", not "AcmeCorp's billing service". Note what was genericized; the user chooses what to de-anonymize. `brag.md` (private) may keep real names since it's for the user's own memory.
