# AGENTS.md

## Project Overview

This repository (`liustack/vibemaster`) has three overlapping identities:

1. **GitHub profile repository** — `README.md` (and `README.zh-CN.md`) render on the GitHub profile page at [github.com/liustack](https://github.com/liustack). Keep it concise and professional.
2. **The vibemaster skill stack** — `skills/` is the product core: a four-skill work loop (shaping unformed intent into specs and designs, coding discipline from plan through review, root-cause digging, task-state snapshots) distributed through multiple plugin marketplaces (Claude Code plugin marketplace, Codex `~/.agents/skills`, skills.sh, etc.).
3. **Shared resources hub** — `scripts/`, `docs/`, and `rules/` collect reusable scripts, docs, and agent rules shared across all repositories.

## Directory Structure

```
README.md          # GitHub profile page content
scripts/           # Shared utility scripts used across repos
skills/            # The vibemaster skill stack (product core)
docs/philosophy.md # Design principles — read before designing or revising any skill
docs/              # Shared documentation and references
rules/             # Reusable agent rules — drop-ins for .claude/rules/, paste-able into AGENTS.md (see rules/README.md)
```

## Docs Discovery

Before starting work, run:

```bash
bash scripts/list-docs.sh
```

It lists every doc under `docs/` and `rules/` with its summary and "Read when" hints. Check the hints and read the relevant docs before coding.

## Conventions

- `README.md` is public-facing. Write in English, keep it clean and professional.
- `scripts/` contains cross-repo utility scripts (e.g., automation, data fetching).
- `skills/` follows the standard skill format: each skill is a directory with a `SKILL.md` and optional `references/` folder.
- Skill `description` fields must be lean and keyword-first: harnesses inject every installed skill's description into context (Claude Code caps the whole listing at ~1% of the context window and truncates long entries), so the opening clause must carry the trigger keywords.
- Triggering discipline for descriptions: state what the skill is + when to use + how it differs from neighboring skills, add an explicit exclusion clause ("Do not trigger for…") when the positive triggers are broad, never use moral imperatives (MUST/ALWAYS — they cause both over- and under-triggering), and one trigger per branch (do not restate the same scenario in synonyms — it wastes the listing budget).
- Invocation control for all skills: none. The description wording is the first guard. `shaping` has a broad surface: product and feature definition may trigger from ordinary wording, while life and career decisions are out of scope entirely (its description excludes them, and personal judgment lives in opcstack's `opc-founder`). Because a mistaken load can turn into unwanted questioning, its body starts with a silent gate. A clear mismatch completes the original request without announcing the gate, asking a diagnostic question, or creating a file.
- Testing layout: deterministic code tests (for scripts/) go in `tests/` once such code exists. Model-behavior evals live in repo-level `evals/<skill-name>/` (author-side, official skill-creator schema) — never inside `skills/`, so installs stay clean. Run `scripts/check-skills.sh` and `scripts/check-contract.sh` before committing skill or manifest changes.
- Language regime: skill bodies, references, and docs are written in English (the authoritative version) with a `.zh-CN.md` translation alongside. Skill descriptions are English-framed: the capability sentence and the exclusion clause are written once, in English, and Chinese appears only as trigger words a user would actually type. They are the trigger surface, not a translated document, so restating the same sentence in both languages buys no extra coverage and spends a listing budget capped at ~1% of the context window. Cross-references and the docs index point at English files only, and authoritative files carry no language links (translations link back to them).
- Working drafts (designs, plans, ideation output, diagnosis logs, research notes) go in `.issues/<YYYY-MM-DD-topic>/` (gitignored via `.git/info/exclude`), organized by task, not by type.
- When adding new shared resources, place them in the appropriate directory and keep naming consistent.
