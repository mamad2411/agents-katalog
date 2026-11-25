---
name: awsserverlessapplicationrepository
description: "AWSServerlessApplicationRepository API skill. Use when working with AWSServerlessApplicationRepository for applications. Covers 14 endpoints."
version: 1.0.0
generator: lapsh
---

# AWSServerlessApplicationRepository
API version: 2017-09-08

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /applications -- verify access
3. POST /applications -- create first applications

## Endpoints

14 endpoints across 1 groups. See references/api-spec.lap for full details.

### applications
| Method | Path | Description |
|--------|------|-------------|
| POST | /applications | Creates an application, optionally including an AWS SAM file to create the first application version in the same call. |
| PUT | /applications/{applicationId}/versions/{semanticVersion} | Creates an application version. |
| POST | /applications/{applicationId}/changesets | Creates an AWS CloudFormation change set for the given application. |
| POST | /applications/{applicationId}/templates | Creates an AWS CloudFormation template. |
| DELETE | /applications/{applicationId} | Deletes the specified application. |
| GET | /applications/{applicationId} | Gets the specified application. |
| GET | /applications/{applicationId}/policy | Retrieves the policy for the application. |
| GET | /applications/{applicationId}/templates/{templateId} | Gets the specified AWS CloudFormation template. |
| GET | /applications/{applicationId}/dependencies | Retrieves the list of applications nested in the containing application. |
| GET | /applications/{applicationId}/versions | Lists versions for the specified application. |
| GET | /applications | Lists applications owned by the requester. |
| PUT | /applications/{applicationId}/policy | Sets the permission policy for an application. For the list of actions supported for this operation, see |
| POST | /applications/{applicationId}/unshare | Unshares an application from an AWS Organization.This operation can be called only from the organization's master account. |
| PATCH | /applications/{applicationId} | Updates the specified application. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a application?" -> POST /applications
- "Update a version?" -> PUT /applications/{applicationId}/versions/{semanticVersion}
- "Create a changeset?" -> POST /applications/{applicationId}/changesets
- "Create a template?" -> POST /applications/{applicationId}/templates
- "Delete a application?" -> DELETE /applications/{applicationId}
- "Get application details?" -> GET /applications/{applicationId}
- "List all policy?" -> GET /applications/{applicationId}/policy
- "Get template details?" -> GET /applications/{applicationId}/templates/{templateId}
- "List all dependencies?" -> GET /applications/{applicationId}/dependencies
- "List all versions?" -> GET /applications/{applicationId}/versions
- "List all applications?" -> GET /applications
- "Create a unshare?" -> POST /applications/{applicationId}/unshare
- "Partially update a application?" -> PATCH /applications/{applicationId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
