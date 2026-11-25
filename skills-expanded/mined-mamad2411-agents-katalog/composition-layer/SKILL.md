---
name: composition-layer
description: >
  Layer-3 (PORTFOLIO) cross-sectional construction pipeline for the
  feelies platform. Owns the `PortfolioAlpha` protocol, the
  `UniverseSynchronizer` fan-in, the `CrossSectionalRanker` (with
  optional decay weighting), `FactorNeutralizer`, `SectorMatcher`,
  the cvxpy-based `TurnoverOptimizer`, and the `CompositionEngine`
  that emits `SizedPositionIntent`. Use when authoring PORTFOLIO
  alphas, designing cross-sectional construction, debugging
  mechanism-cap enforcement, factor-loading ingestion, or the
  L3 sized-intent parity contract.
---

# Composition Layer — Layer 3 Cross-Sectional Construction

The Layer-3 PORTFOLIO layer is **cross-sectional**: a portfolio alpha
sees the entire declared universe at once and is responsible for
inter-symbol weight construction (factor neutralization, sector
matching, turnover optimization, mechanism capping). It bypasses the
per-symbol `IntentTranslator` and instead emits a typed
`SizedPositionIntent` per `(alpha_id, horizon_seconds, boundary_index)`,
which the risk engine decomposes into per-leg `OrderRequest`s with
**per-leg veto** semantics (Inv-11).

`PortfolioAlpha` instances are loaded from `*.alpha.yaml` files with
`layer: PORTFOLIO`. The PORTFOLIO layer is gated on
`AlphaRegistry.has_portfolio_alphas()` at bootstrap — if no PORTFOLIO
alpha is registered, no composition components are constructed.

## Core Invariants

Inherits Inv-5 (deterministic replay), Inv-6 (causality), Inv-11
(fail-safe), Inv-13 (provenance). Additionally:

1. **Cross-sectional contemporaneity** — `CrossSectionalContext`
   carries only `Signal` events from the same horizon boundary; no
   look-ahead, no stale-window mixing.
2. **Mechanism-cap enforcement** — every `SizedPositionIntent`
   carries a typed `mechanism_breakdown: dict[TrendMechanism, float]`.
   Per-family `max_share_of_gross` declared on the alpha YAML is
   validated by G16 at load time (see the ranker section below for
   the runtime-enforcement gap).
3. **Replay-parity over intents** — replay determinism is verified by
   the L3 sized-intent stream parity hashes
   (`tests/determinism/test_sized_intent_with_decay_replay.py`
   compares full intent streams); provenance lives in
   `target_positions` + `mechanism_breakdown` + `correlation_id`.
4. **Per-leg veto on risk** — the risk engine evaluates each leg of
   the intent independently; a single vetoed leg never aborts the
   intent.
5. **Replay byte-identical emission order** — contexts are keyed by
   `(horizon_seconds, boundary_index)`; the engine iterates registered
   alphas sorted by `(horizon_seconds, alpha_id)` so the downstream
   engine emits intents in a stable order.

---

## Pipeline

```
Signal[symbol_i] (Layer 2, multiple symbols, same boundary)
  → UniverseSynchronizer fan-in
    → CrossSectionalContext(horizon_seconds, boundary_index, universe,
                            signals_by_symbol, signals_by_strategy_by_symbol,
                            snapshots_by_symbol, completeness)
      → CompositionEngine._on_context(ctx)  (bus-subscribed handler)
        → PortfolioAlpha.construct(ctx, params)
          → CrossSectionalRanker (raw scores)
            → FactorNeutralizer (factor exposures)
              → SectorMatcher (long/short sector pairing)
                → TurnoverOptimizer (cvxpy QP, optional)
                  → mechanism-cap enforcement
                    → SizedPositionIntent(target_positions, mechanism_breakdown,
                                          correlation_id)
                      → bus.publish(intent)
                        → RiskEngine.check_sized_intent (per-leg veto)
                          → per-leg OrderRequest with reason="PORTFOLIO"
```

Implementation files: `feelies.composition.{protocol, synchronizer,
engine, cross_sectional, factor_neutralizer, sector_matcher,
turnover_optimizer}`.

---

