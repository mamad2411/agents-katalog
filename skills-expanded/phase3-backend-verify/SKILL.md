---
name: phase3-backend-verify
description: Review backend native tool measurements and reports from the sole table engine against their original limits, including synthesis, DEF, GDS, STA and DRC.
tier: verification
paired_program: flow_engine.py
---

# Phase 3 Backend Verification

Read `<project>/reports/flow_engine.json` from the normal public runner. The
Router selects the task window and `flow/steps.json` defines its ordered rows;
there is one engine run path. Identify steps by their current table position
and `name`, never by a retired public step ID.

For every selected backend row, read `tool_ran`, `native_steps`,
`native_metrics`, `metrics`, and the native paths in `reports`. Open each
underlying tool report and compare the actual measurement, operator and limit
with the original spec, PDK or owner requirement. Check that the tool consumed
the intended design and corner. An exit code or summary PASS does not prove
that the resulting silicon satisfies its engineering requirements.

AI review each result for physical plausibility, missing coverage and defects
that the reported number cannot describe. Keep the existing per-row review
and measured review duration with that result. A missing native value, missing
original limit or unexecuted selected tool remains `NOT_MEASURED`; disclose it
without fabricating a number or changing a limit. Do not claim tapeout readiness
without DRC=0, WNS≥0 and all applicable native measurements meeting their
original limits. Deferred work remains open work.

Use the actual report paths saved by the engine. The paths below illustrate
the corresponding report type; they do not override the run's native paths.

## Verification checklist

1. **Synth quality**:
   - Read the actual Yosys log and native elaboration/synthesis result. Resolve inferred latches, width truncation, unresolved modules and other tool diagnostics in the design or tool before rerunning synthesis.
   - AI residual only: read cells/area/gate-types and compare cell count to L8
     typical_gate_count if defined (judgment, no fixed threshold in spec).

2. **Floorplan / utilization**:
   - Read utilization from the native physical database. Retain the advisory 50–75% planning band; fixed-die designs may legitimately differ. A value at or below zero or above 100% requires investigation, not a fabricated placement result.
   - AI residual only: confirm core_area covers all macro instances + std cells, and that the
     IO ring + power straps are not overlapping the core (structural judgment).

3. **STA — multi-corner**:
   - Read `phase3/reports/sta.rpt` — ALL slacks must be ≥0
   - Critical paths shouldn't hit `set_max_delay` boundary; identify margin
   - Hold violations are NOT acceptable even if setup is clean
   - For complete sign-off: SS / TT / FF corner all checked, not just TT

4. **DRC**:
   - Read `phase3/reports/drc.rpt`
   - violations=0 PASS, ≥1 FAIL or WAIVED depending on rule
   - If WAIVED with Calibre deck pointer: confirm offline Calibre run is scheduled
   - Density / antenna violations are common late-stage issues

5. **LVS**:
   - Read `phase3/reports/lvs.rpt` (or note if WAIVED)
   - Net mismatches indicate floorplan / connectivity bug
   - Device count mismatches indicate wrong macro picked

6. **GDS sanity**:
   - Open the final GDS with the native layout tool. Check that the intended geometry was loaded and compare its measured extent and content with the required design scope.
   - Read the GDS hierarchy with the native layout tool and confirm that the selected top cell is the intended root, with all required child cells resolved.
   - AI residual only: sanity-check that the file size is consistent with a merged macro
     PA-GDS (size jumps when a hard macro is merged) — judgment, no fixed threshold.

7. **Power / EM / IR estimates**:
   - if available, read `phase3/reports/power.rpt`
   - Compare to L8 power budget if defined

## Spot-check actions

- Open the GDS in KLayout (offscreen) and visually confirm metal stack reasonable.
- Diff this design's `area.rpt` and `sta.rpt` vs prior known-good run; flag regressions.
- Check critical timing paths: do they make sense (clock-to-clock through expected logic) or are they bizarre artifacts?

## When to escalate

- DRC violations >0 → invoke `drc-fix`
- Setup slack <0 → invoke `sta-review` then `eco-plan`
- Hold violations → invoke `hold-fix`
- LVS mismatch → invoke `lvs-triage`
- Utilization wildly off → re-run with adjusted `--die-um` / `--util`

