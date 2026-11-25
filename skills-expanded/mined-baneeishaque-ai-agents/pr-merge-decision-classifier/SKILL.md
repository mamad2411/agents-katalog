---
name: pr-merge-decision-classifier
description: Composer — classify a PR's merge decision with a local Laya (Jev wire-compatible) System One model: build read-only state from gh, ask typed choice/score/noul questions, apply the confidence/risk gate, output a MERGE/HOLD verdict; optional --execute auto-merge on MERGE.
category: Composer
---

# PR Merge Decision Classifier Skill (v1)

> **Skill ID:** `pr-merge-decision-classifier`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

A composer skill that turns a pull request into a deterministic merge decision using a
**System One** model — a typed-decision model (no text generation) that answers `choice`,
`score`, and `noul` (calibrated binary) questions over a JSON state object. It builds a
read-only PR state via `gh`, sends it to a `POST /v1/systemone` endpoint, and applies a
fixed confidence/risk gate to emit a `MERGE` / `HOLD` verdict with per-condition reasons.

The default backend is a **local Laya server** (`laya-system-one`, keyless, offline, Jev
wire-compatible); hosted alternates (`apimaster`, `morphllm`, `typesafe`) speak the same
wire protocol and are optional. With `--execute`, the skill merges automatically — and only
ever — on a `MERGE` verdict, via the fixed command
`gh pr merge <N> --repo <R> --rebase --delete-branch`. The default remains decision-only.

The classifier is **decision support**: it never bypasses Stage 4 verification or the user's
per-PR merge approval policy; it never merges on `HOLD` or on any error.

## Composition Rationale

This skill is a **composer**; it orchestrates without reimplementing:

| Composed Skill | Used for |
| --- | --- |
| [`opencode-jsonc-util`](../../../opencode-jsonc-util/SKILL.md) | `scripts/read-jsonc.py` reads `provider.<name>.api` base URLs and key locations from the OpenCode JSONC config for hosted backends |

The remaining dependencies are direct tools, not skills: the GitHub CLI (read-only PR state;
the sanctioned merge command), `curl`/`urllib` (health + `/v1/systemone`), `npx` (local Laya
server). No config files are mutated; API keys are never printed.

## Related Skills

- [`github-repo-commit-fetch`](../../../github-repo-commit-fetch/SKILL.md) — read-only `gh api` fetch primitives
- [`gh-pr-edit`](../../../gh-pr-edit/SKILL.md) — PR title/body viewing and editing via `gh` CLI
- [`mise-tool-management`](../../../mise-tool-management/SKILL.md) — runtime tool resolution (§3.3)
- [`skill-library-domain-grouping`](../../../general/skill-library-domain-grouping/SKILL.md) — taxonomy placement

## Source Rules

| Rule File | Scope Incorporated |
| --- | --- |
| [`ai-rule-standardization-rules.md`](../../../../../ai-agent-rules/ai-rule-standardization-rules.md) | Skill-First architecture; no parallel rule file |
| [`scripting-language-selection-rules.md`](../../../../../ai-agent-rules/scripting-language-selection-rules.md) | Tier-1 (Python) default; documented Tier-2 borderline for the bash wrapper |
| [`skill-factory/SKILL.md`](../../../skill-factory/SKILL.md) | Skill creation protocol, companion bridge, metadata separation |

***

## 1. When to Apply

Apply before merging any reviewed pull request when a deterministic, model-backed second
opinion is wanted:

- The review verdict is posted and all blocking findings are resolved (Stage 4 complete in
  [`pr-review-workflow-guide.md`](../../../../../docs/pr-review-workflow-guide.md)).
- You want a MERGE/HOLD gate with explicit numeric thresholds rather than prose judgement.
- You want optional auto-merge that is safe by construction: fixed command, no bypass flags,
  no retry, never on HOLD/error.

Do NOT apply when:

- The PR is already merged or closed (state building still works, but the verdict is moot).
- A backend is unreachable and the decision must proceed anyway — errors are exit 2 and
  never mean approval.
- You need free-form review comments; System One models return typed decisions only.

***

## 2. Environment & Dependencies

