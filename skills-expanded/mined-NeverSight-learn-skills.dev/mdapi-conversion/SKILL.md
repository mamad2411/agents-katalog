---
name: mdapi-conversion
description: Use mdapi.io to convert documents, images, webpages, and text into AI-ready Markdown or structured data, with prompt-driven transformation, streaming, x402 payments, token activation, and REST/MCP/ACP/A2A/OpenAI-compatible access.
version: 1.0.0
---

# mdapi.io - Minimal Data API I/O: a content transformation layer primitive for AI systems.


Transforms documents, images, and webpages into AI-ready Markdown and structured data, optimized for LLM efficiency and token usage.

## Features

- Stateless, in-memory processing
- Edge execution with automatic scaling
- Prompt-driven transformation
- AI-optimized output for LLMs
- Pay-per-use via x402 v1/v2 or manual payment

## Philosophy

mdapi.io is minimal by design: responses are Markdown or JSON only. No HTML, CSS, or JavaScript.
- `GET /` always returns Markdown.
- `POST /` always returns JSON.
- The `result` parameter controls output completeness: `markdown`, `prompt`, or `both`.

## Quick Start

Choose your entry point based on your role:

| Role                                                     | Protocol                     | Endpoint                  | When to use                                                                                              |
|----------------------------------------------------------|------------------------------|---------------------------|----------------------------------------------------------------------------------------------------------|
| IDE / coding agent (JetBrains, Cursor, VS Code, etc.)    | ACP (Agent Client Protocol)  | POST /acp                 | You are an IDE plugin or coding agent. Use tools/call with convert tool.                                 |
| AI agent (Claude Code, Codex, OpenClaw, Hermes, etc.)    | A2A (Agent-to-Agent)         | POST /a2a                 | You are an autonomous agent. Use SendMessage with text/file parts. Supports streaming and task tracking. |
| AI agent (any framework)                                 | MCP (Model Context Protocol) | GET  /mcp + POST /mcp     | You need tool discovery. Use tools/call with convert tool.                                               |
| OpenAI-compatible client                                 | OpenAI API                   | POST /v1/chat/completions | You already use OpenAI SDK. Pass URL/file in messages. Supports streaming.                               |
| Direct HTTP / curl / script                              | REST API                     | GET  / or POST /          | Simplest path. GET returns Markdown directly. POST returns JSON with metadata.                           |

### Universal discovery

All protocols and capabilities are described in one file:
GET /.well-known/ai-discovery.json

## When to use this skill

Use this skill when the task includes any of the following:
- Transform webpages or uploaded files into clean LLM context.
- Process raw text into Markdown or prompt-driven output.
- Summarize, extract, or transform content with a `prompt`.
- Use streaming for long-running or large transformations.
- Activate and use a paid token.
- Handle manual payment or autonomous agent payment flows.
- Connect via MCP, ACP, A2A, or OpenAI‑compatible endpoints.

## Core behavior

- Detect the input type `url`, `file`, or `text`, and choose the simplest valid endpoint.
- Use `GET /` for direct Markdown output.
- Use `POST /` for JSON output or file upload.
- If `prompt` is provided, set `result` explicitly.
- Prefer `result=both` when both raw conversion and prompt result are useful.
- Use streaming only when the output is large or incremental delivery is beneficial.
- Treat all requests as stateless and in-memory; do not assume session persistence.

## Supported formats

Documents:
- PDF
- DOCX
- XLSX
- XLS
- ODT
- ODS

Images:
- JPEG
- JPG
- PNG
- WebP
- SVG

Text:
- HTML
- XML
- JSON
- CSV
- TXT

Webpages:
- Any publicly accessible URL

## Limits

- Max file size: 50 MB
- Max URL content: 50 MB
- URL length: ~2048 characters (browser limit) - use POST for long text/prompt combinations
- Rate limit: 10,000 requests per hour
- Free tier: 10 requests per day (no token required), within the service’s overall free quota
- Paid tier: min $0.01 per conversion
- Token validity: 1 year