## Output

Append findings to `<project>/reports/phase3_verify.md`. For each selected row, record its current position/name, native report and value, original limit, AI finding, and any FAIL or `NOT_MEASURED` obligation. Keep a measured PASS distinct from deferred or unmeasured work.

## Captured rule — Split full functional GLS from chip timing

Run the complete existing suite on the routed netlist with compiled zero-delay
simulation. When native pad models require unsupported switch primitives and
the PDK supplies no compatible functional view, export the routed core through
the declared preparation's pad connections. Keep native chip models on Icarus
for fixed documented transactions and a walking check of every signal pad path.
Repeated-message stress stays complete in the compiled arm. Both arms must pass.
Unlaunched or undecided checks stay NOT_MEASURED, and coverage limits stay intact.
Only restrict VPI visibility when the bench's DUT access is limited to port
values; retain full visibility for other access patterns.

One retained chip row failed after 61,753.1 seconds. The split row preserved FAIL
in 100.9 seconds with 126 native SDF errors; its pad checks passed 77/77 paths.
The complete professional suite passed 6/6 on the routed core in 272.0 seconds
including preparation and compilation, and all six HDL benches passed in a
separate 184.6-second replay. The corresponding IP prototype passed all six
tests and 2,951,777 cycles in 196.4 seconds plus 30.2 seconds compilation.
These single retained trials establish component execution and faster rejection,
not a healthy chip timing PASS.

## Captured rule

A physical pad Liberty master can be a simulation-only transparent wrapper:
Sky130 `sky130_ef_io__gpiov2_pad` has no specify block and instantiates the
pin-for-pin native `sky130_fd_io__top_gpiov2` as `gpiov2_base`. Bind the SDF
CELLTYPE/INSTANCE to that declared child scope. Preserve the original DIVIDER,
all conditional OUT/OE_N/PAD paths, unconditional INP_DIS paths, timing checks,
and every delay tuple; top-level INTERCONNECT endpoints stay at wrapper ports.
Do not synthesize specify arcs or turn conditional paths into unconditional ones.
On the original SHA256 v1.40.54 State, cpu_queue job `sha256-pad-sdf-bind-oai`
replayed both GLS rows: candidate SDF errors 2464 -> 0 (407862 applied records),
final nine-corner SDF errors 22638 -> 0 (3670758 applied records). Directed pad
checks passed 77/77 in every selected corner. This exposed, rather than waived,
5 candidate / 45 final functional transaction failures; full Verilator coverage
remained unmeasured. Annotation closure alone is not GLS PASS. The same packet's
broad unit selection was 402 PASS / 6 FAIL, all six in unrelated formal source
path assertions; do not describe that broad selection as green.

## Captured rule

For a physical chip GLS replay, bind the **external boundary environment** as
well as the testbench clock period to the native SDC. An RTL bench that changes
bus controls immediately after an external posedge does not implement an SDC
`set_input_delay 5.18`: the controls can race the propagated internal clock.
Do not change any cell/SDF arc, expected value, transaction, timeout or clock
period. Apply the declared uniform input arrival on the existing pad-driver
bridge (never on the clock), and observe the existing read capture at the SDC
`T - output_delay - uncertainty` deadline. Leave nonuniform/unsupported
constraints unguessed.

On the v1.40.54 SHA256 State, native tracing showed the initially valid one-hot
FSM become `0000` at INIT with the zero-offset RTL stimulus. Changing output
sampling alone from 1 ns to the SDC 20.47 ns deadline still failed 5 candidate /
45 final transactions. Binding the original SDC 5.18 ns external input arrival
as well closed those failures: cpu_queue `sha256-gls-sdc-boundary-oai` measured
candidate/final `gls_failures` **5/45 -> 0/0**, SDF annotation errors **0/0**,
with **407862/3670758** applied native delay records unchanged. Candidate:
6 Icarus + 7 Verilator PASS; final: 54 Icarus + 7 Verilator PASS, no unmeasured
functional arm. The original error limit is still zero. Parser tests: 5 PASS
locally; packet narrow suite had 109 PASS plus one newly added test's malformed
single-line fixture failure; correcting the fixture's instance line boundary
passes all 5 new tests without changing implementation behavior.

