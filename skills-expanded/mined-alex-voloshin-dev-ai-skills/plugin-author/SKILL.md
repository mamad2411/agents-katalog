---
name: plugin-author
description: >-
  Use this skill when extending, repairing, or improving plugin assets,
  when ingesting a `/feedback` report as a fix-cycle backlog, or when you
  do not remember which lower-level command is right for the job — the
  umbrella workflow for ai-skills plugin-asset authoring and maintenance:
  creating, auditing, fixing, improving, refactoring, and migrating skills,
  agents, rules, hooks, prompts, schemas, and rubrics inside the plugin.
  Auto-classifies the request, loads the right knowledge skills
  (`@prompt-engineering`, `@context-engineering`, `@team-protocols`), and
  spawns the right subagents (`prompt-engineer`, `system-architect`,
  `python-engineer`, `software-engineer`, `qa-engineer`, `eval-judge`) via
  the `Agent` tool.
argument-hint: "<create | audit | fix-feedback | improve | refactor | migrate> [target] [--from <report>] [--deep] [--learnings] [--strict]"
---

<!-- ARCHITECTURAL NOTE: no `context: fork` — like `/develop`, this orchestrator runs in the main thread to retain the `Agent` spawn primitive (subagents cannot spawn subagents). -->

# /plugin-author — Plugin Asset Authoring & Maintenance Orchestrator

Single entry point for the full lifecycle of assets under `plugin/`. Classifies the request, picks a pipeline shape, runs a light single-pass or spawns a DEV → REVIEW → QA team. Absorbs `/plugin-skill-create` and `/plugin-skill-audit`; their SKILL.md files stay on disk as internal procedure references, no longer slash-invocable.

> **YOU MUST orchestrate via `Agent({...})` spawns for the HEAVY pipeline.** Inline Lead edits of prompts/agents/rubrics bypass the per-role review gates and violate `team-protocols`. Every HEAVY role-step is an explicit `Agent({...})` call.

## When to use

"Add a new skill / agent / rule / hook"; "audit this skill — description not triggering"; "fix the findings in this `/feedback` report"; "improve rubric or calibration"; "refactor an oversized SKILL.md"; "migrate an older skill to current spec"; or when scope is unclear and you do not remember which lower-level command applies.

Not for: application/feature code (use `/develop`, `/bugfix`, `/refactor`); Codex/Windsurf parity mirrors (outside `plugin/`); Tier 3 suites (not yet shipped); plugin-wide diagnostic (`/plugin-doctor` directly).

## Operations

| Op | Trigger | Shape | DEV |
|---|---|---|---|
| `create` | "new skill", "scaffold", "add a hook" | scaffold + interview + HEAVY | per asset kind |
| `audit` | "audit", "lint a skill" | SIMPLE; `--deep` → HEAVY | `prompt-engineer` + `eval-judge` (`--deep`) |
| `fix-feedback` | `--from <path>` | HEAVY per finding | per asset kind |
| `improve` | "not triggering", "rubric is fuzzy" | HEAVY (one asset) | `prompt-engineer` or `eval-judge` |
| `refactor` | "split this SKILL.md" | HEAVY + equivalence gate | `prompt-engineer` |
| `migrate` | "update to current spec" | HEAVY per skill | `prompt-engineer` |

Full trigger-phrase + disambiguation table: `operation-router.md`.

## Invocation

```text
/plugin-author create <name> [--type workflow|knowledge|companion] [--agent-spawn] [--ralph]
/plugin-author audit [<name> | --all] [--deep] [--strict] [--fix]
/plugin-author fix-feedback --from .ai-skills-memory/feedback/feedback-2026-05-13-0910.json
/plugin-author improve <name> [--scope description|body|rubric|calibration]
/plugin-author refactor <name>
/plugin-author migrate <name>
/plugin-author                                # no args → one clarifying question, then route
```

`--learnings` (any op) opts into user-global memory via `/learnings-write`; off by default.

## Pre-flight

