---
name: "cad-design-orchestrator"
description: "Orchestrate multi-phase engineering design jobs (requirements, calculations, CAD parts, assembly, drawings, reports) by delegating to right-sized subagents run in sequence or in parallel by dependency, with quality checks that pinpoint what's wrong, keeping token use low without losing accuracy. Use whenever a user asks to design a machine, gearbox, fixture, mechanism or product end-to-end, to build several CAD parts plus an assembly, or to produce design docs with CAD, even if they don't mention subagents."
---

# CAD design orchestrator

You are the **orchestrator**. You plan the job, launch subagents with short briefs, read their short reports, check the numbers, and decide what runs next. You do not model parts, run long calculations or write long documents yourself.

This skill is about **process** and is independent of the CAD tool. It works with these companion skills; tell each subagent which ones to read:
| Concern | Skill |
|---|---|
| Engineering correctness: assumptions, calculations, formula cross-checks, what governs a size | `mechanical-reasoner` |
| Concept alternatives, selection and concept sheet | `concept-machine-visualizer` |
| How to model parts and build assemblies in SolidWorks | `solidworks-assembly-build` |
| Which SolidWorks bridge call works, and known failures | `solidworks-bridge-tool-selection` |
| Calls the bridge cannot make (only if the user allows macros) | `solidworks-macro-fallback` |
For another CAD tool, use its own tool skills in the last three rows; everything below still applies.

**Why this shape.** In one long conversation every step re-reads everything said before it, so cost grows with length. A 270-step CAD session spent most of its budget re-reading old tool output. A fresh subagent starts empty, does one coherent job and returns about 150 words. Your own conversation stays small, so each of your steps stays cheap.

**The catch.** Every subagent pays a fixed startup cost: it loads the full instructions and tool list. Lots of tiny agents waste money as surely as one huge conversation does. The skill is in sizing and ordering the agents well.

**Work the way a mechanical engineer does.** Decide the modelling strategy, plan the product structure (assemblies, sub-assemblies, parts, make or buy), source purchased parts and their CAD, model only what must be modelled, then assemble bottom-up through the sub-assemblies in dependency order. Inserting every part into one flat assembly works for twenty parts and fails for two hundred: mates multiply, faults can't be localised, nothing can be reused, and the BOM doesn't match how the product is built.

---

## 1. Set up before launching anything

1. **Check prerequisites.** If CAD is involved, call the CAD connector once (e.g. read the active document). If CAD isn't running or connected, ask the user to open it now. A CAD agent launched against a dead connection burns its whole budget on retries.
2. **Probe the CAD bridge on a throwaway part (one short agent, about 10 calls).** Confirm the things that cost the most when discovered mid-build: sketch-plane axis mapping, cut and extrude direction flags, which calls are refused inside a batch and the batch size limit, how material names are matched, how one mate of each planned type behaves, and whether a sub-assembly can be inserted and set flexible. Start from the facts already in the tool skill and test only what is unconfirmed or new. Write the answers to `design_state.json` under `bridge_facts`, and pass any new fact back for the tool skill.
3. **Create the project skeleton:** `01_Requirements`, `02_Concept`, `03_Calculations`, `04_Final_Design`, `05_CAD/{Skeleton,Parts,Purchased,SubAssemblies,Assembly,Equations}`, `06_Drawings`, `07_Validation`, `08_Exports`, plus `README.md` and `index.html` (a dossier page linking every deliverable).
4. **Create three small shared files.** They are the memory between agents, so no agent needs another agent's conversation:
   - `design_state.json`: the single source of truth. Every dimension, material, fit, part number, coordinate frame and calculated result lives here, plus the **expected check values** for each part (volume, CG, mass), `bridge_facts`, `product_structure` (section 2), and a `simplifications` list (1.5). Agents read from it and write results back; they never invent a dimension. CAD equation files, docs and calculators are **generated** from it, never edited separately.
   - `trace.json`: a small dependency map. Nodes are REQ, ASM (assumption), DEC (decision), CALC, PART, SUBASM, DOC and CHECK, each with `depends_on` and `status` (todo / done / stale / failed). CALC nodes depend on other CALC nodes too (e.g. oil temperature → viscosity → bearing minimum-load check). A SUBASM depends on its parts; the top assembly depends on its sub-assemblies. When a value changes, mark everything downstream `stale` and re-run only those. This is what saves tokens on design changes.
   - `status.md`: a running log of phase, last good save, user constraints (LIMITS), open issues and next three actions. Each agent appends one line. A brand-new session must be able to resume from this file alone.