## `PortfolioAlpha` Protocol

```python
class PortfolioAlpha(Protocol):
    @property
    def alpha_id(self) -> str: ...
    @property
    def horizon_seconds(self) -> int: ...

    def construct(
        self,
        ctx: CrossSectionalContext,
        params: Mapping[str, Any],
    ) -> SizedPositionIntent: ...
```

(`src/feelies/composition/protocol.py`; `universe` and
`depends_on_signals` live on the alpha YAML / loaded module, not on
the protocol.)

`construct` is a **pure function**. The `CrossSectionalContext`
carries the most-recent `Signal` per symbol (and per upstream
strategy via `signals_by_strategy_by_symbol`) within the context's
`universe` for the current `boundary_index`. `TargetPosition` is a
value object with signed `target_usd: float` and an `urgency` hint
(0..1); mechanism provenance lives on the consumed `Signal`s and the
intent's `mechanism_breakdown`, not on `TargetPosition`.

`G10` (PORTFOLIO universe presence) and `G11` (factor-neutralization
disclosure) gate alpha load.

---

## `UniverseSynchronizer`

`composition/synchronizer.py` publishes one `CrossSectionalContext`
per `(horizon_seconds, boundary_index)` pair, fanning in the most
recent `Signal` per symbol within the universe. The engine
dispatches the same context to **all** PORTFOLIO alphas registered
on that horizon.

```python
@dataclass(frozen=True, kw_only=True)
class CrossSectionalContext(Event):
    horizon_seconds: int
    boundary_index: int
    universe: tuple[str, ...]
    signals_by_symbol: dict[str, Signal | None]
    signals_by_strategy_by_symbol: dict[str, dict[str, Signal | None]]
    snapshots_by_symbol: dict[str, HorizonFeatureSnapshot | None]
    completeness: float   # fraction of universe with non-stale signal
```

### Completeness Gate

Portfolio alphas may opt-out of low-completeness boundaries via
`composition_completeness_threshold` in `platform.yaml` (default
`0.80`). The synchronizer **always emits** the context; below
threshold the `CompositionEngine` publishes a degenerate empty
`SizedPositionIntent` ("hold existing positions") rather than
silently dropping the decision.

### Emission Order

Contexts are keyed by `(horizon_seconds, boundary_index)`; the
engine iterates registered alphas sorted by
`(horizon_seconds, alpha_id)` so cross-sectional construction is
replay-byte-identical (Inv-5; locked by L3 + L3-orders parity tests).

---

## `CrossSectionalRanker`

`composition/cross_sectional.py` ranks symbols by raw alpha score
from `Signal.strength × sign(direction) × edge_estimate_bps`, then:

1. **Optional decay weighting** (Phase 4.1) — when
   `decay_weighting_enabled: true` in the PORTFOLIO alpha's
   `parameters:` block, multiplies each symbol's raw score by
   `exp(-age_s / hl)` where
   `age_s = (ctx.timestamp_ns - signal.timestamp_ns) / 1e9` and
   `hl = signal.expected_half_life_seconds` (in seconds). The decay
   multiplier is clamped below by `decay_floor` — a
   `CrossSectionalRanker` constructor argument defaulting to `1e-6`;
   bootstrap wires only `decay_weighting_enabled` from alpha params
   (`bootstrap.py`). Decay weighting is **additive** —
   it does not change structural ranking semantics, only the relative
   emphasis of fresh vs stale signals. Produces a different
   `SizedPositionIntent` stream from the decay-OFF baseline (verified
   by the Level-3 decay-ON parity test,
   `tests/determinism/test_sized_intent_with_decay_replay.py`).
   Platform budget: ≤ 5 % wall-clock regression.
2. **Standardisation** — robust z-score across the universe.
3. **Mechanism-cap enforcement** — when any `TrendMechanism` family
   would exceed the ranker's `mechanism_max_share_of_gross`, scales
   that family's contribution proportionally before re-normalizing
   the gross. **Known gap**: G16 PORTFOLIO rule 8 validates the
   `trend_mechanism.consumes[*].max_share_of_gross` declaration at
   LOAD time, but bootstrap builds the `CrossSectionalRanker` with
   the default `mechanism_max_share_of_gross=1.0` (cap disabled) and
   does not pass the alpha-declared caps through — runtime
   enforcement of alpha YAML caps is not wired today.

