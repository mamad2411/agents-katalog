---
name: aws-marketplace-catalog-service
description: "AWS Marketplace Catalog Service API skill. Use when working with AWS Marketplace Catalog Service for BatchDescribeEntities, CancelChangeSet, DeleteResourcePolicy. Covers 13 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Marketplace Catalog Service
API version: 2018-09-17

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /DescribeChangeSet -- verify access
3. POST /BatchDescribeEntities -- create first BatchDescribeEntities

## Endpoints

13 endpoints across 13 groups. See references/api-spec.lap for full details.

### BatchDescribeEntities
| Method | Path | Description |
|--------|------|-------------|
| POST | /BatchDescribeEntities | Returns metadata and content for multiple entities. This is the Batch version of the DescribeEntity API and uses the same IAM permission action as DescribeEntity API. |

### CancelChangeSet
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /CancelChangeSet | Used to cancel an open change request. Must be sent before the status of the request changes to APPLYING, the final stage of completing your change request. You can describe a change during the 60-day request history retention period for API calls. |

### DeleteResourcePolicy
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /DeleteResourcePolicy | Deletes a resource-based policy on an entity that is identified by its resource ARN. |

### DescribeChangeSet
| Method | Path | Description |
|--------|------|-------------|
| GET | /DescribeChangeSet | Provides information about a given change set. |

### DescribeEntity
| Method | Path | Description |
|--------|------|-------------|
| GET | /DescribeEntity | Returns the metadata and content of the entity. |

### GetResourcePolicy
| Method | Path | Description |
|--------|------|-------------|
| GET | /GetResourcePolicy | Gets a resource-based policy of an entity that is identified by its resource ARN. |

### ListChangeSets
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListChangeSets | Returns the list of change sets owned by the account being used to make the call. You can filter this list by providing any combination of entityId, ChangeSetName, and status. If you provide more than one filter, the API operation applies a logical AND between the filters. You can describe a change during the 60-day request history retention period for API calls. |

### ListEntities
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListEntities | Provides the list of entities of a given type. |

### ListTagsForResource
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListTagsForResource | Lists all tags that have been added to a resource (either an entity or change set). |

### PutResourcePolicy
| Method | Path | Description |
|--------|------|-------------|
| POST | /PutResourcePolicy | Attaches a resource-based policy to an entity. Examples of an entity include: AmiProduct and ContainerProduct. |

### StartChangeSet
| Method | Path | Description |
|--------|------|-------------|
| POST | /StartChangeSet | Allows you to request changes for your entities. Within a single ChangeSet, you can't start the same change type against the same entity multiple times. Additionally, when a ChangeSet is running, all the entities targeted by the different changes are locked until the change set has completed (either succeeded, cancelled, or failed). If you try to start a change set containing a change against an entity that is already locked, you will receive a ResourceInUseException error. For example, you can't start the ChangeSet described in the example later in this topic because it contains two changes to run the same change type (AddRevisions) against the same entity (entity-id@1). For more information about working with change sets, see  Working with change sets. For information about change types for single-AMI products, see Working with single-AMI products. Also, for more information about change types available for container-based products, see Working with container products. |

### TagResource
| Method | Path | Description |
|--------|------|-------------|
| POST | /TagResource | Tags a resource (either an entity or change set). |

### UntagResource
| Method | Path | Description |
|--------|------|-------------|
| POST | /UntagResource | Removes a tag or list of tags from a resource (either an entity or change set). |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a BatchDescribeEntity?" -> POST /BatchDescribeEntities
- "List all DescribeChangeSet?" -> GET /DescribeChangeSet
- "List all DescribeEntity?" -> GET /DescribeEntity
- "List all GetResourcePolicy?" -> GET /GetResourcePolicy
- "Create a ListChangeSet?" -> POST /ListChangeSets
- "Create a ListEntity?" -> POST /ListEntities
- "Create a ListTagsForResource?" -> POST /ListTagsForResource
- "Create a PutResourcePolicy?" -> POST /PutResourcePolicy
- "Create a StartChangeSet?" -> POST /StartChangeSet
- "Create a TagResource?" -> POST /TagResource
- "Create a UntagResource?" -> POST /UntagResource
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
