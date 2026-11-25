---
name: source-management
description: >
  Manage and configure search sources, connectors, and indexing settings
  for the enterprise search system. Add, remove, test, and monitor data
  source connections. Control what gets indexed, how often, and with what
  permissions. View connector health and troubleshoot sync issues.
  TRIGGER when: user asks to add a source, connect a tool, configure
  indexing, check connector status, manage search sources, troubleshoot
  sync issues, or asks "what sources are connected".
argument-hint: "[add|remove|list|status|test|configure] [source name] [--options]"
user-invocable: true
---

# Search Source Management

Add, configure, monitor, and troubleshoot enterprise search source connectors and indexing pipelines.

## Source Management Operations

### List Connected Sources

Display all currently configured sources with their status:

```
# Connected Search Sources

| #  | Source Name       | Type     | Status  | Last Sync          | Items Indexed | Health |
|----|-------------------|----------|---------|--------------------|---------------|--------|
| 1  | [Name]            | [Type]   | Active  | [timestamp]        | [count]       | Good   |
| 2  | [Name]            | [Type]   | Active  | [timestamp]        | [count]       | Warn   |
| 3  | [Name]            | [Type]   | Paused  | [timestamp]        | [count]       | —      |
| 4  | [Name]            | [Type]   | Error   | [timestamp]        | [count]       | Error  |

Legend: Good = syncing normally | Warn = degraded performance | Error = sync failing
```

### Add a New Source

Guided process for connecting a new data source:

#### Step 1: Identify the Source Type

| Source Type       | Supported Platforms                              | Auth Method         |
|-------------------|--------------------------------------------------|---------------------|
| Email             | Gmail, Outlook/Exchange, Yahoo                   | OAuth 2.0           |
| Chat              | Slack, Microsoft Teams, Discord                  | OAuth 2.0 / Bot Token|
| Documents         | Google Drive, SharePoint, Dropbox, Box           | OAuth 2.0           |
| Wiki              | Confluence, Notion, GitBook, MediaWiki           | API Key / OAuth     |
| Tickets           | Jira, Linear, Asana, GitHub Issues, ServiceNow   | API Key / OAuth     |
| Code              | GitHub, GitLab, Bitbucket                        | OAuth / PAT         |
| Calendar          | Google Calendar, Outlook Calendar                | OAuth 2.0           |
| CRM               | Salesforce, HubSpot                              | OAuth 2.0           |
| Custom            | REST API, GraphQL, Database                      | API Key / Custom    |

#### Step 2: Configure Connection

Required configuration for each source:

```
Source Configuration:
  name:           [human-readable name for this connection]
  type:           [source type from table above]
  platform:       [specific platform, e.g., "slack"]
  auth_method:    [OAuth, API Key, PAT, etc.]
  credentials:    [securely stored reference — never display in plain text]
  base_url:       [API endpoint if custom]
  
Indexing Configuration:
  sync_frequency: [realtime | 5min | 15min | 1hour | 6hours | daily]
  scope:          [what to index — channels, folders, spaces, projects]
  content_types:  [messages, files, pages, comments, attachments]
  date_range:     [how far back to index — 30d | 90d | 1y | all]
  max_items:      [optional cap on indexed items]

Access Configuration:
  respect_source_permissions: [true/false — recommended: true]
  allowed_users:              [user list or "all"]
  allowed_groups:             [group list or "all"]
```

#### Step 3: Set Indexing Scope

Define what content gets indexed:

| Scope Setting     | Options                                        | Default              |
|-------------------|------------------------------------------------|----------------------|
| Channels/Folders  | All, specific list, exclude list               | All accessible       |
| Content depth     | Titles only, titles + body, full + attachments | Titles + body        |
| File types        | All, documents only, exclude binary            | Documents only       |
| History depth     | Last 30/90/365 days, all time                  | Last 90 days         |
| Update tracking   | New only, new + modified, all changes          | New + modified       |

#### Step 4: Test Connection

Run a connection test before activating:

```
Connection Test Results: [Source Name]
  Authentication:  [PASS/FAIL] — [details]
  API Access:      [PASS/FAIL] — [details]
  Permissions:     [PASS/FAIL] — [details]
  Sample Query:    [PASS/FAIL] — returned [N] results
  Index Write:     [PASS/FAIL] — [details]
  
  Overall: [READY / NOT READY]
  [If NOT READY: specific remediation steps]
```

