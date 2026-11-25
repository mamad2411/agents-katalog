---
name: equivalence-check
description: Run Logic Equivalence Checking (LEC) between two representations of a design — RTL vs gate-level netlist, pre-ECO vs post-ECO, or golden vs revised RTL — to prove functional identity. Use when the user says "LEC", "equivalence check", "formal equivalence", "is this netlist equivalent", "post-ECO check".
---

# Equivalence Check (LEC)

> **Doctrine (v0.1.50):** 把修法寫進工具，而非寫進 prompt.
> Programs first; AI is the backstop. Never claim PASS without the tool's verdict.

After every transformation that touches the netlist — synthesis, DFT
insertion, clock gating, ECO — someone has to prove the result is
functionally identical to the golden RTL. This skill drives that check
through MCP-EDA's `eda_lvs` `yosys_equiv` mode.

## Mandatory Deterministic Preflight

```bash
# MCP tool call (handles SAT-engine corner cases since v0.1.12):
eda_lvs({
  mode: "yosys_equiv",
  layout_netlist: "<post-transformation-netlist>.v",
  schematic_netlist: "<golden-netlist>.v",
  top_module: "<top>",
  pdk: "sky130",  // or "gf180" or "custom" with custom_lib
})
```

The tool returns `equiv_cells_total / proven / unproven` plus
`sat_model_unsupported_cells[]` (for custom-PDK Liberty primitives
without built-in SAT models), and writes the result to `reports/lec.json`
(+ optional `reports/lec.rpt`).

Run the selected native equivalence tool and read its compared-point count, unmatched points and proven/unproven status. An empty or incomplete comparison is NOT_MEASURED, not equivalence.

Refuse to claim PASS based on log inspection alone — the rc of the program
above is the verdict.

## When to use

- Post-synthesis (RTL ↔ synth netlist)
- Post-DFT (pre-DFT ↔ post-DFT netlist, with test pins held at functional values)
- Post-ECO (pre-ECO netlist ↔ post-ECO netlist)
- Post-hand-edit (sanity check RTL refactor)

## Inputs

1. Golden (reference) design
2. Revised design
3. Key-point mapping hints (register name correspondence) if names changed
4. Constraints: which pins are test-mode, which are scan-enable, etc.
5. Tool: Yosys `equiv_*` commands (open), Synopsys Formality, Cadence Conformal

## Workflow

1. **Compile both sides** into a common internal representation
2. **Map key points**: registers, primary I/O, black-box boundaries
3. **Report unmapped points** — usually where the bug is
4. **Run verification** — prove cone-of-logic equivalence per key point
5. **Triage mismatches**:
   - Real functional change → flag to user
   - Reset-state difference → may be benign if documented
   - Uninitialized X-propagation → investigate

## Output format

- `lec/<design>_lec.tcl` (Yosys / Formality script)
- `lec/<design>_report.md`:
  - Mapped / unmapped point count
  - Status per key point
  - Debug pointers for every mismatch

## Tool prerequisites

Open flow: Yosys with `equiv_make` / `equiv_simple` / `equiv_induct`. Commercial: Formality, Conformal. The skill produces the script; execution requires the tool.

## Technical basis

Cone-of-logic equivalence checking with SAT / BDD back-ends is the industry standard for post-synthesis sign-off. Yosys implements this via the `equiv_*` pass family (https://yosyshq.readthedocs.io/).

## Handoff

- Mismatch → `/rtl-repair` or `/eco-plan`
- Re-run after fix → re-invoke this skill

## Captured rule — size EQY scratch before launching a CPU-class design

EQY partitions a CPU-class design into many small proofs, and each one keeps its
own copy of the work. Measured on Ibex chip runs (2026-11-07): 198 GB and
168 GB of partition files in two runs on one host, and 768 GB in one run on
another, against 400 GB planned. A full disk stops every job on that host, and
the later copy-back error hides the cause. Before launching, check free space
with `df` on the run directory itself, which is often a data disk, not `/`, and
plan about 800 GB for an Ibex-class chip.

## Captured rule

### SHA256: model instantiated ICG clock edges with native `clk2fflogic`

A reset-aware gated implementation cannot be compared as if each surviving
clock were the same implicit single SAT edge. Detect **instantiated** ICG
masters from their existing synthesis Liberty clock-input/output pin roles;
when present, select native Yosys `clk2fflogic` instead of `async2sync` in the
shared EQY preparation. Keep the reset replay, operands, aliases, partitions,
assertions, strategy depths, timeouts and original zero-unproved limit intact.
An unused ICG in the library, or an ordinary clock-marked buffer, must not
change preparation. Do not rewrite gate-netlist topology or disable a failing
partition to obtain equivalence.

Program capture: `flow_native_verification.eqy_clock_gates` uses the existing
Liberty pin-role reader (including compressed libraries), and `eqy` records
the selected native clock model and actual ICG masters. cpu_queue
`sha256-eqy-native-edge-model0476-oai`, image 0.4.76, replays unchanged SHA256
operands: **288 disproved partitions -> 0 unproved**, **all 1623 partitions
PASS including 59 gold-X partitions**, native wrapper comparison **0
mismatches**; **451.735 s** native tools. Native `eqy` still decides every
partition and still owns the verdict.

`sha256-eqy-clockmodel-negative-control0476-oai`: **4/4 PASS**, including an
edge-mode positive proof and an intentionally wrong data function that must
produce native **FAIL**, not merely a checker/tool error. Matched existing
regressions: **389 PASS / 6 pre-existing FAIL** at both base and repair; all six
are unrelated formal-source-path expectation cases, not suppressed or changed.
The combined repair run is **393 PASS / the same 6 FAIL**. `NEW_FAILED=[]` in
the measured regression population. This repairs the gated candidate's native
LEC row, not its residual power budget or full-chip physical signoff. Do not
adopt a gated physical point merely because this equivalence step passes.