## Request selection

### Use GET / when:
- The user wants direct Markdown output.
- The input is a URL or plain text.
- You do not need multipart upload.
- You want the simplest response path.
- **Note:** GET URLs are limited to ~2048 characters (browser dependent). For long `text` or `prompt` values, use POST.

### Use POST / when:
- The user uploads a file.
- You want a JSON response.
- You want `markdown`, `prompt_result`, and metadata together.
- You need programmatic handling.
- The input (text/prompt) exceeds URL length limits.

### Use POST /v1/chat/completions when:
- The client expects OpenAI-compatible chat format.
- The request contains messages with URLs, images, or files.
- You want streaming chat-completion semantics.

### Use MCP when:
- The host environment supports MCP discovery and tool calls.
- The agent should discover mdapi.io as a tool provider.

## Response rules

### GET /
- Always returns Markdown as plain text.
- Use query parameters for input and behavior control.

Supported query parameters:
  - `url`
  - `text`
  - `prompt`
  - `result`
  - `stream`
  - `token`
  - `memo`

 **Note:** GET URLs are limited to ~2048 characters (browser-dependent). For long `text` or `prompt` values, use POST with form data or multipart upload.

 ### POST /
- Always returns JSON.
- Use form data or multipart form data.

Expected JSON fields may include:
- `success`
- `markdown`
- `prompt_result`
- `resource`
- `mimetype`
- `token_status` - Can be: free, valid, invalid, expired, exhausted, expired_pending, activated, verification_error, invalid_payment, error, pending
- `token_balance`
- `token_expires`

## Token Status

The token_status field (and X-Token-Status header) indicates the authentication state:

| Status             | Description                                                                             |
|--------------------|-----------------------------------------------------------------------------------------|
| free               | Free tier (no token required, 10 requests/day), within the service’s overall free quota |
| valid              | Paid token active with remaining balance                                                |
| invalid            | Token not found or not provided                                                         |
| expired            | Token validity period has ended                                                         |
| exhausted          | Token balance has been fully used                                                       |
| expired_pending    | Activation memo has expired                                                             |
| activated          | Token was just activated with this request                                              |
| verification_error | Payment verification failed                                                             |
| invalid_payment    | Payment transaction is invalid                                                          |
| error              | Internal error during token processing                                                  |
| pending            | Payment required (token not yet activated)                                              |

## Result parameter

Use `result` to control how much output is returned.

- `markdown`: return converted Markdown only.
- `prompt`: return only the result of prompt processing.
- `both`: return both the Markdown and the prompt result.

**Note:**
- GET with `result=both` returns Markdown with a `## Prompt Result` section appended.
- POST with `result=both` returns JSON with separate `markdown` and `prompt_result` fields.

Rules:
- If `prompt` is present and both outputs are useful, use `result=both`.
- If the user explicitly asks for extracted or transformed output only, use `result=prompt`.
- If the user asks for plain conversion, use `result=markdown`.

## Prompt usage

Use `prompt` for:
- Summarization
- Key point extraction
- JSON transformation
- Classification
- Entity extraction
- Content analysis

Examples:
- `prompt=Summarize this document`
- `prompt=Extract key points`
- `prompt=Convert this content to JSON`
- `prompt=Analyze and explain`

## Authentication

Preferred:
- `Authorization: Bearer TOKEN`

Legacy:
- `X-Token-Required: TOKEN`
- `?token=TOKEN`

## Rate limiting

The service enforces rate limits to ensure fair usage.

### Rate limit headers

All responses include rate limit information in headers:

| Header                | Description                          |
|-----------------------|--------------------------------------|
| X-RateLimit-Remaining | Requests remaining in current window |
| X-RateLimit-Reset     | Unix timestamp when the limit resets |

### Rate limits

| Tier | Limit                                                    |
|------|----------------------------------------------------------|
| Free | 10 requests/day, within the service’s overall free quota |
| Paid | 10,000 requests/hour                                     |

