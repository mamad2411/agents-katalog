---
name: model-params
description: >
  Confirm an LLM's capability parameters and reference prices with curl + jq
  against two public catalogs (OpenRouter /models and models.dev), no tools
  installed and no API key. Use when the agent needs to verify context
  length, tool call support, structured output, reasoning/effort levels,
  modalities, or per-1M-token pricing for a model, or restate prices in CNY
  at a live exchange rate.
---

# Confirm model parameters via public catalogs (curl + jq)

> 中文版：[SKILL.zh-CN.md](SKILL.zh-CN.md)

Two public JSON sources cover this task; both work without any API key:

- OpenRouter catalog — `https://openrouter.ai/api/v1/models`: canonical
  OpenRouter ids (`vendor/model`), per-token price strings, and the
  `supported_parameters` list.
- models.dev — `https://models.dev/api.json`: ~9000 models across providers
  with richer capability flags and vendor reference prices.

Download models.dev once per session; it is a few MB:

```bash
curl -s https://models.dev/api.json -o /tmp/models-dev.json
```

## 1. Known OpenRouter-style id

```bash
curl -s https://openrouter.ai/api/v1/models \
  | jq '.data[] | select(.id=="anthropic/claude-sonnet-4.5")'
```

Read: `context_length`, `architecture` (modalities, tokenizer),
`supported_parameters` (tools, structured_outputs, reasoning, ...),
`pricing.prompt` / `pricing.completion` — USD **per token**, multiply by
1e6 for per-1M.

## 2. Capability flags models.dev has and OpenRouter lacks

```bash
jq '.openrouter.models["anthropic/claude-sonnet-4.5"]' /tmp/models-dev.json
```

Read: `tool_call`, `structured_output`, `temperature`, `reasoning` +
`reasoning_options` (effort levels / budget_tokens min-max), `limit.context`
/ `limit.output`, `cost.input` / `cost.output` / `cost.cache_read` — already
USD per 1M — plus `status`, `release_date`, `knowledge`, and
`canonical_model_id` mapping to the OpenRouter-style id.

If the id is missing there, search vendor providers, which use their own
native ids:

```bash
jq 'to_entries[] | .key as $p | .value.models | to_entries[]
    | select(.key | test("glm-5.3-flash"; "i"))
    | {provider: $p, id: .key, cost: .value.cost, limit: .value.limit}' \
  /tmp/models-dev.json
```

## 3. Id is approximate

- Strip OpenRouter variant suffixes before lookup:
  `deepseek/deepseek-chat-v3.1:free` → key on the part before `:`.
- Separators differ between catalogs: OpenRouter writes versions with `.`
  (`claude-sonnet-4.5`), vendor entries often with `-`
  (`claude-sonnet-4-5`); `_` also occurs. Try both.
- Vendor aliases: `z-ai` ~ `zai`, `moonshot-ai` ~ `moonshotai`.

## 4. CNY conversion for Chinese output

Fetch a USD→CNY rate once per session from any keyless source below; all
are authoritative and reachable from both inside and outside China. Try
them in order until one answers:

```bash
# ExchangeRate-API open endpoint (exchangerate-api.com)
curl -s https://open.er-api.com/v6/latest/USD | jq '.rates.CNY'
# Frankfurter — European Central Bank reference rates
curl -s 'https://api.frankfurter.dev/v1/latest?base=USD&symbols=CNY' | jq '.rates.CNY'
# fawazahmed0 currency-api (jsDelivr CDN mirror)
curl -s https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json | jq '.usd.cny'
# fawazahmed0 currency-api (Cloudflare Pages mirror)
curl -s https://latest.currency-api.pages.dev/v1/currencies/usd.json | jq '.usd.cny'
```

Multiply USD prices by the rate and state the rate and its source, e.g.
`input $3/M（¥20.1/M，1 USD = 6.71 CNY，open.er-api.com）`. models.dev
`cost.*` is USD per 1M — multiply directly; OpenRouter `pricing.*` is per
token — multiply by 1e6 first, then by the rate. Sanity-check the value:
reject anything outside roughly 1–20 CNY per USD as a broken response.

## Interpreting the data

- Prices: models.dev `cost.*` is USD per 1M tokens; OpenRouter `pricing.*`
  strings are USD per token. `-`/absent means unknown, `0` means free.
- An absent boolean means the catalog does not claim the capability;
  `status: "deprecated"` marks legacy entries — prefer a newer match.
- `reasoning_options` types: `toggle` (on/off), `effort` (allowed levels
  such as low/medium/high), `budget_tokens` (min/max thinking budget).