Output: a public `RankResult` value object
(`feelies.composition.cross_sectional.RankResult`, exported in
`__all__`) carrying ranked alphas and the realised
`mechanism_breakdown: dict[TrendMechanism, float]`. `RankResult` is
not a bus event — it is consumed in-process by `CompositionEngine`.

---

## `FactorNeutralizer`

`composition/factor_neutralizer.py` reads a loadings artifact from
`loadings_dir/loadings.json` (schema `{symbol: {factor_name: float}}`;
`factor_loadings_max_age_seconds` guard at bootstrap) and projects
the ranked weights onto the factor-neutral subspace. Factors
typically include: market beta, size, value, momentum, sector
dummies.

`MissingFactorLoadingsError` is raised at construction when the
loadings **file** is missing or unreadable; symbols or factors absent
from the file are zero-filled rather than erroring. G11 gates the
boolean disclosure of whether the alpha opts into factor
neutralization.

The platform refuses to load factor loadings older than
`factor_loadings_max_age_seconds` (default 7 days = 604800 s). Stale
loadings → bootstrap failure (Inv-11).

---

## `SectorMatcher`

`composition/sector_matcher.py` enforces long-short sector pairing
when `PlatformConfig.sector_map_path` is set (a JSON file mapping
`{symbol: sector_id}`); there is no alpha YAML flag — with no sector
map the matcher is a no-op. Symbols are bucketed by sector code;
per-sector net exposure is constrained.

---

## `TurnoverOptimizer` (Optional)

`composition/turnover_optimizer.py` is a cvxpy-based QP that
penalizes turnover against the previous boundary's intent. Activated
by the `[portfolio]` install extra (`pip install -e ".[portfolio]"`,
which pulls `cvxpy`, `ecos`, `pyarrow`).

Without the extra, PORTFOLIO alphas still load and run: the default
`require_solver=False` falls back to a deterministic closed-form
rescale — no bootstrap failure. `MissingOptionalDependencyError` is
raised only when `require_solver=True` and cvxpy is absent.

`OptimizerResult` carries optimised dollar targets and a solver
status code. A CVXPY solve exception logs a warning and falls back
to the closed-form rescale; a non-OPTIMAL solver status logs a
warning and returns an empty allocation. No `Alert` event is emitted
in either case.

---

## `CompositionEngine`

`composition/engine.py` is **bus-driven**: `attach()` subscribes the
private `_on_context` handler to `CrossSectionalContext` events
(there is no public `evaluate`); the orchestrator enters the
`CROSS_SECTIONAL` sub-state separately.

Responsibilities (per context, per registered alpha on that horizon):

1. Skip alphas whose `horizon_seconds` doesn't match the context
2. If `context.completeness < composition_completeness_threshold`,
   publish a degenerate empty `SizedPositionIntent` (hold positions)
3. Call `PortfolioAlpha.construct(ctx, params)`
4. Run the construction pipeline (rank → neutralize → sector → optimize → cap)
5. Patch in the deterministic envelope (timestamp, sequence,
   correlation_id, per-symbol disclosed cost)
6. Publish on the bus → `RiskEngine.check_sized_intent` consumes it

`SizedPositionIntent.correlation_id =
f"intent:{alpha_id}:{horizon_seconds}:{boundary_index}"` (degenerate
intents append `":degenerate"`) provides forensic lineage; per-leg
`OrderRequest`s inherit this so post-trade attribution can recover
the intent.

---

## `SizedPositionIntent`

```python
@dataclass(frozen=True, kw_only=True)
class SizedPositionIntent(Event):
    strategy_id: str
    layer: Literal["PORTFOLIO"] = "PORTFOLIO"
    horizon_seconds: int = 0
    target_positions: dict[str, TargetPosition]       # symbol → target_usd + urgency
    factor_exposures: dict[str, float]
    expected_turnover_usd: float
    expected_gross_exposure_usd: float
    mechanism_breakdown: dict[TrendMechanism, float]  # gross-share per family
    disclosed_cost_total_bps_by_symbol: dict[str, float]
```