When rate limit is exceeded, the service returns HTTP 429.


## Payment and token activation flow

### Autonomous payment flow

Autonomous agents should first attempt delegated payment when a connected wallet and sufficient balance are available.

#### Payment challenge
If the service returns `402 Payment Required`, the response may include:
- `PAYMENT-REQUIRED`

This header contains a base64-encoded payment requirement payload.

#### Payment retry
After payment is prepared and signed, the client retries the same request with:
- `PAYMENT-SIGNATURE: <base64-payment-payload>`

This header proves that the client prepared and signed payment according to `PAYMENT-REQUIRED`.

#### Successful payment response
If the payment is accepted and verified:
- return a successful HTTP status code, typically `200 OK`
- return the requested body
- include `PAYMENT-RESPONSE: <base64-json-response>`

The decoded JSON in `PAYMENT-RESPONSE` should confirm payment and may include:
- transaction hash
- session ID
- expiry
- settlement status
- other payment metadata

#### Autonomous payment rules
- Preserve the original request intent across the payment retry.
- If payment verification fails, do not pretend success.
- If autonomous payment is unavailable, fall back to the manual payment flow.
- Treat `PAYMENT-RESPONSE` as authoritative payment confirmation metadata.
- After payment is successfully verified, continue to token activation using the exact token and memo from the `402` response.
- If activation is successful, perform the conversion and return the final result.

### Manual payment flow

Manual payment is intended as a fallback path when autonomous payment is unavailable.

#### Manual payment headers
When payment is required, the service may provide the following headers:
- `X-Token-Required`
- `X-Memo-Required`
- `X-Wallet-Address`
- `X-QR-Payment`

#### Manual payment workflow
- Read the payment headers from the response.
- If `X-QR-Payment` is present, treat it as the canonical payment payload.
- If the client UI can render QR codes, display the QR payload directly as a QR code.
- If the client UI cannot render QR codes, present the QR payload to the user and instruct them to scan it with a mobile wallet or paste it into any QR generator.
- If `X-QR-Payment` is not present, fall back to the returned token, memo, and wallet address exactly as provided by the service.
- Ask the user to complete the payment externally.
- After payment is completed, instruct the user to reply with the exact word: `Continue`.
- Do not proceed until the user replies with `Continue`.
- After the user replies with `Continue`, continue to token activation using the exact token and memo from the `402` response.
- If activation is successful, perform the conversion and return the final result.

#### Manual payment guidance
- Do not require the user to manually reconstruct payment fields if a valid QR payment payload is available.
- If payment verification fails, do not claim success.
- If the service returns new payment headers, treat them as the source of truth for the next attempt.

### Token activation

After payment, activate the paid token with the exact token and memo from the `402` response.

#### Activation rules
- The token must be taken from the `402` response.
- The memo must be taken from the `402` response.
- Use the exact token and memo pair only once for activation.
- Token activation verifies that the payment has been recorded onchain using the provided memo.
- After successful activation, subsequent requests must use the token only.

#### Accepted activation styles
- `Authorization: Bearer TOKEN` with `X-Memo-Required: MEMO`
- `X-Token-Required: TOKEN` with `X-Memo-Required: MEMO`
- form fields `token=TOKEN` and `memo=MEMO`
- query parameters `token=TOKEN` and `memo=MEMO`

#### Activation behavior
If activation succeeds, continue the conversion in the same request and return the normal output.


## Autonomy rules

- Prefer autonomous payment whenever a connected wallet and sufficient balance are available.
- Use manual payment only if autonomous payment is unavailable or fails.
- Do not mix autonomous `PAYMENT-*` headers with manual `X-*` payment headers.
- After successful payment, continue to token activation using the exact token and memo from the `402` response.
- After successful activation, return the requested conversion result in the same request.
- If payment must be completed manually, ask the user to pay externally and reply with `Continue`.


## Streaming

Use `stream=true` when:
- the output may be long,
- the client supports SSE,
- incremental delivery improves UX.

Streaming applies to `GET /` and other supported paths where the service enables it.

