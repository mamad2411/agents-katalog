# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an OR-Tools based intelligent task scheduler that combines mathematical optimization with realistic human behavior modeling. The system uses Google OR-Tools CP-SAT solver to create optimal daily schedules considering energy budgets, task rewards, fatigue, and various real-world constraints.

## Development Commands

### Running the Application

**Web Interface (Primary Entry Point):**
```bash
uv run ortools-planner
# or directly
uv run python -m src.ortools_planner.webui_app
```

**Command Line Usage:**
```bash
# Using configuration file
uv run ortools-planner --config examples/config_unified_sample.json

# Direct parameters
uv run ortools-planner --tasks examples/tasks_stage2_sample.csv --horizon-minutes 600 --energy-budget 300
```

### Testing

**Run all tests:**
```bash
uv run pytest
```

**Run specific test file:**
```bash
uv run pytest tests/test_unified_energy_budgets.py
```

**Run tests with verbose output:**
```bash
uv run pytest -v
```

### Development Tools

**Package management:**
```bash
# Install dependencies
uv sync

# Add new dependency
uv add package-name
```

## Architecture Overview

### Core Components

1. **`scheduler_unified.py`** - Main scheduling engine and entry point
2. **`unified_models.py`** - Data models (TaskU, UnifiedConfig, PieceRate, etc.)
3. **`unified_chunking.py`** - Variable construction and task chunking logic
4. **`chunking_core.py`** - Core chunking algorithms and task injection
5. **`unified_objective.py`** - Objective function construction
6. **`objective/`** - Modular objective subsystems (reward, energy, rollback, piecewise)
7. **`webui_app.py`** - FastAPI web interface with LLM integration

### Key Data Models

- **`TaskU`**: Unified task model with comprehensive attributes including timing, rewards, energy costs, and advanced features
- **`UnifiedConfig`**: Central configuration for all solver parameters
- **`PieceRate`**: Defines piecewise linear rates for rewards and energy
- **`RollbackRule`**: Models interruption recovery behavior

### Scheduling Process Flow

1. **Input**: Tasks loaded from CSV/ICS/JSON + UnifiedConfig
2. **Preprocessing**: Task enhancement with blank blocks and daily tasks
3. **Variable Construction**: CP-SAT variables created with adaptive chunking
4. **Objective Building**: Reward, energy, penalty terms assembled
5. **Solving**: OR-Tools CP-SAT execution
6. **Output**: Structured schedule with timing and energy analysis

## Common Development Tasks

### Adding New Objective Components

1. Create new module in `objective/` directory
2. Implement offset integration logic following existing patterns
3. Integrate into `unified_objective.py` via `build_objective()`
4. Add corresponding fields to `TaskU` model if needed

### Modifying Task Chunking Logic

- **Fixed Chunking**: Modify `_build_chunked_task()` in `chunking_core.py`
- **Adaptive Chunking**: Modify `_build_chunked_task_adaptive()`
- **Buffer System**: Modify `_build_buffers()` for uncertainty handling

### Extending Data Models

1. Add new fields to `TaskU` dataclass in `unified_models.py`
2. Update CSV loading in `scheduler_unified.py` if needed
3. Modify objective construction to use new fields

### Web Interface Development

- Templates are in `src/ortools_planner/templates/`
- LLM integration uses LiteLLM with DeepSeek models
- Real-time progress via WebSocket in `webui_app.py`

## Configuration and Parameters

### Key Configuration Fields

- **Energy Budgets**: `mental_budget`, `will_budget`, `physical_budget`
- **Task Splitting**: `chunk_max_minutes`, `break_reset_minutes`
- **Penalties**: `fatigue_penalty`, `energy_overuse_penalty`
- **Advanced Features**: `urgency_weight`, `startup_will_cost`

### Example Configuration

See `examples/config_unified_sample.json` for comprehensive configuration example.

## Testing Strategy

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test complete scheduling pipeline
- **Feature Tests**: Test specific features like energy budgets, task splitting
- **Performance Tests**: Test with realistic task loads

## Important Notes

- The system uses **uv** for Python package management
- Requires **Python 3.13+** and **OR-Tools 9.14+**
- Web interface includes **LLM integration** for intelligent task parameter generation
- Multi-day planning with sleep continuity is supported
- Real-world human factors are modeled (energy, fatigue, flow states)

## Troubleshooting

- **Solver Infeasible**: Check task durations vs horizon, fixed time conflicts
- **Performance Issues**: Reduce chunk_max_minutes, increase time limits
- **Import Errors**: Ensure src/ortools_planner is in Python path
- **LLM Integration**: Check API keys in environment variables