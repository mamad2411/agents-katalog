---
name: aws-sso-oidc
description: "AWS SSO OIDC API skill. Use when working with AWS SSO OIDC for token, token?aws_iam=t, client. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS SSO OIDC
API version: 2019-06-10

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST /token -- create first token

## Endpoints

4 endpoints across 4 groups. See references/api-spec.lap for full details.

### token
| Method | Path | Description |
|--------|------|-------------|
| POST | /token | Creates and returns access and refresh tokens for clients that are authenticated using client secrets. The access token can be used to fetch short-term credentials for the assigned AWS accounts or to access application APIs using bearer authentication. |

### token?aws_iam=t
| Method | Path | Description |
|--------|------|-------------|
| POST | /token?aws_iam=t | Creates and returns access and refresh tokens for clients and applications that are authenticated using IAM entities. The access token can be used to fetch short-term credentials for the assigned Amazon Web Services accounts or to access application APIs using bearer authentication. |

### client
| Method | Path | Description |
|--------|------|-------------|
| POST | /client/register | Registers a client with IAM Identity Center. This allows clients to initiate device authorization. The output should be persisted for reuse through many authentication requests. |

### device_authorization
| Method | Path | Description |
|--------|------|-------------|
| POST | /device_authorization | Initiates device authorization by requesting a pair of verification codes from the authorization service. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a token?" -> POST /token
- "Create a token?aws_iam=t?" -> POST /token?aws_iam=t
- "Create a register?" -> POST /client/register
- "Create a device_authorization?" -> POST /device_authorization
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
