---
name: mechanical-teardown
description: Reverse-engineers a physical product (power tool, appliance, consumer device, mechanism, vehicle part) as an engineering system — function structure, costed BOM, materials and processes, Boothroyd DFA index, should-cost, repairability, FMEA, design decisions worth copying, benchmark and redesign opportunities — and renders a print-ready HTML teardown report. Use when the user says "tear down", "teardown", "reverse engineer", "how is this made", "what would this cost to make", "why is this designed this way", or shares photos of a disassembled product or an exploded view.
---

# Mechanical Teardown

A teardown explains why a product is built the way it is, what it costs to make, and what the next
design should change. Treat the product as a system. Start from what it must do. Use every part to
explain a decision, and back every number with an observation or a stated estimate.

## Workflow
1. **Frame it.** Pin down the product (make, model, price, year) and why the user wants the teardown:
   competitive benchmark, cost-down, design for repair, learning, or patent and design-around work.
   The purpose decides which sections get the most depth. Note the annual volume. If it is unknown,
   assume one and say so, because tooling amortisation depends on it.
2. **Gather evidence, in this order of trust.**
   1. The user's own disassembly: photos of each layer, kitchen-scale masses, caliper readings.
   2. Exploded parts diagrams and service manuals, which give part names and counts.
   3. Regulatory internal photos (FCC ID for anything with a radio) and patents (claims explain intent).
   4. Published teardowns and repair guides.
   5. Your own engineering judgement, labelled as an estimate.

   Follow `references/teardown_protocol.md` for what to photograph and measure at each layer. Never
   invent part counts you cannot support. When a section is hidden, say "not inspected".
3. **Function structure and requirements.** Write 4–8 user needs as measurable engineering metrics,
   and say how the design meets each one. Then build a function tree (store/convert/transmit/control/
   protect...) and map every part to a function. A part that maps to no function is a finding.
4. **Fill the spec.** Run `python scripts/teardown.py template > spec.json`. For each part record id,
   name, qty, subassembly, kind (part / fastener / label / process, e.g. lubrication or regulation), material, process, mass_g, and either
   cost_usd (quote, catalogue price, or a purchased-part estimate) or the process inputs (cycle_s,
   cavities, tooling_usd). Then record the DFA fields:
   - handling: `easy | orient | small | flexible | heavy`
   - insertion: `drop_in | align | snap | hold_down | press | screw | rivet | connector | solder | adhesive | weld | wire_route`
   - the three Boothroyd questions: `moves`, `different_material`, `separate_for_service`

   Mark the parts that wear out or fail as `wear_part`, with `depth` (how many parts must come off
   first). If a step takes a known time (regulation, a measured operation), set `time_s` per item
   instead. Times and tables are in `references/dfa_times.md`; cost data is in `references/should_cost.md`.
5. **Compute.** Run `python scripts/teardown.py analyze spec.json`. Read the output critically:
   - **DFA index.** Under 10 % is poor, 20–30 % is typical of good consumer products, and over 40 %
     is excellent.
   - **Elimination candidates.** Check every part that fails the minimum-part test. Each one is a
     possible consolidation, unless a reason outside the test applies (cost, tolerance, supply).
   - **Cost Pareto.** A handful of parts usually make 80 % of the cost; focus the cost discussion there.
   - **Assumptions.** Every default the calculator applied is listed. Replace the ones that matter.
6. **Judge.** Fill these sections of the spec:
   - `design_signals`: 3–6 specific decisions worth copying, each with evidence and the trade-off it
     makes. This is the most valuable section, so make it concrete ("clutch ramps molded into the
     ring-gear face", not "clever design").
   - `fmea`: S/O/D on 1–10, with an action for every High-priority row.
   - `benchmark`: 2–4 real or typical rivals on 4–6 measurable dimensions.
   - `opportunities`: each a specific change, its impact, its effort, and the saving per unit
     (negative if it adds cost).
   - `verdict`: 3–4 sentences covering where it wins, where it leaks, and what the next design should do.
7. **Report.** Run `python scripts/teardown.py report spec.json -o <product>_teardown.html`. Add teardown
   photos under `images`; they are embedded in the file, so it stays one self-contained page that
   prints cleanly to PDF. Publish it as an artifact or send the file. In chat, give the five headline
   numbers and the verdict. Do not repeat the report.

## Principles
- **Function first, parts second.** List parts only to explain how a function is delivered.
- **Numbers with provenance.** Every mass and cost is measured, quoted, or estimated, and the report
  says which. Should-cost is for ranking and comparison, not a quote.
- **Name the trade-off.** Every design decision costs something, such as repairability, noise, tooling
  or tolerance. Say what was paid for it.
- **Specific opportunities only.** "Replace 4 solder joints with a keyed connector: −30 s assembly,
  motor swap in 2 min" is an opportunity. "Improve repairability" is not.
- **Respect IP and safety.** Reverse engineering for analysis is fine. Do not help copy trade dress or
  bypass safety interlocks. Warn before opening capacitors, lithium packs, mains-powered devices, or
  springs under preload.

## Related skills
`dfm-review` (rule-level DFM on one part), `design-review-package` (full FMEA and BOM for your own
design), `material-selection` (alternatives for a part the teardown flags), `machine-element-sizing`
(check a gear, spring or bearing you measured), `tolerance-stackup` (a fit you suspect is marginal).

## Examples
- `examples/cordless_drill.json`: a generic 18 V drill/driver (clamshell, planetary gearbox,
  slip clutch). [Report](https://baratilab.github.io/mechanical-engineering-skills/examples/mechanical-teardown-drill.html).
- `examples/automatic_watch.json`: a generic automatic diver's watch with the movement torn down
  (gear train checked by calculation, pawl-lever winding, lever escapement, keyless works,
  process steps such as lubrication and regulation with `time_s`). Its exploded view and gear-train
  figures are drawn by `examples/make_watch_figures.py` and embedded through `images`.
  [Report](https://baratilab.github.io/mechanical-engineering-skills/examples/mechanical-teardown-watch.html).

Both are illustrative: the structure and mechanics are right, and the masses and costs are labelled
estimates. Run the tests with `python tests/test_teardown.py`.

## Credits
The idea of a fixed-spine teardown that ends in a printable HTML report comes from
[yanliudesign/product-teardown-skill](https://github.com/yanliudesign/product-teardown-skill), which
does product-strategy teardowns of software. This skill is an independent mechanical-engineering
counterpart, with its own method, calculator and report.
