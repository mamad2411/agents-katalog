---
name: twilio-verify
description: "Twilio - Verify API skill. Use when working with Twilio - Verify for Services, Forms, SafeList. Covers 57 endpoints."
version: 1.0.0
generator: lapsh
---

# Twilio - Verify
API version: 1.0.0

## Auth
Bearer basic

## Base URL
https://verify.twilio.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v2/Services -- verify access
3. POST /v2/Services/{ServiceSid}/AccessTokens -- create first AccessTokens

## Endpoints

57 endpoints across 5 groups. See references/api-spec.lap for full details.

### Services
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/Services/{ServiceSid}/AccessTokens | Create a new enrollment Access Token for the Entity |
| GET | /v2/Services/{ServiceSid}/AccessTokens/{Sid} | Fetch an Access Token for the Entity |
| POST | /v2/Services/{ServiceSid}/RateLimits/{RateLimitSid}/Buckets | Create a new Bucket for a Rate Limit |
| GET | /v2/Services/{ServiceSid}/RateLimits/{RateLimitSid}/Buckets | Retrieve a list of all Buckets for a Rate Limit. |
| POST | /v2/Services/{ServiceSid}/RateLimits/{RateLimitSid}/Buckets/{Sid} | Update a specific Bucket. |
| GET | /v2/Services/{ServiceSid}/RateLimits/{RateLimitSid}/Buckets/{Sid} | Fetch a specific Bucket. |
| DELETE | /v2/Services/{ServiceSid}/RateLimits/{RateLimitSid}/Buckets/{Sid} | Delete a specific Bucket. |
| POST | /v2/Services/{ServiceSid}/Entities/{Identity}/Challenges | Create a new Challenge for the Factor |
| GET | /v2/Services/{ServiceSid}/Entities/{Identity}/Challenges | Retrieve a list of all Challenges for a Factor. |
| GET | /v2/Services/{ServiceSid}/Entities/{Identity}/Challenges/{Sid} | Fetch a specific Challenge. |
| POST | /v2/Services/{ServiceSid}/Entities/{Identity}/Challenges/{Sid} | Verify a specific Challenge. |
| POST | /v2/Services/{ServiceSid}/Entities | Create a new Entity for the Service |
| GET | /v2/Services/{ServiceSid}/Entities | Retrieve a list of all Entities for a Service. |
| DELETE | /v2/Services/{ServiceSid}/Entities/{Identity} | Delete a specific Entity. |
| GET | /v2/Services/{ServiceSid}/Entities/{Identity} | Fetch a specific Entity. |
| DELETE | /v2/Services/{ServiceSid}/Entities/{Identity}/Factors/{Sid} | Delete a specific Factor. |
| GET | /v2/Services/{ServiceSid}/Entities/{Identity}/Factors/{Sid} | Fetch a specific Factor. |
| POST | /v2/Services/{ServiceSid}/Entities/{Identity}/Factors/{Sid} | Update a specific Factor. This endpoint can be used to Verify a Factor if passed an `AuthPayload` param. |
| GET | /v2/Services/{ServiceSid}/Entities/{Identity}/Factors | Retrieve a list of all Factors for an Entity. |
| POST | /v2/Services/{ServiceSid}/Entities/{Identity}/Factors | Create a new Factor for the Entity |
| POST | /v2/Services/{ServiceSid}/MessagingConfigurations | Create a new MessagingConfiguration for a service. |
| GET | /v2/Services/{ServiceSid}/MessagingConfigurations | Retrieve a list of all Messaging Configurations for a Service. |
| POST | /v2/Services/{ServiceSid}/MessagingConfigurations/{Country} | Update a specific MessagingConfiguration |
| GET | /v2/Services/{ServiceSid}/MessagingConfigurations/{Country} | Fetch a specific MessagingConfiguration. |
| DELETE | /v2/Services/{ServiceSid}/MessagingConfigurations/{Country} | Delete a specific MessagingConfiguration. |
| POST | /v2/Services/{ServiceSid}/Entities/{Identity}/Challenges/{ChallengeSid}/Notifications | Create a new Notification for the corresponding Challenge |
| POST | /v2/Services/{ServiceSid}/RateLimits | Create a new Rate Limit for a Service |
| GET | /v2/Services/{ServiceSid}/RateLimits | Retrieve a list of all Rate Limits for a service. |
| POST | /v2/Services/{ServiceSid}/RateLimits/{Sid} | Update a specific Rate Limit. |
| GET | /v2/Services/{ServiceSid}/RateLimits/{Sid} | Fetch a specific Rate Limit. |
| DELETE | /v2/Services/{ServiceSid}/RateLimits/{Sid} | Delete a specific Rate Limit. |
| POST | /v2/Services | Create a new Verification Service. |
| GET | /v2/Services | Retrieve a list of all Verification Services for an account. |
| GET | /v2/Services/{Sid} | Fetch specific Verification Service Instance. |
| DELETE | /v2/Services/{Sid} | Delete a specific Verification Service Instance. |
| POST | /v2/Services/{Sid} | Update a specific Verification Service. |
| POST | /v2/Services/{ServiceSid}/Verifications | Create a new Verification using a Service |
| POST | /v2/Services/{ServiceSid}/Verifications/{Sid} | Update a Verification status |
| GET | /v2/Services/{ServiceSid}/Verifications/{Sid} | Fetch a specific Verification |
| POST | /v2/Services/{ServiceSid}/VerificationCheck | challenge a specific Verification Check. |
| POST | /v2/Services/{ServiceSid}/Webhooks | Create a new Webhook for the Service |
| GET | /v2/Services/{ServiceSid}/Webhooks | Retrieve a list of all Webhooks for a Service. |
| POST | /v2/Services/{ServiceSid}/Webhooks/{Sid} |  |
| DELETE | /v2/Services/{ServiceSid}/Webhooks/{Sid} | Delete a specific Webhook. |
| GET | /v2/Services/{ServiceSid}/Webhooks/{Sid} | Fetch a specific Webhook. |
| POST | /v2/Services/{ServiceSid}/Passkeys/VerifyFactor | Verify a Passkeys Factor |
| POST | /v2/Services/{ServiceSid}/Passkeys/Factors | Create a new Passkeys Factor for the Entity |
| POST | /v2/Services/{ServiceSid}/Passkeys/Challenges | Create a Passkeys Challenge |
| POST | /v2/Services/{ServiceSid}/Passkeys/ApproveChallenge | Approve a Passkeys Challenge |

