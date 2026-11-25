---
name: aws-elemental-mediapackage
description: "AWS Elemental MediaPackage API skill. Use when working with AWS Elemental MediaPackage for channels, harvest_jobs, origin_endpoints. Covers 19 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Elemental MediaPackage
API version: 2017-10-12

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /channels -- verify access
3. POST /channels -- create first channels

## Endpoints

19 endpoints across 4 groups. See references/api-spec.lap for full details.

### channels
| Method | Path | Description |
|--------|------|-------------|
| PUT | /channels/{id}/configure_logs | Changes the Channel's properities to configure log subscription |
| POST | /channels | Creates a new Channel. |
| DELETE | /channels/{id} | Deletes an existing Channel. |
| GET | /channels/{id} | Gets details about a Channel. |
| GET | /channels | Returns a collection of Channels. |
| PUT | /channels/{id}/credentials | Changes the Channel's first IngestEndpoint's username and password. WARNING - This API is deprecated. Please use RotateIngestEndpointCredentials instead |
| PUT | /channels/{id}/ingest_endpoints/{ingest_endpoint_id}/credentials | Rotate the IngestEndpoint's username and password, as specified by the IngestEndpoint's id. |
| PUT | /channels/{id} | Updates an existing Channel. |

### harvest_jobs
| Method | Path | Description |
|--------|------|-------------|
| POST | /harvest_jobs | Creates a new HarvestJob record. |
| GET | /harvest_jobs/{id} | Gets details about an existing HarvestJob. |
| GET | /harvest_jobs | Returns a collection of HarvestJob records. |

### origin_endpoints
| Method | Path | Description |
|--------|------|-------------|
| POST | /origin_endpoints | Creates a new OriginEndpoint record. |
| DELETE | /origin_endpoints/{id} | Deletes an existing OriginEndpoint. |
| GET | /origin_endpoints/{id} | Gets details about an existing OriginEndpoint. |
| GET | /origin_endpoints | Returns a collection of OriginEndpoint records. |
| PUT | /origin_endpoints/{id} | Updates an existing OriginEndpoint. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resource-arn} |  |
| POST | /tags/{resource-arn} |  |
| DELETE | /tags/{resource-arn} |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a channel?" -> POST /channels
- "Create a harvest_job?" -> POST /harvest_jobs
- "Create a origin_endpoint?" -> POST /origin_endpoints
- "Delete a channel?" -> DELETE /channels/{id}
- "Delete a origin_endpoint?" -> DELETE /origin_endpoints/{id}
- "Get channel details?" -> GET /channels/{id}
- "Get harvest_job details?" -> GET /harvest_jobs/{id}
- "Get origin_endpoint details?" -> GET /origin_endpoints/{id}
- "List all channels?" -> GET /channels
- "List all harvest_jobs?" -> GET /harvest_jobs
- "List all origin_endpoints?" -> GET /origin_endpoints
- "Get tag details?" -> GET /tags/{resource-arn}
- "Delete a tag?" -> DELETE /tags/{resource-arn}
- "Update a channel?" -> PUT /channels/{id}
- "Update a origin_endpoint?" -> PUT /origin_endpoints/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
