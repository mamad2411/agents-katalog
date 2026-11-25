---
name: managing-google-drive-api
description: |
  Use when working with Google Drive Api — google Drive API management covering
  files, folders, shared drives, permissions, storage quotas, and activity
  analytics. Use when monitoring storage usage, analyzing file sharing patterns,
  reviewing permission health, managing Google Drive resources, or
  troubleshooting Drive API access and sync issues.
connection_type: google-drive
preload: false
---

# Google Drive API Management Skill

Manage and analyze Google Drive resources including files, permissions, shared drives, and storage.

## API Conventions

### Authentication
All API calls use Bearer OAuth 2.0 token, injected automatically.

### Base URL
`https://www.googleapis.com/drive/v3`

### Core Helper Function

```bash
#!/bin/bash

gdrive_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN" \
            -H "Content-Type: application/json" \
            "https://www.googleapis.com/drive/v3${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN" \
            "https://www.googleapis.com/drive/v3${endpoint}"
    fi
}
```

## Output Rules
- Target ≤50 lines per script output
- Use `jq` to extract only needed fields
- Never dump full API responses

## Phase 1: Discovery

```bash
#!/bin/bash
echo "=== About (User & Storage) ==="
gdrive_api GET "/about?fields=user,storageQuota" \
    | jq '{
        user: .user.emailAddress,
        storage_used_gb: (.storageQuota.usage | tonumber / 1073741824 | . * 10 | floor / 10),
        storage_limit_gb: (.storageQuota.limit | tonumber / 1073741824 | . * 10 | floor / 10),
        drive_usage_gb: (.storageQuota.usageInDrive | tonumber / 1073741824 | . * 10 | floor / 10),
        trash_usage_gb: (.storageQuota.usageInDriveTrash | tonumber / 1073741824 | . * 10 | floor / 10)
    }'

echo ""
echo "=== Recent Files ==="
gdrive_api GET "/files?pageSize=20&orderBy=modifiedTime%20desc&fields=files(id,name,mimeType,size,modifiedTime,owners)" \
    | jq -r '.files[] | "\(.name[0:30])\t\(.mimeType | split("/") | last | .[0:15])\t\(.size // "-")\t\(.modifiedTime[0:10])"' \
    | column -t | head -20

echo ""
echo "=== Shared Drives ==="
gdrive_api GET "/drives?pageSize=20&fields=drives(id,name,createdTime)" \
    | jq -r '.drives[] | "\(.id)\t\(.name[0:30])\t\(.createdTime[0:10])"' | head -15
```

## Phase 2: Analysis

### Storage & File Analysis

```bash
#!/bin/bash
echo "=== Largest Files ==="
gdrive_api GET "/files?pageSize=20&orderBy=quotaBytesUsed%20desc&fields=files(name,size,mimeType,modifiedTime)&q=trashed=false" \
    | jq -r '.files[] | "\(.size // 0 | tonumber / 1048576 | . * 10 | floor / 10) MB\t\(.name[0:30])\t\(.mimeType | split("/") | last | .[0:15])\t\(.modifiedTime[0:10])"' \
    | head -15

echo ""
echo "=== Files in Trash ==="
gdrive_api GET "/files?pageSize=20&q=trashed=true&fields=files(name,size,trashedTime)&orderBy=quotaBytesUsed%20desc" \
    | jq -r '.files[] | "\(.size // 0 | tonumber / 1048576 | . * 10 | floor / 10) MB\t\(.name[0:30])\t\(.trashedTime[0:10] // "")"' \
    | head -10

echo ""
echo "=== Files by Type ==="
gdrive_api GET "/files?pageSize=100&fields=files(mimeType)&q=trashed=false" \
    | jq -r '.files[] | .mimeType' | sort | uniq -c | sort -rn | head -10
```

### Sharing & Permission Health

```bash
#!/bin/bash
echo "=== Externally Shared Files ==="
gdrive_api GET "/files?pageSize=20&fields=files(name,shared,sharingUser,permissions)&q=sharedWithMe=true" \
    | jq -r '.files[] | "\(.name[0:30])\t\(.sharingUser.emailAddress // "?")"' | head -15

echo ""
echo "=== Files Shared with Anyone (link sharing) ==="
gdrive_api GET "/files?pageSize=20&fields=files(name,permissions)&q=visibility='anyoneWithLink'" \
    | jq -r '.files[] | "\(.name[0:30])\t\(.permissions | map(select(.type=="anyone")) | length) public perms"' | head -10

echo ""
echo "=== Recent Activity ==="
gdrive_api GET "/changes/startPageToken" | jq '.startPageToken'
gdrive_api GET "/activity/v2/activity?consolidationStrategy.legacy.period=day&pageSize=10" 2>/dev/null \
    || echo "Activity API requires separate enablement"
```

## Output Format

```
=== Google Drive: <email> ===
Storage: <used>GB / <limit>GB (Trash: <trash>GB)

--- Files ---
Total (page): <n>  Largest: <name> (<size>MB)

--- Sharing ---
Shared Drives: <n>
Public Links: <n>

--- By Type ---
document: <n>  spreadsheet: <n>  pdf: <n>
```

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

## Common Pitfalls
- **Fields parameter**: Always specify `fields` to limit response size and avoid quota waste
- **Query syntax**: Use `q` parameter with Drive query syntax (e.g., `trashed=false`, `mimeType='application/pdf'`)
- **Pagination**: Use `pageToken` from response `nextPageToken`; default page size is 100
- **Rate limits**: 12,000 queries/minute per project; 12 queries/second per user
- **MIME types**: Google Docs use `application/vnd.google-apps.*` MIME types
