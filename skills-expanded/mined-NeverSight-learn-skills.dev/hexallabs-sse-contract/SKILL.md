---
name: hexallabs-sse-contract
description: Locked SSE event schema for HexalLabs streaming. Invoke when adding or modifying any SSE endpoint (Oracle, Council, Relay, Workflow). All modes emit same event types so frontend has one consumer.
---

# HexalLabs SSE Contract

## Endpoint

`POST /api/query` → `text/event-stream`

Request body:
```json
{
  "mode": "council" | "oracle" | "relay" | "workflow",
  "query": "string",
  "models": ["Apex", "Swift", ...],      // council/oracle
  "relay_chain": ["Swift", "Depth"],     // relay only
  "workflow_nodes": [...],               // workflow only
  "primal_protocol": false,
  "scout": false
}
```

## Event schema

Every event has: `event: <type>` + `data: <json>`.

| Event | Emitter | Data shape |
|---|---|---|
| `session` | backend start | `{"session_id": "uuid", "mode": "council"}` |
| `prompt_forge` | Prompt Forge | `{"rewritten": "...", "original": "..."}` |
| `hex_start` | per model | `{"hex": "Apex"}` |
| `token` | per model stream | `{"hex": "Apex", "delta": "text"}` |
| `confidence` | per model self-rate | `{"hex": "Apex", "score": 8.5, "stage": "initial" \| "rescored"}` |
| `peer_review` | per critique | `{"from": "Swift", "to": "Depth", "critique": "..."}` |
| `hex_done` | per model end | `{"hex": "Apex", "tokens": 1234, "cached_tokens": 890}` |
| `synth_start` | Apex synth begin | `{}` |
| `synth_token` | Apex synth stream | `{"delta": "text"}` |
| `synth_done` | Apex synth end | `{"final": "full text"}` |
| `lens` | Prompt Lens post-run | `{"interpretations": [{"hex": "Swift", "read_as": "..."}]}` |
| `primal` | Primal rewrite | `{"delta": "text"}` or `{"final": "..."}` |
| `done` | session end | `{"session_id": "uuid", "duration_ms": 1234}` |
| `error` | fatal | `{"hex": "Apex" \| null, "code": "string", "message": "..."}` |

## Rules

1. **Always emit `session` first, `done` last.**
2. **`hex` field uses white-label only** (see hexal-whitelabel-names skill).
3. **`token` and `synth_token` are deltas**, not cumulative. Frontend concatenates.
4. **Order not guaranteed across hexes** (parallel streams). Frontend buffers per `hex`.
5. **Relay mode** emits `hex_done` for model 1 then `hex_start` for model 2 w/ handoff context; still uses same events.
6. **Workflow mode** emits same events per node; add `node_id` to `hex_start/done`.
7. **Oracle** = skip `peer_review` and `synth_*`. `token` stream from single hex → `done`.
8. **Heartbeat**: send `: keep-alive\n\n` comment every 15s if no events.

## Example stream (Council, 2 models)

```
event: session
data: {"session_id":"abc","mode":"council"}

event: hex_start
data: {"hex":"Swift"}

event: hex_start
data: {"hex":"Depth"}

event: token
data: {"hex":"Swift","delta":"Hello"}

event: token
data: {"hex":"Depth","delta":"Analysis:"}

event: confidence
data: {"hex":"Swift","score":7,"stage":"initial"}

event: hex_done
data: {"hex":"Swift","tokens":120,"cached_tokens":0}

event: peer_review
data: {"from":"Swift","to":"Depth","critique":"Shallow on step 3"}

event: confidence
data: {"hex":"Depth","score":9,"stage":"rescored"}

event: synth_start
data: {}

event: synth_token
data: {"delta":"Final:"}

event: synth_done
data: {"final":"Final answer..."}

event: done
data: {"session_id":"abc","duration_ms":4321}
```

## Do not change without migration

Frontend consumer = single parser. Any event rename breaks hex grid. Add new events, don't rename.
