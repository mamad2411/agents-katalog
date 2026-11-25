---
name: aws-iot-1-click-devices-service
description: "AWS IoT 1-Click Devices Service API skill. Use when working with AWS IoT 1-Click Devices Service for claims, devices, tags. Covers 13 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS IoT 1-Click Devices Service
API version: 2018-05-14

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /devices -- verify access
3. POST /devices/{deviceId}/methods -- create first methods

## Endpoints

13 endpoints across 3 groups. See references/api-spec.lap for full details.

### claims
| Method | Path | Description |
|--------|------|-------------|
| PUT | /claims/{claimCode} | Adds device(s) to your account (i.e., claim one or more devices) if and only if you |

### devices
| Method | Path | Description |
|--------|------|-------------|
| GET | /devices/{deviceId} | Given a device ID, returns a DescribeDeviceResponse object describing the |
| PUT | /devices/{deviceId}/finalize-claim | Given a device ID, finalizes the claim request for the associated device. |
| GET | /devices/{deviceId}/methods | Given a device ID, returns the invokable methods associated with the device. |
| PUT | /devices/{deviceId}/initiate-claim | Given a device ID, initiates a claim request for the associated device. |
| POST | /devices/{deviceId}/methods | Given a device ID, issues a request to invoke a named device method (with possible |
| GET | /devices/{deviceId}/events | Using a device ID, returns a DeviceEventsResponse object containing an |
| GET | /devices | Lists the 1-Click compatible devices associated with your AWS account. |
| PUT | /devices/{deviceId}/unclaim | Disassociates a device from your AWS account using its device ID. |
| PUT | /devices/{deviceId}/state | Using a Boolean value (true or false), this operation |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resource-arn} | Lists the tags associated with the specified resource ARN. |
| POST | /tags/{resource-arn} | Adds or updates the tags associated with the resource ARN. See AWS IoT 1-Click Service Limits for the maximum number of tags allowed per |
| DELETE | /tags/{resource-arn} | Using tag keys, deletes the tags (key/value pairs) associated with the specified |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Update a claim?" -> PUT /claims/{claimCode}
- "Get device details?" -> GET /devices/{deviceId}
- "List all methods?" -> GET /devices/{deviceId}/methods
- "Create a method?" -> POST /devices/{deviceId}/methods
- "List all events?" -> GET /devices/{deviceId}/events
- "List all devices?" -> GET /devices
- "Get tag details?" -> GET /tags/{resource-arn}
- "Delete a tag?" -> DELETE /tags/{resource-arn}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
