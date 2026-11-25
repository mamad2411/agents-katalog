---
name: aws-transit-gateway
description: |
  Use when working with Aws Transit Gateway — aWS Transit Gateway attachment
  analysis, route table management, peering configuration, and network topology
  review. Covers TGW inventory, attachment health, route propagation, VPN
  connection status, and bandwidth utilization.
connection_type: aws
preload: false
---

# AWS Transit Gateway Skill

Analyze AWS Transit Gateway networking with parallel execution and anti-hallucination guardrails.

**Relationship to other AWS skills:**

- `aws-transit-gateway/` → Transit Gateway-specific analysis (attachments, routes, peering)
- `aws/` → "How to execute" (parallel patterns, throttling, output format)

## CRITICAL: Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
#!/bin/bash
export AWS_PAGER=""

for tgw_id in $tgws; do
  get_tgw_attachments "$tgw_id" &
done
wait
```

## Helper Functions

```bash
#!/bin/bash
export AWS_PAGER=""

# List transit gateways
list_tgws() {
  aws ec2 describe-transit-gateways \
    --output text \
    --query 'TransitGateways[].[TransitGatewayId,State,OwnerId,Options.DefaultRouteTableAssociation,Options.DefaultRouteTablePropagation,Options.AmazonSideAsn]'
}

# List attachments for a TGW
list_attachments() {
  local tgw_id=$1
  aws ec2 describe-transit-gateway-attachments \
    --filters Name=transit-gateway-id,Values="$tgw_id" \
    --output text \
    --query 'TransitGatewayAttachments[].[TransitGatewayAttachmentId,ResourceType,ResourceId,State,Association.TransitGatewayRouteTableId]'
}

# List route tables for a TGW
list_route_tables() {
  local tgw_id=$1
  aws ec2 describe-transit-gateway-route-tables \
    --filters Name=transit-gateway-id,Values="$tgw_id" \
    --output text \
    --query 'TransitGatewayRouteTables[].[TransitGatewayRouteTableId,State,DefaultAssociationRouteTable,DefaultPropagationRouteTable]'
}

# Search routes in a route table
search_routes() {
  local rt_id=$1
  aws ec2 search-transit-gateway-routes \
    --transit-gateway-route-table-id "$rt_id" \
    --filters "Name=state,Values=active,blackhole" \
    --output text \
    --query 'Routes[].[DestinationCidrBlock,State,Type,TransitGatewayAttachments[0].TransitGatewayAttachmentId,TransitGatewayAttachments[0].ResourceType]'
}

