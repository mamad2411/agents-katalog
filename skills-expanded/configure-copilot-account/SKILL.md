---
name: configure-copilot-account
description: Point the GitHub Copilot CLI adapter at a different account. Use when a run must use the machine's own Copilot account, a provider key (BYOK, including a Chinese provider), or an OAuth-only plan such as a ChatGPT subscription reached through a local bridge.
compatibility: Linux, Node.js 24+, an installed Copilot CLI, and this repository's installed dependencies.
---

# Run Copilot on a chosen account

The Copilot CLI has three sources of model access, and the adapter keeps them apart in the published
data. Pick the one your account has; `docs/running.md` explains each in full.

## Its own GitHub account

```sh
npm run benchmark:submit -- --harness github-copilot-cli-default --model claude-haiku-4.5 --thinking low \
  --auth-file "$HOME/.copilot/config.json"
```

No provider file, because the CLI already knows your account. `--auth-file` copies that one file into
the sandbox. Published transport: `harness-native`.

A plan or organization can block the CLI itself. The run then stops in a few seconds with
`Access denied by policy settings`, which GitHub reports, not the benchmark. Two model ids on this
machine were refused that way, so use the BYOK route below for such an account.

## A provider key (BYOK)

This is how a Chinese provider is measured through Copilot. Copy the provider block from
`configs/chinese-flash-roster.json`, keep the key in its own env file, and run:

```sh
node scripts/prepare-benchmark.mjs --harness github-copilot-cli-default --model glm-5.3-flash --thinking low \
  --provider-file provider.json --env-file private-env.json --auth-file "$HOME/.copilot/config.json" \
  --output /tmp/copilot-byok.json
npm run benchmark -- run --config /tmp/copilot-byok.json --smoke --task replace-all-10-plain
```

Fields the adapter uses: `copilotWireApi` (`completions` or `responses`), `copilotModelId`,
`copilotReasoningEffort`, `copilotMaxPromptTokens`, `copilotMaxOutputTokens`, and `copilotHeadersEnv`.
Leave `copilotReasoningEffort` off for a model that has no reasoning effort: the CLI refuses the
request with `Model ... does not support reasoning effort configuration` when the adapter passes
`--effort` anyway. Published transport: `direct-completions` or `direct-responses`. Verified:
`glm-5.3-flash` PASS in 30 seconds.

## An OAuth-only plan, such as a ChatGPT subscription

The plan gives a login instead of a key, so it is fronted by a local bridge and then used as BYOK:

```sh
node scripts/export-subscription-credentials.mjs                 # snapshot from Pi, no second login
export CODEX_HOME="$HOME/.local/share/explicit-edit-benchmark/subscription/codex"
CODEX_HOME="$CODEX_HOME" vekil --host 127.0.0.1 --port 1337 --providers-config providers.json --log-level warn
node scripts/wire-bridge.mjs --upstream http://127.0.0.1:1337 --port 1339 --log .tmp/wire.jsonl
```

Then use `examples/openai-subscription.example.json` as the provider file with any non-empty key in
the env file: the OAuth session authenticates, the key only satisfies the CLI. The bridge must stay
running for the whole run; a dead bridge shows up as `Connection timed out to provider`. Verified:
`gpt-5.6-luna` through the subscription, PASS in 24 seconds, published as `direct-responses`.

## Keep the secrets local

`provider.json`, `private-env.json`, and `benchmark.config.ts` are ignored by git for a reason, and
the prepared config carries the values from the env file. The adapter always sets
`COPILOT_OFFLINE=true`, so a misconfigured run fails instead of quietly spending your GitHub quota.
