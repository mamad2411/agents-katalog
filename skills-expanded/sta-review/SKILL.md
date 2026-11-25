---
name: sta-review
description: Read Static Timing Analysis reports, triage setup/hold/recovery/removal violations, and propose fixes (RTL pipelining, sizing, useful skew, buffer insertion). Use when the user says "STA", "timing report", "timing violation", "setup fail", "hold fail", "close timing", "WNS", "TNS".
---

# STA Review

> **Doctrine (v0.1.50):** 把修法寫進工具，而非寫進 prompt。
> Run the native timing tools first. AI reviews their results.

STA signoff uses the selected native OpenSTA, PrimeTime or Tempus reports.
Read the launch and capture paths, SDC clocks and exceptions, Liberty corner,
SPEF and electrical drive/load model before proposing an implementation fix.

## Read the native timing results

Read the selected rows in `<project>/reports/flow_engine.json` and open their
native `reports`. `flow/steps.json` names each current tool and
`flow/native_limits.json` retains its original limits. Review `tool_ran`,
`native_steps`, `native_metrics`, and each metric's value, operator and limit.
A missing native measurement is `NOT_MEASURED`. AI reviews the engineering
meaning of every result and fixes problems in the design, tool or plugin.

```bash
python3 programs/flow_engine.py report --project <project>
```

Classify the reported failing paths as cell delay, net delay, logic depth,
clock skew or hold problems. If the I/O constraints or drive/load model are
unresolved, fix those constraints before attributing the failure to RTL.
Use the actual path components to support each classification.

## When to use

- After synthesis, after CTS, after routing, after ECO
- Any time WNS (Worst Negative Slack) or TNS (Total Negative Slack) goes positive
- When hold violations appear after routing
- Multi-corner sign-off (ss/tt/ff × low/high temp × low/high Vdd)

## Inputs

1. STA report(s) — setup + hold + recovery/removal + min-pulse-width
2. SDC constraints
3. Top violating paths (usually `-max_paths 100`)
4. Corner/mode matrix
5. Optional: RTL source for the violating module

## Workflow

1. **Categorize** every violating endpoint:
   - Cell delay limited → upsize driver, Vt swap
   - Net delay limited → insert buffer, reroute, shorten wire
   - Logic depth limited → pipeline / restructure RTL
   - Clock skew limited → useful skew, CTS re-balance
   - Hold → buffer insertion on min paths
2. **Propose fix per endpoint** with an estimated slack gain
3. **Flag paths that cannot be fixed by ECO** — require RTL change
4. **Cross-corner view**: if a path fails only at one corner, adjust margin first
5. **Summarize**: WNS/TNS before → after, number of endpoints touched

## Output format

