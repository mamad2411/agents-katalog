---
name: managing-google-cloud-dns
description: |
  Use when working with Google Cloud Dns — google Cloud DNS management covering
  managed zones, record sets, DNSSEC configuration, DNS policies, and peering.
  Use when managing GCP Cloud DNS zones, configuring DNS records, enabling
  DNSSEC, setting up DNS forwarding or peering, or troubleshooting DNS
  resolution within Google Cloud.
connection_type: gcp
preload: false
---

# Google Cloud DNS Skill

Manage Google Cloud DNS zones, record sets, DNSSEC, policies, and DNS peering.

## Core Helper Functions

```bash
#!/bin/bash

# List managed zones
gcp_dns_zones() {
    gcloud dns managed-zones list --format=json 2>/dev/null
}

# List record sets
gcp_dns_records() {
    local zone="$1"
    gcloud dns record-sets list --zone="$zone" --format=json 2>/dev/null
}
```

## MANDATORY: Discovery-First Pattern

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Managed Zones ==="
gcloud dns managed-zones list \
    --format="table(name,dnsName,visibility,dnssecConfig.state)" 2>/dev/null | head -20

echo ""
echo "=== DNS Policies ==="
gcloud dns policies list \
    --format="table(name,enableInboundForwarding,enableLogging,networks.len())" 2>/dev/null | head -10

echo ""
echo "=== Record Set Summary ==="
for ZONE in $(gcloud dns managed-zones list --format="value(name)" 2>/dev/null); do
    COUNT=$(gcloud dns record-sets list --zone="$ZONE" --format="value(type)" 2>/dev/null | sort | uniq -c | sort -rn | head -5 | tr '\n' '  ')
    echo "$ZONE: $COUNT"
done | head -15

echo ""
echo "=== DNSSEC Status ==="
gcloud dns managed-zones list --format=json 2>/dev/null | jq -r '
    .[] | "\(.name)\t\(.dnssecConfig.state // "off")\t\(.dnsName)"
' | column -t | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash
ZONE="${1:?Zone name required}"

echo "=== Zone Configuration ==="
gcloud dns managed-zones describe "$ZONE" --format=json 2>/dev/null | jq '{
    name, dnsName, visibility,
    dnssec: .dnssecConfig.state,
    nameServers, description,
    peeringConfig: .peeringConfig,
    forwardingConfig: .forwardingConfig
}'

echo ""
echo "=== Record Sets ==="
gcloud dns record-sets list --zone="$ZONE" \
    --format="table(name,type,ttl,rrdatas.list())" 2>/dev/null | head -30

echo ""
echo "=== DNSSEC Key Info ==="
gcloud dns dns-keys list --zone="$ZONE" \
    --format="table(id,keyTag,type,algorithm,isActive)" 2>/dev/null | head -10

echo ""
echo "=== Pending Changes ==="
gcloud dns record-sets changes list --zone="$ZONE" --sort-order=descending --limit=5 \
    --format="table(id,startTime,status)" 2>/dev/null
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `gcloud` CLI with `--format=json` and jq for structured data
- Use `--format=table(...)` for quick summaries

## Safety Rules
- **Read-only by default**: Use list/describe for inspection
- **Never delete record sets** without explicit confirmation -- causes outages
- **DNSSEC disabling** can break resolution if DS records exist at registrar
- **Policy changes** affect all networks attached to the policy

## Output Format

Present results as a structured report:
```
Managing Google Cloud Dns Report
════════════════════════════════
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
- **Zone names vs DNS names**: Zone name is a resource identifier, DNS name is the domain
- **Private vs public zones**: Private zones only resolve within specified VPC networks
- **DNSSEC key rotation**: Managed automatically by Cloud DNS but DS records at registrar need updating
- **Forwarding zones**: Forward queries to on-prem DNS; requires VPN/Interconnect connectivity
- **Response policy**: Can override DNS responses for specific names -- useful for split-horizon
