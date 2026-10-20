# PostTool Hook Self Correction

## Summary

**One-sentence:** Produces a PostToolUse-hook config wiring validators (ruff/eslint/tsc/pytest) into Write/Edit hooks so failures appear to the agent as tool errors and self-correct on the next turn.

**One-paragraph:** Code-editing agents that "remember to lint" are unreliable — the model omits the check exactly when it matters (long contexts, tricky edits). PostToolUse hooks (matcher Write|Edit) make verification deterministic: hook stderr is injected into the next turn as a tool-result error; the agent is RLHF-trained to retry-with-fix. The methodology emits a hook spec scoped per file pattern with a validator selection and timeout.

**Ефективно для:** Claude Code user whose agents keep landing code that fails ruff/tsc; manual "now run lint" prompts waste turns.

## Applies If (ALL must hold)

- Code-editing agent running with Claude Code's hook system.
- CI bots or headless runs without human-in-loop lint discipline.
- Strict-format pipelines (markdownlint, JSON schema, ruff, tsc).
- Validator runtime &lt; 5s per file.

## Skip If (ANY kills it)

- Read-only research agent — no mutations to validate.
- Slow validator (&gt;5s) — hook stalls every Edit.
- Exploratory refactor spanning many files where mid-flight failures are expected.
- Project has no validator (greenfield prototype).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `file-patterns.yaml` | list of {glob, validator_cmd, timeout_seconds} | operator |
| `settings_json_path` | path | repo (.claude/settings.json) |
| `validators_installed` | list of {name, version} | repo |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[tdd-workflow]] | Hook fires after Write/Edit on test files. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 rules: scope validator to file, non-zero exit surfaces stderr, timeout cap, no infinite-retry loop, exempt patterns documented. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the hook-config artefact. | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: full-suite validator per file, no timeout, infinite retry loop, wrong matcher. | ~700 |
| `content/04-procedure.xml` | recommended | 4-step procedure: list file patterns → pick validator → set timeout → emit settings.json. | ~600 |
| `content/05-examples.xml` | recommended | Ruff + Vitest + tsc hook configs. | ~600 |
| `content/06-decision-tree.xml` | essential | Picks scope, validator, timeout from drivers. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `parse_file_patterns` | haiku | Mechanical YAML→typed list. |
| `pick_validators` | sonnet | Tradeoff between coverage and runtime. |
| `audit_for_loops` | opus | Detect self-correction infinite-loop risk. |
| `emit_hook_json` | sonnet | Mechanical emission. |

## Templates

| File | Purpose |
|---|---|
| `templates/settings-json-snippet.json` | PostToolUse hook fragment ready to merge into settings.json. |
| `templates/_smoke-test.yaml` | Minimum pattern (one ruff hook). |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-posttool-hook-self-correction.py` | Validates config JSON. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[tdd-workflow]]
- [[multi-agent-production-bus]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on `language` (python → ruff; typescript → tsc/eslint; mixed → multi-validator), then on `runtime_per_file` (&lt;1s → keep; 1-5s → narrow glob; &gt;5s → defer to commit gate). Each leaf cites a rule id.
