---
name: aws-iot-1-click-projects-service
description: "AWS IoT 1-Click Projects Service API skill. Use when working with AWS IoT 1-Click Projects Service for projects, tags. Covers 16 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS IoT 1-Click Projects Service
API version: 2018-05-14

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /projects -- verify access
3. POST /projects/{projectName}/placements -- create first placements

## Endpoints

16 endpoints across 2 groups. See references/api-spec.lap for full details.

### projects
| Method | Path | Description |
|--------|------|-------------|
| PUT | /projects/{projectName}/placements/{placementName}/devices/{deviceTemplateName} | Associates a physical device with a placement. |
| POST | /projects/{projectName}/placements | Creates an empty placement. |
| POST | /projects | Creates an empty project with a placement template. A project contains zero or more placements that adhere to the placement template defined in the project. |
| DELETE | /projects/{projectName}/placements/{placementName} | Deletes a placement. To delete a placement, it must not have any devices associated with it.  When you delete a placement, all associated data becomes irretrievable. |
| DELETE | /projects/{projectName} | Deletes a project. To delete a project, it must not have any placements associated with it.  When you delete a project, all associated data becomes irretrievable. |
| GET | /projects/{projectName}/placements/{placementName} | Describes a placement in a project. |
| GET | /projects/{projectName} | Returns an object describing a project. |
| DELETE | /projects/{projectName}/placements/{placementName}/devices/{deviceTemplateName} | Removes a physical device from a placement. |
| GET | /projects/{projectName}/placements/{placementName}/devices | Returns an object enumerating the devices in a placement. |
| GET | /projects/{projectName}/placements | Lists the placement(s) of a project. |
| GET | /projects | Lists the AWS IoT 1-Click project(s) associated with your AWS account and region. |
| PUT | /projects/{projectName}/placements/{placementName} | Updates a placement with the given attributes. To clear an attribute, pass an empty value (i.e., ""). |
| PUT | /projects/{projectName} | Updates a project associated with your AWS account and region. With the exception of device template names, you can pass just the values that need to be updated because the update request will change only the values that are provided. To clear a value, pass the empty string (i.e., ""). |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Lists the tags (metadata key/value pairs) which you have assigned to the resource. |
| POST | /tags/{resourceArn} | Creates or modifies tags for a resource. Tags are key/value pairs (metadata) that can be used to manage a resource. For more information, see AWS Tagging Strategies. |
| DELETE | /tags/{resourceArn} | Removes one or more tags (metadata key/value pairs) from a resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Update a device?" -> PUT /projects/{projectName}/placements/{placementName}/devices/{deviceTemplateName}
- "Create a placement?" -> POST /projects/{projectName}/placements
- "Create a project?" -> POST /projects
- "Delete a placement?" -> DELETE /projects/{projectName}/placements/{placementName}
- "Delete a project?" -> DELETE /projects/{projectName}
- "Get placement details?" -> GET /projects/{projectName}/placements/{placementName}
- "Get project details?" -> GET /projects/{projectName}
- "Delete a device?" -> DELETE /projects/{projectName}/placements/{placementName}/devices/{deviceTemplateName}
- "List all devices?" -> GET /projects/{projectName}/placements/{placementName}/devices
- "List all placements?" -> GET /projects/{projectName}/placements
- "List all projects?" -> GET /projects
- "Get tag details?" -> GET /tags/{resourceArn}
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Update a placement?" -> PUT /projects/{projectName}/placements/{placementName}
- "Update a project?" -> PUT /projects/{projectName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
