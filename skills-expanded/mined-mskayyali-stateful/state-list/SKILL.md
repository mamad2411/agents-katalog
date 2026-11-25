---
name: state-list
description: "Build a Stateful condition inventory for a confirmed system sentence across four related lenses: lifecycle states, failures, interruptions, and surfaces. Use after system-sentence on greenfield or feature-level work when the user needs systematic discovery with evidence, explicit coverage checks, typed relationships, and an optional v0.1 JSON mirror. For existing products, prefer state-audit. Do not treat the four lenses as equivalent state-machine node types or claim exhaustive completeness."
---

# Condition Inventory

Create a sourced, saturation-tested inventory. The four lenses compose; they are not equivalent machine-state types.

## Procedure

1. Read `STATEFUL.md`. Require a human-confirmed system sentence and note the surfaces, evidence, assumptions, and cross-cutting inventory.
2. Extract the sentence’s structural verbs and time-bearing nouns as the coverage anchor.
3. List **lifecycle states** from before/during/after and before/within/beyond probes.
4. For every lifecycle state or transition, ask what can reject or prevent the next change. Record **failures** and their cause: `user-input`, `system`, `external`, or `policy`.
5. For every lifecycle state, ask what happens when the user leaves, time passes, or actor, device, session, permission, network, dependency, or data changes. Record these as **interruption contexts**.
6. Inventory **surfaces** and their independent content, action, accessibility, freshness, authentication, and privacy constraints.
7. Connect conditions with typed relationships where evidence supports them:
   - `transition`;
   - `interrupted-by`;
   - `reenters-as`;
   - `projects-to`.
8. Attach at least one evidence reference to every condition. Use `type: assumption` when no stronger source exists.
9. Merge duplicates. Retain specialisations only when behavior or requirements materially differ.
10. Run the coverage check:
    - every structural term generates a lifecycle state or is flagged as decorative;
    - every lifecycle state has an explicit failure and interruption answer, including `none`;
    - every surface connects to at least one condition;
    - applicable cross-cutting conditions are referenced;
    - every condition has evidence or an explicit assumption.
11. Stop after three successive probes produce only specialisations. Record unconsulted evidence and known unknowns; do not claim completeness.
12. Update `STATEFUL.md` with per-lens counts, evidence consulted, assumptions, and known unknowns.
13. Ask whether the user wants `state-map.json`. If yes, write a working map with `schema_version: "0.1"`, `conditions`, `scenarios: []`, `relationships`, and `metadata.maturity: working`. New conditions use `status: discovered`; scope and priority are intentionally absent until triage.

## Output

```text
## Lifecycle states
| ID | Condition | Evidence | Why distinct |

## Failures
| ID | Condition | Cause | Evidence | Prevents/rejects |

## Interruptions
| ID | Context | Applies to | Evidence | Re-entry implication |

## Surfaces
| ID | Surface | Presents | Evidence | Independent constraints |

## Relationships
| Type | From | To | Trigger |

## Coverage
- Structural terms: <covered>/<total>
- Lifecycle interrogation: <covered>/<total>
- Surfaces connected: <covered>/<total>
- Evidence: <sourced>/<total>; assumptions: <n>
- Known unknowns: <items>
- Stopping reason: <saturation result>
```

## Failure modes

- Calling every record a lifecycle state.
- Generating a target number instead of testing coverage.
- Treating a surface as a resized screen.
- Inventing relationships without evidence.
- Using source code as the only account of intended behavior.
- Writing triage decisions during discovery.