### Remove a Source

Checklist before removal:
- [ ] Confirm the source name with the user
- [ ] Warn about data that will be removed from the index
- [ ] Check if any saved searches or digests depend on this source
- [ ] Offer to export indexed metadata before removal
- [ ] Remove index data after confirmation
- [ ] Update any dependent configurations (digests, alerts, saved searches)

### Source Health Monitoring

#### Health Check Dashboard

```
# Source Health Report — [Date]

## Summary
Total sources: [N] | Healthy: [N] | Degraded: [N] | Failed: [N]

## Detailed Status

### [Source Name] — [Status Emoji] [Healthy/Degraded/Failed]
  Last successful sync: [timestamp]
  Sync frequency:       [configured frequency]
  Items indexed:        [total] ([+N new] since last sync)
  Average sync time:    [duration]
  Error rate:           [percentage over last 24h]
  Quota usage:          [X/Y API calls used]
  
  Recent issues:
  - [timestamp] [issue description]
```

#### Common Health Issues and Remediation

| Issue                        | Symptoms                        | Resolution                                |
|------------------------------|---------------------------------|-------------------------------------------|
| Authentication expired       | 401 errors, sync failing        | Re-authenticate with OAuth flow           |
| Rate limit exceeded          | 429 errors, partial syncs       | Reduce sync frequency or scope            |
| Permission revoked           | 403 errors on specific content  | Re-grant access in source platform        |
| API endpoint changed         | Connection errors                | Update base_url configuration             |
| Source unavailable           | Timeout errors                   | Check source platform status; retry later |
| Index corruption             | Missing or duplicate results     | Trigger a full re-index                   |
| Quota exhausted              | Sync stops mid-way              | Wait for quota reset or upgrade plan      |
| Schema change in source      | Parse errors on new content     | Update connector mapping configuration    |

### Configure Indexing Settings

Modify settings for an existing source:

```
# Indexing Configuration: [Source Name]

Current Settings → Proposed Changes:
  sync_frequency: 1hour → [new value]
  scope:          #general,#engineering → [new value]
  content_types:  messages,files → [new value]
  date_range:     90d → [new value]

Impact Assessment:
  Estimated index size change: [+/- N items]
  Estimated sync time change:  [+/- duration]
  API quota impact:            [+/- N calls per day]

Proceed? [Confirm required]
```

## Security and Compliance

### Permission Model

| Setting                         | Description                                    | Recommended |
|---------------------------------|------------------------------------------------|-------------|
| Respect source permissions      | Only show results user has access to in source | Always on   |
| Audit logging                   | Log all search queries and results accessed    | Always on   |
| Data retention                  | How long indexed data is kept                  | Match source|
| Encryption at rest              | Encrypt stored index data                      | Always on   |
| PII detection                   | Flag or exclude personally identifiable info   | On          |
| Credential rotation             | How often to rotate API keys/tokens            | 90 days     |

### Compliance Checklist

- [ ] All sources configured with least-privilege access
- [ ] Source permissions are respected in search results
- [ ] Audit logging is enabled for all queries
- [ ] Sensitive content patterns are configured for detection
- [ ] Data retention policies align with company policy
- [ ] Credentials are stored in a secure vault, never in plain text
- [ ] Regular access reviews are scheduled

## Edge Cases

- **Duplicate sources**: Warn if a source of the same type and scope is already connected
- **Overlapping scope**: If two connectors index the same content, flag potential duplicates
- **Large initial sync**: For sources with extensive history, recommend starting with a short date range and expanding
- **Source deprecation**: If a platform announces API deprecation, alert the user proactively
- **Partial permissions**: If the connector has access to only some channels/folders, clearly document what is and is not indexed
- **Free tier limits**: Track API quotas and warn before reaching limits

## Follow-Up Actions

After any source management operation, offer:
1. "Want me to run a test search to verify the source is working?"
2. "Should I check the health of all other connected sources?"
3. "Want me to update your digest configuration to include this source?"
4. "Should I trigger an initial sync now or wait for the scheduled time?"
