# CLAUDE.md

This file provides guidance to coding agents when working with code in this repository.

## Project Overview

OpenCode Monitor (ocmonitor) is a Python CLI tool for monitoring and analyzing OpenCode AI coding sessions. It parses OpenCode session data, calculates costs based on token usage, and generates comprehensive reports with a rich terminal UI.

**Note**: The main project code is located in `/ocmonitor/ocmonitor/` (nested directories).

## Common Commands

### Installation & Setup
```bash
# Install in development mode (from ocmonitor/ocmonitor/ directory)
cd ocmonitor
python3 -m pip install -r requirements.txt
python3 -m pip install -e .

# Or use automated installer
./install.sh

# Verify installation
ocmonitor --help
```

### Running Tests
```bash
# From ocmonitor/ocmonitor/ directory
python3 test_basic.py        # Basic functionality tests
python3 test_simple.py       # Simple import tests
python3 test_zero_token_filter.py  # Token filtering tests

# For development with pytest
pytest tests/
```

### Development
```bash
# Run with mock data (from ocmonitor/ocmonitor/)
python3 generate_mock_data.py
ocmonitor sessions test_sessions/

# Configuration check
ocmonitor config show

# Run CLI directly
python3 -m ocmonitor.cli --help
```

## Architecture

### Core Structure
```
ocmonitor/ocmonitor/           # Main package (note nested structure)
├── cli.py                     # Click-based CLI interface, all commands
├── config.py                  # Configuration management, TOML parsing
├── models/                    # Pydantic data models
│   ├── session.py            # TokenUsage, TimeData, InteractionFile, SessionData
│   └── analytics.py          # DailyUsage, WeeklyUsage, MonthlyUsage, ModelUsageStats
├── services/                  # Business logic layer
│   ├── session_analyzer.py   # Core session analysis and summary generation
│   ├── report_generator.py   # Rich UI report generation for all report types
│   ├── export_service.py     # CSV/JSON export functionality
│   └── live_monitor.py       # Real-time dashboard with auto-refresh
├── ui/                        # Rich UI components
│   └── table_builder.py      # Table formatting with progress bars
└── utils/                     # Utility functions
    ├── file_utils.py         # FileProcessor: loads OpenCode JSON session files
    ├── time_utils.py         # Time formatting and calculations
    ├── formatting.py         # Number/cost formatting utilities
    └── error_handling.py     # User-friendly error messages

config.toml                    # User configuration (UI, paths, export settings)
models.json                    # AI model pricing data (per 1M tokens)
```

### Data Flow

1. **File Loading** (`utils/file_utils.py:FileProcessor`):
   - Loads OpenCode session JSON files from `~/.local/share/opencode/storage/message/`
   - Each session contains multiple interaction files with token usage data
   - Extracts: provider_id, model_id, tokens (input/output/cache_read/cache_write), project_path, timestamps

2. **Session Analysis** (`services/session_analyzer.py:SessionAnalyzer`):
   - Aggregates token usage across all interactions in a session
   - Calculates costs using `models.json` pricing data
   - Groups sessions by day/week/month or by model/project
   - Generates summary statistics

3. **Report Generation** (`services/report_generator.py:ReportGenerator`):
   - Creates Rich tables with color-coded progress bars
   - Handles 9 report types: session, sessions, daily, weekly, monthly, models, projects, live dashboard
   - Applies session quota warnings and context window indicators

4. **Export** (`services/export_service.py:ExportService`):
   - Converts reports to CSV/JSON with metadata
   - Saves to configured export directory

### Key Components

**SessionData Model**: Represents a complete OpenCode session with:
- `session_id`, `project_name`, `session_title` (extracted from first interaction)
- Aggregated `tokens` (TokenUsage with input/output/cache_read/cache_write)
- Calculated `cost` based on model pricing
- Session time tracking with duration and 5-hour quota progress

**Pricing System**:
- `models.json` defines cost per 1M tokens for each model, keyed by `provider/model-id`
- Format: `{"provider/model-name": {"input": float, "output": float, "cacheWrite": float, "cacheRead": float, "contextWindow": int, "sessionQuota": float}}`
- Lookup chain (5 steps, backward compatible): `provider/model_id` → `provider/normalize(model_id)` → bare `model_id` → `normalize(model_id)` → scan `*/model_id`
- Cost calculation in `session_analyzer.py` multiplies token counts by pricing rates

