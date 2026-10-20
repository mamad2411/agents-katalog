---
name: design-page-contract
description: Virtual lead-orchestrated gate for post-fan-out behavior contract audit (#1387). Not a spawned subagent — the verdict is produced by `.claude/scripts/lib/behavior_contract_auditor.py` invoked by state-11c lead, then consumed via `.claude/scripts/verify-state-11c-behavior-audit.py` at state-registry:bootstrap.11c.
model: opus
tools: []
disallowedTools:
  - Edit
  - Write
  - Bash
  - Read
  - Glob
  - Grep
  - Agent
maxTurns: 0
---

# Design Page Contract — Virtual Lead-Orchestrated Gate

**This is NOT a spawned subagent.** The frontmatter `tools: []` and `maxTurns: 0` make spawning a no-op. This file exists to satisfy the `post-completion-respawn-doc-required` template-coherence rule for entries in `.claude/patterns/agent-registry.json` `hard_gates` that declare `pass_lead_orchestrated` in `allow_predicates`.

## Role

Post-fan-out behavior-contract audit for scaffold-pages output (#1387). Sibling of `design-critic` and `design-consistency-checker`:

- All three are **post-generation gates** consuming scaffold-pages output.
- All three produce a verdict consumed by state-11c VERIFY.
- All three share `allow_predicates` enforced by the `design-agents-hard-gate-parity` linter (`.claude/patterns/template-coherence-rules.json`).

## Executor

Lead-orchestrated Python invocation:

```bash
python3 .claude/scripts/lib/behavior_contract_auditor.py
```

The auditor:
1. Reads `.runs/scaffold-pages-contracts.json` (pre-fan-out structured contract) via `unstamped_items` from `verify_helpers.py`.
2. For each tagged contract entry, runs Layer 4a static AST + grep audit against the page's `.tsx` files.
3. Writes `.runs/behavior-implementation-audit.json` (verdict consumed at state-11c VERIFY) and `.runs/behavior-verifier-static-stubs.json` (runtime check annotations consumed by behavior-verifier B7 in `/verify`).

## Verdict Schema

The audit artifact `.runs/behavior-implementation-audit.json` carries:
- `provenance: "lead-orchestrated"`
- `lead_attestation: true`
- `uncovered_count: 0` ⇒ verdict pass (state-11c VERIFY blocks when > 0)
- `runtime_check_signaled: [...]` — entries for behavior-verifier B7 to validate at /verify time

## When Spawning Is Forbidden

The frontmatter forbids ALL tools. If a hook or skill attempts to spawn `design-page-contract` via the Agent tool, the spawn is structurally inert (no-op). The verdict MUST come from the lead-orchestrated Python invocation above; any other path is an audit-bypass and should be treated as a regression.

## Predicate Rationale

Allowed verdict predicates (mirrors `design-critic`):
- `pass_clean`, `pass_after_fixes`, `pass_self_pass_or_fail`, `validated_fallback`, `aggregate_ok`, `legacy_pass_no_recovery` — standard pass-class.
- `pass_lead_synthesized` — lead writes a coverage-provider trace pointing at the audit artifact.
- `pass_lead_orchestrated` — lead-orchestrated re-spawn (post-completion identity supplied via `--source-run-id` / `--source-skill`).

## Post-completion re-spawn

This gate is **lead-orchestrated by construction** — there is no spawned-subagent execution path. The `pass_lead_orchestrated` predicate covers re-runs of the audit under post-completion conditions (every `.runs/*-context.json` has `completed:true`, so `resolve_active_identity` returns empty).

Re-spawn procedure for a lead re-running the audit retrospectively (e.g., during `/resolve` or `/observe` reviewing a prior bootstrap):

```bash
# 1. Identify the source bootstrap run from the spawn-log or context file.
SOURCE_RUN_ID=$(python3 -c "
import json
ctx = json.load(open('.runs/bootstrap-context.json'))
print(ctx.get('run_id', ''))
")
SOURCE_SKILL=bootstrap

# 2. Re-run the auditor (re-derives from current experiment.yaml + .tsx).
python3 .claude/scripts/lib/behavior_contract_auditor.py --skill bootstrap

# 3. The auditor writes .runs/behavior-implementation-audit.json via
#    write-gate-artifact.sh. When invoked post-completion, the canonical
#    writer requires explicit source flags; the auditor's invocation of
#    write-gate-artifact.sh propagates them via the --skill flag and the
#    source-identity validator. The resulting artifact carries
#    provenance=lead-orchestrated + lead_attestation=true, satisfying the
#    pass_lead_orchestrated predicate.

# 4. State-11c VERIFY (.claude/scripts/verify-state-11c-behavior-audit.py)
#    reads the artifact and asserts run_id matches bootstrap-context.json.
#    Drift between audit.run_id and the active context's run_id BLOCKS.
```

**Expected verdict**: when the auditor's `uncovered_count == 0`, the audit artifact is accepted by `verify-state-11c-behavior-audit.py`. When `uncovered_count > 0`, the gate blocks and the lead must EITHER fix the uncovered pages (via `/resolve` or `/change`) OR justify suppression in the audit's `runtime_check_signaled[]` for behavior-verifier B7 to validate at `/verify` time.

**Forbidden paths**: `recovery_forbidden` (high-risk fixers) and `lead_orchestrated_forbidden` (security-* probes) do NOT apply to this gate — the audit is deterministic Python with no side-effects beyond the artifact write, and it does not interact with live endpoints.
