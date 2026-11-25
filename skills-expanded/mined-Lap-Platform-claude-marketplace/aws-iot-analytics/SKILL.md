---
name: aws-iot-analytics
description: "AWS IoT Analytics API skill. Use when working with AWS IoT Analytics for messages, pipelines, channels. Covers 34 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS IoT Analytics
API version: 2017-11-27

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /logging -- verify access
3. POST /messages/batch -- create first batch

## Endpoints

34 endpoints across 8 groups. See references/api-spec.lap for full details.

### messages
| Method | Path | Description |
|--------|------|-------------|
| POST | /messages/batch | Sends messages to a channel. |

### pipelines
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /pipelines/{pipelineName}/reprocessing/{reprocessingId} | Cancels the reprocessing of data through the pipeline. |
| POST | /pipelines | Creates a pipeline. A pipeline consumes messages from a channel and allows you to process the messages before storing them in a data store. You must specify both a channel and a datastore activity and, optionally, as many as 23 additional activities in the pipelineActivities array. |
| DELETE | /pipelines/{pipelineName} | Deletes the specified pipeline. |
| GET | /pipelines/{pipelineName} | Retrieves information about a pipeline. |
| GET | /pipelines | Retrieves a list of pipelines. |
| POST | /pipelines/{pipelineName}/reprocessing | Starts the reprocessing of raw message data through the pipeline. |
| PUT | /pipelines/{pipelineName} | Updates the settings of a pipeline. You must specify both a channel and a datastore activity and, optionally, as many as 23 additional activities in the pipelineActivities array. |

### channels
| Method | Path | Description |
|--------|------|-------------|
| POST | /channels | Used to create a channel. A channel collects data from an MQTT topic and archives the raw, unprocessed messages before publishing the data to a pipeline. |
| DELETE | /channels/{channelName} | Deletes the specified channel. |
| GET | /channels/{channelName} | Retrieves information about a channel. |
| GET | /channels | Retrieves a list of channels. |
| GET | /channels/{channelName}/sample | Retrieves a sample of messages from the specified channel ingested during the specified timeframe. Up to 10 messages can be retrieved. |
| PUT | /channels/{channelName} | Used to update the settings of a channel. |

### datasets
| Method | Path | Description |
|--------|------|-------------|
| POST | /datasets | Used to create a dataset. A dataset stores data retrieved from a data store by applying a queryAction (a SQL query) or a containerAction (executing a containerized application). This operation creates the skeleton of a dataset. The dataset can be populated manually by calling CreateDatasetContent or automatically according to a trigger you specify. |
| POST | /datasets/{datasetName}/content | Creates the content of a dataset by applying a queryAction (a SQL query) or a containerAction (executing a containerized application). |
| DELETE | /datasets/{datasetName} | Deletes the specified dataset. You do not have to delete the content of the dataset before you perform this operation. |
| DELETE | /datasets/{datasetName}/content | Deletes the content of the specified dataset. |
| GET | /datasets/{datasetName} | Retrieves information about a dataset. |
| GET | /datasets/{datasetName}/content | Retrieves the contents of a dataset as presigned URIs. |
| GET | /datasets/{datasetName}/contents | Lists information about dataset contents that have been created. |
| GET | /datasets | Retrieves information about datasets. |
| PUT | /datasets/{datasetName} | Updates the settings of a dataset. |

### datastores
| Method | Path | Description |
|--------|------|-------------|
| POST | /datastores | Creates a data store, which is a repository for messages. |
| DELETE | /datastores/{datastoreName} | Deletes the specified data store. |
| GET | /datastores/{datastoreName} | Retrieves information about a data store. |
| GET | /datastores | Retrieves a list of data stores. |
| PUT | /datastores/{datastoreName} | Used to update the settings of a data store. |

### logging
| Method | Path | Description |
|--------|------|-------------|
| GET | /logging | Retrieves the current settings of the IoT Analytics logging options. |
| PUT | /logging | Sets or updates the IoT Analytics logging options. If you update the value of any loggingOptions field, it takes up to one minute for the change to take effect. Also, if you change the policy attached to the role you specified in the roleArn field (for example, to correct an invalid policy), it takes up to five minutes for that change to take effect. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags | Lists the tags (metadata) that you have assigned to the resource. |
| POST | /tags | Adds to or modifies the tags of the given resource. Tags are metadata that can be used to manage a resource. |
| DELETE | /tags | Removes the given tags (metadata) from the resource. |

### pipelineactivities
| Method | Path | Description |
|--------|------|-------------|
| POST | /pipelineactivities/run | Simulates the results of running a pipeline activity on a message payload. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a batch?" -> POST /messages/batch
- "Delete a reprocessing?" -> DELETE /pipelines/{pipelineName}/reprocessing/{reprocessingId}
- "Create a channel?" -> POST /channels
- "Create a dataset?" -> POST /datasets
- "Create a content?" -> POST /datasets/{datasetName}/content
- "Create a datastore?" -> POST /datastores
- "Create a pipeline?" -> POST /pipelines
- "Delete a channel?" -> DELETE /channels/{channelName}
- "Delete a dataset?" -> DELETE /datasets/{datasetName}
- "Delete a datastore?" -> DELETE /datastores/{datastoreName}
- "Delete a pipeline?" -> DELETE /pipelines/{pipelineName}
- "Get channel details?" -> GET /channels/{channelName}
- "Get dataset details?" -> GET /datasets/{datasetName}
- "Get datastore details?" -> GET /datastores/{datastoreName}
- "List all logging?" -> GET /logging
- "Get pipeline details?" -> GET /pipelines/{pipelineName}
- "List all content?" -> GET /datasets/{datasetName}/content
- "List all channels?" -> GET /channels
- "List all contents?" -> GET /datasets/{datasetName}/contents
- "List all datasets?" -> GET /datasets
- "List all datastores?" -> GET /datastores
- "List all pipelines?" -> GET /pipelines
- "List all tags?" -> GET /tags
- "Create a run?" -> POST /pipelineactivities/run
- "List all sample?" -> GET /channels/{channelName}/sample
- "Create a reprocessing?" -> POST /pipelines/{pipelineName}/reprocessing
- "Create a tag?" -> POST /tags
- "Update a channel?" -> PUT /channels/{channelName}
- "Update a dataset?" -> PUT /datasets/{datasetName}
- "Update a datastore?" -> PUT /datastores/{datastoreName}
- "Update a pipeline?" -> PUT /pipelines/{pipelineName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
