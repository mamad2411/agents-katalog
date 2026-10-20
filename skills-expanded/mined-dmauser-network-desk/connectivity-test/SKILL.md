# Skill: Connectivity Testing (ntsh_connectivity-test)

Systematic connectivity testing using cloud-native diagnostic tools and traditional network utilities. This skill covers Azure Network Watcher, AWS VPC Reachability Analyzer, GCP Connectivity Tests, and standard TCP/ICMP/UDP testing methodology.

---

## Azure Network Watcher — Connection Troubleshoot

Connection Troubleshoot tests actual TCP or ICMP connectivity from a source VM to a destination, identifying the hop where connectivity fails.

### Usage
```bash
# TCP connectivity test — VM to endpoint
az network watcher test-connectivity \
  --source-resource MySourceVM \
  --resource-group MyRG \
  --dest-address 10.0.2.5 \
  --dest-port 443 \
  --protocol TCP

# TCP test to external endpoint
az network watcher test-connectivity \
  --source-resource MySourceVM \
  --resource-group MyRG \
  --dest-address api.example.com \
  --dest-port 443 \
  --protocol TCP

# ICMP test (ping)
az network watcher test-connectivity \
  --source-resource MySourceVM \
  --resource-group MyRG \
  --dest-address 10.0.2.5 \
  --protocol ICMP
```

### Interpreting Results
The output includes `connectionStatus` (Reachable, Unreachable, Unknown) and a `hops` array showing each hop in the path:

- **Source NIC**: If blocked here → outbound NSG rule or VM firewall.
- **Route Table**: If "NextHopType: None" → no route to destination (black hole).
- **Virtual Appliance / Firewall**: If blocked here → NVA/firewall policy.
- **Peering / Gateway**: If blocked here → peering not configured, or gateway down.
- **Destination NIC**: If blocked here → inbound NSG rule at destination.
- **Destination VM**: If blocked here → OS firewall or application not listening.

---

## AWS VPC Reachability Analyzer

Configuration-based analysis — does not send actual traffic. Evaluates whether traffic could flow based on current networking configuration.

```bash
# Create path analysis: EC2 to EC2
INSIGHT_PATH=$(aws ec2 create-network-insights-path \
  --source i-src123 \
  --destination i-dst456 \
  --protocol TCP \
  --destination-port 443 \
  --query 'NetworkInsightsPath.NetworkInsightsPathId' \
  --output text)

# Run analysis
ANALYSIS_ID=$(aws ec2 start-network-insights-analysis \
  --network-insights-path-id $INSIGHT_PATH \
  --query 'NetworkInsightsAnalysis.NetworkInsightsAnalysisId' \
  --output text)

# Wait and get results
aws ec2 wait network-insights-analysis-complete \
  --network-insights-analysis-ids $ANALYSIS_ID

aws ec2 describe-network-insights-analyses \
  --network-insights-analysis-ids $ANALYSIS_ID \
  --query 'NetworkInsightsAnalyses[0].{
    Reachable: NetworkPathFound,
    Explanations: Explanations[].{
      Component: Component.Id,
      Direction: Direction,
      Issue: ExplanationCode
    }
  }'
```

### Common Explanations
- `SECURITY_GROUP_NOT_FOUND`: SG referenced in rule no longer exists.
- `ROUTE_NOT_FOUND`: No route to destination in the route table.
- `NETWORK_ACL_DENY`: NACL explicitly denying the traffic.
- `SECURITY_GROUP_DENY`: No matching allow rule in the SG.

---

## GCP Connectivity Tests

```bash
# VM-to-VM test
gcloud network-management connectivity-tests create vm-to-vm-test \
  --source-instance=projects/my-proj/zones/us-central1-a/instances/src-vm \
  --destination-instance=projects/my-proj/zones/us-central1-a/instances/dst-vm \
  --protocol=TCP \
  --destination-port=8080

# VM-to-internet test
gcloud network-management connectivity-tests create outbound-test \
  --source-instance=projects/my-proj/zones/us-central1-a/instances/my-vm \
  --destination-ip-address=8.8.8.8 \
  --protocol=TCP \
  --destination-port=443

# Internet-to-VM test (via external LB)
gcloud network-management connectivity-tests create inbound-test \
  --source-ip-address=203.0.113.1 \
  --destination-instance=projects/my-proj/zones/us-central1-a/instances/web-vm \
  --protocol=TCP \
  --destination-port=443

# Describe results
gcloud network-management connectivity-tests describe vm-to-vm-test \
  --format="json(reachabilityDetails)"
```

### Result Verdicts
- **REACHABLE**: Traffic would be delivered successfully.
- **UNREACHABLE**: Traffic would be dropped. Check `traces[].steps[]` for the DROP step.
- **AMBIGUOUS**: Partial reachability (e.g., some paths work, others don't due to ECMP).
- **UNDETERMINED**: Insufficient permissions to evaluate all components.

---

## Standard Network Testing Tools

### Systematic TCP Testing
```bash
# ncat — verbose TCP connection test with timeout
ncat -vzw 5 target.example.com 443
# Output: "Ncat: Connected to 10.0.2.5:443."  (success)
# Output: "Ncat: Connection timed out."  (firewall drop / no route)
# Output: "Ncat: Connection refused."  (RST received — port closed or firewalled with reject)

# Test-NetConnection (PowerShell)
Test-NetConnection -ComputerName target.example.com -Port 443 -InformationLevel Detailed
# Key fields: TcpTestSucceeded, RemoteAddress, InterfaceAlias, SourceAddress, PingSucceeded

# nmap — targeted port scan (not a full scan — specific ports only)
nmap -sT -p 22,80,443,3389,5432 target.example.com -Pn
# -sT: TCP connect scan (no root needed)
# -Pn: skip ICMP ping (may be blocked)
# Look for: open, closed, filtered states
```

### ICMP Testing
```bash
# Standard ping — basic reachability
ping -c 4 target.example.com        # Linux
ping -n 4 target.example.com        # Windows

# Ping with specific packet size (MTU testing)
ping -M do -s 1472 target.example.com  # Linux — don't fragment, 1472+28=1500
ping -f -l 1472 target.example.com     # Windows
```

**Important**: ICMP may be blocked by NSGs/SGs even when TCP connectivity works. Never conclude "unreachable" based solely on failed ping. Always test with TCP on the actual application port.

### UDP Testing
```bash
# ncat — UDP connectivity test
ncat -vzu target.example.com 53

# DNS resolution test (UDP 53)
nslookup target.example.com
dig target.example.com @10.0.0.53

# Note: UDP has no connection handshake — "open" results from nmap/ncat
# may be false positives (no RST to indicate closed). Verify with
# application-level response (e.g., DNS query, SNMP, etc.)
```

### Systematic Test Order
1. **TCP on application port** (most definitive) — timeout = drop, RST = reject/closed, success = reachable.
2. **ICMP ping** (supplementary) — confirms IP-level reachability if allowed.
3. **Traceroute/mtr** (path analysis) — identifies which hop drops or delays traffic.
4. **DNS resolution** — verify FQDN resolves to the expected IP.
5. **Cloud-native tools** — use IP flow verify, Reachability Analyzer, or Connectivity Tests to pinpoint the blocking component.

**Analysis only — verify against vendor documentation before applying.**
