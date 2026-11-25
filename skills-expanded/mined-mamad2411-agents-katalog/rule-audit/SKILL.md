# Skill: Firewall Rule Audit

## Purpose

Perform comprehensive firewall rule-base audits across all 14 supported platforms. Identify security risks, operational inefficiencies, and compliance gaps in existing rule sets. Produce a risk-rated findings table with actionable remediation recommendations.

---

## Audit Categories

Every rule audit checks for the following categories:

| Category | Description | Risk Level |
|----------|-------------|------------|
| **Any/Any Allow** | Rules permitting all sources to all destinations on all services | Critical |
| **Overly Broad Source/Dest** | Rules using excessively wide CIDR ranges (e.g., /8, /16) or "any" on one axis | High |
| **Shadow Rules** | Rules that can never match because a broader rule above already handles the traffic | High |
| **Unused Rules** | Rules with zero hit count over a significant observation period (30+ days) | Medium |
| **Redundant Rules** | Multiple rules that achieve the same effect — consolidation candidates | Medium |
| **Expired Time-Based Rules** | Rules with schedule objects whose valid dates have passed | Medium |
| **Missing Logging** | Allow rules without logging enabled (compliance gap) | Medium |
| **Disabled Rules** | Rules in disabled state — review for removal or re-enablement | Info |
| **Documentation Gaps** | Rules without descriptions or comments | Info |

---

## Per-Vendor Rule Export and Hit Count Retrieval

### Azure Firewall

```bash
# Export rule collections via CLI
az network firewall policy rule-collection-group list \
  --policy-name <policy> --resource-group <rg> -o json

# Hit counts via Azure Monitor / Log Analytics (KQL)
AzureDiagnostics
| where Category == "AzureFirewallNetworkRule" or Category == "AzureFirewallApplicationRule"
| summarize HitCount=count() by RuleName=msg_s
| order by HitCount asc

# Structured logs (resource-specific tables — preferred)
AZFWNetworkRule
| summarize HitCount=count() by Rule
| order by HitCount asc
```

### AWS Network Firewall

```bash
# List rule groups
aws network-firewall list-rule-groups --type STATEFUL
aws network-firewall describe-rule-group --rule-group-arn <arn>

# Hit counts via CloudWatch Metrics
# Metric: DroppedPackets, PassedPackets per rule group
aws cloudwatch get-metric-statistics \
  --namespace AWS/NetworkFirewall \
  --metric-name PassedPackets \
  --dimensions Name=FirewallName,Value=<name> \
  --start-time <30-days-ago> --end-time <now> \
  --period 2592000 --statistics Sum
```

### GCP Cloud Firewall

```bash
# List firewall rules
gcloud compute firewall-rules list --format=json

# Firewall rule hit counts via Firewall Insights
# Enable Firewall Rules Logging first:
gcloud compute firewall-rules update <rule-name> --enable-logging

# Query logs in Cloud Logging
gcloud logging read 'resource.type="gce_subnetwork" AND jsonPayload.rule_details.reference:*' \
  --format=json --limit=1000
```

### Palo Alto Networks (PAN-OS)

```bash
# Show running security policy
> show running security-policy

# Rule hit counts
> show rule-use rule-base security type used
> show rule-use rule-base security type unused

# Detailed rule usage
> show running rule-use rule-base security json

# Export via API
curl -k "https://<firewall>/api/?type=config&action=show&xpath=/config/devices/entry/vsys/entry/rulebase/security" \
  -H "X-PAN-KEY: <api-key>"
```

### Fortinet FortiGate (FortiOS)

```bash
# List firewall policies
# config firewall policy
FGT# show firewall policy

# Hit counts
FGT# diagnose firewall iprope list

# Per-policy hit counts (FortiOS 7.x)
FGT# get firewall policy <policy-id> | grep -i "bytes\|packets\|hit"

# Export via REST API
curl -k "https://<fortigate>/api/v2/cmdb/firewall/policy" \
  -H "Authorization: Bearer <token>"
```

### Check Point (R81+)

```bash
# Export rulebase via mgmt_cli
mgmt_cli show access-rulebase name "Network" details-level full -f json

# Hit counts
mgmt_cli show access-rulebase name "Network" use-object-dictionary true \
  hits-settings.from-date "2024-01-01" -f json

# SmartConsole: Policy > Access Control > hit count column (enable if hidden)
# cpstat fw -f policy for real-time policy stats
```

### Cisco ASA / Firepower (FTD)

```bash
# ASA: Show access-lists with hit counts
ASA# show access-list
# Output includes hitcnt=<N> per ACE

# Clear hit counts to start fresh observation
ASA# clear access-list <name> counters

# FTD via FMC REST API
GET /api/fmc_config/v1/domain/{domainUUID}/policy/accesspolicies/{policyId}/accessrules

# Packet tracer to simulate flow
ASA# packet-tracer input <iface> tcp <src> <sport> <dst> <dport>
```

