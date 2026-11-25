---
name: managing-make-integromat
description: |
  Use when working with Make Integromat — make (formerly Integromat) scenario
  management covering scenario inventory, execution history, connection health,
  webhook monitoring, and data store analysis. Use when auditing automation
  scenarios, investigating execution failures, monitoring operation quotas, or
  reviewing integration configurations.
connection_type: make
preload: false
---

# Make (Integromat) Management Skill

Manage and monitor Make automation scenarios, executions, and connected services.

## MANDATORY: Discovery-First Pattern

**Always list scenarios and connections before querying specific resources.**

### Phase 1: Discovery

```bash
#!/bin/bash

MAKE_API="https://us1.make.com/api/v2"

make_api() {
    curl -s -H "Authorization: Token $MAKE_API_TOKEN" \
         -H "Content-Type: application/json" \
         "${MAKE_API}/${1}"
}

echo "=== Make Organization ==="
make_api "organizations" | jq -r '.organizations[] | "\(.id)\t\(.name)\t\(.zone)"' | column -t

echo ""
echo "=== Scenarios Summary ==="
make_api "scenarios?pg[limit]=50" | jq -r '
    .scenarios[] |
    "\(.id)\t\(.name)\t\(.isEnabled // false)\t\(.scheduling.type // "manual")"
' | column -t | head -30

echo ""
echo "=== Connections ==="
make_api "connections" | jq -r '
    .connections[] |
    "\(.id)\t\(.name)\t\(.accountType)\t\(.metadata.status // "unknown")"
' | column -t | head -20
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Failed Executions (recent) ==="
make_api "scenarios" | jq -r '.scenarios[].id' | while read sid; do
    make_api "scenarios/${sid}/executions?pg[limit]=5" | jq -r --arg sid "$sid" '
        .executions[]? |
        select(.status == "failed") |
        "\($sid)\t\(.id)\t\(.status)\t\(.finished)"
    '
done | column -t | head -20

echo ""
echo "=== Operations Usage ==="
make_api "organizations" | jq -r '
    .organizations[] |
    "Org: \(.name) | Ops used: \(.operations.used // 0) / \(.operations.limit // "unlimited")"
'

echo ""
echo "=== Disabled Scenarios ==="
make_api "scenarios" | jq -r '
    .scenarios[] |
    select(.isEnabled == false) |
    "\(.id)\t\(.name)\tDISABLED\tLast: \(.lastExec // "never")"
' | column -t
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use pagination parameters to limit results
- Never dump full scenario blueprints -- extract key module names

## Output Format

Present results as a structured report:
```
Managing Make Integromat Report
═══════════════════════════════
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

- **Operation limits**: Make bills by operations -- monitor usage across all scenarios
- **Incomplete executions**: Stuck executions consume slots -- check and cancel stale runs
- **Connection expiry**: OAuth connections expire -- renew before scenarios fail
- **Webhook queue**: Webhooks queue data when scenarios are off -- data loss risk if queue overflows
- **Error handlers**: Scenarios without error handler routes silently fail -- always add error paths
- **Data stores**: Data store row limits depend on plan -- monitor capacity
