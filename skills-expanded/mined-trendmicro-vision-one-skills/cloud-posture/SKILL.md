# Cloud Posture

Manage cloud security posture, compliance scanning, and security settings across cloud environments using Trend Micro Vision One. This skill includes both read and write operations for posture management.

## Instructions

1. When the user asks about cloud posture, compliance, or cloud security configuration, use this skill to query and manage posture data.

2. **Check posture status**: Start with `get_cloud_posture_overview` to understand the current compliance and posture state.

3. **List compliance findings**: Use `list_cloud_posture_findings` to identify misconfigurations and compliance violations.

4. **Review templates**: Use `list_cloud_posture_templates` to see available compliance templates and standards.

5. **Before write operations**: Always confirm with the user before executing any write operations (scan triggers, settings updates).

6. **Trigger scans**: Use `trigger_cloud_posture_scan` to initiate compliance scans when requested by the user.

7. **Update settings**: Use `update_cloud_posture_settings` to modify posture configurations with user approval.

8. **Track remediation**: Help users track which findings have been addressed and which remain open.

## Tools

This skill uses the following Vision One MCP tools:

### CSPM Accounts
| Tool | Purpose | Type |
|------|---------|------|
| `cloud_posture_accounts_list` | List all CSPM accounts | Read |

### Compliance Checks
| Tool | Purpose | Type |
|------|---------|------|
| `cloud_posture_account_checks_list` | List compliance checks for an account | Read |

### Scan Management
| Tool | Purpose | Type |
|------|---------|------|
| `cloud_posture_account_scan` | Start scanning a cloud posture account | Write |
| `cloud_posture_account_scan_settings_get` | Get scan settings for an account | Read |
| `cloud_posture_account_scan_settings_update` | Update scan settings (enabled/interval) | Write |

### Template Scanner
| Tool | Purpose | Type |
|------|---------|------|
| `cloud_posture_template_scanner_run` | Scan IaC templates (CloudFormation/Terraform) | Write |

### Cloud Risk Management
| Tool | Purpose | Type |
|------|---------|------|
| `cloud_risk_management_accounts_list` | List cloud accounts you can access | Read |
| `cloud_risk_management_account_scan_rules_get` | Get scan rule settings for an account | Read |
| `cloud_risk_management_services_list` | List cloud services and associated rules | Read |

## Common Workflows

### Compliance Assessment
1. Get posture overview for current state
2. List findings grouped by severity
3. Identify critical misconfigurations
4. Map findings to compliance frameworks
5. Prioritize remediation activities

### Compliance Scan Request
1. List available templates to identify scan scope
2. **Confirm with user** before triggering scan
3. Trigger cloud posture scan
4. Monitor scan progress
5. Review new findings after completion

### Posture Configuration Update
1. Review current settings
2. Discuss proposed changes with user
3. **Get explicit user approval** for changes
4. Apply settings update
5. Verify changes were applied successfully

### Remediation Tracking
1. List findings filtered by status
2. Identify findings marked for remediation
3. Check if remediated findings have been rescanned
4. Report on remediation progress
5. Highlight remaining open items

### Infrastructure as Code Scanning
1. Receive CloudFormation or Terraform template content
2. **Confirm with user** before scanning
3. Run template scanner
4. Review findings for misconfigurations
5. Report security issues before deployment
6. Recommend remediations for template issues

### Scan Rule Configuration
1. List cloud risk management accounts
2. Get scan rule settings for specific account
3. Review customized rules vs. defaults
4. List available services and rules
5. Document rule configuration for compliance

## Output Format

### Posture Overview
```
## Cloud Posture Summary

**Overall Compliance**: [%]
**Last Scan**: [Timestamp]

### Findings by Severity
- Critical: [count]
- High: [count]
- Medium: [count]
- Low: [count]

### Compliance by Framework
| Framework | Score | Pass | Fail |
|-----------|-------|------|------|
| CIS | [%] | [count] | [count] |
| SOC 2 | [%] | [count] | [count] |
| PCI DSS | [%] | [count] | [count] |
```

### Compliance Finding
```
## Finding: [Title]

**Severity**: [Critical/High/Medium/Low]
**Framework**: [CIS/SOC 2/etc.]
**Rule ID**: [ID]

### Description
[Finding description]

### Affected Resources
- [Resource type]: [Resource ID]

### Remediation
[Steps to remediate]

### Compliance Impact
- [Framework]: [Control ID]
```

### Write Operation Confirmation
```
## Action Required: [Operation Type]

**Operation**: [Description of what will be changed]
**Scope**: [What resources/settings will be affected]

### Current State
[Current configuration]

### Proposed Change
[What will change]

**Do you want to proceed with this operation? (yes/no)**
```

## Security Considerations

- **Write operations require explicit user confirmation** before execution
- Scan triggers may impact cloud API rate limits
- Settings changes affect security policy enforcement
- Document all configuration changes for audit purposes
- Critical findings should be addressed promptly
- Coordinate posture changes with cloud operations teams
- Test settings changes in non-production environments first when possible
