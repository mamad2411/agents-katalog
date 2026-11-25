---
name: fusion-data-analysis
description: >-
  Fusion plasma data analysis across the tokamak/stellarator research pipeline. Use when the user
  asks to analyze, interpret, or QA equilibrium reconstructions (EFIT, LIUQE, G-EQDSK, gfile,
  eqdsk, flux-surface geometry, safety factor q-profile, magnetic shear s, normalized flux ψ_N,
  ρ_tor, r/a, elongation κ, triangularity δ), kinetic profiles (electron/ion temperature T_e/T_i,
  electron density n_e, toroidal/impurity rotation v_φ/v_t, profile fitting with
  polynomial/tanh/mtanh/Gaussian, normalized gradient scale lengths R/L_T and R/L_n, profile
  alignment and interpolation, error propagation), transport analysis (power balance, particle
  balance, stored energy W_MHD, energy confinement time τ_E, effective thermal diffusivity χ_eff,
  effective particle diffusivity D_eff, TGLF/NEO comparison), MHD stability (ideal/resistive MHD
  modes, m/n mode number identification, tearing mode, NTM, sawtooth, kink, ballooning,
  no-wall/with-wall β_N limit, resistive wall mode RWM, ELM classification), edge plasma
  (H-mode/L-mode identification, L-H transition, ELM frequency f_ELM and energy loss ΔW_ELM,
  pedestal height/width extraction, scrape-off layer SOL parameters, divertor heat flux λ_q), or
  OMFIT workflow integration (module chaining, data passing, workflow templates). Also trigger on
  Chinese requests such as 平衡重建、剖面分析、输运分析、MHD稳定性、边缘等离子体、EFIT、LIUQE、
  eqdsk、G-file、G文件、磁面、安全因子、磁剪切、通量坐标、温度剖面、密度剖面、梯度、功率平衡、
  能量守恒、储能、约束时间、有效输运系数、撕裂模、ELM、台基、pedestal、刮削层、SOL、H模、L模、
  OMFIT、数据分析、径向剖面.
metadata:
  author: fusion-domain skill library
  skill-type: fusion-native (built from scratch, no nature-* source)
---

# Fusion Data Analysis — Router

This skill performs physics analysis on fusion plasma data — equilibrium, kinetic profiles,
transport, MHD stability, edge plasma, and OMFIT integration. It is a **router**: this file
holds the protocol; the real content lives in `static/` and `references/`, and the shared
definitions (terminology, parameter definitions, constants, formats, machine data) live in
`../fusion-shared/` and are loaded on demand, never copied here.

Do **not** do fusion data analysis from memory. Always load fragments from disk as described
below, and always resolve terminology, parameter definitions, and numbers against the shared
knowledge base (`../fusion-shared/core/`).

## Static / dynamic split

- **Static layer** — versioned, reusable content under `static/`:
  - `static/core/stance.md` — analysis red lines (equilibrium version & coordinates first,
    units travel with data, errors mandatory, shot+time dual key, provenance, no cherry-picking,
    β/β_N/q_95 conventions, energy-conservation closure).
  - `static/core/workflow.md` — the end-to-end eight-step analysis workflow and output format.
  - `static/fragments/*.md` — one per `analysis_type` module (equilibrium / profile / transport /
    mhd-stability / edge-plasma).
- **Dynamic layer** — this file + `manifest.yaml`: loads the core every time, selects the
  matching fragment(s) via the `analysis_type` axis, and reaches deeper references only when a
  step needs them.

## Routing protocol

Follow these steps every time the skill is invoked.

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). Then read every file listed under `always_load`:

- `../fusion-shared/core/terminology-ledger.md` — bilingual terminology and symbol conventions
  (single source of truth; use exact spellings: H-mode, ELM, SOL, T_e, q_95, β_N, τ_E …).
- `../fusion-shared/core/parameter-definitions.md` — canonical definitions of β/β_N/β_p, q_95,
  τ_E, χ_e/χ_i/D, R/L_T, n_GW, m/n, β_N limits, pedestal/ELM quantities.
- `static/core/stance.md` — red lines that govern every analysis.
- `static/core/workflow.md` — the eight-step workflow and output format.

### 2. Detect the analysis_type and load the matching fragment(s)

Use the `axes.analysis_type.detect` hint in [manifest.yaml](manifest.yaml) to classify the
request into one or more of: `equilibrium`, `profile`, `transport`, `mhd-stability`,
`edge-plasma` (`multi: true`, so a request may span several). Load every matching fragment from
`static/fragments/` before starting. When the request spans modules (e.g. pedestal-gradient
transport), load all of them and run the workflow across the union of steps.

OMFIT is not an `analysis_type` value — it is a cross-cutting integration layer. When the task
involves OMFIT module chaining or data passing, also open
`references/omfit-workflow-templates.md`.

### 3. Run the workflow

Follow the eight-step workflow in `static/core/workflow.md`: (1) intake machine/shot/time/
diagnostic; (2) load the equilibrium; (3) map data to flux coordinates; (4) fit profiles and
compute gradients; (5) transport/power balance; (6) MHD/edge analysis as requested; (7) QA
against the consistency sweep; (8) report numbers + uncertainties + provenance.

For every numeric claim, carry units and uncertainties; for every derived quantity, state the
input data and its diagnostic source. Use the bundled scripts (`scripts/read_eqdsk.py`,
`scripts/fit_profile.py`, `scripts/power_balance.py`) when they apply, and pass them the raw
inputs rather than re-deriving by hand.

### 4. Reach for references only when needed

The files under `references/` are deep references, not defaults. Open them per the
`references.on_demand` table in the manifest — e.g. `references/gfile-format.md` and
`references/efit-output-spec.md` when parsing equilibrium files, `references/power-balance-formula.md`
for term-by-term power-balance arithmetic and pitfalls, `references/tglf-neo-comparison.md` when
comparing turbulent (TGLF) vs neoclassical (NEO) fluxes, and
`references/omfit-workflow-templates.md` for OMFIT module chains.

### 5. Never invent physics

Resolve every physical constant and unit conversion against
`../fusion-shared/core/physics-constants.md`; every machine parameter against
`../fusion-shared/core/machine-database.md`; every data-format field against
`../fusion-shared/core/data-formats.md`. Do not fabricate numbers, file fields, or OMFIT
module names.

## Why this split

- The static layer is versioned and reviewable; the core stays small for a routine request.
- The dynamic layer keeps each invocation cheap: fragments load only for the detected
  `analysis_type`, and deep references load only when a step needs them.
- This router is short on purpose. Update fragments and references, not this file, when adding
  scope.
- This structure mirrors the `nature-*` skills (static/dynamic + manifest routing) but is built
  from scratch with fusion content.
