---
name: replicate-run-models
description: Run models on Replicate, predictions API, synchronous Prefer wait mode, polling, streaming, file inputs and outputs, webhooks, and client libraries. Use when the user wants to execute a model or is coding against the Replicate API.
---

# Running models on Replicate

Base URL `https://api.replicate.com/v1`, auth header
`Authorization: Bearer $REPLICATE_API_TOKEN` (see `replicate-api-key`).
Through the connected MCP server, use its search and prediction tools; the
shapes below matter for direct API and SDK code.

## Two ways to create a prediction

- Official models (maintained by Replicate, no version pinning needed):
  `POST /v1/models/{owner}/{name}/predictions`, for example
  `/v1/models/black-forest-labs/flux-1.1-pro/predictions` with
  `{"input": {"prompt": "..."}}`.
- Community models: `POST /v1/predictions` with
  `{"version": "<64-char version id>", "input": {...}}`. The version id is
  on the model's API page.

## Sync vs polling

- Add header `Prefer: wait` to hold the connection and get the completed
  prediction in one round trip. The server waits up to 60 seconds; if the
  job is slower you get it back in `starting` state and must poll.
- Polling: `GET /v1/predictions/{id}` until `status` is terminal. Statuses:
  `starting`, `processing`, `succeeded`, `failed`, `canceled`. Back off
  between polls; do not hammer sub-second loops for video models.
- Webhooks: pass `webhook` (and `webhook_events_filter`) at creation to get
  a POST on completion; the right pattern for long jobs from servers.

## Streaming

Language models and some others support streaming: create the prediction
with `"stream": true` and consume the SSE stream at `urls.stream` from the
response. In the JS client, `for await (const event of replicate.stream(
"owner/model", {input}))`.

## Files in and out

- Inputs: pass a public HTTPS URL (best), a data URI (small files only,
  roughly under 256 KB), or upload first via the Files API
  (`POST /v1/files`) and pass the returned URL.
- Outputs: `output` contains URLs on `replicate.delivery`. They expire
  (about an hour), so download or re-host anything you need to keep, and do
  so before telling the user the job is done.

## Client libraries

Python (`pip install replicate`):

```python
import replicate  # reads REPLICATE_API_TOKEN
out = replicate.run(
    "black-forest-labs/flux-1.1-pro",
    input={"prompt": "studio photo of a ceramic mug, softbox lighting"},
)
```

JS (`npm install replicate`): `await replicate.run("owner/model", {input})`.
`run()` handles waiting internally; drop to `predictions.create` when you
need webhooks, streaming handles, or the prediction id.

## Cost and error notes

- Official models bill per output (per image, per second of video, per
  token); community models bill by hardware time. The model page shows
  which; tell the user the expected cost before large batches.
- `failed` predictions include an `error` string; input validation problems
  (wrong field names, bad enum values) come back as 422 at creation. Fetch
  the model's OpenAPI-style input schema from its API page instead of
  guessing parameter names.
- Cold starts are real for rarely-run community models; the first
  prediction can take minutes while hardware boots.
