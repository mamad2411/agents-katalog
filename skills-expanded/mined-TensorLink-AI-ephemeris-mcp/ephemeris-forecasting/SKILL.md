---
name: ephemeris-forecasting
description: Forecast numeric time series with uncertainty bands using the Ephemeris API (remote MCP server or REST). Use when the user wants a forecast, prediction, projection or capacity/demand plan for a numeric series they can supply - sales, demand, traffic, load, prices, sensor readings, metrics - or asks for prediction intervals. Do not use for non-numeric prediction or to invent missing data.
---

# Forecasting with Ephemeris

Ephemeris forecasts numeric time series with a panel of zero-shot foundation models. It returns quantile forecasts (for example the 10th, 50th and 90th percentiles), so every forecast carries its own uncertainty band. Full reference: https://ephemeris.cascade.industries/llms-full.txt

## Connect

Preferred: the remote MCP server, which exposes `get_version`, `forecast`, `describe_forecast`, `plot_forecast`, `list_models`, `get_balance` and `get_usage`.

- URL: `https://ephemeris.cascade.industries/api/mcp` (Streamable HTTP)
- Header: `Authorization: Bearer <EPHEMERIS_API_KEY>`

In Hermes Agent, add it to `~/.hermes/config.yaml` and put the key in `~/.hermes/.env` as `EPHEMERIS_API_KEY`:

```yaml
mcp_servers:
  ephemeris:
    url: "https://ephemeris.cascade.industries/api/mcp"
    headers:
      Authorization: "Bearer ${EPHEMERIS_API_KEY}"
```

If MCP is not available, call `POST https://ephemeris.cascade.industries/api/v1/forecast` with the same bearer header (request and response format in llms-full.txt).

The user must provide the API key. Never hard-code it or write it to files in their repository. If they have none, ask them to run `npx ephemeris-mcp login` in their own terminal: it signs them in through the browser and saves a key the stdio bridge uses, so the key never passes through the conversation.

## Workflow

1. **Get the data right first.** Use only the history the user gives you, oldest first. Do not pad, interpolate or invent points. Work out the sampling frequency (e.g. `"H"`, `"D"`, `"15min"`) and the horizon in steps of that frequency.
2. **Check the panel** with `list_models` once per session. Model names, health, `max_horizon` and covariate support come from the live panel, not from memory.
3. **Pick the mode:**
   - `route` by default: Ephemeris picks the model that suits the data, at the cost of about one model.
   - `ensemble` to combine eligible models when the user accepts its additional cost. Benchmark results do not establish accuracy or calibrated coverage for the user's series.
   - `explicit` only when the user names a model; check it supports the request (`covariates`, `multivariate`, `max_horizon`). A model past its `auto_max_horizon` is left out of route and ensemble but can still be named here.
4. **Covariates** (known drivers such as price, promotions, holidays, weather): pass `past` aligned with the history and `future` for values known over the horizon. Only covariate-capable models use them; route and ensemble narrow to those automatically.
5. **Call `forecast`** with `quantiles` that answer the user's question, e.g. `[0.1, 0.5, 0.9]` for an 80% interval. Pass an `idempotency_key` if you might retry.
6. **Report the band, not just the median.** Say what the interval means, mention which models were used (`meta.models_used`) and anything in `meta.notes`, and the credits spent.

## Costs and safety

Every successful forecast spends the user's credits (the response reports `settled_mc` and `balance_mc`). Do not forecast speculatively, do not loop forecasts without the user asking, and check `get_balance` before large batches (up to 64 series per call). On a 402, tell the user to top up rather than retrying.

## Saved forecasts and updates

Retain an `idempotency_key` before a paid MCP `forecast` submission. If the outcome is uncertain, retry identical inputs with that key within the server's retention period; a fresh or expired key may incur another charge. Forecasts include an `ephemeris.forecast` v1 artifact by default. It contains the submitted input history, response, billing information and supplied local context. Save it privately in the client; embedded URNs are not permanent download links or hosted storage.

Pass the complete saved object as `artifact` to `describe_forecast` or `plot_forecast`; neither accepts a local path or URL. Plotting defaults to PNG; use `format: "svg"` for SVG. These authenticated tools do not run inference or charge for a new forecast. Correcting supplied local labels or plotting a result does not require another forecast. Artifact input is limited to 1 MiB; use the CLI for larger local artifacts. If `artifact_status` is `unavailable`, preserve the raw successful result and original request rather than paying to rerun it.

Supply units, timezone, target definition and measurement semantics in `context` when known. Context reaches the hosted service but is not sent as model input. Ask for missing definitions; do not guess. A horizon counts sampling steps. Quantile bands are nominal marginal intervals: they do not establish calibrated coverage, cumulative intervals, path probabilities or the actual peak distribution. Distinguish observed sales from underlying demand and known future inputs from scenario assumptions. Billing amounts ending in `_mc` are millicredits (1000 mc = 1 credit).

Hosted MCP updates are deployed centrally. Reconnect or start a new conversation if the client caches its tool list. Existing npm bridges forward the new tools; updating the bridge package is only necessary for changes to the bridge itself. Client transport support and image/attachment rendering vary. The hosted endpoint uses Streamable HTTP; SSE-only clients need compatible transport support.

Version diagnostics: MCP `get_version` with `{}` reports the hosted server version, nullable build commit and supported forecast schemas without an API key or inference charge. `ephemeris-mcp --version` reports this installed npm bridge version offline, not the remote server version. For the standalone CLI, use `ephemeris --version` or `ephemeris version --json`. These versions are independent.
