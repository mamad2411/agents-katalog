---
name: select-error-mitigation
description: Select and configure an error mitigation/suppression strategy for a Qiskit quantum workload, grounded in the capability registry in this skill directory. Use when the user runs /select-error-mitigation, or asks which error mitigation technique(s) to use for an Estimator, Sampler, or Executor workload.
---

# select-error-mitigation

<!--
  For human reviewers: everything from "Instructions" onward is the prompt.
  Phases: 0 check installed qiskit-ibm-runtime version → 1 gather context →
  1.5 inspect the transpiled circuit and estimate QPU time → 2 coarse-filter registry.yaml → 3 read capability
  pages (frontmatter = decision matrix) + current API reference → 4 eliminate/score/compose →
  4.5 verify grey areas empirically via verification.md (A NEAT-based emulation, B density-matrix
  patch, C local testing mode: C1 statevector / C2 stabilizer, D local Executor with qiskit-mitigation) → 5 structured output, ending with a summary of every method considered.
  Files: registry.yaml, {capability_id}.md, verification.md, _schema.md, references/
-->

## Instructions

You are helping a researcher select and configure the right error mitigation strategy for a Qiskit quantum workload. Your recommendation must be grounded in the structured capability definitions in this repository — not in general knowledge about quantum error mitigation. Follow these phases in order.

---

### Phase 0: Check the installed qiskit-ibm-runtime version

Run `importlib.metadata.version("qiskit-ibm-runtime")`. Several later steps depend on the result:

| | `>= 0.50.0` (client-side primitives) | `< 0.50.0` (server-side primitives only) |
|---|---|---|
| Primitives | `qiskit_ibm_runtime.executor_estimator.Estimator`, `qiskit_ibm_runtime.executor_sampler.Sampler`; the server-side `EstimatorV2`/`SamplerV2` are deprecated | `qiskit_ibm_runtime.EstimatorV2`, `qiskit_ibm_runtime.SamplerV2` |
| PEA / PEC noise learning | A separate `NoiseLearnerV3` job, passed in as `resilience.layer_noise_model` | Learned automatically by the service; tuned with `resilience.layer_noise_learning` |
| Counting unique layers (Phase 1.5) | `estimator.find_unique_layers(pubs)` or the version-neutral count | Version-neutral count only |

The capability pages' `## Configuration` code targets `>= 0.50.0`. For an older version, take the syntax from that version's API reference (Phase 3).

The Executor primitive (`QuantumProgram` / `Executor`) needs `>= 0.47.0`.

If the installed version is below 0.50.0, tell the researcher at the start and again in Open questions that upgrading to the latest `qiskit-ibm-runtime` gives better verification. Local testing mode then runs the real TREX, gate-folding ZNE and twirling implementations, instead of a hand-written emulation (see Step 4.5b).

---

### Phase 1: Gather context

Check `$ARGUMENTS` first. If the researcher has already provided enough context to determine the primitive, circuit scale, goal, and constraints, extract that information and skip to Phase 1.5. Otherwise, ask for the following in a single message — not as a sequential interview.

**Required context:**

1. **Primitive** — Which Qiskit Runtime primitive are you using?
   - `EstimatorV2` — computing expectation values of Pauli observables
   - `SamplerV2` — computing bitstring distributions / quasi-probability outputs
   - `Executor` — using the directed execution model (Samplomatic + QuantumProgram) for fine-grained control; required for PEC+SLC and PNA. TREX, gate-folding ZNE, PEA and PEC also work with the Executor through the `qiskit-mitigation` package, twirling through samplomatic's boxing, and DD through Qiskit's scheduling passes

   The primitive in the code is a starting point, not a constraint: the Executor returns raw samples, so an Estimator or Sampler workload can move to it (Phase 2).

2. **Circuit scale** — Approximate qubit count and circuit depth.
   Rough categories are sufficient: small (<20 qubits, <20 two-qubit gate layers), moderate (20–50 qubits, 20–50 layers), utility-scale (50+ qubits, 50+ layers).

3. **Primary goal** — What matters most for this workload?
   - Best possible accuracy (minimize bias)
   - Cost-effective accuracy (acceptable bias at low shot overhead)
   - Unbiased estimate required (bias elimination is a hard constraint)
   - Baseline or research (no mitigation; measuring raw hardware noise)