- `sta/sta_review.md`:
  - Summary (WNS, TNS, #failing endpoints, corner)
  - Top 20 paths with classification + fix + slack delta
  - RTL change recommendations (handoff to `/rtl-repair`)
  - ECO fix list (handoff to `/eco-plan`)

## Technical basis

Static timing analysis is governed by setup/hold relationships around launch/capture flops. Standard references: Bhasker & Chadha "Static Timing Analysis for Nanometer Designs". OpenSTA is the open-source signoff-class engine (https://github.com/The-OpenROAD-Project/OpenSTA).

## Handoff

- RTL change → `/rtl-repair`
- Metal-only fix → `/eco-plan`
- Power impact of sizing → `/ir-drop-triage`
## Captured rule — PnR must run set_wire_rc + repair_design + repair_timing -setup (not hold-fix-only)

**Enforced by two programs — no longer prose judgment:**
- The full deterministic command sequence (`set_wire_rc -signal/-clock` with
  NONFATAL fallbacks → `estimate_parasitics` → `repair_design` →
  `repair_timing -setup` → `detailed_placement`; then post-CTS `repair_timing -hold`;
  then post-global-route re-estimate + repair) is **emitted by
  `programs/phase3_one_shot_runner.py`** (phase3 PnR template).
- **`programs/pnr_timing_repair_completeness_check.py`** is the static gate that
  FAILs any PnR script missing that chain (the hold-only silicon-DOA shape).

Worked example (kept for context): benchmark_clean/sha256 v0.1.25 post-route
WNS = -102.76 ns, mis-blamed on the SHA round; real cause was the missing
`set_wire_rc` / `repair_design` / `repair_timing -setup` (STA optimistic,
RSZ-0089). After adding the chain (v0.1.26): WNS = +10.95 ns MET on the same RTL.
General across all OpenROAD-driven PnR — template-level, not chip-specific.

_Captured by benchmark-enhancement-capture 2026-05-28; extracted to programs in M4._

## Captured rule — a corner that is unreported is not a corner that met

**Enforced by a program — no longer prose judgment.**

This skill already said, in prose, *"Multi-corner sign-off (ss/tt/ff × low/high
temp × low/high Vdd)"* and *"Cross-corner view: if a path fails only at one
corner, adjust margin first."* Prose cannot fail a run. Measured consequence: a
campaign ledger carried **no STA column at all** while two ICs violated setup at
the slow sign-off corner (worst setup slack **-4.33 ns**, TNS -259.13; and
**-2.35 ns**, TNS -10.36), both persisting unchanged into the post-fix verify
runs. Because timing was simply absent from the record, "the phase-3 failures
were LVS tooling artifacts" — true of the LVS part — was allowed to stand as the
whole explanation.

```bash
python3 programs/flow_engine.py report --project <run_dir>
```

Review the native STA results and their original limits for each reported corner.
Open the referenced OpenSTA logs and resolved configuration. Check:

- **R1** a reported corner is unnamed, or a corner carrying no sign-off role is
  characterised only half-way (setup without hold, or the reverse);
- **R2** a corner the flow DECLARED it would analyse has no datapoint for the
  role it was declared to serve — including the case where an STA verdict JSON
  outlives the report it cites;
- **R3** any sign-off corner violates. **A typ-only "MET" is a misleading pass**
  and never carries the run; when the typ corner met while a sign-off corner
  violated, the finding says so in those words;
- **R4** a multi-corner claim is not backed by multiple corner LIBRARIES —
  either the collapse is undisclosed (`R4_MULTI_CORNER_CLAIM_UNSUPPORTED`) or
  the run records no corner-to-liberty resolution at all
  (`R4_LIBRARY_RESOLUTION_UNRECORDED`);
- **R5** DRV is violated (`R5_DRV_VIOLATION`) **or was never queried**
  (`R5_DRV_UNQUERIED`).

### R4: a "multi-corner" run that read one library

Measured: a flow's "multi-corner" STA read the **typ liberty three times**,
varying only the SPEF. Three corners were reported; **one library was analysed**,
and the report did not say so. The degradation path is *designed* — the runner's
own docstring says that when corner libs are unavailable *"it degrades to the
single-corner `read_liberty` (byte-identical to the pre-multi-corner
emission)"*. **The degradation is not the defect; the silence is.** A degraded
run was byte-indistinguishable from a genuine one. What that silence cost: real
PVT STA run by hand closed setup+hold at three corners with TNS=0, but carried
**139 `max_slew` DRV violations at the slow corner**, entirely invisible to the
flow's single-corner check.

R4 is judged at **run level**, not per axis: a single-library RC axis is *not* a
degradation (the RC axis varies parasitics, and one process library across its
corners is correct by design). The degradation is when the run as a whole reports
several corners while never analysing more than one distinct library on **any**
axis. Judging per axis would label every healthy run degraded — the mirror image
of the defect.

A disclosed collapse is **not** a FAIL. It yields the verdict
**`SINGLE_CORNER_ONLY`** (exit 0): a PDK that genuinely ships one library cannot
do better, and failing it would fabricate a violation on every single-library
PDK. But the verdict *string* carries the limitation, so no downstream summary
can quote a bare "PASS" and have it read as multi-corner closure. **Never record
a `SINGLE_CORNER_ONLY` run as multi-corner sign-off.**

### R5: DRV must actually be asked for

`report_check_types -max_slew -max_capacitance` is what surfaces slew/cap
violations. If the flow never emits it, the report **cannot** show a slew
violation however many exist — an unqueried limit is indistinguishable from a
met one, which is the same disease R2 names for unreported slack. The emitter
attests the query with a `SIGNOFF_CHECK_TYPES_REPORTED` marker; its **absence**
is what separates "queried and clean" from "never asked".

Use the native configuration's `STA_CORNERS`, resolved Liberty files and
per-corner OpenSTA reports to identify the analysed corners. Compare their
setup WNS, hold WNS, TNS and DRV values against the original limits. A corner
name alone does not prove which library was read. Report absent corner or
library measurements as `NOT_MEASURED`, and review every tool result before
claiming signoff.

## Captured rule — split register paths from port paths before repairing

Read the native `summary.rpt` column "Reg to Reg Paths" next to "Worst Slack"
before touching the core. When every register-to-register path meets and only
the overall worst slack fails, the violators start or end at a port. Port paths
include the chip SDC (input/output delay, output load), pad cells and the core
data segment. Classify those contributions before choosing a physical or RTL
repair.

Measured on the SHA256 chip (sky130, 25.9 ns, nine corners, 2026-11-08):
register-to-register setup +0.0158 ns and hold +0.0308 ns in all nine corners,
while the overall result was setup -0.207 ns (`address[2]` to `read_data[0]`,
combinational input to output) and hold -0.031 ns (`write_data[25]` to a
flip-flop), both only in `max_ss_100C_1v60`.

Do the budget arithmetic for a combinational input-to-output path through two
`sky130_ef_io__gpiov2_pad` cells at the slow corner. The stock 20 % input delay
plus 20 % output delay is 10.36 ns. Pad IN costs 2.36 ns and pad OUT 4.94 ns
into 1.2 pF. That is 17.66 ns of 25.9 ns before any core cell switches.

In the same corner, read the design-rule counts. Max slew 5,131 and max cap 179
in `max_ss` against 73 slew in the ff corners do not establish repair scope.
The repair logs subsequently confirmed all nine corners were loaded. Check
the native configuration and loaded libraries. Never pass by changing IO delays,
loads or limits: they are documented or stock values. Close it with repair over
every sign-off corner, or in the design: register the port, or have the design
documents declare the interface budget.

## Captured rule — preserve routed SPEF through native setup and hold repair

Initialize detailed-route parasitic estimation before reading routed SPEFs.
Run native `repair_design`, then `repair_timing -setup`, then `-hold`, keeping
native buffer-removal moves available. Recheck the rerouted, re-extracted State.

Measured together on one sky130 routed State at 25.9 ns with nine corners and
image 0.4.75: these changes moved setup/hold from -0.207178/-0.031304 ns to
+0.011912/+0.047841 ns, with route DRC and antenna zero. The input-port hold
path measured -0.031304 ns before hold repair and +0.189559 ns afterward,
before rerouting. IO delays, loads and zero-slack limits stayed unchanged.
This was a routed-State replay, not a fresh full-chain proof or an isolation
of each individual change.

Timing closure did not close DRV. The final `max_ss` report retained 5,042 slew
pin violations: 66 on PAD nets, 8 on pad core-facing nets and 4,968 on core
nets. Cap retained 179: 166 on two AMUX ring nets, 10 on pad core-facing nets
and 3 on clock nets. Design repair loaded all nine corners. Join native
violating pins to netlist nets before attributing residual DRV to pads or
missing corners; retain the native failures.

## Captured rule

Do not interpret a merged diagnostic as a changed native power model. On
SHA256's original routed State, cpu_queue
`sha256-power-stock-native-complete0476-oai` ran released 0.4.76 STAPostPNR
across nine corners: TT min/nom/max each remained **41.623584926 mW** against
the unchanged strict **<5 mW** limit. Native Liberty marks the shared AMUX
pins `signal_voltage_type : "analog"`; a functionless analog connection is
not an implicit digital toggle generator.

Fork repair https://github.com/vibeic/OpenSTA/pull/23 preserves that Liberty
attribute and leaves such unannotated pins unknown. In cpu_queue
`sha256-power-analog-compile0476-oai`, compiled baseline/patched OpenSTA on
the same SHA256 State gave TT **41.623584926 -> 0.001230405587 mW**;
SS **36.502283067 -> 0.148756459 mW**; FF
**104.360230267 -> 0.009407562 mW**. All non-power STA metrics were unchanged.
No chip activity annotation or original limit was changed. Minimal floating
analog activity changed **3.86100e6/s propagated -> 0/s unknown**; an explicit
annotation and a genuinely driven analog connection retained **3.86100e6/s**.
Two existing power regression outputs matched their goldens byte-for-byte.

These are source-repair measurements, not a released-image full-chain PASS.
Unknown analog activity does not mean physically zero power, and both reports
still have zero core dynamic power, which must be investigated independently
before claiming actual operating-power closure. Do not carry the repaired
TT number into another State or replace a fresh native FAIL with it.

A low native power total is not closure if a disabled bidirectional driver
has erased incoming activity. Probe the actual input-pad and core-clock
pins before interpreting it. On SHA256's routed State, released 0.4.76
reports **41.623584926 mW TT**. OpenSTA analog-source repair #23 alone drops
that to **0.001230405587 mW**, but the real pad PAD/IN and core flop CLK/Q
all remain at **0 transitions/s**. Do not adopt that as operating power.

Dependent native repair https://github.com/vibeic/OpenSTA/pull/24 preserves
load-side activity when a three-state driver is disabled, does not charge
that disabled driver's external switching to the chip, seeds clock roots,
and retains generated-clock waveforms. cpu_queue
`sha256-bidir-clock-waveform0476-oai` built both sources in image 0.4.76 and
replayed the same SHA256 State across nine corners: combined TT
**33.619578928 mW**, SS **27.256652713 mW**, FF **73.854938149 mW**. TT still
**FAILs the original <5 mW**. All non-power STA metrics were unchanged.

Actual pad PAD/IN and core flop CLK now have **7.72201e7 transitions/s**;
flop Q has **4.06224e4/s**. Three existing native power regressions remain
byte-identical to their goldens, including generated-clock **duty 0.250**.
An intermediate clock experiment produced duty 0.500 and was rejected,
not used to change the baseline. No chip activity override, clock-period
change, library edit, waiver or limit adjustment was used. Native TT group
power is **14.30617 mW Clock**, **16.48368 mW Macro**, **2.566122 mW Sequential**,
and **0.2634334 mW Combinational**; actual design power reduction is still
needed, not merely a new acceptance summary.

## Captured rule

Do not infer `CTS_DISTANCE_BETWEEN_BUFFERS` from cell height. The explicit
TritonCTS `-distance_between_buffers` mode is a different construction policy
from ordinary slew/capacitance characterization; a legal physical segment
length is not an electrical buffer-spacing budget. Preserve native automatic
spacing unless the implementation explicitly requests a distance. Do not
change max slew/capacitance, clock period, uncertainty, or I/O delay to make
a timing row pass.

Subservient on image 0.4.76, main v1.40.65 (document-authorized 35% utilization):
removing the injected 13.6 um forced distance changed Chip routed setup from
−5.38684845 ns to −2.67480268 ns and hold from −0.04831780 ns to +0.10409396 ns.
Chip candidate SI remains FAIL on its original setup >= 0 limit; no closure
claim is justified. Classic candidate SI now PASSes: setup +0.58434148 ns,
hold +0.10575452 ns (previously +0.26383874 ns / −0.01205236 ns). Bounded
chains: Chip 28 PASS / 1 FAIL; Classic 27 PASS / 0 FAIL. No new failed rows
relative to the utilization-corrected baseline. Before the utilization fix,
the same CTS change exposed compact-core placement/padding failures: fix the
earlier floorplan root cause, do not hide those failures or accept a fallback.
Native focused config/CTS/PPA tests before rebase: 140 passed / 1 skipped
baseline, 141 passed / 1 skipped changed. Evidence:
`subservient-{ic,ip}-cts-characterization-v14065-i0476-oai-20261109`, native
reports preserved in `reports/native-steps.tar.gz`.

Leader-review cleanup on v1.40.66 removes the obsolete spacing helper, its
import/call, and tests' helper monkeypatches rather than retaining a no-op.
Generated configuration tests cover both absent and explicitly selected CTS
spacing. Native narrow tests (`subservient-cts-cleanup-v14066-unit-i0476-oai`):
baseline 146 passed / 1 skipped; cleanup 148 passed / 1 skipped. No new design
chain was requested or run for this behavior-preserving cleanup. The IC
output-path document gap and negative setup slack above remain unresolved.

## Captured rule

Do not silently filter a design author's supported native repair actuator.
`VIBEIC_PRR_SLEW_MARGIN_PCT` is an implementation optimization target, not the
original signoff max-transition limit. Make it available in the same existing
configuration path as native setup/hold margins; keep signoff at the original
0.75 ns in all corners and retain electrical/functional regressions explicitly.

Subservient IP on v1.40.69/image 0.4.76, authored native slew margin 40%:
final SS slew counts 138/66/192 -> 0/0/0; final electrical row FAIL -> PASS,
setup +1.467326746 ns / hold +0.014141966 ns. Candidate GLS still PASSes. Final
GLS remains FAIL (5 -> 15 functional failures against the boundary-corrected
baseline), and EM remains FAIL (514 violations, 664.63% -> 678.78% utilization).
Do not call tighter slew closure full signoff, suppress the functional failure,
or weaken the original limits. Native configuration/PPA tests: 124 -> 125
passed, 1 unchanged skip. The authored choice is retained in
`docs/research/subservient-native-implementation/slew.json`; native evidence is
`subservient-ip-native-slew-repair-i0476-oai` and
`subservient-native-slew-margin-unit-i0476-oai`.

## Captured rule

### SHA256: retain floating extracted RC networks when `*CONN` is empty

If native OpenRCX emits `*D_NET`, an empty `*CONN`, then real `*CAP`/`*RES`
records, do not delete that network, rewrite SPEF, invent pin connections, or
call a parser abort a timing/power PASS. A floating extracted network can still
contain real resistance/capacitance. The native reader must retain those
components and continue parsing the next network without treating the empty
connection list as a terminal.

OpenSTA fork PR #25 (`38ad897`, base `7ffe5da`) extends the connection-list
production from one-or-more to zero-or-more. Measured cpu_queue
`sha256-spef-empty-conn-retained0476-oai`, image 0.4.76: identical **233** native
parasitics/power module tests, **1 FAIL -> 0 FAIL**, `NEW_FAILED=[]`; all existing
goldens remain unchanged. The new C++ control already passes with omitted
`*CONN`; the explicit-empty variant fails on base and passes after the repair.
Both assert two retained orphan nodes, **2/3 fF** capacitances, one **17 ohm**
resistor, no terminal on either orphan node, and the subsequent connected
network's **24.2 ohm** resistor.

`sha256-spef-empty-conn-state0476-oai` replays the unchanged gated SHA256
extraction: **nine parser-failed STA corners -> nine measured reports**. Those
reports expose residual hold violations and **TT 5.275317 mW**, still FAIL at
the original **<5 mW** bound. This is a parser repair, not SHA256 power/timing,
physical-connectivity, or final-adoption closure. Fork gatekeeper review and a
released image containing the repair remain required.

## Captured rule

An implementation setting accepted by configuration is not an automatic fix if
a fresh design never selects it. Offer native `VIBEIC_PRR_SLEW_MARGIN_PCT` values
20 and 40 as ordinary Level-2 proposals when the reference actually executed
`Vibeic.PostRouteSizing`. Keep reference-first ordering, the existing 24-run
budget, pinned document settings, and the original all-PASS/native-violation
eligibility in `flow_explore`; do not adopt an otherwise failing trial or feed
a hand-authored margin file into a proof chain.

Subservient's earlier native 40% actuator qualification changed original final
SS slew counts 138/66/192 to 0/0/0 at the unchanged 0.75 ns bound, but was not an
automatic fresh-chain selection and retained EM/GLS failures. The program now
proposes both isolated native margin moves inside the existing search budget;
it also records this setting in resolved candidate configuration. No default
margin or acceptance limit changes. Focused native PPA tests: 14 -> 17 passed,
1 unchanged skip (`subservient-native-slew-search-unit-i0476-oai`). A complete
Subservient all-PASS PPA winner is still required; no adoption is claimed while
an original electrical/functional row fails. The automatic proposer and the
unchanged native-only selector are the program-level capture.

## Captured rule

Clock-to-Q path SPICE must precondition the launch register before capturing
the requested transition. An asynchronous clear/preset is not a reason to omit
warmup when the native exported side-input assignments prove that control
inactive. Keep complex/unknown controls unsupported rather than guessing;
do not force Q or change the chosen path, PDK models, or correlation tolerance.
The program repair is https://github.com/vibeic/OpenSTA/pull/26, branch
`fix/spice-async-sequential-warmup`, head `8949df9f`, base `7ffe5dae` (fork
review/merge belongs to the gatekeeper, not the author).

Measured PWM4, image 0.4.76: `pwm4-ic-spice-and-pin-native-v14072-i0476-oai`
reported NOT_MEASURED on all three original worst-corner paths because the
endpoint never transitioned. `pwm4-ic-spice-async-warmup-after-i0476-oai`
reported the same native row PASS, correlation errors 0, 3/3 CORRELATED.
STA/SPICE delays were 15.846740/14.893308 ns, 15.757048/14.804521 ns, and
15.955847/14.911439 ns. Absolute percentage errors 6.0166%, 6.0451%, 6.5456%
are below their unchanged native tolerances 13.5726%, 13.6498%, 13.4798%.
`pwm4-opensta-async-spice-headers-i0476-oai` measured two failing async warmup
controls before the repair and all 20 native SPICE regressions passing after.
This capture is program-level: the actual fix is in the tool fork; this plugin
branch records the routing and measured reusable experience only.

## Captured rule

### SKY130: estimate unrouted wires with the platform's calibrated layer RC

When routed max-slew/max-cap counts are an order of magnitude above what
global-route repair reported, compare the pre-route wire estimate with the
extracted one before touching any repair margin. LibreLane applies wire RC
from the PDK variable `LAYERS_RC` (its `set_rc.tcl`); the sky130 PDK
configuration does not set it (the values sit commented out in LibreLane
`config/pdk_compat.py`), so OpenROAD falls back to tech-LEF RC, about half of
the extracted capacitance. OpenROAD-flow-scripts sets the calibrated values in
`flow/platforms/sky130hd/setRC.tcl`. Our default lives in ONE place,
`programs/flow_config.py` `SKY130_LAYERS_RC` (`native_wire_rc`), is compared
with the installed ORFS file by `test_native_wire_rc_matches_installed_orfs_platform`,
applies only when `PDK` starts with `sky130` and `LAYERS_RC` is unset, and
never overrides a PDK- or project-supplied value. Signoff extraction, limits
and corners are unchanged; it is not a margin.

Caravel `user_proj_example` IP, image 0.4.76, paired full child chains:
final max_ss slew/cap 579/13 -> 21/0 (nom_ss 551/12 -> 10/0), setup WS
+0.643 -> +1.271 ns, hold WS +0.157 -> +0.389 ns, std-cell area
108020 -> 109709 um2, power 0.773 -> 0.831 mW
(`caravel-child-layersrc-base-v14082-i0476-cl`, `caravel-child-wirerc2-i0476-cl`).
Subservient IP sky130 full public entry stays 44/44 before and after
(`caravel-wirerc2-subservient-ip-{before,after}-i0476-cl`). The 21 remaining
pins are weak drivers that routed `repair_design` does not resize (Resized 0);
that is a separate routed-sizing rule, not a wire-RC residue.

## Captured rule

### Routed max slew left by `repair_design`: size the weak driver, do not add a margin

On detailed-routing parasitics OpenROAD `repair_design` does not resize
drivers and buffers a net only when its own Steiner estimate violates, so a
weak driver whose routed load breaks the Liberty slew limit survives routed
sizing with `Resized 0`. When the routed SPEF still reports max slew after
`repair_design`, `Vibeic.PostRouteSizing` runs the existing bounded
linked-Liberty drive-strength pass (the one `Vibeic.PostRouteRepair` already
uses): smallest legal functionally-equivalent master that measurably improves
the violating net, kept only if it does. It is a measured repair on the routed
SPEF, not a target margin; the v1.40.82 routed-repair headroom and all limits
are unchanged. `VIBEIC_PRR_BOUNDED_DRIVE_STRENGTH` (default on) is the one switch.

Caravel `user_proj_example` IP, image 0.4.76, paired full child chains on the
calibrated wire RC: max_ss slew 21 -> 0, nom_ss 10 -> 0 (18 drivers tried, 16
kept: `and2_0`, `clkbuf_2`, `buf_1`), setup WS +1.271 -> +1.362 ns, hold WS
+0.389 -> +0.375 ns, std-cell area 109709 -> 109583 um2, power 0.831 -> 0.823 mW;
`final_electrical_analysis` FAIL -> PASS
(`caravel-child-wirerc2-i0476-cl`, `caravel-child-drivestrength-i0476-cl`).
