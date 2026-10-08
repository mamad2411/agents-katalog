# Project Agent Skills

This repository includes local Agent Skills in `.agents/skills/` using the open `SKILL.md` format.

## Available skills

- `trading-data-pipeline`
  - Path: `.agents/skills/trading-data-pipeline/SKILL.md`
  - Use for downloading and validating raw BTCUSDT OHLCV data.
- `trading-feature-pipeline`
  - Path: `.agents/skills/trading-feature-pipeline/SKILL.md`
  - Use for building and checking phase-2 feature parquet outputs.

## Trigger rules

- If user asks to refresh raw data, validate data quality, or debug ingestion:
  use `trading-data-pipeline`.
- If user asks to create/check/debug feature engineering outputs:
  use `trading-feature-pipeline`.

## Notes

- Skills are project-local and version controlled with this repo.
- Keep `pyproject.toml` as dependency source of truth.
- Run pipeline commands inside `.venv`.
