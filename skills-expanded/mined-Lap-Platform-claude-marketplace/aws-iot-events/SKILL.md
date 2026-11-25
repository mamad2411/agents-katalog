---
name: aws-iot-events
description: "AWS IoT Events API skill. Use when working with AWS IoT Events for alarm-models, detector-models, inputs. Covers 26 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS IoT Events
API version: 2018-07-27

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /logging -- verify access
3. POST /alarm-models -- create first alarm-models

## Endpoints

26 endpoints across 7 groups. See references/api-spec.lap for full details.

### alarm-models
| Method | Path | Description |
|--------|------|-------------|
| POST | /alarm-models | Creates an alarm model to monitor an AWS IoT Events input attribute. You can use the alarm to get notified when the value is outside a specified range. For more information, see Create an alarm model in the AWS IoT Events Developer Guide. |
| DELETE | /alarm-models/{alarmModelName} | Deletes an alarm model. Any alarm instances that were created based on this alarm model are also deleted. This action can't be undone. |
| GET | /alarm-models/{alarmModelName} | Retrieves information about an alarm model. If you don't specify a value for the alarmModelVersion parameter, the latest version is returned. |
| GET | /alarm-models/{alarmModelName}/versions | Lists all the versions of an alarm model. The operation returns only the metadata associated with each alarm model version. |
| GET | /alarm-models | Lists the alarm models that you created. The operation returns only the metadata associated with each alarm model. |
| POST | /alarm-models/{alarmModelName} | Updates an alarm model. Any alarms that were created based on the previous version are deleted and then created again as new data arrives. |

### detector-models
| Method | Path | Description |
|--------|------|-------------|
| POST | /detector-models | Creates a detector model. |
| DELETE | /detector-models/{detectorModelName} | Deletes a detector model. Any active instances of the detector model are also deleted. |
| GET | /detector-models/{detectorModelName} | Describes a detector model. If the version parameter is not specified, information about the latest version is returned. |
| GET | /detector-models/{detectorModelName}/versions | Lists all the versions of a detector model. Only the metadata associated with each detector model version is returned. |
| GET | /detector-models | Lists the detector models you have created. Only the metadata associated with each detector model is returned. |
| POST | /detector-models/{detectorModelName} | Updates a detector model. Detectors (instances) spawned by the previous version are deleted and then re-created as new inputs arrive. |

### inputs
| Method | Path | Description |
|--------|------|-------------|
| POST | /inputs | Creates an input. |
| DELETE | /inputs/{inputName} | Deletes an input. |
| GET | /inputs/{inputName} | Describes an input. |
| GET | /inputs | Lists the inputs you have created. |
| PUT | /inputs/{inputName} | Updates an input. |

### analysis
| Method | Path | Description |
|--------|------|-------------|
| GET | /analysis/detector-models/{analysisId} | Retrieves runtime information about a detector model analysis.  After AWS IoT Events starts analyzing your detector model, you have up to 24 hours to retrieve the analysis results. |
| GET | /analysis/detector-models/{analysisId}/results | Retrieves one or more analysis results of the detector model.  After AWS IoT Events starts analyzing your detector model, you have up to 24 hours to retrieve the analysis results. |
| POST | /analysis/detector-models/ | Performs an analysis of your detector model. For more information, see Troubleshooting a detector model in the AWS IoT Events Developer Guide. |

### logging
| Method | Path | Description |
|--------|------|-------------|
| GET | /logging | Retrieves the current settings of the AWS IoT Events logging options. |
| PUT | /logging | Sets or updates the AWS IoT Events logging options. If you update the value of any loggingOptions field, it takes up to one minute for the change to take effect. If you change the policy attached to the role you specified in the roleArn field (for example, to correct an invalid policy), it takes up to five minutes for that change to take effect. |

### input-routings
| Method | Path | Description |
|--------|------|-------------|
| POST | /input-routings | Lists one or more input routings. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags | Lists the tags (metadata) you have assigned to the resource. |
| POST | /tags | Adds to or modifies the tags of the given resource. Tags are metadata that can be used to manage a resource. |
| DELETE | /tags | Removes the given tags (metadata) from the resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a alarm-model?" -> POST /alarm-models
- "Create a detector-model?" -> POST /detector-models
- "Create a input?" -> POST /inputs
- "Delete a alarm-model?" -> DELETE /alarm-models/{alarmModelName}
- "Delete a detector-model?" -> DELETE /detector-models/{detectorModelName}
- "Delete a input?" -> DELETE /inputs/{inputName}
- "Get alarm-model details?" -> GET /alarm-models/{alarmModelName}
- "Get detector-model details?" -> GET /detector-models/{detectorModelName}
- "Get detector-model details?" -> GET /analysis/detector-models/{analysisId}
- "Get input details?" -> GET /inputs/{inputName}
- "List all logging?" -> GET /logging
- "List all results?" -> GET /analysis/detector-models/{analysisId}/results
- "List all versions?" -> GET /alarm-models/{alarmModelName}/versions
- "List all alarm-models?" -> GET /alarm-models
- "List all versions?" -> GET /detector-models/{detectorModelName}/versions
- "List all detector-models?" -> GET /detector-models
- "Create a input-routing?" -> POST /input-routings
- "List all inputs?" -> GET /inputs
- "List all tags?" -> GET /tags
- "Create a detector-model?" -> POST /analysis/detector-models/
- "Create a tag?" -> POST /tags
- "Update a input?" -> PUT /inputs/{inputName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
