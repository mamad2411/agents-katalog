---
name: grok-delegate
description: >-
  Use when delegating Grok task nodes via native CLI (-p, -r, worktrees, leader)
  from Codex/OpenCode waves and tune loops. NOT for harness sync or wrappers.
license: MIT
metadata:
  author: wyattowalsh
  version: "1.2.0"
user-invocable: true
---

# Grok Delegate

Cross-harness orchestration of **Grok Build native CLI only**. Parent harness owns the macro graph; Grok executes micro nodes.

## Dispatch

| $ARGUMENTS | Action |
| --- | --- |
| *(empty)* | Show pre-flight, wave taxonomy, critical rules, and reference index |
| `preflight` | Run `scripts/preflight.sh`; stop on `fail` checks |
| `wave <0\|1\|2>` | Show command templates for scout / build / verify waves |
| `tune` | Show session resume / delta prompt loop |
| `leader` | Show leader pool lifecycle |
| `ledger` | Show session ledger schema |
| `patterns` | Show orchestrator Pattern A–F → Grok flag mapping |

## Classification Gate

1. **Use** when the parent harness owns a multi-node graph and at least one node should run on Grok Build via native CLI.
2. **Use** when a gate failed and the parent needs `-r <sessionId>` tune passes on an existing ledger row.
3. **Do not use** for single-session work the parent can finish directly.
4. **Do not use** for Grok config/MCP sync, skill installs, or nested Grok-in-Grok orchestration.
5. **Malformed dispatch** — `wave` without `0|1|2` is invalid; show valid tiers or the empty-args gallery. Never invent a default wave.

## Operator Contract

### `preflight`

1. Run `bash skills/grok-delegate/scripts/preflight.sh` from any cwd (bundled `doctor.py`; optional `--cwd` for target repo).
2. Stop fleet dispatch when JSON `ok` is false or `grok-binary` is `fail`.
3. Treat `warn` as advisory; do not block unless the parent policy requires a clean doctor.

### `wave <0|1|2>`

1. Load [references/command-templates.md](references/command-templates.md) for the requested tier.
2. Assign distinct `-w w<wave>-<role>-<n>` names and non-overlapping file ownership for wave 1.
3. State the parent gate that must pass before the next wave.

### `tune`

1. Load [references/session-ledger.md](references/session-ledger.md) and resume with `-r <sessionId>`.
2. Prefix delta prompts with `Tune:`; cap `parent_tune_count` at 3 per `node_id`.
3. Never default `--always-approve`.

### `leader`

1. Load [references/leader-lifecycle.md](references/leader-lifecycle.md).
2. Start one leader per cwd pool; kill orphans with `grok leader kill` after graph completion.

### `ledger`

1. Load [references/session-ledger.md](references/session-ledger.md).
2. Require N terminal ledger rows before opening the next parent gate.

### `patterns`

1. Load [references/graph-patterns.md](references/graph-patterns.md) and map to `/orchestrator` Pattern A–F.
2. Keep parent accounting: N dispatched nodes = N resolved before synthesis.

### *(empty)*

1. Show pre-flight, wave taxonomy, critical rules, and the reference index.
2. Run the Classification Gate on the current parent request before dispatching nodes.

## Canonical Vocabulary

| Term | Meaning |
| --- | --- |
| **parent harness** | Codex, OpenCode, or Claude session owning the macro DAG |
| **node** | One `grok` subprocess invocation for a graph task |
| **wave** | Staged batch of nodes (0 scout, 1 build, 2 verify) |
| **gate** | Parent checkpoint before the next wave |
| **tune** | `-r <sessionId> -p "Tune: ..."` delta on an existing node |
| **ledger** | `grok-delegate-ledger.jsonl` tracking `sessionId` per node |
| **worktree** | `-w w<wave>-<role>-<n>` git isolation per parallel builder |
| **leader pool** | Shared `grok agent leader` backend for dense graphs |

## Critical Rules

1. **Native CLI only** — no `bin/gk`, MCP control server, or custom headless wrapper scripts.
2. **Pre-flight mandatory** — run `scripts/preflight.sh` before fleet dispatch.
3. **Parent owns the graph** — Grok depth is 1; parallelize siblings via parent bash, not nested Grok orchestration.
4. **Never default `--always-approve`** for cross-harness delegation.
5. **Always `--no-auto-update` and explicit `--cwd`** on automation paths.
6. **Accounting** — N dispatched nodes = N terminal ledger rows before the next gate.
7. **One writer per worktree** — non-overlapping file ownership across parallel wave 1 nodes.

## When to use

