---
skillx:
  name: ac-branch-pi-model
  purpose: Implement exact AC branch pi-model equations (with TAP/SHIFT handling) so branch flows, thermal loading, and nodal-flow terms are physically correct and verifier-compatible.
  scope_in:
    - bidirectional branch P/Q flow equations in per-unit
    - branch apparent-power and loading calculations against rateA
    - branch-contribution terms used by nodal balance constraints
  scope_out:
    - not for DC approximations or linearized substitutes
    - not for parsing network files or remapping bus IDs
    - not for solver orchestration or feasibility-status decisions
  requires:
    - parsed branch matrix with MATPOWER column semantics
    - bus-id to index map from data stage
    - per-unit Vm and Va vectors with angles in radians
  preferred_tools:
    - exact acopf branch equations
    - explicit i->j and j->i calculations
    - deterministic equation-level sanity checks
  risks:
    - TAP=0 mishandled (must be treated as 1.0)
    - SHIFT degree/radian mismatch
    - sign mistakes in Q flow expressions
    - mixing per-unit internals with MW/MVAr/MVA mid-stage
  examples:
    - input: Given Vm/Va and branch rows, compute branch flows and loading inputs for AC OPF constraints and report fields.
      expected_behavior: emit equation-consistent bidirectional branch metrics with deterministic checks passing.
---

# Stage Contract

## Input Artifact
- `network_parsed` from the data stage containing:
  - `baseMVA`
  - `branch` rows with MATPOWER ordering
  - `bus_id_to_idx`
- Candidate state vectors:
  - `Vm` (per-unit)
  - `Va` (radians)

## Output Artifact
- `branch_flow_state` with one record per in-service branch:
  - `P_ij_pu`, `Q_ij_pu`, `P_ji_pu`, `Q_ji_pu`
  - `S_ij_pu`, `S_ji_pu`
  - `S_ij_MVA`, `S_ji_MVA`
  - `loading_pct` (if `rateA > 0`)
  - `rateA_MVA`
- Optional bus-aggregated arrays for nodal balance:
  - `P_out_pu[i]`, `Q_out_pu[i]`

## Handoff Rule to NLP Stage
- NLP stage consumes branch flows as physics constraints, not as heuristic penalties.
- Thermal limits must be enforced in both directions.
- Any branch with invalid TAP/SHIFT/unit handling is a hard handoff failure.

# Execution Guidance

1. Normalize branch parameters deterministically:
   - If `abs(TAP) < 1e-12`, use `tap = 1.0`.
   - Convert `SHIFT` degrees to radians before angle arithmetic.
   - Use `g,b` from `1/(r+jx)`; for `r=x=0`, set `g=b=0`.
2. Compute forward and reverse flows explicitly (`i->j`, `j->i`).
3. Compute apparent power per direction from computed P/Q, then convert to MVA only at the edge.
4. Build optional bus-level outgoing sums from branch-direction outputs for nodal-balance assembly.
5. Keep all internal equations in per-unit; avoid mixed-unit expressions.

# Deterministic Pre-Handoff Checks (Required)

- Equation consistency:
  - all in-service branches produce finite `P/Q/S` values in both directions
  - no NaN/Inf in branch outputs
- Transformer normalization:
  - zero TAP is treated as 1.0
  - SHIFT conversion to radians is applied exactly once
- Thermal computation:
  - `S = sqrt(P^2 + Q^2)` per direction
  - `loading_pct = 100 * max(S_ij_MVA, S_ji_MVA) / rateA` for `rateA > 0`
- Unit discipline:
  - per-unit values are not directly compared to MVA limits without `baseMVA` conversion

# Common Failure Modes

- Correct-looking flows with wrong SHIFT sign convention.
- Using only one branch direction for thermal checks.
- Applying rate limits in per-unit while rateA is interpreted as MVA.
- Quietly accepting malformed branch rows and passing corrupted artifacts downstream.