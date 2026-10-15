---
name: openclaw-log-report
metadata:
  version: "0.1.4"
description: |
  Parse OpenClaw session JSONL logs and upload structured telemetry to Langfuse
  via the Cobo Agentic Wallet TelemetryAPI. Zero external dependencies — only
  requires Python 3 and a valid caw installation (API key auto-detected).
  Use when: user wants to analyze an OpenClaw session, upload session telemetry,
  view session traces in Langfuse, or debug OpenClaw agent behavior.
---

# OpenClaw Log Report

Parse OpenClaw `session.jsonl` logs → structured telemetry → Langfuse.

## What It Does

Reads an OpenClaw session log file and uploads it as a structured trace to Langfuse:

```
Langfuse Trace
└── session:<id>                    ← root span (full session)
    ├── turn:0                      ← user message + agent response
    │   ├── OpenAI-generation       ← LLM call (model, tokens, latency)
    │   ├── skill_install:exec      ← tool call
    │   ├── OpenAI-generation
    │   ├── caw.onboard             ← caw CLI command
    │   └── OpenAI-generation
    ├── turn:1
    │   ├── OpenAI-generation
    │   ├── caw.wallet.balance
    │   └── ...
    └── turn:N
```

Each span includes:
- **Original timestamps** — latency reflects actual execution time
- **Input/Output** — user messages, assistant responses, tool results
- **Token usage** — per-generation input/output token counts
- **caw command classification** — 106 commands across 15 categories
- **Error detection** — failed commands, policy denials, process poll errors

## Prerequisites

1. **caw installed and onboarded** — the script reads API key from `~/.cobo-agentic-wallet/`
2. **Backend telemetry endpoint available** — `POST /api/v1/telemetry/session`
3. **Session JSONL file** — from `~/.openclaw/agents/main/sessions/`

## Usage

### Upload a session

```bash
python scripts/otel_report.py <session.jsonl>
```

The script auto-detects API URL and key from caw config. Override with env vars:

```bash
AGENT_WALLET_API_URL=https://api-core.agenticwallet.sandbox.cobo.com \
python scripts/otel_report.py session.jsonl
```

### Custom trace name

```bash
python scripts/otel_report.py --trace-name "bugbash-lishu-0403" session.jsonl
```

Default trace name format: `script_{user}@{hostname}_{MMDDHHmm}`, e.g. `script_ubuntu@baiyang-openclew-dev-v1_04061109`

### Upload multiple sessions

```bash
# Multiple files
python scripts/otel_report.py a.jsonl b.jsonl c.jsonl

# Glob pattern
python scripts/otel_report.py ~/.openclaw/agents/main/sessions/*.jsonl
```

### Upload by time range

Filters by **session content time** (not file modification time). Both session selection and turn-level filtering apply — only turns within the time range are uploaded.

```bash
# Last 2 hours — only uploads turns from the last 2h
python scripts/otel_report.py --since 2h

# Last 1 day
python scripts/otel_report.py --since 1d

# Specific time range (UTC+8)
python scripts/otel_report.py --since 2026-04-05T10:00 --until 2026-04-05T18:00

# A full day
python scripts/otel_report.py --since 2026-04-05 --until 2026-04-06

# Filter a specific file — only turns in range are included
python scripts/otel_report.py --since 8h ~/Downloads/session.jsonl

# Custom sessions directory + time range
python scripts/otel_report.py --since 2h /path/to/sessions/
```

Supported time formats: `2h` (hours ago), `30m` (minutes ago), `1d` (days ago), `2026-04-05`, `2026-04-05T10:00`

### Dry run (preview without uploading)

```bash
python scripts/otel_report.py --dry-run session.jsonl
```

Shows the span tree structure with timestamps and latencies.

### Dump JSON (debug)

```bash
python scripts/otel_report.py --dump session.jsonl
```

Prints the first turn's full JSON payload for inspection.

### Watch mode (continuous)

```bash
python scripts/otel_report.py --watch [sessions_dir]
```

Monitors a directory for new `.jsonl` files and auto-uploads.

### Upload latest session

```bash
python scripts/otel_report.py
```

Without arguments, uploads the most recent session file from the default path.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AGENT_WALLET_API_URL` | `https://api-core.agenticwallet.sandbox.cobo.com` | Backend API URL |
| `USER_ID` | auto-detected from session messages | User identifier in Langfuse |

## caw Command Categories

The script classifies 106 caw CLI subcommands into categories:

| Category | Examples |
|----------|---------|
| `onboarding` | onboard, onboard bootstrap, onboard self-test |
| `transaction` | tx transfer, tx call, tx sign-message, tx speedup |
| `query` | wallet balance, tx list, tx records, address list, status |
| `auth` | pending approve/reject, pact submit/status, policy create |
| `wallet` | wallet use/rename/archive/claim, address create |
| `agent` | agent status, agent api-key |
| `ap2` | ap2 purchase/cancel/search, ap2 shipping |
| `node` | node start/stop/status/health |
| `meta` | meta chains/tokens/prices, version, health, schema |
| `util` | util abi encode/decode, util base64, fetch |
| `dev` | faucet deposit/tokens, demo |
| `audit` | audit logs |
| `monitor` | track |

## Langfuse Dimensions

| Langfuse Dimension | Value | Source |
|-------------------|-------|--------|
| Trace Name | `script_{user}@{hostname}_{MMDDHHmm}` | User + hostname + timestamp (UTC+8), or custom via `--trace-name` |
| Session ID | OpenClaw session UUID | session.jsonl |
| User ID | Telegram sender_id or "unknown" | First user message |
| Tags | `[skill_name, "openclaw", provider, "upload:YYYYMMDD"]` | Session metadata + upload date |

## Constraints

- **Don't modify this script** — treat it as a read-only tool
- **Don't modify uploaded reports** in Langfuse
- Session files are read-only; never write to `~/.openclaw/`

## Security Notes

安装时 `npx skills` 可能显示 Socket / Snyk 安全告警，这些是脚本正常功能所需：

| 告警 | 原因 |
|------|------|
| **网络请求** | 脚本通过 `urllib.request` POST 数据到 TelemetryAPI（后端转发至 Langfuse） |
| **文件读取** | 读取 `~/.openclaw/` 下的 session.jsonl 日志文件 |
| **凭证访问** | 从 `~/.cobo-agentic-wallet/` 读取 caw API key 用于鉴权 |
| **主机信息** | 通过 `socket.gethostname()` 获取机器名写入 metadata |

脚本不包含任何恶意代码，所有网络请求仅发往配置的 `AGENT_WALLET_API_URL`。