### Juniper SRX

```bash
# Show security policies with hit counts
> show security policies hit-count

# Detailed policy listing
> show security policies detail

# Export config
> show configuration security policies | display json

# Unused policies (zero hit count)
> show security policies hit-count | match " 0$"
```

### Zscaler (ZIA)

```bash
# ZIA API: List firewall filtering rules
GET /api/v1/webApplicationRules

# ZIA API: List firewall rules
GET /api/v1/firewallRules

# Hit counts available in ZIA Admin Portal > Analytics > Firewall Insights
# NSS feed to SIEM for detailed per-rule analysis
```

### Sophos XG / XGS

```bash
# CLI: Show firewall rules
console> show firewall-rule all

# REST API: List firewall rules
GET /webconsole/APIController?reqxml=
<Request>
  <Login><Username>admin</Username><Password>pass</Password></Login>
  <Get><FirewallRule></FirewallRule></Get>
</Request>

# Log Viewer in web GUI for hit counts per rule
```

### OPNsense

```bash
# REST API: List filter rules
curl -u "<key>:<secret>" \
  "https://<opnsense>/api/firewall/filter/searchRule"

# Show loaded ruleset via pfctl
pfctl -sr          # show rules
pfctl -vsr         # verbose with hit counts (evaluations, packets, bytes)
pfctl -ss          # show state table

# Export config.xml for offline analysis
curl -u "<key>:<secret>" \
  "https://<opnsense>/api/core/backup/download/this"
```

### pfSense

```bash
# Show loaded rules with hit counts
pfctl -vsr

# Show state table
pfctl -ss

# Export config via GUI: Diagnostics > Backup & Restore
# Or via xmlrpc / config.xml directly

# Per-rule counters visible in GUI: Firewall > Rules > hit count column
# easyrule utility for quick rule inspection context
```

### VyOS

```bash
# Show firewall rulesets
$ show firewall

# Show firewall statistics (hit counts)
$ show firewall name <ruleset-name> statistics

# Show specific rule details
$ show firewall name <ruleset-name> rule <n>

# Export configuration
$ show configuration commands | grep firewall
```

### iptables / nftables

```bash
# iptables: List all rules with hit counts
iptables -L -v -n --line-numbers
iptables -L FORWARD -v -n --line-numbers

# NAT rules
iptables -t nat -L -v -n --line-numbers

# Zero counters to start observation
iptables -Z

# nftables: List all rules with counters
nft list ruleset
nft list chain inet filter forward

# Export for offline analysis
iptables-save > fw-export.txt
nft list ruleset > nft-export.txt
```

---

## Output Format

Present findings in the following table format:

| Rule # | Name/ID | Source | Destination | Service | Action | Hit Count | Risk | Finding | Recommendation |
|--------|---------|-------|-------------|---------|--------|-----------|------|---------|----------------|
| 5 | Legacy-Any-Allow | any | any | any | Allow | 45,231 | **Critical** | Unrestricted allow rule | Decompose into specific rules by traffic analysis, then disable |
| 12 | Old-Vendor-Access | 10.0.0.0/8 | 192.168.1.0/24 | TCP/22,443 | Allow | 0 | **Medium** | Unused for 90 days | Disable with monitoring; remove after 30-day hold |
| 23 | Web-DMZ-Alt | 10.1.0.0/16 | DMZ_Servers | TCP/443 | Allow | 1,203 | **High** | Shadowed by rule 20 | Merge into rule 20 or re-order |
| 47 | Temp-Migration | 10.5.0.0/16 | DB_Servers | TCP/1433 | Allow | 312 | **Medium** | Schedule expired 2024-01-15 | Remove — expired temporary rule |

---

## Risk Summary Template

```
=== FIREWALL RULE AUDIT SUMMARY ===
Platform:       [vendor / version]
Rule Count:     [total]
Audit Period:   [start] to [end]

Critical:  [N] findings  — Immediate action required
High:      [N] findings  — Address within 7 days
Medium:    [N] findings  — Address within 30 days
Info:      [N] findings  — Best-practice improvements

Top Recommendations:
1. [Most critical finding and action]
2. [Second most critical]
3. [Third]
```

---

## Procedure

1. **Export** the current rule set and hit counts using the vendor-specific commands above.
2. **Normalize** rules into the common table format (Rule #, Source, Dest, Service, Action, Hit Count).
3. **Analyze** each rule against the audit categories.
4. **Score** each finding using the risk levels defined above.
5. **Recommend** specific remediations — be precise (e.g., "merge rule 23 into rule 20" not "clean up rules").
6. **Report** using the output format and risk summary template.

---
**Analysis only — verify against vendor documentation before applying.**
