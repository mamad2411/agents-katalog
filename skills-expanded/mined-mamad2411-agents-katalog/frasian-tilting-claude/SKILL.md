# Frasian Inference Framework

## Project Overview

A research framework for studying alternatives to power-law tilting in the
Frasian inference setting. The driving question: **does optimal-transport
or geodesic interpolation between prior, likelihood, and posterior produce
smoother families than naive power-law tilting, and which test statistics
exploit them best?**

The framework is structured as a **(TiltingScheme × TestStatistic) cross-
product**. Every cell of the matrix produces a `RawResult` consumed by a
shared diagnostic suite (coverage, width, smoothness). Adding a new tilting
or statistic is a one-file change plus its brief, property tests, and demo.

The legacy code that motivated this design lives under `legacy/` for
reference. The migration status (which Steps are done) is at the bottom.

## The Conjugate Normal Sandbox

All experiments operate on the 1D conjugate Normal-Normal model:

- **Prior**: θ ~ N(μ₀, σ₀²)
- **Likelihood**: D | θ ~ N(θ, σ²)
- **Posterior**: θ | D ~ N(μₙ, σₙ²)
- **Data weight**: w = σ₀²/(σ² + σ₀²) ∈ (0, 1)
- **Posterior mean**: μₙ = wD + (1-w)μ₀
- **Posterior std**: σₙ = √w · σ

**Key quantities** used by tilting / WALDO / smoothness:
- Scaled prior-data conflict: Δ = (1-w)(μ₀ - D)/σ
- Prior residual: δ(θ) = (θ - μ₀)/σ₀
- Non-centrality: λ(θ) = (1-w)²(μ₀ - θ)² / (w² σ²)

The protocols in `src/frasian/models/base.py` are designed so future work
can add non-conjugate or non-Gaussian models without rewriting consumers,
but **everything implemented today is Normal-Normal only**. Generic
posterior inference is a flagged future extension.

## Architecture: Six Protocols

Every concrete implementation conforms to one of:

| Protocol                | Purpose                              | Module                            |
|-------------------------|--------------------------------------|-----------------------------------|
| `Model`                 | Sample data, build posterior, MLE    | `frasian/models/base.py`          |
| `TiltingScheme`         | tilt(posterior, prior, lik, η)→post  | `frasian/tilting/base.py`         |
| `TestStatistic`         | evaluate, pvalue, CI, accept region  | `frasian/statistics/base.py`      |
| `ConfidenceDistribution`| pdf/cdf/quantile/interval/mean/mode  | `frasian/cd/base.py`              |
| `Experiment`            | grid → cells → diagnostics           | `frasian/experiments/base.py`     |
| `Diagnostic`            | RawResult → DiagnosticTable + figure | `frasian/diagnostics/base.py`     |

Plus `EtaSelector` and `LearnedArtifact` for the support layer.

### Plugin Registry

Concrete implementations register via decorators:

```python
@register_tilting(name="power_law", brief="docs/methods/power_law.md")
class PowerLawTilting:
    ...
```

The decorator records the brief path so `tools/check_method_completeness.py`
can verify every registered class ships with documentation, property tests,
and an illustration. A single `_registry_bootstrap.py` enumerates the
imports so static tooling can find every method.

User-facing call:

```python
from frasian import default_cells, run_experiment, registry, Config

tiltings, statistics = default_cells(experiment="coverage")
summary = run_experiment(
    experiment=registry.experiments["coverage"](),
    tiltings=tiltings,                   # [IdentityTilting(), PowerLawTilting(selector=DynamicNumericalEtaSelector(...))]
    statistics=statistics,               # [WaldStatistic(), WaldoStatistic()]
    config=Config.fast(),                # or Config.default()
    out_dir=Path("results/coverage"),
)
```

`default_cells(experiment="smoothness")` returns the bare-family
tiltings instead, since the smoothness experiment sweeps the parameter
itself and would produce duplicate output if the cell carried a
non-default selector.

The runner persists each cell's `RawResult` through the cache layer (keyed
on Config fingerprint + git sha + raw fingerprint), runs the experiment's
diagnostics, and writes a `manifest.json` with relative cache paths.

## Models (status)

| Name           | Status        | Notes                                     |
|----------------|---------------|-------------------------------------------|
| `normal_normal`| implemented   | 1D conjugate Gaussian; framework's sandbox |

The framework's research focus is the Normal-Normal sandbox. A prior
Bernoulli + Beta-conjugate model was shelved (see commit
`chore: shelve Bernoulli ...`); the generic model-agnostic paths
in `power_law`, `mixture`, and `ot` remain and stay useful for any
future non-NN model that lands.

## Tilting Schemes (status)

