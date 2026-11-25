---
name: configure-codex-account
description: Point the Codex CLI adapter at a different account or provider. Use when a run must use a ChatGPT subscription, an API-key route, or a Chinese provider such as Z.AI, DeepSeek, or Xiaomi, or when the model lives behind a provider endpoint instead of the account login.
compatibility: Linux, Node.js 24+, an installed Codex CLI, and this repository's installed dependencies.
---

# Run Codex on a chosen account

The adapter measures whatever `codex` is authenticated as, unless a provider route replaces that
login. `docs/running.md` has the full picture; this is the short version with commands that were run.

## A ChatGPT subscription

```sh
npm run benchmark:submit -- --harness codex-cli-default --model gpt-5.6-luna --thinking low \
  --auth-file "$HOME/.codex/auth.json"
```

`--auth-file` copies that one file into the sandbox, where the adapter reads it through
`CODEX_HOME=/state/codex`. Sign in with `codex login` first; the subscription is what pays, and the
published transport stays `harness-native`. Verified: `gpt-5.6-luna`, PASS in 24 seconds.

## Your own provider key, including Chinese providers

Ready-made provider blocks are checked in at `configs/chinese-flash-roster.json`. Copy the one you
need into a private file and keep the key in a separate env file:

```sh
node scripts/prepare-benchmark.mjs --harness codex-cli-default --model glm-5.3-flash --thinking low \
  --provider-file provider.json --env-file private-env.json --output /tmp/codex-route.json
npm run benchmark -- run --config /tmp/codex-route.json --smoke --task replace-all-10-plain
```

Fields the Codex adapter uses from the provider block:

- `id`, `displayName`, `apiKeyEnv` — the route name, the label, and the environment variable name;
- `endpoints.responses` — Codex speaks the Responses API, so this one is required;
- `codexReasoningEffort` — whether to send `model_reasoning_effort` with your thinking level;
- `transport` — the published label, `direct-responses` by default.

Keys for the Chinese providers are already in `<Pi home>/auth.json` under `zai`, `deepseek`, and
`xiaomi` (field `key`); any other key works the same way. Verified: `glm-5.3-flash` PASS in 29
seconds, `deepseek-v4-flash` PASS in 13 seconds, both published as `direct-responses`.

## Keep the secrets local

The adapter writes the route into a private `codex/config.toml` inside the sandbox and passes the
key through the environment. `provider.json`, `private-env.json`, and `benchmark.config.ts` are
ignored by git for that reason, and the prepared config carries the values from the env file, so
never submit it. The published bundle holds the route label, never a key.
