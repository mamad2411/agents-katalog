---
name: twilio-accounts
description: "Twilio - Accounts API skill. Use when working with Twilio - Accounts for AuthTokens, Consents, Contacts. Covers 20 endpoints."
version: 1.0.0
generator: lapsh
---

# Twilio - Accounts
API version: 1.0.0

## Auth
Bearer basic

## Base URL
https://accounts.twilio.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v1/Credentials/AWS -- verify access
3. POST /v1/AuthTokens/Promote -- create first Promote

## Endpoints

20 endpoints across 6 groups. See references/api-spec.lap for full details.

### AuthTokens
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/AuthTokens/Promote | Promote the secondary Auth Token to primary. After promoting the new token, all requests to Twilio using your old primary Auth Token will result in an error. |
| POST | /v1/AuthTokens/Secondary | Create a new secondary Auth Token |
| DELETE | /v1/AuthTokens/Secondary | Delete the secondary Auth Token from your account |

### Consents
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/Consents/Bulk |  |

### Contacts
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/Contacts/Bulk |  |

### Credentials
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/Credentials/AWS | Retrieves a collection of AWS Credentials belonging to the account used to make the request |
| POST | /v1/Credentials/AWS | Create a new AWS Credential |
| GET | /v1/Credentials/AWS/{Sid} | Fetch the AWS credentials specified by the provided Credential Sid |
| POST | /v1/Credentials/AWS/{Sid} | Modify the properties of a given Account |
| DELETE | /v1/Credentials/AWS/{Sid} | Delete a Credential from your account |
| GET | /v1/Credentials/PublicKeys | Retrieves a collection of Public Key Credentials belonging to the account used to make the request |
| POST | /v1/Credentials/PublicKeys | Create a new Public Key Credential |
| GET | /v1/Credentials/PublicKeys/{Sid} | Fetch the public key specified by the provided Credential Sid |
| POST | /v1/Credentials/PublicKeys/{Sid} | Modify the properties of a given Account |
| DELETE | /v1/Credentials/PublicKeys/{Sid} | Delete a Credential from your account |

### Messaging
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /v1/Messaging/GeoPermissions |  |
| GET | /v1/Messaging/GeoPermissions |  |

### SafeList
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/SafeList/Numbers | Add a new phone number or phone number 1k prefix to SafeList. |
| GET | /v1/SafeList/Numbers | Check if a phone number or phone number 1k prefix exists in SafeList. |
| DELETE | /v1/SafeList/Numbers | Remove a phone number or phone number 1k prefix from SafeList. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a Promote?" -> POST /v1/AuthTokens/Promote
- "Create a Bulk?" -> POST /v1/Consents/Bulk
- "Create a Bulk?" -> POST /v1/Contacts/Bulk
- "List all AWS?" -> GET /v1/Credentials/AWS
- "Create a AWS?" -> POST /v1/Credentials/AWS
- "Get AWS details?" -> GET /v1/Credentials/AWS/{Sid}
- "Delete a AWS?" -> DELETE /v1/Credentials/AWS/{Sid}
- "List all PublicKeys?" -> GET /v1/Credentials/PublicKeys
- "Create a PublicKey?" -> POST /v1/Credentials/PublicKeys
- "Get PublicKey details?" -> GET /v1/Credentials/PublicKeys/{Sid}
- "Delete a PublicKey?" -> DELETE /v1/Credentials/PublicKeys/{Sid}
- "List all GeoPermissions?" -> GET /v1/Messaging/GeoPermissions
- "Create a Number?" -> POST /v1/SafeList/Numbers
- "List all Numbers?" -> GET /v1/SafeList/Numbers
- "Create a Secondary?" -> POST /v1/AuthTokens/Secondary
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
