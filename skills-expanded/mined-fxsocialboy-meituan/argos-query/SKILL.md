---
name: argos-query
description: Search Argos service logs by PSM, keyword, or time range, query logs by logID, and analyze error log aggregation. Use when the user wants to inspect runtime logs, trace a request, search by keyword, or summarize error logs for a service.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# Argos Query Skill

Search Argos logs in four modes: centralized search, local file search, logID query, and error analysis.

## When to Use

Use this skill when the user wants to:

- search service logs by keyword
- search service logs by PSM, with or without keywords
- inspect a service's local file logs
- trace a request by `logid`
- aggregate and summarize error logs

## Hard Rules

1. If the result depends on `vregion` and the user did **not** specify it, **ask first**. Do not guess.
2. Do **not** probe multiple regions one by one to see which one returns logs.
3. Use multi-region queries only when the user explicitly asked for multiple regions.
4. Prefer `time_range` over raw timestamps unless the user explicitly gave an absolute time window.
5. `total: 0` is not a reason to silently switch `vregion`, `env`, or mode.

## Four Modes

| Mode | Trigger | Typical use |
|------|---------|-------------|
| Central Search | `psm` with optional `keywords` / `log_level` | Search centralized service logs |
| Local File | `psm` + any of `env`, `env_type`, `path` | PPE / instance-local log inspection |
| LogID Query | `logid` | Trace one request across services |
| Error Analysis | `psm` + `aggregator` | Aggregate top error sources |

## Quick Start

```bash
gdpa-cli run argos-query --session-id "$SESSION_ID" --input '<json_params>'
```

## High-Frequency Examples

### 1. Central search without keywords

```bash
gdpa-cli run argos-query --session-id "$SESSION_ID" --input '{
  "psm": "my.service.name",
  "vregion": "China-North",
  "time_range": "2h"
}'
```

Use this for the common "查这个服务最近一段时间的日志" case.

### 2. Keyword search

```bash
gdpa-cli run argos-query --session-id "$SESSION_ID" --input '{
  "psm": "my.service.name",
  "keywords": ["timeout"],
  "vregion": "US-East",
  "time_range": "1h"
}'
```

Use this for the common "查这个服务最近有没有 timeout/error 日志" case.

### 3. Keyword search with log level

```bash
gdpa-cli run argos-query --session-id "$SESSION_ID" --input '{
  "psm": "my.service.name",
  "keywords": ["error"],
  "log_level": "Error",
  "vregion": "Singapore-Central",
  "time_range": "30m"
}'
```

Use this when the user wants a narrower error-focused scan.

### 4. Local file search

```bash
gdpa-cli run argos-query --session-id "$SESSION_ID" --input '{
  "psm": "desrpc.stability.thrift_server",
  "vregion": "US-East",
  "env": "ppe_desrpc_test",
  "env_type": "ppe",
  "time_range": "3h"
}'
```

Use this for PPE verification or when the user clearly wants instance-local logs.

### 5. Query by logID

```bash
gdpa-cli run argos-query --session-id "$SESSION_ID" --input '{
  "logid": "021772604201988fdbddc55000210240c40819c720000d18743a7",
  "vregion": "Singapore-Central",
  "scan_span_in_min": 30
}'
```

Use this to trace a single request.

### 6. Error analysis

```bash
gdpa-cli run argos-query --session-id "$SESSION_ID" --input '{
  "psm": "desrpc.test.client",
  "aggregator": "location",
  "vregion": "EU-TTP2",
  "time_range": "1h"
}'
```

Use this for "Top error location / summary" style questions.

## Common Inputs

| Field | Required | Notes |
|-------|----------|-------|
| `psm` | most modes | Required for central search, local file, error analysis |
| `logid` | logID mode | Switches to trace query mode |
| `keywords` | central search | Optional array of search strings |
| `aggregator` | error analysis | Common value: `location` |
| `vregion` | usually yes | Ask user when missing and region matters |
| `time_range` | no | Prefer this over timestamps |
| `env`, `env_type`, `path` | local file only | Explicitly switches to local file mode |
| `scan_span_in_min` | logID mode | Search-back window in minutes |

## Region Guidance

- If the user gave a `vregion`, use it exactly.
- If the user wants multi-region results, use only the named regions.
- If the user did not provide a region and the answer could vary by region, ask:
  - "这个日志要查哪个 vregion？"
  - "如果要多 region，对比范围请明确给我。"
- Do not retry with `sg`, `us`, `euttp2` in sequence.

## Mode Selection Guidance

- Prefer **Central Search** for general service log queries, with or without keywords.
- Prefer **Local File** only when PPE / env / path matters, and make that intent explicit in the input.
- Prefer **LogID Query** when the user already has a `logid`.
- Prefer **Error Analysis** when the user wants a summary, not raw logs.

## Output Expectations

### Central Search

Returns matching logs with content snippets and total hit count.

### Local File

Returns pod-level local log lines for the chosen `env` / `path`.

### LogID Query

Returns trace-style entries such as PSM, pod, IP, env, IDC, level, and message.

### Error Analysis

Returns aggregated error items such as top code locations, counts, and sampled messages.

## Defaults and Caveats

- `time_range` defaults differ by mode; check the reference file when precision matters.
- `start` / `end` use different units in Central Search vs Local File mode. Prefer `time_range`.
- `total: 0` often means wrong `vregion` or `env`, not necessarily "no logs exist".
- This skill is read-only.

## Reference

Detailed schemas, VRegion mapping, timestamp rules, output formats, and extended examples live in [SKILL_reference.md](./SKILL_reference.md).