| Requirement | Minimum | Notes |
| --- | --- | --- |
| Python | 3.10+ (3.12 recommended) | stdlib only; `classify-pr.py` declares `requires-python >= 3.10` |
| `gh` CLI | authenticated | read-only ops for state; `gh pr merge` only under `--execute` |
| `curl` | any | health probe used by `laya-server.bash` |
| Node / `npx` | any | only for the local Laya server (`laya-system-one@1.0.0`) |
| Disk | ~324 MB once | first local Laya launch downloads the model |
| Port | 8081 free | local Laya default; `--port` overridable |
| Hosted backends | optional | keys via env (`APIMASTER_API_KEY`, `MORPHLLM_KEY`, `TYPESAFE_API_KEY`) or OpenCode `auth.json` |

Runtime note: documentation uses the simplified `python3` invocation. Where `python3` resolves
to an older interpreter, resolve the mise-managed one per
[`mise-tool-management` §3.3](../../../mise-tool-management/SKILL.md#33-runtime-tool-resolution)
(e.g. `mise x python@3.12 -- python3`).

***

## 3. CLI Contract

### 3.1 Server manager — `scripts/laya-server.bash`

```bash
bash scripts/laya-server.bash <start|stop|restart|status|health> [--port N] [--host H] [--wait SECS]
```

| Argument | Default | Description |
| --- | --- | --- |
| `start` | — | Launch `npx --yes laya-system-one@1.0.0` in the background; wait for `/health` |
| `stop` | — | Stop the PID recorded in `${TMPDIR:-/tmp}/laya-system-one.<port>.pid` |
| `restart` | — | `stop` (tolerating "not running") then `start` |
| `status` / `health` | — | Print health JSON; exit 1 when not running |
| `--port` | `8081` | Listening port (8080 is often taken; never bind `0.0.0.0`) |
| `--host` | `127.0.0.1` | Loopback only |
| `--wait` | `600` | Seconds to wait for health (first run includes the model download) |

Exit codes: `0` = success/healthy · `1` = not running · `2` = usage/startup failure.
Logs and the PID file live in `${TMPDIR:-/tmp}` — the script never writes inside the repository.

### 3.2 Classifier — `scripts/classify-pr.py`

```bash
python3 scripts/classify-pr.py --repo <owner/name> --pr <N> --backend laya --json
```

| Argument | Required | Default | Description |
| --- | --- | --- | --- |
| `--repo` | no | `anushadpk/acers-web` | GitHub repository |
| `--pr` | yes | — | Pull request number |
| `--backend` | no | `laya` | `laya` \| `apimaster` \| `morphllm` \| `typesafe` \| `all` |
| `--base-url` | no | per backend | Override endpoint base |
| `--api-key` | no | env / `auth.json` | Override key (never echoed) |
| `--model` | no | per backend | Model id override |
| `--timeout` | no | `60` | Per-request timeout (s); local Laya measures ~33–45 s per call |
| `--min-confidence` | no | `0.9` | Gate: minimum `merge_decision.confidence` |
| `--max-risk` | no | `0.5` | Gate: maximum `risk.score` |
| `--max-state-chars` | no | `20000` | State size cap |
| `--diff-chars` | no | `8000` | Diff excerpt cap |
| `--body-chars` | no | `2000` | PR body cap |
| `--review-chars` | no | `500` | Per-review cap |
| `--state-file` | no | — | Offline: read a canned state JSON instead of calling `gh` |
| `--answers-file` | no | — | Offline: read canned answers instead of calling a backend |
| `--out` | no | — | Also write the verdict JSON to a file |
| `--json` / `--text` | no | `--text` | Output format (mutually exclusive) |
| `--self-test` | no | — | Run the offline fixture suite (`SELF-TEST: PASS (5/5)`) |
| `--dry-run` | no | — | Build state + payload; print without any HTTP call |
| `--execute` | no | off | Merge on `MERGE` only (see §5 and §6) |

Exit codes: `0` = MERGE · `1` = HOLD · `2` = error (backend / `gh` / parse / merge failure).

### 3.3 Backends

| Backend | Effective URL | Model | Auth |
| --- | --- | --- | --- |
| `laya` (default) | `http://127.0.0.1:8081/v1/systemone` | `laya-multilingual` | none (local) |
| `apimaster` | `https://apimaster.ai/v1/systemone` | `jev-latest` | `APIMASTER_API_KEY` / `auth.json` |
| `morphllm` | `https://api.morphllm.com/v1/systemone` | `systemone-latest` | `MORPHLLM_KEY` / `auth.json` |
| `typesafe` | `https://api.typesafe.ai/v1/systemone` | `jev-latest` | `TYPESAFE_API_KEY` |

URL construction strips a trailing `/v1` from the base and appends `/systemone`, otherwise
appends the full `/v1/systemone`. `--backend all` asks every reachable backend and requires
**unanimous** MERGE-eligible answers; a backend that is skipped (no key / server down) is not
an error, but a backend that is attempted and fails makes the whole run exit 2.

***

## 4. Protocol

1. **Bring up the local server** (once per machine session):

   ```bash
   bash scripts/laya-server.bash start
   ```

2. **Classify** (read-only):

   ```bash
   python3 scripts/classify-pr.py --repo owner/name --pr 42 --backend laya --json
   ```

   The script builds the state (`gh pr view --json …` + diff + reviews + checks), sends the
   five typed questions, and applies the gate. Inspect `reasons[]` on HOLD.

3. **Optional auto-merge** — add `--execute`:

   ```bash
   python3 scripts/classify-pr.py --repo owner/name --pr 42 --backend laya --execute --json
   ```

   Only on `MERGE`, the script runs the fixed command
   `gh pr merge 42 --repo owner/name --rebase --delete-branch` and records it in the
   `execution` block (`executed`, `command`, `result`, `merge_commit`, `timestamp_ist`).
   `result` values: `not_requested` · `merged` · `failed` · `skipped_hold` · `skipped_dry_run`.

4. **Stop the server** when done:

   ```bash
   bash scripts/laya-server.bash stop
   ```

***

## 5. Gate Semantics

```text
MERGE iff answers.merge_decision.choice == "merge"
      and answers.merge_decision.confidence >= min_confidence   (default 0.9)
      and answers.risk.score              <= max_risk           (default 0.5)
      and answers.breaking_change.decision is False
      and answers.scope_creep.decision    is False
      and answers.checks_satisfied.decision is True

HOLD  otherwise
```

`reasons[]` lists **every** failed condition with its observed value, e.g.
`merge_decision.confidence=0.62 < 0.9`, `risk.score=2.41 > 0.5`,
`breaking_change.decision=True (noul=0.87)`.

Questions asked (all five, one request): `merge_decision` (choice: merge/hold),
`risk` (score: Low/Moderate/High/Critical), `breaking_change`, `scope_creep`, and
`checks_satisfied` (noul, threshold 0.5).

### 5.1 Output contract

```json
{
  "verdict": "MERGE",
  "reasons": [],
  "backends": { "laya": { "ok": true, "model": "laya-multilingual", "answers": {} } },
  "thresholds": { "min_confidence": 0.9, "max_risk": 0.5 },
  "state_summary": { "repo": "owner/name", "pr": 0, "head_oid": "", "files": 0, "checks": 0 },
  "suggested_next_command": "gh pr merge <N> --repo <R> --rebase --delete-branch",
  "execution": { "executed": false, "command": "", "result": "not_requested", "merge_commit": "", "timestamp_ist": "" },
  "timestamp_ist": "2026-09-25 03:01 IST"
}
```

`suggested_next_command` is informational only — the script never executes it. Execution
happens solely through `--execute` on a `MERGE` verdict.

***

## 6. Prohibited Actions

- **Never merge on `HOLD` or on any error** — exit 2 is not approval.
- **Never use bypass flags** (`--admin`, `--force`, squash/merge overrides) — the merge
  method is fixed at `--rebase --delete-branch`.
- **Never retry a failed merge** — a failed `gh pr merge` is terminal for the run.
- **Never print, log, or embed API keys** — keys are read from env or `auth.json` and stay
  in-process; output contains no credentials.
- **Never bind the local server to `0.0.0.0`** — loopback only.
- **Never mutate OpenCode configuration** — `read-jsonc.py` is invoked read-only.
- **Never treat this skill as a substitute for Stage 4 verification or the user's merge
  approval policy.**

***

## 7. Acceptance Criteria

1. `bash -n scripts/laya-server.bash` exits 0.
2. `python3 -m py_compile scripts/classify-pr.py` exits 0.
3. `python3 scripts/classify-pr.py --self-test` prints `SELF-TEST: PASS (5/5)`.
4. `--dry-run --execute` prints the exact merge command, sets
   `execution.result=skipped_dry_run`, and performs no merge.
5. A real-PR decision-only run yields well-formed verdict JSON (exit 0 or 1).
6. Hosted degradation surfaces a clear exit-2 error without key echo.
7. `AGENTS.md`, `CHANGELOG.md`, `TRACEABILITY.md` present; markdown lint and the
   skill-library audits pass.

## Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release history.

## Traceability

See [`TRACEABILITY.md`](TRACEABILITY.md) for session logs and provenance.
