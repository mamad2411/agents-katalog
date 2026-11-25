---
name: jira-actions
description: "Use this skill for ANY mention of ES tickets, JIRA ES, engineering support tickets, or filing tickets. Triggers on: 'ES ticket', 'ES-123456', 'file a ticket', 'create an ES', 'JIRA ES'. This skill handles searching, viewing, commenting, and creating ES tickets."
---

# JIRA Actions Skill

Read, search, comment, and create Engineering Support (ES) tickets using the JIRA MCP tools.

## CRITICAL: Use the JIRA Ticket Assistant Agent

**For any non-trivial JIRA operation, IMMEDIATELY delegate to the `fe-jira-tools:jira-ticket-assistant` agent using the Task tool.** This ensures proper handling of:
- Creating tickets with all required fields
- Looking up required field values and IDs
- Searching and analyzing tickets
- Adding properly formatted comments

```
Task(subagent_type="fe-jira-tools:jira-ticket-assistant", prompt="<user's request>")
```

Only handle simple read operations (like viewing a single ticket by ID) directly. For anything involving field lookups, ticket creation, or complex searches, use the agent.

## Prerequisites

### Check MCP Connection

The JIRA MCP should be configured automatically via vibe setup. If you encounter connection errors, run:
```bash
echo "" | llm agent configure mcp
```

Or use the `validate-mcp-access` skill to check your MCP connections.

## Important Access Restrictions

**CRITICAL**: Since December 2024, most Field Engineering members (SAs, DSAs, SSAs, RSAs, STS below L7) cannot create ES tickets directly in JIRA. They must use:
- **go/FEfileaticket** - The JIRA Portal for filing tickets (preferred)
- **go/fe-break-glass** - Temporary 1-hour access via Opal for emergencies
- **Clone existing tickets** - Find similar tickets and clone them (works if you can view the ticket)

Only users in the **FE.Exception.ES.Access** group can create tickets directly.

## Operations

### Search ES Tickets

Use `jira_read_api_call` with the `issues.search` endpoint and JQL (JIRA Query Language):

```
# Search by keyword
jira_read_api_call("issues.search", {"jql": "project = ES AND summary ~ 'keyword'", "max_results": 20})

# Search by customer name
jira_read_api_call("issues.search", {"jql": "project = ES AND summary ~ 'CustomerName'", "max_results": 10})

# Search by component (use custom field)
jira_read_api_call("issues.search", {"jql": "project = ES AND cf[18150] = 'Storage.Delta'", "max_results": 10})

# Search by issue type
jira_read_api_call("issues.search", {"jql": "project = ES AND issuetype = 'Incident'", "max_results": 10})

# Search recent tickets
jira_read_api_call("issues.search", {"jql": "project = ES ORDER BY created DESC", "max_results": 20})
```

**JQL Syntax Notes:**
- Use single quotes for string values
- Common operators: `=`, `!=`, `~` (contains), `IN`, `NOT IN`, `ORDER BY`
- Custom fields use syntax: `cf[18150]` for Component

### View ES Ticket Details

Use `jira_read_api_call` with the `issues.get` endpoint:

```
# View ticket details
jira_read_api_call("issues.get", {"issue_id": "ES-123456"})

# View with specific fields
jira_read_api_call("issues.get", {"issue_id": "ES-123456", "fields": "key,summary,status,description,comment"})

# Analyze ticket content (for large tickets)
jira_read_api_call("issues.get", {"issue_id": "ES-123456", "analysis_prompt": "What errors are reported?"})
```

### Add Comments (Non-Destructive)

Use `jira_write_api_call` with the `issues.add_comment` endpoint:

```
# Add a comment (ADF format)
jira_write_api_call("issues.add_comment", {
    "issue_id": "ES-123456",
    "comment": {
        "type": "doc",
        "version": 1,
        "content": [{
            "type": "paragraph",
            "content": [{"type": "text", "text": "Your comment here"}]
        }]
    }
})
```

### Update Existing Tickets

Use `jira_write_api_call` with the `issues.update` endpoint:

```
# Update summary
jira_write_api_call("issues.update", {
    "issue_id": "ES-123456",
    "updates": {"summary": "Updated Summary"}
})

# Update status (uses workflow transitions automatically)
jira_write_api_call("issues.update", {
    "issue_id": "ES-123456",
    "updates": {"status": "In Progress"}
})

# Update multiple fields
jira_write_api_call("issues.update", {
    "issue_id": "ES-123456",
    "updates": {
        "summary": "New Summary",
        "description": "New description text",
        "priority": "High"
    }
})
```

### Create ES Tickets (Restricted Access)

**Only use if you have FE.Exception.ES.Access permission or break-glass access.**

Use `jira_write_api_call` with the `issues.create` endpoint.

#### STEP 1: ALWAYS Look Up Required Fields First

**Before creating ANY ticket, use `issues.get_create_metadata` to discover the required fields for that issue type:**

```
jira_read_api_call("issues.get_create_metadata", {
    "project": "ES",
    "issuetype": "Incident"
})
```

This returns all available fields for that project/issue type combination, including:
- Whether each field is `required: True/False`
- The field's `name`, `key`, and `schema` (type)
- `allowedValues` for select/radio fields (with IDs you need to use)

**To filter for just required fields:**
```
jira_read_api_call("issues.get_create_metadata", {
    "project": "ES",
    "issuetype": "Incident",
    "bash_query": "grep -B10 'required: True'"
})
```

**CRITICAL: Field Format for Select Fields**

Select/radio button fields (like severity, component, customer facing) must use the `{"id": "XXXXX"}` format, NOT `{"value": "..."}`. Using `{"value": "..."}` will cause the request to fail silently.

