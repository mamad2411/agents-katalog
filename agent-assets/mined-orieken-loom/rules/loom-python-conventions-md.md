# Python Conventions

Grounded in `saturday-monorepo-python` (the not-yet-published Python port of Saturday) — confirmed
2026-07-07 against that repo's own README, not assumed.

## Project Tooling
- **Package & workspace manager**: [`uv`](https://github.com/astral-sh/uv) (v0.11+) — `uv sync` to
  install, `uv run <command>` to execute inside the managed environment.
- **Linter & formatter**: [`ruff`](https://github.com/astral-sh/ruff) — `ruff check .` for linting,
  `ruff format .` for formatting. One tool for both, replaces the old flake8+black+isort combo.
- **Async-first**: this stack is asynchronous by default — prefer `async`/`await` APIs over sync
  wrappers where a library offers both.

## Project Structure
Saturday's own Python port is workspace-based (`packages/` with one directory per publishable
component — `saturday-core`, `saturday-bdd`, `saturday-certs`, `saturday-k6-exporter`,
`saturday-k6-redaction`, `saturday-otel`, `saturday-ml`, `saturday-swagger`). For a general application
(not a Saturday port itself), follow the same principle at smaller scale: one `pyproject.toml` at the
root, source under `src/<package_name>/`, tests under `tests/` mirroring the source tree.

## Testing & QA Tooling
- **Unit / integration testing framework**: [`pytest`](https://pytest.org/) with
  [`pytest-asyncio`](https://github.com/pytest-dev/pytest-asyncio) for async test support.
- **BDD**: [`pytest-bdd`](https://github.com/pytest-dev/pytest-bdd) — Gherkin `.feature` files
  integrated directly into pytest, the Python-ecosystem parallel to Cucumber.js/Reqnroll/Cucumber-JVM
  in the other Saturday ports.
- **Browser automation**: [`playwright`](https://playwright.dev/python/) (async API) — official
  Microsoft-maintained binding.
- **Fake/synthetic data (faker-equivalent)**: [`Faker`](https://faker.readthedocs.io/) (PyPI package
  `Faker`, `from faker import Faker`) — the standard, official Python faker library.
- **Factories / fixtures (fishery-equivalent)**: given this stack's async-first, type-safe philosophy,
  PREFER [`polyfactory`](https://github.com/litestar-org/polyfactory) — modern, Pydantic-native, and
  async-friendly, a better fit than the classic alternative below for this specific stack.
  [`factory_boy`](https://factoryboy.readthedocs.io/) is the more established, widely-known Python
  factory library (the origin of the "factory" naming pattern `fishery`/`factory-go` are modeled after)
  and remains a reasonable choice for a non-Pydantic, sync-first codebase.
- **Mutation testing** (ADR-008 clause 2): `mutmut` — a candidate, **not yet verified** against a
  real project. Verify before relying on its score: a mutant that did not compile, or timed out,
  must never be counted as killed.
- **Performance testing**: k6, via this stack's own internal `saturday-k6-exporter` package (converts
  recorded Playwright requests into k6 scripts — the same pattern as the C# port's
  `Saturday.K6Exporter`), plus `saturday-k6-redaction` for stripping secrets (tokens, auth headers) from
  exported scripts before they leave the machine.
- **Reporting**: **no dedicated reporting package exists yet** in this stack (unlike the C# port's
  `Saturday.Reporting` / `Saturday.Reporting.Cli`, which compiles video-embedded HTML reports) — this is
  a known, honest gap, not an oversight. Until a Python equivalent exists, `pytest-html` or
  `allure-pytest` are reasonable interim picks; don't treat either as the "correct" long-term answer,
  they're placeholders.

## Other Saturday-Python Packages (context, not testing-specific)
`saturday-otel` (OpenTelemetry tracing/metrics), `saturday-certs` (mTLS client cert & runner config),
`saturday-ml` (visual baselines, regression, heatmap generation) — mentioned for completeness since
they're part of the same monorepo, not because they're testing-tooling categories this file is scoped to.