**CLI Commands** (all in `cli.py`):
- `ocmonitor session <path>` - Analyze single session
- `ocmonitor sessions <path> [--limit N]` - Analyze all sessions
- `ocmonitor live <path> [--interval N]` - Real-time dashboard
- `ocmonitor daily/weekly/monthly <path>` - Time-based breakdowns
- `ocmonitor weekly <path> [--start-day <day>]` - Weekly breakdown with custom week start
- `ocmonitor models <path>` - Model usage statistics
- `ocmonitor projects <path>` - Project usage statistics
- `ocmonitor export <report_type> <path> [--format csv|json]` - Export reports
- `ocmonitor config show` - Show configuration

## Configuration

User config location: `~/.config/ocmonitor/config.toml`

Default config: `ocmonitor/config.toml` (in repo)

Key settings:
- `paths.messages_dir`: OpenCode session storage path
- `ui.table_style`, `ui.progress_bars`, `ui.colors`: UI preferences
- `ui.live_refresh_interval`: Dashboard update frequency
- `export.default_format`: CSV or JSON
- `models.config_file`: Path to pricing data

## Important Patterns

### Adding a New Model
Edit `models.json` using `provider/model-id` as the key:
```json
{
  "provider/model-name": {
    "input": 3.00,
    "output": 15.00,
    "cacheWrite": 3.75,
    "cacheRead": 0.30,
    "contextWindow": 200000,
    "sessionQuota": 6.00
  }
}
```

### Error Handling
All CLI commands use `@handle_errors` decorator and `create_user_friendly_error()` for readable error messages. Verbose mode (`--verbose`) shows full stack traces.

### Rich UI Components
- Progress bars show percentage usage with color coding (green/yellow/red)
- Tables use `rich.table.Table` with configurable styles
- Live dashboard uses `rich.live.Live` for auto-refreshing displays
- All UI rendering happens in `services/report_generator.py` and `ui/table_builder.py`

### Testing
Mock data generation via `generate_mock_data.py` creates realistic session files in `test_sessions/`. Use this for testing without real OpenCode data.

Unit tests in `tests/unit/test_time_utils.py` cover custom week calculation logic.

## Custom Week Start Day Feature

The `weekly` command supports custom week start days via the `--start-day` flag:

```bash
# Default (Monday start)
ocmonitor weekly

# Sunday to Sunday weeks (US standard)
ocmonitor weekly --start-day sunday

# Friday to Friday weeks
ocmonitor weekly --start-day friday --breakdown

# All 7 options: monday, tuesday, wednesday, thursday, friday, saturday, sunday
```

### Implementation Details

**Module-level constants** (`utils/time_utils.py`):
- `WEEKDAY_MAP`: Dictionary mapping day names to integers (0=Monday, 6=Sunday)
- `WEEKDAY_NAMES`: List of day names for formatting output

**New TimeUtils methods** (`utils/time_utils.py`):
- `get_custom_week_start(date, week_start_day)`: Get the week start date for a given date
- `get_custom_week_range(date, week_start_day)`: Get (start, end) tuple for a week
- `format_week_range(start, end)`: Human-readable week range formatting

**Modified components**:
- `TimeframeAnalyzer.create_weekly_breakdown()`: Added `week_start_day` parameter (default 0=Monday)
- `SessionAnalyzer.create_weekly_breakdown()`: Passes through `week_start_day` parameter
- `ReportGenerator.generate_weekly_report()`: Added `week_start_day` parameter
- `ReportGenerator._display_weekly_breakdown_table()`: Shows week start day in title and displays date ranges
- CLI `weekly` command: Added `--start-day` option with 7 day choices

**Data model compatibility**:
- `WeeklyUsage` model remains unchanged
- `start_date` and `end_date` fields reflect custom week boundaries
- `year` and `week` fields show ISO week number of week start date (for reference/display)

## Dependencies

Core: click (CLI), rich (UI), pydantic (models), toml (config)
Dev: pytest, pytest-click, pytest-mock, coverage

All dependencies specified in `requirements.txt` and `setup.py`.