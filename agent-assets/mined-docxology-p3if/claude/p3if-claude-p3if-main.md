# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

P3IF (Properties, Processes, Perspectives Inter-Framework) is a Python meta-framework for integrating and visualizing complex data relationships across multiple domains. It organizes information around three dimensions:
- **Properties**: System characteristics (security, usability, performance)
- **Processes**: Actions and transformations (authentication, data processing)
- **Perspectives**: Stakeholder viewpoints (technical, business, legal, user)

## Build and Run Commands

```bash
# Install development version
pip install -e ".[dev,web]"

# Run complete pipeline (tests, visualizations, benchmarks, examples, validation)
python scripts/run_all.py

# Interactive development menu
./interactive_terminal.sh
```

## Testing

```bash
# Run full test suite
pytest tests/ -v

# Run only unit tests
pytest tests/ -k unit -v

# Run integration tests
pytest tests/ -k integration -v

# Run with coverage
pytest --cov=src/p3if tests/

# Run a single test file
pytest tests/unit/test_models.py -v

# Run a specific test
pytest tests/unit/test_models.py::TestProperty::test_basic -v
```

Test markers: `unit`, `integration`, `visualization`, `slow`

## Code Style and Linting

```bash
# Format code
black src/ tests/ --line-length 100

# Lint
ruff check src/ tests/

# Type checking
mypy src/
```

## Key Scripts

| Script | Purpose |
|--------|---------|
| `scripts/run_all.py` | Master orchestrator for full pipeline |
| `scripts/run_examples.py` | Execute example orchestrators |
| `scripts/generate_final_visualizations.py` | Generate all visualizations |
| `scripts/benchmark_performance.py` | Performance analysis |
| `scripts/validate_system.py` | System health checks |

## Architecture

### Package Layout

The codebase uses a modern `src/` layout:

```
src/p3if/
├── core/           # Core framework (P3IFFramework, models, validation, caching)
├── orchestrators/  # Thin orchestrator patterns for domain-specific workflows
├── visualization/  # Static, interactive, animated visualizations and portals
├── utils/          # Config, logging, performance monitoring, storage
└── data/           # Domain management, importers, exporters, synthetic data
```

### Core Components

**P3IFFramework** (`core/framework.py`): Main entry point. Manages patterns (Property, Process, Perspective) and relationships with indexing, caching, and validation.

**ThinOrchestrators** (`core/orchestration.py`): Lightweight workflow patterns that compose framework components without heavy inheritance. Examples in `orchestrators/`.

**CompositionEngine** (`core/composition.py`): Dynamic framework multiplexing with conflict resolution for integrating multiple frameworks.

**ValidationEngine** (`core/validation.py`): Constraint checking and quality validation.

**CacheManager** (`core/caching.py`): LRU-based caching with configurable strategies.

### API Usage

```python
from p3if import P3IFFramework, Property, Process, Perspective
from p3if.orchestrators import CognitiveSecurityOrchestrator

# Create framework and add patterns
framework = P3IFFramework()
framework.add_pattern(Property(name="Security", domain="cybersecurity"))
framework.add_pattern(Process(name="Authentication", domain="cybersecurity"))
framework.add_pattern(Perspective(name="Technical", domain="cybersecurity", viewpoint="developer"))

# Use orchestrators
orchestrator = CognitiveSecurityOrchestrator()
results = orchestrator.execute_analysis()
```

## Critical Development Rules

**NEVER USE MOCKS**: Always use real P3IF classes (P3IFFramework, P3IFCore, Property, Process, Perspective). If P3IF modules are unavailable, fix import paths - do not create mocks. For external dependencies (matplotlib, PIL), use pytest.skip if unavailable.

**Absolute imports only**: Use `from p3if.core import P3IFCore`, not relative imports.

**Run from project root**: All scripts assume execution from the repository root.

**Type hints required**: Complete type annotations for all functions.

**Docstrings required**: Google-style docstrings for all public functions/classes.

## Web Portal

```bash
# Start development server
python website/run.py

# Or stable server
python website/run_stable.py
```

Flask-based portal in `website/` with routes for docs, domains, visualizations, and API endpoints.

## Output Organization

Scripts generate outputs in timestamped directories:
```
outputs/p3if_run_{timestamp}/
├── tests/
├── visualizations/
├── benchmarks/
├── examples/
├── validation/
└── logs/
```
