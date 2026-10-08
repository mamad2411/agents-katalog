---
name: functional-verification
description: Use tgo-cli (staff) and tgo-widget-cli (visitor) to verify API and service changes at runtime, beyond static lint/build checks. Trigger after modifying backend API endpoints, service logic, chat flow, agent config, knowledge/RAG, workflow, or platform integration — requires local services to be running. Auto-detects changed services from git diff and runs the corresponding CLI smoke tests (system info, CRUD listing, chat e2e).
---

# functional-verification

## Purpose
Use tgo-cli (staff) and tgo-widget-cli (visitor) to verify API/service changes at runtime — beyond static lint/build checks.

## Trigger
After modifying backend API endpoints, service logic, chat flow, agent config, knowledge/RAG, workflow, or platform integration — when local services are running.

## Prerequisites
- Local services must be running (`make dev-all` or individual `make dev-*`)
- tgo-cli configured (`~/.tgo/config.json` with server + token, via `tgo auth login`)
- tgo-widget-cli configured (`~/.tgo-widget/config.json`, via `tgo-widget init`)

## What it does
1. Checks CLI build status and config availability
2. Verifies server reachability
3. Based on `git diff`, maps changed services to verification commands:

| Changed Service | Verification |
|----------------|-------------|
| tgo-api | `tgo system info`, `tgo auth whoami`, `tgo conversation list --limit 1` |
| tgo-ai | `tgo chat team --message "ping"`, `tgo agent list --limit 1` |
| tgo-rag | `tgo knowledge list --limit 1` |
| tgo-workflow | `tgo workflow list --limit 1` |
| tgo-platform | `tgo platform list` |
| tgo-api + visitor flow | `tgo-widget platform info`, `tgo-widget chat send --message "ping" --no-stream` |

4. Outputs pass/fail per check

## Usage
```bash
# Auto-detect from git diff
bash .skills/functional-verification/scripts/verify.sh

# Target specific service
bash .skills/functional-verification/scripts/verify.sh tgo-api

# Full smoke test (all checks)
bash .skills/functional-verification/scripts/verify.sh --all
```

## Manual verification commands

### Staff-side (tgo-cli)
```bash
TGO_CLI="node repos/tgo-cli/dist/index.js"

# System health
$TGO_CLI system info
$TGO_CLI auth whoami

# Chat e2e (sends to AI, gets response)
$TGO_CLI chat team --message "say ok"

# CRUD verification
$TGO_CLI agent list
$TGO_CLI provider list
$TGO_CLI knowledge list
$TGO_CLI workflow list
$TGO_CLI conversation list --limit 1
$TGO_CLI visitor list --limit 1
$TGO_CLI platform list
$TGO_CLI staff list
```

### Visitor-side (tgo-widget-cli)
```bash
WIDGET_CLI="node repos/tgo-widget-cli/dist/index.js"

# Platform & channel
$WIDGET_CLI platform info
$WIDGET_CLI channel info

# Chat e2e (visitor sends, AI responds via SSE)
$WIDGET_CLI chat send --message "say ok" --no-stream

# History
$WIDGET_CLI chat history --limit 3
```
