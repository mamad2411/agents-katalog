---
name: managing-aws-gamelift
description: |
  Use when working with Aws Gamelift — aWS GameLift fleet management including
  game server deployments, fleet scaling, matchmaking configuration, game
  session monitoring, and player session tracking. Covers fleet health, capacity
  utilization, matchmaking metrics, and cost analysis.
connection_type: aws-gamelift
preload: false
---

# AWS GameLift Management Skill

Monitor and manage AWS GameLift fleets, matchmaking, and game sessions.

## MANDATORY: Discovery-First Pattern

**Always discover fleets and aliases before inspecting sessions or scaling.**

### Phase 1: Discovery

```bash
#!/bin/bash
REGION="${AWS_REGION:-us-east-1}"

echo "=== GameLift Fleets ==="
aws gamelift describe-fleet-attributes --region "$REGION" \
  --query 'FleetAttributes[].{Name:Name,ID:FleetId,Status:Status,Type:ComputeType,OS:OperatingSystem}' \
  --output table

echo ""
echo "=== Fleet Capacity ==="
aws gamelift describe-fleet-capacity --region "$REGION" \
  --query 'FleetCapacity[].{Fleet:FleetId,Desired:InstanceCounts.DESIRED,Active:InstanceCounts.ACTIVE,Idle:InstanceCounts.IDLE,Pending:InstanceCounts.PENDING}' \
  --output table

echo ""
echo "=== Aliases ==="
aws gamelift list-aliases --region "$REGION" \
  --query 'Aliases[].{Name:Name,ID:AliasId,Strategy:RoutingStrategy.Type,Fleet:RoutingStrategy.FleetId}' \
  --output table

echo ""
echo "=== Matchmaking Configurations ==="
aws gamelift describe-matchmaking-configurations --region "$REGION" \
  --query 'Configurations[].{Name:Name,Status:ConfigurationStatus,Timeout:RequestTimeoutSeconds,Backfill:BackfillMode}' \
  --output table
```

**Phase 1 outputs:** Fleet list with status, capacity, aliases, matchmaking configs

### Phase 2: Analysis

```bash
#!/bin/bash
FLEET_ID="${1:-$GAMELIFT_FLEET_ID}"

echo "=== Fleet Utilization ==="
aws gamelift describe-fleet-utilization --fleet-ids "$FLEET_ID" --region "$REGION" \
  --query 'FleetUtilization[].{Fleet:FleetId,ActiveSessions:ActiveGameSessionCount,ActivePlayers:CurrentPlayerSessionCount,MaxSessions:MaximumPlayerSessionCount}' \
  --output table

echo ""
echo "=== Active Game Sessions ==="
aws gamelift describe-game-sessions --fleet-id "$FLEET_ID" --region "$REGION" \
  --status-filter ACTIVE \
  --query 'GameSessions[].{ID:GameSessionId,Status:Status,Players:CurrentPlayerSessionCount,Max:MaximumPlayerSessionCount,Created:CreationTime}' \
  --output table | head -20

echo ""
echo "=== Scaling Policies ==="
aws gamelift describe-scaling-policies --fleet-id "$FLEET_ID" --region "$REGION" \
  --query 'ScalingPolicies[].{Name:Name,Type:PolicyType,Metric:MetricName,Threshold:Threshold,Status:Status}' \
  --output table

echo ""
echo "=== Fleet Events (last 24h) ==="
aws gamelift describe-fleet-events --fleet-id "$FLEET_ID" --region "$REGION" \
  --start-time "$(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-24H +%Y-%m-%dT%H:%M:%SZ)" \
  --query 'Events[].{Time:EventTime,Code:EventCode,Message:Message}' \
  --output table | head -20
```

## Output Format

```
AWS GAMELIFT STATUS
===================
Region: {region}
Fleets: {count} (Active: {active}, Error: {error})
Total Capacity: {instances} instances
Active Sessions: {count} | Players: {count}
Utilization: {percent}%
Matchmaking Configs: {count}
Scaling Policies: {count} active
Issues: {list_of_warnings}
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

- **Fleet ID vs Alias**: Always resolve aliases to fleet IDs before querying sessions
- **Multi-region**: GameLift fleets are regional — check all active regions
- **Spot vs On-Demand**: Spot fleets can lose instances — monitor FLEET_ACTIVATION_FAILED events
- **Session limits**: Default 1 game session per instance — check runtime configuration
