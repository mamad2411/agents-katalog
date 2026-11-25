---
name: amazon-appflow
description: "Amazon Appflow API skill. Use when working with Amazon Appflow for cancel-flow-executions, create-connector-profile, create-flow. Covers 25 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Appflow
API version: 2020-08-23

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /tags/{resourceArn} -- verify access
3. POST /cancel-flow-executions -- create first cancel-flow-executions

## Endpoints

25 endpoints across 23 groups. See references/api-spec.lap for full details.

### cancel-flow-executions
| Method | Path | Description |
|--------|------|-------------|
| POST | /cancel-flow-executions | Cancels active runs for a flow. You can cancel all of the active runs for a flow, or you can cancel specific runs by providing their IDs. You can cancel a flow run only when the run is in progress. You can't cancel a run that has already completed or failed. You also can't cancel a run that's scheduled to occur but hasn't started yet. To prevent a scheduled run, you can deactivate the flow with the StopFlow action. You cannot resume a run after you cancel it. When you send your request, the status for each run becomes CancelStarted. When the cancellation completes, the status becomes Canceled.  When you cancel a run, you still incur charges for any data that the run already processed before the cancellation. If the run had already written some data to the flow destination, then that data remains in the destination. If you configured the flow to use a batch API (such as the Salesforce Bulk API 2.0), then the run will finish reading or writing its entire batch of data after the cancellation. For these operations, the data processing charges for Amazon AppFlow apply. For the pricing information, see Amazon AppFlow pricing. |

### create-connector-profile
| Method | Path | Description |
|--------|------|-------------|
| POST | /create-connector-profile | Creates a new connector profile associated with your Amazon Web Services account. There is a soft quota of 100 connector profiles per Amazon Web Services account. If you need more connector profiles than this quota allows, you can submit a request to the Amazon AppFlow team through the Amazon AppFlow support channel. In each connector profile that you create, you can provide the credentials and properties for only one connector. |

### create-flow
| Method | Path | Description |
|--------|------|-------------|
| POST | /create-flow | Enables your application to create a new flow using Amazon AppFlow. You must create a connector profile before calling this API. Please note that the Request Syntax below shows syntax for multiple destinations, however, you can only transfer data to one item in this list at a time. Amazon AppFlow does not currently support flows to multiple destinations at once. |

### delete-connector-profile
| Method | Path | Description |
|--------|------|-------------|
| POST | /delete-connector-profile | Enables you to delete an existing connector profile. |

### delete-flow
| Method | Path | Description |
|--------|------|-------------|
| POST | /delete-flow | Enables your application to delete an existing flow. Before deleting the flow, Amazon AppFlow validates the request by checking the flow configuration and status. You can delete flows one at a time. |

### describe-connector
| Method | Path | Description |
|--------|------|-------------|
| POST | /describe-connector | Describes the given custom connector registered in your Amazon Web Services account. This API can be used for custom connectors that are registered in your account and also for Amazon authored connectors. |

### describe-connector-entity
| Method | Path | Description |
|--------|------|-------------|
| POST | /describe-connector-entity | Provides details regarding the entity used with the connector, with a description of the data model for each field in that entity. |

### describe-connector-profiles
| Method | Path | Description |
|--------|------|-------------|
| POST | /describe-connector-profiles | Returns a list of connector-profile details matching the provided connector-profile names and connector-types. Both input lists are optional, and you can use them to filter the result.  If no names or connector-types are provided, returns all connector profiles in a paginated form. If there is no match, this operation returns an empty list. |

### describe-connectors
| Method | Path | Description |
|--------|------|-------------|
| POST | /describe-connectors | Describes the connectors vended by Amazon AppFlow for specified connector types. If you don't specify a connector type, this operation describes all connectors vended by Amazon AppFlow. If there are more connectors than can be returned in one page, the response contains a nextToken object, which can be be passed in to the next call to the DescribeConnectors API operation to retrieve the next page. |

### describe-flow
| Method | Path | Description |
|--------|------|-------------|
| POST | /describe-flow | Provides a description of the specified flow. |

### describe-flow-execution-records
| Method | Path | Description |
|--------|------|-------------|
| POST | /describe-flow-execution-records | Fetches the execution history of the flow. |

