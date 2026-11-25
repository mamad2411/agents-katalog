---
name: managing-backblaze-b2
description: |
  Use when working with Backblaze B2 — backblaze B2 cloud storage management via
  the b2 CLI. Covers buckets, files, lifecycle rules, keys, and usage
  statistics. Use when managing B2 storage or reviewing bucket configurations
  and costs.
connection_type: backblaze-b2
preload: false
---

# Managing Backblaze B2

Manage Backblaze B2 cloud storage using the `b2` CLI.

## MANDATORY: Discovery-First Pattern

**Always discover available resources before performing analysis.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Account Info ==="
b2 get-account-info 2>/dev/null | jq '{accountId, allowed: .allowed}' || echo "Run: b2 authorize-account"

echo ""
echo "=== Buckets ==="
b2 list-buckets --json 2>/dev/null | jq -r '.[] | "\(.bucketId)\t\(.bucketName)\t\(.bucketType)\t\(.revision)"' | head -20

echo ""
echo "=== Keys ==="
b2 list-keys 2>/dev/null | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash

BUCKET_NAME="${1:?Bucket name required}"

echo "=== Bucket Details ==="
b2 get-bucket --show-size "$BUCKET_NAME" 2>/dev/null | jq '{
    bucketId, bucketName, bucketType, revision,
    options, defaultServerSideEncryption,
    fileLockConfiguration,
    totalSize: .totalSize,
    fileCount: .fileCount
}' | head -20

echo ""
echo "=== Recent Files ==="
b2 ls --long --recursive "$BUCKET_NAME" 2>/dev/null | head -30

echo ""
echo "=== Lifecycle Rules ==="
b2 get-bucket "$BUCKET_NAME" 2>/dev/null | jq '.lifecycleRules' | head -15

echo ""
echo "=== CORS Rules ==="
b2 get-bucket "$BUCKET_NAME" 2>/dev/null | jq '.corsRules' | head -15

echo ""
echo "=== Bucket Notification Rules ==="
b2 get-bucket "$BUCKET_NAME" 2>/dev/null | jq '.eventNotificationRules // []' | head -10

echo ""
echo "=== Large Unfinished Uploads ==="
b2 list-unfinished-large-files "$BUCKET_NAME" 2>/dev/null | head -10
```

## Output Format

```
BUCKET_ID                   BUCKET_NAME    TYPE       FILES    SIZE
abc123def456789             assets         allPublic  12450    45GB
ghi789jkl012345             backups        allPrivate 890      120GB
```

## Safety Rules
- Use read-only commands: `list-buckets`, `ls`, `get-bucket`, `get-account-info`
- Never run `delete-*`, `create-*`, `update-*` without explicit user confirmation
- Use `--json` with jq for structured output parsing
- Limit output with `| head -N` to stay under 50 lines

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

