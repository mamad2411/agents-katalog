---
name: design-governance
description: Assess implementation, integration, and contract tasks against the merged AI-Kit design policy. Use before authoritative QA when architecture boundaries, public contracts, generated artifacts, dependency direction, or legacy behavior may change. Produces evidence only; it never advances lifecycle state.
version: 0.1.0
tier: core
stack: [any]
owner: architect
gates: [G8, G9]
related: [.ai/policies/design-policy.json, architecture-decisions, system-designer, contract-testing]
---

# Skill: design-governance

## Purpose

Turn architecture judgment into a reviewable assessment that the AI-Kit
control plane can validate deterministically. The assessor reports facts and
rationales; only `ai-kit qa run` can apply the G8 gate.

## Procedure

1. Run `ai-kit design rules --task <TASK>` and record the returned normalized
   policy hash. Never assess against a remembered or copied policy.
2. Inspect the task contract, declared file scope, registered context, contract
   refs, and the actual diff in the assigned worktree.
3. For every applicable rule, emit one result: `pass`, `fail`, or
   `not-applicable`. A `SHOULD` result always includes a concrete rationale.
   Evidence paths must point to files, commands, tests, diffs, or decision
   records that another actor can inspect.
4. Submit schema-version-1 JSON with
   `ai-kit design assess <TASK> --input <FILE> --actor <ROLE>
   [--agent-id <ID>]`.
5. Run `ai-kit design validate <TASK>` to diagnose missing, stale, or failing
   evidence. Do not call lifecycle transitions from this skill.
6. If a hard rule cannot be followed, request an exception. `MUST` exceptions
   require a reviewer independent of the executor. `FORBIDDEN` exceptions also
   require explicit user confirmation and a durable decision record.

## Artifact Architecture procedure

When the task changes architecture facts or their presentation, apply this
pipeline in order:

1. **Observe** canonical config, source/imports, assessments, and decisions.
2. **Classify** every module, dependency, or relationship as `observed`,
   `inferred`, or `proposed`.
3. **Normalize** it to stable IDs and explicit source references, confidence,
   rationale, and proposer where required.
4. **Validate** the complete bundle with `ai-kit artifact validate`. Treat this
   as projection validation only, never QA or lifecycle authority.
5. **Publish** only through `ai-kit artifact generate`. Keep
   `.ai-work/artifacts/project/manifest.json` as the manifest-last commit marker.
6. **Render** by consuming the published bundle. Allow filters, layout, and
   grouping; forbid source discovery or architecture inference in Visualizer.

Keep the artifact bundle derived from authoritative workflow, configuration,
contract, evidence, Git, and discovery sources. Keep archival events outside
the bundle; use `events.json` only as a bounded replay projection. Exclude
proposed relationships from impact, ownership, DAG, QA, and dependency gates.
Promote them only by updating an authoritative config/source/decision and
regenerating.

## Assessment shape

```json
{
  "schema_version": 1,
  "task": "T1",
  "policy_hash": "sha256...",
  "rules": [
    {
      "rule_id": "DG-BOUNDARY-TESTS",
      "result": "pass",
      "rationale": "Producer and consumer conformance tests cover v1.",
      "evidence": ["tests/contracts/order-v1.test.ts"]
    }
  ]
}
```

## Guardrails

- Treat `domain/api-contract/backend/frontend` as reference vocabulary, not a
  required directory layout. Project identity and registered contexts own the
  actual structure.
- Never invent endpoint/type comparison capability. Semantic contract claims
  require a configured executable verifier.
- Never weaken a core rule silently. Project overrides name the rule and carry
  a rationale; exceptions remain task-scoped evidence.
- Do not create QA or review verdicts. The assessment is evidence input only.
- Do not let AI, CLI subcommands, Visualizer, or legacy adapters independently
  synthesize a competing architecture truth. `artifact generate` is the only
  project-bundle generator; legacy JSON is a projection from its output.

## Output

Canonical design assessment and optional exception artifacts under
`.ai-work/evidence/design/`, consumed by `ai-kit design validate`, `qa run`,
`review apply`, and `delivery attest`.
