# Copilot Instructions

## Project Goal

OllieBot is a modular async Twitch bot for Froggen's channel, with pyramid tracking as the first feature and Twitch Helix integration as a core platform concern.

## Engineering Standards

- Prefer async-first code paths.
- Use `httpx.AsyncClient` for HTTP.
- Use `aiosqlite` for SQLite access.
- Keep Twitch API access in dedicated service modules.
- Keep commands and features isolated in cog or feature modules.
- Add type annotations to all new code.
- Avoid blocking calls in event handlers.
- Prefer pure functions for parsing and scoring logic so they are easy to test.

## Packaging And Tooling

- Use `uv` for Python installation, virtual environment management, dependency sync, and builds.
- Target Python 3.14.
- Run tests with `uv run pytest`.
- Keep runtime dependencies in `[project.dependencies]` and development-only dependencies in `[dependency-groups]`.

## Repository Direction

- Migrate legacy top-level scripts into the `olliebot` package over time.
- Preserve behavior first, then improve architecture in small verified steps.
- Replace direct Twitch Helix calls in command handlers with reusable client methods.
- Avoid hardcoded channel or moderator identities.

## Deployment

- The bot should remain container-friendly for AWS Lightsail.
- Environment-driven configuration only; do not hardcode secrets.
