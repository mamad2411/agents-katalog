---
name: deepsky-sustain
description: Operate `deepsky sustain` for Deepsky self-supervision. Use when the user asks the agent to keep itself alive, monitor balance or runway, inspect pricing, top up an account, retry pending top-up orders, clear auth state, or change sustain guardrails and config.
---

# Deepsky Sustain CLI

Use `deepsky sustain` as an observe -> decide -> act toolset. Keep planning in the agent, not in the CLI.

## CLI Preflight

Before using any sustain command:

1. Check whether `deepsky sustain` is already available.
2. If the command is missing or unusable, install the published CLI globally:

```bash
npm install -g @superise/deepsky-cli
deepsky sustain --help
```

3. If the install fails, report the exact npm error and stop instead of pretending the CLI is available.

Do not assume a local workspace checkout is already wired into `PATH`. The supported fallback is the published npm package.

## Boundary

- Use only the sustain commands this package actually implements.
- Do not assume legacy commands such as `set-model` or `mcp-server` exist.
- The only sustain setup flow restored here is `deepsky sustain setup openclaw`.
- OpenClaw provider bootstrap is separate: use `deepsky setup openclaw` when OpenClaw still needs the Deepsky provider, wallet prerequisite handling, or repository skill installation.
- Prefer explicit sustain commands over ad hoc wallet transfers for recharge.
- Report wallet-side auth dependencies clearly instead of inventing local workarounds.

## Do Not Mix Balance Domains

This distinction is mandatory. Treat it as a hard rule, not as a stylistic preference.

- `deepsky sustain health-check --json` reports the Deepsky platform-side account balance.
- `criticalBalance` and `lowBalance` are thresholds for that Deepsky platform balance.
- `deepsky sustain top-up <amount>` takes a wallet-side CKB amount as input.
- SupeRISE wallet CKB and Deepsky platform balance are different units and different ledgers.

Never do these things:

- Never compare wallet CKB directly against `criticalBalance` or `lowBalance`.
- Never describe platform balance as if it were CKB.
- Never assume `1 CKB == 1` unit of Deepsky balance.
- Never say a recharge was "too small" only from the CKB amount without checking `exchangeAmount`, `newBalance`, or a fresh `health-check`.

Always do these things:

- Use `health-check.balance`, `criticalBalance`, and `lowBalance` for platform-side health decisions.
- Use CKB only as the transfer input for `top-up`.
- Use `exchangeAmount` and `newBalance` to judge how much platform balance a recharge actually produced.
- If the post-top-up state is still `critical`, estimate the next required CKB amount from the observed recharge result instead of guessing blindly.

## Units And Money Semantics

Do not mix up account balance and recharge input units.

- `health-check.balance` is the platform-side account balance. Treat it as the platform's USD-like balance or credits, not as CKB.
- `criticalBalance` and `lowBalance` are thresholds on that platform-side balance, not on wallet CKB.
- `top-up <amount>` always takes a CKB amount as input.
- `exchangeAmount` from order creation or top-up results is the platform-side credited amount after exchange-rate conversion, not the requested CKB amount.
- `newBalance` is again the platform-side balance after the credited amount is applied.

When reporting outcomes:

- State the requested top-up amount in CKB.
- State the credited or exchanged amount separately when `exchangeAmount` is available.
- Do not describe `exchangeAmount` as "only X CKB arrived". It is not a CKB field.
- If the wallet rejects or limits a transfer, quote the exact wallet error instead of inferring a hidden local limit.

## Autonomous Delegation

If the user says anything like:

- "keep yourself alive"
- "self-supervise"
- "manage your own balance"
- "watch your account"
- "你自己维持余额"
- "你自己监控并充值"

treat that as delegation of ongoing sustain responsibility.

When that happens, do not stop at explaining commands. Start acting:

1. Run the CLI preflight first.
2. Gather the current state with `health-check`, `forecast`, and `config show`.
3. Make an immediate decision based on balance, runway, and the user's risk tolerance.
4. If balance is critical or runway is too short, choose a top-up amount and execute `deepsky sustain top-up <amount>` immediately.
5. If ongoing supervision is wanted and the immediate risk is already handled, register recurring checks with `deepsky sustain setup openclaw` unless the user explicitly prefers app automation.
6. Report what you decided and why.

The CLI does not do the planning for you. The agent remains responsible for observe -> decide -> act behavior.

## Natural Language Triggers

Map intent to commands like this:

