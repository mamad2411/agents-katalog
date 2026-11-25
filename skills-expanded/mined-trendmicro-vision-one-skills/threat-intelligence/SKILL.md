# Threat Intelligence

Manage threat intelligence data including suspicious objects, exceptions, intelligence feeds, and custom reports using Trend Micro Vision One. This skill enables proactive threat hunting, indicator management, and intelligence-driven security operations.

## Instructions

1. When the user asks about threat indicators, suspicious objects, exceptions, intelligence feeds, or threat hunting, use this skill.

2. **Suspicious Object List**: Use suspicious object tools to manage known-bad indicators that should be blocked or logged across the environment.

3. **Exception List**: Use exception tools to manage false positive exclusions and trusted entities that should bypass security scanning.

4. **Threat Intelligence Feeds**: Query Trend's threat intelligence feeds for the latest IoCs, intelligence reports, and threat actor information.

5. **Custom Intelligence Reports**: Manage custom intelligence reports created from imported or collected threat data.

6. **Threat Sweeping**: Trigger searches across your environment for indicators from intelligence reports.

7. **CRITICAL - Write operations**: Adding/deleting suspicious objects and exceptions affects security enforcement. Confirm with user before making changes.

## Tools

This skill uses the following Vision One MCP tools:

### Suspicious Object List
| Tool | Purpose | Type |
|------|---------|------|
| `threatintel_suspicious_objects_list` | List suspicious objects (domains, IPs, URLs, file hashes, emails) | Read |
| `threatintel_suspicious_objects_add` | Add indicator to suspicious object list | Write |
| `threatintel_suspicious_objects_delete` | Remove indicator from suspicious object list | Write |

### Exception List
| Tool | Purpose | Type |
|------|---------|------|
| `threatintel_exceptions_list` | List exception entries (allowed indicators) | Read |
| `threatintel_exceptions_add` | Add indicator to exception list | Write |
| `threatintel_exceptions_delete` | Remove indicator from exception list | Write |

### Intelligence Feeds
| Tool | Purpose | Type |
|------|---------|------|
| `threatintel_feeds_list` | Retrieve intelligence reports with associated objects | Read |
| `threatintel_feed_indicators_list` | List IoCs from Trend Threat Intelligence Feed | Read |
| `threatintel_feed_filter_definition_get` | Get supported filter keys for feed queries | Read |

### Custom Intelligence Reports
| Tool | Purpose | Type |
|------|---------|------|
| `threatintel_intelligence_reports_list` | List custom intelligence reports | Read |
| `threatintel_intelligence_report_get` | Download a custom report as STIX Bundle | Read |
| `threatintel_intelligence_reports_delete` | Delete custom intelligence reports | Write |

### Threat Hunting
| Tool | Purpose | Type |
|------|---------|------|
| `threatintel_sweep_trigger` | Search environment for indicators from a report | Write |
| `threatintel_tasks_list` | List threat intelligence tasks and jobs | Read |
| `threatintel_task_results_get` | Get results of a threat intelligence task | Read |

## Indicator Types

All suspicious object and exception tools support these indicator types:

| Type | Description | Example |
|------|-------------|---------|
| `url` | Malicious URL | `http://malware.example.com/payload` |
| `domain` | Malicious domain | `malware.example.com` |
| `ip` | Malicious IP address | `192.168.1.100` |
| `senderMailAddress` | Malicious email sender | `attacker@phishing.com` |
| `fileSha1` | File SHA-1 hash | `da39a3ee5e6b4b0d3255bfef95601890afd80709` |
| `fileSha256` | File SHA-256 hash | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

## Common Workflows

### Review Suspicious Objects
1. List suspicious objects filtered by type or risk level
2. Review scan actions (block vs. log)
3. Check expiration dates
4. Identify indicators needing updates
5. Document findings for threat intel team

