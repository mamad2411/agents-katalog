# Cyber Risk Exposure Management

Analyze attack surface exposure, vulnerabilities, and risk posture using Trend Micro Vision One's Cyber Risk Exposure Management capabilities. This comprehensive skill provides visibility into internet-facing assets, CVE exposure, domain risks, and account compromise indicators.

## Instructions

1. When the user asks about attack surface, external exposure, vulnerabilities, or risk posture, use this skill to query exposure data.

2. **Assess overall risk**: Start with `get_attack_surface_risk_overview` to understand the organization's risk posture and exposure levels.

3. **Analyze internet-facing assets**: Use `list_internet_facing_assets` to identify externally accessible systems and their risk levels.

4. **CVE analysis**: Use `list_cves` and `get_cve_details` to identify vulnerable systems and prioritize patching based on exploitability and exposure.

5. **Domain security**: Check domain risks with `list_domain_accounts_with_weak_credentials`, `get_domain_risk_overview`, and related tools.

6. **Account compromise**: Use `list_accounts_with_compromised_credentials` to identify accounts requiring immediate password resets.

7. **Device risk**: Query `list_devices` and `get_global_device_risk_indicators` to understand endpoint risk distribution.

8. **Regional exposure**: Use geographic queries to understand exposure by region when relevant.

9. **Prioritize findings**: Always present findings ordered by risk score or severity, with actionable remediation steps.

## Tools

This skill uses the following Vision One MCP tools (all read-only):

### Devices & Endpoints
| Tool | Purpose |
|------|---------|
| `crem_attack_surface_devices_list` | List discovered attack surface devices with risk scores |

### User Accounts
| Tool | Purpose |
|------|---------|
| `crem_attack_surface_high_risk_users_list` | List high risk users |
| `crem_attack_surface_domain_accounts_list` | List discovered domain accounts |
| `crem_attack_surface_service_accounts_list` | List discovered service accounts |

### Internet-Facing Assets
| Tool | Purpose |
|------|---------|
| `crem_attack_surface_public_ips_list` | List discovered public IP addresses |
| `crem_attack_surface_global_fqdns_list` | List internet-facing domains (FQDNs) |

### Cloud Assets
| Tool | Purpose |
|------|---------|
| `crem_attack_surface_cloud_assets_list` | List discovered cloud assets |
| `crem_attack_surface_cloud_asset_profile_get` | Get a cloud asset's profile |
| `crem_attack_surface_cloud_asset_risk_indicators_list` | List a cloud asset's risk indicators |

### Local Applications
| Tool | Purpose |
|------|---------|
| `crem_attack_surface_local_apps_list` | List discovered local applications |
| `crem_attack_surface_local_app_profile_get` | Get a local app's profile |
| `crem_attack_surface_local_app_risk_indicators_list` | List a local app's risk indicators |
| `crem_attack_surface_local_app_devices_list` | List devices with specific local app installed |
| `crem_attack_surface_local_app_executable_files_list` | List local app executable files |

### Tags & Organization
| Tool | Purpose |
|------|---------|
| `crem_attack_surface_custom_tags_list` | List custom tag definitions |

## Common Workflows

### Attack Surface Assessment
1. Get attack surface risk overview
2. List internet-facing assets sorted by risk
3. Identify high-risk services (RDP, SSH, databases exposed)
4. List CVEs affecting exposed systems
5. Provide prioritized remediation recommendations

### Vulnerability Management
1. List CVEs sorted by severity and exploitability
2. Get details on critical CVEs
3. List vulnerable devices for each priority CVE
4. Cross-reference with internet-facing assets
5. Generate patching priority list

### Credential Risk Assessment
1. Get account compromise summary
2. List accounts with compromised credentials
3. List domain accounts with weak credentials
4. Correlate with privileged account lists
5. Recommend immediate password resets

### Executive Risk Report
1. Get exposure overview and risk metrics
2. Summarize internet-facing asset exposure
3. Highlight critical vulnerabilities
4. Show credential risk statistics
5. Provide trend analysis if available

### Cloud Asset Risk Assessment
1. List discovered cloud assets
2. Filter by asset type, criticality, or risk score
3. Get profile for high-risk cloud assets
4. List risk indicators for specific assets
5. Correlate with cloud posture findings

### Local Application Risk Assessment
1. List discovered local applications
2. Filter by OS platform or risk score
3. Get profile for applications of interest
4. List risk indicators and vulnerabilities
5. Identify devices running vulnerable applications

### High-Risk User Analysis
1. List high-risk users by risk score
2. Analyze user risk factors
3. Correlate with domain and service accounts
4. Identify accounts requiring attention
5. Recommend access reviews or password resets

## Output Format

### Risk Overview
```
## Attack Surface Risk Summary

**Overall Risk Score**: [Score]/100
**Risk Level**: [Critical/High/Medium/Low]

### Exposure Metrics
- Internet-facing assets: [count]
- Critical CVEs: [count]
- Compromised credentials: [count]

### Top Risks
1. [Risk description] - Score: [X]
2. [Risk description] - Score: [X]
```

### CVE Report
```
## Vulnerability: [CVE-ID]

**CVSS Score**: [Score]
**Exploitability**: [High/Medium/Low]
**Affected Devices**: [count]

### Description
[CVE description]

### Affected Systems
- [hostname/IP] - [risk context]

### Remediation
[Patch information and mitigation steps]
```

### Compromised Credentials
```
## Credential Exposure Alert

**Account**: [username/email]
**Exposure Source**: [breach name/date if available]
**Risk Level**: [Critical/High]

### Recommended Actions
1. Force password reset immediately
2. Enable MFA if not enabled
3. Review recent account activity
4. Check for lateral movement indicators
```

## Security Considerations

- This skill provides read-only access to sensitive risk data
- Vulnerability and credential information is highly sensitive
- Do not share CVE details or compromised credential lists externally
- Use findings to prioritize remediation, not for compliance reporting without proper context
- Credential exposure data should trigger immediate security response