- "Check your balance" -> `deepsky sustain health-check --json`
- "How long can you keep running?" -> `deepsky sustain forecast --json`
- "Show models" -> `deepsky sustain list-models --json`
- "Show sustain settings" -> `deepsky sustain config show`
- "Top up 3000 CKB" -> `deepsky sustain top-up 3000`
- "Dry-run a recharge" -> `deepsky sustain top-up <amount> --dry-run --json`
- "Retry failed top-up orders" -> `deepsky sustain retry-orders --json`
- "Configure OpenClaw for Deepsky" -> `deepsky setup openclaw`
- "Bootstrap OpenClaw provider" -> `deepsky setup openclaw`
- "Set up recurring sustain checks" -> `deepsky sustain setup openclaw`
- "Install sustain cron jobs" -> `deepsky sustain setup openclaw`
- "Clean OpenClaw setup" -> `deepsky clean openclaw`
- "Remove the Deepsky provider only" -> `deepsky clean openclaw --provider-only`
- "Remove sustain cron jobs only" -> `deepsky clean openclaw --jobs-only`
- "Clear your login" -> `deepsky sustain logout`

## Observe

Start any survival task by gathering state:

```bash
deepsky sustain --help
deepsky sustain health-check --json
deepsky sustain forecast --json
deepsky sustain list-models --json
deepsky sustain config show
```

Use `--json` whenever the result will drive a follow-up decision.

## Act

Use these commands to change state:

```bash
deepsky setup openclaw
deepsky setup openclaw --defaults
deepsky setup openclaw --api-key <key>
deepsky sustain top-up <amount>
deepsky sustain top-up <amount> --json
deepsky sustain retry-orders --json
deepsky sustain setup openclaw
deepsky sustain setup openclaw --json
deepsky sustain setup openclaw --tick-every 20m --retry-every 10m --session isolated
deepsky clean openclaw
deepsky clean openclaw --provider-only
deepsky clean openclaw --jobs-only
deepsky sustain config set <key> <value>
deepsky sustain config unset <key>
deepsky sustain config reset
deepsky sustain logout
```

Follow these rules:

- Use `deepsky setup openclaw` when the user needs the Deepsky OpenClaw provider configured before sustain automation can work.
- That top-level setup now treats the wallet as a prerequisite: with the default local wallet MCP URL it auto-installs or auto-starts the SupeRISE Agent Wallet before configuring OpenClaw.
- For non-default wallet MCP URLs, `deepsky setup openclaw` expects the configured wallet health endpoint to already be reachable and fails early when it is not.
- `deepsky setup openclaw --defaults` runs non-interactively with defaults, keeps the current primary model unchanged, and reminds the user to switch the OpenClaw primary model to Deepsky manually.
- Top-level setup also runs `Install skills`, which silently installs all skills from both `https://github.com/appfi5/deepsky-tools.git` and `https://github.com/appfi5/superise-for-agent` in global copy mode.
- Choose a top-up amount based on the user's intent and current balance posture.
- Let wallet-side policy enforce transfer limits. If the wallet rejects the amount, report the wallet error directly.
- Use `top-up` for recharge because it creates the order, transfers CKB, and submits the tx hash as one flow.
- In autonomous loops, prefer `deepsky sustain top-up <amount> --json` so you can read `exchangeAmount`, `amountCkb`, and `newBalance` directly.
- If status is `critical`, do not stop after only installing recurring checks or retuning cadence. Handle the immediate top-up first, then schedule future reviews.
- After each critical top-up, re-run `deepsky sustain health-check --json`. If the account is still `critical`, choose a larger amount and top up again instead of waiting for the next scheduled pass.
- Use `retry-orders` when transfer likely succeeded but platform-side submission or finalization did not complete cleanly.
- Use `deepsky clean openclaw` when the user wants to remove the Deepsky provider config, Deepsky sustain jobs, or both.
- Use `logout` to clear stale local auth state.
- Keep requested CKB, credited platform amount, and resulting balance separate in your reasoning and reporting.

## Survival Loop

When the user delegates self-supervision:

1. Run the CLI preflight.
2. Run `deepsky sustain health-check --json`.
3. Run `deepsky sustain forecast --json`.
4. If balance is low but not critical, run `deepsky sustain list-models --json` when pricing context would help the preventive top-up decision.
5. If balance is critical or runway is too short, choose an amount and run `deepsky sustain top-up <amount> --json` immediately.
6. Use `exchangeAmount`, `amountCkb`, `newBalance`, and the critical threshold to estimate whether the recharge was large enough to leave `critical`.
7. Re-run `deepsky sustain health-check --json` after each critical top-up if `newBalance` is unavailable or if you need to confirm the post-top-up status.
8. If status is still `critical`, estimate the next required CKB amount from the observed credit-per-CKB ratio (`exchangeAmount / amountCkb`), round up with safety margin, and top up again immediately.
9. If the wallet rejects the amount, report the wallet-side limit or policy instead of inventing local rules.
10. If OpenClaw is not yet configured for Deepsky, run `deepsky setup openclaw` first.
11. If recurring supervision is expected, run `deepsky sustain setup openclaw`.
12. If a recharge looked partial, run `deepsky sustain retry-orders --json`.
13. Report the decision and the reason.

## Threshold Strategy

Unless the user overrides policy, use the configured thresholds like this:

