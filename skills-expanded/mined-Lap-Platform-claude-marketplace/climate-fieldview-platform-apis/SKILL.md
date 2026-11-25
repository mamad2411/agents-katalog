---
name: climate-fieldview-platform-apis
description: "Climate FieldView Platform APIs API skill. Use when working with Climate FieldView Platform APIs for fields, farmOrganizations, operations. Covers 28 endpoints."
version: 1.0.0
generator: lapsh
---

# Climate FieldView Platform APIs
API version: 4.0.11

## Auth
OAuth2 | ApiKey X-Api-Key in header

## Base URL
https://platform.climate.com/

## Setup
1. Set your API key in the appropriate header
2. GET /v4/fields -- verify access
3. POST /v4/boundaries/query -- create first query

## Endpoints

28 endpoints across 8 groups. See references/api-spec.lap for full details.

### fields
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/fields | Retrieve list of Fields |
| GET | /v4/fields/{fieldId} | Retrieve a specific Field by ID |

### farmOrganizations
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/farmOrganizations/{farmOrganizationType}/{farmOrganizationId} | Retrieve a specific farm organization by organization type and ID |

### operations
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/operations/all | Retrieve the operations accessible to a a given user. |

### resourceOwners
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/resourceOwners/{resourceOwnerId} | Retrieve a resource owner by ID |

### boundaries
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/boundaries/{boundaryId} | Retrieve a Boundary by ID |
| POST | /v4/boundaries/query | Retrieve Boundaries in batch |
| POST | /v4/boundaries | Upload a boundary |

### uploads
| Method | Path | Description |
|--------|------|-------------|
| POST | /v4/uploads | Initiate a new upload |
| PUT | /v4/uploads/{uploadId} | Chunked upload of data |
| GET | /v4/uploads/{uploadId}/status | Retrieve Upload status |
| POST | /v4/uploads/status/query | Retrieve Upload statuses in batch |

### exports
| Method | Path | Description |
|--------|------|-------------|
| POST | /v4/exports | Initiate a new export request. |
| GET | /v4/exports/{exportId}/status | Retrieve the status of an Export. |
| GET | /v4/exports/{exportId}/contents | Retrieve the binary contents of a processed export request. |

### layers
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/layers/scoutingObservations | Retrieve a list of scouting observations |
| GET | /v4/layers/scoutingObservations/{scoutingObservationId} | Retrieve individual scouting observation |
| GET | /v4/layers/scoutingObservations/{scoutingObservationId}/attachments | Retrieve attachments associated with a given scouting observation. |
| GET | /v4/layers/scoutingObservations/{scoutingObservationId}/attachments/{attachmentId}/contents | Retrieve the binary contents of a scouting observation’s attachment. |
| GET | /v4/layers/asPlanted | Retrieve a list of planting activities |
| GET | /v4/layers/asPlanted/{activityId}/contents | Retrieve the raw planting activity |
| GET | /v4/layers/asPlanted/{activityId} | Retrieve the summary of an activity as planted agronomic data |
| GET | /v4/layers/asApplied | Retrieve a list of application activities |
| GET | /v4/layers/asApplied/{activityId}/contents | Retrieve the raw application activity |
| GET | /v4/layers/asApplied/{activityId} | Retrieve the summary of an activity as applied agronomic data |
| GET | /v4/layers/asHarvested | Retrieve a list of harvest activities |
| GET | /v4/layers/asHarvested/{activityId}/contents | Retrieve the raw harvest activity |
| GET | /v4/layers/asHarvested/{activityId} | Retrieve the summary of an activity as harvested agronomic data |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all fields?" -> GET /v4/fields
- "Get field details?" -> GET /v4/fields/{fieldId}
- "Get farmOrganization details?" -> GET /v4/farmOrganizations/{farmOrganizationType}/{farmOrganizationId}
- "List all all?" -> GET /v4/operations/all
- "Get resourceOwner details?" -> GET /v4/resourceOwners/{resourceOwnerId}
- "Get boundary details?" -> GET /v4/boundaries/{boundaryId}
- "Create a query?" -> POST /v4/boundaries/query
- "Create a boundary?" -> POST /v4/boundaries
- "Create a upload?" -> POST /v4/uploads
- "Update a upload?" -> PUT /v4/uploads/{uploadId}
- "List all status?" -> GET /v4/uploads/{uploadId}/status
- "Create a query?" -> POST /v4/uploads/status/query
- "Create a export?" -> POST /v4/exports
- "List all status?" -> GET /v4/exports/{exportId}/status
- "List all contents?" -> GET /v4/exports/{exportId}/contents
- "List all scoutingObservations?" -> GET /v4/layers/scoutingObservations
- "Get scoutingObservation details?" -> GET /v4/layers/scoutingObservations/{scoutingObservationId}
- "List all attachments?" -> GET /v4/layers/scoutingObservations/{scoutingObservationId}/attachments
- "List all contents?" -> GET /v4/layers/scoutingObservations/{scoutingObservationId}/attachments/{attachmentId}/contents
- "List all asPlanted?" -> GET /v4/layers/asPlanted
- "List all contents?" -> GET /v4/layers/asPlanted/{activityId}/contents
- "Get asPlanted details?" -> GET /v4/layers/asPlanted/{activityId}
- "List all asApplied?" -> GET /v4/layers/asApplied
- "List all contents?" -> GET /v4/layers/asApplied/{activityId}/contents
- "Get asApplied details?" -> GET /v4/layers/asApplied/{activityId}
- "List all asHarvested?" -> GET /v4/layers/asHarvested
- "List all contents?" -> GET /v4/layers/asHarvested/{activityId}/contents
- "Get asHarvested details?" -> GET /v4/layers/asHarvested/{activityId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
