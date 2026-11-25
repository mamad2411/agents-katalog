---
name: "mechanical-reasoner"
description: "Engineering reasoning loop for mechanical and machine design, from requirements through calculation, CAD and validation. Use whenever the user asks to size, select or check a mechanical part or drive (shaft, beam, bracket, frame, plate, pulley, bearing, gearmotor, belt, conveyor, fixture, bolted joint), choose a material, section or architecture, asks \"will this hold\", \"what motor do I need\", \"how thick should this be\", wants a part or assembly modeled in SolidWorks or other CAD from engineering requirements, or reports a failed check, FEA result, interference, slip, overheating, deflection or breakage that needs diagnosing. Use it even when the request sounds like a quick sizing question."
---

# Mechanical reasoner

Treat the job as a closed loop:

requirements -> evidence -> hypotheses -> constraints -> calculations -> design decision -> CAD or physical realization -> validation -> diagnosis -> revision

Six roles stay separate, because mixing them is how confident-sounding but wrong designs get made. Reasoning decides what to investigate, compare, change, or test. Rules decide what is allowed or forbidden. Calculators and solvers establish mathematical or physical consequences. The dependency model tracks what changes when an input changes. CAD and execution tools realize the design. Validation decides whether the realized design satisfies the intent.

Fluent reasoning is not engineering proof. When equations, standards, catalog data, material properties, or safety-critical values matter, use authoritative data or a deterministic calculation, and mark every assumption.

This skill owns **engineering correctness**. For a multi-part job with CAD and documents, `cad-design-orchestrator` owns the process (agents, shared files, checks); for concept alternatives use `concept-machine-visualizer`; for SolidWorks modelling use `solidworks-assembly-build` and `solidworks-bridge-tool-selection`.

## 1. Normalize

Write the engineering state before designing.

- Objective and machine or function
- Loads, speeds, duty cycle, throughput, life, environment
- Product or workpiece geometry and mass
- Envelope and interfaces
- Materials and process constraints
- Commercial or manufacturing constraints
- Safety factors or governing standards when known
- Unknowns and assumptions

Tag each value: **given** (the user said it), **assumed** (you chose it to proceed; say why and how sensitive the answer is to it), **derived** (calculated from others), **selected** (a catalog or standard choice), or **validated** (checked against the realized design).

If a missing value would change the answer by more than a standard size step, or is safety-critical, ask for it. Otherwise assume a stated, typical value, flag it, and carry on, so the user gets a usable answer and knows which number to confirm.

## 2. Choose the mode

Use the smallest set that fits this step.

- Abduction: a requirement or an observation needs a concept, cause, or architecture.
- Constraint reasoning: hard limits remove infeasible options.
- Deduction: a rule plus this case forces a result.
- Causal reasoning: name what depends on what, and how a change propagates.
- Counterfactual reasoning: change one input, recalculate the affected nodes, compare.
- Induction: a reusable pattern from many validated examples. One case is not a law.
- Analogy: reuse a similar solution only after naming where the analogy breaks.
- Probabilistic reasoning: rank diagnoses or choices while evidence is incomplete. Confidence stays below 1.

A first principle (equilibrium, conservation, compatibility, units that close) may be a rule in a deduction. A catalog rating, code allowable, or shop habit is an adopted premise. Say which it is.

## 3. Make the conclusion executable

An important conclusion is not left as prose. Turn it into one or more of: a deterministic equation, a Boolean constraint, a scoring rule, a dependency edge, a hypothesis with the evidence that would confirm it, a validation criterion, or a CAD intent operation.

Every input the result needs must appear in `inputs`; otherwise someone checking the record cannot reproduce it. Example:

```json
{"reasoning_type":"deduction",
 "claim":"Drive torque must be recalculated",
 "because":["Throughput increased","Belt speed changed"],
 "inputs":{"drive_force_N":410,"belt_speed_mps":0.22,"pulley_diameter_m":0.15},
 "rule":"P = F*v; omega = v/r; T = F*r",
 "result_source":"deterministic_calculator",
 "result":{"power_W":90.2,"pulley_rpm":28.0,"pulley_torque_Nm":30.75},
 "confidence":1.0}
```