| Name         | Status        | Notes                                                                                |
|--------------|---------------|--------------------------------------------------------------------------------------|
| `identity`   | implemented   | No-op tilting; identity element of the matrix                                        |
| `power_law`  | implemented   | e-geodesic / log-linear (geometric mean); Theorem 6 closed form on Normal-Normal     |
| `ot`         | implemented   | W2 geodesic; general 1D quantile-mixture, Gaussian fast path; posterior↔likelihood   |
| `mixture`    | implemented   | m-geodesic / linear-density (arithmetic mean); dual partner of `power_law`. Closed-form NN tilt + WALDO p-value, structural sigmoid (0,1) bound on EtaNet output (row 13c). |
| `fisher_rao` | implemented   | Levi-Civita / Riemannian geodesic on the Gaussian half-plane; closed-form NN tilt + WALDO p-value (Stage A), generic autodiff path via diffrax shooting BVP (Stage B), Phase G v4 learned-η fixtures for all 3 heads (Stage C). Smoothness comparison vs PL/OT/MX in Stage D. |

These four cover the canonical geodesic taxonomy: e-/m-geodesics
(`power_law`/`mixture` — the dually-flat pair under the Fisher
metric), the Levi-Civita / Fisher-Rao geodesic (`fisher_rao`), and
the Wasserstein geodesic (`ot`). An `exp_family` natural-parameter
scheme would be redundant with `power_law` on conjugate exponential
families and is omitted by design.

Each `TiltingScheme` owns its **selector** (`EtaSelector`) as a
constructor argument: `FixedEtaSelector` is the static identity,
`NumericalEtaSelector` is static-with-context (post-selection — see
caveat below), and `DynamicNumericalEtaSelector` varies η per θ. The
cell name picks up the selector when non-default, so
`power_law[dynamic_numerical]` is the **Dynamic-WALDO** cell when
paired with `waldo`. The `identity` tilting + a uniform
`tilting.confidence_interval(alpha, data, model, prior, statistic)`
API let coverage / width / smoothness all share one cell loop.

**CI region semantics — important.** Dynamic-η inversion can produce
a CI that is the union of multiple disjoint regions (the dynamic
p-value is non-monotone in θ at conflict). Two methods on
`TiltingScheme` resolve this:

- `confidence_regions(...) -> list[(lo, hi)]` returns the **actual
  union**: every disjoint accept-region, sorted. This is what
  `coverage` and `width` experiments call. `width` records
  `sum(hi - lo)` — true union width, NOT the convex hull.
- `confidence_interval(...) -> (lo, hi)` returns the **convex hull**
  `(min lo, max hi)` as a single-tuple summary. Use this only when a
  caller needs a single interval.

Single-region cells (Wald, identity, fixed-η static cells) have
`len(regions) == 1` so the two coincide. Multi-region cells (e.g.
`power_law[dynamic_numerical]` at extreme conflict) — `confidence_regions`
gives the honest answer, `confidence_interval` over-counts the gaps.

**Calibration caveat — important.** The framework's calibrated default
is `DynamicNumericalEtaSelector`: η at each θ depends only on θ (not
on D), so the WALDO p-value at any fixed η is U[0,1] under H0 and the
CI achieves exact 1-α coverage. The static `NumericalEtaSelector`
gives strictly narrower CIs (≤ Wald asymptotically) but is post-
selection inference and **undercovers by ~2 points at α=0.05** —
pinned by `tests/regression/test_post_selection_coverage.py`. The
static selector is exposed via `post_selection_demo_tiltings()` only
to make the trade-off measurable; never use it for production CI
estimation.

**Calibrated AND narrow: `LearnedDynamicEtaSelector`.** The
Phase G **conditional dual-head** learned selector (`EtaNet` +
`ValidityNet`, in `src/frasian/learned/eta_artifact.py` +
`learned/training/`) is the production calibrated-and-narrower
alternative to `numerical` (which inflates width ~30% at the
conflict band). EtaNet maps `(θ, prior_hp, lik_hp) → η`;
ValidityNet maps `(θ, prior_hp, lik_hp, η) → logit` and provides
the boundary penalty for Head A. **Conditional**: each checkpoint
is trained over a *range* of `(prior_hp, lik_hp)` (the
`hyperparam_distribution` block in the v4 YAML); the selector
refuses inference when the observed class doesn't match the
trained `prior_class` / `model_class`, or when the observed
hyperparams fall outside the trained range.

Two architectural ingredients are essential and ON by default:
**σ₀-anchored θ training** (`Sigma0AnchoredUniformThetaDistribution`
in `sampling.py`; canonical class name as of 2026-05-10, with
backwards-compat alias `SigmaAnchoredUniformThetaDistribution`. The
"σ₀" specifically means the **prior's σ₀**, NOT the likelihood's σ —
this distinction caused real confusion during the 2026-05-10
investigation; see
[`docs/notes/2026-05-10-eta-conventions-and-loss-derivation.md`](docs/notes/2026-05-10-eta-conventions-and-loss-derivation.md).)
and **per-channel input z-score normalization** on EtaNet/ValidityNet.
Without σ₀-anchored training the model
collapses to η ≈ 1 (= Wald); see
[`docs/notes/2026-05-09-phase-g-v4-fix.md`](docs/notes/2026-05-09-phase-g-v4-fix.md)
for the diagnosis and the per-loss audit results.

`LearnedDynamicEtaSelector` runtime now **clamps** η to admissible
range when EtaNet extrapolates out of bounds (the dynamic-CI
calibration guarantee holds for any η, so clamping preserves
coverage; only widths inflate at the boundary). A warning still
fires for inspection.

