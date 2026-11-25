---
name: validate-mcp-access
description: Validate MCP connection access for Slack, Glean, JIRA, and Confluence in the logfood workspace
---

# Validate MCP Access Skill

Validates that the user has active credentials for MCP connections (Slack, Glean, JIRA, Confluence) in the logfood Databricks workspace.

## Quick Validation

For a quick check that all MCPs are configured correctly, run:
```bash
echo "" | llm agent configure mcp
```

This will verify MCP server availability and configuration.

## Detailed Validation Instructions

### 1. Get User Identity

First, retrieve the user's Databricks ID from the logfood workspace:

```bash
databricks current-user me --profile logfood
```

Extract the `id` field from the response - this is the user identity needed to check credentials.

### 2. Check MCP Connection Credentials

For each MCP connection, check if the user has valid credentials:

#### Slack

```bash
databricks api get /api/2.1/unity-catalog/connections/slack/user-credentials/<USER_ID> --profile logfood
```

#### Glean MCP

```bash
databricks api get /api/2.1/unity-catalog/connections/glean-mcp/user-credentials/<USER_ID> --profile logfood
```

#### JIRA MCP

```bash
databricks api get /api/2.1/unity-catalog/connections/jira-mcp/user-credentials/<USER_ID> --profile logfood
```

#### Confluence MCP

```bash
databricks api get /api/2.1/unity-catalog/connections/confluence-mcp/user-credentials/<USER_ID> --profile logfood
```

### 3. Evaluate Results

For each connection, evaluate the response:

**Success Response** - User has valid credentials:
```json
{
  "connection_user_credential": {
    "options_kvpairs": {
      "options": {
        "access_token_expiration": "...",
        "refresh_token_expiration": "..."
      }
    },
    "provisioning_info": {
      "state": "ACTIVE"
    },
    "user_identity": "<USER_ID>"
  }
}
```

**Error Response** - User needs to authenticate:
```
Error: Credential for user identity('<USER_ID>') is not found for the connection '<CONNECTION_NAME>'.
Please login first to the connection by visiting <LOGIN_URL>
```

### 4. Report Status

Present results in a clear table format:

| Connection | Status | Action Required |
|------------|--------|-----------------|
| slack      | ACTIVE / NOT CONFIGURED | None / Login required |
| glean-mcp  | ACTIVE / NOT CONFIGURED | None / Login required |
| jira-mcp   | ACTIVE / NOT CONFIGURED | None / Login required |
| confluence-mcp | ACTIVE / NOT CONFIGURED | None / Login required |

### 5. Provide Login Instructions

For any connection that requires authentication, provide the login URL:

- **Slack**: https://adb-2548836972759138.18.azuredatabricks.net/explore/connections/slack?o=2548836972759138
- **Glean MCP**: https://adb-2548836972759138.18.azuredatabricks.net/explore/connections/glean-mcp?o=2548836972759138
- **JIRA MCP**: https://adb-2548836972759138.18.azuredatabricks.net/explore/connections/jira-mcp?o=2548836972759138
- **Confluence MCP**: https://adb-2548836972759138.18.azuredatabricks.net/explore/connections/confluence-mcp?o=2548836972759138

Instruct the user to:
1. Click the login URL
2. Complete the OAuth flow in their browser
3. Return and re-run this validation to confirm access

### 6. Completion

Once all connections show ACTIVE status, confirm that MCP tools are ready to use.