- `healthy`: balance is above `lowBalance`. Stay quiet. Do not top up unless there is some unusual context the user explicitly cares about.
- `low`: balance is at or below `lowBalance` but still above `criticalBalance`. Treat this as a preventive-action zone. Check forecast, inspect pricing context if useful, and usually decide for yourself whether a preventive top-up reduces interruption risk. Prefer self-handling over asking the user.
- `critical`: balance is at or below `criticalBalance`. Treat this as immediate-action territory. Choose a top-up amount and execute it by default so the account recovers before work is interrupted.

Extra rules:

- Compare thresholds against platform balance only, never against wallet CKB.
- A recharge request is expressed in CKB, but the success criterion is whether account balance recovers after exchange-rate conversion.
- If the first critical top-up still leaves the account in `critical`, do not wait for the next cadence. Re-check immediately and continue the top-up loop until status leaves `critical` or a wallet/platform failure blocks you.
- When `exchangeAmount`, `amountCkb`, and `newBalance` are available, estimate the next required CKB amount from the observed credit-per-CKB ratio instead of guessing from scratch.
- If the wallet rejects the requested CKB amount, surface the wallet rejection exactly and adjust from there instead of inventing a local max.
- If forecast shows the runway is too short, treat that as justification to act more aggressively even if the current status is only `low`.
- Only interrupt the user when autonomy is blocked: wallet failures, platform failures, authentication failures, or manual-review situations.

## Sustain Config For Decisions

The agent should not invent hidden sustain policy. Inspect the configured thresholds first:

```bash
deepsky sustain config show
deepsky sustain config get criticalBalance
deepsky sustain config get lowBalance
deepsky sustain config get requestTimeoutMs
```

If the user gives an explicit policy like "treat anything below 20 as critical", update config:

```bash
deepsky sustain config set criticalBalance 20
deepsky sustain config set lowBalance 100
```

Do not invent local recharge bounds. Wallet-side policy is authoritative for transfer limits.

## How To Choose A Top-Up Amount

The amount is still the agent's decision unless the user gave one explicitly.

Use:

- current balance from `deepsky sustain health-check --json`
- runway from `deepsky sustain forecast --json`
- the user's current activity level and tolerance for interruption
- any wallet-side limit or rejection message returned during recharge

Guidelines:

- Do not always choose the smallest possible amount.
- Prefer enough runway for the user's near-term usage.
- If the user is actively relying on the agent, bias toward fewer future interruptions.
- In `critical`, choose an amount that is likely to move the account out of `critical` after exchange-rate conversion, not an amount that merely produces some positive recharge.
- After an insufficient critical top-up, estimate the next amount from `exchangeAmount / amountCkb`, then round up with margin so the expected credited amount should land above the remaining gap to the critical threshold.
- If the wallet rejects the amount, surface the exact rejection and adjust from there.
- Remember that the top-up input is CKB while the target outcome is platform-side balance recovery after conversion.
- When in doubt, choose the amount that reduces the chance of another near-term interruption rather than the amount that minimizes immediate spend.

## Scheduled Runs

When the user asks for recurring monitoring, automatic keepalive, or a timed sustain loop:

- Prefer `deepsky sustain setup openclaw` for one-click recurring sustain setup when OpenClaw is available.
- Before sustain scheduling, use `deepsky setup openclaw` if the Deepsky OpenClaw provider has not been configured yet.
- The default sustain setup installs the keepalive review loop. It starts at `20m`, then retunes to `2h` when healthy, `1h` when low, and `20m` when critical.
- The retry-orders loop is scheduled only when a top-up enters pending-retry state, and is removed once pending orders are cleared or escalated to manual review.
- Use `--tick-every` for a different initial health-check cadence, and `--retry-every` or `--session` if the user asks for a different retry cadence or OpenClaw target when retry scheduling is needed.
- Keep the scheduled loop focused on observe -> decide -> act, not on ad hoc wallet transfers.
- Only rely on automatic `top-up` inside the scheduled loop when the user explicitly delegated autonomous recharge.
- If OpenClaw is unavailable or the user explicitly wants app-managed scheduling, fall back to app automation instead.

Default OpenClaw setup:

```bash
deepsky sustain setup openclaw
```

Customized OpenClaw setup:

```bash
deepsky sustain setup openclaw --retry-every 30m --session isolated
```

If the user explicitly asks for `--session main`, still use `setup openclaw`, but remember that current OpenClaw requires main-session jobs to be registered as system events instead of announced chat turns.

## Reporting Language

When you describe sustain work to the user:

- Call it a sustain check or survival review.
- Report the decision, balance, requested CKB amount, credited amount, and next action clearly.
- Prefer concrete outcomes over internal deliberation.
- Default to quiet success. Only send an update when you took a material action, hit an exception, or need human help.

## Auth Assumption

Login assumes one of these is true:

- `marketPublicKey` is configured explicitly, or
- wallet MCP exposes Nervos public identity through `nervos.identity`, including `address` and `publicKey`

If wallet MCP does not provide that contract yet, stop and report the wallet-side dependency.