v4 fixtures are gitignored (`artifacts/learned_eta_*_v4.eqx`) — train
via `scripts.train_learned_eta --config
experiments/<config>_v4.yaml`. Activate via env var:

```
export FRASIAN_DEFAULT_DYNAMIC_ETA=learned   # vs default "numerical"
```

For per-method theory + derivation see `docs/methods/learned_eta.md`.
For headline numbers + audit results + per-loss tradeoffs see
`docs/notes/2026-05-09-phase-g-v4-fix.md`. Regenerate the headline
with `PYTHONHASHSEED=0 python -m scripts.regen_headline`; plot
η(θ) curves with `python -m scripts.plot_v4_eta_curves`.

## Test Statistics (status)

| Name          | Status        | Notes                                          |
|---------------|---------------|------------------------------------------------|
| `wald`        | implemented   | Closed-form CI on Normal-Normal: D ± z·σ; identity-tilting only. Generic path on any Model: τ=(mle−θ)²·I(θ), χ²₁ calibration. |
| `waldo`       | implemented   | Closed-form on Normal-Normal+Normal: p(θ)=Φ(b−a)+Φ(−a−b). Generic path on any (Model, Prior): MC reference under H_0 via model.sample_data, knobs n_mc/seed (CRN across brentq). |
| `lrt`         | implemented   | -2 log Λ; on Normal-location reduces to Wald. Cross-product extended via trinity collapse on PL/OT/FR closed-form and analytic 2-Gaussian-mixture stats on MX (see `docs/notes/2026-05-12-tilted-trinity-derivation.md`). |
| `lrto`        | implemented   | Posterior-LR (Aitkin / Dempster); -2[log π(θ|D) - log π(θ_MAP|D)]; on NN+Normal collapses to WALDO `Φ(b−a)+Φ(−a−b)`. Cross-product extended via trinity collapse on PL/OT/FR closed-form (route to waldo arithmetic) and analytic 2-Gaussian-mixture stats on MX (analytic τ + MC over D'). See `docs/notes/2026-05-12-tilted-trinity-derivation.md`. |
| `score`       | implemented   | U(θ)²/I(θ); on Normal-location reduces to Wald. Cross-product extended via trinity collapse on PL/OT/FR closed-form and analytic 2-Gaussian-mixture stats on MX (see `docs/notes/2026-05-12-tilted-trinity-derivation.md`). |
| `scoreo`      | implemented   | Posterior score (Lindley / Aitkin); U_post(θ)²/I_post(θ); on NN+Normal collapses to WALDO `Φ(b−a)+Φ(−a−b)`. Cross-product extended via trinity collapse on PL/OT/FR closed-form (route to waldo arithmetic) and analytic 2-Gaussian-mixture stats on MX (analytic τ + MC over D'). See `docs/notes/2026-05-12-tilted-trinity-derivation.md`. |
| `signed_root` | stub          | sign·√LRT; on Normal-location equals Wald      |
| `bartlett`    | stub          | LRT/E[LRT]; decorator over base LRT (planned)  |

Each statistic declares which tiltings it accepts via
`accepts_tilting(tilting)`. Wald accepts only `identity` (it ignores
the prior, so non-identity cells are degenerate duplicates). Other
statistics accept any tilting by default. The runner gates incompatible
cells before `run_cell` and records them in the manifest with
`status="incompatible"`.

## Experiments (status)

| Name                       | Status      | Output                                              |
|----------------------------|-------------|-----------------------------------------------------|
| `coverage`                 | implemented | Empirical coverage on (θ_true, w) grid              |
| `width`                    | implemented | Mean CI width on (θ_true, w) grid                   |
| `smoothness`               | implemented | η*(|Δ|) Lipschitz / TV / discontinuity / spectral   |
| `confidence_distribution`  | implemented | CD median / 95-width / W₁-to-Wald / non-monotone fraction |

All three experiments dispatch CI computation through
`tilting.confidence_interval(alpha, data, model, prior, statistic)` —
the tilting owns its selector and so produces plain WALDO at
`(identity, waldo)` and Dynamic-WALDO at `(power_law[dynamic_numerical],
waldo)` from the same loop. The legacy `dynamic_ci` experiment was
folded into `coverage` / `width` (it was effectively those two
diagnostics on a different selector); the underlying
`PowerLawTilting.dynamic_tilted_*` engine still exists.

## Project Structure

```
src/frasian/
  __init__.py                # public surface: run_experiment, registry, Config
  config.py                  # frozen settings (alpha, grids, eps, seeds)
  _registry.py               # decorators + Registry singleton
  _registry_bootstrap.py     # explicit imports of every concrete impl
  _runner.py                 # cross-product runner + manifest writer
  _errors.py                 # FrasianError, EmptyRegistryError, etc.

  _default_cells.py          # default (tiltings, statistics) cell list, env-var dispatch

  models/
    base.py                  # Model, Prior, Posterior, Likelihood protocols (incl. fingerprint())
    _dispatch.py             # require_model decorator (Normal-only gating)
    distributions.py         # NormalDistribution, GaussianLikelihood, Gaussian/MixtureDistribution
    normal_normal.py         # NormalNormalModel + math primitives

  tilting/
    __init__.py              # Re-exports `TiltingScheme` / `EtaSelector` / `TiltingDomainError` only; concrete schemes are imported via `frasian._registry_bootstrap`.
    base.py                  # TiltingScheme, EtaSelector, TiltingDomainError
    _solvers.py              # ONE brentq_with_doubling
    _dynamic.py              # shared dynamic-η-per-θ CI scan (used by power_law/ot)
    _generic_pvalue.py       # shared generic-MC tilted_pvalue helpers (CRN seed, support resolver)
    _grid_distribution.py    # GridDistribution: tilted-density grid materialiser
    eta_selectors.py         # Fixed / Numerical / DynamicNumerical / LearnedDynamic
    identity.py              # IdentityTilting (no-op identity element)
    power_law.py             # PowerLawTilting (e-geodesic / Theorem 6)
    ot.py                    # OTTilting (W2 geodesic, general 1D + Gaussian fast path)
    quantile_mixture.py      # QuantileMixturePath: 1D W2-geodesic Distribution wrapper
    fisher_rao.py            # FisherRaoTilting (Levi-Civita geodesic on the Gaussian half-plane; Stages A-D)
    mixture.py               # MixtureTilting (m-geodesic / dual partner of power_law)

  statistics/
    base.py                  # TestStatistic + AsymptoticDistribution
    wald.py                  # WaldStatistic
    waldo.py                 # WaldoStatistic
    lrt.py                   # planned stub
    signed_root.py           # planned stub
    bartlett.py              # planned stub

  cd/
    base.py                  # ConfidenceDistribution protocol
    grid.py                  # GridConfidenceDistribution (concrete)
    from_pvalue.py           # universal constructor (p-value → density → CDF)
    from_closed_form.py      # closed-form Wald/WALDO CDs (test fixtures)
    distances.py             # wasserstein_1, wasserstein_2, total_variation

  experiments/
    base.py                  # Experiment, ExperimentContext, RawResult
    coverage.py              # CoverageExperiment
    width.py                 # WidthExperiment
    smoothness.py            # SmoothnessExperiment
    confidence_distribution.py  # ConfidenceDistributionExperiment
    illustrations/           # one demo per registered method
      identity_demo.py, wald_demo.py, waldo_demo.py,
      power_law_demo.py, ot_demo.py, mixture_demo.py, fisher_rao_demo.py,
      learned_eta_demo.py, smoothness_demo.py, confidence_distribution_demo.py

  diagnostics/
    base.py                  # Diagnostic + DiagnosticTable
    coverage_table.py        # CoverageRateDiagnostic
    width_table.py           # MeanWidthDiagnostic
    smoothness_metrics.py    # SmoothnessDiagnostic
    cd_summary.py            # CDSummaryDiagnostic

  simulation/
    storage.py               # npz + json sidecar I/O
    cache.py                 # mandatory content-keyed cache
    raw.py                   # generate_normal_D_samples + RawSamples
    processing.py            # ProcessedResult dataclass
    runner.py                # persist_cell helper

  learned/
    base.py                  # LearnedArtifact protocol
    null.py                  # NullArtifact (for tests)
    eta_artifact.py          # Phase G EtaArtifact (loads dual-head v4 Equinox checkpoint)
    training/
      __init__.py            # public surface: EtaNet, ValidityNet, fit_eta_artifact, ...
      architecture.py        # EtaNet ((θ, prior_hp, lik_hp) → η) + ValidityNet ((θ, prior_hp, lik_hp, η) → logit), GELU MLPs
      losses.py              # integrated_p / cd_variance / static_width + boundary_penalty_from_validity
      validity.py            # is_pair_valid, validity_mask, compute_pvalues_per_sample{,_with_hp}
      sampling.py            # ExperimentConfig (v4), ThetaDistribution, lhs_1d
      hyperparam_distribution.py  # HyperparamDistribution: per-batch (prior_hp, lik_hp) sampler
      pvalue_jax.py          # JAX ports of tilted_pvalue per scheme (autograd path; post-Phase-F port from torch)
      cd_jax.py              # JAX port of CD density (for cd_variance loss)
      train.py               # fit_eta_artifact: dual-head training loop
      _setup.py              # device resolver / x64 / RNG plumbing for fit_eta_artifact
      _train_loop.py         # the training step + eval loop driving optax
      _losses_compose.py     # per-scheme loss composition (NN closed-form + generic-grid)
      _checkpoint.py         # Equinox .eqx file I/O (CHECKPOINT_FORMAT_VERSION = 4)
      _validity_data.py      # offline (θ, prior_hp, lik_hp, η, valid) sampler used to seed Head B

tests/
  conftest.py                # autouse registry isolation + bootstrapped fixture
  properties/                # hypothesis-based protocol invariants (L1)
  regression/                # tight-tolerance baselines (L0/L2)
  experiments/               # end-to-end Experiment runs (L4)
  integration/               # registry + empty-registry checks

docs/
  methods/                   # one .md brief per registered method
    _template.md             # the skeleton /propose-method writes against
    {normal_normal,wald,waldo,power_law,...}.md
  notes/                     # dated empirical findings (results, diagnoses)
    README.md                # convention: when to add a note, naming, format
    YYYY-MM-DD-<slug>.md     # one per finding
  audit/                     # multi-agent audit outputs
  paper/                     # STAMPS@CMU workshop paper writeup — see "Workshop paper writeup" section below
    paper-draft.md           # markdown source (§§1–8 + References, ~450 lines)
    paper.pdf                # pandoc → xelatex compiled output (~31 pages)
    figures/                 # 19 PNGs embedded in the paper
      scripts/               # one matplotlib script per figure (re-runnable)
  superpowers/               # implementation plans (gitignored except plans/)
  workflows.md               # /propose-method lifecycle + cookbook
  jax_style.md               # coding convention for the JAX/Equinox layer

scripts/
  run.py                     # python -m scripts.run [--list] [--fast] experiment=<name>
  figures.py                 # python -m scripts.figures <results_dir>
  train_learned_eta.py       # train Phase G EtaNet+ValidityNet from a v4 experiment YAML
  regen_headline.py          # PYTHONHASHSEED=0 python -m scripts.regen_headline
  run_wald_audit.py          # (NN × tilting × statistic) audit; --flavor pl_learned_intp etc.
  plot_v4_eta_curves.py      # η(θ) diagnostic plot for trained v4 fixtures

experiments/
  canonical_normal_normal_powerlaw_v4.yaml   # Phase G v4 conditional fixture (NN + power_law)
  canonical_normal_normal_ot_v4.yaml         # Phase G v4 conditional fixture (NN + ot)
  canonical_normal_normal_mixture_v4.yaml    # Phase G v4 conditional fixture (NN + mixture)
  canonical_normal_normal_fisher_rao_v4.yaml # Phase G v4 conditional fixture (NN + fisher_rao)

artifacts/                   # trained Phase G v4 checkpoints; gitignored — train locally

tools/
  check_method_completeness.py  # verify brief + tests + illustration per method

.claude/
  agents/                    # skeptic, literature-reviewer, deriver
  commands/                  # /critique, /litreview, /derive, /propose-method

.github/workflows/
  ci.yaml                    # pytest L0-L4 on Python 3.11/3.12
  method-completeness.yaml   # check_method_completeness + smoke runs

legacy/                      # archived original implementation; reference only
```

## Test Layering

| Layer | Purpose                                                  | Tools                  |
|-------|----------------------------------------------------------|------------------------|
| L0    | Scalar math primitives (atol 1e-12)                      | pytest                 |
| L1    | Protocol invariants (continuity, identity, calibration)  | pytest + hypothesis    |
| L2    | Array-result regression vs committed baselines           | pytest + .npz / formula|
| L3    | Statistical (KS uniformity, coverage at nominal level)   | pytest + seeded RNG    |
| L4    | End-to-end Experiment runs on small grids                | pytest                 |
| L5    | Cross-product cells, smoke mode (nightly)                | pytest + parallel      |

Markers replace the legacy `tier1`...`tier5`. Hypothesis lives only in L1.
The L3 calibration check (Wald p-values uniform under H0) lives in
`tests/properties/test_wald_invariants.py`.

## Method Brief Discipline

Every registered class ships with a markdown brief at the path declared in
its decorator. Briefs follow `docs/methods/_template.md` with these
required sections (CI-checked by `tools/check_method_completeness.py`):

1. Summary
2. Motivation
3. Definition
4. Derivation
5. Predicted behavior
6. Failure modes
7. Invariants (mirrored as property tests)
8. Literature
9. Links

The `.claude/` subagents (`skeptic`, `literature-reviewer`, `deriver`),
slash commands (`/propose-method`, `/critique`, `/derive`, `/litreview`),
and GitHub Actions workflows (`ci.yaml` running L0-L4 tests +
`method-completeness.yaml` running `tools/check_method_completeness.py`
plus illustration smoke runs) gate brief / property-test / illustration
completeness on every PR. See `docs/workflows.md` for the full lifecycle.

## Running Things

```bash
# List registered methods
python -m scripts.run --list

# Run an experiment end-to-end (Config.fast() ~ 30s for coverage)
python -m scripts.run --fast experiment=coverage
python -m scripts.run --fast experiment=width
python -m scripts.run --fast experiment=smoothness

# Regenerate figures + CSVs from a persisted results dir
python -m scripts.figures results/coverage

# Run the test suite
python -m pytest                    # ~1480 collected (~25 stub-skips), ~7 min
python -m pytest -m L0              # math primitives only
python -m pytest -m "L0 or L1"      # core + properties
python -m pytest -m L4              # end-to-end
python -m pytest -n auto            # parallel (pytest-xdist)

# Verify method-completeness (briefs, tests, illustrations)
python tools/check_method_completeness.py

# Run an illustration
python -m frasian.experiments.illustrations.power_law_demo --smoke

# Learned-η workflow (Phase G v4)
# 1. Train a v4 conditional fixture (~5 min on CPU)
python -m scripts.train_learned_eta \
    --config experiments/canonical_normal_normal_powerlaw_v4.yaml \
    --out artifacts/learned_eta_canonical_normal_normal_powerlaw_v4.eqx
# 2. Regenerate the headline table (matches v3 beats-Wald margin)
PYTHONHASHSEED=0 python -m scripts.regen_headline
# 3. Audit a learned cell at full Config.fast() w_grid (~5 min)
python -m scripts.run_wald_audit --flavor pl_learned_intp
# 4. Plot η(θ) curves for the trained fixtures
python -m scripts.plot_v4_eta_curves
```

## Notes & Findings

Empirical results, diagnoses, and non-obvious framework decisions
live in `docs/notes/<YYYY-MM-DD>-<slug>.md`. The
[`docs/notes/README.md`](docs/notes/README.md) describes when to add
a note (regression diagnosed, audit run, calibration property
discovered) and when not to (commit-message material, per-method
theory). Index of available notes is maintained in that README.

CLAUDE.md is the orientation document — it documents what exists
and where to look. Findings (numbers, narratives, dated context)
go in `docs/notes/`. Per-method theory + derivations go in
`docs/methods/<name>.md`.

## Workshop paper writeup

A reference document for STAMPS@CMU workshop collaborators lives in
`docs/paper/`. The deliverables are the markdown source
`paper-draft.md` (~450 lines, §§1–8 + References) and the compiled
`paper.pdf` (~31 pages, ~65 references, ~6 MB total tree).

**Sections.** §1 motivation (Prospector-β rare-galaxy shrinkage);
§2 Frasian inference (test inversion + posterior-based statistic →
confidence distributions); §3 the conflict tax (WALDO is calibrated
but inflates under conflict); §4 η-tilting + post-selection +
dynamic tilting; §5 four geodesic schemes (PL/MX/FR/OT); §6 cross-θ
objective + learned dual-head selector; §7 experimental matrix
(audit slices on `run_wald_audit`); §8 discussion (back to
Prospector-β, beyond NN, open questions).

**Three-stage construction.**

- **Stage 1** (outline + narrative spine): `docs/superpowers/specs/2026-05-12-adaptive-frasian-paper-outline-design.md`. Gitignored (per `docs/superpowers/` convention).
- **Stage 2** (derivations + literature, ~30 pages, ~60 references, deriver/litreview-verified): `docs/superpowers/specs/2026-05-12-adaptive-frasian-paper-stage2-details.md`. Gitignored.
- **Stage 3** (figures, tables, polished prose): `docs/paper/` (tracked).

**Figures.** 19 figures at `docs/paper/figures/`, each with a
re-runnable script at `docs/paper/figures/scripts/fig_<sec>_<n>_<slug>.py`.
Experimental-data figures (F3.1, F3.2, F4.2, F7.1–F7.3) read CSVs
from `results/wald_audit/*/{coverage,width,smoothness}/*.csv`.
Learned-η figures (F6.2, F6.4) load v4 fixtures from `artifacts/`.
Pedagogical figures (F1.1, F2.1–F2.4, F4.1, F4.3, F4.4, F5.1, F5.2)
generate from closed-form NN+Normal math.

**PDF compilation.** From repo root:

```bash
cd docs/paper && python3 -c "
import pypandoc
pypandoc.convert_file('paper-draft.md', 'pdf', outputfile='paper.pdf',
    extra_args=['--pdf-engine=xelatex',
                '-V', 'geometry:margin=1in',
                '-V', 'mainfont=DejaVu Serif'])"
```

`DejaVu Serif` (Unicode-capable) is required for the Greek letters in
the prose (η, θ, σ, μ); Computer Modern would print missing-glyph
boxes outside math mode. Pandoc itself is not installed; `pypandoc_binary`
bundles its own.

**Conventions in the paper.** η-convention follows the codebase
(η=0 ⇔ WALDO, η=1 ⇔ Wald). Inline citations use informal
`[Author Year]` style; full bibliographic detail is in the
References section at the end of the document, aggregated
alphabetically from Stage 2.

## Cache Discipline

The cache at `<results_dir>/cache/` keys on `(experiment, tilting,
statistic, config_fingerprint, git_sha, raw_fingerprint, extra)` →
24-char SHA-256 digest. **Dirty git trees never hit the cache** —
uncommitted changes always recompute. Same `(config, sha)` on a
clean tree is byte-reproducible.

**Gitignored-artifact policy.** `git status --porcelain` ignores
gitignored paths, so swapping a checkpoint at
`artifacts/learned_eta_*_v1.eqx` (a gitignored production
artifact) does **not** flip the tree to dirty and the cache key
does not move on `git_sha` alone. Invalidation in that case hinges
on `selector_artifact_fingerprint` (24-char digest of the artifact
file) being plumbed into the cache key via the cell's `extra`
dict — the `_runner` does this automatically for any selector
that exposes `.artifact.fingerprint()`. If you train a fresh
`v1` artifact, the next cache lookup returns a miss and recomputes;
if the runner cannot read the fingerprint (artifact removed mid-
run, fingerprint method raises), it bails to a recompute. Never
edit a checkpoint file in place — replace atomically. Pinned by
`tests/regression/test_cache_learned_invalidation.py`.

## Migration Status

| Step | Status | Description                                                     |
|------|--------|-----------------------------------------------------------------|
| 1    | done   | Scaffolding: protocols, registry, Config, empty-registry runner |
| 2    | done   | Wald + WALDO + power_law + NormalNormalModel + briefs + demos   |
| 3    | done   | simulation/ (storage, cache, raw, runner) + LearnedArtifact     |
| 4    | done   | CoverageExperiment + WidthExperiment + diagnostics + figures.py |
| 5    | done   | SmoothnessExperiment quantifying the power-law discontinuity    |
| 6    | done   | Stubs: OT / geodesic / mixture / exp_family / LRT / SR / BCLRT  |
| 7    | done   | .claude/ subagents + slash commands + GitHub Actions CI gates   |
| 8    | done   | Selector-as-tilting-member refactor: IdentityTilting + accepts_tilting + uniform `tilting.confidence_interval`; dynamic_ci subsumed by coverage/width |
| 9    | done   | Geodesic taxonomy refactor: `ot_normal`→`ot` (general 1D W2 + Gaussian fast path implemented); `geodesic_normal`→`fisher_rao` (renamed stub); `exp_family` dropped (redundant with `power_law` on conjugate exp-families); `mixture` reframed as m-geodesic / dual partner of `power_law`'s e-geodesic |
| 10   | done   | Phase E learned-η rewrite: model-agnostic dual-head selector (`EtaNet` + `ValidityNet`) trained per-experiment; replaces Phase D `MonotonicEtaNet` (deleted). `EtaNet`: smooth GELU-MLP from raw θ → η, no monotonicity prior, no bounded sigmoid. `ValidityNet`: learns `P(valid \| θ, η)` from observed `(θ, η, valid)` triples; provides `-log P(valid)` boundary penalty for Head A. Per-experiment fingerprints (`Prior.fingerprint()`/`Model.fingerprint()`) + strict cross-experiment refusal. New `ExperimentConfig` YAML schema. Smoke fixtures `learned_eta_canonical_normal_normal_<scheme>_v0_smoke.eqx` committed for `power_law` and `ot` (Equinox `.eqx` format after the Phase F JAX port; `.pt` torch checkpoints are gone). |
| 11   | done   | Phase G conditional learned-η: `EtaNet` and `ValidityNet` now take `(θ, prior_hp, lik_hp)` / `(θ, prior_hp, lik_hp, η)` instead of θ / (θ, η). Each checkpoint is trained over a *range* of `(prior_hp, lik_hp)` (the `hyperparam_distribution` block in the v4 YAML); the selector dispatches per-inference and refuses out-of-range hyperparams. Checkpoint format bumped 3 → 4. v3 YAMLs / fixtures / 14 v3-bound tests deleted; v4 YAMLs added; v4 fixtures gitignored (re-train via `scripts.train_learned_eta`). `eta_explore_box` restored to ExperimentConfig (per-config; defaults to `[-5, 5]`). Headline numbers in this file updated to the v4 fixture. |
| 12   | done   | Phase G v4 fix: σ₀-anchored θ training + input normalization (default ON) + clamp-instead-of-refuse on out-of-admissible η. See [`docs/notes/2026-05-09-phase-g-v4-fix.md`](docs/notes/2026-05-09-phase-g-v4-fix.md). |
| 13a  | done   | MixtureTilting (m-geodesic) Stage A+B: closed-form NN tilt + WALDO p-value via quadratic-roots branching + GaussianMixtureDistribution / MixtureDistribution + generic-MC path + 4 selectors + 9 mx_* audit flavors. Briefs + tests + minimal illustration. See `docs/methods/mixture.md` and `docs/notes/2026-05-09-mixture-smoothness-and-learned-eta-tails.md`. |
| 13b  | partial limitation | Phase G v4 `integrated_p` training produces near-constant per-cell η across all four schemes (median per-cell std ~5e-4, cross-cell spread 0.10-0.20). Other losses (`cd_variance`, `static_width`) can produce stronger adaptation on specific scheme combinations (FR cd_variance: spread 1.43; PL static_width: spread 0.78) but most non-integrated_p fixtures still show modest per-cell stds (1e-3 to 4e-3). The architecture **is** capable of input-sensitive learning; the limitation is loss-specific to integrated_p, not architectural. See [`docs/notes/2026-05-11-row-13b-loss-specificity-cross-scheme.md`](docs/notes/2026-05-11-row-13b-loss-specificity-cross-scheme.md). |
| 13c  | done   | Mixture EtaNet structural sigmoid bound. EtaNet supports `output_bounds: tuple[float, float] \| None`; `train.py` dispatches `(0.0, 1.0)` for `scheme=="mixture"`, `None` otherwise (no-op for PL/OT). Fixes the cd_variance boundary-attractor pathology: pre-bound mx_learned_cd_var had coverage 0.22-0.93 (catastrophic), post-bound 0.955-0.965 (calibrated). cd_var val 13.57 → 1.25, η_valid 0.811 → 1.000. Bound is no-op for mx intp/static_w (their optima already in [0, 1]). See [`docs/notes/2026-05-10-mixture-cd-variance-instability.md`](docs/notes/2026-05-10-mixture-cd-variance-instability.md). |
| 14   | done   | FisherRaoTilting (Levi-Civita / Riemannian geodesic on the Gaussian half-plane) implemented end-to-end across Stages A-D: closed-form NN tilt + WALDO p-value via half-plane geodesic (Stage A), generic autodiff path via diffrax shooting BVP (Stage B), Phase G v4 learned-η training across all 3 loss heads (integrated_p / cd_variance / static_width) with FR cd_var hyperparam regime fix (Stage C), and 4×4 schemes-vs-selectors smoothness comparison (`scripts/compare_geodesic_smoothness.py` + 32-row CSV; Stage D). Headline finding: FR/MX/OT all produce smoother CI-width(D) than PL on Lipschitz/TV/spectral metrics by 3-100×, but FR `dyn_numerical` collapses to bare WALDO at w=0.5 (per-θ static optimum η=0). See [`docs/notes/2026-05-11-fisher-rao-vs-others-smoothness.md`](docs/notes/2026-05-11-fisher-rao-vs-others-smoothness.md). Post-merge `run_wald_audit` populated all 16 (4 schemes × 4 selectors) cells: all calibrated (mean cov 0.953-0.959); on tail-max CI-width at the conflict band, **OT learned cells are tightest** (`ot[learned_cd_var]` at +13% over Wald; OT occupies 3 of the top 4 ranks) followed by `pl[learned_cd_var]` (+18%) and `fr[learned_static_w]` (+25%). `fr[learned_cd_var]` is pathological (+135% — trained negative-η produces wide CIs even unclamped); `fr[dyn_numerical]` reproduces bare WALDO. Full table in [`docs/notes/2026-05-12-cross-scheme-wald-audit.md`](docs/notes/2026-05-12-cross-scheme-wald-audit.md). |
| 15   | done   | (TiltingScheme × {lrto, scoreo}) cross-product wired up: trinity collapse routes PL/OT/FR through waldo arithmetic on closed-form NN+Normal; MX uses analytic 2-Gaussian-mixture stats + MC over D'; generic-MC path supports lrto/scoreo for all 4 schemes via grid-distribution τ helpers (`_grid_tau_lrto` / `_grid_tau_scoreo`); JAX training kernels accept lrto/scoreo for PL/OT/FR (mixture explicit N/A — 2-Gaussian-mixture mode-finder not JAX-traceable). 24 new audit flavors in `scripts/run_wald_audit.py`. See [`docs/notes/2026-05-12-tilted-trinity-derivation.md`](docs/notes/2026-05-12-tilted-trinity-derivation.md). |

## Easily-Conflated Distinctions (read before diagnostic work)

When investigating learned-η or tilting losses, four distinctions are
easy to get wrong and produce reversed conclusions. Full discussion in
[`docs/notes/2026-05-10-eta-conventions-and-loss-derivation.md`](docs/notes/2026-05-10-eta-conventions-and-loss-derivation.md).
Headlines:

- **η = 0 is WALDO, η = 1 is Wald** in `power_law_tilted_pvalue_jax`.
  At η=1 the prior cancels (`mu_eta = D`, `b = 0`, `p = 2Φ(−|D−θ|/σ)`);
  at η=0 the full prior is in. The naming feels backwards. Always
  verify which η value you mean when comparing to "Wald".
- **`integrated_p` loss = average CI width across all α-levels**:
  `∫ p(θ) dθ = ∫₀¹ W(α) dα` by Fubini. The framework's σ₀-anchored
  truncation makes "Wald loss" appear σ₀-dependent (purely an
  integration-domain artifact — the Wald CI width 2zσ does not change).
- **Per-θ_test argmin η ≠ per-θ_true argmin η**. The integrated_p
  loss decomposes as `∫ G(θ_test, η(θ_test)) dθ_test`, so the
  function-constrained optimum is the per-θ_test argmin (independent
  at each integration point), NOT the per-θ_true argmin.
- **The framework's hypothesis is η(θ_test) U-shaped**: small near μ₀
  (use prior to tighten CI), → 1 far from μ₀ (Wald fallback when prior
  is uninformative). v4 fixtures train on σ₀-anchored θ_test (entirely
  inside prior support) and so cannot have learned the
  far-from-μ₀ behavior. Evaluating v4 on a likelihood-anchored grid
  is an extrapolation test, not a framework-correctness test. Out-of-
  distribution behavior should ideally clamp to η=1.

## Key Anti-Patterns to Avoid

- Importing from `frasian.models.normal_normal` outside `frasian/models/`.
  Other modules go through the `Model` protocol; the discipline keeps the
  framework extensible.
- Module-level mutable state. The legacy `_get_optimal_eta_predictor`
  global is replaced by an injected `LearnedArtifact`.
- Bypassing the cache. Every script goes through `simulation.cache.
  get_or_compute`; the legacy plot scripts that recomputed grids in the
  module body are gone.
- Using α≠0.05 in one place and 0.05 elsewhere. All α values come from
  `Config.alpha`; tests override via `Config.from_overrides(alpha=...)`.
- Adding a method without its brief, property tests, and illustration —
  the completeness check blocks merge.