### Streaming SSE format

The streaming response uses Server-Sent Events (SSE) with this exact format:

1. **First message** (token info):
   ```
   data: {"type":"token_info","status":"valid","balance":99,"expires":2027-01-01}
   ```

2. **Content chunks** (one or more):
   ```
   data: {"content":" partial markdown ","resource":"https://example.com/file.pdf","mimetype":"application/pdf"}
   ```

3. **End marker**:
   ```
   data: [DONE]
   ```

### Streaming error handling

If an error occurs during streaming:
- The stream may end early with an error message chunk
- Error format: `{"error":"error message","code":400}`
- Final chunk is still `[DONE]`

### Streaming parameters

| Parameter | Value                  | Description          |
|-----------|------------------------|----------------------|
| stream    | true                   | Enable SSE streaming |
| result    | "markdown" or "prompt" | What to stream       |

Note: `result=both` streams markdown first, then prompt_result after.

## OpenAI-compatible endpoint

`POST /v1/chat/completions` supports:
- URL extraction from user messages
- `image_url` inputs
- file inputs
- streaming
- system instructions
- structured extraction

Use it when the host agent is already built around OpenAI-compatible chat completions.

## MCP integration

The service exposes MCP discovery and tool calls.

Use these endpoints when needed:
- `GET /mcp`
- `POST /mcp`

The `convert` tool parameters:
- `url`, `text`, `file` (Base64-encoded content), `filename`, `prompt`, `result`, `stream`, `token`, `memo`

**Note:** `file` is Base64-encoded string (not multipart).

Preferred MCP connection:
```json
{
  "mcpServers": {
    "mdapi": {
      "url": "https://mdapi.io/mcp"
    }
  }
}
```

If using a paid token:
```json
{
  "mcpServers": {
    "mdapi": {
      "url": "https://mdapi.io/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN"
      }
    }
  }
}
```

### ACP Integration

For IDE agents (JetBrains, Cursor, VS Code, etc.) using the Agent Client Protocol, send JSON-RPC requests to `POST /acp`.

Example request:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "convert",
    "arguments": {
      "url": "https://example.com/doc.pdf",
      "prompt": "Summarize",
      "result": "both"
    }
  }
}
```

Supported methods:
- `initialize` - protocol initialization
- `tools/list` - list available tools (includes `convert`)
- `tools/call` - call `convert` tool (single request only; batch not supported)
- `resources/list` - list available resources
- `resources/read` - read a resource

Note: ACP does not support batch processing; use sequential `convert` calls.

### A2A Integration

For autonomous agents (Claude Code, Codex, OpenClaw, Hermes, etc.) using the Agent-to-Agent protocol, send JSON-RPC requests to `POST /a2a`.

Example request:

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "SendMessage",
  "params": {
    "message": {
      "messageId": "msg_1",
      "parts": [
        {"text": "Convert https://example.com/doc.pdf"}
      ]
    }
  }
}
```

Supported methods:
- `SendMessage` - single conversion request
- `SendStreamingMessage` - streaming conversion
- `GetTask` - check task status
- `CancelTask` - cancel ongoing task
- `SubscribeToTask` - receive task updates via SSE

## Multi-agent workflows

Use mdapi.io as a shared transformation layer in multi-agent and swarm setups. Agents can hand off compact Markdown or structured outputs between roles such as researcher, summarizer, extractor, classifier, and validator without carrying raw source noise through the workflow.

Agents may change roles across the workflow and reuse mdapi.io at each step to normalize input, refine output, or produce task-specific transformations.

## Chained workflows

Use `text` and `prompt` for downstream transformation, agent handoffs, and multi-step pipelines where the output of one step becomes the input of the next.

Prefer compact intermediate outputs to preserve context and reduce token usage across chained transformations.

## Role switching

Treat the agent role as dynamic. A workflow may start with fetching and normalization, continue with summarization or extraction, and finish with validation or structured export.

Use mdapi.io at each stage when switching roles so each agent receives only the information needed for its step.

