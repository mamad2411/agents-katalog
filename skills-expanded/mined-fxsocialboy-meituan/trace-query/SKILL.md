---
name: trace-query
description: Query BytedTrace distributed tracing data by trace_id across multiple regions (Singapore, US-East, EU-TTP2, US-EastRed, US-TTP, US-TTP2, China-North)
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# Trace Query

Query BytedTrace distributed tracing data by trace_id across multiple regions.

## Usage

```
/trace-query trace_id=<trace_id> [vregion=<vregion>] [time_range=<time_range>]
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| trace_id | string | Yes | - | The trace ID to query (e.g., '5ae9863e-1065-4a6b-276f-0dab00000000') |
| vregion | string | No | Singapore-Central | Target region(s), comma-separated for multiple regions. Supported: Singapore-Central, US-East, EU-TTP2, US-EastRed, US-TTP, US-TTP2, China-North |
| time_range | string | No | 10m | Time range for query (e.g., '5m', '1h', '24h') |
| start | int64 | No | now-10m | Start time (Unix timestamp) |
| end | int64 | No | now | End time (Unix timestamp) |
| summary | bool | No | true | Include summary information in response |
| trace_format_options | []string | No | polish,group_low_level_trace,add_peer_info_in_rpc_span,add_span_ext_abstract | Trace formatting options |

## Examples

### Query trace in Singapore region

```
/trace-query trace_id=5ae9863e-1065-4a6b-276f-0dab00000000 vregion=Singapore-Central
```

### Query trace in multiple regions

```
/trace-query trace_id=413ef3dc61fc1da220fce1df888abb03 vregion=Singapore-Central,US-East,China-North
```

### Query trace with custom time range

```
/trace-query trace_id=762d99494eb5950527e9641b238761cd vregion=US-TTP time_range=1h
```

## Supported Regions

| VRegion | Trace Region | BaseURI |
|---------|--------------|---------|
| Singapore-Central | Singapore-Central | https://bytedtrace-sg.tiktok-row.org |
| US-East | US-East | https://bytedtrace-us.tiktok-row.org |
| EU-TTP2 | EU-TTP2 | https://bytedtrace-euttp2.tiktok-eu.org |
| US-EastRed | US-EastRed | https://bytedtrace-i18n.tiktok-eu.org |
| US-TTP | US-TTP | https://bytedtrace-og.tiktok-us.org |
| US-TTP2 | US-TTP2 | https://bytedtrace-og.tiktok-us.org |
| China-North | China-North | https://bytedtrace.byted.org |

## Response Format

The response includes:

- `error_code`: API error code (0 = success)
- `error_type`: Error type if any
- `error_message`: Error message if any
- `data`: Response data containing:
  - `root_info`: Root span information including sampling type, trace ID, timing
  - `transactions`: Array of trace transactions with spans, tags, and metadata
  - `summary`: Summary information including span counts and highlighted errors
  - `scan_time_range`: Time range that was scanned
  - `is_normal`: Whether the trace is normal

## API Client

The underlying API client is located at:

```
pkg/devflow-api-clients/impl/bytedtrace/
├── client.go      # Client initialization and configuration
├── helper.go      # Helper functions for headers
├── vregion.go     # VRegion configuration mapping
└── gen/
    ├── service.go # Generated service interface
    └── model/     # Generated request/response models
```

## Implementation Details

The skill uses the BytedTrace HTTP API:

- **Endpoint**: `POST /trace_api/v1/trace/query_transactions`
- **Authentication**: JWT Token (obtained via `region.GetJWT()`)
- **Request Format**: JSON with trace_id, regions, time range, and formatting options
- **Response Format**: JSON with transactions, spans, and summary data
