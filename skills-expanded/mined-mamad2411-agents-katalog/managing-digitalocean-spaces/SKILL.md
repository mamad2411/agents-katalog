---
name: managing-digitalocean-spaces
description: |
  Use when working with Digitalocean Spaces — digitalOcean Spaces object storage
  management via the AWS CLI (S3-compatible) and doctl CLI. Covers Spaces
  buckets, objects, CDN endpoints, CORS, and lifecycle policies. Use when
  managing DigitalOcean Spaces storage.
connection_type: digitalocean-spaces
preload: false
---

# Managing DigitalOcean Spaces

Manage DigitalOcean Spaces using `doctl` or AWS CLI with Spaces-compatible endpoints.

## MANDATORY: Discovery-First Pattern

**Always discover available resources before performing analysis.**

### Phase 1: Discovery

```bash
#!/bin/bash
export AWS_PAGER=""

DO_REGION="${DO_SPACES_REGION:-nyc3}"
SPACES_ENDPOINT="https://${DO_REGION}.digitaloceanspaces.com"

echo "=== Spaces (via doctl) ==="
doctl compute cdn list --format ID,Origin,Endpoint,TTL,CreatedAt --no-header 2>/dev/null | head -10

echo ""
echo "=== Spaces Buckets ==="
aws s3api list-buckets --endpoint-url "$SPACES_ENDPOINT" \
    --query 'Buckets[*].[Name,CreationDate]' --output text | head -20

echo ""
echo "=== Bucket Summary ==="
for bucket in $(aws s3api list-buckets --endpoint-url "$SPACES_ENDPOINT" --query 'Buckets[*].Name' --output text); do
    count=$(aws s3api list-objects-v2 --bucket "$bucket" --endpoint-url "$SPACES_ENDPOINT" --query 'KeyCount' --output text 2>/dev/null)
    echo "$bucket	objects=$count"
done | head -20
```

### Phase 2: Analysis

```bash
#!/bin/bash
export AWS_PAGER=""

DO_REGION="${DO_SPACES_REGION:-nyc3}"
SPACES_ENDPOINT="https://${DO_REGION}.digitaloceanspaces.com"
BUCKET_NAME="${1:?Space name required}"

echo "=== Space Objects (sample) ==="
aws s3api list-objects-v2 --bucket "$BUCKET_NAME" --max-items 20 \
    --endpoint-url "$SPACES_ENDPOINT" \
    --query 'Contents[*].[Key,Size,LastModified]' --output text | head -20

echo ""
echo "=== Space Size Summary ==="
aws s3 ls "s3://$BUCKET_NAME" --summarize --recursive --endpoint-url "$SPACES_ENDPOINT" 2>/dev/null | tail -3

echo ""
echo "=== CORS Configuration ==="
aws s3api get-bucket-cors --bucket "$BUCKET_NAME" \
    --endpoint-url "$SPACES_ENDPOINT" --output json 2>/dev/null | jq '.CORSRules' | head -15 || echo "No CORS rules"

echo ""
echo "=== Lifecycle Rules ==="
aws s3api get-bucket-lifecycle-configuration --bucket "$BUCKET_NAME" \
    --endpoint-url "$SPACES_ENDPOINT" \
    --query 'Rules[*].[ID,Status,Prefix]' --output text 2>/dev/null || echo "No lifecycle rules"

echo ""
echo "=== Bucket ACL ==="
aws s3api get-bucket-acl --bucket "$BUCKET_NAME" \
    --endpoint-url "$SPACES_ENDPOINT" \
    --query 'Grants[*].[Grantee.Type,Permission]' --output text

echo ""
echo "=== CDN Endpoints ==="
doctl compute cdn list --format ID,Origin,Endpoint,TTL,CreatedAt --no-header 2>/dev/null | grep "$BUCKET_NAME" | head -5
```

## Output Format

```
SPACE           REGION   OBJECTS    TOTAL_SIZE   CDN
assets          nyc3     12450      45GB         enabled
media           sfo3     890        120GB        disabled
```

## Safety Rules
- Use read-only commands: `list-*`, `get-*`, `ls`
- Never run `delete-*`, `put-*`, `rm` without explicit user confirmation
- Always include `--endpoint-url` for Spaces endpoints
- Include `export AWS_PAGER=""` at script start
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