4. **Constraints** — Which of the following apply? (state "none" if none)
   - Circuit uses fractional gates
   - Circuit is very dense (nearly all qubits are active at all times — few idle gaps)
   - Shot budget is limited
   - Noise learning phase is not acceptable (time-sensitive execution)
   - Dynamic circuits (mid-circuit measurement or classical feed-forward)

**Unstated goal.** If the researcher gives no goal, infer one from the code and proceed rather than stopping to ask. A coarse `precision` or an optimizer loop indicates cost-effective accuracy. State the assumption in the output.

**Workloads with more than one primitive.** If the workload uses several primitives (for example, an Estimator optimization loop followed by a final Sampler run), run Phases 2–5 once per stage and give one recommendation per stage.

**Optimization loops.** Inside an optimizer loop, every technique's overhead is multiplied by the number of iterations:
- Judge mitigation in the loop by whether it preserves the ranking of parameter points (Spearman ρ against the ideal values on a few points), not only by MAE.
- Reserve high-overhead techniques (ZNE, PEA, PEC) for a single final evaluation at the optimum.
- When the spread of each evaluation is the limiting factor, a smaller `precision` (more shots) improves results more than adding ZNE.
- When verifying a loop (Phase 4.5), test only `rl0`, `trex` and `trex_twirl` at one precision. Leave ZNE out of the test unless the workload has a final Estimator evaluation at the optimum; testing it in the loop only confirms a rule already decided, at the highest local runtime.

---

### Phase 1.5: Inspect the transpiled circuit

Transpile the workload for the target backend, or its `Fake*` counterpart, and report the following. These are simulator-only checks and need no confirmation.

Run `scripts/inspect_isa.py` on a `RuntimeEncoder` JSON file of `(isa_circuit, isa_observable)` tuples (see the script docstring) instead of writing a new script. One call reports every item below: gate names and fractional gates, two-qubit count and depth against the per-qubit gate count (flagging serialized commuting terms), unique layers, idle fraction and windows against T2, the estimated QPU time per technique (pass `--shots` and `--rep-delay` to match the workload), and with `--neat` the signal strength. `--save-cpubs` saves the Clifford PUBs the same way for Phase 4.5. Use the code below only for checks the script doesn't cover.

- **Two-qubit gate count and depth**, compared with a reasonable minimum for the connectivity. For example, one layer of ZZ terms on heavy-hex needs a two-qubit depth of about 2 × the number of edge colors. A depth far above the largest number of two-qubit gates on any one qubit usually means commuting terms are applied in an order that serializes them (for example `QAOAAnsatz` or `PauliEvolutionGate` with terms in edge-list order). Sorting the terms by edge color (`rx.graph_misra_gries_edge_color`, or `rx.graph_bipartite_edge_color` on bipartite graphs) fixes it.
- **Fractional gates.** List the gate names in the ISA circuit and note whether it contains `rx` or `rzz` from a backend loaded with `use_fractional_gates=True`. Phase 4a matches this against each capability page's `avoid_when`. The two gates are not equivalent: with the client-side Estimator/Sampler or the Executor, gate twirling supports `rx` with any twirling group, but `rzz` only with `twirling.group="local_pauli"`. PEA and PEC with `rzz` also need the Executor with `inject_noise_site="before"`, since noise injected after an `rzz` layer fails on the Estimator (see the "Fractional gates" section of `pauli-twirling.md`, `zne-pea.md` and `pec.md`). Twirling `rzz` is relatively untested: when a recommended technique twirls `rzz`, warn the researcher in the output and in Open questions. Also count what fractional gates save over the non-fractional transpile (gate count, duration). If the saving is small (for example, they only replace single-qubit `rx` rotations), ask the researcher whether fractional gates are required before running any Phase 4.5 verification, since the answer changes which techniques are eliminated.
- **Unique entangling layers.** This is the number of noise-learning experiments PEA or PEC would need. Learning takes about **1 minute of QPU time per unique layer** with the `NoiseLearnerV3` defaults (32 randomizations × 128 shots per randomization), so report the estimated learning time as the unique-layer count in minutes. More randomizations or shots per randomization lengthen it.
  - With `>= 0.50.0`: set the PEA or PEC option first (`find_unique_layers` returns no layers otherwise), then call `estimator.find_unique_layers(pubs)`. The result depends on `twirling.strategy` (see `pauli-twirling.md`).
  - Any version: count distinct sets of two-qubit-gate qubit pairs per DAG layer. This count does not include the effect of the twirling strategy.
    ```python
    from qiskit.converters import circuit_to_dag

    def count_unique_2q_layers(isa_circuit):
        layers = set()
        for layer in circuit_to_dag(isa_circuit).layers():
            pairs = frozenset(
                tuple(sorted(isa_circuit.find_bit(q).index for q in node.qargs))
                for node in layer["graph"].op_nodes() if node.op.num_qubits == 2)
            if pairs:
                layers.add(pairs)
        return len(layers)
    ```
