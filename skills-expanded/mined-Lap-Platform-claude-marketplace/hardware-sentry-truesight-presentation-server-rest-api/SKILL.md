---
name: hardware-sentry-truesight-presentation-server-rest-api
description: "Hardware Sentry TrueSight Presentation Server REST API skill. Use when working with Hardware Sentry TrueSight Presentation Server REST for hardware. Covers 23 endpoints."
version: 1.0.0
generator: lapsh
---

# Hardware Sentry TrueSight Presentation Server REST API
API version: 11.1.00

## Auth
ApiKey Cookie in header

## Base URL
/tsws/10.0/api/

## Setup
1. Set your API key in the appropriate header
2. GET /hardware/applications -- verify access
3. POST /hardware/actions/{deviceId}/collect-now -- create first collect-now

## Endpoints

23 endpoints across 1 groups. See references/api-spec.lap for full details.

### hardware
| Method | Path | Description |
|--------|------|-------------|
| POST | /hardware/actions/{deviceId}/collect-now | Triggers a new collect on a specific device. |
| POST | /hardware/actions/{deviceId}/rediscover | Triggers a new discovery on a specific device. |
| POST | /hardware/actions/{deviceId}/reinitialize | Sends a 'Reinitialize KM' command. |
| POST | /hardware/actions/{deviceId}/remove | Removes a specific instance from the monitoring environment. |
| POST | /hardware/actions/{deviceId}/reset-error-count | Resets the Error Count parameter. |
| GET | /hardware/applications | Gets summarized information about all monitored applications. |
| GET | /hardware/applications/{applicationId} | Gets detailed information for a specific application. |
| GET | /hardware/device-monitors/{deviceId} | Gets the Monitors for a specific device. |
| GET | /hardware/devices | Gets summarized information about all monitored devices. |
| GET | /hardware/devices-summary | Gets overall information for all devices. |
| GET | /hardware/devices/{deviceId} | Gets detailed information about a specific device. |
| GET | /hardware/devices/{deviceId}/agent | Gets detailed information about an Agent. |
| GET | /hardware/devices/{deviceId}/agent-devices | Gets a list of all the devices monitored by an Agent. |
| GET | /hardware/devices/{deviceId}/parameter-history | Gets data history for a parameter of a specific device over a given period. |
| GET | /hardware/energy-usage/{deviceId} | Gets the energy usage for a specific device and a given period. |
| GET | /hardware/groups | Gets all group summaries. |
| GET | /hardware/groups/{groupId} | Gets detailed information about a specific group. |
| PUT | /hardware/groups/{groupId} | Updates the values of the energy footprint parameter for a specific group. |
| GET | /hardware/heating-margin-devices | Gets the heating margin values for each monitored device, when available. |
| GET | /hardware/history | Gets historical data for a specific group, application or service. |
| GET | /hardware/search-devices | Searches devices by name, model, manufacturer or serial number. |
| GET | /hardware/services | Gets summarized information about all monitored services. |
| GET | /hardware/services/{serviceId} | Gets detailed information about a specific service. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a collect-now?" -> POST /hardware/actions/{deviceId}/collect-now
- "Create a rediscover?" -> POST /hardware/actions/{deviceId}/rediscover
- "Create a reinitialize?" -> POST /hardware/actions/{deviceId}/reinitialize
- "Create a remove?" -> POST /hardware/actions/{deviceId}/remove
- "Create a reset-error-count?" -> POST /hardware/actions/{deviceId}/reset-error-count
- "List all applications?" -> GET /hardware/applications
- "Get application details?" -> GET /hardware/applications/{applicationId}
- "Get device-monitor details?" -> GET /hardware/device-monitors/{deviceId}
- "List all devices?" -> GET /hardware/devices
- "List all devices-summary?" -> GET /hardware/devices-summary
- "Get device details?" -> GET /hardware/devices/{deviceId}
- "List all agent?" -> GET /hardware/devices/{deviceId}/agent
- "List all agent-devices?" -> GET /hardware/devices/{deviceId}/agent-devices
- "List all parameter-history?" -> GET /hardware/devices/{deviceId}/parameter-history
- "Get energy-usage details?" -> GET /hardware/energy-usage/{deviceId}
- "List all groups?" -> GET /hardware/groups
- "Get group details?" -> GET /hardware/groups/{groupId}
- "Update a group?" -> PUT /hardware/groups/{groupId}
- "List all heating-margin-devices?" -> GET /hardware/heating-margin-devices
- "List all history?" -> GET /hardware/history
- "List all search-devices?" -> GET /hardware/search-devices
- "List all services?" -> GET /hardware/services
- "Get service details?" -> GET /hardware/services/{serviceId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
