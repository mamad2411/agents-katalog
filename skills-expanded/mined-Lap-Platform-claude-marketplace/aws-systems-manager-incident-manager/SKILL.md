---
name: aws-systems-manager-incident-manager
description: "AWS Systems Manager Incident Manager API skill. Use when working with AWS Systems Manager Incident Manager for batchGetIncidentFindings, createReplicationSet, createResponsePlan. Covers 31 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Systems Manager Incident Manager
API version: 2018-05-10

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /getIncidentRecord -- verify access
3. POST /batchGetIncidentFindings -- create first batchGetIncidentFindings

## Endpoints

31 endpoints across 29 groups. See references/api-spec.lap for full details.

### batchGetIncidentFindings
| Method | Path | Description |
|--------|------|-------------|
| POST | /batchGetIncidentFindings | Retrieves details about all specified findings for an incident, including descriptive details about each finding. A finding represents a recent application environment change made by an CodeDeploy deployment or an CloudFormation stack creation or update that can be investigated as a potential cause of the incident. |

### createReplicationSet
| Method | Path | Description |
|--------|------|-------------|
| POST | /createReplicationSet | A replication set replicates and encrypts your data to the provided Regions with the provided KMS key. |

### createResponsePlan
| Method | Path | Description |
|--------|------|-------------|
| POST | /createResponsePlan | Creates a response plan that automates the initial response to incidents. A response plan engages contacts, starts chat channel collaboration, and initiates runbooks at the beginning of an incident. |

### createTimelineEvent
| Method | Path | Description |
|--------|------|-------------|
| POST | /createTimelineEvent | Creates a custom timeline event on the incident details page of an incident record. Incident Manager automatically creates timeline events that mark key moments during an incident. You can create custom timeline events to mark important events that Incident Manager can detect automatically. |

### deleteIncidentRecord
| Method | Path | Description |
|--------|------|-------------|
| POST | /deleteIncidentRecord | Delete an incident record from Incident Manager. |

### deleteReplicationSet
| Method | Path | Description |
|--------|------|-------------|
| POST | /deleteReplicationSet | Deletes all Regions in your replication set. Deleting the replication set deletes all Incident Manager data. |

### deleteResourcePolicy
| Method | Path | Description |
|--------|------|-------------|
| POST | /deleteResourcePolicy | Deletes the resource policy that Resource Access Manager uses to share your Incident Manager resource. |

### deleteResponsePlan
| Method | Path | Description |
|--------|------|-------------|
| POST | /deleteResponsePlan | Deletes the specified response plan. Deleting a response plan stops all linked CloudWatch alarms and EventBridge events from creating an incident with this response plan. |

### deleteTimelineEvent
| Method | Path | Description |
|--------|------|-------------|
| POST | /deleteTimelineEvent | Deletes a timeline event from an incident. |

### getIncidentRecord
| Method | Path | Description |
|--------|------|-------------|
| GET | /getIncidentRecord | Returns the details for the specified incident record. |

### getReplicationSet
| Method | Path | Description |
|--------|------|-------------|
| GET | /getReplicationSet | Retrieve your Incident Manager replication set. |

### getResourcePolicies
| Method | Path | Description |
|--------|------|-------------|
| POST | /getResourcePolicies | Retrieves the resource policies attached to the specified response plan. |

### getResponsePlan
| Method | Path | Description |
|--------|------|-------------|
| GET | /getResponsePlan | Retrieves the details of the specified response plan. |

### getTimelineEvent
| Method | Path | Description |
|--------|------|-------------|
| GET | /getTimelineEvent | Retrieves a timeline event based on its ID and incident record. |

### listIncidentFindings
| Method | Path | Description |
|--------|------|-------------|
| POST | /listIncidentFindings | Retrieves a list of the IDs of findings, plus their last modified times, that have been identified for a specified incident. A finding represents a recent application environment change made by an CloudFormation stack creation or update or an CodeDeploy deployment that can be investigated as a potential cause of the incident. |

### listIncidentRecords
| Method | Path | Description |
|--------|------|-------------|
| POST | /listIncidentRecords | Lists all incident records in your account. Use this command to retrieve the Amazon Resource Name (ARN) of the incident record you want to update. |

### listRelatedItems
| Method | Path | Description |
|--------|------|-------------|
| POST | /listRelatedItems | List all related items for an incident record. |