### list-connector-entities
| Method | Path | Description |
|--------|------|-------------|
| POST | /list-connector-entities | Returns the list of available connector entities supported by Amazon AppFlow. For example, you can query Salesforce for Account and Opportunity entities, or query ServiceNow for the Incident entity. |

### list-connectors
| Method | Path | Description |
|--------|------|-------------|
| POST | /list-connectors | Returns the list of all registered custom connectors in your Amazon Web Services account. This API lists only custom connectors registered in this account, not the Amazon Web Services authored connectors. |

### list-flows
| Method | Path | Description |
|--------|------|-------------|
| POST | /list-flows | Lists all of the flows associated with your account. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Retrieves the tags that are associated with a specified flow. |
| POST | /tags/{resourceArn} | Applies a tag to the specified flow. |
| DELETE | /tags/{resourceArn} | Removes a tag from the specified flow. |

### register-connector
| Method | Path | Description |
|--------|------|-------------|
| POST | /register-connector | Registers a new custom connector with your Amazon Web Services account. Before you can register the connector, you must deploy the associated AWS lambda function in your account. |

### reset-connector-metadata-cache
| Method | Path | Description |
|--------|------|-------------|
| POST | /reset-connector-metadata-cache | Resets metadata about your connector entities that Amazon AppFlow stored in its cache. Use this action when you want Amazon AppFlow to return the latest information about the data that you have in a source application. Amazon AppFlow returns metadata about your entities when you use the ListConnectorEntities or DescribeConnectorEntities actions. Following these actions, Amazon AppFlow caches the metadata to reduce the number of API requests that it must send to the source application. Amazon AppFlow automatically resets the cache once every hour, but you can use this action when you want to get the latest metadata right away. |

### start-flow
| Method | Path | Description |
|--------|------|-------------|
| POST | /start-flow | Activates an existing flow. For on-demand flows, this operation runs the flow immediately. For schedule and event-triggered flows, this operation activates the flow. |

### stop-flow
| Method | Path | Description |
|--------|------|-------------|
| POST | /stop-flow | Deactivates the existing flow. For on-demand flows, this operation returns an unsupportedOperationException error message. For schedule and event-triggered flows, this operation deactivates the flow. |

### unregister-connector
| Method | Path | Description |
|--------|------|-------------|
| POST | /unregister-connector | Unregisters the custom connector registered in your account that matches the connector label provided in the request. |

### update-connector-profile
| Method | Path | Description |
|--------|------|-------------|
| POST | /update-connector-profile | Updates a given connector profile associated with your account. |

### update-connector-registration
| Method | Path | Description |
|--------|------|-------------|
| POST | /update-connector-registration | Updates a custom connector that you've previously registered. This operation updates the connector with one of the following:   The latest version of the AWS Lambda function that's assigned to the connector   A new AWS Lambda function that you specify |

### update-flow
| Method | Path | Description |
|--------|------|-------------|
| POST | /update-flow | Updates an existing flow. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a cancel-flow-execution?" -> POST /cancel-flow-executions
- "Create a create-connector-profile?" -> POST /create-connector-profile
- "Create a create-flow?" -> POST /create-flow
- "Create a delete-connector-profile?" -> POST /delete-connector-profile
- "Create a delete-flow?" -> POST /delete-flow
- "Create a describe-connector?" -> POST /describe-connector
- "Create a describe-connector-entity?" -> POST /describe-connector-entity
- "Create a describe-connector-profile?" -> POST /describe-connector-profiles
- "Create a describe-connector?" -> POST /describe-connectors
- "Create a describe-flow?" -> POST /describe-flow
- "Create a describe-flow-execution-record?" -> POST /describe-flow-execution-records
- "Create a list-connector-entity?" -> POST /list-connector-entities
- "Create a list-connector?" -> POST /list-connectors
- "Create a list-flow?" -> POST /list-flows
- "Get tag details?" -> GET /tags/{resourceArn}
- "Create a register-connector?" -> POST /register-connector
- "Create a reset-connector-metadata-cache?" -> POST /reset-connector-metadata-cache
- "Create a start-flow?" -> POST /start-flow
- "Create a stop-flow?" -> POST /stop-flow
- "Create a unregister-connector?" -> POST /unregister-connector
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Create a update-connector-profile?" -> POST /update-connector-profile
- "Create a update-connector-registration?" -> POST /update-connector-registration
- "Create a update-flow?" -> POST /update-flow
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
