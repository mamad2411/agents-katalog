# .cursorrules — IndusDiag Agent
# Cursor AI configuration for intelligent code assistance in this project.
# Place this file in the root of your project directory.

## Project Identity
You are assisting with **IndusDiag**, an AI-powered industrial sensor diagnostics agent.
This is a Python project that analyzes sensor telemetry from industrial equipment
(motors, furnaces, conveyors, cooling lines) and generates AI diagnostic reports.

## Project Structure
```
indusdiag/
├── app/
│   ├── agent.py          # Core agentic loop — orchestrates all phases
│   ├── detectors.py      # 5 anomaly detectors (spike, flatline, drift, etc.)
│   ├── parser.py         # CSV sensor log ingestion + validation
│   ├── reasoner.py       # OpenRouter LLM integration
│   ├── claude_reasoner.py# Anthropic Claude API integration
│   ├── memory.py         # SessionMemory + PersistentMemory (JSON-backed)
│   ├── tools.py          # 11 callable agent tools
│   ├── scorer.py         # Anomaly scoring + asset risk profiling
│   ├── formatter.py      # Terminal output formatting
│   ├── benchmark.py      # Precision/recall/F1 evaluation
│   ├── schemas.py        # Pydantic models (AnomalyFinding, DiagnosticReport)
│   └── config.py         # Environment variable loading
├── data/
│   ├── samples/          # Sample sensor CSV files
│   └── memory/           # Persistent agent memory (JSON)
├── prompts/
│   └── system_prompt.txt # LLM system prompt
├── main.py               # CLI entry point
└── .env                  # Local secrets (never commit)
```

## Coding Standards — Always Follow These

### Python Style
- Python 3.11+
- Type hints on ALL function signatures
- Docstrings on every module and public function
- Max line length: 88 characters (Black-compatible)
- Use f-strings, not .format() or %

### Naming Conventions
- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore`

### Data Handling
- Always use `pd.DataFrame` for sensor data, never raw lists
- All sensor DataFrames MUST have columns: timestamp, tag, value, unit, asset, status
- Convert numpy types before JSON serialization (use `convert_numpy_types()` from claude_reasoner.py)
- Never mutate input DataFrames — always work on copies

### Error Handling
- All file I/O must be wrapped in try/except with descriptive ValueError messages
- API calls must handle: missing keys, rate limits, malformed responses
- Agent phases must not crash silently — always log and re-raise

### Agent Architecture Rules
- All detector calls go through `tools.py` tool wrappers — never call detectors directly in agent.py
- Every tool call must be logged via `session.log_tool_call()`
- Memory must be saved at end of every run, even if no anomalies found
- The agent loop order is FIXED: Parse → Detect → Score → Memory → Report → Save

### Security Rules
- NEVER hardcode API keys, tokens, or credentials in any .py file
- ALWAYS load secrets from environment variables via `app/config.py`
- NEVER print or log full API keys — mask them: `key[:8]...`
- The `.env` file must never be committed (it's in .gitignore)

## Sensor Data Domain Knowledge
When suggesting code for this project, be aware:
- `sensor_spike`: sudden value jump > threshold in one reading
- `flatline`: sensor stuck at same value (hardware failure indicator)
- `missing_data`: timestamp gaps > 2x expected interval
- `out_of_range`: value outside safe operating bounds [min, max]
- `drift`: gradual upward OR downward trend over time window
- Flow sensors (L/min): downward drift = blockage risk
- Temperature sensors (C): upward drift = overheating risk
- Pressure sensors (bar): spikes = valve failure, flatline = sensor fault

## When Adding New Detectors
1. Add the function to `app/detectors.py`
2. Add a tool wrapper in `app/tools.py`
3. Add tool metadata to `TOOL_DEFINITIONS` list
4. Call it inside `run_detection_tools()` in `app/agent.py`
5. Add benchmark support in `app/benchmark.py`

## When Adding New LLM Backends
1. Create `app/{name}_reasoner.py`
2. Implement `generate_diagnostic_report_{name}()` with same signature
3. Add config vars to `app/config.py` and `.env.example`
4. Add backend selection logic in `agent.py`

## Dependencies
Core: pandas, numpy, requests, python-dotenv, pydantic, rich
Do NOT add heavy ML frameworks (sklearn, torch) — keep it lightweight.
If adding a new dependency, update requirements.txt.

## Test Data Format
All sample CSVs must have: timestamp, tag, value, unit, asset, status
Benchmark CSVs additionally need: label (values: normal, sensor_spike, flatline, missing_data, out_of_range, drift)