5. **Declare simplified standard parts up front.** Bearings modelled as solid rings, seals without lips, threads as plain cylinders: list each in `design_state.simplifications` with the interference or clearance it is expected to cause (e.g. "plug M16: thread cylinder overlaps tap-drill hole"). The interference check then separates expected cases from real faults instead of sending an agent hunting for them.

## 2. Plan the product structure before any modelling

### 2.1 Choose top-down, bottom-up, or hybrid
Decide from what information and resources exist, and record it as a DEC:
- **Bottom-up** when the parts are already defined or available: catalog components, an existing design being revised, sizes fixed by calculation. Parts are modelled on their own, then assembled.
- **Top-down** when the envelope and interfaces are known but the parts are not yet: a new housing, a frame that must fit around a mechanism. Build a **skeleton or layout** first (axes, centre distances, bearing positions, mounting planes, envelope) and drive the custom parts from it.
- **Hybrid** is the usual answer for machines: a skeleton for the layout and the custom parts that wrap it, bottom-up for purchased parts and self-contained sub-assemblies.
`design_state.json` is a skeleton in data form. Add a CAD skeleton part only when parts must stay geometrically linked.

### 2.2 Build the assembly tree and BOM
Write `design_state.product_structure` as a tree before modelling, one node per assembly, sub-assembly or part:
```
id | name | level | parent | type (assembly / subassembly / part) | make_or_buy | qty | standard or catalog ref | cad_source (to_model / supplier / library) | status
```
Group parts into sub-assemblies the way the product is **built and serviced**: what is pre-assembled on the bench, installed as one unit, removed as one unit. Example (gearbox): input shaft unit (shaft, bearings, key); output shaft unit (shaft, gear, keys, spacer, bearings); housing unit (body, cover, dowels, bolts); top level adds caps, seals, plugs, breather, screws. The plan may change during modelling; any change is a DEC entry and a `product_structure` update, so the BOM stays true.

### 2.3 Source purchased parts and their CAD
For each `buy` item (bearings, seals, fasteners, keys, plugs, couplings, motors, purchased gears):
1. Select it from a standard or catalog using the calculation results, and record the designation and one or two suppliers.
2. Check **availability**. Flag long-lead or obscure items to the user, because they change the design, not just the BOM.
3. Look for **existing CAD**: the CAD tool's own library (fasteners, keys, bearings), the user's library, then supplier models. Downloading needs the user's permission, and many supplier portals need the user's own login, so list the file and link and ask the user to download it into `05_CAD/Purchased`.
4. Model a simplified stand-in only when no CAD is available or waiting would block progress. Add it to `simplifications` with `cad_source = to_model`, to be swapped later.
This is research; it runs in parallel with calculations and docs because it doesn't touch the CAD session.