Confidence is 1 only for a deterministic result from stated inputs, and it describes the arithmetic, not the inputs. If an input is assumed, the conclusion that rests on it inherits that uncertainty. Heuristic, catalog, empirical, and uncertain results stay below 1.

## 4. Screen concepts

When the architecture is not obvious, produce more than one concept before committing. For each: why it could satisfy the function, then hard constraints, then calculations, then soft preferences. Keep a rejected concept with a one-line reason. A concept that breaks a hard constraint is out. When a visual concept sheet or a hand-off to CAD is needed, do this with `concept-machine-visualizer`, whose `concept.json` then seeds the design state.

## 5. Calculate

Do not do critical arithmetic in your head. Run it. The bundled calculator covers the common cases and prints a JSON record with inputs, formula, result and validity range:

```
python <skill-dir>/scripts/mech_calc.py list
python <skill-dir>/scripts/mech_calc.py drive --force_N 410 --speed_mps 0.22 --pulley_d_m 0.15 --motor_rpm 1450 --efficiency 0.9
```

Commands: `drive` (power, rpm, torque, gear ratio), `conveyor_force`, `shaft_diameter`, `shaft_stress`, `shaft_twist`, `beam` (four standard cases, rectangle/round/custom section), `bearing_life`, `equivalent_load`, `inertia_torque`, `linear_inertia`, `bolt_preload`, `tipping`, `units`. All inputs are SI. The script refuses to default friction coefficients, nut factors, bearing X/Y factors or allowables, because those are exactly the numbers that must come from a source.

For anything it does not cover (gear rating to ISO 6336 or AGMA, thermal balance, fatigue to a specific method), write a short Python calculation, or use FEA, a solver, or a trusted engineering service when one is available. An equation whose units do not close is dropped.

Store inputs and units, the formula or model, assumptions, the result, the safety factor or margin, and the validity range of the model. Do not invent a missing material property, friction coefficient, service factor, catalog limit, or allowable stress. When you must use a typical handbook value to proceed, label it assumed and name its usual range. Rerun the calculation at the unfavorable end of that range only for the one or two assumptions that decide the selection (a motor size step, a shaft size step, pass or fail); for the rest, the label is enough. Sweeping every assumption multiplies the work without changing the answer.

