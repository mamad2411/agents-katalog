---
name: specialist-dispatch
description: >
  Use when the operator wants specialised build/review/proof agents, says agents
  are not specialised enough, asks for subagent prompts, multi-axis review,
  one-job agents, or needs work split into bounded roles before building.
  Produces compact specialist briefs with one job per agent, allowed scope,
  forbidden actions, evidence outputs, and stop rules. This is a dispatch/prompt
  skill, not a broad builder.
---

# Specialist Dispatch

## Overview

Create one-job specialist briefs. The lead remains orchestrator and integrator; no specialist receives more than one responsibility.

## Required Inputs

- Repo or workspace.
- Source artifact: issue, plan, diagnosis packet, diff, PR, or explicit work description.
- Current route/worktree/edit constraints when relevant.
- Whether specialists may mutate or must stay read-only.
- Desired closeout: diagnosis, plan, implementation, patch/fix review, runtime proof, PR closeout, or merge/deploy proof.

If source truth or hardening gates are missing, route through `pre-code-hardening` or `diagnose` before dispatching builders.

## Specialist Roles

Use only roles that are needed:

- `source-truth-mapper`: read current source/docs/runtime state and map exact files/symbols. Read-only.
- `domain-srp-reviewer`: find domain boundary, SRP, refactor, and wrong-owner opportunities. Read-only.
- `table-ownership-auditor`: prove DB table/write ownership, tenant/scope, SQL/schema risks. Read-only unless explicitly approved.
- `live-proof-engineer`: identify and/or run safe runtime, schema, browser, API, worker, or canary proof. No unsafe writes.
- `test-ratchet-engineer`: design failing test, recurrence guard, and ratchet coverage. May code only if builder authority exists.
- `builder`: implement the approved build packet only. No scope expansion.
- `patch-or-fix-reviewer`: run `patch-or-fix` after implementation.
- `prove-it-closer`: run `prove-it` and proof-chain closeout before done/ready claims.
- `pr-closer`: settle PR checks, review threads, wrapper requirements, and merge/deployed proof where authorized.
- `hook-hygiene-reviewer`: inspect hook config or hook changes without adding context-heavy hooks.

## Brief Rules

- One role, one job, one output.
- Include exact repo/worktree/branch/issue/PR coordinates when known.
- Include allowed files, symbols, or domains; include forbidden files/actions.
- Include evidence required and output schema.
- Include stop rules before mutation, unsafe env access, production-looking targets, or scope expansion.
- Do not send specialists to explore raw source without a compact source bundle when the lead can pre-read.
- If using actual subagent tools is unavailable, output copy-paste prompts instead.

## Brief Template

```markdown
## <role>

**Job:** <one responsibility>
**Context:** <issue/plan/diff/packet and current coordinates>
**Allowed scope:** <paths/symbols/domains>
**Forbidden:** <actions/paths/assumptions>
**Must reuse skills:** <deep-think/diagnose/patch-or-fix/prove-it/etc. if applicable>
**Evidence required:** <file lines, commands, runtime proof, schema proof>
**Output:** <specific schema or sections>
**Stop rule:** <when to stop and report blocked>
```

End by naming which briefs are ready to send and which are blocked by missing source truth or authorization.
