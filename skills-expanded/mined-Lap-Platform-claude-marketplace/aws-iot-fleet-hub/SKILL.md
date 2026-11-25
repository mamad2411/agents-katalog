---
name: aws-iot-fleet-hub
description: "AWS IoT Fleet Hub API skill. Use when working with AWS IoT Fleet Hub for applications, tags. Covers 8 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS IoT Fleet Hub
API version: 2020-11-03

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /applications -- verify access
3. POST /applications -- create first applications

## Endpoints

8 endpoints across 2 groups. See references/api-spec.lap for full details.

### applications
| Method | Path | Description |
|--------|------|-------------|
| POST | /applications | Creates a Fleet Hub for IoT Device Management web application. When creating a Fleet Hub application, you must create an organization instance of IAM Identity Center if you don't already have one. The Fleet Hub application you create must also be in the same Amazon Web Services Region of the organization instance of IAM Identity Center. For more information see Enabling IAM Identity Center and Organization instances of IAM Identity Center. |
| DELETE | /applications/{applicationId} | Deletes a Fleet Hub for IoT Device Management web application. |
| GET | /applications/{applicationId} | Gets information about a Fleet Hub for IoT Device Management web application. |
| GET | /applications | Gets a list of Fleet Hub for IoT Device Management web applications for the current account. |
| PATCH | /applications/{applicationId} | Updates information about a Fleet Hub for IoT Device Management web application. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Lists the tags for the specified resource. |
| POST | /tags/{resourceArn} | Adds to or modifies the tags of the specified resource. Tags are metadata which can be used to manage a resource. |
| DELETE | /tags/{resourceArn} | Removes the specified tags (metadata) from the resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a application?" -> POST /applications
- "Delete a application?" -> DELETE /applications/{applicationId}
- "Get application details?" -> GET /applications/{applicationId}
- "List all applications?" -> GET /applications
- "Get tag details?" -> GET /tags/{resourceArn}
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Partially update a application?" -> PATCH /applications/{applicationId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
