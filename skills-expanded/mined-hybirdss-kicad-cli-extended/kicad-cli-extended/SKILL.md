---
name: kicad-cli-extended
description: >-
  Drive KiCad 10 with kce: schematic/PCB editing, ERC/DRC, Gerber/BOM/CPL/STEP, JLCPCB/PCBWay,
  first PCBs, netlist-first apply/verify, ECOs, rollback, CI, placement optimization, custom
  symbols/footprint wizards, Altium/Eagle import, SPICE simulation, differential pairs and
  length tuning, via fences, teardrops and panelization. Use for KiCad, .kicad_pro/.kicad_sch/
  .kicad_pcb, make me a board, replace a part, decoupling, warm worker, RC filter and V-score.
---

# kce: KiCad CLI Extended

Choose recipes from intent. Run R1 first.
[COMMANDS.md](COMMANDS.md) lists commands; info describe COMMAND explains flags.
[Details](https://github.com/Hybirdss/kicad-cli-extended/blob/main/docs/AGENT-RECIPES.md) expand
these chains. P means the project; replace path/to/project below.

## Rules

* Use --json --project P or work inside P. Millimetres; schematic Y down; 1.27 mm grid.
* Mutations auto-save with KiCad validation. Preview with --dry-run (isolated, returns
  dry_run/would_write). --read-only refuses writes/exports/control. Do not bypass guards.
* Stderr errors: {error,type,category,hint,details?}, validated by the error schema. Exits:
  input 2, design 3, validation 4, crash 5, timeout 6, environment 7, internal 1.
  Branch on category. [Detailed JSON contract](https://github.com/Hybirdss/kicad-cli-extended#json-output-contract).
* ERC/DRC are report-only by default. Gate with --fail-on error|warning; read stdout even
  on design/3. --baseline REPORT gates new findings. Never weaken rules to pass.
* Checkpoint each stage. Restore removes later files; excludes outputs/state/VCS. Keep plans,
  journals and independent oracles outside P, plan step inputs inside P before checkpointing.
  Use absolute project-local input paths from other working directories.
* run is atomic for project/history; exports stay inside P. Restore on later rejection.
  rolled_back:false/commit_state:unknown requires repair and recovery before retry;
  commit_state:unchanged means nothing was written. Rerun ConcurrentEdit (retryable:true).
* Never order, pay, upload or commit unless asked. Inspect images, orientation and pin 1.
* sch nets has stable ordering and nullable code. Compare pin sets. sch add --uuid preserves
  identity; pcb update --stable-uuids converges all symbol-linked footprints, existing too.

## Choose a scenario recipe

### R1: Orient a new session

Triggers: KiCad, Gerber, JLCPCB, my board, open this project, first PCB.

```bash
P="--json --project path/to/project"
kce --json info doctor
kce skill status
kce --json info commands --full
kce $P project info
kce --json info describe sch no-connect
kce --json errors
```

Verify doctor.ok/capabilities/warnings; missing tables need lib init-global-tables. Gate 3D with
info doctor --require step,render. Install KiCad 10 or set KCE_KICAD_CLI/KCE_PYTHON if unavailable.

### R2: Build a board from a specification

Triggers: make me a board, first PCB, netlist-first, intent.json, USB-C LED, ESP32/STM32.
Chain: pins/pads, project new, checkpoint initial, dry-run apply, run apply/annotate/verify/ERC,
preview, checkpoint schematic-ok, outline, sync, score.

```bash
S="--json --project sensor"
kce --json project new sensor --name sensor
kce $S --dry-run sch apply sensor/intent.json --power-flags
kce $S run schematic-stage.json
kce $S sch verify --expect sensor/intent.json --strict
kce $S pcb outline rect --at 100,100 --size 50,40
kce $S --dry-run pcb update --stable-uuids
kce $S pcb update --stable-uuids
```

Create sensor/intent.json first (info schema netlist-intent). Plan apply/annotate/verify/ERC;
require match:true, clean ERC, no missing footprints/unmatched pins. Repeat apply gives changes:0.
Intent supports no_connect/power_flags/remove. ECO: apply --patch, verify --subset --strict.
Add --check-lib-id/--check-uuid/--check-net-names for identity gates. Follow R6/R7.

### R3: Create a missing library part

Triggers: missing symbol, custom footprint, datasheet, QFN/BGA wizard, STEP model.
Chain: checkpoint before-part, search/show, datasheet, local libraries/tables, check/link-check,
apply/verify, sync mismatches, ERC/DRC.

```bash
kce --json lib sym search nfc eeprom --pins 8+ep
kce --json lib fp search DFN 2x2 --pads 9 --type smd
kce --json lib suggest-footprints Device:R --size 0603
kce $P lib sym new P/parts.kicad_sym Switch --pin '1:A:passive:left,2:B:passive:right' --footprint partsfp:Switch --add-to-table parts
kce $P lib fp new P/partsfp.pretty Switch --kind custom --pad '1:-1,0:1,1:smd' --pad '2:1,0:1,1:smd' --add-to-table partsfp
kce $P lib fp wizard qfn P/partsfp.pretty --name DFN --param Pads.nx=0 --param Pads.ny=4 --param Pads.pitch=0.5 --add-to-table partsfp
kce $P lib link-check parts:Switch partsfp:Switch
kce $P lib fp check partsfp:Switch
kce $P session history
```

Separate geometry examples, not vendor parts. EP counts as a pin; --size 0603 is imperial 1608.
Inspect pin/pad numbers, model_details.exists, coverage/unsupported[]. Use ${KIPRJMOD} tables.
Checks use conservative pad boxes/model existence, not STEP/IPC certification. External libraries
escape checkpoints. Attach models via lib fp model set FPID body.step --copy-into 3d.

### R4: Rehearse and accept a stage

Triggers: try this, rollback on failure, make it brighter, recover, show changes.
Chain: checkpoint, Preview dry-run plan, execute with expect, compare/preview diff, accept or restore.

```bash
kce $P session checkpoint before-change --immutable
kce $P --dry-run run stage.json
kce $P run stage.json
kce $P project compare checkpoint:before-change --geometry
kce $P preview diff --against checkpoint:before-change --recipe board
# On rejection:
kce $P session restore before-change
```

Example stage.json, with acceptance before commit:

```json
{"version":1,"steps":[{"args":["sch","set-value","R1","470"]},
 {"args":["sch","show","R1"],"expect":[{"path":"value","op":"eq","value":"470"}]},
 {"args":["check","erc","--fail-on","error"]}]}
```

Verify intended field/net changes and ERC/DRC, then checkpoint accepted --immutable or restore.
Predicates address dotted paths/array indices; missing paths fail with AcceptanceFailed/design/3.
session checkpoints lists hashes; undo/redo/history span processes. Save REPL edits first.

### R5: Make an ECO without disturbing routing

Triggers: ECO, rev B, second source, replace capacitor, add decoupling, regenerate outputs.
Pre-KiCad-10 project: run pcb upgrade and sch upgrade first (format_upgrade:true means a write
just rewrote an older file). Checkpoint pre-eco after capturing approved nets/footprints/score
and ERC/DRC baselines. Keep approved expected-eco.json inside P. Preview --dry-run run eco.json,
then run schematic setters/read-backs/sch verify --strict/ERC. Preview --dry-run pcb update
--lock-existing (no --stable-uuids on an existing board: it rewrites every UUID); review
removals/adoption, replaced[].pads_moved, tracks_ending_on_old_pads and unmatched_pins before
applying. Pad-moving swaps need review.

```bash
kce $P pcb place near C10 --to U2 --net VCC --max-dist 6 --rotation auto
kce $P pcb autoroute --refs C10 --grid auto
kce $P project compare checkpoint:pre-eco --geometry --allow C2,C10,net:VCC,net:GND --fail-on-unexpected
```

Verify unchanged positions/UUIDs/pad nets/tracks. Compare exits 4 on unexpected changes;
review coverage.excluded/allowed-ref diffs. Scoped edits preserve others/locks. Verify symbol-swap
connectivity before sync. R7 writes fresh outputs; restore pre-eco on regression.

### R6: Place, route and pour

Triggers: connector edge, decoupling near chip, route it, ground pour, DRC errors.
Chain: checkpoint pre-place, move/lock anchors, place near, score, bounded legalize, preview,
set actual rules/netclasses, route, zones/fill, connectivity, DRC, checkpoint accepted.

```bash
kce $P pcb score
kce $P --dry-run pcb legalize --strict --max-move 5
kce $P pcb legalize --strict --max-move 5
kce $P pcb autoroute --grid auto --skip-net GND
kce $P pcb zone add --net GND --layer F.Cu --layer B.Cu --pad-connection auto
```

Verify closed outline and zero courtyard_overlaps.count/outside_outline.count. Inspect fallback
geometry. HPWL/crossings/congestion are heuristics. Gate legalize unmoved[] empty. PlacementBlocked:
review blockers/radius; reason_code new_drc_violations lists the KiCad DRC errors the move would
add in new_violations, and nothing was saved. Autoroute takes width and via size from netclass and
board minimums; grid auto refines 0.25/0.15/0.1/0.05 mm. Read failed[] and warning. New DRC
errors, or lost_connections from a route that cuts a pour, exit 3 and save nothing. Zone auto is
solid SMD/thermal THT. Connector edges need manual move/lock.

### R7: Build a fabrication hand-off

Triggers: order PCB, send to fab, JLCPCB/PCBWay/OSH Park, assembly, BOM+CPL, Gerber.
Chain: verify intent, gate ERC/DRC, inspect manufacturer limits, parts/BOM check, fresh package,
review files/manifest/CPL orientation and hand off. Never pay or place an order automatically.

```bash
kce $P fab parts check --offline
kce $P fab bom-check --require MPN,LCSC,Footprint
kce $P fab package --preset jlcpcb --require-lcsc --manifest -o RELEASE
kce $P pcb export drill --output P/outputs/drill/
kce $P pcb export step --output P/outputs/board.step
```

Require complete:true, empty failed_steps, nonempty files[]/ZIP hashes. DRC errors refuse the
package (failed_steps [drc], drc.error_violations); never hand off with --allow-drc-errors. Failure is
complete:false/design/3, preserving accepted output. Use fresh directories. rules_preset:null
is not fab qualification. Review BOM/CPL/polarity/rotation in the fab viewer; --rotation-fix
changes CPL only. Jobset fab-template archives Gerber/drill. Passthrough files use outputs[].

### R8: Gate CI and tagged releases

Triggers: GitHub Actions, ERC/DRC on PRs, BOM/cost gate, build Gerbers on tag, jobset CI.
Chain: doctor, explicit check thresholds/baseline policy, compare base, preview diff, BOM gate,
revision gate, fresh fab package (refuses DRC errors), clean-tree assertion, artifact review.
Use README templates with fetch-depth: 0/reviewed pins; preserve stdout/stderr. Cost gate:
`fab bom-check --prices prices.csv --price-key LCSC --against git:HEAD --max-delta-pct 10`.
Unpriced fails. Release uses --require-rev/--manifest. Verify bad/clean go red/green.
jobset execute gates failed_jobs with design/3. Templates are not Windows execution evidence.

### R9: Search thousands of placement trials

Triggers: optimize placement, hypcb, warm worker, 5000 trials, keep/revert, deterministic replay.
Chain: strict intent/ERC/DRC baseline, immutable baseline/best-000000 checkpoint then best,
foreground serve, move/verify/score plan with expect, keeper DRC, immutable generation then best;
restore best on rejection. Journal/oracle outside P, step inputs inside. Keep --session-dir or
KCE_SESSION_DIR outside P consistently.

```bash
kce $P serve --request-timeout-ms 30000
```

Send one JSON-RPC object per line; wait for matching mutation ids:

```json
{"jsonrpc":"2.0","id":1,"method":"run","params":{"args":["pcb","info"],"timeout_ms":2000}}
{"jsonrpc":"2.0","id":2,"method":"run","params":{"args":["run","trial.json"]}}
{"jsonrpc":"2.0","id":3,"method":"shutdown"}
```

Verify meta.worker_reused, objective and gates. response.result holds the CLI value (arrays too).
Cancel method takes {request_id:2}; acknowledgement follows rollback/reaping. On lost transport
or unknown commit_state restore accepted bytes/nets/score before retry; inspect retryable.
Journal infrastructure failures separately from scores. --progress emits stderr JSON lines.
EOF/shutdown drains accepted requests. Close pipes and wait.

### R10: Intake a foreign board

Triggers: Altium/Eagle import, .PcbDoc/.brd, contractor design, migrate into KiCad.
Chain: source inventory, import to NEW, inspect read_back/source_unchanged/losses, checkpoint,
carry rules, DRC. Board import is not an editable schematic migration. Companion ace
(altium-cli-extended, GPL-3.0-or-later) inspects Altium; check its help. Verify independent
hashes/counts/nets/layers/lengths. Source-derived intent needs strict verify before
--dry-run pcb update --keep-extra/removal review. Self-consistency is not source equivalence.

### R11: Simulate before layout

Triggers: SPICE, ngspice, RC filter, corner frequency, transfer function.
Chain: scratch project, sim model, sim directive, sim netlist, sim run, inspect probes/CSV,
compare analytical result, then apply checked intent to the real project and follow R6.

```bash
kce $P sch label-pin C1:2 0 --kind global
kce $P sim model V1 --device V --type SIN --params 'dc=0 ampl=1 f=1k ac=1'
kce $P sim directive add '.ac dec 20 10 1meg'
kce $P sim netlist
kce $P sim run --probe 'v(/out)' --points 3
```

Verify node 0, ac=1, exact /probe names, warnings/errors and nonzero samples; compare RC corner
with 1/(2*pi*R*C). power:GND alone is not SPICE ground. Simulation does not replace ERC/DRC.

### R12: Route a high-speed block and panelize

Triggers: differential pair, USB/LVDS/MIPI/DDR, skew, length match, via fence, teardrop, panel.
Chain: checkpoint pre-hs, inspect stackup/netclasses/pairs, rules, route, shorter-leg tune,
fence, stitch, scoped teardrops, fill, DRC, length report, separate panel and panel DRC/package.

```bash
kce $P pcb diffpair rule /USB --gap 0.2 --gap-max 0.25 --max-skew 0.5
kce $P pcb diffpair route /USB --from U1 --to J1 --layer F.Cu
kce $P pcb length tune /USB_D- --match /USB_D+ --amplitude 1 --tolerance 0.02
kce $P pcb teardrops add --target vias --net /CLK
kce $P pcb panelize --rows 2 --cols 3 --mode vscore --spacing 0 --strict --drc -o panel/board-panel.kicad_pcb
```

Verify routed/skew/length DRC, via counts and unchanged source hash. V-score forces zero spacing;
--strict rejects conflicts. Independently review impedance/fab capability. Package panels with R7.

## Advanced

Use `preview capture`/`preview diff` for visual review and `preview live` while iterating:

```bash
kce $P preview live start --recipe board
kce $P preview live push
kce $P preview live stop
```

See COMMANDS.md for models/variants/graphics. Live gui needs IPC/kicad-python: save before disk
edits, then reload. sch move does not drag wires; prefer label-pin. Piped repl emits one JSON
line per command; session save before EOF. Archive --include-outputs preserves release outputs.

PowerShell uses arrays and its call operator:

```powershell
$KCE = '--json','-p','P'
& kce @KCE info doctor
```

Pass negative lists as --rotate=-45,0,45. Prefer plans to shell loops.
