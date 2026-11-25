---
name: hold-fix
description: "Post-CTS and post-route hold violation fixing via buffer/delay cell insertion. CTS always introduces hold violations that must be fixed. Use when: 'hold violation', 'hold fix', 'hold slack', 'fix hold', 'negative hold slack', 'post-CTS hold', 'short path padding', or after CTS completes (Step 19)."
---

# Hold Fix — Post-CTS / Post-Route Hold Violation Repair

After CTS, clock insertion delay makes fast data paths arrive too early at capture flops, causing hold violations. This is expected and must be fixed by inserting buffers or delay cells on short paths. Hold fixing is iterative: fix -> check -> re-fix until all hold slack >= 0 at the fast (FF) corner.

## When to use

- **After CTS (Step 19)**: CTS introduces clock insertion delay that creates hold violations on short paths. This is the primary trigger.
- **After routing**: parasitics change path delays, potentially creating new hold violations.
- **After ECO**: any timing ECO can shift hold margins.
- **Before signoff**: hold must be clean at FF corner for tapeout.

## Inputs

1. Post-CTS or post-route database (DEF + netlist)
2. SDC constraints with clock definitions
3. Liberty files for the fast (FF) corner — hold is worst at FF
4. STA hold report (`report_checks -path_delay min`)
5. Area budget — maximum area overhead for buffer insertion (typically 2-5%)
6. Hold slack margin target (e.g., 0 ps for nominal, +50 ps for guardband)

## Workflow

### Step 1: Analyze Hold Violations

Run STA at the FF corner (fast process, high voltage, low temperature):

```tcl
# OpenSTA
read_liberty gf180mcu_fd_sc_mcu7t5v0__ff_1p10v_m40c.lib
read_verilog <design>.v
read_sdc constraints/<design>.sdc
report_checks -path_delay min -slack_max 0 -format full_clock_expanded
```

Collect:
- Total number of hold-violating endpoints
- Worst Hold Slack (WHS)
- Total Hold Slack (THS) — sum of all negative hold slacks
- Distribution: how many endpoints per slack bucket (0 to -100 ps, -100 to -200 ps, etc.)

### Step 2: Hold Fix Strategy

The fix is always the same: **slow down the data path** by inserting buffers or delay cells.

Use native OpenSTA path details to choose a hold repair. Rerun hold and setup analysis at the same required corners and confirm that the repair does not break setup or the original area budget.

Select a delay/buffer cell from the actual available Liberty and physical views. Check input count, delay, drive and legal placement against the path and PDK requirements.

### Step 3: Execute Hold Fix in OpenROAD

Do not hand-copy the `repair_timing -hold` block — **emit it via
`programs/openroad_hold_repair_tcl_gen.py`**, which bakes in the two hard
guardrails (`-allow_setup_violations false`, never tradeable; `-max_buffer_percent`
capped at 5%) and the post-fix verification reports. It FAILs rather than emit a
budget over the cap or a `true` setup-violation flag:

```bash
python3 ../../programs/openroad_hold_repair_tcl_gen.py \
    --margin-ps <margin_ps> --max-buffer-percent <area_budget_%> --out hold_repair.tcl
```

Key parameters:
- `-slack_margin`: target hold slack (0 for exact, positive for guardband)
- `-allow_setup_violations false`: **critical** — never trade setup for hold (the
  emitter refuses any other value)
- `-max_buffer_percent`: cap area overhead (default 5%; emitter rejects > 5%)

### Step 4: Verify — No Setup Regression

After hold fix, verify setup timing is still clean:

```tcl
# Check setup at SS corner
report_checks -path_delay max -slack_max 0
report_worst_slack -max
```

If setup degrades:
- The inserted buffers added delay on paths that were also setup-critical
- Reduce hold margin target
- Or upsize the hold buffers to reduce their setup impact

### Step 5: Iterate Until Clean

```
Iteration 1: WHS = -180 ps, THS = -12400 ps, 87 endpoints
  -> Insert 143 buffers
Iteration 2: WHS = -22 ps, THS = -340 ps, 8 endpoints
  -> Insert 12 buffers
Iteration 3: WHS = +5 ps, THS = 0 ps, 0 endpoints
  -> CLEAN. Hold fixed.
```

Choose the next bounded design change from the failing native measurements and engineering sensitivity. Keep the stated iteration budget, record the changed parameters, and rerun the owning native tools with unchanged limits.

Typical iteration count: 2-4 rounds for a clean design.

### Step 6: Corner Coverage

Hold must be verified at the FAST (FF, high-V, low-T) corner — the worst-case
corner for hold. That the hold (min-path) analysis is actually driven by the FF
Liberty / operating condition (not SS/TT) is **enforced by
`programs/hold_corner_coverage_check.py`**, which FAILs if the hold view reads a
non-fast corner or if no hold analysis is present at all:

```bash
python3 ../../programs/hold_corner_coverage_check.py <hold_analysis.tcl_or_log>
```

Review the native configuration and reports for every required corner and analysis role. Record missing libraries or unexecuted corners as NOT_MEASURED.

## Constraints and Guardrails

The two numeric/template guardrails are enforced by programs (not prose):

1. **Never violate setup while fixing hold** (`-allow_setup_violations false`) —
   enforced by `programs/openroad_hold_repair_tcl_gen.py` (refuses `true`).
2. Read hold-buffer area from the native implementation database and keep the stated 5% total-cell-area budget. If it is exceeded, investigate CTS imbalance or skew rather than blindly adding buffers.

