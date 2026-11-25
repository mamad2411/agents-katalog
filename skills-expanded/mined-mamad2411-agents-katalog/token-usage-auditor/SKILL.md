---
name: token-usage-auditor
description: Audit project token usage from local Codex and Claude Code logs. Use when the user asks to measure token burn, token consumption, project attention, agent usage, Codex/Claude Code usage, token efficiency, or lifecycle telemetry for a project.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Token Usage Auditor

Measure token usage as project telemetry: where agent attention went, how much fresh work versus cached context was spent, and which sessions should be tied back to project phases and artifacts.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
├── scripts/
│   └── collect_token_usage.py
└── references/
    └── data-model.md
```

## Core Principles

- Treat token usage as attention and cost telemetry, not as quality by itself.
- Prefer local exact logs for Codex and Claude Code before asking the user for estimates.
- Keep raw prompts and message text out of project memory by default; record only session metadata, usage totals, classification, and artifact links.
- Preserve agent-specific token fields. Do not collapse prompt cache reads, cache creation, fresh input, reasoning output, and normal output into one unexplained number.
- Mark inferred phase/task labels with confidence. Do not invent artifact links when no commit, report, run, or paper section can be tied to a session.

## Quick Start

For the current project, run:

```bash
python3 <installed-skill-dir>/scripts/collect_token_usage.py --project-root .
```

For a recent window:

```bash
python3 <installed-skill-dir>/scripts/collect_token_usage.py --project-root . --since 2026-05-01 --until 2026-05-31
```

To write repo-local reports:

```bash
python3 <installed-skill-dir>/scripts/collect_token_usage.py --project-root . --format markdown --output docs/reports/token_usage/2026-05.md
python3 <installed-skill-dir>/scripts/collect_token_usage.py --project-root . --format json --output memory/token_ledger/sessions.json
```

The script is read-only with respect to Codex and Claude Code logs. It writes only when `--output` is provided.

## Workflow

1. Identify the project root.
   - Use `git rev-parse --show-toplevel` when possible.
   - For research project control roots, use the shared root if the user wants cross-component accounting, or `code/` / `paper/` if they want component-local accounting.

2. Run the collector.
   - Include `--since` and `--until` when the user asks for a week, month, phase, or release window.
   - Use `--format markdown` for discussion and `--format json` when updating project memory.
   - Use `--codex-root` or `--claude-root` only when logs live outside the defaults.

3. Interpret the report.
   - `total_context_tokens`: all context observed by the agent, including cached reads when the provider reports them.
   - `fresh_tokens`: non-cached input plus cache creation plus output. Use this as the closer proxy for incremental cost/effort.
   - `cached_tokens`: prompt-cache reads or cached input. Use this as context reuse, not equal fresh work.
   - `session_count`: number of project-matched local sessions.

4. Add project labels only when supported.
   - `phase`: idea, literature, design, implementation, experiment, diagnosis, writing, rebuttal, release, maintenance, tooling, project-management.
   - `task_type`: design, implementation, debug, writing, review, release, sync, setup, experiment, diagnosis, literature, coordination.
   - `confidence`: exact, inferred, manual, unknown.

5. Connect to artifacts.
   - Link sessions to commits, PRs, experiment runs, reports, paper sections, or memory updates only when there is evidence from git history, docs, user notes, or the session metadata.
   - If artifact linkage is not known, leave it blank and report the session as unlinked.

## Updating Project Memory

Use `references/data-model.md` when writing long-lived project memory.

Recommended outputs:

- `docs/reports/token_usage/YYYY-MM.md` for human-readable monthly reports
- `memory/token_ledger/sessions.json` for structured session summaries
- `memory/token_ledger/README.md` only if the project needs policy notes

Do not commit copied raw transcript logs unless the user explicitly asks and privacy has been reviewed.

## Report Framing

When summarizing, separate these conclusions:

- attention allocation: what the project focused on
- fresh token burn: approximate incremental token cost
- context reuse: cached/read context that made work cheaper or less repetitive
- yield: shipped commits, reports, experiments, paper sections, decisions, or memory updates
- friction: repeated context setup, failed commands, abandoned branches, duplicate analysis, or high-burn sessions without artifacts

Avoid saying high token burn means good work. Prefer phrasing such as: "token usage was concentrated in experiment diagnosis; yield was decision-heavy rather than commit-heavy."
