# SKILL: cli.transfer
# Endpoint: POST /cli/transfer
# Description: Receive an ae transfer payload

## Overview

This endpoint is used by `ae transfer` to restore a backup payload on a
destination agent-exec machine.

It is disabled by default. The destination administrator must explicitly enable
remote transfer before this endpoint accepts restore requests.

## Request

```http
POST /cli/transfer
X-API-Key: <API_KEY>
Content-Type: application/json
```

## Behavior

- `dryRun: true` validates the payload without writing files.
- confirmed restore requires `confirm: true`.
- secrets and restored categories are controlled by the transfer payload.

Prefer the CLI:

```bash
ae transfer --to host:3333 --apiKey <API_KEY> --dry-run
```
