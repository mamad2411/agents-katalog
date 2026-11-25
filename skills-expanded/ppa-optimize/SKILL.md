---
name: ppa-optimize
description: Propose bounded, reversible actuator moves that trade power, performance and area against each other — placement density, clock period, synthesis effort, buffering, floorplan aspect — each with the effect it predicts, the remeasurement that would falsify it, and its rollback. Use when the user says "improve PPA", "close timing", "shrink area", "reduce power", "what should I try next", or when a closure loop needs its next candidate.
---

# PPA Optimize

## The boundary this skill lives inside

This skill produces a **structured proposal**. It never produces a gate
verdict, and it never reports that a move worked. A proposal becomes a result
only when `ppa-measure` re-reads the artefacts afterwards and a deterministic
program — `_ppa/feasibility.py` and `_ppa/pareto.py` per
`docs/PPA_INTERFACES.md` §4 — compares the records.

That ordering is the whole point. The failure mode it prevents is the one that
looks most like success: a model proposes a change, the change is applied, and
the same model reports the improvement it predicted. Nothing in that loop is a
measurement, and the number it produces is indistinguishable from one that is.

Every candidate this skill emits therefore carries four things that make it
falsifiable: the actuator, the predicted effect, the remeasurement that would
refute the prediction, and the rollback.

## When to use

Trigger when the user:
- Has measured PPA and wants the next thing to try
- Is missing a target on one axis and wants to know what it costs on the others
- Needs candidates for a closure controller (`_ppa/closure.py`) to actuate
- Wants the trade-off surface rather than one recommendation

## Inputs to gather

1. The baseline: canonical metric records from `ppa-measure`, with their scope
2. The target: which metric, which threshold, at which scope
3. The actuators that are legal here — some designs forbid touching the RTL,
   some forbid moving the clock period, some allow only PnR configuration
4. The budget: how many tool iterations and how much wall clock the loop may spend
5. What must not regress: the axes that are already at their limit

## Workflow

1. **Pin the baseline scope first.** A proposal that improves a post-place
   number and is checked against a post-route number has not been checked at
   all. State the baseline scope on its own line and require every candidate's
   remeasurement to name the same one.
2. **Enumerate actuators, not outcomes.** "Reduce area 5%" is a wish. "Placement
   density 0.62 to 0.58" is an actuator: it is a thing that can be moved, its
   move can be undone, and the move is visible in a config diff.
3. **Predict, in the units of the metric record.** A prediction in words cannot
   be refuted. A prediction of `+0.05 ns` on `timing.setup.wns_ns` at a named
   scope can be.
4. **Attach the remeasurement.** Name it, with its scope, before the move is
   made. A remeasurement chosen after seeing the result is a different
   experiment from the one that was proposed.
5. **Attach the rollback.** Every candidate states the exact state the design
   returns to. A move with no rollback is not a candidate; it is a commitment,
   and it belongs in a different conversation.
6. **Keep the triple, do not collapse it.** Rank candidates on the frontier over
   power, performance and area. A single weighted score hides which axis paid.
7. **Spend the budget explicitly.** State how many iterations the proposal
   assumes, so a controller can refuse it before it starts rather than halfway.

## Do not

- Do not report an improvement. Report a prediction, and the remeasurement that
  would refute it.
- Do not compare a candidate against a baseline at a different stage, corner,
  mode or activity basis. That comparison is `UNDETERMINED`.
- Compare the native netlist or implementation database before and after optimization. Preserve every unused ECO spare, its keep attributes and the reserved pads; an unintentionally removed spare must be restored.
- Do not propose relaxing a rule deck, waiving a check, or hand-editing a
  layout. An improvement obtained that way is worth less than the number it replaces.
- Do not fill a required field with a placeholder. `X_no_placeholder_fields`
  catches it, and it should: an unfillable rollback field means the candidate is
  not reversible and the honest report of that is a sentence, not a dash.

## Output format