#### Required Fields for ES Incident

**ALL of these fields are REQUIRED - missing any will cause creation to fail:**

| Field | Key | Format | Notes |
|-------|-----|--------|-------|
| Project | `project` | `"ES"` | Always ES for Engineering Support |
| Issue Type | `issuetype` | `"Incident"` | String value |
| Summary | `summary` | String | Format: `[CustomerName] Brief description` |
| **Affects Versions** | `versions` | `[{"name": "N/A"}]` | **REQUIRED** - Use "N/A" or DBR version |
| **Support Severity Level** | `customfield_11500` | `{"id": "XXXXX"}` | **REQUIRED** - See severity IDs below |
| **External Customer Facing?** | `customfield_14677` | `{"id": "13344"}` | **REQUIRED** - Yes=13344, No=13345 |
| **ES Component** | `customfield_18150` | `{"id": "XXXXX"}` | **REQUIRED** - Get ID from metadata or similar tickets |

#### Severity Level IDs

| Severity | ID | Value |
|----------|-----|-------|
| SEV0 Critical | `10600` | Production down, major impact |
| SEV1 High | `10601` | Partial outage, significant impact |
| SEV2 Standard-Non-Critical | `10602` | Important but not urgent (default) |
| SEV3 Low | `10603` | Minor issues |

#### Recommended Additional Fields

| Field | Key | Format |
|-------|-----|--------|
| Workspace ID (single) | `customfield_11600` | String: `"1234567890"` |
| Workspace IDs (multiple) | `customfield_17025` | String: `"1234567890"` |
| Customer Name | `customfield_21301` | String: `"CustomerName"` |
| Cloud | `customfield_14207` | String: `"AWS"`, `"Azure"`, or `"GCP"` |

#### Complete Example: Create an Incident

**IMPORTANT:** Always include full error details directly in the ticket description. Do NOT rely solely on Slack links - not everyone has access, and messages can be deleted. Copy the actual error messages and stack traces into the ticket.

```
jira_write_api_call("issues.create", {
    "project": "ES",
    "issuetype": "Incident",
    "summary": "[CustomerName] Brief description of the issue",
    "description": "**Customer:** CustomerName\n**Workspace ID:** 1234567890\n**Region:** AWS US Oregon\n\n---\n\n**Problem Description:**\nBrief description of what is happening.\n\n**Error Message (FULL):**\n```\nPaste the complete error message here\nInclude the full stack trace\nDo not truncate\n```\n\n**Customer Context:**\n- Any relevant customer observations\n- Recent changes, scale of operation, etc.\n\n**Customer Impact:**\n- Business impact of the issue\n\n**Similar Previous Tickets:**\n- ES-XXXXXX: Brief description if applicable\n\n**Slack Discussion:**\nhttps://databricks.slack.com/...",
    "additional_fields": {
        "customfield_11500": {"id": "10602"},
        "customfield_18150": {"id": "20802"},
        "customfield_14677": {"id": "13344"},
        "versions": [{"name": "N/A"}],
        "customfield_17025": "1234567890"
    }
})
```

#### Finding the Right ES Component ID

1. Search for a similar ticket: `jira_read_api_call("issues.search", {"jql": "project = ES AND cf[18150] = 'ComponentName'"})`
2. Get the component from a similar ticket: `jira_read_api_call("issues.get", {"issue_id": "ES-XXXXXX"})`
3. Or use `issues.get_create_metadata` with bash_query to search: `jira_read_api_call("issues.get_create_metadata", {"project": "ES", "issuetype": "Incident", "bash_query": "grep -i 'mlflow'"})`

Common ES Component IDs (from production tickets):
- `20802` - MLflow.ModelRegistry
- Use go/whoownsit to find the correct component name, then search metadata for the ID

#### Create a Customization/Service Request

```
jira_write_api_call("issues.create", {
    "project": "ES",
    "issuetype": "Customization/Service Request",
    "summary": "[CustomerName] Request for quota increase",
    "description": "Request details...",
    "additional_fields": {
        "customfield_11500": {"id": "10602"},
        "customfield_18150": {"id": "XXXXX"},
        "customfield_14677": {"id": "13344"},
        "versions": [{"name": "N/A"}],
        "customfield_17025": "1234567890"
    }
})
```

**If create fails with permission error:**
1. Use go/FEfileaticket portal instead
2. Or request break-glass access via go/fe-break-glass (temporary 1-hour access)
3. Or find a similar ticket, view it, and request someone with access to clone it

## Issue Type Reference

See `resources/ES_TICKET_TYPES.md` for detailed information on:
- Incident
- Advanced Support
- Customization/Service Request
- Private Preview Bugs
- Xteam-Ask

## Severity Level Reference

See `resources/ES_SEVERITY_LEVELS.md` for definitions of:
- SEV0 (Critical) - Total outages, data integrity, >$10k impact
- SEV1 (High) - Partial outages, production impact
- SEV2 (Standard Non-Critical) - Customer impacting but not critical
- SEV3 (Low) - Trivial, minimal impact

## Key Fields Reference

See `resources/ES_KEY_FIELDS.md` for common custom fields:
- Support Severity Level
- Workspace ID
- Cloud (AWS/Azure/GCP)
- Customer Name
- Component/Service Area

## Best Practices

1. **Always search first** - Look for similar existing tickets before creating new ones
2. **Use descriptive summaries** - Include customer name: `[CustomerName] Brief issue description`
3. **Set correct severity** - Follow the severity level guidelines
4. **Assign to Unassigned** - Let the owning team triage unless you know the assignee
5. **Link related tickets** - Reference Salesforce cases, other ES tickets
6. **Include workspace IDs** - Always include affected workspace IDs