### Forms
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/Forms/{FormType} | Fetch the forms for a specific Form Type. |

### SafeList
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/SafeList/Numbers | Add a new phone number to SafeList. |
| GET | /v2/SafeList/Numbers/{PhoneNumber} | Check if a phone number exists in SafeList. |
| DELETE | /v2/SafeList/Numbers/{PhoneNumber} | Remove a phone number from SafeList. |

### Attempts
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/Attempts | List all the verification attempts for a given Account. |
| GET | /v2/Attempts/{Sid} | Fetch a specific verification attempt. |
| GET | /v2/Attempts/Summary | Get a summary of how many attempts were made and how many were converted. |

### Templates
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/Templates | List all the available templates for a given Account. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a AccessToken?" -> POST /v2/Services/{ServiceSid}/AccessTokens
- "Get AccessToken details?" -> GET /v2/Services/{ServiceSid}/AccessTokens/{Sid}
- "Create a Bucket?" -> POST /v2/Services/{ServiceSid}/RateLimits/{RateLimitSid}/Buckets
- "List all Buckets?" -> GET /v2/Services/{ServiceSid}/RateLimits/{RateLimitSid}/Buckets
- "Get Bucket details?" -> GET /v2/Services/{ServiceSid}/RateLimits/{RateLimitSid}/Buckets/{Sid}
- "Delete a Bucket?" -> DELETE /v2/Services/{ServiceSid}/RateLimits/{RateLimitSid}/Buckets/{Sid}
- "Create a Challenge?" -> POST /v2/Services/{ServiceSid}/Entities/{Identity}/Challenges
- "List all Challenges?" -> GET /v2/Services/{ServiceSid}/Entities/{Identity}/Challenges
- "Get Challenge details?" -> GET /v2/Services/{ServiceSid}/Entities/{Identity}/Challenges/{Sid}
- "Create a Entity?" -> POST /v2/Services/{ServiceSid}/Entities
- "List all Entities?" -> GET /v2/Services/{ServiceSid}/Entities
- "Delete a Entity?" -> DELETE /v2/Services/{ServiceSid}/Entities/{Identity}
- "Get Entity details?" -> GET /v2/Services/{ServiceSid}/Entities/{Identity}
- "Delete a Factor?" -> DELETE /v2/Services/{ServiceSid}/Entities/{Identity}/Factors/{Sid}
- "Get Factor details?" -> GET /v2/Services/{ServiceSid}/Entities/{Identity}/Factors/{Sid}
- "List all Factors?" -> GET /v2/Services/{ServiceSid}/Entities/{Identity}/Factors
- "Create a Factor?" -> POST /v2/Services/{ServiceSid}/Entities/{Identity}/Factors
- "Get Form details?" -> GET /v2/Forms/{FormType}
- "Create a MessagingConfiguration?" -> POST /v2/Services/{ServiceSid}/MessagingConfigurations
- "List all MessagingConfigurations?" -> GET /v2/Services/{ServiceSid}/MessagingConfigurations
- "Get MessagingConfiguration details?" -> GET /v2/Services/{ServiceSid}/MessagingConfigurations/{Country}
- "Delete a MessagingConfiguration?" -> DELETE /v2/Services/{ServiceSid}/MessagingConfigurations/{Country}
- "Create a Notification?" -> POST /v2/Services/{ServiceSid}/Entities/{Identity}/Challenges/{ChallengeSid}/Notifications
- "Create a RateLimit?" -> POST /v2/Services/{ServiceSid}/RateLimits
- "List all RateLimits?" -> GET /v2/Services/{ServiceSid}/RateLimits
- "Get RateLimit details?" -> GET /v2/Services/{ServiceSid}/RateLimits/{Sid}
- "Delete a RateLimit?" -> DELETE /v2/Services/{ServiceSid}/RateLimits/{Sid}
- "Create a Number?" -> POST /v2/SafeList/Numbers
- "Get Number details?" -> GET /v2/SafeList/Numbers/{PhoneNumber}
- "Delete a Number?" -> DELETE /v2/SafeList/Numbers/{PhoneNumber}
- "Create a Service?" -> POST /v2/Services
- "List all Services?" -> GET /v2/Services
- "Get Service details?" -> GET /v2/Services/{Sid}
- "Delete a Service?" -> DELETE /v2/Services/{Sid}
- "Create a Verification?" -> POST /v2/Services/{ServiceSid}/Verifications
- "Get Verification details?" -> GET /v2/Services/{ServiceSid}/Verifications/{Sid}
- "List all Attempts?" -> GET /v2/Attempts
- "Get Attempt details?" -> GET /v2/Attempts/{Sid}
- "List all Summary?" -> GET /v2/Attempts/Summary
- "Create a VerificationCheck?" -> POST /v2/Services/{ServiceSid}/VerificationCheck
- "List all Templates?" -> GET /v2/Templates
- "Create a Webhook?" -> POST /v2/Services/{ServiceSid}/Webhooks
- "List all Webhooks?" -> GET /v2/Services/{ServiceSid}/Webhooks
- "Delete a Webhook?" -> DELETE /v2/Services/{ServiceSid}/Webhooks/{Sid}
- "Get Webhook details?" -> GET /v2/Services/{ServiceSid}/Webhooks/{Sid}
- "Create a VerifyFactor?" -> POST /v2/Services/{ServiceSid}/Passkeys/VerifyFactor
- "Create a Factor?" -> POST /v2/Services/{ServiceSid}/Passkeys/Factors
- "Create a Challenge?" -> POST /v2/Services/{ServiceSid}/Passkeys/Challenges
- "Create a ApproveChallenge?" -> POST /v2/Services/{ServiceSid}/Passkeys/ApproveChallenge
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
