# Workbench Alerts

Investigate and analyze security alerts from Trend Micro Vision One Workbench. This skill provides read-only access to alert data for SOC analysts and incident responders.

## Instructions

1. When the user asks about security alerts, incidents, or wants to investigate suspicious activity, use this skill to query the Workbench.

2. **Start with alert listing**: Use `list_workbench_alerts` to get an overview of alerts matching the user's criteria (severity, time range, status).

3. **Get alert details**: When investigating a specific alert, use `get_workbench_alert` with the alert ID to retrieve full context including affected entities, indicators, and timeline.

4. **Search for patterns**: Use `get_workbench_alerts_list` when you need to search across multiple alerts or correlate activity.

5. **Prioritize by severity**: When presenting alerts, organize by severity (critical > high > medium > low) and highlight actionable items.

6. **Correlate entities**: Look for common entities (IPs, domains, users, endpoints) across alerts to identify attack patterns.

7. **Provide context**: For each alert, explain the detection rule, potential impact, and recommended response actions.

## Tools

This skill uses the following Vision One MCP tools (all read-only):

### Alert Management
| Tool | Purpose |
|------|---------|
| `workbench_alerts_list` | List alerts with filtering by severity, status, time range |
| `workbench_alert_detail_get` | Get detailed information for a specific alert by ID |

### Attack Techniques
| Tool | Purpose |
|------|---------|
| `workbench_observed_attack_techniques_list` | List observed MITRE ATT&CK techniques detected in your environment |

## Common Workflows

### Daily Alert Review
1. List alerts from the last 24 hours filtered by critical/high severity
2. For each alert, get details and summarize the threat
3. Group alerts by attack pattern or affected system

### Incident Investigation
1. Get the specific alert details
2. Search for related alerts involving the same entities
3. Build a timeline of the attack progression

### Alert Triage
1. List unresolved alerts by severity
2. Categorize by alert type (malware, phishing, lateral movement, etc.)
3. Prioritize based on affected asset criticality

### MITRE ATT&CK Analysis
1. List observed attack techniques for a time period
2. Filter by risk level or specific technique IDs
3. Correlate techniques with active alerts
4. Identify attack patterns and kill chain progression
5. Map detections to MITRE ATT&CK framework for reporting

## Output Format

When presenting alerts, use this format:

```
## Alert Summary

**Alert ID**: [ID]
**Severity**: [Critical/High/Medium/Low]
**Status**: [New/In Progress/Resolved]
**Detected**: [Timestamp]

### Description
[Brief description of the alert]

### Affected Entities
- Endpoints: [list]
- Users: [list]
- IPs: [list]

### Indicators of Compromise
- [IOC type]: [value]

### Recommended Actions
1. [Action item]
2. [Action item]
```

## Security Considerations

- This skill provides read-only access to alert data
- Alert data may contain sensitive information about your environment
- Use alert IDs when referencing specific alerts in reports
- Do not share raw alert data outside authorized channels