Routed timing-repair margins are per-design optimization settings, not signoff
limits or global headroom defaults. Preserve `PostRouteSizing`'s shipped defaults.
Allow an explicitly selected `VIBEIC_PRR_SETUP_MARGIN` / `VIBEIC_PRR_HOLD_MARGIN`
to survive document/native-config filtering just like the other PPA settings.
For the v1.40.54 SHA256 routed State, the original native setup/hold slacks were
-0.25775649011418533 / -0.03923617097834743 ns. Selecting 0.5 / 0.1 ns margins
in that design's `work/flow/native_overrides.json`, then native routed sizing,
rerouting, RCX and nine-corner STA measured +0.25528735403758707 /
+0.0747262273210573 ns (cpu_queue `sha256-per-design-routed-margins-oai`). The
original candidate SI checks remain >= 0 ns; both pass. Narrow tests: 14 passed,
1 skipped (the existing external-tool prerequisite). The replay harness failed
only when it tried to write into an uncreated SI report directory after STA;
`repair.json` and native STA reports completed, and the ordinary SI comparator
on those emitted Decimal metrics passes. This is not final electrical closure:
slew/cap/fanout and layout checks still require their own native results.

## Captured rule: functional GLS is not an STA timed-view consumer

Keep the v1.40.54 split explicit: Verilator runs the **complete original
functional suite** on the routed core (zero delay); Icarus runs the directed
SDF replay on the native physical chip, including pad paths and all requested
corners. Both arms must pass. Generated arithmetic scenario/serial-oracle
metadata must not send the compiled arm through STA-bound bench regeneration.
Its existing operands, reset/state checks, assertions, transaction population,
clock schedule and timeout remain those of the original functional bench.

On SPM gf180mcuD, v1.40.57's `_postlayout_output_deadline` correctly compared
resolved `nl`, `sdc` and the complete `sdf` path set against the selected native
STAPostPNR `state_out.json`. The split's functional `nl` was `routed_core.v`,
not that State's `spm_chip.nl.v`; the generated arithmetic preparation therefore
incorrectly rejected all five Verilator cases with
`POSTLAYOUT_OBSERVATION_UNMEASURED: GLS and STA do not use the same timed views`.
The Icarus arm already passed (6 candidate / 54 final runs), applying
11304 / 99942 SDF records with zero annotation errors. Do not loosen the view
identity check, substitute a chip STA deadline for a zero-delay core, or accept
a successful timing arm as coverage for an unmeasured functional arm. Restrict
STA observation preparation to the timed Icarus path, leaving its SDC/SDF,
scene provenance, deadline checks and original zero-error limits unchanged.
Native unit coverage must also inject a functional mismatch and prove that it
still fails with either scenario or serial-parallel generated-bench metadata.

Native proof: cpu_queue `spm-gls-functional-views-oai` (image 0.4.75) replayed
only Steps 75 and 96 from the retained SPM State. Both originally NOT_MEASURED
rows now have zero GLS errors: 6 Icarus + 5 Verilator PASS at candidate, 54
Icarus + 5 Verilator PASS at final. Applied delays remain 11304 / 99942 and
annotation errors remain zero. The focused packet suite reports 114 PASS /
303 deselected; the complete workload test file separately reports 23 PASS.
This is a two-row repair, not an unexecuted full-flow/adoption PASS claim.
SHA256 control: cpu_queue `sha256-gls-functional-views-oai` replayed the same
two rows on its retained native State; both stay PASS (6 Icarus + 7 Verilator
candidate, 54 Icarus + 7 Verilator final). Applied records remain
407862 / 3670758, annotation and GLS errors remain zero; focused tests are
114 PASS / 303 deselected. Neither replay has a newly failed row.

## Captured rule

