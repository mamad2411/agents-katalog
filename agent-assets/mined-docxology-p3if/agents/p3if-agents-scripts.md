# AGENTS.md — `p3if/scripts`

Thin-orchestrator scripts for the P3IF framework. This directory is a
committed, versioned part of the repository (referenced by the root README,
CHANGELOG, and docs; safe to run locally and in CI). There is no local-only
invariant here.

Parent standard: [`../AGENTS.md`](../AGENTS.md).

## Thin-Orchestrator Contract

- Scripts are orchestration only: argparse, path bootstrap, logging, and a
  single delegated call into `src/p3if/` entrypoints.
- Business/data/plot/analysis logic lives in `src/p3if/` (importable + tested).
- Scripts must not import `tests.*`; shared data builders live in
  `src/p3if/utils/fixtures.py` (re-exported by `tests/fixtures/helpers.py`).
- Subprocess/timeout/result plumbing lives in
  `src/p3if/utils/command_runner.py`.
- Measurement/statistics logic for benchmarks lives in
  `src/p3if/utils/benchmark.py`.

## Script Inventory

| Script | Purpose | Delegates to | Command |
|--------|---------|--------------|---------|
| `run_all.py` | Master orchestrator: tests, visualizations, benchmarks, examples, validation | `p3if.utils.command_runner.run_command`, `p3if.visualization.portals.orchestrator.P3IFVisualizationOrchestrator`, `p3if.orchestrators.*` | `python scripts/run_all.py [--tests\|--viz\|--bench\|--examples\|--validate]` |
| `run_examples.py` | Run example orchestrators (cognitive security, healthcare, framework integration) | `p3if.orchestrators.*` | `python scripts/run_examples.py` |
| `generate_final_visualizations.py` | Generate all visualization types | `p3if.visualization.portals.orchestrator.P3IFVisualizationOrchestrator` | `python scripts/generate_final_visualizations.py [--output-dir DIR]` |
| `benchmark_performance.py` | Performance benchmarks and metrics | `p3if.utils.benchmark.PerformanceBenchmark` | `python scripts/benchmark_performance.py [--quick\|--full] [-o FILE]` |
| `validate_system.py` | System validation and health checks | pytest suite, `p3if.utils.logging` | `python scripts/validate_system.py` |
| `setup_development.py` | Development environment setup (`pip install -e .`, deps) | pip | `python scripts/setup_development.py` |
| `view_p3if_website.py` | Open the local interactive dashboard in a browser | `p3if.data.synthetic.SyntheticDataGenerator`, `p3if.visualization.interactive.InteractiveVisualizer` | `python scripts/view_p3if_website.py` |

7 Python files.

## Gotchas

- `run_all.py` is the one sanctioned fat orchestrator (its declared role);
  its subprocess plumbing still delegates to `src/p3if/utils/command_runner.py`.
- `benchmark_performance.py` full run builds 1000-pattern frameworks and
  renders visualizations — use `--quick` for smoke runs.
