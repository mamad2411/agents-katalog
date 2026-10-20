---
description: /click, /track, OpenRTB, macros, CAPI, Cost Sync, shard routing
globs:
  - internal/ingestion/**
  - web/src/**
  - deploy/nginx/**
alwaysApply: false
---

# Traffic Endpoints and Routing

## Purpose

Wire policy for parsers: `parser.mdc`. RTB runbook: `rtb.mdc`. Hot-path constraints: `hot-path.mdc`.

## Domain model

| Role | Host | Endpoints |
| :--- | :--- | :--- |
| Click / track | `trk.example.com` | `GET /click`, `POST /track` |
| OpenRTB | same or dedicated | `POST /openrtb/bid` |
| Telegram Mini App | edge | `GET /tg/click`, `GET /tg/impression` |
| Admin | `control.example.com` | `/admin`, `/api/v1/*` (:8188) |

Keitaro/Voluum: Campaign URL (click) != Postback URL (`/track`). Admin Integration tab shows both.

## GET /click

| Rule | Detail |
| :--- | :--- |
| Response | **302** redirect with macros; required `campaign_id` (UUID) |
| Filters | Campaign `click_filter_tier` or env `CLICK_FILTER_TIER_DEFAULT` (default `full`) |
| Tier `full` | Full FilterEngine; debits click budget (<= 1 EVALSHA) |
| Tier `light` | license, license RPS, emergency breaker, geo, schedule only; **no** stream publish or unified Lua debit |
| Tier `redirect_only` | License gates only; parse + macro redirect; **no** Redis; requires `CLICK_FILTER_REDIRECT_ONLY_LICENSED=1` on tracker |
| Fail-closed | `light` / `redirect_only` escalate to `full` when campaign has fraud enforcement flags (silent reject, segments, behavior flags, etc.) |
| Edge gate | `EDGE_EXPOSE_CLICK=true` (404 on :8180 when off). Tracker :8181-8184 always serves click |
| DMR referer | `legacy_dmr` profile only: `dmr=1` or campaign `dmr_enabled` uses **200** meta refresh + `location.replace` instead of 302; `strict` (default) is **302** only |
| Strict redirect | `redirect_compliance_mode=strict` (PG default): ignores `dmr_enabled` and `dmr=1`; `Referrer-Policy: no-referrer` on plain 302 |

### Click ingress latency budget (T27)

Per-path ceilings on synchronous `/click` work before first byte (302 or safe view). Exceeding a stage increments `ad_click_ingress_latency_budget_exceeded_total{stage}`.

| Stage | Env knob | Default | Ceiling |
| :--- | :--- | :--- | :--- |
| Local parse + L7 wire filters | (inline) | n/a | < 5 ms p99 target |
| FilterEngine + Redis EVALSHA | `FILTER_TIMEOUT_MS` | 5000 dev / 100 prod | hard deadline; 504 on exceed |
| Click upstream proxy | `CLICK_PROXY_TIMEOUT_MS` | 300 | fallback 302 when `proxy_timeout_fallback` enabled |
| Safe-page verify hop | `SAFE_PAGE_VERIFY_TIMEOUT_MS` | campaign/env | async on conversion; not on first click byte |

Banned on `landing_bundle.go` click hot path: sync `http.Get` / outbound verdict HTTP (use `click_proxy.go` only). Gate: `bash scripts/ci/static/click_ingress_hotpath_gate.sh`.

## POST /track

- Body: native JSON, protobuf (`ad_event_processor_native`), or OpenRTB 3 ingress per Traffic format setting.
- `Content-Length` required; chunked rejected (`parser.mdc`).
- FilterEngine -> stream -> processor -> **202**.

## POST /openrtb/bid

- OpenRTB 2.x JSON; chunked OK (extensions rejected).
- `RunAuction` -> bid/no-bid; **no** FilterEngine debit path.
- Exchange partners must use `/openrtb/bid`, not `/track`.

## RTB: /track vs /openrtb/bid

| | `POST /track` + `RTB_MODE` | `POST /openrtb/bid` |
| :--- | :--- | :--- |
| Auction | Only when `RTB_MODE=shadow\|live` | Always (when licensed) |
| After auction | FilterEngine chain | Bid/no-bid immediately |

Lifecycle with RTB on track: parse -> `applyRtbAuction` -> `FilterEngine.Check` -> 202 or reject.

| Knob | Default |
| :--- | :--- |
| `RTB_MODE` | `off` |
| `RTB_BUDGET_AUTHORITY` | `redis` |
| `RTB_PREBID_IVT` | `false` |

## Macros

| Token | Role |
| :--- | :--- |
| `{campaign_id}` | Required on click URL |
| `{click_id}` | S2S correlation (set by processor) |
| `{sub1}`...`{sub30}` | Source labels |
| UTMs | Stored + passthrough |

## S2S and CAPI

Inbound: affiliate -> `POST /track`. Outbound: worker -> Meta/Google/TikTok (Campaign -> CAPI & Postbacks).

**Postback token rotation** (`POSTBACK_ENCRYPTION_KEY`):

1. Pause sender
2. Re-encrypt configs
3. Restart sender + control
4. Smoke `ad_postback_dispatch_total{status="success"}`

No dual-key window.

## Cost Sync / True ROI

Join keys: calendar day + campaign; prefer UUID in ad-network id; pass network id as `sub2` on click URL.

## Zero-redirect tracking

Host `src/static/track.js` (admin dist); set `TRACK_CORS_ORIGINS`; script POSTs `/track`. `OPTIONS /track` -> 204 when origin allowed.

## Shard routing

```
slot = crc32_castagnoli(campaign_id) & 1023
shard = slot_table[slot]
```

| Endpoint | Campaign ID source |
| :--- | :--- |
| `/track`, `/tg/*` | Body DFA |
| `/click` | Query UUID |
| `/openrtb/bid` | Body peek or `X-Campaign-Id` |

Edge toggles: Platform settings -> Expose click / OpenRTB -> Apply to disk -> reload nginx.

## Related rules

`architecture.mdc`, `data-layer.mdc`, `edge.mdc`, `hot-path.mdc`, `parser.mdc`, `rtb.mdc`.