Select a GLS chip-pad extraction from the active native configuration, not
merely from a retained `work/flow/chip/preparation.json`. A Classic hard macro
may share a project history with a Chip run; retained wrapper inputs cannot
change its selected DUT. PWM4 IP v1.40.59/image 0.4.76 had candidate/final GLS
NOT_MEASURED: native routed `chip_top` was compared against retained
`chip_top_chip`. The narrow native-simulator reproduction
`pwm4-ip-retained-chip-before-i0476-oai` failed 1 test with no `gls_failures`
measurement. After matching the prepared chip's DESIGN_NAME to the selected
native DESIGN_NAME, `pwm4-ip-native-top-unit-i0476-oai` passed 24 tests in
82.77 s; the retained-input reproduction measures GLS failures 0 and both
Icarus and Verilator PASS. Chip pad-path/bad-connectivity and functional
negative cases remain tested. This is a subject-binding repair, not a waiver
or a limit change; full PWM4 path proof is still required.

### SHA256: preserve selected-bit predicate text in the simulator, not the SDF

When native GPIO SDF cannot bind conditional paths, reduce a real CELL record
with the unchanged installed PDK model, and inspect native `-sdf-warn` output.
Zero SDF ERROR lines alone do not demonstrate annotation: unsupported predicate
text may leave paths **skipped**. Repair the simulator's predicate representation;
never replace conditional paths with unconditional ones or edit native delays.

Icarus master `0d9012941` had lost constant bit-select rendering during source
identity integration. Its existing `sdf_cond_bit_select` waveform test was also
unregistered. Fork PR vibeic/iverilog#20 (`40e0d54b2`) restores declared-index
text only for one-bit equality operands; the existing unsupported bare-select
fallback/ifnone/reject contracts and goldens remain unchanged. It registers the
existing regression and a bitwise-AND counterpart, both checking actual edges
at **103/205/307/411 ps** on ascending and nonzero-based packed ranges.

Measured cpu_queue `sha256-iverilog-bitcondition-regression0476-oai`, image
0.4.76: identical 112 native tests, base **2 FAIL**, repair **0 FAIL**,
`NEW_FAILED=[]`. A real single-pad CELL emitted **24 skipped conditional-path
warnings** with the released tool and **0** with the rebuilt repair. The known
TIMINGCHECK capability warning remains visible. This is a simulator reproducer
repair, NOT proof that SHA256's original 1824-error candidate GLS row or either
complete chain passes. Keep their original results until native replay on a
released image measures them; only the fork gatekeeper merges tool changes.

## Captured rule

