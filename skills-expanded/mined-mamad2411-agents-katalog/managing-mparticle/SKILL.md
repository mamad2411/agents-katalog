---
name: managing-mparticle
description: |
  Use when working with Mparticle — mParticle CDP management — monitor inputs,
  outputs, data plans, event forwarding, and audience health. Use when debugging
  event delivery, reviewing data quality rules, auditing integrations, or
  inspecting audience segment configurations.
connection_type: mparticle
preload: false
---

# Managing mParticle

Manage and monitor mParticle customer data platform — inputs, outputs, data plans, and event forwarding.

## Discovery Phase

```bash
#!/bin/bash

MPARTICLE_API="https://api.mparticle.com/v1"
AUTH_HEADER="Authorization: Basic $(echo -n "$MPARTICLE_API_KEY:$MPARTICLE_API_SECRET" | base64)"

echo "=== Workspace Info ==="
curl -s -H "$AUTH_HEADER" "$MPARTICLE_API/workspaces" \
  | jq -r '.[] | [.id, .name, .created_on] | @tsv' | column -t | head -5

echo ""
echo "=== Inputs (Sources) ==="
curl -s -H "$AUTH_HEADER" "$MPARTICLE_API/inputs" \
  | jq -r '.[] | [.id, .name, .platform, .status] | @tsv' | column -t | head -15

echo ""
echo "=== Outputs (Destinations) ==="
curl -s -H "$AUTH_HEADER" "$MPARTICLE_API/outputs" \
  | jq -r '.[] | [.id, .name, .output_type, .status] | @tsv' | column -t | head -15

echo ""
echo "=== Data Plans ==="
curl -s -H "$AUTH_HEADER" "$MPARTICLE_API/data-plans" \
  | jq -r '.[] | [.data_plan_id, .data_plan_name, .last_modified_on] | @tsv' | column -t | head -10
```

## Analysis Phase

```bash
#!/bin/bash

MPARTICLE_API="https://api.mparticle.com/v1"
AUTH_HEADER="Authorization: Basic $(echo -n "$MPARTICLE_API_KEY:$MPARTICLE_API_SECRET" | base64)"

echo "=== Event Forwarding Stats ==="
curl -s -H "$AUTH_HEADER" "$MPARTICLE_API/forwarding-stats?hours=24" \
  | jq -r '.[] | [.output_name, .successful, .failed, .filtered] | @tsv' | column -t | head -10

echo ""
echo "=== Data Plan Violations ==="
curl -s -H "$AUTH_HEADER" "$MPARTICLE_API/data-plans/$MPARTICLE_DATA_PLAN_ID/violations?hours=24" \
  | jq -r '.violations[:10][] | [.event_name, .violation_type, .count] | @tsv' | column -t

echo ""
echo "=== Audiences ==="
curl -s -H "$AUTH_HEADER" "$MPARTICLE_API/audiences" \
  | jq -r '.[] | [.id, .name, .size, .status, .last_calculated] | @tsv' | column -t | head -10

echo ""
echo "=== Integration Health ==="
curl -s -H "$AUTH_HEADER" "$MPARTICLE_API/outputs/health" \
  | jq -r '.[] | [.name, .status, .error_rate, .last_event_at] | @tsv' | column -t | head -10
```

## Output Format

```
INPUTS
ID       Name            Platform    Status
<id>     <input-name>    <platform>  active

OUTPUTS
ID       Name            Type        Status
<id>     <output-name>   <type>      active

FORWARDING STATS (24h)
Output           Successful  Failed  Filtered
<output-name>    <n>         <n>     <n>

DATA PLAN VIOLATIONS
Event Name       Violation Type    Count
<event>          <type>            <n>
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