- **Estimated QPU time.** IBM Quantum Compute Service [usage](https://quantum.cloud.ibm.com/docs/en/guides/estimate-job-run-time) is the time the QPU is locked for the workload. QPU time is not the dollar cost. Usage is tracked in [resource units](https://quantum.cloud.ibm.com/docs/en/guides/plans-overview#resource-units) (1 RU = 1 minute of QPU time for standard QPU workloads), and what an RU costs depends on the researcher's plan, which this skill doesn't know. So report QPU time in seconds or minutes, never as a price. In session mode, usage is the wall-clock time the session stays active, so idle time between jobs also counts.
  - `inspect_isa.py` applies the guide's local estimate for one parameter point, per technique. Pass `--shots` ≈ `1 / precision²` and `--rep-delay` if the workload sets it.
  - Multiply by the number of parameter points, and in an optimization loop by the expected iteration count.
  - For PEC, multiply the printed per-γ² time by the actual γ² (from noise learning, or from `compute_local_scales` for PEC+SLC). For post-selection, multiply the shots by 1 / kept fraction.
  - Noise learning for PEA and PEC runs once per set of unique layers and can be reused across jobs on the same circuit structure.
  - The estimate excludes server-side work such as TREX calibration circuits. On plans that support it, a [dry-run job](https://quantum.cloud.ibm.com/docs/en/guides/dry-run-jobs) (`run(..., dry_run=True)` then `job.usage()`) reports the exact usage without using QPU time. Suggest it in Open questions when the estimate decides the recommendation. For the dollar cost or remaining allocation, point the researcher to [View the cost](https://quantum.cloud.ibm.com/docs/en/guides/view-cost).
- **Idle structure.** Measure idle fraction and window durations as described in the dynamical-decoupling page, Validation step 1.
- **Signal strength (Estimator).** Use NEAT (`qiskit_ibm_runtime.debug_tools.Neat`): convert the PUBs to Clifford form with `to_clifford`, then compare `ideal_sim` with `noisy_sim`.
  - Report the fraction of each observable's ideal value that survives the noise.
  - When little signal survives at noise factor 1, the higher noise factors of ZNE retain almost none and the extrapolation becomes unstable. In that regime, prefer TREX with a smaller `precision`.
  - The surviving fraction falls with observable weight and circuit depth.
  - If an observable's ideal value is 0 on the *original* circuit (for example a mirror circuit without basis preparation), no technique can be judged on it. Report this as a structural problem.
  - Save the Clifford PUBs from `to_clifford` with `RuntimeEncoder` (e.g. `inspect_isa.py --save-cpubs /tmp/em/cpubs.json`). Phase 4.5 Method C2 reuses them instead of converting again.

If depth is far above the minimum, look for a structural cause before recommending mitigation, and report it first. Examples are duplicated Hamiltonian terms, commuting gates scheduled one after another, or a sequential entanglement pattern. A structural fix improves results more than any technique choice.

---

### Phase 2: Read the capability registry

Read the file at `.claude/skills/select-error-mitigation/registry.yaml`.

This is the authoritative index of all available error mitigation and suppression capabilities. Each entry has:
- `id` — the capability identifier (matches the filename of the full definition page)
- `primitive` — list of supported primitives: `estimator`, `sampler`, `executor`
- `overhead_class` — `none`, `low`, `medium`, `high`, or `exponential`
- `estimate_bias` — `unbiased`, `reduced-bias`, or `not-applicable`
- `resilience_level` — the resilience level that activates this technique, or `null` for manual-only
- `path` — path to the full capability definition page (or an external URL)
- `external` / `external_package` — present if the capability always requires an external addon
- `executor_package` — a package needed only when the capability is used with the Executor (`qiskit-mitigation`)

**Coarse filter:** From the registry, retain entries where the researcher's chosen primitive appears in the `primitive` list. Also retain every entry that lists `executor`, whatever primitive the code uses: the Executor returns raw per-shot samples, from which expectation values or distributions can be computed, so any Estimator or Sampler workload can move to it. Mark these entries "needs the Executor" and weigh the workflow change (`QuantumProgram`, samplomatic boxing, own post-processing) as a cost in Step 4b. Discard all others. Also discard entries with `external: true` that the researcher has not explicitly asked about, unless no in-repo option satisfies their goal.

---

### Phase 3: Read the relevant capability pages

For each capability that survived the coarse filter, read its full definition page at the path listed in the registry. These are the files in `.claude/skills/select-error-mitigation/`.

From each page's frontmatter, extract:
- `use_when` — list of conditions where this technique is appropriate
- `avoid_when` — contraindications; if any match the researcher's context, this technique is eliminated
- `prerequisites` — required preconditions; note any that may not be met
- `compatible_with` — capability IDs that work alongside this one
- `incompatible_with` — capability IDs that cannot be used in the same job
- `overhead_class`, `estimate_bias`, `requires_noise_learning`, `requires_hardware`

Also note the `## Configuration` section of each page body. It shows which options turn the technique on, but its code was written against one `qiskit-ibm-runtime` version and can go stale. Before writing code, read the current API references for the Estimator and Sampler primitives and their options, and treat those as the source of truth for class names, import paths, option names and allowed values:
- If the **qiskit-docs MCP server** is connected, use `search_docs_tool` to find the pages and `get_page_tool` to read them. With `>= 0.50.0`, start with `api/qiskit-ibm-runtime/executor-estimator` and `api/qiskit-ibm-runtime/executor-sampler` and the `options-models-*` option pages they link to. With an older version, read the server-side `EstimatorV2`/`SamplerV2` and options pages for that version.
- Otherwise, read the same pages from the [qiskit-ibm-runtime API reference](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime).
- For an Executor workload that uses `qiskit-mitigation`, also read its API reference and the guide linked from the capability page's "With the Executor" section.
- Read the reference for the version found in Phase 0. Where the reference and a capability page disagree, follow the reference and mention the discrepancy in your output.

Also read the feature-compatibility section for the primitive in use: [Estimator](https://quantum.cloud.ibm.com/docs/en/guides/estimator-options.md#feature-compatibility) or [Sampler](https://quantum.cloud.ibm.com/docs/en/guides/sampler-options.md#feature-compatibility). The capability pages' `avoid_when` and `incompatible_with` should already contain every pair it lists. If the table lists a restriction the pages don't, follow the table, mention it in your output, and suggest adding it to the page.

---

### Phase 4: Apply the decision matrix

**Step 4a — Hard elimination.**
For each candidate capability, check every `avoid_when` condition against the researcher's context. If any condition matches, eliminate the capability entirely. Do not suggest eliminated capabilities as alternatives.

One rule applies across pages: on the Executor, a dynamic circuit (conditional operations) eliminates every technique that relies on samplomatic boxing, because samplomatic does not support dynamic circuits. That covers gate twirling, TREX, gate-folding ZNE, PEA and PEC through `qiskit-mitigation`, PEC+SLC and PNA. Dynamical decoupling remains, inserted by hand (see `dynamical-decoupling.md`).

**Step 4b — Fit scoring.**
For each remaining capability, count how many `use_when` conditions match the researcher's context. This is the fit score. Higher is better.

Weigh the fit score against the estimated QPU time from Phase 1.5. When two techniques give similar accuracy, prefer the one that needs less QPU time. When the goal is cost-effective accuracy, or the researcher gave a QPU-time budget (a budget in money has to be converted with their plan's rate first; ask for it rather than assuming one), eliminate a technique whose estimated time (including noise learning) exceeds the budget.

**Step 4c — Stack composition.**
Most Estimator and Executor workloads benefit from combining multiple techniques. Compose a recommended stack using these rules:

1. For Estimator or Executor: select the highest-fit technique that addresses gate errors (ZNE variants or PEC). This is the primary technique.
2. For Estimator or Executor: add TREX if it was not eliminated (it handles readout errors at low cost and is compatible with all gate-error techniques).
3. For Estimator, Sampler or Executor: add the suppression techniques (dynamical decoupling, Pauli twirling) that survived Step 4a if the circuit has idle periods. For twirling, choose `strategy` per `pauli-twirling.md`: the default `"active-accum"` harms circuits with many sequential entangling layers. On the Executor, apply DD after twirling. On a dynamic circuit with conditional operations, insert DD by hand, preferably with stretch (see `dynamical-decoupling.md`).
4. For Sampler or Executor: add post-selection (`postselection-non-markovian.md`) only if it survived Step 4a and the shot budget covers the discarded shots. Its overhead is 1 / kept fraction. It stacks with the gate-error technique from rule 1, but on the Executor the mask goes through `executor_expectation_values(postselect_mask=...)`, not a `qiskit-mitigation` task's `postprocess` (see the page's Composability section).
5. Verify the stack: for every pair of techniques in the stack, confirm neither appears in the other's `incompatible_with` list.

**Step 4d — Prerequisite check.**
For every technique in the final stack, verify that all `prerequisites` are met given the researcher's context. Flag any that are uncertain.

---

### Phase 4.5: Empirically verify grey-area decisions

Some decisions from Phase 4 can't be resolved with confidence from the decision matrix alone — the frontmatter conditions don't cover every real workload, and the researcher's context may leave a deciding condition unknown. When this happens, verify empirically instead of guessing or silently picking a default.

**Step 4.5a — Identify grey areas.**
A candidate technique is a grey area if either:
- A `use_when` or `avoid_when` condition that would change whether it's included depends on information the researcher didn't provide, answered as "unsure," or that can't be determined from static context alone (e.g., whether noise on this specific backend/circuit pair actually scales predictably with depth).
- Two candidates competing for the same role in the stack (e.g., two gate-error mitigation options) land within one point of each other on fit score, and only one can be included.

If no candidate is a grey area, skip straight to Phase 5.

**Step 4.5b — Pick the verification method, then run it.**
Read `.claude/skills/select-error-mitigation/verification.md` for how to run each method. Using the wrong method gives a confident but meaningless result:

| Grey-area technique | Method |
|---|---|
| TREX, gate-folding ZNE, twirling, resilience level (Estimator or Sampler) | With `>= 0.50.0`: **C — local testing mode**. The client-side primitives apply the real technique locally, so no custom emulation is needed. **C1** statevector runs the real circuit, but only on a ≤~30-qubit backend. **C2** `AerSimulator(method="stabilizer")` runs a Clifford version of the circuit at any width. With `< 0.50.0`: **A**, and recommend upgrading (Phase 0) |
| PEA or PEC (Estimator) | **A — custom emulation** on NEAT's Clifford circuit and Pauli noise model, in any version. With `>= 0.50.0`, run the competing gate-folding side of a fold-vs-PEA comparison through Method C2 on the same Clifford circuit and noise model |
| TREX, gate-folding ZNE, PEA or PEC on an Executor workload (`qiskit-mitigation`) | **D — local Executor run**: the `qiskit-mitigation` tasks run on an `AerSimulator` with an injected layer noise model. For PEA/PEC on an Estimator workload, D is an alternative to A that runs a real PEA/PEC implementation (`qiskit-mitigation`'s, not the Estimator's) instead of a hand-written emulation |
| Dynamical decoupling, or any coherent-error question | **B — small density-matrix patch** with a coherent-noise model. A, C and D are all blind to DD |
| Post-selection on non-Markovian error checks | **None locally.** Aer noise is Markovian, so no method can measure the benefit. Run a noiseless local check of the wiring (every shot must pass), then carry the decision to Open questions as a hardware comparison against the raw circuit |

For C1 on an Estimator workload, run `scripts/verify_c1.py` on the logical circuit and observable. For C2, run `scripts/verify_c2.py` on the Clifford PUBs saved in Phase 1.5. Don't write new scripts for either. Launch the run in the background and continue with the Phase 5 option-path checks while it runs.

For either runner, run only the configurations that resolve the grey area, plus `rl0` as the baseline; pass `--fractional` only when the circuit has fractional `rzz` gates, which makes the twirled configurations use `twirling.group="local_pauli"` (an `rx`-only circuit twirls with the default group). Add other noise-factor grids only if the default (1, 3, 5) result is inconclusive.

If no method fits (e.g. PEC+SLC or PNA on the Executor, post-selection, or SamplerV2 on `qiskit-ibm-runtime < 0.50.0`), carry the grey area into Phase 5's Open Questions and rely on the Phase 4 scoring.

**Step 4.5c — Confirmation rule (all methods).** If the only backend available is real hardware (no simulator or fake backend to fall back to), stop before submitting any job and ask the researcher to confirm first — this consumes real shot budget and queue time. Simulator-only runs (`AerSimulator`, fake backends, and locally-built noise models from live calibration) don't require confirmation. Fetching live calibration reads the researcher's saved IBM credentials, so ask before doing it (see `verification.md`).

**Step 4.5d — Fold the result back into Phase 4.**
Use the subagent's verdict to resolve the grey area: include the technique if it measurably reduced the error against the ideal result (MAE for Estimator, distribution distance for Sampler), and exclude it otherwise. Carry the numbers forward — they become the citation for this technique's inclusion or exclusion in Phase 5, alongside (or in place of) the `use_when` citation.

State the method used and its limits:
- **Method A** is a custom emulation on a structural Clifford stand-in. It answers gate- and readout-error questions only, and its depolarizing noise model favours gate folding over PEA.
- **C1 (statevector local mode)** runs the real technique on the real circuit, but with a small proxy backend's noise rather than the target's.
- **C2 (stabilizer local mode)** runs the real technique on the target's noise, but on a Clifford stand-in circuit.
- **Method D (local Executor)** runs the real `qiskit-mitigation` implementation, on a modeled layer noise model. For PEA/PEC it is only as faithful as the noise model it is given as "learned".
- **Method B** comes from a small patch under a *modeled* coherent-noise assumption. Static detuning under-models low-frequency 1/f drift, which DD is especially good at, so carry a marginal or negative suppression result into Phase 5 as a hardware A/B test rather than a hard exclusion.

Some methods cannot measure some techniques at all. Examples are gate twirling under a depolarizing or Pauli noise model, and DD under any method except B. Report such a result as "not measurable by this method", keep or drop the technique on its Phase 4 score, and flag it in Open questions. Never treat it as "no reduction".

---

### Phase 5: Produce the output

Structure your response as follows. Use plain prose — no marketing language.

Keep it short: the stack, the scaffold, the open questions, and the closing summary of every method considered. Put per-configuration tables and multi-step elimination reasoning in only when the researcher asks, or when a result contradicts the Phase 4 scoring.

#### Recommended configuration

Name the technique stack (e.g., "TREX + ZNE with gate folding + dynamical decoupling"). For each technique in the stack, give one sentence of justification that cites the specific `use_when` condition from the capability page that drove the inclusion. If a technique's inclusion or exclusion was instead (or additionally) resolved via Phase 4.5 empirical verification, say so explicitly and report the MAE-vs-ideal numbers for both configurations.

If any technique requires a noise learning phase or an external package, state this explicitly here. Report any structural problem found in Phase 1.5 ahead of the technique stack.

**Estimated QPU time.** State the estimated QPU time of the recommended stack, split into circuit execution and noise learning (for PEA and PEC). Give the shots, circuit count and `rep_delay` the estimate assumes, the per-evaluation and total time for an optimization loop, and the same figure for the Alternative. Say that it is a local estimate (Phase 1.5) and, on plans that support it, that a dry-run job gives the exact usage. Don't convert it to a price: say that the dollar cost, or the share of an allocation, depends on the researcher's plan.

#### Resilience level shortcut (Estimator only)

If the recommended stack maps cleanly to a resilience level (0, 1, or 2), state this. Otherwise note that manual options are required.

#### Alternative

Describe one alternative configuration that trades a significant dimension (e.g., lower overhead at the cost of higher bias, or higher accuracy at the cost of more shots). One sentence per trade-off.

#### Code scaffold

Produce a minimal, runnable Python code snippet implementing the recommended configuration. Rules:
- Choose the techniques and options from the capability pages, but take the syntax (imports, class names, option paths, allowed values) from the API references read in Phase 3, not from the pages' `## Configuration` code. Do not invent parameters that appear in neither.
- Use the primitive classes for the installed version (Phase 0).
- Include the primitive initialization, relevant options, and a placeholder `estimator.run(...)` or equivalent call.
- For Executor-based techniques, use the `QuantumProgram` / `Executor` pattern from the capability page. Note that Executor has no built-in mitigation options — all technique configuration is in the circuit boxing and post-processing steps. For TREX, gate-folding ZNE, PEA and PEC, that means the `qiskit-mitigation` tasks (each page's "With the Executor" section).
- If the technique is from an external addon, include the `pip install` command.

**Validate the option paths and the PUB before presenting.** The mitigation config is only half the scaffold; a job also fails if the PUB is malformed, and that failure has nothing to do with the technique choice. Two things are cheap to check against the fake backend and worth checking:
- **Option paths** — construct the primitive with the recommended options on the fake backend (e.g. `Estimator(mode=FakeKingston(), options={"resilience_level": 2})` and each explicit `estimator.options...` assignment). This catches renamed or invented attributes before the researcher hits them. For PEA and PEC, which need a learned noise model, set a hand-built `layer_noise_model` as in verification.md, "Syntax check for PEA and PEC"; that checks the job builds, not that it works. Steps that only run on hardware cannot be validated this way; say so.
- **PUB broadcasting** — coerce the actual PUB (`qiskit.primitives.containers.EstimatorPub.coerce((circuit, observables, params))`) and confirm the resulting `.shape` is what you claim. When a PUB combines several observables with several parameter points, read `references/pub-broadcasting.md` first.

#### Open questions

List any context you needed but could not determine (e.g., whether the circuit has idle gaps, whether fractional gates are used). These are the questions the researcher should answer before finalizing the configuration.

Also list any grey area from Phase 4.5 that could **not** be verified empirically, and state that it was resolved by `use_when`/`avoid_when` scoring alone, so the researcher should treat it as lower-confidence. This applies when:
- the workload used the Executor with a technique Method D doesn't cover (PEC+SLC, PNA)
- the stack includes post-selection, whose benefit can only be measured on hardware
- the workload used SamplerV2 with `qiskit-ibm-runtime < 0.50.0`
- the researcher declined a real-hardware run
- the method could not measure the technique (Step 4.5d)

If the installed `qiskit-ibm-runtime` is below 0.50.0, repeat the upgrade recommendation from Phase 0 here.

#### Summary of methods considered

Always end with this section, so the researcher can see how the recommendation was reached and how much to trust it. Give one row per capability that survived the Phase 2 coarse filter, whether it was selected or not:

| Method | Verdict | Est. QPU time | Reason | Decided by |
|---|---|---|---|---|
| e.g. TREX | Selected | ~5 s | Readout errors matter and the overhead is low (`use_when`: ...) | Decision matrix |
| e.g. ZNE (gate folding) | Not selected | ~9 s | MAE 0.12 vs 0.08 for TREX alone; the folded circuits lost the signal | Method C2 (stabilizer local mode) |
| e.g. PEC | Eliminated | ~3 s × γ² + 5 min learning | `avoid_when`: shot budget is limited | Decision matrix |

- **Verdict** is one of: Selected, Alternative, Not selected (survived Step 4a but lost on fit score, verification or composability), or Eliminated (an `avoid_when` matched or a prerequisite was unmet).
- **Est. QPU time** is the Phase 1.5 estimate for the whole workload (the script reports one parameter point; multiply by the parameter points and loop iterations) with that technique alone added to the base circuits, with noise learning listed separately. Give it for every row, including eliminated ones, so the researcher can compare the QPU time of each option.
- **Reason** cites the specific `use_when` or `avoid_when` condition, the incompatibility, or the verification numbers. Each reason must be specific to this workload; never use a generic description of the technique.
- **Decided by** names the decision matrix, the verification method that ran (A, B, C1, C2, D), or "not measurable by this method" (Step 4.5d), so the researcher can tell which choices were tested and which rest on scoring alone.

After the table, list in one line the registry entries dropped by the coarse filter (wrong primitive, or an external addon the researcher did not ask about), so the researcher can see nothing was skipped silently.
