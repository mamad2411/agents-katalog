# Custom Rules

Create, manage, and test custom security rules for Cloud Risk Management in Trend Micro Vision One. Custom rules allow organizations to define their own compliance checks tailored to specific security requirements.

## Instructions

1. When the user asks about custom rules, custom compliance checks, or organization-specific security rules, use this skill.

2. **List existing rules**: Start with `cloud_posture_custom_rules_list` to see all custom rules in the organization.

3. **Get rule details**: Use `cloud_posture_custom_rule_get` to retrieve the full configuration of a specific rule.

4. **Test before deploying**: Always use `cloud_posture_custom_rule_test` to validate rule configuration before creating or updating rules.

5. **Write operations require Master Administrator role**: Creating, updating, and deleting custom rules requires elevated permissions.

6. **Confirm with user**: Always confirm with the user before executing create, update, or delete operations.

7. **Understand rule structure**: Custom rules consist of attributes (data to extract from resources) and event rules (conditions to evaluate).

## Tools

This skill uses the following Vision One MCP tools:

| Tool | Purpose | Type | Role Required |
|------|---------|------|---------------|
| `cloud_posture_custom_rules_list` | List all custom rules in the organization | Read | Any |
| `cloud_posture_custom_rule_get` | Get detailed configuration of a specific rule | Read | Any |
| `cloud_posture_custom_rule_create` | Create a new custom rule | Write | Master Administrator |
| `cloud_posture_custom_rule_update` | Update an existing custom rule | Write | Master Administrator |
| `cloud_posture_custom_rule_delete` | Permanently delete a custom rule | Write | Master Administrator |
| `cloud_posture_custom_rule_test` | Test a rule configuration against an account or mock data | Write | Master Administrator |

## Custom Rule Structure

### Required Fields for Creating Rules

| Field | Description | Example Values |
|-------|-------------|----------------|
| `name` | Display name for the rule | "Require S3 bucket encryption" |
| `description` | Detailed explanation | "Ensures all S3 buckets have encryption enabled" |
| `categories` | Compliance categories | security, cost-optimisation, reliability, performance-efficiency, operational-excellence, sustainability |
| `riskLevel` | Severity level | LOW, MEDIUM, HIGH, VERY_HIGH, EXTREME |
| `provider` | Cloud provider | aws, azure, gcp, oci, alibabaCloud |
| `enabled` | Whether rule is active | true, false |
| `service` | Cloud service | S3, EC2, IAM, etc. |
| `resourceType` | Resource to evaluate | AWS::S3::Bucket, AWS::EC2::Instance, etc. |
| `attributes` | Data to extract | Array of {name, path, required} |
| `eventRules` | Evaluation conditions | Array of {conditions, description} |

### Optional Fields

| Field | Description |
|-------|-------------|
| `slug` | URL-friendly identifier (auto-generated if omitted) |
| `remediationNote` | Steps to fix issues |
| `resolutionReferenceLink` | URL to documentation |

## Common Workflows

### List and Review Custom Rules
1. Use `cloud_posture_custom_rules_list` to get all rules
2. Review enabled/disabled status
3. Identify rules by provider and service
4. Get details for specific rules of interest

### Create a New Custom Rule
1. Define the rule requirements with the user
2. Identify the target provider, service, and resource type
3. Define attributes to extract from resources
4. Define event rules with conditions
5. **Test the rule** using `cloud_posture_custom_rule_test` with mock data or a test account
6. Review test results with the user
7. **Get user confirmation** before creating
8. Create the rule using `cloud_posture_custom_rule_create`
9. Verify the rule was created successfully

### Update an Existing Rule
1. Get current rule configuration with `cloud_posture_custom_rule_get`
2. Identify changes needed
3. **Test updated configuration** before applying
4. **Get user confirmation** for changes
5. Update the rule using `cloud_posture_custom_rule_update`
6. Verify changes were applied

### Test Rule Configuration
1. Define rule configuration (attributes and eventRules)
2. Choose test method:
   - Provide `accountId` to test against real cloud resources
   - Provide `resource` object with mock data for isolated testing
3. Execute `cloud_posture_custom_rule_test`
4. Review results for expected behavior
5. Iterate on rule configuration if needed

### Delete a Custom Rule
1. Get rule details to confirm deletion target
2. **Warn user** that deletion is permanent
3. **Get explicit confirmation**
4. Delete using `cloud_posture_custom_rule_delete`
5. Confirm deletion was successful

## Output Format

### Custom Rule List
```
## Custom Rules Summary

**Total Rules**: [count]
**Enabled**: [count] | **Disabled**: [count]

### Rules by Provider
| Provider | Count |
|----------|-------|
| AWS | [count] |
| Azure | [count] |
| GCP | [count] |

### Rule List
| Name | Rule ID | Provider | Service | Risk Level | Status |
|------|---------|----------|---------|------------|--------|
| [name] | [id] | [provider] | [service] | [risk] | Enabled/Disabled |
```

### Custom Rule Details
```
## Custom Rule: [Name]

**Rule ID**: [id]
**Status**: Enabled/Disabled
**Risk Level**: [EXTREME/VERY_HIGH/HIGH/MEDIUM/LOW]

### Target
- **Provider**: [aws/azure/gcp/oci/alibabaCloud]
- **Service**: [service]
- **Resource Type**: [resourceType]

### Categories
- [category1]
- [category2]

### Description
[description]

### Attributes
| Name | Path | Required |
|------|------|----------|
| [name] | [JSONPath] | Yes/No |

### Event Rules
[conditions and logic]

### Remediation
[remediationNote or "Not specified"]

### Reference
[resolutionReferenceLink or "Not specified"]
```

### Test Results
```
## Rule Test Results

**Configuration**: [Valid/Invalid]
**Test Method**: Account [id] / Mock Resource

### Results Summary
- **Resources Evaluated**: [count]
- **Passed**: [count]
- **Failed**: [count]

### Findings
| Resource | Status | Details |
|----------|--------|---------|
| [resource] | Pass/Fail | [reason] |
```

### Write Operation Confirmation
```
## Action Required: [Create/Update/Delete] Custom Rule

**Operation**: [Description]
**Rule**: [name or id]

### Details
[Configuration summary or changes]

### Impact
- This rule will be [created/modified/permanently deleted]
- [Additional impact notes]

**Do you want to proceed? (yes/no)**
```

## Example Rule Configurations

### S3 Bucket Encryption Check (AWS)
```json
{
  "name": "Require S3 Server-Side Encryption",
  "description": "Ensures all S3 buckets have server-side encryption enabled",
  "categories": ["security"],
  "riskLevel": "HIGH",
  "provider": "aws",
  "enabled": true,
  "service": "S3",
  "resourceType": "AWS::S3::Bucket",
  "attributes": [
    {
      "name": "BucketEncryption",
      "path": "$.BucketEncryption",
      "required": false
    }
  ],
  "eventRules": [
    {
      "conditions": {
        "all": [
          {
            "fact": "BucketEncryption",
            "operator": "equal",
            "value": null
          }
        ]
      },
      "description": "S3 bucket does not have encryption enabled"
    }
  ],
  "remediationNote": "Enable server-side encryption in the S3 bucket settings"
}
```

## Security Considerations

- **Master Administrator role required** for all write operations
- **Test rules before deployment** to avoid false positives in production
- Enabled custom rules immediately affect all connected cloud accounts
- **Deletion is permanent** - rules cannot be recovered
- Custom rules complement but do not replace built-in compliance checks
- Consider rule performance impact when evaluating large numbers of resources
- Document custom rules for audit and compliance purposes
- Coordinate rule changes with security and compliance teams
