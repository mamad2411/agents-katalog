---
name: managing-chronicle
description: |
  Use when working with Chronicle — google Chronicle SIEM security operations,
  threat detection, asset investigation, and log analysis. Covers UDM search
  queries, detection rule management, asset and IOC lookups, reference list
  management, and retrohunt execution. Use when investigating security events,
  reviewing detection rules, searching for IOCs, or analyzing Chronicle data
  ingestion health.
connection_type: chronicle
preload: false
---

# Google Chronicle Management Skill

Manage and analyze Google Chronicle detections, assets, IOC matches, and security telemetry.

## API Conventions

### Authentication
All API calls use `Authorization: Bearer $CHRONICLE_ACCESS_TOKEN` -- injected automatically via Google Cloud service account. Never hardcode tokens.

### Base URL
`https://$CHRONICLE_INSTANCE.backstory.chronicle.security/v2`

### Core Helper Function

```bash
#!/bin/bash

chronicle_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    local base="https://${CHRONICLE_INSTANCE}.backstory.chronicle.security/v2"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $CHRONICLE_ACCESS_TOKEN" \
            -H "Content-Type: application/json" \
            "${base}${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $CHRONICLE_ACCESS_TOKEN" \
            -H "Content-Type: application/json" \
            "${base}${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target <=50 lines per script output
- Always filter by relevant time range to avoid huge response sets
- Never dump full API responses

## Discovery Phase

```bash
#!/bin/bash
echo "=== Detection Summary ==="
chronicle_api GET "/detect/rules" \
    | jq '{total_rules: (.rules | length), enabled: ([.rules[] | select(.liveRuleEnabled == true)] | length)}'

echo ""
echo "=== Recent Alerts (last 24h) ==="
START=$(date -u -v-1d +%Y-%m-%dT%H:%M:%SZ)
END=$(date -u +%Y-%m-%dT%H:%M:%SZ)
chronicle_api GET "/detect/alerts?startTime=${START}&endTime=${END}" \
    | jq '.alerts | length | "Alerts (24h): \(.)"' -r

echo ""
echo "=== Data Sources ==="
chronicle_api GET "/feeds" \
    | jq '[.feeds[].feedSourceType] | group_by(.) | map({source: .[0], count: length}) | .[] | "\(.source): \(.count)"' -r
```

## Analysis Phase

### Alert Investigation

```bash
#!/bin/bash
echo "=== High Priority Alerts (last 7 days) ==="
START=$(date -u -v-7d +%Y-%m-%dT%H:%M:%SZ)
END=$(date -u +%Y-%m-%dT%H:%M:%SZ)
chronicle_api GET "/detect/alerts?startTime=${START}&endTime=${END}" \
    | jq -r '.alerts[] | select(.severity == "HIGH" or .severity == "CRITICAL") | "\(.detectionTime[0:16])\t\(.severity)\t\(.ruleName[0:50])\t\(.alertState)"' \
    | column -t | head -20

echo ""
echo "=== Alerts by Rule ==="
chronicle_api GET "/detect/alerts?startTime=${START}&endTime=${END}" \
    | jq -r '[.alerts[].ruleName] | group_by(.) | map({rule: .[0][0:50], count: length}) | sort_by(.count) | reverse | .[:10][] | "\(.count)\t\(.rule)"' \
    | column -t
```

### IOC Search

```bash
#!/bin/bash
IOC="${1:?IOC value required (IP, domain, or hash)}"

echo "=== IOC Lookup: $IOC ==="
chronicle_api GET "/ioc/listiocs?startTime=$(date -u -v-30d +%Y-%m-%dT%H:%M:%SZ)&endTime=$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    | jq -r --arg ioc "$IOC" '.response.matches[] | select(.artifact.domainName == $ioc or .artifact.ip == $ioc or .artifact.hashSha256 == $ioc) | {sources: .sources, categories: .iocIngestTime, firstSeen: .firstSeenTime, lastSeen: .lastSeenTime}'
```

### Rule Health

```bash
#!/bin/bash
echo "=== Detection Rules Status ==="
chronicle_api GET "/detect/rules" \
    | jq -r '.rules[] | "\(if .liveRuleEnabled then "LIVE" else "OFF" end)\t\(.ruleType)\t\(.ruleName[0:50])"' \
    | sort | column -t | head -20

echo ""
echo "=== Rules with Recent Detections ==="
START=$(date -u -v-7d +%Y-%m-%dT%H:%M:%SZ)
chronicle_api GET "/detect/rules" | jq -r '.rules[].ruleId' | head -10 | while read RULE_ID; do
    RESULT=$(chronicle_api GET "/detect/rules/${RULE_ID}/detections?startTime=${START}")
    COUNT=$(echo "$RESULT" | jq '.detections | length')
    NAME=$(chronicle_api GET "/detect/rules/${RULE_ID}" | jq -r '.ruleName')
    echo "$COUNT\t$NAME"
done | sort -rn | column -t
```

## Output Format

Present results as a structured report:
```
Managing Chronicle Report
═════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

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

- **Time format**: Always use RFC 3339 format (`2024-01-01T00:00:00Z`)
- **UDM vs raw logs**: Search queries use Unified Data Model fields, not raw log fields
- **YARA-L rules**: Detection rules use YARA-L 2.0 syntax, not standard regex
- **Rate limits**: API rate limits vary by endpoint -- use exponential backoff
- **Instance-specific URL**: Each Chronicle instance has a unique subdomain