### Add Threat Indicator
1. Validate the indicator format and type
2. Determine appropriate risk level (high/medium/low)
3. Choose scan action (block for known-bad, log for suspicious)
4. **Confirm with user** before adding
5. Add to suspicious object list
6. Verify indicator was added successfully

### Manage Exceptions (False Positives)
1. List current exceptions
2. Identify indicator causing false positive
3. Verify indicator is truly benign
4. **Confirm with user** before adding exception
5. Add to exception list
6. Document reason for exception

### Query Threat Intelligence Feed
1. Get filter definitions to understand query options
2. Query feed indicators for specific time range or criteria
3. Filter by location, industry, or threat type
4. Review associated intelligence reports
5. Identify relevant IoCs for your environment

### Threat Hunting with Intelligence Reports
1. List available intelligence reports
2. Download report of interest (STIX Bundle format)
3. Review indicators in the report
4. **Confirm with user** before sweeping
5. Trigger sweep to search environment
6. Monitor task status
7. Review sweep results for matches

### Intelligence Report Management
1. List custom intelligence reports
2. Review report details and creation dates
3. Identify outdated or irrelevant reports
4. **Confirm with user** before deleting
5. Delete obsolete reports
6. Document cleanup for audit

## Output Format

### Suspicious Object List
```
## Suspicious Objects Summary

**Total Objects**: [count]
- URLs: [count]
- Domains: [count]
- IPs: [count]
- File Hashes: [count]
- Email Addresses: [count]

### High Risk Objects
| Type | Value | Scan Action | Expires | Description |
|------|-------|-------------|---------|-------------|
| [type] | [value] | [block/log] | [date] | [description] |

### Expiring Soon (< 7 days)
[List of indicators expiring soon]
```

### Exception List
```
## Exception List Summary

**Total Exceptions**: [count]

### Exceptions by Type
| Type | Value | Added | Description |
|------|-------|-------|-------------|
| [type] | [value] | [date] | [reason for exception] |
```

### Intelligence Report
```
## Intelligence Report: [Name]

**Report ID**: [ID]
**Created**: [Date]
**Updated**: [Date]

### Summary
[Report description]

### Indicators
- Domains: [count]
- IPs: [count]
- URLs: [count]
- File Hashes: [count]

### Related Threat Actors
[List if available]

### Recommended Actions
1. Review indicators for relevance
2. Consider adding high-confidence IoCs to suspicious object list
3. Run environment sweep if indicators are recent
```

### Sweep Results
```
## Threat Sweep Results

**Report**: [Report Name]
**Task ID**: [ID]
**Status**: [Completed/Running/Failed]

### Matches Found
| Indicator | Type | Match Location | First Seen | Last Seen |
|-----------|------|----------------|------------|-----------|
| [value] | [type] | [endpoint/network] | [date] | [date] |

### Recommended Actions
[Based on matches found]
```

### Write Operation Confirmation
```
## CONFIRMATION REQUIRED: [Operation Type]

**Operation**: [Add/Delete] [indicator type]
**Value**: [indicator value]
**List**: [Suspicious Objects/Exceptions]

### Impact
[Description of what will happen]

### Details
- Risk Level: [if applicable]
- Scan Action: [if applicable]
- Expiration: [if applicable]

**Type 'CONFIRM' to proceed or 'CANCEL' to abort:**
```

## Security Considerations

- **Write operations affect security enforcement** - adding/removing indicators changes what gets blocked or allowed
- Suspicious objects with "block" action will actively block matching traffic/files
- Exceptions bypass security scanning - only add truly benign indicators
- Intelligence feed data is sensitive and should not be shared externally
- Sweep operations may generate significant activity - coordinate with SOC
- Expired indicators are automatically removed - set appropriate expiration periods
- Document all changes to suspicious objects and exceptions for audit
- Review exception list regularly to prevent security blind spots
- High-risk indicators should have short expiration to ensure review
- Coordinate threat intel changes with your security operations team
