---
name: add-benchmark-harness
description: Add, update, or verify a harness adapter for this benchmark. Use whenever a contributor wants to run a new agent CLI, register a custom harness, map harness output into safe normalized trajectory facts, or prepare a harness adapter PR.
compatibility: Linux, Node.js 24+, and this repository's installed dependencies.
---

# Add a benchmark harness

Add the smallest adapter that lets the existing runner call a new harness. Do not teach the benchmark how that agent works inside.

## Read first

- `docs/benchmark-automation.md`
- `docs/running.md`
- `scripts/harness-runtime.mjs`
- `scripts/benchmark-config.mjs`
- `examples/benchmark.config.ts`
- the closest adapter tests in `test/integration/`, and `test/unit/prepare-benchmark.test.mjs`

## Pick the path

- **Private or experimental harness**: define it locally with `defineHarness({ createAdapter() })` in a config file. Nothing changes in the repository, and the contributor runs it with `npm run benchmark:submit -- --config FILE`.
- **Harness that needs several steps** (start a server, spawn a worker thread, read a native timeline): copy `examples/bb/`. It holds a driver script, a timeline parser, and the config that ties them together, and it stays outside the built-in list because it is a starting point, not a verified family.
- **Reusable harness**: add a built-in adapter. Four places know the adapter list, and all four change together:
  - `scripts/prepare-benchmark.mjs`: the `makeAdapter` switch, the `ADAPTER_AGENT`, `ADAPTER_IDS`, and `ADAPTER_BINARIES` maps, and the `--harness` validator, because a name missing from them cannot resolve an agent or a binary;
  - the `--harness` help text in `scripts/prepare-benchmark.mjs`;
  - the ready adapter list in `usage` in `scripts/benchmark-submit.mjs`;
  - the adapter tables in `README.md` and `docs/running.md`.

`createAdapter` receives `{ model, modelId, harnessId, profileId, overrides }` and returns the adapter object.

## Describe the identity first

Keep the stable family separate from the exact build:

- harness family, such as `codex` or `my-company/my-agent`;
- exact harness version or immutable source revision;
- adapter version or source hash;
- agent family and version, when the agent is not the same thing as the harness;
- model family, exact model or version, provider, and reasoning setting;
- a safe recipe for reproducing the setup, with `configurationId`, tools, extensions, rules, runtime flags, and environment variable names.

Every public export needs non-empty strings for `agentFamily`, `agentVersion`, `modelFamily`, `modelVersion`, `harnessFamily`, and `adapterVersion`, plus a `configurationLabels` array. `provider` is optional and is exported as `null` when there is none. `harnessVersion` falls back to `version` when it is not set. `npm run benchmark -- check --config FILE` rejects missing identity before a paid run.

Never put an API key, prompt, command, argument, output, file content, user name, home path, or credential-store path into an identity field.

A recipe tells a reader how to reproduce the public setup. It is not an installer and it does not promise a bit-for-bit rebuild. Store environment variable names, never their values.

## Implement

1. Return an explicit command, arguments, version, model, thinking setting, and `ready: false`.
2. Use only the placeholders the runtime expands: `{prompt}`, `{workspace}`, and `{state}`. They become the prompt and the sandbox paths `/workspace` and `/state`. There is no artifacts placeholder; use `seedFiles` and `stateFiles` for prepared files.
3. Implement `inspectOutput` when the harness exposes structured events. Return observed metrics and normalized call events, nothing invented. A metric the harness does not report stays `null`. Never turn an unknown cost, token count, round count, or call count into zero.
4. Implement `continueSession` only when same-session recovery is supported and you have verified it.
5. Keep raw harness output local. Public exports must exclude prompts, model prose, commands, arguments, output, and file contents.

`ready` only gates a direct `npm run benchmark -- run`. `npm run benchmark:submit` runs its own smoke task and does not need it.

## Verify

1. Add deterministic adapter and config tests for routing, identity, placeholders, and readiness.
2. Add parser tests with synthetic safe events when `inspectOutput` exists.
3. Run `npm run check`, or the focused unit and integration tests while you work.
4. Run a one-task smoke. A paid smoke needs the user's approval.
5. Check the actual model, reasoning, tools, exit state, normalized calls, and which metrics are available.
6. Export and validate the bundle, and confirm nothing sensitive got in.
7. Set `ready: true` only when the adapter will also be used through `npm run benchmark -- run`.

## What to put in the PR

Explain the supported harness and version, the authentication it needs, which metrics you observed and which stay unavailable, whether continuation works, the smoke evidence, and anything still rough. Leave out credentials and raw trajectories.
