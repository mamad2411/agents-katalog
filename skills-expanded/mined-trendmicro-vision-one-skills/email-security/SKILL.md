# Email Security

Monitor email security infrastructure and protection status using Trend Micro Vision One. This skill provides visibility into email gateways, servers, and security configurations.

## Instructions

1. When the user asks about email security, mail servers, or email protection status, use this skill to query email infrastructure.

2. **List email servers**: Start with `list_email_servers` to get an overview of all monitored email infrastructure.

3. **Check gateway status**: Use `list_email_gateways` to review email gateway configurations and health.

4. **Get activity data**: Use `get_email_activity_data` to retrieve email security events and metrics.

5. **Correlate with alerts**: Cross-reference email security data with Workbench alerts for phishing or email-based threats.

6. **Monitor trends**: Look for patterns in email threats to identify targeted campaigns.

## Tools

This skill uses the following Vision One MCP tools (all read-only):

| Tool | Purpose |
|------|---------|
| `email_security_accounts_list` | List email accounts managed by email protection with sensor and policy status |
| `email_security_domains_list` | List email domains managed by email protection |
| `email_security_servers_list` | List email servers managed by on-premises email protection |

## Common Workflows

### Email Account Review
1. List email accounts with protection status
2. Filter by sensor detection status or mail service type
3. Identify accounts without full protection
4. Check Cloud Email and Collaboration Protection policy status
5. Recommend enabling protection for unprotected accounts

### Email Domain Inventory
1. List all email domains managed by protection solutions
2. Verify domain ownership and configuration
3. Check protection coverage per domain
4. Identify domains requiring attention
5. Document domain security posture

### Email Server Management
1. List on-premises email servers
2. Check server connectivity and health
3. Verify protection agent status
4. Identify servers requiring updates
5. Document server inventory for compliance

## Output Format

### Email Accounts Summary
```
## Email Account Protection Overview

**Total Accounts**: [count]

### By Mail Service
| Service | Count | Protected | Sensor Enabled |
|---------|-------|-----------|----------------|
| Exchange Online | [count] | [count] | [count] |
| Gmail | [count] | [count] | [count] |

### Protection Status
| Status | Count |
|--------|-------|
| Fully enabled | [count] |
| Partially enabled | [count] |
| Disabled | [count] |

### Accounts Requiring Attention
[List of accounts with protection gaps]
```

### Email Domains Summary
```
## Email Domain Inventory

**Total Domains**: [count]

### Managed Domains
| Domain | Protection Status | Mail Service |
|--------|-------------------|--------------|
| [domain.com] | [Protected/Unprotected] | [Exchange/Gmail] |
```

### Email Servers Summary
```
## On-Premises Email Servers

**Total Servers**: [count]

### Servers
| Server | Status | Last Seen | Protection |
|--------|--------|-----------|------------|
| [Name] | [Connected/Disconnected] | [Timestamp] | [Enabled/Disabled] |
```

## Security Considerations

- This skill provides read-only access to email security data
- Email server names and configurations are sensitive infrastructure details
- Use this data to verify protection status, not for external reporting
- High phishing volumes may indicate targeted campaigns requiring additional response
- Coordinate with email administrators for configuration changes
