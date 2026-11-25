---
name: aws-single-sign-on
description: "AWS Single Sign-On API skill. Use when working with AWS Single Sign-On for federation, assignment, logout. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Single Sign-On
API version: 2019-06-10

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /federation/credentials -- verify access
3. POST /logout -- create first logout

## Endpoints

4 endpoints across 3 groups. See references/api-spec.lap for full details.

### federation
| Method | Path | Description |
|--------|------|-------------|
| GET | /federation/credentials | Returns the STS short-term credentials for a given role name that is assigned to the user. |

### assignment
| Method | Path | Description |
|--------|------|-------------|
| GET | /assignment/roles | Lists all roles that are assigned to the user for a given AWS account. |
| GET | /assignment/accounts | Lists all AWS accounts assigned to the user. These AWS accounts are assigned by the administrator of the account. For more information, see Assign User Access in the IAM Identity Center User Guide. This operation returns a paginated response. |

### logout
| Method | Path | Description |
|--------|------|-------------|
| POST | /logout | Removes the locally stored SSO tokens from the client-side cache and sends an API call to the IAM Identity Center service to invalidate the corresponding server-side IAM Identity Center sign in session.  If a user uses IAM Identity Center to access the AWS CLI, the user’s IAM Identity Center sign in session is used to obtain an IAM session, as specified in the corresponding IAM Identity Center permission set. More specifically, IAM Identity Center assumes an IAM role in the target account on behalf of the user, and the corresponding temporary AWS credentials are returned to the client. After user logout, any existing IAM role sessions that were created by using IAM Identity Center permission sets continue based on the duration configured in the permission set. For more information, see User authentications in the IAM Identity Center User Guide. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all credentials?" -> GET /federation/credentials
- "List all roles?" -> GET /assignment/roles
- "List all accounts?" -> GET /assignment/accounts
- "Create a logout?" -> POST /logout
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
