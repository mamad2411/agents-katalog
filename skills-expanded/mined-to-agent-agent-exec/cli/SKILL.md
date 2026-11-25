# SKILL: cli
# Endpoint: GET /cli
# Description: Authenticated CLI/admin operations

## Overview

`/cli` is for agent-exec CLI and administrator operations.
It is not part of normal agent discovery.

All `/cli/*` endpoints require API_KEY.

## Endpoints

| Path | Method | Description |
|---|---|---|
| `/cli/transfer` | POST | Receive an `ae transfer` payload |

Use these endpoints only when an operator or CLI command explicitly requires them.