### Cross-check formulas before trusting them
A script runs a formula exactly as typed, including a typo. Units closing does not catch a missing factor of ½ or a wrong exponent. Before a hand-coded standard formula feeds a decision:
- Compare its output with a published reference value for one known case: a chart reading, a worked example in the standard or a textbook, or a catalog figure. Record the reference and the agreement.
- Check each intermediate factor against its usual range (examples: a gear tooth form factor YFa is roughly 2–3.5; a face-load factor roughly 1.0–2.0; one gear mesh's efficiency roughly 0.97–0.99; a shaft stress-concentration factor at a shoulder roughly 1.3–2.5). A value outside its usual range is a formula error until shown otherwise.
- Feed values consistent with the operating state. A property taken at the wrong condition (oil viscosity at 40 °C instead of at the calculated operating temperature) is the same kind of error as a wrong formula.
If no reference is available, say so and keep the result's confidence below 1.

### A second implementation must agree with the first
An interactive calculator, spreadsheet or report formula that re-implements a calculation is a second copy that can disagree. Run it at the design point and at one other point and confirm it matches the reference calculation to rounding before publishing it.

### Say what governs each size
Most sizes in a compact machine are set by something other than strength: a bearing bore that must fit a standard shaft, a seal size, a coupling interface, a minimum casting wall, stiffness or deflection limits, gear geometry, or a standard size step. When a check shows a very large margin (a safety factor of 5 or 12 where 1.5 is required), state what actually governs the size and why the margin cannot be traded away, instead of leaving the reader to suspect an over-design or an error. When a size is governed by strength, say so too, because that is the one to revisit if loads change.

## 6. Track dependencies

Write the edges, for example:

Throughput -> BeltSpeed -> PulleyRPM -> GearRatio

ProductMass -> TotalLoad -> BeltTension -> PulleyTorque -> ShaftDiameter -> BearingLoad

PowerLoss -> OilTemperature -> OperatingViscosity -> BearingMinimumLoad, LubricationFilm

When a parameter changes: find the downstream parameters, invalidate stale derived values, recalculate that subgraph, and rerun the validations that those nodes feed. Say explicitly which earlier numbers are now stale, so the user does not reuse them. (In an orchestrated job these edges live in `trace.json`.)

This applies to **corrected results** as much as to changed requirements: when a formula is fixed or an input revised mid-job, everything computed from the old value is stale, including documents, calculators and CAD sizes. It also applies to a dimension changed during CAD (to clear a feature clash, to hit a standard size): write it back into the design state, record the reason, and rerun what uses it.

## 7. CAD intent

Target this path: engineering requirement -> validated design state -> geometry intent -> CAD operations. Model after the numbers are settled; geometry built on unvalidated sizes gets rebuilt.

Use the highest-level tool that actually exists in this session, and check the tool list rather than assuming a tool by its name: engineering primitives if a connector provides them, then named modelling tools, then raw API calls only when nothing named covers the intent. For SolidWorks, the modelling method is in `solidworks-assembly-build` and the working calls and known failures are in `solidworks-bridge-tool-selection`.

Write geometry intent so that it can be checked: each part's expected volume and mass from the design state, each feature tied to one design intent, and each interface (bore, fit, mating face) named, so validation can compare the realized model with the intent.

## 8. Validate

Check the engineering claim and the realized CAD state. Cover the items that apply: stress, deflection, fatigue margin, motor and gearbox service factor, shaft torque and bending, bearing life and load, speed and acceleration, stability, friction, slip, tipping, clearances and interferences, mates, manufacturability and standard sizes, envelope and interfaces, BOM availability.

Read evidence back from the model rather than trusting what you asked it to build: feature errors after rebuild, mass properties against the design state, interference for assemblies, realized dimensions, a view or section to look at it, and the BOM against the intended parts list. (`cad-design-orchestrator` §6 says how to localise each failure.)

A successful rebuild is not engineering validation. It shows the geometry exists, not that it carries the load. Where a validation cannot be performed with the tools at hand (motion, thermal test, FEA), say so instead of implying it passed.

## 9. Diagnose

When validation fails, or the user reports a failure:

1. List plausible causes, at least two.
2. For each, predict the evidence it would produce (fracture location and surface, timing, temperature, noise, which load case).
3. Ask for or run the cheapest high-information test first.
4. Update confidence (below 1) as evidence arrives.
5. Make the smallest justified change.
6. Rerun every check the change invalidated (section 6).

Do not jump from symptom to fix. "It broke, make it thicker" can hide a fatigue, alignment or stress-concentration cause that thickness will not cure.

## 10. Learn

Promote a reusable rule only from a validated outcome. Record its kind (first-principles law, standard or catalog rule, company rule, empirical heuristic, or learned pattern), its source population, its scope, and its confidence. An unvalidated generated design does not become a rule or a procedure skill.

## Decision record

Close substantial work with this record:

1. Problem and requirements
2. Knowns, unknowns, assumptions
3. Reasoning modes used
4. Candidate hypotheses or concepts
5. Hard constraints
6. Calculations and derived values, with the reference each critical formula was cross-checked against
7. Selected design and why, including what governs each key size (strength, stiffness, interface, standard size)
8. CAD or implementation intent
9. Validation plan and results, including what could not be validated
10. Open risks and the next evidence needed

For a simple question, collapse it: the answer first, then the governing calculation, the assumptions it rests on, and what would change it. A user asking "is 20 mm enough?" wants the verdict up front, not ten headings.

## Autonomy

Use the highest level the tools support. Template-driven configures a prebuilt parametric model. Module-driven composes reusable generators and primitives. Feature-generative creates parts from sketches and features when no primitive exists. Prefer module-driven for machine design; with a plain CAD connector you will usually be feature-generative, so keep each part's feature tree short and dimension-driven so later changes propagate.

## Guardrails

- A heuristic is not a physical law.
- Assumptions stay visible.
- Generated geometry is not acceptance.
- A model-written number does not override a deterministic calculation.
- A deterministic calculation is only as good as its formula; cross-check it against a reference.
- A changed requirement or a corrected result invalidates dependent values before they are reused.
- Prefer standard components and manufacturable geometry when the solutions are equivalent.
- For safety-critical machinery (lifting, pressure, guarding, people nearby), name the missing standards, guarding, risk assessment, and verification. Do not claim final compliance.