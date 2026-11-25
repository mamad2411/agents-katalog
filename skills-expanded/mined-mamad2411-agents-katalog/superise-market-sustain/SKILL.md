---
name: superise-market-sustain
description: Operate `superise market-sustain` for SupeRISE Market self-supervision. Use when the user asks the agent to keep itself alive, monitor balance or runway, inspect market pricing, top up a market account, retry pending top-up orders, clear market auth state, or change sustain guardrails and config.
---

# Market Sustain CLI

Use `superise market-sustain` as an observe -> decide -> act toolset. Keep planning in the agent, not in the CLI.

## CLI Preflight

Before using any sustain command:

1. Check whether `superise market-sustain` is already available.
2. If the command is missing or unusable, install the published CLI globally:

```bash
npm install -g @superise/market-sustain-cli
superise market-sustain --help
```

3. If the install fails, report the exact npm error and stop instead of pretending the CLI is available.

Do not assume a local workspace checkout is already wired into `PATH`. The supported fallback is the published npm package.

## Boundary

- Use only the sustain commands this package actually implements.
- Do not assume legacy commands such as `set-model` or `mcp-server` exist.
- The only setup flow restored here is `superise market-sustain setup openclaw`.
- Prefer explicit sustain commands over ad hoc wallet transfers for market recharge.
- Report wallet-side auth dependencies clearly instead of inventing local workarounds.

## Autonomous Delegation

If the user says anything like:

- "keep yourself alive"
- "self-supervise"
- "manage your own balance"
- "watch your market account"
- "你自己维持余额"
- "你自己监控并充值"

treat that as delegation of ongoing sustain responsibility.

When that happens, do not stop at explaining commands. Start acting:

1. Run the CLI preflight first.
2. Gather the current state with `health-check`, `forecast`, and `config show`.
3. Make an immediate decision based on balance, runway, and the user's risk tolerance.
4. If ongoing supervision is wanted, register recurring checks with `superise market-sustain setup openclaw` unless the user explicitly prefers app automation.
5. Report what you decided and why.

The CLI does not do the planning for you. The agent remains responsible for observe -> decide -> act behavior.

## Natural Language Triggers

Map intent to commands like this:

- "Check your market balance" -> `superise market-sustain health-check --json`
- "How long can you keep running?" -> `superise market-sustain forecast --json`
- "Show market models" -> `superise market-sustain list-models --json`
- "Show sustain settings" -> `superise market-sustain config show`
- "Top up 3000 CKB" -> `superise market-sustain top-up 3000`
- "Dry-run a recharge" -> `superise market-sustain top-up <amount> --dry-run --json`
- "Retry failed top-up orders" -> `superise market-sustain retry-orders --json`
- "Set up recurring sustain checks" -> `superise market-sustain setup openclaw`
- "Install sustain cron jobs" -> `superise market-sustain setup openclaw`
- "Clear your market login" -> `superise market-sustain logout`

## Observe

Start any survival task by gathering state:

```bash
superise market-sustain --help
superise market-sustain health-check --json
superise market-sustain forecast --json
superise market-sustain list-models --json
superise market-sustain config show
```

Use `--json` whenever the result will drive a follow-up decision.

## Act

Use these commands to change state:

```bash
superise market-sustain top-up <amount>
superise market-sustain top-up <amount> --json
superise market-sustain retry-orders --json
superise market-sustain setup openclaw
superise market-sustain setup openclaw --json
superise market-sustain setup openclaw --tick-every 5m --retry-every 10m --session isolated
superise market-sustain config set <key> <value>
superise market-sustain config unset <key>
superise market-sustain config reset
superise market-sustain logout
```

Follow these rules:

- Choose a top-up amount based on the user's intent and current balance posture.
- Let wallet-side policy enforce transfer limits. If the wallet rejects the amount, report the wallet error directly.
- Use `top-up` for market recharge because it creates the order, transfers CKB, and submits the tx hash as one flow.
- Use `retry-orders` when transfer likely succeeded but market-side submission or finalization did not complete cleanly.
- Use `logout` to clear stale local market auth state.

## Survival Loop

When the user delegates self-supervision:

1. Run the CLI preflight.
2. Run `superise market-sustain health-check --json`.
3. Run `superise market-sustain forecast --json`.
4. If balance is low, run `superise market-sustain list-models --json`.
5. If recurring supervision is expected, run `superise market-sustain setup openclaw`.
6. If balance is critical or runway is too short, choose an amount and run `superise market-sustain top-up <amount>`.
7. If the wallet rejects the amount, report the wallet-side limit or policy instead of inventing local rules.
8. If a recharge looked partial, run `superise market-sustain retry-orders --json`.
9. Report the decision and the reason.

## Sustain Config For Decisions

The agent should not invent hidden sustain policy. Inspect the configured thresholds first:

```bash
superise market-sustain config show
superise market-sustain config get criticalBalance
superise market-sustain config get lowBalance
superise market-sustain config get requestTimeoutMs
```

If the user gives an explicit policy like "treat anything below 20 as critical", update config:

```bash
superise market-sustain config set criticalBalance 20
superise market-sustain config set lowBalance 100
```

Do not invent local recharge bounds. Wallet-side policy is authoritative for transfer limits.

## How To Choose A Top-Up Amount

The amount is still the agent's decision unless the user gave one explicitly.

Use:

- current balance from `superise market-sustain health-check --json`
- runway from `superise market-sustain forecast --json`
- the user's current activity level and tolerance for interruption
- any wallet-side limit or rejection message returned during recharge

Guidelines:

- Do not always choose the smallest possible amount.
- Prefer enough runway for the user's near-term usage.
- If the user is actively relying on the agent, bias toward fewer future interruptions.
- If the wallet rejects the amount, surface the exact rejection and adjust from there.

## Scheduled Runs

When the user asks for recurring monitoring, automatic keepalive, or a timed sustain loop:

- Prefer `superise market-sustain setup openclaw` for one-click recurring sustain setup when OpenClaw is available.
- The default setup installs two jobs: a keepalive review loop and a retry-orders loop.
- Use `--tick-every`, `--retry-every`, and `--session` if the user asks for a different cadence or OpenClaw target.
- Keep the scheduled loop focused on observe -> decide -> act, not on ad hoc wallet transfers.
- Only rely on automatic `top-up` inside the scheduled loop when the user explicitly delegated autonomous recharge.
- If OpenClaw is unavailable or the user explicitly wants app-managed scheduling, fall back to app automation instead.

Default OpenClaw setup:

```bash
superise market-sustain setup openclaw
```

Customized OpenClaw setup:

```bash
superise market-sustain setup openclaw --tick-every 15m --retry-every 30m --session isolated
```

If the user explicitly asks for `--session main`, still use `setup openclaw`, but remember that current OpenClaw requires main-session jobs to be registered as system events instead of announced chat turns.

## Reporting Language

When you describe sustain work to the user:

- Call it a sustain check or survival review.
- Report the decision, balance, and next action clearly.
- Prefer concrete outcomes over internal deliberation.

## Auth Assumption

Market login assumes one of these is true:

- `marketPublicKey` is configured explicitly, or
- wallet MCP exposes Nervos public identity through `nervos.identity`, including `address` and `publicKey`

If wallet MCP does not provide that contract yet, stop and report the wallet-side dependency.
