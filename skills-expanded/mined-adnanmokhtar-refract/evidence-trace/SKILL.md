---
name: evidence-trace
description: "Trace each requirement to its evidence (research, tickets, metric, commitment); names the UNSOURCED and MISLINKED set."
kind: skill
pack: product
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: evidence-trace

## Premise

Backlogs accumulate requirements whose origin nobody remembers. Some are evidence-backed, some are bets that were never labelled, and a few are the residue of a meeting three quarters ago. All three look identical in a ticket system, which is why they get built in the order they were entered rather than in the order they matter.

This skill makes provenance visible. It is not an accusation — an assumption is a legitimate reason to build something. An *unlabelled* assumption is not, because it is treated as fact by everyone downstream.

## Halt conditions

- **No evidence sources reachable at all** — no research, no tickets, no metrics, no commitment records. Report every requirement as unsourced and say the trace could not be performed, rather than implying they are all baseless.
- **Research exists but is unsynthesised** — raw notes are not a citable finding. Run `/synthesize-research` first; citing raw notes lets anyone quote any sentence.
- **Evidence is behind access you do not have** (a customer contract, a private research repository) — mark those requirements `UNVERIFIED — access required`, distinct from unsourced.
- **The requirement set is not enumerated** — a trace over a sample tells you nothing about the backlog.

## When to run

- Before estimation, so unsourced work is visible while it is still cheap to cut.
- When a backlog needs pruning and everything looks equally justified.
- When "who asked for this" has no answer.
- After a research synthesis, to check that existing requirements still match what the material actually said — findings change, and requirements descended from a superseded finding are the quietest kind of waste.
- Before a roadmap review, so the evidence-backed and the speculative are visibly separated.

## Procedure

### 1. Enumerate the requirements

Every requirement in scope, with its locator. Include the ones added verbally and never written down, where they can be recovered — those are the least traceable and the most likely to be unsourced.

### 2. Classify each source found

| Class | Example | Strength | What it supports |
|---|---|---|---|
| **observed behaviour** | a metric, a funnel drop-off, session data | strongest | that the problem occurs, how often |
| **support / sales record** | ticket volume with a tag, a lost-deal reason | strong | frequency, severity, who |
| **direct research** | a synthesised finding with `n of N` | strong for *why* | the mechanism and the workaround |
| **named commitment** | a contract clause, a signed renewal condition | binding | obligation, regardless of evidence |
| **regulatory / security** | a named regulation, an audit finding | binding | obligation |
| **stated preference** | survey, feature vote | weak | direction of interest only |
| **internal opinion** | a meeting, a strategy document | weakest | hypothesis |
| **none found** | — | — | — |

Each link cites the source with a locator. "Research says" is not a link; a finding number is.

### 3. Check the link, do not accept it

A citation that does not support the requirement is worse than no citation, because it stops anyone looking further. For each claimed link, verify:
- The finding actually says what the requirement claims.
- The evidence class supports the claim's strength — a survey cannot support "users will pay".
- The finding is current — it predates no significant product change that would invalidate it.
- The population matches — a finding about churned users does not automatically justify a requirement for prospects.

Report **MISLINKED** separately from unsourced. It is a different and more dangerous defect.

### 4. Report the unsourced set by name

Not a count. Names, so the conversation can happen per item. Then split them:
- **candidate assumption** — plausible, worth labelling and testing. Hand to `assumption-ledger`.
- **candidate cut** — nobody can articulate why it is there. Propose removal.
- **infrastructural / prerequisite** — no user evidence expected; justified by a technical or compliance class instead. Legitimate, and must state which class.

### 5. Report

```
## evidence-trace — <requirement set> — <date>

Requirements enumerated: <n>

| # | Requirement | Evidence class | Source (locator) | Link verified | Currency | Verdict |
|---|-------------|----------------|------------------|---------------|----------|---------|

Totals: evidence-backed <n> · binding (commitment/regulatory) <n> · labelled assumption <n> ·
        UNSOURCED <n> · MISLINKED <n> · UNVERIFIED (access) <n>

Unsourced, by name:
| # | Requirement | Split | Proposed action |
|   |             | candidate assumption / candidate cut / infrastructural | |

Mislinked, by name:
| # | Requirement | Claimed source | What the source actually supports |

Superseded: requirements descended from a finding that a later synthesis changed: <n> (named)
```

## Inputs

- The enumerated requirement set with locators.
- `ai/product/research/` synthesised findings.
- Support-ticket volumes, product metrics, commitment records where reachable.
- Prior syntheses, to detect superseded findings.

## Outputs

- The trace table, into `/audit-requirements`'s traceability line.
- The unsourced set, split, into `assumption-ledger` and into `@scope-arbiter`'s evidence column.
- The mislinked set, which usually needs a conversation rather than a ticket.

## False positives / gotchas

- **Treating unsourced as illegitimate.** Infrastructural, security, and compliance work needs no user evidence — it needs its justification class named.
- **Accepting a citation without reading it.** The most common defect this skill finds is a real finding cited for a claim it does not support.
- **Missing currency.** A finding from before a pivot is a historical note, and requirements descended from it are the quietest waste in the backlog.
- **Population mismatch.** Evidence about one segment justifying a requirement for another.
- **Counting a loud account as evidence of prevalence.** It is evidence of severity for one customer, which is a different claim and may still be sufficient — say which.
- **Reporting counts rather than names.** A count cannot be acted on.
- **Tracing a sample.** Enumerate or do not run.

## Related

### Skills
- `assumption-ledger` — receives the unsourced set and ranks it.
- `acceptance-criteria-check` — whether a requirement can be verified; this skill is whether it should exist.

### Agents
- `@user-research-synthesizer` — produces the findings this skill traces to.
- `@requirements-reviewer` — consumes the traceability line.
- `@scope-arbiter` — consumes the evidence column.

### Commands
- `/audit-requirements`, `/synthesize-research`, `/frame-problem`

### Patterns
- `ai/patterns/research-synthesis.md`, `ai/patterns/problem-framing.md`