The deliverable is one markdown proposal. The template below is the whole shape.

    # PPA Optimization Proposal — <design>

    Verdict authority: _ppa/feasibility.py - this proposal states no pass/fail of its own.

    ## Summary
    <what is being missed, on which axis, at which scope>

    Baseline scope: post_route_extracted / ss / 1.62 V / 125 C / rc_corner=max
    Budget: 6 PnR iterations, 4 h wall clock

    ## Proposal

    ### C1 — loosen placement density
    Actuator: PL_TARGET_DENSITY 0.62 -> 0.58
    Expected effect: timing.setup.wns_ns +0.04 to +0.07 ns; area.core_um2 +1 to +2%
    Remeasure: run /ppa-measure at post_route_extracted, same scope as baseline
    Rollback: restore config revision 4f21 and re-run PnR from the checkpoint
    Costs: 1 PnR iteration

    ### C2 — raise synthesis effort on the critical module
    Actuator: synthesis effort low -> high, scoped to <module>
    Expected effect: timing.setup.wns_ns +0.02 to +0.05 ns; power.total_mw +0 to +3%
    Remeasure: run /ppa-measure at post_route_extracted, same scope as baseline
    Rollback: restore the previous synthesis script revision
    Costs: 1 synthesis + 1 PnR iteration

    ## Frontier

    | candidate | performance | power | area | dominated by |
    |---|---|---|---|---|
    | C1 | + | 0 | - | none |
    | C2 | + | - | 0 | none |

    ## Evidence

    | artefact | sha256 | tool |
    |---|---|---|
    | phase3/stage3/sta/sta_mcorner_ocv.rpt | sha256:0a5b93f6 | opensta |

    Next: run /ppa-measure

Baseline and candidate numbers travel as canonical records, never as loose
figures in the table above:

Read the requested PPA values from the actual native synthesis, timing, power or physical reports. Name the design scope, corner, units and source paths; an absent measurement remains NOT_MEASURED.

Serialize with `programs/_ppa/canonical_json.py` and nothing else.

## Captured rule

Native electrical closure belongs in the existing bounded PPA proposer, not in
hand-fed margin/grid files. For a template-owned Classic grid with measured EM
overload, derive grid-density scale from the native utilization ratio (next
power of two), snap pitches/landing widths to the actual PDK manufacturing grid,
and retain native spacing/supply ownership. Keep custom and pad-connected grids
unchanged. Pair native grid/slew proposals with existing native CTS options when
the reference still reports fanout violations; never raise that fanout limit or
ignore the clock counter. All original native limits and all-PASS/zero-violation
eligibility, document pins, seed and the 24-trial budget remain unchanged.

Subservient IP, image 0.4.76: fresh main v1.40.75 was 40 PASS / 4 FAIL (EM514,
664.63% worst utilization; final SS slew138/66/192; dependent aggregation). Native
program-generated proposals qualified one zero-counter candidate. Its 33 fresh
rows plus 11 ordinary remaining rows on the same unchanged worker project give
44 PASS / 0 FAIL / 0 NOT_MEASURED, native signoff/compliance counts0: EM0/69.98%,
slew/cap/fanout/route/antenna0, setup+1.671524300ns, hold+0.022734537ns, Magic and
KLayout DRC0, LVS0, final GLS0. The unchanged native comparison marks it eligible.
This is complete candidate qualification, not yet a fresh-main full PPA proof.

The generated settings came from native context: overload scale8, PDK-grid
pitches19.2/19.15um, unchanged1.6um landing width, native slew probe40 and existing
CTS8/100 option. No hand file feeds the chain. Other measured proposals remain
ineligible (including a step-PASS candidate with native fanout1); do not adopt a
partial success. Evidence: `subservient-native-electrical-spool-prepare-i0476-oai`
and its 12 existing worker packets, plus
`subservient-electrical-1-2-2-remaining-native-i0476-oai`. Automatic context reading,
native proposal generation and the existing original-limit selector are the
program-level capture. Remove the obsolete one-off slew JSON instructions.