Read `CLAUDE.md` + `plugin/.claude-plugin/plugin.json`. Load Path B tools: `ToolSearch(select:TeamCreate,TaskCreate,TaskUpdate,SendMessage,TeamDelete,TaskStop,Monitor)`. Treat `@prompt-engineering`, `@context-engineering`, `@team-protocols` as knowledge — never spawn them. Refuse `create`/`fix-feedback`/`improve`/`refactor`/`migrate` on a dirty tree touching the target asset; `audit` without `--fix` is always allowed.

## Classify

Apply `operation-router.md`. Two ops match → pick broader, pass narrower as a flag (`audit --fix`). `--from <path>` → always `fix-feedback`. Ambiguous → ask ONE clarifying question, never silently pick. For `fix-feedback` prefer `<path>.json` (parity counterpart of `<path>.md`) per `feedback-parser.md`; only `.md` → warn + `scripts/parse_feedback_report.py --md` (degraded).

## Build the plan

- `create`/`improve`: 1–3 WPs typically. `audit`: one WP per target (each `--all --deep` skill = one WP).
- `fix-feedback`: one WP per finding; group by severity (H first) then source kind so related findings batch onto one subagent.
- `refactor`/`migrate`: 2–4 WPs (extract → reference → rewire → re-validate).

Wave sizing per `team-protocols/lead-protocol.md`: >6 WPs → split into waves of 3–6, foundations first. After each wave clears, print a checkpoint and auto-continue unless the user pauses within 60 s.

Asset-kind → DEV-role (`asset-to-role-map.md`):

| Asset under `plugin/` | DEV subagent |
|---|---|
| `skills/<name>/SKILL.md` (frontmatter + body + refs) | `ai-skills:prompt-engineer` |
| `agents/<name>.md` | `ai-skills:prompt-engineer` |
| `rules/<name>.md` | `ai-skills:prompt-engineer` |
| `hooks/scripts/<name>.py` | `ai-skills:python-engineer` |
| `schemas/<name>.json` | `ai-skills:system-architect` |
| `eval/judge-rubrics/<name>.md` | `ai-skills:eval-judge` |
| `eval/calibration/<name>/*.md` | `ai-skills:eval-judge` |
| `eval/config.json`, `eval/cases/*` | `ai-skills:system-architect` |

REVIEW (every WP, `disallowedTools: ["Write", "Edit"]`): fresh `ai-skills:prompt-engineer` for prompt assets; `ai-skills:software-engineer` for code/schema. One reviewer, no co-review.

QA (every WP): `ai-skills:qa-engineer` behavioral checks + Lead-side post-checks (`validate.py`, internal audit per `plugin-skill-audit/SKILL.md`, `/plugin-doctor`, `/eval --skill <name> --tier 1` when applicable).

## Pipeline shape

**SIMPLE.** `audit` without `--deep` and trivial scaffolds. Run inline via the absorbed procedure docs (`plugin-skill-create/SKILL.md`, `plugin-skill-audit/SKILL.md`). No subagent spawn.

**HEAVY.** `create` (interview + first DEV pass), `audit --deep`, `fix-feedback`, `improve`, `refactor`, `migrate`. DEV → REVIEW → QA per `@team-protocols`. Prefer Path B; fall back to Path A only on a documented `TeamCreate` technical block per `team-protocols/path-selection-rules.md` — **no silent fallback** (sequential WPs / "simpler" / tmux absence are invalid triggers). Path B `TeamCreate` prompt, file-channel backstop, `Monitor` wiring, Path A spawn loop: see `develop/SKILL.md`, apply verbatim with team name `plugin-author-<op>-<stamp>`.

Every `Agent({...})` `prompt` MUST embed a full G7 spawn payload (six fields: `trace_id`, `subagent_role`, `goal`, `constraints`, `allowed_tools`, `budget`). See `team-protocols/g7-contracts.md`. `subagent-start-budget.py` blocks the third malformed payload — never paste a prose-only prompt.

## Mandatory gates per WP (HEAVY)

WP DONE only after all of: DEV G7 `status=success`; Reviewer `verdict: approved`; QA `qa_verdict: pass`; Lead-side post-checks (`validate.py` exit 0, internal audit `--strict`, `/plugin-doctor` clean, `/eval --skill <name> --tier 1` for user-invocable workflow skills/rubrics). On any failure: requeue with failure as `constraints`, re-spawn DEV — Lead never patches inline. Max 3 cycles per WP, then escalate.

