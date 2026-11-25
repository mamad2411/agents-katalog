---
name: local-session-search
description: Locate, inspect, and summarize locally ingested AI agent sessions through agent-trail ingest/BFF APIs. Use when the user asks to find/search/retrieve local sessions or messages, identify a session by session id/source/sourceSessionId, locate historical Codex/Claude/OpenClaw/opencode/qoder work, return session id/source/project/title/updatedAt/snippet, or use the ingest service/API to search sessions ("找 session", "搜索历史会话", "查本地 session", "通过 ingest 找").
---

# Local Session Search

Use this skill for local agent-trail sessions already ingested into SQLite. Prefer the BFF when working through the running Next app; use direct ingest for CLI/debugging or when the frontend port is unknown.

## Scope

This skill is the **agent-usage layer** on top of the global session-content search *primitive* (`GET /api/v1/sessions/search`). The primitive answers "which sessions match this text?"; this skill describes how an agent picks candidates from it and when to drill down.

Responsibility boundary:

- **ingest only searches and reads.** Its job is the four endpoints below: global search, session detail, `turns`, `messages`, and `lookup`. Nothing more.
- **the agent orchestrates everything else.** Candidate selection, deciding when to drill down, and any summarization happen agent-side — read the relevant turns/messages first, then summarize.
- **out of ingest scope, on purpose:** result summaries, related-session recommendations, deep-link orchestration, and complex filter sets. Do not push these back into the ingest API; keep them in the agent's own workflow.

## Bases

- Direct ingest default: `INGEST=http://localhost:8078`
- BFF frontend: `BASE=http://localhost:<frontend-port>`; the user may run it on `3000`, `3029`, `3030`, or another port
- Valid source tools: `openclaw`, `claude-code`, `codex`, `opencode`, `qoder`
- BFF global search also accepts `[tool]=all`

Health checks:

```bash
curl -sS "$INGEST/health" | jq
curl -sS "$BASE/api/agent-tools/all/health" | jq
```

If `GET /api/v1/sessions/search` returns `{"error":"Session not found","sessionId":"search"}`, the running ingest process is stale and does not include the global search route. Restart/rebuild ingest before relying on search.

## Workflow

### 1. Unknown session: search message bodies globally

Use the global session-content search endpoint. It returns one row per candidate session with enough metadata to decide whether to drill down.

```bash
curl -sS --get "$INGEST/api/v1/sessions/search" \
  --data-urlencode "q=WebSocket reconnection" \
  --data-urlencode "limit=5" \
  | jq '.results[] | {source, sessionId, sourceSessionId, displayTitle, project, updatedAt, snippet, matchCount}'
```

Via BFF:

```bash
curl -sS --get "$BASE/api/agent-tools/all/sessions/search" \
  --data-urlencode "q=WebSocket reconnection" \
  --data-urlencode "limit=5" \
  | jq '.results[] | {source, sessionId, sourceSessionId, displayTitle, project, updatedAt, snippet, matchCount}'
```

For source-scoped BFF search, replace `all` with the source tool:

```bash
curl -sS --get "$BASE/api/agent-tools/codex/sessions/search" \
  --data-urlencode "q=WebSocket reconnection" \
  --data-urlencode "limit=5" \
  | jq '.results[] | {source, sessionId, displayTitle, project, updatedAt, snippet}'
```

Search heuristics:

- Use 2-4 specific terms, not one broad token: `WebSocket reconnection`, `JWT refresh token`, `CORS preflight error`, project names, error messages, function/file names, or memorable phrases.
- Try aliases and language variants when the first pass is noisy.
- For Chinese/Japanese short phrases, include ASCII aliases such as the English library/API name, error code, or function/file name; the default FTS tokenizer can miss CJK-only queries.
- Inspect several candidates. Current sorting prioritizes recent sessions first, so a recent meta-discussion can beat the older target when the query is broad.
- Add `includeChildren=true` only when subagent/child sessions are relevant; root sessions are the default.
- Do not use `GET /api/v1/sessions?q=...` for message-body search. That endpoint only searches session metadata.

### 2. Known session id: fetch details, turns, or messages

Direct ingest works even if the source is not known:

```bash
SESSION_ID="..."
curl -sS "$INGEST/api/v1/sessions/$SESSION_ID" | jq '{id, source, sourceSessionId, displayTitle, project, updatedAt}'
curl -sS "$INGEST/api/v1/sessions/$SESSION_ID/turns?limit=20" | jq
curl -sS "$INGEST/api/v1/sessions/$SESSION_ID/messages?limit=100" | jq
```

Via BFF, use the source returned by search/details. BFF routes are source-scoped and return 404 when `[tool]` does not match the session source.

```bash
SOURCE="codex"
SESSION_ID="..."
curl -sS "$BASE/api/agent-tools/$SOURCE/sessions/$SESSION_ID" | jq
curl -sS "$BASE/api/agent-tools/$SOURCE/sessions/$SESSION_ID/turns?limit=20" | jq
curl -sS "$BASE/api/agent-tools/$SOURCE/sessions/$SESSION_ID/messages?limit=100" | jq
```

Use turns for replay-style summaries. Use messages when you need the flat chronological log or role filters.

### 3. Known session, unknown location inside it: search within the session

```bash
curl -sS --get "$INGEST/api/v1/sessions/$SESSION_ID/search" \
  --data-urlencode "q=reconnection" \
  | jq '.results[] | {ordinal, role, turnIndex, snippet}'
```

This returns message-level hits. Use the returned `turnIndex` or nearby `ordinal` to fetch enough turns/messages for context before summarizing.

### 4. Known external key/sourceSessionId: lookup first

When the user gives a source-specific external key, use lookup to convert it to the canonical ingest `sessionId`.

```bash
curl -sS --get "$INGEST/api/v1/sessions/lookup" \
  --data-urlencode "source=codex" \
  --data-urlencode "key=$SOURCE_SESSION_ID" \
  | jq '{id, source, sourceSessionId, displayTitle, project, updatedAt}'
```

## Reporting

When reporting candidates or the selected session, include:

- `source`
- `sessionId`
- `sourceSessionId` if present
- `displayTitle` or `name`
- `project`
- `updatedAt`
- why it matched: `snippet`, `matchCount`, or a short evidence summary

For summaries, cite the session metadata first, then summarize only after reading the relevant turns/messages. If the answer depends on a noisy search result, state that multiple candidates were inspected and why the selected one is the best match.

## Avoid

- Do not infer source from `messages[].sourceMetadata.sourceType`; it is not reliable. Use the parent session `source`.
- Do not assume the first result is correct for broad queries.
- Do not call direct ingest from frontend code; frontend code should use BFF routes.
- Do not summarize from only the global search snippet when the user asks for the session content. Fetch turns/messages first.
