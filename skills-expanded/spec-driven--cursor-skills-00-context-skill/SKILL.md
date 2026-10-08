---
name: 00-context
description: >
  Analyzes any existing codebase, documentation, research paper, or prior work the user
  provides. Produces a context brief that pre-fills Stage 01 (requirements interview).
  Runs paper-analyst and repo-researcher agents in parallel when applicable, cross-references
  findings, and surfaces contradictions/ambiguities/decisions to the user. When the project
  belongs to a multi-repo organization, scans sibling repos to discover integration patterns,
  API contracts, deployment conventions, and shared dependencies that constrain this project's
  design. Optional stage — skipped when the user has no existing artifacts.
---

# 00 — Context Gathering

Analyze existing artifacts and produce `docs/context-brief.md` for downstream skills.

**Preamble:** [pipeline-preamble.md](../pipeline-preamble.md)
**Cross-cutting:** [considerations.md](../considerations.md), [connectivity-gates.md](../connectivity-gates.md)
**State:** [workflow-state-reference.md](../workflow-state-reference.md) · [workflow-state-manager](../../agents/workflow-state-manager.md)
**Detail:** [reference.md](reference.md)

## When to use

| Scenario | Action |
|----------|--------|
| Before **01-requirements** with existing code, paper, or docs | Run full workflow |
| Standalone deep-dive | Run without planning |
| No existing artifacts | Set status `skipped` in workflow-state |

## Prerequisites

| Input | Required | Notes |
|-------|----------|-------|
| Input type | Yes | paper, repo, docs, or combination |
| Paper / repo / docs paths | Per type | See reference §Inputs |
| Org directory | No | Enables Phase 1B ecosystem scan |
| Output directory | No | Default `docs/` |

Invoke **workflow-state-manager** `read_context` first; `update` after each phase. Do not edit
`workflow-state.yaml` directly.

## Workflow summary

```
Phase 1A ──► Run agents (paper-analyst, repo-researcher, doc-scanner) in parallel
    │
Phase 1B ──► Ecosystem scan (sibling repos) — skip if standalone
    │
Phase 1C ──► Template classification → template-registry + deployment-catalog
    │
Phase 2  ──► Cross-reference (7 scans: contradiction → ecosystem alignment)
    │
Phase 3  ──► Surface issues via AskQuestion; Resolution Log + ADRs
    │
Phase 4  ──► Write context-brief.md
    │
Phase 5  ──► Summary → ready for 01-requirements
```

| Phase | Blocking? | Output |
|-------|-----------|--------|
| 1A Analysis agents | — | Agent reports in state |
| 1B Ecosystem scan | User repo selection + hard constraints | Integration map, constraints |
| 1C Template classification | User confirms template + service name | `workflow-state.yaml` §template |
| 2 Cross-reference | — | Issue counts |
| 3 Surface issues | Blocking issues must resolve | Resolution Log, ADRs |
| 4 Context brief | — | `docs/context-brief.md` |
| 5 Summary | — | User report |

Step-by-step prompts, schemas, and AskQuestion templates: [reference.md](reference.md).

## Connectivity (stage 00)

In `docs/context-brief.md`, document **multi-app topology**: browser-facing deployables, API origins,
CORS/BFF plans. Flag **browser integration risk** when static UI and APIs are on different hosts.

## Delta mode

From **16-evolve**: run only for new external context; merge into existing brief; tag `evolve_cycle_id`
and `feature_ids`. See [reference.md §Delta](reference.md#delta--feature-addition-mode).

## Key rules

1. **Evidence-based** — every claim traces to an agent report; never fabricate.
2. **Citations** — `[Paper §X]`, `[Repo: path:L#]`, `[Docs: path]`.
3. **No silent resolution** — blocking issues require user input (considerations §Uncertainty).
4. **Commit-as-you-go** — commit artifacts before next stage or blocking AskQuestion.
5. **Resolution traceability** — numbered R1, R2, … referenced downstream and in ADRs.

## Output rules

| Artifact | Path |
|----------|------|
| Context brief | `docs/context-brief.md` |
| ADRs (from resolved decisions) | `docs/adr/` |
| State | `workflow-state.yaml` §`stages.00-context`, §`template` |

Full brief section list and summary template: [reference.md §Phase 4–5](reference.md#phase-4--context-brief).
