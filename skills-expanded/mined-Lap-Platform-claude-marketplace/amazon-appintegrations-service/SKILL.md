---
name: amazon-appintegrations-service
description: "Amazon AppIntegrations Service API skill. Use when working with Amazon AppIntegrations Service for applications, dataIntegrations, eventIntegrations. Covers 23 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon AppIntegrations Service
API version: 2020-07-29

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /applications -- verify access
3. POST /applications -- create first applications

## Endpoints

23 endpoints across 4 groups. See references/api-spec.lap for full details.

### applications
| Method | Path | Description |
|--------|------|-------------|
| POST | /applications | Creates and persists an Application resource. |
| DELETE | /applications/{ApplicationIdentifier} | Deletes the Application. Only Applications that don't have any Application Associations can be deleted. |
| GET | /applications/{ApplicationIdentifier} | Get an Application resource. |
| GET | /applications/{ApplicationIdentifier}/associations | Returns a paginated list of application associations for an application. |
| GET | /applications | Lists applications in the account. |
| PATCH | /applications/{ApplicationIdentifier} | Updates and persists an Application resource. |

### dataIntegrations
| Method | Path | Description |
|--------|------|-------------|
| POST | /dataIntegrations | Creates and persists a DataIntegration resource.  You cannot create a DataIntegration association for a DataIntegration that has been previously associated. Use a different DataIntegration, or recreate the DataIntegration using the CreateDataIntegration API. |
| POST | /dataIntegrations/{Identifier}/associations | Creates and persists a DataIntegrationAssociation resource. |
| DELETE | /dataIntegrations/{Identifier} | Deletes the DataIntegration. Only DataIntegrations that don't have any DataIntegrationAssociations can be deleted. Deleting a DataIntegration also deletes the underlying Amazon AppFlow flow and service linked role.   You cannot create a DataIntegration association for a DataIntegration that has been previously associated. Use a different DataIntegration, or recreate the DataIntegration using the CreateDataIntegration API. |
| GET | /dataIntegrations/{Identifier} | Returns information about the DataIntegration.  You cannot create a DataIntegration association for a DataIntegration that has been previously associated. Use a different DataIntegration, or recreate the DataIntegration using the CreateDataIntegration API. |
| GET | /dataIntegrations/{Identifier}/associations | Returns a paginated list of DataIntegration associations in the account.  You cannot create a DataIntegration association for a DataIntegration that has been previously associated. Use a different DataIntegration, or recreate the DataIntegration using the CreateDataIntegration API. |
| GET | /dataIntegrations | Returns a paginated list of DataIntegrations in the account.  You cannot create a DataIntegration association for a DataIntegration that has been previously associated. Use a different DataIntegration, or recreate the DataIntegration using the CreateDataIntegration API. |
| PATCH | /dataIntegrations/{Identifier} | Updates the description of a DataIntegration.  You cannot create a DataIntegration association for a DataIntegration that has been previously associated. Use a different DataIntegration, or recreate the DataIntegration using the CreateDataIntegration API. |
| PATCH | /dataIntegrations/{Identifier}/associations/{DataIntegrationAssociationIdentifier} | Updates and persists a DataIntegrationAssociation resource.   Updating a DataIntegrationAssociation with ExecutionConfiguration will rerun the on-demand job. |

### eventIntegrations
| Method | Path | Description |
|--------|------|-------------|
| POST | /eventIntegrations | Creates an EventIntegration, given a specified name, description, and a reference to an Amazon EventBridge bus in your account and a partner event source that pushes events to that bus. No objects are created in the your account, only metadata that is persisted on the EventIntegration control plane. |
| DELETE | /eventIntegrations/{Name} | Deletes the specified existing event integration. If the event integration is associated with clients, the request is rejected. |
| GET | /eventIntegrations/{Name} | Returns information about the event integration. |
| GET | /eventIntegrations/{Name}/associations | Returns a paginated list of event integration associations in the account. |
| GET | /eventIntegrations | Returns a paginated list of event integrations in the account. |
| PATCH | /eventIntegrations/{Name} | Updates the description of an event integration. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Lists the tags for the specified resource. |
| POST | /tags/{resourceArn} | Adds the specified tags to the specified resource. |
| DELETE | /tags/{resourceArn} | Removes the specified tags from the specified resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a application?" -> POST /applications
- "Create a dataIntegration?" -> POST /dataIntegrations
- "Create a association?" -> POST /dataIntegrations/{Identifier}/associations
- "Create a eventIntegration?" -> POST /eventIntegrations
- "Delete a application?" -> DELETE /applications/{ApplicationIdentifier}
- "Delete a dataIntegration?" -> DELETE /dataIntegrations/{Identifier}
- "Delete a eventIntegration?" -> DELETE /eventIntegrations/{Name}
- "Get application details?" -> GET /applications/{ApplicationIdentifier}
- "Get dataIntegration details?" -> GET /dataIntegrations/{Identifier}
- "Get eventIntegration details?" -> GET /eventIntegrations/{Name}
- "List all associations?" -> GET /applications/{ApplicationIdentifier}/associations
- "List all applications?" -> GET /applications
- "List all associations?" -> GET /dataIntegrations/{Identifier}/associations
- "List all dataIntegrations?" -> GET /dataIntegrations
- "List all associations?" -> GET /eventIntegrations/{Name}/associations
- "List all eventIntegrations?" -> GET /eventIntegrations
- "Get tag details?" -> GET /tags/{resourceArn}
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Partially update a application?" -> PATCH /applications/{ApplicationIdentifier}
- "Partially update a dataIntegration?" -> PATCH /dataIntegrations/{Identifier}
- "Partially update a association?" -> PATCH /dataIntegrations/{Identifier}/associations/{DataIntegrationAssociationIdentifier}
- "Partially update a eventIntegration?" -> PATCH /eventIntegrations/{Name}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