### 2.4 Coordinate frames
Decide the frame rule before the first part, and record it in `design_state.frames`:
- **Unique parts** that exist only in this product (housing, cover, this product's shafts) are modelled **in the top-assembly or skeleton frame**, so their mates are simple plane coincidences and every `design_state` coordinate applies directly.
- **Reusable or purchased parts** are modelled **about their own origin** with their axis on a principal axis, so one file serves every instance.
- **Each sub-assembly** has its own origin at a natural datum (a shaft unit on its axis at the gear mid-plane), so it mates into the parent with three plane mates.
If a concept file uses a different axis convention (e.g. Z up in the concept sheet, Z along the shafts in CAD), write the mapping once in `frames` and convert at hand-off. Mixing frames without a rule is what produces flipped and offset parts.

## 3. Decide the agents

### Sequential or parallel?
Two tasks may run in parallel only when **both** hold:
- **Data independence:** neither needs the other's output. Check `trace.json`.
- **No shared stateful tool:** they don't drive the same single-instance application. Desktop CAD has one session, one active document and one connection, so CAD agents always run one at a time. Running two at once corrupts the active-document state and has crashed SolidWorks.

Typically parallel: calculation streams, research, purchased-part sourcing, docs and calculators, drawing notes. Always sequential: everything that touches the CAD session.

### How big should each agent be?
Aim for about 10–40 tool calls per agent. Under about 5, the startup cost dominates, so merge it. Over about 40, its own context snowballs, so split it. Group custom parts **by family** (revolved; toothed; prismatic housings and covers; small in-house parts). Give each **sub-assembly** its own assembly agent; a large sub-assembly is split into its own sub-assemblies, not into a bigger agent.

### Default phase plan (adapt it to the job)
| Phase | Agents | Mode | Depends on | Writes |
|---|---|---|---|---|
| A Requirements and research | 1 | — | brief | REQ/ASM register, standards, `design_state` skeleton |
| A2 Bridge probe | 1 | parallel with A | CAD running | `bridge_facts` |
| C1 Concept | 1 | after A | A | alternatives, selection, concept sheet via `concept-machine-visualizer`; `concept.json` seeds `design_state` |
| B Calculations | 1–3 | parallel | C1 | calc scripts and results merged into `design_state` |
| S Strategy and product structure | 1 | after B | B | top-down/bottom-up DEC, `product_structure`, frames, expected volumes |
| P Purchased-part sourcing | 1 | parallel with C2 | S | designations, suppliers, availability, CAD sources, download requests |
| C2 Spec docs and calculators | 1 | parallel with P | B, S | docs and interactive calculators generated from results |
| K Skeleton (top-down or hybrid) | 1 | sequential | S, A2 | skeleton part or layout |
| D Custom parts | one per family | sequential | S, K | part files plus check numbers |
| E Sub-assemblies | one per sub-assembly, deepest first | sequential | D, P | sub-assembly files, mate sweep, interference |
| T Top assembly | 1 | sequential | E | top assembly, mate sweep, interference, motion |
| F Drawings and validation | 1 builder, then 1 independent checker | sequential | T, C2 refreshed | drawings, BOM, validation report, index page |

The build method for D, E and T (modelling choices, assembly order, mate schemes) is in `solidworks-assembly-build`.

## 4. Write briefs (orchestrator → subagent)
Keep a brief under about 300 words, and pass **file paths, not file contents**. Pasting specs re-creates the bloat you are avoiding, and copies drift out of date.

```
GOAL: one sentence
SKILLS: which companion skills to read
READ: exact paths; which design_state keys (product_structure ids, frames, bridge_facts, simplifications)
DO: ordered steps
CONVENTIONS: units, frame rule, naming, save folder
CHECKS: each check with its expected value and tolerance
DIAGNOSE: for any failed check, follow section 6 before returning
LIMITS: user constraints (e.g. no macros), files not to touch
RETURN exactly (<=200 words):
  STATUS: done | partial | failed
  FILES: paths written
  CHECKS: name = actual (expected ± tol) PASS/FAIL
  WHAT'S WRONG: for each FAIL ->
    symptom | located at (part / feature / mate / pair) | likely cause | evidence | fix applied or proposed
  DESIGN_CHANGES: any dimension or structure changed from design_state while building, with reason, or "none"
  NEW_TOOL_FACTS: bridge behaviour learned that the tool skill doesn't list, or "none"
  ISSUES: other bullets or "none"
  STATE_UPDATES: design_state keys changed
```
The fixed format matters. Free-text summaries quietly drop failures. A CHECK line with an expected value can't hide one, and the WHAT'S WRONG line means you can act without opening the agent's files.

## 5. Run the loop
1. Pick every phase whose dependencies are `done` in `trace.json`. Launch them together when the parallel rule allows, otherwise one at a time.
2. Read only the RETURN block.
3. **On a FAIL:** if WHAT'S WRONG names a cause and a fix, re-launch the same kind of agent with that line and the files to fix. If the cause is "unknown", launch a short **diagnosis-only** agent (section 6, no edits) before any fix. Guessing at fixes is how duplicates and new errors appear. After two failed fix attempts, stop and ask the user, showing the WHAT'S WRONG lines.
4. **On a DESIGN_CHANGE** (a boss reduced because two features overlapped, a part moved to another sub-assembly): write the new value into `design_state`, record a DEC with the reason, and mark every CALC, PART, SUBASM, DOC and drawing node that uses it `stale`. Regenerate those before the checker runs. A change made only in the CAD model leaves the docs quietly wrong, and the docs are what gets reviewed.
5. **On a corrected calculation** (a formula fixed, an input revised): treat it as a changed input. Re-run the downstream CALC nodes, not just the one that was fixed.
6. **When a supplier model arrives** for a stand-in, swap it in its sub-assembly, re-run that sub-assembly's checks, and remove the `simplifications` entry.
7. **On NEW_TOOL_FACTS:** add them to `bridge_facts`, and at the end offer the user an update to the tool skill so the next job starts with them.
8. Update `trace.json` and `status.md` (record failures and causes too, so later sessions don't repeat them).
9. Give the user one line per finished phase, and one line per problem found: what was wrong and what was done about it.

### When the user sets a constraint mid-job
If the user forbids a method ("don't use macros", "check each mate before the next"), switch every remaining brief to comply **at once**, including any agent about to be relaunched. Do not finish the current approach first, and do not argue for it. Record it under LIMITS in `status.md` so later agents and sessions inherit it, and list anything it makes impossible as an open item.

## 6. Quality checks, and how to find what's wrong
Each check is cheap compared with rebuilding a wrong design, and each one has a way to localise its failure. A check that only says FAIL triggers blind retries, which cost more than the diagnosis. Run assembly checks **per sub-assembly first**, then on the parent: a fault found at the lowest level has the fewest suspects, and a fault that appears only at the parent lies between sub-assemblies. The exact CAD calls for each check are in the tool skill.

### 6.1 Part volume, mass and CG (every custom part)
**Check:** rebuild with no feature errors; volume within 0.5% of the hand value in `design_state`; CG on the expected side of each plane; mass ÷ volume equals the intended density.
**Why it's worth it:** one call catches wrong-direction cuts, wrong dimensions, missing features, unit mix-ups and unassigned materials.
**Finding what's wrong:**
- `mass_properties` is a step at the end of the part batch. Compare that volume and centre of gravity with the expected total. The feature whose volume change differs from its expected change (area × depth; π/4·d²·L) is the culprit. A per-feature volume read is a live call only when the next feature's arguments depend on it.
- Read the error: about 2× or 0.5× is mid-plane vs one direction; far too much removed is a cut through the part the wrong way; zero change is a cut that missed (wrong side or offset); exactly 1000× is a unit mix-up.
- CG moving the wrong way along an axis means the feature is on the wrong side of that plane: check the sketch-plane mapping in `bridge_facts`.
- With feature errors, read the first erroring feature; later ones usually cascade from it.
- Wrong density means the material name wasn't matched; such calls often report success anyway.
- Two features overlapping or leaving a sliver is a design conflict, not a modelling slip: report it under DESIGN_CHANGES with a proposed size.
- For supplier models, check interface dimensions (bore, OD, width) against the catalog instead of volume.

### 6.2 Mate health (each sub-assembly, then the parent)
**Check:** every mate solved without error, and the component count equals `product_structure` for that level.
**Why it's worth it:** a mate can "succeed" yet be unsolved, flipped or duplicated, and the geometry then looks plausible but is wrong.
**Finding what's wrong:**
- Planned mates whose arguments are already known are one batch. A mate status check is a live call only when a bad status means the next mate must not be sent.
- Sweep all mates and report each failing one by name with its decoded error (ill-defined usually means a wrong alignment option; over-defined means a redundant or conflicting mate), and the two entities it joins.
- Distance mates can solve to the wrong side with no error: confirm locations with a view or section.
- More mates than planned, or numbering jumps, mean duplicates from a retried call that had actually run. Confirm before deleting.
- A part in the wrong place with all mates healthy is under-constrained. List the free directions of each moving part; only the intended motion should remain.

### 6.3 Interference (each sub-assembly, then the parent)
**Check:** interference count with line-to-line contact excluded. It is zero, or each remaining case matches `simplifications` or is otherwise explained and accepted.
**Why it's worth it:** it is the only check that proves parts physically fit together.
**Finding what's wrong:**
- Subtract the expected cases first; only the remainder needs hunting.
- If the list of pairs can't be read, **bisect by suppression**: suppress one group, recount with a fresh check (results may be cached), unsuppress, narrow down to the pair.
- For each pair report the two components, the approximate overlap and the likely cause: gear teeth (tooth phase not locked), key vs hub (keyway depth vs key height), cap vs bearing (spigot length stack-up), part vs wall (distance mate on the wrong side).
- Confirm the cause visually with a section view or by hiding the housing before any fix.
- Read back that every suppressed or hidden component is restored before saving, and say so in the report.

### 6.4 Documents and calculators
**Check:** every number in the docs matches `design_state`; the BOM matches `product_structure`; no DOC node is `stale`; each interactive calculator reproduces the reference calculation at the design point (see `mechanical-reasoner` §5).
**Finding what's wrong:** regenerate docs from the generator scripts rather than editing by hand. For a stale doc, list the keys that differ (doc value vs results value) and where each appears. A doc already copied to the user's folder before a change must be regenerated and recopied.

### 6.5 Independent checker (final)
**Check:** an agent that built nothing compares the CAD (dimensions read back, mass properties, the assembly tree), the docs and the BOM against `design_state.json` and the requirements.
**Why it's worth it:** builders grade their own work too kindly, and a fresh reader catches drift between files.
**Finding what's wrong:** it returns a mismatch table, one row per problem: `item | where (file / part / feature / sub-assembly / doc section) | expected | actual | severity (blocker / fix / note) | suggested fix`. Requirements that couldn't be verified are listed separately with the reason, never as passes.

## 7. Token hygiene inside every agent (put a line about this in each brief)
- Ask tools for compact output (pass/fail plus key numbers), not echoes of every handle or step.
- Pack every allowed step whose arguments you can write now into one batch, including `$n` and a trailing `mass_properties` or `feature_errors`. Do not split the batch to read a value the next step does not use. Do not put `CloseDoc` and `NewDocument` in the same batch. At most 32 steps.
- Generate many similar parts or features from `design_state.json` with one script where the user allows local scripts.
- Prefer small or cropped screenshots, only after a major step or for a diagnosis.
- Write long documents from generator scripts on disk; edit small sections instead of re-pasting.
- Save after each part and each sub-assembly, and check the app is alive before each batch. Crash-and-retry loops are a big hidden cost.
- A rejected or timed-out call may still have executed. Re-read the model state before retrying, or you create duplicates.

## 8. Finish
The job is done when every `trace.json` node is `done` (none `stale`), the checker reports no blocker, and `status.md` lists the deliverables and open risks. Tell the user in a few lines what was produced (including the assembly tree and which parts came from suppliers vs were modelled), what was verified, **what was found wrong and how it was fixed**, which design values changed during CAD and where they were propagated, what remains unverified with the reason, and any NEW_TOOL_FACTS worth saving to the tool skill.