# Get TGW bandwidth metrics
get_tgw_metrics() {
  local tgw_id=$1 days=${2:-7}
  local end_time start_time
  end_time=$(date -u +"%Y-%m-%dT%H:%M:%S")
  start_time=$(date -u -d "$days days ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-${days}d +"%Y-%m-%dT%H:%M:%S")
  aws cloudwatch get-metric-statistics \
    --namespace AWS/TransitGateway --metric-name BytesIn \
    --dimensions Name=TransitGateway,Value="$tgw_id" \
    --start-time "$start_time" --end-time "$end_time" \
    --period $((days * 86400)) --statistics Sum \
    --output text --query 'Datapoints[0].Sum'
}
```

## Common Operations

### 1. Transit Gateway Inventory

```bash
#!/bin/bash
export AWS_PAGER=""
aws ec2 describe-transit-gateways \
  --output text \
  --query 'TransitGateways[].[TransitGatewayId,State,OwnerId,Options.AmazonSideAsn,Options.DefaultRouteTableAssociation,Options.AutoAcceptSharedAttachments]'
```

### 2. Attachment Health Overview

```bash
#!/bin/bash
export AWS_PAGER=""
TGWS=$(aws ec2 describe-transit-gateways --output text --query 'TransitGateways[].TransitGatewayId')
for tgw in $TGWS; do
  aws ec2 describe-transit-gateway-attachments \
    --filters Name=transit-gateway-id,Values="$tgw" \
    --output text \
    --query "TransitGatewayAttachments[].[\"$tgw\",TransitGatewayAttachmentId,ResourceType,ResourceId,State]" &
done
wait
```

### 3. Route Table Analysis

```bash
#!/bin/bash
export AWS_PAGER=""
TGWS=$(aws ec2 describe-transit-gateways --output text --query 'TransitGateways[].TransitGatewayId')
for tgw in $TGWS; do
  {
    RTS=$(aws ec2 describe-transit-gateway-route-tables \
      --filters Name=transit-gateway-id,Values="$tgw" \
      --output text --query 'TransitGatewayRouteTables[].TransitGatewayRouteTableId')
    for rt in $RTS; do
      aws ec2 search-transit-gateway-routes \
        --transit-gateway-route-table-id "$rt" \
        --filters "Name=state,Values=active,blackhole" \
        --output text \
        --query "Routes[].[\"$rt\",DestinationCidrBlock,State,Type,TransitGatewayAttachments[0].ResourceType]" &
    done
  }
done
wait
```

### 4. VPN Attachment Status

```bash
#!/bin/bash
export AWS_PAGER=""
aws ec2 describe-transit-gateway-attachments \
  --filters Name=resource-type,Values=vpn \
  --output text \
  --query 'TransitGatewayAttachments[].[TransitGatewayAttachmentId,TransitGatewayId,ResourceId,State]'

VPN_IDS=$(aws ec2 describe-transit-gateway-attachments \
  --filters Name=resource-type,Values=vpn \
  --output text --query 'TransitGatewayAttachments[].ResourceId')
for vpn in $VPN_IDS; do
  aws ec2 describe-vpn-connections --vpn-connection-ids "$vpn" \
    --output text \
    --query 'VpnConnections[].[VpnConnectionId,State,VgwTelemetry[].[Status,StatusMessage]]' &
done
wait
```

### 5. Bandwidth Utilization

```bash
#!/bin/bash
export AWS_PAGER=""
END=$(date -u +"%Y-%m-%dT%H:%M:%S")
START=$(date -u -d "7 days ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-7d +"%Y-%m-%dT%H:%M:%S")
TGWS=$(aws ec2 describe-transit-gateways --output text --query 'TransitGateways[].TransitGatewayId')
for tgw in $TGWS; do
  {
    bytes_in=$(aws cloudwatch get-metric-statistics \
      --namespace AWS/TransitGateway --metric-name BytesIn \
      --dimensions Name=TransitGateway,Value="$tgw" \
      --start-time "$START" --end-time "$END" \
      --period 604800 --statistics Sum \
      --output text --query 'Datapoints[0].Sum')
    bytes_out=$(aws cloudwatch get-metric-statistics \
      --namespace AWS/TransitGateway --metric-name BytesOut \
      --dimensions Name=TransitGateway,Value="$tgw" \
      --start-time "$START" --end-time "$END" \
      --period 604800 --statistics Sum \
      --output text --query 'Datapoints[0].Sum')
    printf "%s\tBytesIn:%s\tBytesOut:%s\n" "$tgw" "${bytes_in:-0}" "${bytes_out:-0}"
  } &
done
wait
```

## Anti-Hallucination Rules

1. **Attachment types** - Valid resource types: vpc, vpn, direct-connect-gateway, peering, connect. Do not fabricate other types.
2. **Blackhole routes** - A blackhole route drops traffic silently. This can indicate a deleted attachment or misconfiguration. Always flag blackhole routes.
3. **search-transit-gateway-routes requires filter** - The `search-transit-gateway-routes` command requires at least one filter. Cannot list all routes without a filter.
4. **Cross-account attachments** - TGW can be shared via RAM. Attachments from other accounts show the remote account's resource ID but may not be describable from your account.
5. **Per-attachment metrics** - CloudWatch TGW metrics can be filtered by TransitGatewayAttachment dimension for per-attachment bandwidth analysis.

## Output Format

Present results as a structured report:
```
Aws Transit Gateway Report
══════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Data transfer charges**: TGW charges $0.02/GB for cross-AZ data transfer. This is in addition to the hourly attachment charge ($0.05/hour).
- **Route limits**: Default 10,000 routes per TGW route table. Static routes have priority over propagated routes.
- **Peering limitations**: TGW peering does not support route propagation. Routes must be added statically.
- **CloudWatch statistics syntax**: Use spaces not commas: `--statistics Average Maximum`.
- **Multi-region**: TGW is regional. Cross-region connectivity requires TGW peering.
