# Cloud Accounts

Query and analyze multi-cloud account inventory across AWS, Azure, and GCP using Trend Micro Vision One. This skill provides visibility into connected cloud accounts, their security status, and configuration.

## Instructions

1. When the user asks about cloud accounts, multi-cloud inventory, or cloud connectivity status, use this skill to query account information.

2. **List all accounts**: Start with `list_cloud_accounts` to get an overview of all connected cloud accounts across providers.

3. **Filter by provider**: Use the cloud provider filter when focusing on a specific platform (AWS, Azure, GCP).

4. **Check account details**: Use `get_cloud_account` to retrieve detailed configuration and status for a specific account.

5. **Verify connectivity**: Check account connection status to identify any disconnected or misconfigured accounts.

6. **Review account features**: Understand which Vision One features are enabled for each cloud account.

7. **Group by organization**: When presenting multi-account environments, group accounts logically by organization or business unit.

## Tools

This skill uses the following Vision One MCP tools (all read-only):

### AWS Accounts
| Tool | Purpose |
|------|---------|
| `cam_aws_accounts_list` | List all AWS accounts connected to Vision One |
| `cam_aws_account_get` | Get detailed information for a specific AWS account |

### GCP Projects
| Tool | Purpose |
|------|---------|
| `cam_gcp_accounts_list` | List all Google Cloud projects connected to Vision One |
| `cam_gcp_account_get` | Get detailed information for a specific GCP project |

### Alibaba Cloud Accounts
| Tool | Purpose |
|------|---------|
| `cam_alibaba_accounts_list` | List all Alibaba Cloud accounts connected to Vision One |
| `cam_alibaba_account_get` | Get detailed information for a specific Alibaba account |

## Common Workflows

### Multi-Cloud Inventory Review
1. List all cloud accounts
2. Group by cloud provider
3. Check connection status for each
4. Identify any accounts with issues
5. Summarize coverage across providers

### Account Health Check
1. List cloud accounts
2. Get integrity status for each account
3. Identify disconnected or unhealthy accounts
4. Review feature enablement
5. Recommend remediation for issues

### Feature Coverage Analysis
1. List all accounts
2. Get features enabled for each account
3. Identify gaps in security coverage
4. Recommend enabling missing features

### New Account Verification
1. Get specific account details
2. Check connection integrity
3. Verify expected features are enabled
4. Confirm resource discovery is working

## Output Format

### Account Inventory
```
## Cloud Account Summary

**Total Accounts**: [count]
- AWS: [count]
- Azure: [count]
- GCP: [count]

### AWS Accounts
| Account ID | Name | Status | Region |
|------------|------|--------|--------|
| [ID] | [Name] | [Connected/Disconnected] | [Region] |

### Azure Subscriptions
| Subscription ID | Name | Status |
|-----------------|------|--------|
| [ID] | [Name] | [Status] |

### GCP Projects
| Project ID | Name | Status |
|------------|------|--------|
| [ID] | [Name] | [Status] |
```

### Account Details
```
## Cloud Account: [Name]

**Provider**: [AWS/Azure/GCP]
**Account ID**: [ID]
**Status**: [Connected/Disconnected]
**Connected Since**: [Date]

### Configuration
- Region: [Region]
- Organization: [Org name if applicable]

### Enabled Features
- [Feature 1]: Enabled
- [Feature 2]: Enabled
- [Feature 3]: Disabled

### Health Status
- Connection: [Healthy/Unhealthy]
- Last Sync: [Timestamp]
- Issues: [None/List issues]
```

## Security Considerations

- This skill provides read-only access to cloud account inventory
- Account IDs and configuration details are sensitive infrastructure information
- Use this data to verify security coverage, not for sharing externally
- Disconnected accounts may indicate security blind spots requiring immediate attention
- Cross-reference with cloud provider consoles for authoritative status
