---
name: aws-iot-events-data
description: "AWS IoT Events Data API skill. Use when working with AWS IoT Events Data for alarms, detectors, inputs. Covers 12 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS IoT Events Data
API version: 2018-10-23

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /alarms/{alarmModelName}/keyValues/ -- verify access
3. POST /alarms/acknowledge -- create first acknowledge

## Endpoints

12 endpoints across 3 groups. See references/api-spec.lap for full details.

### alarms
| Method | Path | Description |
|--------|------|-------------|
| POST | /alarms/acknowledge | Acknowledges one or more alarms. The alarms change to the ACKNOWLEDGED state after you acknowledge them. |
| POST | /alarms/disable | Disables one or more alarms. The alarms change to the DISABLED state after you disable them. |
| POST | /alarms/enable | Enables one or more alarms. The alarms change to the NORMAL state after you enable them. |
| POST | /alarms/reset | Resets one or more alarms. The alarms return to the NORMAL state after you reset them. |
| POST | /alarms/snooze | Changes one or more alarms to the snooze mode. The alarms change to the SNOOZE_DISABLED state after you set them to the snooze mode. |
| GET | /alarms/{alarmModelName}/keyValues/ | Retrieves information about an alarm. |
| GET | /alarms/{alarmModelName} | Lists one or more alarms. The operation returns only the metadata associated with each alarm. |

### detectors
| Method | Path | Description |
|--------|------|-------------|
| POST | /detectors/delete | Deletes one or more detectors that were created. When a detector is deleted, its state will be cleared and the detector will be removed from the list of detectors. The deleted detector will no longer appear if referenced in the ListDetectors API call. |
| POST | /detectors | Updates the state, variable values, and timer settings of one or more detectors (instances) of a specified detector model. |
| GET | /detectors/{detectorModelName}/keyValues/ | Returns information about the specified detector (instance). |
| GET | /detectors/{detectorModelName} | Lists detectors (the instances of a detector model). |

### inputs
| Method | Path | Description |
|--------|------|-------------|
| POST | /inputs/messages | Sends a set of messages to the IoT Events system. Each message payload is transformed into the input you specify ("inputName") and ingested into any detectors that monitor that input. If multiple messages are sent, the order in which the messages are processed isn't guaranteed. To guarantee ordering, you must send messages one at a time and wait for a successful response. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a acknowledge?" -> POST /alarms/acknowledge
- "Create a delete?" -> POST /detectors/delete
- "Create a disable?" -> POST /alarms/disable
- "Create a enable?" -> POST /alarms/enable
- "Create a message?" -> POST /inputs/messages
- "Create a reset?" -> POST /alarms/reset
- "Create a snooze?" -> POST /alarms/snooze
- "Create a detector?" -> POST /detectors
- "List all keyValues?" -> GET /alarms/{alarmModelName}/keyValues/
- "List all keyValues?" -> GET /detectors/{detectorModelName}/keyValues/
- "Get alarm details?" -> GET /alarms/{alarmModelName}
- "Get detector details?" -> GET /detectors/{detectorModelName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