- Parent dispatches independent Grok nodes via bash (Pattern A/E).
- Tune-in-place after gate failure: `-r <sessionId>`.
- Parallel builders with `-w` worktrees or hypothesis `--best-of-n`.

## When NOT to use

- Single-session work the parent can do directly.
- Grok config/MCP sync — `/harness-master`.
- Skill installs — Skills CLI dry-run preview only (no live `--apply` unless maintainer requests).
- Nested Grok-in-Grok graphs beyond platform depth 1.

## Pre-flight

Authoritative procedure: Operator Contract → `preflight` above.

```bash
bash skills/grok-delegate/scripts/preflight.sh
```

Inspect target repo: `cd <target-repo> && grok inspect --json` (`grok inspect` has no `--cwd` flag).

## Three-tier model

1. **Parent** — `/orchestrator` or OpenCode Ensemble owns waves and gates.
2. **This skill** — templates, ledger, safety, recovery.
3. **Grok CLI** — `-p`, `-r`, worktrees, leader, optional `grok agent stdio`.

## Wave taxonomy

| Wave | Purpose | Typical `--agent` | `--max-turns` |
| --- | --- | --- | --- |
| 0 scout | Read-only exploration | `researcher` | 8 |
| 1 build | Implementation | repo agent | 25 |
| 2 verify | Tests, review | `code-reviewer` | 10 |
| tune | Delta on session | inherit | 10 |
| hypothesis | Competing theories | `researcher` | 12 |

Templates: [references/command-templates.md](references/command-templates.md).

## Single node

```bash
grok --no-auto-update \
  -p "<self-contained task>" \
  --cwd "<absolute-repo-path>" \
  --output-format json \
  --max-turns 25 \
  --agent "<agent-name>"
```

Parse JSON per [references/output-json.md](references/output-json.md). Append ledger row per [references/session-ledger.md](references/session-ledger.md).

## Tune loop

```bash
grok --no-auto-update \
  -r "<sessionId>" \
  -p "Tune: <delta only>" \
  --cwd "<same cwd>" \
  --output-format json \
  --max-turns 10
```

Cap `parent_tune_count` at 3 per `node_id`.

## Parallel wave dispatch

Dispatch **N independent bash subprocesses** in one parent message. Each node gets unique `-w w<wave>-<role>-<n>` and non-overlapping ownership. See [references/concurrency.md](references/concurrency.md).

## Leader pool

```bash
grok agent leader --no-exit-on-disconnect --no-auto-update
```

Clients attach with `grok agent --leader`. Details: [references/leader-lifecycle.md](references/leader-lifecycle.md).

## Recovery ladder

1. Node fail → one retry; else ledger `failed`.
2. JSON parse fail → `--output-format plain` triage.
3. Leader dead → `grok leader list`; restart pool.
4. Auth fail → stop fleet; fix doctor `fail` checks.

## Completion criteria

- Pre-flight doctor JSON `ok: true`
- Every dispatched node has terminal ledger status
- Parent gate passed or explicit user abort recorded
- Orphan leaders killed: `grok leader kill`

## Validation

`check.py` runs skill validation, eval validation, audit, bundled `doctor.py` smoke, and `parse_grok_json` smoke.

```bash
uv run python skills/grok-delegate/scripts/check.py
uv run pytest tests/test_grok_delegate_skill.py tests/test_grok_delegate_preflight.py -q
uv run python skills/skill-creator/scripts/package.py skills/grok-delegate --dry-run
```

## Reference index

| File | Content |
| --- | --- |
| [wave-dag.md](references/wave-dag.md) | Wave gates on bash dispatch |
| [graph-patterns.md](references/graph-patterns.md) | Orchestrator A–F mapping |
| [command-templates.md](references/command-templates.md) | Copy-paste invocations |
| [output-json.md](references/output-json.md) | Headless JSON fields |
| [session-ledger.md](references/session-ledger.md) | Ledger schema |
| [agent-map.md](references/agent-map.md) | Repo agents → `--agent` |
| [concurrency.md](references/concurrency.md) | Budgets, naming |
| [leader-lifecycle.md](references/leader-lifecycle.md) | Leader start/stop |
| [acp-driver.md](references/acp-driver.md) | Official ACP stdio excerpt |
| [safety-permissions.md](references/safety-permissions.md) | Permission matrix |
| [doctor-output.md](references/doctor-output.md) | Bundled doctor JSON |

Official docs: https://docs.x.ai/build/cli/headless-scripting

## Scope boundaries

**IS for:** native Grok CLI delegation, wave templates, session tune loops, parallel worktree dispatch, leader pool policy.

**NOT for:** Grok config sync, custom wrappers, MCP servers, or live `skills sync --apply` unless the maintainer requests it.