The remaining guardrails need LLM intent/spec judgment and stay here:

3. **Don't fix false paths**: verify that hold-violating paths are real (not async
   crossings that SHOULD be `false_path` / `set_clock_groups -asynchronous` in the
   SDC). A path missing its constraint vs a genuinely fast path is a spec judgment.
4. **Clock gating paths**: hold fix near ICG cells needs special care — the enable
   timing must remain correct.
5. **Scan chain**: DFT scan paths also need hold clean at scan clock frequency.

## Output format

- `timing/hold_fix_report.md`:
  - Before/after summary: WHS, THS, #violating endpoints
  - Buffers inserted: count, type, total area overhead
  - Setup impact: WNS before/after hold fix
  - Per-iteration log
  - Corner coverage matrix
  - Any remaining violations (if area budget exceeded)

## Technical basis

Hold timing: T_hold < T_clk_skew + T_data_delay. When CTS adds clock insertion delay (skew), short data paths violate hold. Standard reference: Bhasker & Chadha "Static Timing Analysis for Nanometer Designs" Chapter 7. OpenROAD `repair_timing -hold` documentation: https://openroad.readthedocs.io/en/latest/main/src/rsz/README.html.

## Handoff

- Hold clean -> `/sta-review` for full signoff timing review
- Setup degraded -> `/sta-review` to classify setup violations
- Area exceeded -> `/placement-optimize` to reclaim area
- New hold after routing -> re-run this skill post-route
- Signoff -> `/tapeout-checklist` includes hold clean as gate

## Iterate using native results

Run the owning tool on each proposed change and read its native result against
the original limit. Keep the previous design and measured result so you can
revert a regression. Stop when the declared requirements are met, the approved
run budget is exhausted, or another trial cannot resolve the remaining cause.
Report the best measured result and every unresolved requirement. Do not add an
admission record or change a limit to obtain a pass.

## Preserve the ECO reserve

Keep unused spare cells, ECO gates and reserved pads through synthesis and
physical repair. Compare the native netlist or database before and after the
change. No unused reserve instance may disappear, and its keep attributes must
remain intact. A consumed spare must be named in the intended ECO. Restore any
unintentionally removed spare before rerunning the native tools. See
`design-for-eco` for the design intent.

## Captured rule: CTS sink clustering must run

Before repairing a clock electrical or congestion failure, read the CTS log.
If `Total number of sinks after clustering` equals the sink count, or the best
solution is `max clustering size of 1 and max clustering diameter of 0`, then
clustering did not run. Each register gets its own leaf buffer and the trunk
drives all of them. Do not compensate with `CTS_DISTANCE_BETWEEN_BUFFERS`
(see `sta-review`), a cluster size or diameter, or new slew or capacitance
limits.

The cause is in OpenROAD and affects every PDK. `TechChar::initCharacterization`
reads the sink buffer input capacitance only when it also reads max slew and
max cap from liberty. `native_defaults` sets `CTS_MAX_CAP` and `CTS_MAX_SLEW`
from the document limits, so LibreLane passes both to
`configure_cts_characterization`. The capacitance therefore stays 0, and the
cluster bound (10 times that capacitance) is 0. The fix is in the OpenROAD
fork (vibeic/OpenROAD#81). Until an image includes it, keep the affected rows
FAIL and leave the plugin defaults unchanged.

Clustering alone does not keep a clock tree net under max cap. The H-tree
accepts an unbuffered segment while the path wirelength stays below
`Resizer::findMaxWireLength`, which is a delay length (8309.5 um on GF180
PWM4), and the slew stays below the limit. It never adds up the capacitance
of the unbuffered subtree. `CTS_CLK_MAX_WIRE_LENGTH` only reaches
`repair_clock_nets`, and `RepairDesign::repairClkNets` repairs only nets
driven by SDC clock source pins, so it cannot split a CTS tree net. Do not
lower it to chase a max cap violation on `clkbuf_*`. That is a CTS tool
defect, not a design or plugin setting.

Evidence from image 0.4.76 (OpenROAD 5333153b):
- Nangate45, 300 sinks, CLKBUF_X3 liberty limits given explicitly: the bound
  is 0 and CTS builds 300 leaf buffers. The same script without the limits
  has a bound of 1.421e-14 F and builds 24 leaf buffers of at most 13 sinks.
- GF180 PWM4: 416 sinks stay 416 after clustering. The root buffer net
  `clkbuf_0__core_port_0` is 0.2144 pF at nom tt (0.2349 pF worst corner)
  against 0.2 pF. With the limits left to liberty, 42 clusters (diameter
  102 um) and 51 clock buffers. The same net then rises to 0.2684 pF (0.2801
  pF worst), and `final_electrical_analysis` still has one max cap violation
  in each of the nine corners, while slew and fanout clear. Forcing size and
  diameter with the document limits gives 0.2122 to 0.2828 pF at the worst
  corner. `CTS_CLK_MAX_WIRE_LENGTH` at 1014.745 um or 300 um leaves the net
  at 0.2144 pF.
- Sky130 AES IP: 2131 sinks stay 2131 and CTS builds 2456 clock buffers.
  Routing then fails with GRT-0116 (met2 usage 99.61%). In a diagnostic
  replay with the limits left to liberty, the bound is set, 2131 sinks become
  138 clusters, CTS builds 162 clock buffers, and every row from floorplan
  through antenna checks passes.
