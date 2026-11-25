# Repo Ref
- source: https://github.com/0xklen/money-machine (path: skills/idempotent-etl-writes/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: Use when a pipeline job may be retried or rerun after a partial failure. Makes every write an upsert keyed on a natural key so a replay converges to the same table state.
