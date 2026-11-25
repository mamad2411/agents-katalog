# Endpoint Security

Monitor and analyze endpoint protection status, agent deployment, and endpoint inventory using Trend Micro Vision One. This skill provides visibility into workstations, servers, and their security posture.

## Instructions

1. When the user asks about endpoints, workstations, servers, or agent status, use this skill to query endpoint data.

2. **List endpoints**: Start with `list_endpoints` to get an overview of all managed endpoints.

3. **Check agent status**: Use `list_endpoint_agents` to review agent deployment and health across the environment.

4. **Get endpoint details**: Use `get_endpoint` to retrieve comprehensive information about a specific endpoint.

5. **Filter by criteria**: Use filtering capabilities to focus on specific OS types, agent versions, or protection status.

6. **Identify gaps**: Look for endpoints with outdated agents, disabled protection, or missing security components.

7. **Correlate with alerts**: Cross-reference endpoint data with Workbench alerts for affected systems.

## Tools

This skill uses the following Vision One MCP tools (all read-only):

### Endpoint Inventory
| Tool | Purpose |
|------|---------|
| `endpoint_security_endpoints_list` | List all managed endpoints with status and filtering |
| `endpoint_security_endpoint_get` | Get detailed endpoint information by ID |

### Agent Management
| Tool | Purpose |
|------|---------|
| `endpoint_security_agent_update_policies_list` | List available agent update policies |
| `endpoint_security_version_control_policies_list` | List endpoint version control policies |

### Tasks
| Tool | Purpose |
|------|---------|
| `endpoint_security_tasks_list` | List endpoint security tasks (export, delete operations) |
| `endpoint_security_task_get` | Get status of a specific endpoint task |

## Common Workflows

### Endpoint Inventory Review
1. List all endpoints
2. Group by OS type (Windows, macOS, Linux)
3. Check protection status for each group
4. Identify unprotected or partially protected endpoints
5. Summarize coverage metrics

### Agent Health Assessment
1. List endpoint agents
2. Check agent versions against current release
3. Identify outdated agents requiring updates
4. Check agent connectivity status
5. Generate update priority list

### Protection Gap Analysis
1. List endpoints with protection status
2. Filter for disabled or degraded protection
3. Identify endpoints missing security components
4. Cross-reference with critical asset lists
5. Prioritize remediation by risk

### Incident Response Support
1. Get details for affected endpoint(s)
2. Check current protection status
3. Review agent version and capabilities
4. Identify available response actions
5. Document endpoint context for investigation

### Compliance Reporting
1. List all endpoints
2. Calculate protection coverage percentage
3. Identify non-compliant endpoints
4. Check agent version compliance
5. Generate compliance summary

### Agent Update Policy Review
1. List all agent update policies
2. Review update schedules and targets
3. List version control policies
4. Identify endpoints with paused updates
5. Recommend policy adjustments

### Task Monitoring
1. List endpoint security tasks
2. Filter by status (running/succeeded/failed)
3. Get details on specific tasks
4. Monitor export or deletion operations
5. Troubleshoot failed tasks

## Output Format

### Endpoint Inventory
```
## Endpoint Summary

**Total Endpoints**: [count]
- Protected: [count] ([%])
- Partially Protected: [count] ([%])
- Unprotected: [count] ([%])

### By Operating System
| OS | Count | Protected | Issues |
|----|-------|-----------|--------|
| Windows 11 | [count] | [count] | [count] |
| Windows 10 | [count] | [count] | [count] |
| Windows Server | [count] | [count] | [count] |
| macOS | [count] | [count] | [count] |
| Linux | [count] | [count] | [count] |

### By Protection Status
- Full protection: [count]
- Missing component(s): [count]
- Agent offline: [count]
- Protection disabled: [count]
```

### Endpoint Details
```
## Endpoint: [Hostname]

**IP Address**: [IP]
**MAC Address**: [MAC]
**Operating System**: [OS Name] [Version]
**Last Seen**: [Timestamp]

### Agent Information
- Agent Version: [Version]
- Agent Status: [Online/Offline]
- Last Check-in: [Timestamp]

### Protection Status
- Real-time scan: [Enabled/Disabled]
- Behavior monitoring: [Enabled/Disabled]
- Web reputation: [Enabled/Disabled]
- Firewall: [Enabled/Disabled]

### Security Posture
- Open vulnerabilities: [count]
- Recent detections: [count]
- Risk score: [score]
```

### Agent Status Report
```
## Agent Deployment Status

**Current Version**: [Version]
**Total Agents**: [count]

### Version Distribution
| Version | Count | Status |
|---------|-------|--------|
| [Version] | [count] | Current |
| [Version] | [count] | Outdated |
| [Version] | [count] | Critical Update Needed |

### Connectivity
- Online: [count]
- Offline (< 24h): [count]
- Offline (> 24h): [count]
- Offline (> 7d): [count]

### Update Priority
1. [count] endpoints require critical updates
2. [count] endpoints have outdated agents
3. [count] endpoints need attention (offline)
```

## Security Considerations

- This skill provides read-only access to endpoint inventory data
- Endpoint names, IPs, and configurations are sensitive infrastructure information
- Unprotected endpoints represent significant security risk
- Offline agents may indicate compromised or isolated systems
- Agent version gaps should be addressed to maintain protection efficacy
- Coordinate with IT operations for agent deployments and updates
- Use endpoint data to prioritize patching and incident response
