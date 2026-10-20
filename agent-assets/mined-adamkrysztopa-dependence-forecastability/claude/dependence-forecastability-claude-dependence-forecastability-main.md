<!-- type: reference -->

# Claude Code — Working in `dependence-forecastability`

Claude-Code-specific working instructions on top of the canonical
[`.github/copilot-instructions.md`](.github/copilot-instructions.md).
For repo-wide rules (deterministic triage first, framework-agnostic core,
forecast-prep contract as the hand-off boundary, etc.) defer to that file.

## Orchestrator-led workflow (binding)

> [!IMPORTANT]
> For **any** code change, plan revision, review, or release operation in this
> repo, **dispatch the `orchestrator` subagent first**. Even a one-line fix
> passes through the orchestrator so concern screens, routing, and stage gates
> are enforced consistently.
>
> Direct work (without orchestrator) is acceptable only for:
> - read-only investigation that produces no edits and no plans
> - answering a factual question that doesn't touch files
> - executing a slash-command skill that's explicitly scoped (`/superpowers:*`,
>   `/skill-creator:*`, etc.)

## Subagent roster (`.claude/agents/`)

| Agent | Owns |
|---|---|
| `orchestrator` | Decomposition, routing, concern screens, stage gates. Never writes code. |
| `coder` | Python implementation: `src/`, `tests/`, `scripts/`, `configs/`, `pyproject.toml` |
| `tester` | Repository-wide verification (`uv run ruff check . && uv run ty check && uv run pytest -q -ra`) |
| `statistician` | Math correctness: MI / pAMI / GCMI / KSG-CMI / TE / surrogate / FWER / calibration |
| `analyst` | Script execution, output verification, triage-result interpretation |
| `reporter` | Reports in `outputs/reports/` with mandatory disclosures |
| `documenter` | `docs/`, `README.md`, CHANGELOG, Mermaid, ADRs, migration guides |
| `rubber_duck` | **Narrow** concern screen (≤ 5 risks): contract, data model, control flow, dependency, test adequacy |
| `software_architect` | Layering, SOLID, hex boundary, public-API surface, refactor design |
| `devops` | `.github/workflows/`, packaging, PyPI Trusted Publishing, pre-commit, Dependabot, release-tag |
| `performance_engineer` | KSG hot loops, batched FFT, joblib backends, PBE-F* perf budgets, request-scoped caching |
| `release-planner` | Plans under `docs/plan/` matching `docs/plan/planning_template.md` style |

The roster mirrors `.github/agents/` for parity with the GitHub Copilot
chatagent setup. `rubber_duck` is genuinely high-signal — use it liberally
for pre-merge screens. `performance_engineer` was added on top of the
Copilot roster because efficiency is the weakest dimension flagged by the
v0.4.3 deep audit ([`docs/reviews/v0.4.3-deep-audit.md`](docs/reviews/v0.4.3-deep-audit.md)).

## Source-of-truth order

1. [`docs/plan/planning_template.md`](docs/plan/planning_template.md) — release-plan structure
2. [`docs/plan/acceptance_criteria.md`](docs/plan/acceptance_criteria.md) — non-negotiable invariants
3. Most recent plans (both complete, under `docs/plan/implemented/`) —
   [`v0_5_1_finish_hex_migration_plan.md`](docs/plan/implemented/v0_5_1_finish_hex_migration_plan.md)
   and [`v0_5_0_review_hardening_ultimate_plan.md`](docs/plan/implemented/v0_5_0_review_hardening_ultimate_plan.md)
4. [`docs/reviews/v0.4.3-deep-audit.md`](docs/reviews/v0.4.3-deep-audit.md) — standing review punch list
5. [`.github/copilot-instructions.md`](.github/copilot-instructions.md) — repo-wide engineering rules

## Verification commands

```bash
uv run ruff check .       # lint
uv run ty check           # type check
uv run pytest -q -ra      # full test suite
```

Never wrap `pytest` in `2>&1 | tail`, `| grep`, `| tee`, or any redirection.
Read pytest output and exit status directly.

## Critical invariants (also enforced by `orchestrator`)

- AMI / pAMI computed **per horizon h separately**; never aggregated before computation
- AMI / pAMI on `split.train` only inside a rolling-origin loop
- `np.trapezoid` for AUC — `np.trapz` is removed in NumPy 2
- `random_state: int` — never `numpy.Generator`
- `n_surrogates >= 99` at every surrogate entry point
- Surrogate phase-randomization preserves Hermitian symmetry (DC + Nyquist phase 0)
- `directness_ratio > 1.0` is a warning boundary, not positive evidence
- Frozen Pydantic at every public boundary; no `dict[str, Any]` on result types
- Determinism: `SeedSequence.spawn` propagation; serial-vs-parallel bit identity
- No `darts` / `mlforecast` / `statsforecast` / `nixtla` in the core package
- pAMI is a **linear approximation** to conditional MI — note in any write-up
- Project extensions (pAMI, agents, etc.) are not paper-native guarantees or causality proofs

## When dispatching the orchestrator

Pass the orchestrator:

- the **task** in 1-2 sentences (what changes, why, scope)
- **specific files or modules** touched (if known)
- the **active release plan** the work lands in (if applicable)
- any **risk you've already screened** for (so the orchestrator doesn't re-screen)

The orchestrator returns a routing decision: which specialist(s), in what
order, with what stage gates between them. Follow the routing.

## Anti-patterns

- ❌ Editing `src/forecastability/` without dispatching `orchestrator` first
- ❌ Drafting a release plan without `release-planner`
- ❌ Approving a math change without `statistician` sign-off
- ❌ Merging a hot-loop rewrite without `performance_engineer` + `tester` (PBE-F*) involvement
- ❌ Cutting a release without `devops` running the Phase-6 checklist
- ❌ `dict[str, Any]` on a public boundary
- ❌ Adding to `_DOMAIN_FORBIDDEN` via a `# TODO` exclusion in `tests/test_architecture_boundaries.py`
