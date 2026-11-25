---
name: lobo-adapter-tests
description: Create and run Python tests for lobo adapters, covering discovery, packet semantics, subscriptions, Polars outputs, and the hosted terminal. Includes runnable local fixtures, reference tests, API guides, and a Playwright runner for an installed wheel without a library checkout.
---

# Test a lobo Python adapter

Work in the consumer's project with their adapter and installed wheel. Deliver runnable tests and report what passed, failed, or could not run. Use public Python APIs and observable HTTP/WebSocket/browser behavior. This skill works independently with any Agent Skills-compatible agent that can run Python. No vendor CLI, MCP server, companion skill, repository checkout, Rust toolchain, or web build is required.

## Read bundled documentation and tests

Resolve paths relative to this installed `SKILL.md`. Read [the test plan](references/test-plan.md) and the relevant API guides before writing tests:

- [Custom adapter guide](references/custom-adapters.md): complete packet example, protocol constructors, message actions, decimals, discovery, subscriptions, and source lifecycle.
- [Server guide](references/server.md) and [hosting custom adapters](references/hosted-adapters.md): commands, shared storage, feed and discovery endpoints, hosted UI differences, and launch commands.
- [Terminal guide](references/terminal.md): scope/selection behavior, OHLC bar semantics, L2/L3 simulations, and WebGPU.
- [Adapter contract](references/adapter-contract.md): integer atoms, wire identity, readiness, snapshots, and trade semantics.

Runnable reference tests are included, with no checkout-relative imports or external venue calls:

| File | What it demonstrates |
| --- | --- |
| [test_custom_adapter.py](assets/tests/test_custom_adapter.py) | Packet decoding, exact 64-bit IDs, FIFO/market simulation, binary replay, shared HTTP state, ordered feed updates. |
| [test_hosted_discovery.py](assets/tests/test_hosted_discovery.py) | Local WebSocket fixture, directory entries without books, initial subscription, explicit scope, selection, invalid requests. |
| [test_levels.py](assets/tests/test_levels.py) | Real Polars LazyFrames, schema/types, native bid priority, projection/filter/limit, empty-side output. |
| [fixture_server.py](assets/fixture_server.py) | A local three-symbol L2 feed with known bid/ask values and recorded subscription requests, serving the wheel's actual terminal. |

Complete declarations are also bundled for [Kraken](references/examples/kraken.md), [Bitfinex](references/examples/bitfinex.md), [Polymarket](references/examples/polymarkets.md), [ITCH](references/examples/itch.md), and [order feeds](references/examples/order_feed.md). Read only the applicable one. [sources.json](references/sources.json) records source paths and hashes. Use the installed package's public `help()` to resolve version differences.

## Prepare and run tests

Reuse a compatible consumer environment, or run `python /path/to/this/skill/scripts/lobo_agent.py setup --testing` from the user's project. Replace the skill path with its installed location. The helper prepares `.venv-lobo`, checks the intended binary distribution, and installs pytest, websockets, Python Playwright, and Chromium. It currently uses CPython 3.14 or `uv`; use `--python`, `--venv`, `--package` (publisher wheel path/URL), or `--distribution` as needed. Use its returned interpreter for all later commands; no source build is attempted.

Context7 and browser MCP tools are optional: reuse available tools or use official documentation and the bundled Python runner. `scripts/lobo_agent.py mcp` defaults to no configuration changes. Explicit `--client claude`, `cursor`, or `codex` can add optional tools when desired; no such registration is needed for other agents. Missing GitHub access is also non-blocking: the helper's optional `references --example <name> --tests` can refresh examples, but all core instructions and fixtures are already here.

Run the bundled baseline in the consumer environment:

```sh
<consumer-python> -m pytest /path/to/this/skill/assets/tests -q
```

Then inspect the user's adapter and write tests that actually construct its protocol/builders. Inject captured/synthetic packets using `Source.packets` for state assertions and local HTTP/WebSocket endpoints for transport. Use [test-plan.md](references/test-plan.md) to choose checks relevant to the feed. The bundled tests validate reference behavior; they do not establish correctness of the user's adapter until adapted to it.

Verify `lobo.__file__` belongs to the installed package. Assert exact quantities, IDs, schema, and subscriptions. Discovering 1,000 instruments must not open 1,000 books. Keep live-feed checks opt-in and bounded. Close adapters, servers, browsers, and fixture workers on errors too; use deadlines and finite `wait()` calls.

## Launch and inspect the terminal

Use an existing capable browser tool, Playwright MCP, or the bundled [browser_smoke.py](scripts/browser_smoke.py). Actually exercise the browser; an HTTP GET alone is insufficient.

```sh
<consumer-python> /path/to/this/skill/scripts/browser_smoke.py --server server.py --switch-symbol --require-quotes --out .lobo-test-artifacts
```

`--server` starts the consumer's script with `--port 0`, reads its printed URL, and stops only that process afterward. `--url http://127.0.0.1:8000` inspects an existing server without stopping it. Use `--symbol` for a known discovered ticker, `--min-symbols` for directory size, and `--timeout`/`--headed` as needed; see `--help`.

For a deterministic baseline, copy [fixture_server.py](assets/fixture_server.py) to the consumer project and pass that file to `--server`, with `--min-symbols 3`. It needs no network service beyond loopback. Expect AAA initially, BBB after switching, and displayed bid/ask 0.59/0.60. Its `subscriptions.jsonl` should contain only AAA and BBB in a fresh run.

The runner checks WebGPU, autocomplete, an actual subscription POST on selection, numeric quotes when requested, page errors, and screenshot/report output. Missing WebGPU or Linux Chromium libraries are a reported browser gap, not a pass. Add adapter-specific assertions for exact quotes, chart behavior, explicit scope, and recorded upstream subscriptions. Hosted source/scope controls differ from the standalone viewer; follow the hosting guide.

Report package version, bundled hashes or optional remote revision, test counts/results, actual launch command, and artifact paths. Distinguish baseline checks, tests of the user's adapter, live-feed checks, and browser results.