### listReplicationSets
| Method | Path | Description |
|--------|------|-------------|
| POST | /listReplicationSets | Lists details about the replication set configured in your account. |

### listResponsePlans
| Method | Path | Description |
|--------|------|-------------|
| POST | /listResponsePlans | Lists all response plans in your account. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Lists the tags that are attached to the specified response plan or incident. |
| POST | /tags/{resourceArn} | Adds a tag to a response plan. |
| DELETE | /tags/{resourceArn} | Removes a tag from a resource. |

### listTimelineEvents
| Method | Path | Description |
|--------|------|-------------|
| POST | /listTimelineEvents | Lists timeline events for the specified incident record. |

### putResourcePolicy
| Method | Path | Description |
|--------|------|-------------|
| POST | /putResourcePolicy | Adds a resource policy to the specified response plan. The resource policy is used to share the response plan using Resource Access Manager (RAM). For more information about cross-account sharing, see Cross-Region and cross-account incident management. |

### startIncident
| Method | Path | Description |
|--------|------|-------------|
| POST | /startIncident | Used to start an incident from CloudWatch alarms, EventBridge events, or manually. |

### updateDeletionProtection
| Method | Path | Description |
|--------|------|-------------|
| POST | /updateDeletionProtection | Update deletion protection to either allow or deny deletion of the final Region in a replication set. |

### updateIncidentRecord
| Method | Path | Description |
|--------|------|-------------|
| POST | /updateIncidentRecord | Update the details of an incident record. You can use this operation to update an incident record from the defined chat channel. For more information about using actions in chat channels, see Interacting through chat. |

### updateRelatedItems
| Method | Path | Description |
|--------|------|-------------|
| POST | /updateRelatedItems | Add or remove related items from the related items tab of an incident record. |

### updateReplicationSet
| Method | Path | Description |
|--------|------|-------------|
| POST | /updateReplicationSet | Add or delete Regions from your replication set. |

### updateResponsePlan
| Method | Path | Description |
|--------|------|-------------|
| POST | /updateResponsePlan | Updates the specified response plan. |

### updateTimelineEvent
| Method | Path | Description |
|--------|------|-------------|
| POST | /updateTimelineEvent | Updates a timeline event. You can update events of type Custom Event. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a batchGetIncidentFinding?" -> POST /batchGetIncidentFindings
- "Create a createReplicationSet?" -> POST /createReplicationSet
- "Create a createResponsePlan?" -> POST /createResponsePlan
- "Create a createTimelineEvent?" -> POST /createTimelineEvent
- "Create a deleteIncidentRecord?" -> POST /deleteIncidentRecord
- "Create a deleteReplicationSet?" -> POST /deleteReplicationSet
- "Create a deleteResourcePolicy?" -> POST /deleteResourcePolicy
- "Create a deleteResponsePlan?" -> POST /deleteResponsePlan
- "Create a deleteTimelineEvent?" -> POST /deleteTimelineEvent
- "List all getIncidentRecord?" -> GET /getIncidentRecord
- "List all getReplicationSet?" -> GET /getReplicationSet
- "Create a getResourcePolicy?" -> POST /getResourcePolicies
- "List all getResponsePlan?" -> GET /getResponsePlan
- "List all getTimelineEvent?" -> GET /getTimelineEvent
- "Create a listIncidentFinding?" -> POST /listIncidentFindings
- "Create a listIncidentRecord?" -> POST /listIncidentRecords
- "Create a listRelatedItem?" -> POST /listRelatedItems
- "Create a listReplicationSet?" -> POST /listReplicationSets
- "Create a listResponsePlan?" -> POST /listResponsePlans
- "Get tag details?" -> GET /tags/{resourceArn}
- "Create a listTimelineEvent?" -> POST /listTimelineEvents
- "Create a putResourcePolicy?" -> POST /putResourcePolicy
- "Create a startIncident?" -> POST /startIncident
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Create a updateDeletionProtection?" -> POST /updateDeletionProtection
- "Create a updateIncidentRecord?" -> POST /updateIncidentRecord
- "Create a updateRelatedItem?" -> POST /updateRelatedItems
- "Create a updateReplicationSet?" -> POST /updateReplicationSet
- "Create a updateResponsePlan?" -> POST /updateResponsePlan
- "Create a updateTimelineEvent?" -> POST /updateTimelineEvent
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
