# Bitcoin DCA Bot - Agent Knowledge Base

**Project**: bitcoin-dca-accumulation-bot  
**Stack**: Python 3.13+, CCXT, pandas, numpy  
**Package Manager**: [uv](https://github.com/astral-sh/uv) - use `uv run` for all Python commands  
**Generated**: 2026-02-08

## OVERVIEW

Automated Bitcoin accumulation bot using the 2-Year Moving Average Multiplier strategy. Buys BTC on a schedule when price is below calculated thresholds (Green Line = 730-day SMA, Red Line = 5x multiplier).

## STRUCTURE

```
.
├── src/btc_dca_bot/     # Main package (7 modules, ~900 LOC)
│   ├── main.py          # Entry point + DCABot orchestration
│   ├── strategy.py      # MAMultiplierStrategy + signals
│   ├── exchange.py      # CCXT wrapper with retry logic
│   ├── data_fetcher.py  # Abstract + CCXT + CSV fetchers
│   ├── state.py         # PortfolioState persistence
│   └── logger.py        # DashboardLogger with ASCII UI
├── tests/               # pytest suite (7 files)
├── test_data/           # Mock CSV data for testing
├── data/                # Runtime state persistence
└── openspec/            # Change management specs
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Entry point | `src/btc_dca_bot/main.py` | `DCABot.run()` heartbeat loop |
| Strategy logic | `src/btc_dca_bot/strategy.py` | 730-day SMA, 5x multiplier |
| Exchange API | `src/btc_dca_bot/exchange.py` | CCXT wrapper, exponential backoff |
| Data sources | `src/btc_dca_bot/data_fetcher.py` | Factory pattern: CCXTDataFetcher / CSVDataFetcher |
| State persistence | `src/btc_dca_bot/state.py` | Atomic JSON writes with tempfile |
| Logging/Dashboard | `src/btc_dca_bot/logger.py` | Box-drawing ASCII dashboard |
| Tests | `tests/test_*.py` | pytest, pytest-asyncio |

## CODE MAP

| Symbol | Type | Location | Role |
|--------|------|----------|------|
| `DCABot` | class | main.py:22 | Main orchestrator with signal handling |
| `MAMultiplierStrategy` | class | strategy.py:28 | 2Y MA multiplier calculation |
| `StrategySignal` | dataclass | strategy.py:15 | Immutable signal output |
| `AccumulationZone` | Enum | strategy.py:7 | AGGRESSIVE / STANDARD / STOP |
| `ExchangeWrapper` | class | exchange.py:15 | CCXT wrapper with retry |
| `ExchangeError` | Exception | exchange.py:9 | Custom exchange errors |
| `DataFetcher` | ABC | data_fetcher.py:9 | Abstract data source |
| `PortfolioState` | dataclass | state.py:9 | Tracks trades + PnL |
| `DashboardLogger` | class | logger.py:11 | Structured logging + dashboard |

## CONVENTIONS

**Code Style** (enforced by ruff):
- Line length: 100
- Google-style docstrings
- Strict mypy: `disallow_untyped_defs=true`
- No `E501` (line too long) - handled by formatter

**Type Safety**:
- ALL functions must have type annotations
- Use `from __future__ import annotations` for forward refs
- Dataclasses for data containers
- Abstract base classes for extensible components

**Error Handling**:
- Custom `ExchangeError` for exchange failures
- Exponential backoff with jitter in `ExchangeWrapper._execute_with_backoff()`
- Graceful shutdown on SIGINT/SIGTERM

**State Management**:
- Atomic file writes: write to temp → `os.replace()`
- State auto-saves after each trade
- JSON serialization in `data/portfolio_state.json`

## ANTI-PATTERNS (AVOID)

1. **Don't block the heartbeat** - Always sleep between cycles
2. **Don't swallow exchange errors** - Raise `ExchangeError` after retries exhausted
3. **Don't use `float` for money** - Already using floats; document precision limits
4. **Don't skip type annotations** - mypy is strict, CI will fail
5. **Don't call `state.save()` directly** - Use `record_trade()` which auto-saves

## UNIQUE STYLES

**Factory Pattern for Data Sources**:
```python
fetcher = create_data_fetcher(exchange_id="coinbase")  # Live
fetcher = create_data_fetcher(csv_path="./test_data/mock.csv")  # Mock
```

**Environment-Driven Configuration**:
- All config via env vars (no config files)
- `MOCK_DATA_CSV` presence triggers mock mode
- Exchange credentials only required for live mode

**Dashboard Output**:
- ASCII box-drawing characters for status display
- Zone visualization: 🟢 AGGRESSIVE / 🟡 STANDARD / 🔴 STOP

## COMMANDS

```bash
# Run with mock data (no API keys)
MOCK_DATA_CSV=./test_data/test_zones.csv TEST_MODE=true uv run python -m btc_dca_bot.main

# Run with live exchange
uv run python -m btc_dca_bot.main

# Run tests
uv run pytest

# Type checking
uv run mypy src/btc_dca_bot

# Linting
uv run ruff check .
uv run ruff format .

# Docker
docker-compose up -d
docker-compose logs -f
```

## NOTES

- **Testing**: Uses pytest-asyncio. Mock CSV data in `test_data/` for zone testing.
- **Exchange Support**: Any CCXT-supported exchange. Tested with Coinbase.
- **Precision**: Float math for BTC amounts; sufficient for retail DCA.
- **Deployment**: Docker Compose with volume mounts for state/logs.
- **No CI/CD**: No `.github/workflows/` - run tests locally before deploying.

<skills_system priority="1">

## Available Skills

<!-- SKILLS_TABLE_START -->
<usage>
When users ask you to perform tasks, check if any of the available skills below can help complete the task more effectively. Skills provide specialized capabilities and domain knowledge.

How to use skills:
- Invoke: `npx openskills read <skill-name>` (run in your shell)
  - For multiple: `npx openskills read skill-one,skill-two`
- The skill content will load with detailed instructions on how to complete the task
- Base directory provided in output for resolving bundled resources (references/, scripts/, assets/)

Usage notes:
- Only use skills listed in <available_skills> below
- Do not invoke a skill that is already loaded in your context
- Each skill invocation is stateless
</usage>

<available_skills>

<skill>
<name>agent-browser</name>
<description>Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task. Triggers include requests to "open a website", "fill out a form", "click a button", "take a screenshot", "scrape data from a page", "test this web app", "login to a site", "automate browser actions", or any task requiring programmatic web interaction.</description>
<location>project</location>
</skill>

<skill>
<name>openspec-apply-change</name>
<description>Implement tasks from an OpenSpec change. Use when the user wants to start implementing, continue implementation, or work through tasks.</description>
<location>project</location>
</skill>

<skill>
<name>openspec-archive-change</name>
<description>Archive a completed change in the experimental workflow. Use when the user wants to finalize and archive a change after implementation is complete.</description>
<location>project</location>
</skill>

<skill>
<name>openspec-bulk-archive-change</name>
<description>Archive multiple completed changes at once. Use when archiving several parallel changes.</description>
<location>project</location>
</skill>

<skill>
<name>openspec-continue-change</name>
<description>Continue working on an OpenSpec change by creating the next artifact. Use when the user wants to progress their change, create the next artifact, or continue their workflow.</description>
<location>project</location>
</skill>

<skill>
<name>openspec-explore</name>
<description>Enter explore mode - a thinking partner for exploring ideas, investigating problems, and clarifying requirements. Use when the user wants to think through something before or during a change.</description>
<location>project</location>
</skill>

<skill>
<name>openspec-ff-change</name>
<description>Fast-forward through OpenSpec artifact creation. Use when the user wants to quickly create all artifacts needed for implementation without stepping through each one individually.</description>
<location>project</location>
</skill>

<skill>
<name>openspec-new-change</name>
<description>Start a new OpenSpec change using the experimental artifact workflow. Use when the user wants to create a new feature, fix, or modification with a structured step-by-step approach.</description>
<location>project</location>
</skill>

<skill>
<name>openspec-onboard</name>
<description>Guided onboarding for OpenSpec - walk through a complete workflow cycle with narration and real codebase work.</description>
<location>project</location>
</skill>

<skill>
<name>openspec-sync-specs</name>
<description>Sync delta specs from a change to main specs. Use when the user wants to update main specs with changes from a delta spec, without archiving the change.</description>
<location>project</location>
</skill>

<skill>
<name>openspec-verify-change</name>
<description>Verify implementation matches change artifacts. Use when the user wants to validate that implementation is complete, correct, and coherent before archiving.</description>
<location>project</location>
</skill>

<skill>
<name>skill-creator</name>
<description>Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.</description>
<location>project</location>
</skill>

</available_skills>
<!-- SKILLS_TABLE_END -->

</skills_system>
