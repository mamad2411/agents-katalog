# Repository Guidance

- Commit cohesive, completed work at appropriate checkpoints after verification. Do not wait for an explicit commit request when a meaningful unit of work is finished.
- Keep unrelated user changes out of a commit.
- Before committing, run `uv run ruff check .`, `uv run ruff format --check .`, and `uv run pytest`.
- When the bundled Skill changes, also run the skill validator and verify the user-level installed copy is either current or explicitly reported as stale.
