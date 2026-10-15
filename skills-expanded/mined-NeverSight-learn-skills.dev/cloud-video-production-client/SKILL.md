---
name: cloud-video-production-client
description: Integrate trusted customer servers or local agents with the Firefly Cloud Video Production API. Use when uploading explicitly selected local image/video files, submitting local or URL assets for asynchronous cloud template production, polling a production by conversation_id through its final video result, handling idempotent retries, receiving signed production webhooks, or diagnosing public API errors from /api/rest/mva/out/cloud endpoints.
---

# Cloud Video Production Client

Integrate with the asynchronous Cloud template-production service. Keep customer credentials outside prompts, source code, logs, and generated documents.

## Load references

- Read `references/api-contract.md` before constructing or interpreting any API request.
- Read `references/webhook-contract.md` when `callback_url` is used or a webhook receiver is implemented.
- Read `references/integration-checklist.md` before integration review, test handoff, or go-live.
- Use `references/openapi.yaml` when a machine-readable contract, SDK generation, or schema validation is needed.
- Run `scripts/make_from_local_media.py` with `uv run --script` for local images, local videos, or mixed local media instead of reimplementing the direct-upload workflow.

## Resolve connection settings

Use the production connection settings defined by this Skill:

- `base_url`: fixed to `https://mp-video-agent.fireflyfusion.cn`; do not search for, infer, or override it.
- `api_key`: load the production credential only from `FIREFLY_MVA_PROD_API_KEY`; require `produce` scope.
- `callback_secret`: required only when verifying Webhook signatures; obtain it through the agreed secure channel.

Send the value of `FIREFLY_MVA_PROD_API_KEY` as `X-API-Key` from a server or secret manager. Never read a generic `API_KEY`/`X_API_KEY` or another environment credential as a fallback. Never place the key in browser code or ask the user to paste a real value into chat.
The service operator creates the credential from the database-backed credential control plane and delivers it once through an approved secure channel. Customers do not self-register a key through the public Cloud endpoints; later list operations cannot recover the plaintext.

## Prepare assets

Accept either HTTP/HTTPS media URLs or local files that the current trusted runtime is allowed to read.

For each explicitly selected local file:

1. Resolve the path inside the runtime's approved read scope. Do not scan a home directory, expand an unspecified directory recursively, or upload a file the user did not select.
2. Prefer the bundled `scripts/make_from_local_media.py` runner. It accepts repeated `--input` values, so one request may contain images, videos, or both.
3. Compute size, MIME type, and SHA-256, then send metadata only to `POST /api/rest/mva/out/cloud/upload/init`.
4. Keep the returned object-scoped COS credentials in memory and use the Tencent COS SDK high-level transfer API with every required header. Let the SDK choose single PUT or multipart internally; do not branch on file size.
5. Send only `upload_id` to `POST /api/rest/mva/out/cloud/upload/complete`. Require one non-empty `data.files[]` descriptor before `/make`.
6. Map `type`, `url`, and `content_sha256` to canonical `assets[]`, then submit `/make`.

Do not embed local bytes or Base64 in prompts or `/make`. Do not fall back to gateway multipart when direct upload fails. The legacy `/upload` endpoint is only for an explicitly requested compatibility diagnostic.

For an end-to-end local-media task, run:

```bash
uv run --script scripts/make_from_local_media.py \
  --input /approved/media/photo.jpg \
  --input /approved/media/clip.mp4 \
  --intent "生成一条节奏明快的短片" \
  --wait
```

The runner reads only `FIREFLY_MVA_PROD_API_KEY`. It does not create an `outputs` directory, persist state, download the final video, or render a preview. With `--wait`, its final JSON line returns only `conversation_id`, `status`, `video_url`, and `request_id`. Return `video_url` as an opaque result field; do not open it, embed it as an inline preview, or download it unless the user explicitly asks for a separate operation. Never print source asset URLs, temporary COS credentials, or signed upload URLs.

