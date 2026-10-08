---
name: managing-filestack
description: |
  Use when working with Filestack — filestack file upload, transformation, and
  delivery platform management covering uploads, transformations, CDN delivery,
  security policies, and usage analytics. Use when monitoring upload health,
  analyzing transformation usage, reviewing CDN performance, managing Filestack
  security policies, or troubleshooting file processing issues.
connection_type: filestack
preload: false
---

# Filestack Management Skill

Manage and analyze Filestack file upload, transformation, and delivery resources.

## API Conventions

### Authentication
All API calls use API key and optional security policy, injected automatically.

### Base URLs
- Upload: `https://www.filestackapi.com/api`
- CDN: `https://cdn.filestackcontent.com`
- Process: `https://process.filestackapi.com`

### Core Helper Function

```bash
#!/bin/bash

filestack_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Content-Type: application/json" \
            "https://www.filestackapi.com/api${endpoint}?key=$FILESTACK_API_KEY" \
            -d "$data"
    else
        curl -s -X "$method" \
            "https://www.filestackapi.com/api${endpoint}?key=$FILESTACK_API_KEY"
    fi
}

# File metadata
filestack_meta() {
    local handle="$1"
    curl -s "https://cdn.filestackcontent.com/${handle}/metadata"
}
```

## Output Rules
- Target ≤50 lines per script output
- Use `jq` to extract only needed fields
- Never dump full API responses

## Phase 1: Discovery

```bash
#!/bin/bash
echo "=== API Key Validation ==="
RESULT=$(curl -s "https://www.filestackapi.com/api/store/S3?key=$FILESTACK_API_KEY" -X POST -d '{}')
echo "$RESULT" | jq '{status: (if .error then "invalid" else "valid" end), message: .error // "OK"}'

echo ""
echo "=== App Info ==="
curl -s "https://www.filestackapi.com/api/app/$FILESTACK_API_KEY/security" \
    | jq '{security_enabled: .security_enabled}' 2>/dev/null || echo "Security status check complete"

echo ""
echo "=== Sample File Metadata ==="
HANDLE="${1:-}"
if [ -n "$HANDLE" ]; then
    filestack_meta "$HANDLE" \
        | jq '{filename: .filename, mimetype: .mimetype, size: .size, width: .width, height: .height, uploaded: .uploaded}'
else
    echo "Provide a file handle to check metadata"
fi
```

## Phase 2: Analysis

### File Health Check

```bash
#!/bin/bash
echo "=== File Validation ==="
HANDLE="${1:?File handle required}"

echo "--- Metadata ---"
filestack_meta "$HANDLE" \
    | jq '{filename: .filename, mimetype: .mimetype, size_kb: (.size / 1024 | floor), width: .width, height: .height}'

echo ""
echo "--- CDN Availability ---"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://cdn.filestackcontent.com/$HANDLE")
echo "CDN Status: HTTP $STATUS"

echo ""
echo "--- Transformation Test ---"
TRANSFORM_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://cdn.filestackcontent.com/resize=w:100/$HANDLE")
echo "Transform Status: HTTP $TRANSFORM_STATUS"
```

### Transformation & CDN Analytics

```bash
#!/bin/bash
echo "=== Transformation Health ==="
HANDLE="${1:?File handle required}"

# Test common transformations
for transform in "resize=w:200" "rotate=deg:90" "compress" "output=format:png"; do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}:%{time_total}" "https://cdn.filestackcontent.com/${transform}/$HANDLE")
    CODE=$(echo "$STATUS" | cut -d: -f1)
    TIME=$(echo "$STATUS" | cut -d: -f2)
    echo "$transform: HTTP $CODE (${TIME}s)"
done

echo ""
echo "=== Security Policy Check ==="
if [ -n "$FILESTACK_POLICY" ] && [ -n "$FILESTACK_SIGNATURE" ]; then
    echo "Security: enabled (policy and signature configured)"
    echo "Policy: $(echo $FILESTACK_POLICY | base64 -d | jq .)"
else
    echo "Security: disabled (no policy/signature)"
fi
```

## Output Format

```
=== Filestack App ===
API Key: <valid|invalid>  Security: <enabled|disabled>

--- File: <handle> ---
Name: <filename>  Type: <mimetype>  Size: <n>KB
CDN: <status>  Transforms: <status>

--- Transformation Health ---
resize: <ok|error>  rotate: <ok|error>  compress: <ok|error>
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
- **File handles**: Filestack uses opaque handles (not URLs) to reference files
- **Security policies**: When enabled, all URLs require policy and signature parameters
- **Transformation chaining**: Chain transforms with `/` separator (e.g., `resize=w:200/compress`)
- **Rate limits**: Vary by plan; check response headers for quota info
- **CDN caching**: Transformed files are cached on CDN; purging requires API call
- **Storage backends**: Default is S3; can also use GCS, Azure Blob, or Dropbox
