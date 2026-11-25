---
name: state-audit
description: Audit an existing software feature or surface by deriving an expected, evidence-sourced condition inventory and comparing it with code, tests, designs, telemetry, incidents, support history, requirements, and domain rules. Use to find undesigned or unimplemented lifecycle states, failures, interruptions, and surfaces with file-line evidence and risk-aware prioritisation. Do not call code-only inference independent evidence or turn the output into a bug list.
---

# State Audit

Compare an expected condition inventory with observed product handling. Separate intended behavior evidence from implementation evidence.

## Procedure

1. Determine the feature or surface. If the user named a directory or scope, proceed. Otherwise show the detected root and ask for a narrower path or confirmation.
2. Read `STATEFUL.md` and existing maps without overwriting confirmed decisions.
3. Inventory available evidence:
   - requirements, policies, research, domain rules;
   - analytics, incidents, support history;
   - designs and prototypes;
   - code, tests, schedulers, enums, data models, dependencies.
4. Derive the expected inventory first from non-implementation evidence. Use code for structural clues only when necessary and mark those records as hypotheses; code cannot prove what ought to exist.
5. Build the four lenses: lifecycle states, failures with cause, interruption contexts, and surfaces. Record evidence and confidence per condition.
6. Inspect actual handling in routes, components, reducers, controllers, jobs, validation, errors, loading/empty branches, tests, stories, templates, notifications, data models, and infrastructure. Cite `file:line`.
7. Compare expected and observed behavior. Distinguish:
   - undesigned;
   - designed but unimplemented;
   - implemented without deliberate design;
   - implemented but unverified;
   - evidence conflict requiring a decision.
8. Score likelihood, impact, and confidence. Rank by risk, not likelihood alone.
9. For the top 3–5 gaps, state current behavior, evidence, design/engineering implication, layers, owner needed, and the next acceptance criterion—not a prescriptive fix unless the user asks.
10. Update the `## Audit` section of `STATEFUL.md`. Preserve evidence sources and known unknowns.
11. Ask whether to produce or update a v0.1 JSON mirror. New gap records begin at `status: discovered`; do not invent scope. Preserve `scenarios` and typed `relationships`, and keep `metadata.maturity: working` until the handoff gate passes.

## Output

```text
## Evidence consulted
| Type | Reference | What it establishes |

## Expected condition inventory
<four lenses with evidence and confidence>

## Observed handling
| Condition | Status | Evidence | Current behavior |

## Gaps
| Condition | Gap type | Likelihood | Impact | Confidence | Evidence | Implication |

## Top gaps
1. <risk-aware narrative with file:line evidence>

## Known unknowns
- <unconsulted evidence or unresolved domain question>
```

## Failure modes

- Claiming independent derivation while using the implementation as the only source.
- Treating absence from code as proof that a condition should exist.
- Reporting a missing condition without observed current behavior.
- Ranking only by traffic.
- Conflating design gaps, implementation gaps, and verification gaps.
- Auditing an entire product at once.