If the runtime cannot read the user's device—for example, a browser-only or remote cloud agent given only a local path—ask the user to attach the file through the host product or move it into an accessible workspace. Never pretend the path was uploaded.

## Select the workflow

### Create and Poll

Use this as the default integration path.

1. Generate one stable `outer_request_id` for the customer's business operation.
2. Upload explicitly selected local files and normalize all local/URL inputs into canonical `assets[]`.
3. Submit `POST /api/rest/mva/out/cloud/make` with canonical fields only.
4. Persist `conversation_id`, `outer_request_id`, and `request_id` from the response.
5. Poll `POST /api/rest/mva/out/cloud/poll` every 3–5 seconds.
6. Stop on `completed`, `failed`, or `cancelled`.
7. Read the final `video_url` from the terminal Poll response. Do not call an additional result endpoint.

### Create and Webhook

Use this when the customer has a public HTTPS receiver.

1. Register the receiver and signing secret before submitting a task.
2. Include `callback_url`; omit `callback_events` to receive the default terminal events.
3. Verify the signature against the raw request bytes before parsing JSON.
4. Deduplicate deliveries by `event_id` or `X-MP-Video-Delivery`.
5. Return 2xx promptly, then process asynchronously.
6. Use Poll for reconciliation when callback state is missing or ambiguous. Do not run continuous Poll merely because a callback was configured; Poll only for recovery or an explicit user action.

## Enforce request rules

- Send flat JSON to upload init/complete, make, and Poll. Never wrap those bodies in `content`, `BaseRequest`, or another envelope.
- Use only documented `assets[]` fields such as `asset_id`, `asset_type`, `asset_url`, and `content_sha256`; do not invent aliases.
- Do not send `productId`, `userId`, `project_id`, `conversation_id`, `templateCode`, aspect ratio, high-light timestamps, or template candidates on task creation.
- Treat unknown fields as invalid because the public request models use `extra="forbid"`.
- Provide HTTP/HTTPS asset URLs that the Agent service can access. `/make` accepts JSON references and never file bytes.
- Treat `user_intent` as optional text or the documented object. Text is trimmed and truncated to 200 Unicode characters.

## Handle responses

Inspect both HTTP status and body `code`. Branch on `code`, not the `message` text.

- `200`: request succeeded.
- Require `/upload/complete` to return one `data.files[]` item with a non-empty `url` before calling `/make`.
- `409102`: idempotent replay. Adopt the returned existing `conversation_id`; do not create another task.
- `409103` or `409104`: terminal production failure or cancellation; stop waiting.
- `429100`: wait for `Retry-After`, then retry with the same `outer_request_id`.
- For `/make`, handle `503100` or `503101` with bounded exponential backoff and the same `outer_request_id`. Retry `/upload/complete` with the same `upload_id` after an ambiguous response; never reuse object-scoped credentials for another file.
- `400100`, `401100`, `403100`, `404100`, `413100`, `422100`, `422101`: fix the request, upload type/size, credential, task identifier, callback, or asset; do not blind-retry.

Retry network failures and ambiguous submit responses with the same `outer_request_id`. Generate a new `outer_request_id` only for an intentional new production.

## Preserve traceability

Log safe identifiers only:

- environment and request time with timezone
- `X-Request-ID`
- `outer_request_id`
- `conversation_id`
- HTTP status, body `code`, task `status`, and `current_node`
- Webhook `event_id`

Never log API keys, callback secrets, source asset URLs, signed upload URLs, raw credentials, or full customer media content. The final production `video_url` may be returned as a result field, but do not automatically render, open, or download it.
Never log local absolute paths. A basename may still be sensitive; include it only when the customer's logging policy allows it.

## Produce integration artifacts

When helping a customer implement or review an integration, produce:

- environment and credential placeholders
- request/response field mapping
- idempotency and retry policy
- Poll or Webhook state machine
- webhook verification and deduplication checklist when applicable
- error-code handling table
- smoke-test and launch-readiness checklist

Do not claim production readiness until the customer has passed the checklist in `references/integration-checklist.md`.
