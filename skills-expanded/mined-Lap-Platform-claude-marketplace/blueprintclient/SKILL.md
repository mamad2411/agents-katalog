---
name: blueprintclient
description: "BlueprintClient API skill. Use when working with BlueprintClient for {resourceScope}. Covers 14 endpoints."
version: 1.0.0
generator: lapsh
---

# BlueprintClient
API version: 2018-11-01-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /{resourceScope}/providers/Microsoft.Blueprint/blueprints -- verify access

## Endpoints

14 endpoints across 1 groups. See references/api-spec.lap for full details.

### {resourceScope}
| Method | Path | Description |
|--------|------|-------------|
| PUT | /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName} | Create or update a blueprint definition. |
| GET | /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName} | Get a blueprint definition. |
| DELETE | /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName} | Delete a blueprint definition. |
| GET | /{resourceScope}/providers/Microsoft.Blueprint/blueprints | List blueprint definitions. |
| PUT | /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}/artifacts/{artifactName} | Create or update blueprint artifact. |
| GET | /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}/artifacts/{artifactName} | Get a blueprint artifact. |
| DELETE | /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}/artifacts/{artifactName} | Delete a blueprint artifact. |
| GET | /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}/artifacts | List artifacts for a given blueprint definition. |
| PUT | /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}/versions/{versionId} | Publish a new version of the blueprint definition with the latest artifacts. Published blueprint definitions are immutable. |
| GET | /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}/versions/{versionId} | Get a published version of a blueprint definition. |
| DELETE | /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}/versions/{versionId} | Delete a published version of a blueprint definition. |
| GET | /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}/versions | List published versions of given blueprint definition. |
| GET | /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}/versions/{versionId}/artifacts/{artifactName} | Get an artifact for a published blueprint definition. |
| GET | /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}/versions/{versionId}/artifacts | List artifacts for a version of a published blueprint definition. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Update a blueprint?" -> PUT /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}
- "Get blueprint details?" -> GET /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}
- "Delete a blueprint?" -> DELETE /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}
- "List all blueprints?" -> GET /{resourceScope}/providers/Microsoft.Blueprint/blueprints
- "Update a artifact?" -> PUT /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}/artifacts/{artifactName}
- "Get artifact details?" -> GET /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}/artifacts/{artifactName}
- "Delete a artifact?" -> DELETE /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}/artifacts/{artifactName}
- "List all artifacts?" -> GET /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}/artifacts
- "Update a version?" -> PUT /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}/versions/{versionId}
- "Get version details?" -> GET /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}/versions/{versionId}
- "Delete a version?" -> DELETE /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}/versions/{versionId}
- "List all versions?" -> GET /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}/versions
- "Get artifact details?" -> GET /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}/versions/{versionId}/artifacts/{artifactName}
- "List all artifacts?" -> GET /{resourceScope}/providers/Microsoft.Blueprint/blueprints/{blueprintName}/versions/{versionId}/artifacts
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