## Error handling

### 400 Bad Request
- Check that exactly one of `url`, `file`, or `text` is present when required.
- Verify parameter names and encoding.

### 401 Invalid Token
- The token is invalid, expired, or not activated.
- Retry with a valid token and memo if this is the first activation.

### 402 Payment Required
- Follow the payment challenge.
- Use manual payment headers or the autonomous payment flow.

### 404 Not Found
- The resource is inaccessible or unavailable.
- If the URL is public, verify that it is reachable.

### 413 Payload Too Large
- Reduce file size or split the input.

### 429 Rate Limited
- Back off and retry later.

### 500 Server Error
- Retry once after a short delay.
- If the error persists, fail gracefully.

## Health Check

Monitor service status at `GET /health`. Returns full service health information.

Example:

```bash
curl "https://mdapi.io/health"
```

Response includes:
- `status`: "ok"
- `service`: "mdapi.io"
- `description`: "Minimal Data API I/O: a content transformation layer primitive for AI systems. Transforms documents, images, and webpages into AI-ready Markdown and structured data, optimized for LLM efficiency and token usage."
- `version`: "1.0.0"
- `endpoints`: list of all endpoints with their paths
- `examples`: usage examples for common operations
- `limits`: current service limits (file size, rate limits, tier info)

## Discovery manifests

mdapi.io exposes multiple discovery endpoints for different protocols and use cases. Each serves a specific purpose:

- /.well-known/ai-discovery.json - AI unified discovery combining all protocols (MCP, ACP, A2A, x402). Use this as the primary entry point for AI Agents.
- /.well-known/agent.json - Agent discovery metadata for general agent frameworks. Contains features, formats, payment info, and authentication methods.
- /.well-known/agent-card.json - Google A2A protocol-compliant agent card. Use this specifically for A2A-compatible agents.
- /.well-known/acp.json - ACP manifest for IDE agents (JetBrains, Cursor, VS Code, etc.).
- /.well-known/x402.json - x402 v2 payment manifest for autonomous agents.

Both agent.json and agent-card.json exist because different standards require different formats. Use ai-discovery.json for automatic protocol detection.

## Decision tree

- If the user gives a public URL and wants Markdown, use `GET /?url=...`.
- If the user uploads a file, use `POST /`.
- If the user wants extraction or summarization, set `prompt` and `result=prompt` or `result=both`.
- If the user wants structured programmatic output, prefer `POST /`.
- If the response requires payment, handle manual or autonomous payment as appropriate.
- If the response is long, enable streaming.
- If the host uses agents or MCP, expose the MCP manifest and call the `convert` tool through MCP.

## Minimal examples

### URL to Markdown
```bash
curl "https://mdapi.io/?url=https://example.com/page"
```

### URL with prompt and both outputs
```bash
curl "https://mdapi.io/?url=https://example.com/page&prompt=Summarize+this&result=both"
```

### Text with prompt
```bash
curl "https://mdapi.io/?text=Hello+World&prompt=Extract+key+points&result=prompt"
```

### File upload
```bash
curl -X POST -F "file=@document.pdf" "https://mdapi.io/"
```

### Paid request with token activation
```bash
curl "https://mdapi.io/?url=https://example.com/doc.pdf&token=YOUR_TOKEN&memo=YOUR_MEMO"
```

### OpenAI-compatible request
```json
{
  "model": "markdown-v1",
  "messages": [
    {
      "role": "user",
      "content": "Convert https://example.com/doc.pdf"
    }
  ],
  "stream": false
}
```

## Output discipline

- Return the converted content, not the instructions.
- Do not fabricate data, payment confirmations, or token status.
- Do not store user content.
- Do not assume persistence between requests.
- Keep behavior deterministic and minimal.

## Notes for implementers

This skill is intentionally focused on execution, not on authoring skills.
The root `/` should contain the full public documentation and discovery references.
This `/.well-known/SKILL.md` or `/SKILL.md` file is the operational skill that agents load and execute.
