---
name: managing-apache-geode
description: |
  Use when working with Apache Geode — apache Geode distributed cache
  management, region inspection, member health monitoring, and WAN gateway
  analysis. Covers locator status, server groups, partition distribution,
  persistent disk store health, and continuous query diagnostics. Read this
  skill before any Geode operations.
connection_type: geode
preload: false
---

# Apache Geode Management Skill

Monitor, analyze, and optimize Apache Geode clusters safely.

## MANDATORY: Discovery-First Pattern

**Always check cluster status and list regions before any data operations. Never assume region names or partition configurations.**

### Phase 1: Discovery

```bash
#!/bin/bash

GEODE_LOCATOR="${GEODE_LOCATOR:-localhost[10334]}"

echo "=== Cluster Status ==="
gfsh -e "connect --locator=$GEODE_LOCATOR" -e "list members" 2>/dev/null

echo ""
echo "=== Regions ==="
gfsh -e "connect --locator=$GEODE_LOCATOR" -e "list regions" 2>/dev/null

echo ""
echo "=== Disk Stores ==="
gfsh -e "connect --locator=$GEODE_LOCATOR" -e "list disk-stores" 2>/dev/null

echo ""
echo "=== Deployed JARs ==="
gfsh -e "connect --locator=$GEODE_LOCATOR" -e "list deployed" 2>/dev/null

echo ""
echo "=== Management REST API ==="
GEODE_REST="${GEODE_REST_URL:-http://localhost:7070}"
curl -s "$GEODE_REST/management/v1/members" 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
for m in data.get('memberStatuses', data.get('result', [])):
    print(f\"  {m.get('id','?')}: host={m.get('host','?')} status={m.get('status','?')}\")
" 2>/dev/null || echo "Management REST not available"
```

**Phase 1 outputs:** Member list, region inventory, disk stores, deployed JARs.

### Phase 2: Analysis

```bash
#!/bin/bash

GEODE_LOCATOR="${GEODE_LOCATOR:-localhost[10334]}"
REGION="${1:-my_region}"

echo "=== Region Details ==="
gfsh -e "connect --locator=$GEODE_LOCATOR" -e "describe region --name=$REGION" 2>/dev/null

echo ""
echo "=== Member Details ==="
gfsh -e "connect --locator=$GEODE_LOCATOR" -e "describe member --name=$(gfsh -e 'connect --locator=$GEODE_LOCATOR' -e 'list members' 2>/dev/null | grep -v "^$\|Name\|---" | head -1 | awk '{print $1}')" 2>/dev/null | head -25

echo ""
echo "=== Disk Store Details ==="
gfsh -e "connect --locator=$GEODE_LOCATOR" -e "describe disk-store --name=DEFAULT --member=$(gfsh -e 'connect --locator=$GEODE_LOCATOR' -e 'list members' 2>/dev/null | grep -v '^$\|Name\|---' | head -1 | awk '{print $1}')" 2>/dev/null | head -15

echo ""
echo "=== Gateway Senders ==="
gfsh -e "connect --locator=$GEODE_LOCATOR" -e "list gateways" 2>/dev/null || echo "No WAN gateways configured"

echo ""
echo "=== Indexes ==="
gfsh -e "connect --locator=$GEODE_LOCATOR" -e "list indexes" 2>/dev/null
```

## Output Format

```
GEODE ANALYSIS
==============
Members: [count] | Locators: [count] | Servers: [count]
Regions: [count] | Disk Stores: [count]

ISSUES FOUND:
- [issue with affected region/member]

RECOMMENDATIONS:
- [actionable recommendation]
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

