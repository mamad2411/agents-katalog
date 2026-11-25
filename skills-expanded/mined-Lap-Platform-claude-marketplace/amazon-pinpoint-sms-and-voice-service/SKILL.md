---
name: amazon-pinpoint-sms-and-voice-service
description: "Amazon Pinpoint SMS and Voice Service API skill. Use when working with Amazon Pinpoint SMS and Voice Service for sms-voice. Covers 8 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Pinpoint SMS and Voice Service
API version: 2018-09-05

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /v1/sms-voice/configuration-sets -- verify access
3. POST /v1/sms-voice/configuration-sets -- create first configuration-sets

## Endpoints

8 endpoints across 1 groups. See references/api-spec.lap for full details.

### sms-voice
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/sms-voice/configuration-sets | Create a new configuration set. After you create the configuration set, you can add one or more event destinations to it. |
| POST | /v1/sms-voice/configuration-sets/{ConfigurationSetName}/event-destinations | Create a new event destination in a configuration set. |
| DELETE | /v1/sms-voice/configuration-sets/{ConfigurationSetName} | Deletes an existing configuration set. |
| DELETE | /v1/sms-voice/configuration-sets/{ConfigurationSetName}/event-destinations/{EventDestinationName} | Deletes an event destination in a configuration set. |
| GET | /v1/sms-voice/configuration-sets/{ConfigurationSetName}/event-destinations | Obtain information about an event destination, including the types of events it reports, the Amazon Resource Name (ARN) of the destination, and the name of the event destination. |
| GET | /v1/sms-voice/configuration-sets | List all of the configuration sets associated with your Amazon Pinpoint account in the current region. |
| POST | /v1/sms-voice/voice/message | Create a new voice message and send it to a recipient's phone number. |
| PUT | /v1/sms-voice/configuration-sets/{ConfigurationSetName}/event-destinations/{EventDestinationName} | Update an event destination in a configuration set. An event destination is a location that you publish information about your voice calls to. For example, you can log an event to an Amazon CloudWatch destination when a call fails. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a configuration-set?" -> POST /v1/sms-voice/configuration-sets
- "Create a event-destination?" -> POST /v1/sms-voice/configuration-sets/{ConfigurationSetName}/event-destinations
- "Delete a configuration-set?" -> DELETE /v1/sms-voice/configuration-sets/{ConfigurationSetName}
- "Delete a event-destination?" -> DELETE /v1/sms-voice/configuration-sets/{ConfigurationSetName}/event-destinations/{EventDestinationName}
- "List all event-destinations?" -> GET /v1/sms-voice/configuration-sets/{ConfigurationSetName}/event-destinations
- "List all configuration-sets?" -> GET /v1/sms-voice/configuration-sets
- "Create a message?" -> POST /v1/sms-voice/voice/message
- "Update a event-destination?" -> PUT /v1/sms-voice/configuration-sets/{ConfigurationSetName}/event-destinations/{EventDestinationName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
