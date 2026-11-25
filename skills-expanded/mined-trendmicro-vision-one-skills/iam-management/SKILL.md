# IAM Management

Manage Vision One identity and access management including API keys, user accounts, and access controls. This skill includes sensitive write operations for identity management.

## Instructions

1. When the user asks about API keys, user accounts, or access management in Vision One, use this skill.

2. **List API keys**: Use `list_api_keys` to review existing API key inventory and status.

3. **Audit user accounts**: Use `list_accounts` to review user access and permissions.

4. **Check account details**: Use `get_account` for detailed user account information.

5. **CRITICAL - Write operations**: All write operations in this skill are sensitive and require explicit user confirmation:
   - Deleting API keys removes programmatic access
   - Inviting users grants access to the platform
   - Updating accounts changes permissions
   - Deleting accounts removes user access entirely

6. **Document changes**: All IAM changes should be documented for audit and compliance purposes.

7. **Principle of least privilege**: When helping with access decisions, recommend minimal necessary permissions.

## Tools

This skill uses the following Vision One MCP tools:

### Read Operations
| Tool | Purpose |
|------|---------|
| `iam_api_keys_list` | List all API keys with status and permissions |
| `iam_accounts_list` | List all user accounts, groups, and invitations |

### Write Operations (Sensitive - Require User Confirmation)
| Tool | Purpose | Risk Level |
|------|---------|------------|
| `iam_api_keys_delete` | Delete API keys (accepts array of key IDs) | High - Removes programmatic access |
| `iam_account_invite` | Invite a new user to Vision One | Medium - Grants platform access |
| `iam_account_update` | Modify user account settings/permissions | Medium - Changes access rights |
| `iam_account_delete` | Remove a user account | High - Removes all user access |

## Common Workflows

### API Key Audit
1. List all API keys
2. Identify keys by purpose/owner
3. Check key permissions and scope
4. Identify unused or excessive permissions
5. Recommend keys for rotation or deletion

### API Key Cleanup
1. List API keys
2. Identify keys for deletion (unused, compromised, etc.)
3. **Confirm with user** which keys to delete
4. **Get explicit approval** before deletion
5. Delete specified keys
6. Document deleted keys for audit

### User Access Review
1. List all accounts
2. Review permissions by role
3. Identify excessive permissions
4. Check for inactive accounts
5. Recommend access adjustments

### User Onboarding
1. Discuss required access level with user
2. Determine appropriate role and permissions
3. **Confirm account details** with user
4. Send account invitation
5. Document new account for audit

### User Offboarding
1. Get account details for departing user
2. Review account permissions
3. **Confirm deletion** with user
4. Delete the account
5. Document removal for audit

### Permission Update
1. Get current account details
2. Discuss required changes with user
3. **Confirm new permissions** are appropriate
4. Update account settings
5. Verify changes applied correctly

## Output Format

### API Key Inventory
```
## API Key Summary

**Total Keys**: [count]
- Active: [count]
- Inactive: [count]

### API Keys
| Key Name | Status | Created | Last Used | Permissions |
|----------|--------|---------|-----------|-------------|
| [Name] | [Active/Inactive] | [Date] | [Date] | [Scope] |

### Recommendations
- [count] keys have not been used in 90+ days
- [count] keys have excessive permissions
```

### User Account Summary
```
## User Account Summary

**Total Accounts**: [count]
- Active: [count]
- Inactive: [count]

### Accounts by Role
| Role | Count |
|------|-------|
| Administrator | [count] |
| Analyst | [count] |
| Viewer | [count] |

### Accounts
| User | Email | Role | Status | Last Login |
|------|-------|------|--------|------------|
| [Name] | [Email] | [Role] | [Active/Inactive] | [Date] |
```

### Write Operation Confirmation (Critical)
```
## CONFIRMATION REQUIRED: [Operation Type]

**Operation**: [Specific action]
**Target**: [API key name / User account]

### Impact
[Description of what will happen]

### This action:
- [ ] Is irreversible (deletion)
- [ ] Affects user access
- [ ] Requires documentation

**Type 'CONFIRM' to proceed or 'CANCEL' to abort:**
```

### Audit Log Entry
```
## IAM Change Record

**Date**: [Timestamp]
**Operation**: [Action performed]
**Target**: [Key/Account affected]
**Performed By**: [User who requested]

### Details
[Specifics of the change]

### Justification
[Reason for the change]
```

## Security Considerations

- **All write operations are sensitive and require explicit user confirmation**
- API key deletion immediately revokes programmatic access - verify no critical integrations depend on the key
- Account deletion is permanent and removes all user access
- Follow your organization's change management process for IAM changes
- Document all changes for compliance and audit purposes
- Apply principle of least privilege when granting permissions
- Regularly audit API keys and accounts for unnecessary access
- Consider impact on integrations before deleting API keys
- Coordinate account changes with user's management chain
- Deletion operations cannot be undone - verify target before confirming
