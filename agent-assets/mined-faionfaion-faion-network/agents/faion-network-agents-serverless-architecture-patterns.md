# Serverless Architecture Patterns

## Summary

**One-sentence:** Routes a workload to the right serverless composition (API Gateway+Lambda, EventBridge, Step Functions, SQS fan-out) and emits a pattern ADR with cost + cold-start trade-offs.

**One-paragraph:** Routes a workload to the right serverless composition (API Gateway+Lambda, EventBridge, Step Functions, SQS fan-out) and emits a pattern ADR with cost + cold-start trade-offs. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Workload is event-driven, bursty, or has variable traffic and fits FaaS execution limits.
- Operational team capacity is small; managed runtime preferred over self-hosted.
- Cost model favours pay-per-invocation over reserved capacity (long idle / spiky).
- Output produces `decision-record` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Workload is event-driven, bursty, or has variable traffic and fits FaaS execution limits.
- Operational team capacity is small; managed runtime preferred over self-hosted.
- Cost model favours pay-per-invocation over reserved capacity (long idle / spiky).

## Skip If (ANY kills it)

- Workload requires sustained high RPS where reserved compute is cheaper per request.
- Long-running (> 15min on AWS) or stateful in-memory needs — choose containers / VMs.
- Sub-50ms p99 latency requirement where cold start is unacceptable.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workload profile (RPS, burst factor, idle fraction) | data | ops |
| Latency budget (p50/p95/p99) | table | SRE |
| Execution-time + memory profile | data | team |
| Cloud provider + region | field | ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[serverless-foundations]] | Foundational FaaS concepts. |
| [[serverless-cold-start-optimization]] | Cold-start mitigations apply when chosen. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 7-step end-to-end procedure with input/action/output per step | 900 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-workload` | haiku | Lookup invocation pattern → candidate composition. |
| `estimate-cost` | sonnet | Bounded calc: RPS × duration × memory + downstream services. |
| `draft-adr` | sonnet | Compose ADR with rejected alternatives + cost + latency trade-offs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/serverless-pattern-adr.md.j2` | ADR skeleton for serverless pattern selection. |
| `templates/serverless-pattern-adr.md` | ADR skeleton for serverless pattern selection. Generated from `templates/serverless-pattern-adr.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/pattern-fit-matrix.md.j2` | Matrix mapping workload signals to pattern fit. |
| `templates/pattern-fit-matrix.md` | Matrix mapping workload signals to pattern fit. Generated from `templates/pattern-fit-matrix.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in artefact for sanity-checking the schema. |
| `templates/_smoke-test.md` | Minimum viable filled-in artefact for sanity-checking the schema. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-serverless-architecture-patterns.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[serverless-foundations]]
- [[serverless-cold-start-optimization]]
- [[serverless-cost-optimization]]
- [[serverless-iac-and-templates]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is the workload pattern compatible with serverless prerequisites?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
