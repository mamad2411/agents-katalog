---
name: registry-api
description: "Registry API skill. Use when working with Registry for projects. Covers 35 endpoints."
version: 1.0.0
generator: lapsh
---

# Registry API
API version: 0.0.1

## Auth
No authentication required.

## Base URL
https://apigeeregistry.googleapis.com

## Setup
1. No auth setup needed
2. GET /v1/projects/{project}/locations/{location}/apis -- verify access
3. POST /v1/projects/{project}/locations/{location}/apis -- create first apis

## Endpoints

35 endpoints across 1 groups. See references/api-spec.lap for full details.

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/projects/{project}/locations/{location}/apis | ListApis returns matching APIs. |
| POST | /v1/projects/{project}/locations/{location}/apis | CreateApi creates a specified API. |
| GET | /v1/projects/{project}/locations/{location}/apis/{api} | GetApi returns a specified API. |
| DELETE | /v1/projects/{project}/locations/{location}/apis/{api} | DeleteApi removes a specified API and all of the resources that it |
| PATCH | /v1/projects/{project}/locations/{location}/apis/{api} | UpdateApi can be used to modify a specified API. |
| GET | /v1/projects/{project}/locations/{location}/apis/{api}/deployments | ListApiDeployments returns matching deployments. |
| POST | /v1/projects/{project}/locations/{location}/apis/{api}/deployments | CreateApiDeployment creates a specified deployment. |
| GET | /v1/projects/{project}/locations/{location}/apis/{api}/deployments/{deployment} | GetApiDeployment returns a specified deployment. |
| DELETE | /v1/projects/{project}/locations/{location}/apis/{api}/deployments/{deployment} | DeleteApiDeployment removes a specified deployment, all revisions, and all |
| PATCH | /v1/projects/{project}/locations/{location}/apis/{api}/deployments/{deployment} | UpdateApiDeployment can be used to modify a specified deployment. |
| DELETE | /v1/projects/{project}/locations/{location}/apis/{api}/deployments/{deployment}:deleteRevision | DeleteApiDeploymentRevision deletes a revision of a deployment. |
| GET | /v1/projects/{project}/locations/{location}/apis/{api}/deployments/{deployment}:listRevisions | ListApiDeploymentRevisions lists all revisions of a deployment. |
| POST | /v1/projects/{project}/locations/{location}/apis/{api}/deployments/{deployment}:rollback | RollbackApiDeployment sets the current revision to a specified prior |
| POST | /v1/projects/{project}/locations/{location}/apis/{api}/deployments/{deployment}:tagRevision | TagApiDeploymentRevision adds a tag to a specified revision of a |
| GET | /v1/projects/{project}/locations/{location}/apis/{api}/versions | ListApiVersions returns matching versions. |
| POST | /v1/projects/{project}/locations/{location}/apis/{api}/versions | CreateApiVersion creates a specified version. |
| GET | /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version} | GetApiVersion returns a specified version. |
| DELETE | /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version} | DeleteApiVersion removes a specified version and all of the resources that |
| PATCH | /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version} | UpdateApiVersion can be used to modify a specified version. |
| GET | /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs | ListApiSpecs returns matching specs. |
| POST | /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs | CreateApiSpec creates a specified spec. |
| GET | /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec} | GetApiSpec returns a specified spec. |
| DELETE | /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec} | DeleteApiSpec removes a specified spec, all revisions, and all child |
| PATCH | /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec} | UpdateApiSpec can be used to modify a specified spec. |
| DELETE | /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec}:deleteRevision | DeleteApiSpecRevision deletes a revision of a spec. |
| GET | /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec}:getContents | GetApiSpecContents returns the contents of a specified spec. |
| GET | /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec}:listRevisions | ListApiSpecRevisions lists all revisions of a spec. |
| POST | /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec}:rollback | RollbackApiSpec sets the current revision to a specified prior revision. |
| POST | /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec}:tagRevision | TagApiSpecRevision adds a tag to a specified revision of a spec. |
| GET | /v1/projects/{project}/locations/{location}/artifacts | ListArtifacts returns matching artifacts. |
| POST | /v1/projects/{project}/locations/{location}/artifacts | CreateArtifact creates a specified artifact. |
| GET | /v1/projects/{project}/locations/{location}/artifacts/{artifact} | GetArtifact returns a specified artifact. |
| PUT | /v1/projects/{project}/locations/{location}/artifacts/{artifact} | ReplaceArtifact can be used to replace a specified artifact. |
| DELETE | /v1/projects/{project}/locations/{location}/artifacts/{artifact} | DeleteArtifact removes a specified artifact. |
| GET | /v1/projects/{project}/locations/{location}/artifacts/{artifact}:getContents | GetArtifactContents returns the contents of a specified artifact. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all apis?" -> GET /v1/projects/{project}/locations/{location}/apis
- "Create a apis?" -> POST /v1/projects/{project}/locations/{location}/apis
- "Get apis details?" -> GET /v1/projects/{project}/locations/{location}/apis/{api}
- "Delete a apis?" -> DELETE /v1/projects/{project}/locations/{location}/apis/{api}
- "Partially update a apis?" -> PATCH /v1/projects/{project}/locations/{location}/apis/{api}
- "List all deployments?" -> GET /v1/projects/{project}/locations/{location}/apis/{api}/deployments
- "Create a deployment?" -> POST /v1/projects/{project}/locations/{location}/apis/{api}/deployments
- "Get deployment details?" -> GET /v1/projects/{project}/locations/{location}/apis/{api}/deployments/{deployment}
- "Delete a deployment?" -> DELETE /v1/projects/{project}/locations/{location}/apis/{api}/deployments/{deployment}
- "Partially update a deployment?" -> PATCH /v1/projects/{project}/locations/{location}/apis/{api}/deployments/{deployment}
- "Delete a deployment?" -> DELETE /v1/projects/{project}/locations/{location}/apis/{api}/deployments/{deployment}:deleteRevision
- "Get deployment details?" -> GET /v1/projects/{project}/locations/{location}/apis/{api}/deployments/{deployment}:listRevisions
- "List all versions?" -> GET /v1/projects/{project}/locations/{location}/apis/{api}/versions
- "Create a version?" -> POST /v1/projects/{project}/locations/{location}/apis/{api}/versions
- "Get version details?" -> GET /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version}
- "Delete a version?" -> DELETE /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version}
- "Partially update a version?" -> PATCH /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version}
- "List all specs?" -> GET /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs
- "Create a spec?" -> POST /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs
- "Get spec details?" -> GET /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec}
- "Delete a spec?" -> DELETE /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec}
- "Partially update a spec?" -> PATCH /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec}
- "Delete a spec?" -> DELETE /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec}:deleteRevision
- "Get spec details?" -> GET /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec}:getContents
- "Get spec details?" -> GET /v1/projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec}:listRevisions
- "List all artifacts?" -> GET /v1/projects/{project}/locations/{location}/artifacts
- "Create a artifact?" -> POST /v1/projects/{project}/locations/{location}/artifacts
- "Get artifact details?" -> GET /v1/projects/{project}/locations/{location}/artifacts/{artifact}
- "Update a artifact?" -> PUT /v1/projects/{project}/locations/{location}/artifacts/{artifact}
- "Delete a artifact?" -> DELETE /v1/projects/{project}/locations/{location}/artifacts/{artifact}
- "Get artifact details?" -> GET /v1/projects/{project}/locations/{location}/artifacts/{artifact}:getContents

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
