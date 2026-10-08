---
name: test-sdk
description: End-to-end test the scrapegraph-py v2 SDK against the live API using a user-provided API key. Exercises every public method on both ScrapeGraphAI (sync) and AsyncScrapeGraphAI (async), including the crawl/monitor/history namespaces. Use when the user asks to "test the SDK", "run full SDK tests", or validate a release candidate. NEVER push directly to main — all changes go via a feature branch + PR.
---

# Test the scrapegraph-py v2 SDK end-to-end

## Hard rules

1. **DO NOT push directly to `main`.** `main` is the protected release branch. If changes are needed, create a feature branch and open a PR. Never `git push origin main`, never force-push to main, never self-merge.
2. **Never hardcode or commit the API key.** Accept it from the user at runtime. Pass it via the `SGAI_API_KEY` env var or the `ScrapeGraphAI(api_key=...)` constructor. Do not write it to any file, log, or commit.
3. **Do not modify production config** (`env.py`, release workflows, `pyproject.toml` version) as part of testing.

## Required input

Ask the user for their ScrapeGraph API key before doing anything else:

> I need a ScrapeGraph API key to run the live SDK tests. Please paste it (I will use it in-process only and will not write it to disk or commit it).

Export it for the session only:

```bash
export SGAI_API_KEY="<user-provided-key>"
```

## Scope — the v2 SDK surface

The SDK exposes two top-level classes in `scrapegraph_py`:

- `ScrapeGraphAI` (sync) — from `scrapegraph_py.client`
- `AsyncScrapeGraphAI` (async) — from `scrapegraph_py.async_client`

> Note: there is **no** `smartscraper`, `markdownify`, or `agentic_scraper` method. Those names are stale. Use the endpoints below — they mirror the Playground (Scrape, Extract, Search, Crawl, Monitor).

### Endpoints to exercise

| Endpoint | Sync method | Async method |
|----------|-------------|--------------|
| Scrape   | `client.scrape(...)`            | `await aclient.scrape(...)`            |
| Extract  | `client.extract(...)`           | `await aclient.extract(...)`           |
| Search   | `client.search(...)`            | `await aclient.search(...)`            |
| Crawl    | `client.crawl.start(...)`       | `await aclient.crawl.start(...)`       |
| Monitor  | `client.monitor.create(...)`    | `await aclient.monitor.create(...)`    |
| Credits  | `client.credits()`              | `await aclient.credits()`              |

### Namespace sub-methods (cover the full lifecycle)

- `client.crawl` — `start`, `get`, `stop`, `resume`, `delete`
- `client.monitor` — `create`, `list`, `get`, `update`, `pause`, `resume`, `activity`, `delete`
- `client.history` — `list`, `get` *(supporting, not shown in Playground)*

The async client exposes the same namespaces under the same attribute names, with `async` methods. `health()` and `close()` also exist as utility methods — call `health()` as a sanity check at the start of the run.

## Scope — test the WHOLE SDK

Every public method above must be exercised against the live API on both `ScrapeGraphAI` and `AsyncScrapeGraphAI`. Do not mock.

For each call:
- Use a minimal valid payload (e.g. `https://example.com` + trivial prompt).
- Record the response type, that it matches the returned Pydantic model / `ApiResult`, and any surfaced error.
- For `crawl` / `monitor`: after `start`/`create`, also exercise `get`, then `stop`/`pause`+`resume`, then `delete` so the full lifecycle is covered and no test artifacts are left behind.
- Call `credits()` before and after the full run so the user can see credit consumption.

## Procedure

1. Confirm the working directory is clean (`git status`). If not, stop and ask the user.
2. Confirm you're not on `main`. If making commits, branch first: `git checkout -b test/sdk-smoke-YYYYMMDD`. Running tests without committing does not require a branch.
3. Install deps: `uv sync`.
4. Run the existing unit tests first: `uv run pytest tests/ -v`. Fix any failures before live testing.
5. Write a throwaway script (e.g. `scripts/smoke_sdk.py`) that:
   - Imports `ScrapeGraphAI` and `AsyncScrapeGraphAI` from `scrapegraph_py`.
   - Calls every top-level method and every namespace method listed above, on both clients.
   - Prints a compact table: method | sync ok | async ok | notes.
6. Run it: `uv run python scripts/smoke_sdk.py`.
7. Delete the throwaway script. Do not commit it.
8. Report a summary: which methods passed, which failed, credits consumed, and any suspicious response shapes.

## If you find a bug

- Branch: `git checkout -b fix/<short-description>`.
- Fix it. Then run the full pre-commit suite from `CLAUDE.md`:
  ```bash
  uv run ruff format src tests
  uv run ruff check src tests --fix
  uv build
  uv run pytest tests/ -v
  ```
- Commit with a `fix:` prefix (keeps the semantic-release bump at patch).
- Push the branch and open a PR. **Do not merge to main yourself.**

## Reminders to surface to the user

- Live tests consume API credits. Confirm before running.
- If any method returns a 4xx/5xx, report it verbatim — do not retry silently more than once.
- If the user's key is invalid or rate-limited, stop and tell them; do not swap in any other key.
