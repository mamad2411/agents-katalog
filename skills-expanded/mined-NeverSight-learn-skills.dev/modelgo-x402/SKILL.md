---
name: modelgo-x402
version: 0.1.5-rc.1
description: "Call ModelGo model APIs through x402 pay-per-call. Use when the user wants anonymous paid model API access, x402, pay-per-call, Alipay AI payment, or modelgo-model-gateway without logging in. Triggers: x402, 支付调用模型, 匿名调用模型, 支付宝AI付, pay-per-call, 402 Payment Required."
metadata:
  requires:
    bins: ["modelgo"]
  cliHelp: |
    modelgo pay methods [--json]
    modelgo pay request --path /v1/chat/completions --method POST --data '{"model":"...","messages":[]}' [--json]
    modelgo pay request --url https://.../v1/chat/completions --method POST --data-file request.json [--json]
---

# modelgo x402 pay-per-call

Use this skill when the user wants to call ModelGo model APIs through x402 without a ModelGo login. The CLI sends `X-Payment-Protocol: x402` and handles the first 402 response.

> **Setup & version check:** install and the skill/CLI version-check protocol
> live in the `modelgo-shared` skill. Align versions there first.

## Command reference (authoritative)

Per-command flags, usage, and examples are auto-generated from the CLI's own
`--help`:

- [`reference/index.md`](reference/index.md) — index + global conventions + exit codes
- [`reference/pay.md`](reference/pay.md) — `pay methods/set/status/header/request`

Don't guess flags — read the reference file or run `modelgo pay --help`.

## Provisioning a stored payment credential (`pay set`)

`modelgo pay request` (below) is the primary flow — it triggers a 402 and hands
off to the `alipay-payment-skill`, which drives the actual Alipay payment. Use
`modelgo pay set` only when you already hold an **agent payment token** (issued
by the Alipay AI-Collect authorization) and want to store it for header-based
retries:

```bash
modelgo pay set --token <agent_token>           # or:
MODELGO_PAYMENT_TOKEN=<agent_token> modelgo pay set   # keeps it out of shell history
```

Prefer the env var when an agent supplies the token, so it never lands in argv.
There is no in-CLI flow yet to *mint* the token from Alipay — obtain it via the
`alipay-payment-skill` (the `pay request` 402 handoff) or out-of-band.

## Domestic vs International

- Domestic `cn` environment: if the gateway advertises `alipay:*`, route payment to the official `alipay-payment-skill`.
- International `intl` environment: do not use Alipay. Report the advertised x402 options and ask the user to configure a non-Alipay payment rail when available.
- Custom envs: follow the explicit `--env`; only `cn` auto-routes to Alipay.

## Model Request Flow

Run the request against the model gateway:

```bash
modelgo pay request --env cn --path /v1/chat/completions --method POST --data '{"model":"gpt-4o","messages":[{"role":"user","content":"hello"}]}' --intent "调用 gpt-4o 完成聊天补全" --json
```

Use `--url` instead of `--path` when the user provides an absolute gateway URL.

## If The CLI Returns A Domestic Alipay Handoff

When JSON output contains:

- `event: x402_payment_required`
- `payment_skill: alipay-payment-skill`
- `payment_required_file`
- `working_directory`
- `resource_url`
- `method`
- `data`
- `headers`
- `intent_summary`

Load and follow `alipay-payment-skill` immediately. Run the Alipay 402 flow from `working_directory`, using `payment_required_file` as the `-f` input, `resource_url` as `-r`, and preserve `method`, `data`, `headers`, and `intent_summary` exactly. Do not rewrite, truncate, decode, or display the PAYMENT-REQUIRED content.

If the Alipay skill reports payment completed and returns the resource response, return that resource response to the user exactly as provided by the Alipay skill.

## Identity Notes

x402 normally starts before ModelGo login. `modelgo pay request` sends a locally persisted `X-ModelGo-Anonymous-ID` so the first unpaid request can be correlated. After Alipay payment, the payer/trade/order identifiers returned by the payment facilitator are the stronger identity for fulfillment and logging.
