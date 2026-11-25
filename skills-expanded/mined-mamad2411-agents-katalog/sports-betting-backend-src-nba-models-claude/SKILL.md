# backend/src/nba/models/ - Data Models

Pure dataclasses and Pydantic schemas. No I/O, no DB access, no imports from services or routes. These were dissolved from standalone domain modules (injuries, odds, llm) during restructuring.

## Files

- `injuries.py` — `PlayerStatus`, `InjuryRecord`, `InjuryContext`, `TeamInjuryReport` dataclasses
- `llm.py` — `ParsedPick`, `PICKS_SCHEMA` (JSON schema for LLM structured output)
- `odds.py` — `SharpReference`, `EVOpportunity`, `ArbitrageOpp`, `MiddleOpp`, `PropEVAnalysis` dataclasses
- `errors.py` — `AppErrorCode` string constants (10 error codes) and `AppError(Exception)` with code/message/status_code

## Key Rules

- No business logic — only field definitions with optional defaults
- No imports from `services/`, `routes/`, `controllers/`, or `db/`
- Imports from `config/` and `utils/` are allowed if needed for type annotations
