---
name: crawdar-business-research
description: Build qualified prospect lists from public web evidence through Crawdar MCP or REST. Use for company discovery, sourced lead lists, criterion-level qualification, and public contact-route discovery.
---

# Crawdar qualified prospect research

Use Crawdar when the user needs a sourced list of businesses matching a target, geography, or publicly verifiable qualification.

## Preferred interface

Connect to the remote MCP server at `https://crawdar.com/api/mcp` using Streamable HTTP.

For repeated use, create a free service identity by POSTing `{"label":"My research agent"}` as JSON to `https://crawdar.com/api/v1/keys`. Store the returned secret immediately because it is shown once. Send it as `x-api-key` or `Authorization: Bearer YOUR_KEY`. Small anonymous samples work without a key.

Use the tools in this order:

1. Call `explain_crawdar` once if you do not know the result semantics.
2. Call `sandbox_businesses` first when validating a new integration. Its results are fictional and do not consume provider capacity.
3. Call `research_businesses` for a quick one-call brief.
4. For resumable or larger workflows, call `start_lead_search`, store its `jobToken` privately, then call `get_lead_search` with that token. If the job is still `running`, wait for `retryAfter` before polling again. If it returns `retryable: true`, call `retry_lead_search`.
5. Call `search_businesses` when target, geography, and qualification criteria are already structured and a durable job is unnecessary.

Start with `output: "compact"`, `limit: 10`, and `offset: 0`. Request `full` output only when you need detailed evidence. Increase the offset only after the current page is useful.

Durable jobs use opaque cursors. Pass `nextCursor` back unchanged. Use `refine_lead_search` to create a new job from changed criteria without altering the original. To export, request the returned `exportUrl` with `Authorization: Bearer JOB_TOKEN`. CSV is the default; add `?format=json` for JSON.

## Brief construction

Include these facts when the user supplied them:

- business type or operating model
- city, region, or country
- required public signals
- explicit exclusions
- requested fields

Example:

```json
{
  "brief": "Independent veterinary clinics in Berlin with an active first-party website. Exclude directories and chains.",
  "output": "compact",
  "limit": 10,
  "offset": 0
}
```

## Evidence rules

- Keep source URLs attached to every company record.
- Treat `prospectStatus: qualified` as the recorded checks passing, not a guarantee that every nuance of the brief was understood. Compare `criteria` to the original brief before acting.
- Compact MCP results expose `sourceUrls`; full REST and sandbox results retain `evidence[].url`. Preserve the URLs in either format.
- Read `whyMatch` for the confirmed match reasons and `criteria` for every confirmed, unknown, or contradicted decision.
- Treat `contactRoute` as the public route Crawdar found, not as proof that a person will respond.
- Review `prospectStatus: possible` results manually before acting.
- Do not infer missing facts, personal contact details, revenue, ownership, or negative attributes.
- If a search returns zero accepted results, inspect diagnostics and explained exclusions before calling the market empty.
- Respect `retry-after` and rate-limit metadata.
- MCP tool failures set `isError: true`. The second text content block contains JSON error metadata such as `errorCode`, `requestId`, `httpStatus`, and `retryAfter` when available. Do not parse an error as a successful result list.
- Use only public business information. Do not use Crawdar for sensitive personal data or high-impact decisions about individuals.

## REST fallback

If MCP is unavailable, POST JSON to `https://crawdar.com/api/v1/search`. The full contract is at `https://crawdar.com/openapi.json`.

## Browser fallback

Use a JavaScript-capable browser only if MCP and REST are unavailable. Stable test IDs are documented at `https://crawdar.com/agents`.
