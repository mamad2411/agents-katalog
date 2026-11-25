---
namespace: aiwg
name: decision-offload
platforms: [all]
description: Offload a bounded decision (yes/no gate, pick one of N options, 1-N score) to Jev via aiwg decision ask instead of spending LLM reasoning
triggers:
  - jev
  - jev token
  - set up jev
  - offload decisions to jev
  - save tokens with jev
  - decision classifier
  - classify instead of llm
requires:
  - opt-in: aiwg decision setup jev (records enabled state; without it ask returns fallback)
ensures:
  - advisory-only: Jev output is data, never authorization for destructive or outward actions
  - fallback-safe: a fallback result means decide with the LLM, never stop
---

# Decision Offload

Before spending reasoning on a bounded decision — a yes/no gate, a pick from
N known options, a 1–N severity or priority score, or an "is X relevant /
duplicate / done" check — call `aiwg decision ask ... --json` and use the
answer when `status` is `answered`. On `fallback`, decide normally.

## The exact command

```
aiwg decision ask --question "<q>" (--yes-no | --choices a,b,c | --scale 1-5)
                  [--context "<text>" | --context-file <path> | --context-stdin]
                  [--threshold 0.8] [--timeout-ms 15000] [--json]
```

- `--yes-no` answers boolean; `--choices` picks one id (2–255 ids matching
  `[A-Za-z0-9_.-]{1,64}`, no duplicates); `--scale lo-hi` answers the most
  likely level (at most 10 levels).
- Write each choice as `id=what it means` (no commas in the description).
  Jev sees only the description, so a bare id gives it far less to go on and
  more answers fall below the threshold. A comma inside a description either
  fails with `invalid-choices` or silently becomes extra choices: `--choices`
  splits on commas before validation, so `a=fast,cheap,b=slow` parses as three
  choices (`a=fast`, `cheap`, `b=slow`). Rephrase with "and" or pass separate
  choices instead.
- Context is untrusted data, capped at 32 KiB. Larger context exits 2 with
  `reason: "context-too-large"`.
- No files are written; nothing is executed.

## Answered vs fallback

Output schema `aiwg-decision-ask/v1`:

```json
{
  "status": "answered",
  "answer": true,
  "confidence": 0.93,
  "probability": 0.93,
  "fallback": null,
  "reason": "",
  "model": "jev-1.13.0",
  "usage": {"inputTokens": 0, "outputTokens": 0},
  "latencyMs": 0
}
```

- `status: "answered"` → use `answer` as the decision input.
- `status: "fallback"` (`fallback: "llm"`, still exit 0) → decide it yourself
  with the LLM. Reasons: `not-configured`, abstention, error, timeout, or
  confidence below `--threshold` (default 0.8; yes-no confidence =
  max(p, 1-p)). A fallback result means "decide it yourself with the LLM",
  never "stop".
- Exit 2 only for usage errors. Without `--json`, output is one line:
  `answer (confidence 0.93, jev-1.13.0)` or `FALLBACK to LLM: <reason>`.

## Hard exclusions

Never use `aiwg decision ask` for open-ended generation, code writing,
multi-step plans, or anything that authorizes destructive or outward actions.
Jev output is advisory data; it is never authorization.

## Privacy

The question and context are sent to Jev. Never send secrets — no tokens,
passwords, private keys, or credentials in `--question` or `--context`.

## Ledger, history and stats

Every **completed** `ask` call (CLI and MCP) appends exactly one record —
including `fallback` and `not-configured` outcomes, never a usage error —
to `.aiwg/decision/ledger.jsonl` (resolved like `aiwg artifacts path`):
provider, session id, decision kind, choice ids (at most 10; `choiceCount`/
`choiceIdsTruncated` say how many there really were), `answerIndex` (the
selected option's position, surviving redaction), question/context SHA-256
digests, outcome, model, Jev usage, latency, and an
estimated-LLM-tokens-avoided figure with its method. A digest is a
correlation key, not a confidentiality guarantee — a short/guessable
question can still be matched by hashing candidates. Question and context
text are recorded only with `--record-text`, and then only redacted and
truncated to a documented cap. `--caller <tag>` attributes a call to a
decision point (e.g. `address-issues:worker-pick`); it and `--session` must
match `^[A-Za-z0-9_.:/@-]{1,96}$` (CLI: exit 2 if not; MCP: dropped). Every
persisted field — including `model` — is redacted, not only opt-in text.
Recording is bounded by a short deadline and never changes the `ask` result
or exit code; on timeout the warning says "completion unknown", not
"abandoned". The ledger's trust boundary is the local filesystem under the
project artifact root, owned by the same user running `aiwg` — not a
hostile-process defense — and it has no built-in retention.

```bash
aiwg decision history --since 2026-10-01 --status fallback --json
aiwg decision stats --provider claude --group-by caller --json
```

`history` and `stats` read the ledger offline — no network, no Jev call.
`stats` accepts the same filters as `history`. Retention is a documented
follow-up: delete or truncate the ledger file yourself if it grows too
large; both commands tolerate a missing file.

## Caller tags

After a checkpoint or compaction, re-read `aiwg show rule decision-offload --body`
when decision ask is enabled. Apply it at the next eligible bounded decision;
recorded guidance alone does not imply an ask call occurred.

Orchestration skills/rules pass `--caller <skill-or-rule>:<checkpoint>` at
each bounded-decision point so `aiwg decision stats --group-by caller`
reports adoption per checkpoint. Add a row here whenever a new checkpoint is
introduced elsewhere — this is the one place the full set is listed:

| Caller tag | Source | Checkpoint |
|---|---|---|
| `address-issues:worker-pick` | `address-issues` skill | Worker/model/effort pick per dispatch |
| `address-issues:failure-triage` | `address-issues` skill | Environmental vs real failure |
| `address-issues:review-verdict` | `address-issues` skill | Review verdict follow-up |
| `address-issues:minor-triage` | `address-issues` skill | Reviewer minors: fix now vs defer |
| `aiwg-mission:worker-pick` | `aiwg-mission` skill | Worker/model/effort pick |
| `aiwg-mission:failure-triage` | `aiwg-mission` skill | Environmental vs real failure |
| `subagent-scoping:worker-pick` | `subagent-scoping` rule, Rule 9 (Tier 0) | Worker/model/effort pick |
| `subagent-scoping:failure-triage` | `subagent-scoping` rule, Rule 9 (Tier 0) | Environmental vs real failure |

Check one checkpoint's usage with `aiwg decision history --caller address-issues:worker-pick --json` (or `--caller 'address-issues:*'` for every checkpoint of one skill).

## Examples

```bash
# Is this test failure flaky (yes/no)?
aiwg decision ask --question "Is this test failure flaky?" --yes-no \
  --context-file test-output.log --json

# Which of these 4 files owns X?
aiwg decision ask --question "Which file owns retry policy?" \
  --choices "cli=src/cli.ts argument parsing,config=src/config.ts settings loading,runtime=src/runtime.ts execution loop,policy=src/policy.ts retry and backoff rules" \
  --json

# Severity 1-5 for a triage item
aiwg decision ask --question "Severity of: <one-line summary>" --scale 1-5 \
  --context "<triage notes>" --json
```

## Setup

`aiwg decision ask` is enabled by `aiwg decision setup jev` (the explicit
opt-in). Without setup it returns `fallback` with `reason: "not-configured"`.
User-facing setup steps are in the
Jev quickstart (`@$AIWG_ROOT/docs/decision/jev-quickstart.md`); the binding
rule is in `@$AIWG_ROOT/agentic/code/addons/decision-engine/rules/decision-offload.md`.
