---
name: api-shakedown
description: Turn an OpenAPI spec into a ready-to-run test harness with API Shakedown - a virtual service (stubs), contract tests, robustness probes and chaos scenarios - then run it against the stubs or a real server. Use when the user wants to mock or stub an API from its spec, generate contract tests, test how their app copes with timeouts, rate limits, 5xx errors or flaky responses from an API they depend on, or check a real server against its OpenAPI spec.
---

# API Shakedown

API Shakedown reads an OpenAPI 3.x spec and writes a self-contained harness folder:

| Path | What it is |
|---|---|
| `docker-compose.yml` | The virtual service: WireMock serving the generated stubs on port 8080 |
| `tests/test_contract.py` | Contract tests: status codes, content types and response schemas |
| `tests/test_robustness.py` | Malformed-request probes: a robust server answers 4xx, never 5xx |
| `chaos/chaos.py` | Failure drills to switch on while a client talks to the stubs |
| `data/dataset.json` | Test records shared by the stubs and the tests |
| `README.md` | How to run this particular harness, plus generation and review notes |

LLM agents propose test data, cases and scenarios; plain code validates every one against the spec, so nothing an LLM wrote is executed. Repository: https://github.com/anzar-ahsan-commits/api-shakedown

## 1. Check the setup

Prefer the MCP tools when they are available (`doctor`, `inspect_spec`, `generate_harness`, `list_chaos_scenarios`, `activate_chaos`, `deactivate_chaos`). Otherwise use the CLI:

```bash
pip install api-shakedown      # or run without installing: uvx api-shakedown <command>
shakedown version
shakedown doctor               # is the LLM provider reachable and the model pulled?
```

To add the MCP server to Claude Code: `claude mcp add api-shakedown -- uvx api-shakedown mcp`.

LLM provider: Ollama runs locally by default (`qwen3:8b`; `ollama pull qwen3:8b`). For a cloud model, set `SHAKEDOWN_PROVIDER=openai` or `anthropic` with `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`, and optionally `SHAKEDOWN_MODEL`. Never print, log or commit API keys.

Running the harness needs Docker (for the virtual service) and `pip install -r requirements.txt` inside the harness folder.

## 2. Look at the spec first

```bash
shakedown inspect path/or/url/to/openapi.yaml
```

This shows the operations, how they are batched for the LLM, and spec warnings. Mention the warnings to the user: contradictory or invalid examples in a spec explain odd results later.

## 3. Generate the harness

Start offline. It takes seconds and needs no LLM, so the user sees the whole flow before waiting on a model:

```bash
shakedown run openapi.yaml --out harness --offline
```

Then the full run, which adds LLM-written test data, error cases and scenarios, and a reviewer agent that checks the others' work:

```bash
shakedown run openapi.yaml --out harness-llm
```

Set expectations before starting a full run: a small spec takes minutes on a local 8B model, but a large one (around 80 operations) can take a couple of hours on a laptop. Progress lines such as `contracts: batch 3/23 done (14m 5s)` show it is moving. `--no-review` roughly halves the time; a cloud model is much faster. Run long jobs in the background and keep the user informed.

`--out` must be empty or new; `--force` overwrites only the harness's own files.

## 4. Run it against the virtual service

```bash
cd harness
docker compose up -d
pip install -r requirements.txt
SHAKEDOWN_SELECT_STATUS=1 pytest tests/test_contract.py
```

`SHAKEDOWN_SELECT_STATUS=1` makes each test ask the stubs for the status it expects, so every documented response gets exercised. On PowerShell: `$env:SHAKEDOWN_SELECT_STATUS = "1"; pytest tests/test_contract.py`.

The stubs serve the URL printed in the harness README (`http://localhost:8080` plus the spec's base path). If port 8080 is taken, start with `SHAKEDOWN_WIREMOCK_PORT=18080 docker compose up -d` and set `SHAKEDOWN_TARGET_URL` to match.

All tests should pass here. A failure against the stubs points at the spec or the generation, so read the harness README's "Generation notes" and "Review" sections before changing anything.

## 5. Chaos drills: test the user's client

The point of the virtual service is to break it on purpose while the user's app talks to it:

```bash
python chaos/chaos.py list                 # scenarios: timeouts, 429s, 503s, flaky starts, ...
python chaos/chaos.py on flaky-start       # switch one on
# ...exercise the user's app against the stubs and watch how it behaves...
python chaos/chaos.py off                  # back to normal
```

For each scenario the harness README states what a resilient client should do, such as retry with backoff, honour `Retry-After` or fail fast. Compare the app's behaviour with that.

## 6. Against a real server

Only with the user's go-ahead, and preferably against a test or staging instance, never production without explicit permission:

```bash
SHAKEDOWN_TARGET_URL=https://staging.example.com/v1 SHAKEDOWN_API_KEY=... pytest tests
```

- Contract cases read records from `data/dataset.json`, so on an empty server many fail with 404. `SHAKEDOWN_SEED=1` creates those records first, using the spec's own create operations, and deletes them afterwards. **It writes to the server**: ask before using it. Records the server refuses are listed in a warning with the reason.
- Robustness probes send malformed requests on purpose. Any 5xx is a real finding worth reporting.
- Auth: `SHAKEDOWN_API_KEY` (API key or bearer token), `SHAKEDOWN_BASIC_AUTH=user:password`. Timeout: `SHAKEDOWN_TIMEOUT` in seconds.

## Reading results against a real server

Sort failures before calling anything a bug:

| Pattern | Usually means |
|---|---|
| Expected 200, got 404 | The test record doesn't exist on the server; try `SHAKEDOWN_SEED=1` |
| Expected 4xx, got 200 | The server is more lenient than its spec; worth flagging |
| Expected 200, got 201 (or similar) | The spec and the server disagree about the status code |
| Expected 200, got 400 | The server enforces rules the spec doesn't document |
| Any 5xx from a robustness probe | A real robustness bug: malformed input crashed something |

Report findings grouped this way, with one concrete example request each, rather than as a raw list of failures.

## Limits

- Not a load-testing tool or a security scanner.
- Stubs are stateless: a record created in one call doesn't appear in later calls.
- Seeding can't reproduce ids that the server assigns itself.
- Generated content is only as good as the spec. Missing schemas, examples or error responses mean thinner tests.