## Eval-loop closure

`create`/`improve` touching a user-invocable workflow skill or rubric MUST close with: rubric present (`plugin/eval/judge-rubrics/<name>.md`, 5 dimensions), calibration ≥ 6 samples (`plugin/eval/calibration/<name>/{good,bad}/`), `/eval --skill <name> --tier 1` pass. Spawn `ai-skills:eval-judge` to author/tune the rubric when missing or when Spearman drifts.

`audit --deep` additionally spawns `ai-skills:prompt-engineer` per target for spec/best-practice (`prompt-engineering/skill-authoring-spec.md`), description (`prompt-engineering/optimizing-descriptions.md`), and security (`prompt-engineering/security-checklist.md`, OWASP LLM Top 10) review. `--all --deep` is opt-in (prints a budget warning).

## Hard rules

- **Plugin scope only.** Touch nothing outside `plugin/`. Codex/Windsurf mirrors get an end-of-run parity-reminder warning — never auto-edit them.
- **English-only assets** per repo CLAUDE.md.
- **Eval-first** for any prompt-modifying op (never change a prompt/tool/schema without defining how to measure impact).
- **G7 spawn payloads required** on every `Agent({...})` call.
- **Never auto-rewrite prose.** Inherit the safe-fix table from `plugin-skill-audit/SKILL.md`; every prose change goes DEV → REVIEW → QA, never regex.
- **Never rename a skill** automatically — refuse and ask.
- **Counts are part of every closure.** Add/hide a skill/agent/rubric/sample → bump `EXPECTED_COUNTS` in `plugin/dev/validate.py` same change set.
- **Memory L4 by default.** L5 only with `--learnings` via `/learnings-write`.
- **Never silently delete an absorbed skill.** Preserve its SKILL.md with `disable-model-invocation: true` + a description pointing here.

## Failure modes

Ambiguous → ask one question. `fix-feedback` missing `.json` → warn, `--md` fallback, WPs `provenance: md-fallback`. Wave overflow → split per `lead-protocol.md`. Gate failure → requeue (failure as `constraints`); max 3 cycles; escalate. `TeamCreate` error → Path A fallback, verbatim error. Spawn-budget exhausted → surface hook diagnostic.

## Memory writes

- L4 every run: append `{ts, op, target, wps, gate_results, fix_cycle_ref?}` to `.ai-skills-memory/plugin-author/runs.log`.
- L4 on `fix-feedback`: write `.ai-skills-memory/plugin-author/fix-cycles/<feedback-stamp>.json` mapping each closed WP to its `finding_id` so future `/feedback` runs detect "fixed".
- L5 only with `--learnings`: delegate to `/learnings-write` — never write `~/.claude/ai-skills/learnings.md` directly.

## Integration

- **Reads (procedure docs)**: `plugin-skill-create/SKILL.md`, `plugin-skill-audit/SKILL.md` (both `disable-model-invocation: true`).
- **Reads (knowledge)**: `@prompt-engineering` (incl. cached agentskills.io digests `prompt-engineering/skill-authoring-spec.md` + `optimizing-descriptions.md`), `@context-engineering`, `@team-protocols`, `@subagent-spawn`.
- **Reads (project)**: `CLAUDE.md`, `plugin/.claude-plugin/plugin.json`, `plugin/dev/validate.py` `EXPECTED_COUNTS`.
- **Spawns**: `ai-skills:` `prompt-engineer`, `system-architect`, `python-engineer`, `software-engineer`, `qa-engineer`, `eval-judge`.
- **Writes**: assets under `plugin/skills|agents|rules|hooks|eval|schemas/`; logs `.ai-skills-memory/plugin-author/runs.log` + `fix-cycles/`.
- **Companions**: `/plugin-doctor`, `/eval`, `/feedback` (input for `fix-feedback`), `/learnings-write`.
- **Supporting docs**: `operation-router.md`, `feedback-parser.md`, `asset-to-role-map.md`, `scripts/parse_feedback_report.py`.
- **Eval (planned)**: `plugin/eval/judge-rubrics/plugin-author.md`, `plugin/eval/calibration/plugin-author/{good,bad}/`, `plugin/eval/cases/plugin-author/`.
