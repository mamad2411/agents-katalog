---
name: spike
description: Use this skill when evaluating new tech, prototyping approaches, researching unknowns, or building a proof-of-concept — for a time-boxed exploration with a go/no-go writeup, single-pass with optional reviewer and no RALF (a spike is exploration, not convergence). Not for development (use /develop) or decisions already made.
context: fork
argument-hint: "<research question> [--time-cap <minutes>] [--poc]"
---

# /spike — Time-Boxed Exploration

Single-pass research workflow producing a SPIKE-REPORT with a go/no-go/needs-more-info recommendation. Time-cap is the primary discipline. Optional `--poc` flag produces a minimal proof-of-concept code alongside the writeup.

## When to use

- "Can we use gRPC instead of REST?"
- "Best way to implement real-time sync?"
- "Is this library production-ready?"
- "Research: what's our path to multi-region deployment?"

## Not for

- Decisions already made → just `/plan` then `/develop`
- Open-ended exploration with no question → `/spike` requires a stated question
- Convergence on a binary success signal → `/ralph` (spike is exploration, not iteration)

## Invocation

```
/spike "Can we use gRPC instead of REST?" --time-cap 120
/spike "Best way to implement real-time sync" --poc
/spike "Is Postgres pg_vector production-ready for our scale?" --time-cap 90
```

## Arguments

| Flag | Default | Effect |
|---|---|---|
| `<question>` (positional) | required | Research question or evaluation goal |
| `--time-cap <min>` | 180 | Wall-time cap for the spike |
| `--poc` | off | Produce minimal proof-of-concept code in `<repo>/spike-poc-<run-id>/` |

## Output

- `<repo>/.ai-skills-memory/spikes/<run-id>/SPIKE-REPORT.md` — findings, pro/con analysis, recommendation
- (optional) `<repo>/spike-poc-<run-id>/` — proof-of-concept code if `--poc`
- Memory write: L4 research record for future reference

## Agent roster

| Agent | Model | Effort | Tools | Role |
|---|---|---|---|---|
| `subject-matter-expert` (role-appropriate, chosen by Lead) | inherit | high | Read, Grep, Glob, Bash, (Write+Edit if `--poc`) | Research + writeup + POC |
| (optional) `technical-reviewer` | inherit | medium | Read, Grep, Glob | Stress-test findings, identify gaps |

The Lead picks the SME role based on the question domain (e.g., `db-engineer` for schema questions, `ml-engineer` for ML questions, `solution-architect` for architecture).

## Pipeline

```
┌─ Lead chooses SME role based on question domain
│
├─ SME researcher:
│  - Research question exhaustively (within time-cap)
│  - Gather evidence (docs, benchmarks, examples)
│  - Build POC if --poc flag set
│  - Estimate effort if go/no-go decision involved
│  → SPIKE-REPORT.md with go/no-go/needs-more-info recommendation
│
├─ (Optional) technical-reviewer validates findings:
│  └─ Stress-test assumptions, identify gaps in evidence
│     → review.md
│
└─ Memory write: L4 research record
   Report: go/no-go + next steps
```

No RALF — spike is exploration, not convergence.

## Decision lens & evidence requirements

- **SME research + evidence gathering:** every quantitative claim in the SPIKE-REPORT cites a source from `references/evidence-hierarchy.md` (level 1–5; level 6–7 requires "low confidence" caveat).
- **SME recommendation (the go/no-go/needs-more-info writeup):** apply Cynefin classification + One-Way/Two-Way Doors lens per `references/decision-frameworks.md`. Recommendation is one of `go-two-way`, `go-one-way`, or `needs more spike before commit`, with each option classified on (Cynefin domain, reversibility, ICE/RICE relative score, confidence level).

## G7 spawn payloads

SME and reviewer spawns use structured G7 payloads per `plugin/schemas/spawn-payload.schema.json`. Returns conform to `plugin/schemas/return-contract.schema.json`.

## Eval rubric

Pointer: `plugin/eval/judge-rubrics/spike.md` (B10).

Dimensions:
1. **Question clarity** — spike clearly answers the stated question
2. **Evidence quality** — findings backed by data (not opinion)
3. **Completeness** — considered trade-offs and alternatives
4. **Feasibility assessment** — if go/no-go, effort estimate is realistic
5. **Actionability** — next steps clear (prototype? deep dive? abandon?)

Pass: avg ≥ 4.0, no dimension < 3.

## Memory writes

| Layer | When | Shape |
|---|---|---|
| L4 | After complete | `.ai-skills-memory/spikes/<run-id>/report.md` — full findings |
| L4 (committed) | **Always ask user explicitly after report**, never auto-write | `.ai-skills-memory/.committed/decisions/<date>-<question>.md` — recorded decision |

**Hard rule on committed decisions:** never auto-create `.committed/decisions/` files. `.committed/` goes to git and the user may want to reword the decision before committing. The skill ALWAYS asks before writing to `.committed/decisions/`. The `pre-tool-use-committed-write.py` hook enforces the allowlist on these paths regardless.

## Failure modes

- **Time cap hit mid-research:** SME pauses at time-cap; produces partial report with explicit `[INVESTIGATION INCOMPLETE]` marker and "more investigation needed" section listing specific data gaps
- **Findings inconclusive:** report states inconclusive with specific data gaps; recommend deeper spike or prototype
- **POC fails to compile/run:** report failure as a finding; do NOT block the spike completing — POC failure is itself a data point for go/no-go

## Observability events

- `workflow_start` — spike + question
- `time_cap_warning` — at 80% of time-cap
- `workflow_end` — `COMPLETE` with go/no-go OR `INCOMPLETE` if time-cap hit

## Integration

- **Orchestrator**: `feature-design-lead` (only agent with `tools: Task`)
- **Schemas**: `plugin/schemas/spawn-payload.schema.json`, `plugin/schemas/return-contract.schema.json`
- **Companions**: `/context-load` (per-role context for SME), `/subagent-spawn` (G7 payload)
- **Rules**: `subagent-isolation` (G7 + bounded recursion), `untrusted-content-wrapping` (G1 wrap on subagent returns + reference docs read), `memory-discipline` (committed writes always-ask + allowlist)
- **Hooks**: `pre-tool-use-committed-write.py` (enforces `.committed/decisions/` allowlist), `tool-output-normalize.py` (G2 on bash output)