The `mechanism_breakdown` is the audit trail for G16 caps and the
input axis to `MultiHorizonAttributor` for per-mechanism PnL
decomposition. **Mechanism concentration** (the realised gross-share
of any single family) drives the post-trade crowding diagnostic.

---

## Layer Gates Specific to PORTFOLIO

| Gate | Check |
|------|-------|
| G10 | `universe:` is a non-empty list of non-empty strings (the universe-size cap is bootstrap's `composition_max_universe_size`, not G10) |
| G11 | `factor_neutralization:` declared as a boolean (`true` opts into the platform factor model; `false` is an explicit opt-out) |
| G12 | `cost_arithmetic:` declared (margin_ratio ≥ 1.5; reconciles ±5%) |
| G14 | `depends_on_signals:` references registered SIGNAL alpha IDs |
| G16 (PORTFOLIO rule 8) | Every consumed mechanism family declares `max_share_of_gross`; sum ≤ 1.0; family whitelist matches upstream `Signal.trend_mechanism` values |

---

## Determinism (Inv-5)

The composition layer contributes four entries to the eleven-baseline
parity-hash registry (`tests/determinism/parity_manifest.py`); the full
list across all layers lives in the testing-validation skill.

| Test | Locks |
|------|-------|
| `tests/determinism/test_horizon_feature_snapshot_replay.py` | L3 — ordered `HorizonFeatureSnapshot` stream byte-identical (Layer-2 input) |
| `tests/determinism/test_sized_intent_replay.py` | L3 — ordered `SizedPositionIntent` stream byte-identical (decay OFF) |
| `tests/determinism/test_sized_intent_with_decay_replay.py` | L3 — ordered `SizedPositionIntent` stream byte-identical (decay ON; compares full intent streams, which must differ from the decay-OFF baseline while structural ranking is unchanged) |
| `tests/determinism/test_portfolio_order_replay.py` | L4 — per-leg `OrderRequest` from PORTFOLIO byte-identical (lex-sorted by symbol) |

---

## Configuration (`platform.yaml`)

```yaml
composition_completeness_threshold: 0.80  # below this the engine emits a degenerate empty intent
composition_max_universe_size: 50         # PORTFOLIO universe cap (bootstrap, not G10)
factor_loadings_max_age_seconds: 604800   # 7 days; stale → bootstrap fail
```

---

## Failure Modes

| Failure | Detection | Response |
|---------|-----------|----------|
| Stale factor loadings | `factor_loadings_max_age_seconds` exceeded at bootstrap | Bootstrap fail (Inv-11) |
| Cvxpy unavailable | `MissingOptionalDependencyError` only when `require_solver=True` | Default `require_solver=False` → closed-form fallback; no bootstrap failure |
| Solver non-OPTIMAL | `OptimizerResult.solver_status` | Log warning; solve exception → closed-form fallback; non-OPTIMAL status → empty allocation (no `Alert`) |
| Mechanism cap unreachable | G16 load-time check | Reject alpha load |
| Missing / empty `universe:` list | G10 | Reject alpha load |
| Low completeness | `context.completeness < threshold` | Emit degenerate empty `SizedPositionIntent` (hold positions); log |

---

## Integration Points

| Dependency | Interface |
|------------|-----------|
| Microstructure Alpha | `Signal` events (with `trend_mechanism`, `expected_half_life_seconds`) — input |
| Risk Engine | `check_sized_intent` per-leg veto — output consumer |
| System Architect | `Clock`, `EventBus`, `CROSS_SECTIONAL` sub-state, `CrossSectionalContext` event |
| Storage Layer | Reference factor loadings (`loadings.json` in `factor_loadings_dir`) |
| Testing & Validation | L3 + L3-orders parity hashes; decay-on/off cross-check |
| Post-Trade Forensics | `mechanism_breakdown` for crowding diagnostics; `MultiHorizonAttributor` per-mechanism axis |

The composition layer is the only path that constructs cross-sectional
weights. Per-symbol SIGNAL alphas never produce sized positions —
they emit `Signal` events that PORTFOLIO alphas optionally consume.
