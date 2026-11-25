---
name: marketing-cloud-rest-api
description: "Marketing Cloud REST API skill. Use when working with Marketing Cloud REST for asset, hub, messaging. Covers 29 endpoints."
version: 1.0.0
generator: lapsh
---

# Marketing Cloud REST API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
https://www.exacttargetapis.com

## Setup
1. No auth setup needed
2. GET /messaging/v1/email/definitions/ -- verify access
3. POST /asset/v1/content/assets -- create first assets

## Endpoints

29 endpoints across 3 groups. See references/api-spec.lap for full details.

### asset
| Method | Path | Description |
|--------|------|-------------|
| GET | /asset/v1/content/assets/{id} | getAssetById |
| PATCH | /asset/v1/content/assets/{id} | partiallyUpdateAssetById |
| DELETE | /asset/v1/content/assets/{id} | deleteAssetById |
| POST | /asset/v1/content/assets | createAsset |

### hub
| Method | Path | Description |
|--------|------|-------------|
| POST | /hub/v1/campaigns | createCampaign |
| GET | /hub/v1/campaigns/{id} | getCampaignById |
| DELETE | /hub/v1/campaigns/{id} | deleteCampaignById |

### messaging
| Method | Path | Description |
|--------|------|-------------|
| POST | /messaging/v1/email/definitions/ | createEmailDefinition |
| GET | /messaging/v1/email/definitions/ | getEmailDefinitions |
| DELETE | /messaging/v1/email/definitions/{definitionKey} | deleteEmailDefinition |
| PATCH | /messaging/v1/email/definitions/{definitionKey} | partiallyUpdateEmailDefinition |
| GET | /messaging/v1/email/definitions/{definitionKey} | getEmailDefinition |
| GET | /messaging/v1/email/definitions/{definitionKey}/queue | getQueueMetricsForEmailDefinition |
| DELETE | /messaging/v1/email/definitions/{definitionKey}/queue | deleteQueuedMessagesForEmailDefinition |
| POST | /messaging/v1/email/messages/ | sendEmailToMultipleRecipients |
| GET | /messaging/v1/email/messages/ | getEmailsNotSentToRecipients |
| GET | /messaging/v1/email/messages/{messageKey} | getEmailSendStatusForRecipient |
| POST | /messaging/v1/email/messages/{messageKey} | sendEmailToSingleRecipient |
| GET | /messaging/v1/sms/definitions/{definitionKey} | getSmsDefinition |
| PATCH | /messaging/v1/sms/definitions/{definitionKey} | partiallyUpdateSmsDefinition |
| DELETE | /messaging/v1/sms/definitions/{definitionKey} | deleteSmsDefinition |
| POST | /messaging/v1/sms/definitions | createSmsDefinition |
| GET | /messaging/v1/sms/definitions | getSmsDefinitions |
| GET | /messaging/v1/sms/definitions/{definitionKey}/queue | getQueueMetricsForSmsDefinition |
| DELETE | /messaging/v1/sms/definitions/{definitionKey}/queue | deleteQueuedMessagesForSmsDefinition |
| POST | /messaging/v1/sms/messages/ | sendSmsToMultipleRecipients |
| GET | /messaging/v1/sms/messages/ | getSMSsNotSentToRecipients |
| POST | /messaging/v1/sms/messages/{messageKey} | sendSmsToSingleRecipient |
| GET | /messaging/v1/sms/messages/{messageKey} | getSmsSendStatusForRecipient |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get asset details?" -> GET /asset/v1/content/assets/{id}
- "Partially update a asset?" -> PATCH /asset/v1/content/assets/{id}
- "Delete a asset?" -> DELETE /asset/v1/content/assets/{id}
- "Create a asset?" -> POST /asset/v1/content/assets
- "Create a campaign?" -> POST /hub/v1/campaigns
- "Get campaign details?" -> GET /hub/v1/campaigns/{id}
- "Delete a campaign?" -> DELETE /hub/v1/campaigns/{id}
- "Create a definition?" -> POST /messaging/v1/email/definitions/
- "List all definitions?" -> GET /messaging/v1/email/definitions/
- "Delete a definition?" -> DELETE /messaging/v1/email/definitions/{definitionKey}
- "Partially update a definition?" -> PATCH /messaging/v1/email/definitions/{definitionKey}
- "Get definition details?" -> GET /messaging/v1/email/definitions/{definitionKey}
- "List all queue?" -> GET /messaging/v1/email/definitions/{definitionKey}/queue
- "Create a message?" -> POST /messaging/v1/email/messages/
- "List all messages?" -> GET /messaging/v1/email/messages/
- "Get message details?" -> GET /messaging/v1/email/messages/{messageKey}
- "Get definition details?" -> GET /messaging/v1/sms/definitions/{definitionKey}
- "Partially update a definition?" -> PATCH /messaging/v1/sms/definitions/{definitionKey}
- "Delete a definition?" -> DELETE /messaging/v1/sms/definitions/{definitionKey}
- "Create a definition?" -> POST /messaging/v1/sms/definitions
- "List all definitions?" -> GET /messaging/v1/sms/definitions
- "List all queue?" -> GET /messaging/v1/sms/definitions/{definitionKey}/queue
- "Create a message?" -> POST /messaging/v1/sms/messages/
- "List all messages?" -> GET /messaging/v1/sms/messages/
- "Get message details?" -> GET /messaging/v1/sms/messages/{messageKey}

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
