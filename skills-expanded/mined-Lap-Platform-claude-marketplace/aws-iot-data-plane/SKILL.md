---
name: aws-iot-data-plane
description: "AWS IoT Data Plane API skill. Use when working with AWS IoT Data Plane for things, retainedMessage, api. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS IoT Data Plane
API version: 2015-05-28

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /retainedMessage -- verify access
3. POST /topics/{topic} -- create first topics

## Endpoints

7 endpoints across 4 groups. See references/api-spec.lap for full details.

### things
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /things/{thingName}/shadow | Deletes the shadow for the specified thing. Requires permission to access the DeleteThingShadow action. For more information, see DeleteThingShadow in the IoT Developer Guide. |
| GET | /things/{thingName}/shadow | Gets the shadow for the specified thing. Requires permission to access the GetThingShadow action. For more information, see GetThingShadow in the IoT Developer Guide. |
| POST | /things/{thingName}/shadow | Updates the shadow for the specified thing. Requires permission to access the UpdateThingShadow action. For more information, see UpdateThingShadow in the IoT Developer Guide. |

### retainedMessage
| Method | Path | Description |
|--------|------|-------------|
| GET | /retainedMessage/{topic} | Gets the details of a single retained message for the specified topic. This action returns the message payload of the retained message, which can incur messaging costs. To list only the topic names of the retained messages, call ListRetainedMessages. Requires permission to access the GetRetainedMessage action. For more information about messaging costs, see Amazon Web Services IoT Core pricing - Messaging. |
| GET | /retainedMessage | Lists summary information about the retained messages stored for the account. This action returns only the topic names of the retained messages. It doesn't return any message payloads. Although this action doesn't return a message payload, it can still incur messaging costs. To get the message payload of a retained message, call GetRetainedMessage with the topic name of the retained message. Requires permission to access the ListRetainedMessages action. For more information about messaging costs, see Amazon Web Services IoT Core pricing - Messaging. |

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/things/shadow/ListNamedShadowsForThing/{thingName} | Lists the shadows for the specified thing. Requires permission to access the ListNamedShadowsForThing action. |

### topics
| Method | Path | Description |
|--------|------|-------------|
| POST | /topics/{topic} | Publishes an MQTT message. Requires permission to access the Publish action. For more information about MQTT messages, see MQTT Protocol in the IoT Developer Guide. For more information about messaging costs, see Amazon Web Services IoT Core pricing - Messaging. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get retainedMessage details?" -> GET /retainedMessage/{topic}
- "List all shadow?" -> GET /things/{thingName}/shadow
- "Get ListNamedShadowsForThing details?" -> GET /api/things/shadow/ListNamedShadowsForThing/{thingName}
- "List all retainedMessage?" -> GET /retainedMessage
- "Create a shadow?" -> POST /things/{thingName}/shadow
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