For timed cocotb replay, bind the constant actually passed to the imported
`cocotb.clock.Clock` constructor to the native SDC period, including its literal
time unit. Do not infer support from a constant's spelling or silently accept
an unbound driver. PWM4's documented reference uses `Clock(dut.clk, CLOCK_NS,
unit="ns")`; the previous binder recognized only custom HALF_NS drivers and
reported its timed Python arm NOT_MEASURED even at the documented 40 ns.
`pwm4-cocotb-constant-before-i0476-oai` measured 2 native positive regressions
FAIL (3 ns / 3 us left unbound instead of 25 ns) and 2 shadowed negatives PASS.
`pwm4-cocotb-constant-after-i0476-oai` passed 39 tests in 124.37 s; both unit
variants measured 25000 ps, native Icarus GLS PASS, and source benches remained
byte-identical. Shadowed constants and clockless suites remain NOT_MEASURED;
existing manual-clock, pad-path and compiled-functional negatives still pass.
Full PWM4 chain proof is separate from these measured narrow tests.

## Captured rule

A hard-macro GLS boundary needs its original SDC input arrival times just as a
pad boundary does. Recording `input_arrivals` without driving that delay models
a different SRAM environment: new synchronous read data can reach delayed
internal clocks in the wrong cycle. Insert the declared delay on the existing
bench driver, never on native cells/SDF and never on the clock. Retain unobserved
native outputs with undriven bench wires so Icarus can annotate their original
INTERCONNECT records. Preserve existing named/escaped connections; do not mix
named and positional syntax or remove SDF errors.

Subservient IP, image 0.4.76, original 10 ns clock / 2 ns SDC input arrivals:
candidate GLS went from 5 failures (3 functional + 2 missing output intermodpaths)
to 0; applied delays 6060 -> 24256 across four Icarus cases, annotation errors
2 -> 0, and all four Verilator cases passed. Native final nine-corner replay
improved 45 -> 5 failures with zero annotation errors: the CPU program still
fails 0/5 in min_ss_100C_1v60, while the other eight program probes pass 5/5.
Existing stop-on-failure leaves the remaining final suite unmeasured; this is
not final replay closure. IC control still reports its original 912 annotation
errors (7743 applied records), not a repaired simulator claim.

Native boundary/workload tests: baseline 29 passed, changed 33 passed. Broader
native verification tests retained the same six pre-existing formal-path
assertion failures (418 -> 421 passed); no original tests or failures were
waived. Evidence: `subservient-ip-gls-boundaries-v14067-i0476-oai`,
`subservient-ip-final-gls-boundaries-v14067-i0476-oai`,
`subservient-ic-gls-escaped-control-v14067-i0476-oai`, and
`subservient-gls-boundaries-final-unit-i0476-oai`.

### Derive child pin sets and SDC names from the native parent binding

A parameterized child must be physically prepared against its parent-bound
native interface, not its standalone default width. Preserve every supplied
pin pattern and its edge. Place missing bits on the edge of the numerically
highest already-placed bit of their bus; for a new bus or scalar, use the last
declared edge. Preserve reverse-edge directives. Supply pins remain owned by
the PDN, not signal IO placement. Run the native IO placer on the derived file;
do not relax missing-pin diagnostics or drop interface bits.

Where a supplied child SDC still queries a parent port name, map only static
`get_ports` objects using unambiguous equal-width whole-port connections from
the native elaborated parent hierarchy (the design's own L8 binding). Never
infer aliases through slices, casts, internal nets or ambiguous connections.
Retain every timing value, exception, clock, load and original limit. Stage
the same derived SDC into Phase 1 and native implementation. Child-authored
`work/flow/native_overrides.json` remains an independent design input; parent
configuration must not leak into the child.

Historical narrow measurements on Caravel/image 0.4.76: the L8 BITS=32 binding
and supplied 16-bit pin order yielded 48 missing pins, reduced to 0 by complete
pin placement; placement and CTS changed FAIL→PASS. The wrapper `user_irq` to
child `irq` alias reduced OpenSTA missing-port diagnostics from 6 to 0 over
three corners, with unconstrained paths/endpoints remaining 0 against limit 0.
These measurements motivated the general preparation code; hand-run per-design
recipes are not a valid fresh-chain fix and have been removed. The general
code is exercised with a neutral WIDTH=4 tile, including native `dir::` glob
preprocessing, preserved original edge placements and SDC values, and rejected
ambiguous/sliced aliases. Fresh from-documents packet
`caravel-ip-fromdocs-v14063-childinputs-glob-i0476-oai` on v1.40.63 plus this
fix ran without manual preparation: native missing-pin diagnostics **48→0**,
SDC invalid diagnostics **6→0** (limit **0**), placement/clock planning/CTS and
pre-layout timing **PASS**. All **16** targeted tests passed. Parent result was
**38 PASS / 7 FAIL / 0 NOT_MEASURED**, NEW_FAILED=[] relative to the provided
chain. The macro row still fails on later child setup timing (**-0.438153 ns**),
SDF annotation (**99** candidate errors), and final electrical analysis;
child functional simulation/activity remain unmeasured. Do not describe this
input-preparation repair as whole-macro or parent signoff closure.

## Captured rule

A sequential UDP's asynchronous level rows and edge rows update the same
state. If a simulator lowers the former to combinational blocking assignments
and the latter to NBA writes, repair that lowering in the simulator; do not
suppress BLKANDNBLK or replace the PDK models. PWM4 native compiled GLS on
image 0.4.76 produced four BLKANDNBLK errors and no JUnit verdict in
`pwm4-ic-compiled-core-native-i0476-oai`. The repair is submitted for fork
review at https://github.com/vibeic/verilator/pull/2 (branch
`fix/udp-async-nba-output`, head `0acd73e7a`, base `806bddcf3`); the author
has not merged it. `pwm4-verilator-udp-configured-tests-i0476-oai` built with
`--enable-ccwarn` and passed all 22 native UDP regressions, 0 failed/skipped.
`pwm4-ic-udp-functional-runtime-i0476-oai` used that built compiler on the
retained routed core: both the retained bench and document-derived expert
reference passed, 2/2 JUnit tests, GLS failures 0. The split workload's separate
Icarus SDF arm and full stock-image chain still require their own proof after
the fork gatekeeper integrates the fix. No native limits or diagnostic gates
were changed.

## Captured rule

Bind generated CPU-case startup reset launch to the native SDC reference edge;
do not add a rising-edge input arrival to an unrelated falling-edge release.
The case producer owns initialization stimulus, not the checker. Launch the CPU
program's startup release nonblocking after its already-counted rising edge.
For the generated retention case, retain both original measured windows and
in-flight reset assertion exactly, hold reset for one additional unmeasured
setup edge, then launch only initial deassertion nonblocking. The existing native
input driver supplies the original arrival delay. Do not initialize RF state,
change memory contents, extend program/retention budgets or suppress Xs.

Measured Subservient IP, image 0.4.76, original 10 ns clock / 2 ns input arrival:
min_ss startup previously advanced bsel at 107.073 ns but pending at 117.101 ns,
skipping the byte-zero tag. RF rdata0[1] first went known-to-X at 127.052 ns;
regzero staying X was a consequence, not permission to initialize it. The paired
nom_ss control aligned bsel/pending at 117.102/117.132 ns. With the owned startup
launch, the pin reset release is 97 ns rather than 102 ns, bsel/pending align at
107.073/107.101 ns, the first byte is captured at 127.091 ns, and regzero resolves
normally. RAM preload and expected program words are unchanged.

Native final GLS: 5 functional failures -> 0, all 36 Icarus cases across nine
corners and all four Verilator cases PASS; 218304 delays applied, 0 annotation
errors. The min_ss four-case control also PASSes (24256 applied delays). Native
boundary/workload tests: 33 -> 38 passed. A blanket clock-resampling experiment
was rejected because it added an extra active-operation latency and produced
9 reset-retention failures; neither that source nor a moved checker window is
used. Evidence: `subservient-ip-final-gls-producer-launch-i0476-oai`,
`subservient-ip-minss-producer-launch-trace-i0476-oai`, and
`subservient-producer-reset-launch-unit-i0476-oai`. Automatic producer helpers
and their native-SDC call sites are the program-level capture.

## Captured rule

### SDF routes through continuous output assignments must retain bit identity

When a native INTERCONNECT from a scalar cell output to a vector output bit
reports `Could not find/insert intermodpath`, inspect the compiled route before
changing the SDF or cell model. An explicit continuous assignment can retain a
Z-preserving `BUFZ` before the vector concatenation. That assignment is part of
the valid route, not a logic gate or an absent endpoint. Icarus must traverse it
while retaining the node and its strength conversion; do not remove the record,
mask its error, replace the tie model, or count it as an applied delay.

Program capture is **Icarus fork PR https://github.com/vibeic/iverilog/pull/21**,
commit `d32f49f`, not a plugin waiver. The native regression checks independent
2/3/4 ns delays on 0/1/X/Z transitions plus constant outputs. Before it failed
with six rejected records and an undelayed edge; after it passed. The complete
native VVP suite passes **1103/1103**, with optional waveform backends enabled.
Evidence: `caravel-iverilog-output-alias-artifact-i0476-oai` (exit 0).

Paired actual Caravel wrapper replay, unchanged routed netlists/SDF and original
limits, base image **0.4.76**, stock tool before and fork-built tool after:
`caravel-parent-iverilog-output-alias-native-i0476-oai`:
- Candidate: annotation errors **111→0**, applied delays **7432→7543**,
  `gls_failures` **111→0**. Icarus **3/3** and Verilator **3/3** tests PASS.
- Final: annotation errors **999→0**, applied delays **66888→67887**,
  `final_gls_function_timing_errors` **999→0**. All nine Icarus corners
  **3/3** tests each and the Verilator **3/3** suite PASS.
- Original requirements remain annotation/function errors **0** and applied
  delays **>0**. Both rows FAIL→PASS, NEW_FAILED=[] in this two-row comparison.

The exact increase in applied records is evidence that the missing paths were
annotated, not discarded. These are native narrow proofs using the fixed fork;
they do not claim that an unmodified old image or the complete design chain
passes. Tool deployment remains with the fork gatekeeper; the author does not
merge the PR. Child functional/activity and final electrical DRVs still need
independent closure.

### Routed sizing needs headroom for legalization and rerouting

Do not use a zero-slack optimization target when the native routed sizing step
is followed by legalization, global routing, timing repair and detailed routing.
Keep every signoff scene, input/output delay, derate and acceptance limit. For
an unspecified routed sizing target, reuse the existing design derating budget
(`CLOCK_PERIOD * TIME_DERATING_CONSTRAINT / 100`) or the native GRT setup
margin, whichever is larger; retain the native GRT hold margin. Project-native
and document-authored routed targets, including explicit zero, still override
these defaults. This is implementation headroom, not a relaxed timing check.

Measured Caravel child, image 0.4.76, base main v1.40.79: the native sizing log
reached +0.431 ns setup slack before subsequent routing, but signoff on the
resulting extracted route had setup **-0.630002734 ns** and hold
**-0.067879038 ns**. Native routed optimization targets were 0/0 ns. With the
existing 25 ns period and 5% derating budget, the default setup target becomes
**1.25 ns** and the existing GRT hold target **0.2 ns**. Fresh native child
implementation through candidate SI then measured setup **+0.643368044 ns**
and hold **+0.157165840 ns**, both against unchanged **0 ns** limits:
`candidate_signal_integrity` FAIL→PASS, **129 tests passed**, NEW_FAILED=[].
Evidence: `caravel-routed-headroom-native-v14079-i0476-oai` versus
`caravel-child-timing-native-v14077-i0476-oai` (same relevant native flow).
This is automatic program capture in `flow_config.native_defaults`.

Do not infer whole signoff closure: max-slew violations remained **579**
(before 586), max-cap violations **13** (before 14), and fanout violations **7**.
Native GLS and missing child functional activity still require separate work.
The earlier CTS-scene experiment was rejected: selecting the measured slow
scene changed setup only to -0.621924 ns and hold to -0.045779 ns; it did not
pass and no scene-selection change is included in this fix.

## Captured rule — the SDF arm needs directed cases the documents declare

A gate-level row that runs for hours is first a question about WHAT the SDF
arm simulates. `gls_workload.directed_benches` gives the Icarus SDF arm the
directed HDL cases of the suite; when the documents declare none, the arm
replays the whole suite at every corner and the row detail now says so ("The
suite has no directed HDL case, so the SDF arm replays the whole existing
suite (...) at every selected corner"). Do not drop a corner, shorten the
contract test or move it between arms to save time.

Fix it in the design documents: declare short directed cases, one per
timing-relevant transaction (a write to every register observed at an output,
an output edge on every channel, reset release, each asynchronous input), as
`- **Name**: stimulus; expect ...` bullets in the verification-plan document,
and deliver each case's test program as `input/sim/tb/<case name>.v`
(`module <case name>;`, a `` `timescale ``, a free-running
`always #<half> clk = ~clk;`, the logical top instantiated with named
connections, `[TB ...] FAIL` lines and `ORACLE_TB_DONE pass=n/m`). The
stimulus text must come before the first "expect/check/assert" word or Phase 1
refuses the case. The full contract test stays in the suite for the compiled
zero-delay arm.

PWM4 IC, gf180mcuD, image 0.4.76, from documents: three directed cases
(reset release; nine register writes with a PWM edge on every channel;
asynchronous reset while running). SDF arm before: `tb_chip_top.py`
(82,215,675 ns, 2.06 M clock cycles, 9171 s per corner in Icarus), row wall
9192 s candidate / 24644 s final. After: 3 directed cases + pad paths, PASS at
all nine corners, `sdf_annotation_errors` 0, failures 0, 3-24 s per case; row
wall 27 s / 66 s; chain 11 h -> 26 min. Both rows stay FAIL on the unchanged
compiled arm: Verilator rejects the gf180 UDP `primitives.v` (BLKANDNBLK), so
the contract test still has no zero-delay gate-level run on this image; it
passes in `functional_simulation_and_coverage`.
