# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

When Exactly is an expressive datetime library for Python. It provides intuitive APIs for working with dates, times, and intervals through a type-safe, immutable design. The library requires Python 3.13+ and has zero runtime dependencies.

## Development Commands

```bash
# Setup
uv sync --all-groups
uv run pre-commit install

# Run all tests with coverage
uv run pytest .

# Run a single test file
uv run pytest tests/test_day.py

# Run a specific test
uv run pytest tests/test_day.py::test_day_creation -v

# Linting and formatting (type checking, ruff, mdformat)
uv run pre-commit run --all-files

# Documentation (live preview)
uv run mkdocs serve

# Build package
uv build
```

## Architecture

### Core Abstractions (`src/when_exactly/core/`)

The library is built on four core abstractions:

- **Moment** (`moment.py`): A point in time (year, month, day, hour, minute, second). Immutable dataclass analogous to `datetime.datetime`.

- **Delta** (`delta.py`): A duration that can be added/subtracted from Moments. Supports calendar-aware arithmetic (months/years), unlike `timedelta`.

- **Interval** (`interval.py`): A half-open interval `[start, stop)` between two Moments.

- **CustomInterval** (`custom_interval.py`): Base class for semantic intervals (Day, Month, Year, etc.). Provides `next`/`previous` navigation.

- **Collection** (`collection.py`): Generic ordered, deduplicated collection of intervals.

### Public API (`src/when_exactly/_api.py`)

All user-facing classes are defined in `_api.py` (single file to avoid circular imports):

**Intervals**: `Year`, `Month`, `Week`, `Day`, `OrdinalDay`, `Weekday`, `Hour`, `Minute`, `Second`

**Collections**: `Years`, `Months`, `Weeks`, `Days`, `Weekdays`, `Hours`, `Minutes`, `Seconds`

Each interval type follows a consistent pattern:

- Constructor from components (e.g., `Day(2025, 1, 15)`)
- `from_moment()` class method
- `next`/`previous` properties for navigation
- Navigation to related intervals (e.g., `day.month`, `month.days()`)

**Day-related Classes**: Three distinct classes represent 24-hour periods:

- `Day(year, month, day)` - Gregorian calendar dates
- `OrdinalDay(year, ordinal_day)` - Day-of-year numbering (1-366)
- `Weekday(year, week, week_day)` - ISO 8601 week dates (1=Monday, 7=Sunday)
- Cross-conversion: `day.ordinal_day` → OrdinalDay, `day.weekday` → Weekday, `weekday.to_day()` → Day

### Package Layout

Uses src layout with main exports in `__init__.py`. Import as `import when_exactly as wnx`.

## Key Conventions

- All core classes are frozen dataclasses (immutable)
- Intervals use half-open semantics: `[start, stop)`
- `from_moment()` factory methods create intervals containing a given Moment
- Collections auto-sort and deduplicate their contents
- Tests use pytest with doctests enabled in source files
