---
name: aws-elemental-mediapackage-vod
description: "AWS Elemental MediaPackage VOD API skill. Use when working with AWS Elemental MediaPackage VOD for packaging_groups, assets, packaging_configurations. Covers 17 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Elemental MediaPackage VOD
API version: 2018-11-07

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /assets -- verify access
3. POST /assets -- create first assets

## Endpoints

17 endpoints across 4 groups. See references/api-spec.lap for full details.

### packaging_groups
| Method | Path | Description |
|--------|------|-------------|
| PUT | /packaging_groups/{id}/configure_logs | Changes the packaging group's properities to configure log subscription |
| POST | /packaging_groups | Creates a new MediaPackage VOD PackagingGroup resource. |
| DELETE | /packaging_groups/{id} | Deletes a MediaPackage VOD PackagingGroup resource. |
| GET | /packaging_groups/{id} | Returns a description of a MediaPackage VOD PackagingGroup resource. |
| GET | /packaging_groups | Returns a collection of MediaPackage VOD PackagingGroup resources. |
| PUT | /packaging_groups/{id} | Updates a specific packaging group. You can't change the id attribute or any other system-generated attributes. |

### assets
| Method | Path | Description |
|--------|------|-------------|
| POST | /assets | Creates a new MediaPackage VOD Asset resource. |
| DELETE | /assets/{id} | Deletes an existing MediaPackage VOD Asset resource. |
| GET | /assets/{id} | Returns a description of a MediaPackage VOD Asset resource. |
| GET | /assets | Returns a collection of MediaPackage VOD Asset resources. |

### packaging_configurations
| Method | Path | Description |
|--------|------|-------------|
| POST | /packaging_configurations | Creates a new MediaPackage VOD PackagingConfiguration resource. |
| DELETE | /packaging_configurations/{id} | Deletes a MediaPackage VOD PackagingConfiguration resource. |
| GET | /packaging_configurations/{id} | Returns a description of a MediaPackage VOD PackagingConfiguration resource. |
| GET | /packaging_configurations | Returns a collection of MediaPackage VOD PackagingConfiguration resources. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resource-arn} | Returns a list of the tags assigned to the specified resource. |
| POST | /tags/{resource-arn} | Adds tags to the specified resource. You can specify one or more tags to add. |
| DELETE | /tags/{resource-arn} | Removes tags from the specified resource. You can specify one or more tags to remove. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a asset?" -> POST /assets
- "Create a packaging_configuration?" -> POST /packaging_configurations
- "Create a packaging_group?" -> POST /packaging_groups
- "Delete a asset?" -> DELETE /assets/{id}
- "Delete a packaging_configuration?" -> DELETE /packaging_configurations/{id}
- "Delete a packaging_group?" -> DELETE /packaging_groups/{id}
- "Get asset details?" -> GET /assets/{id}
- "Get packaging_configuration details?" -> GET /packaging_configurations/{id}
- "Get packaging_group details?" -> GET /packaging_groups/{id}
- "List all assets?" -> GET /assets
- "List all packaging_configurations?" -> GET /packaging_configurations
- "List all packaging_groups?" -> GET /packaging_groups
- "Get tag details?" -> GET /tags/{resource-arn}
- "Delete a tag?" -> DELETE /tags/{resource-arn}
- "Update a packaging_group?" -> PUT /packaging_groups/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
