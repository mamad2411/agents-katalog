---
name: amazon-data-lifecycle-manager
description: "Amazon Data Lifecycle Manager API skill. Use when working with Amazon Data Lifecycle Manager for policies, tags. Covers 8 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Data Lifecycle Manager
API version: 2018-01-12

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /policies -- verify access
3. POST /policies -- create first policies

## Endpoints

8 endpoints across 2 groups. See references/api-spec.lap for full details.

### policies
| Method | Path | Description |
|--------|------|-------------|
| POST | /policies | Creates an Amazon Data Lifecycle Manager lifecycle policy. Amazon Data Lifecycle Manager supports the following policy types:   Custom EBS snapshot policy   Custom EBS-backed AMI policy   Cross-account copy event policy   Default policy for EBS snapshots   Default policy for EBS-backed AMIs   For more information, see  Default policies vs custom policies.  If you create a default policy, you can specify the request parameters either in the request body, or in the PolicyDetails request structure, but not both. |
| DELETE | /policies/{policyId} | Deletes the specified lifecycle policy and halts the automated operations that the policy specified. For more information about deleting a policy, see Delete lifecycle policies. |
| GET | /policies | Gets summary information about all or the specified data lifecycle policies. To get complete information about a policy, use GetLifecyclePolicy. |
| GET | /policies/{policyId} | Gets detailed information about the specified lifecycle policy. |
| PATCH | /policies/{policyId} | Updates the specified lifecycle policy. For more information about updating a policy, see Modify lifecycle policies. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Lists the tags for the specified resource. |
| POST | /tags/{resourceArn} | Adds the specified tags to the specified resource. |
| DELETE | /tags/{resourceArn} | Removes the specified tags from the specified resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a policy?" -> POST /policies
- "Delete a policy?" -> DELETE /policies/{policyId}
- "List all policies?" -> GET /policies
- "Get policy details?" -> GET /policies/{policyId}
- "Get tag details?" -> GET /tags/{resourceArn}
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Partially update a policy?" -> PATCH /policies/{policyId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
