---
description: Ingress wire policy, parser budgets, edge parity, chaos verification
globs:
  - internal/ingestion/**
  - deploy/nginx/lua/**
  - scripts/fault/parser*
alwaysApply: false
---

# Parser and Ingress Wire Policy

## Purpose

Scope: `internal/ingestion` + nginx edge seam only. Admin JSON uses `pkg/coldpath` 64KiB - not this file. XDP: `edge.mdc`.

Design goals: reject hostile wire early (0 allocs on reject); close slow streams; edge-tracker parity; control cohort p99 < **80 ms** under chaos.

## POST /track parity (mandatory)

| Rule | Edge (`edge_track_policy.lua`) | Tracker (`http1TrackEdgePolicy`) |
| :--- | :---: | :---: |
| `Content-Length` required | yes | yes |
| Chunked rejected | yes | yes |
| Duplicate/obfuscated `TE` rejected | yes | yes |

Verify: `go test ./internal/ingestion/ -run=TestChaos_CrossHop_NginxGnet -count=1` - `differential_count=0`.

Chunked allowed on **`POST /openrtb/bid`** only.

Implementation pairs: `http1TrackEdgePolicy` <-> `deploy/nginx/lua/edge_track_policy.lua`; `http1IngressCanonical` for differential tests.

## GET /click

Query-only; strict UUID `campaign_id`. Gate: `EDGE_EXPOSE_CLICK` on edge.

## HTTP/1 incomplete-body

| Knob | Default |
| :--- | :---: |
| `HTTP1_INCOMPLETE_MAX` | 3 |
| `HTTP1_BODY_IDLE_MS` | 5000 |
| `MaxRequestBodySize` | 1 MiB |

Metric: `ad_http1_incomplete_close_total{reason}`. H2: `H2_INCOMPLETE_MAX=3`.

## Framing budgets

| Rule | Detail |
| :--- | :--- |
| Chunk extensions | `;` rejected; hex overflow guard; cap > 64 KiB dropped |
| H2 header block | Cap 16 KiB -> `RST_STREAM` |
| TE.TE | Obfuscation rejected |
| OpenRTB scan | `ORTB_SCAN_MAX_BYTES=262144`, `ORTB_MAX_QUOTE_CHECKS=65536` |
| Protobuf | `PROTO_MAX_FIELDS=256`; wire budget before `UnmarshalVT` |
| HPACK | Continuation cap 8 octets |
| vtproto hot patch | `make proto` -> `patch-vtproto-hotpath` -> `appendReuseBytes` (`pb/unmarshal_helpers.go`) |

## JSON parse budgets

| Constant | Default |
| :--- | ---: |
| `MaxJSONTotalWSkip` | 4096 |
| `MaxJSONStringScanBytes` | 65536 |
| `MaxJSONStringEscapes` | 16384 |
| `MaxJSONKeyPairs` | 10000 |
| `MaxJSONDepth` | 16 (track), 32 (ORTB) |
| `JSON_STRICT_UTF8` | on |

## Sustained chaos

~90% valid protobuf + ~10% chaos. Pass criteria:

- Control p99 < **80 ms**
- `WorkerPoolRejectTotal` delta **0**
- >= 500 control samples

```bash
bash scripts/fault/parser_chaos_drill.sh
bash scripts/fault/parser_chaos_load.sh --duration=300s --rps=5000 --chaos-pct=10
go test ./internal/ingestion/ -run=TestChaos_ParserSecurity -count=1
```

Chaos tests emit `fault_proof proof=open|closed`.

## Verification

| Step | Command |
| :--- | :--- |
| Cross-hop | `go test ./internal/ingestion/ -run=TestChaos_CrossHop_NginxGnet` |
| TE/proto/HPACK | `go test ./internal/ingestion/ -run='TestChaos_TE_TE\|TestChaos_Proto_FieldBudget\|TestChaos_HPACK'` |
| Alloc gates | `make test-alloc-gate` |
| Slow body | `go test ./internal/ingest/ -run=TestChaos_ParserSecurity_SlowBodyStall -count=1 -v` |

## Related rules

`edge.mdc`, `fault-tests.mdc`, `hot-path.mdc`, `testing.mdc`, `traffic.mdc`.
