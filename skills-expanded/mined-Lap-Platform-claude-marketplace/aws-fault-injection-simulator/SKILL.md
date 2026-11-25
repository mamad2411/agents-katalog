---
name: aws-fault-injection-simulator
description: "AWS Fault Injection Simulator API skill. Use when working with AWS Fault Injection Simulator for experimentTemplates, actions, experiments. Covers 26 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Fault Injection Simulator
API version: 2020-12-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /actions -- verify access
3. POST /experimentTemplates -- create first experimentTemplates

## Endpoints

26 endpoints across 6 groups. See references/api-spec.lap for full details.

### experimentTemplates
| Method | Path | Description |
|--------|------|-------------|
| POST | /experimentTemplates | Creates an experiment template.  An experiment template includes the following components:    Targets: A target can be a specific resource in your Amazon Web Services environment, or one or more resources that match criteria that you specify, for example, resources that have specific tags.    Actions: The actions to carry out on the target. You can specify multiple actions, the duration of each action, and when to start each action during an experiment.    Stop conditions: If a stop condition is triggered while an experiment is running, the experiment is automatically stopped. You can define a stop condition as a CloudWatch alarm.   For more information, see experiment templates in the Fault Injection Service User Guide. |
| POST | /experimentTemplates/{id}/targetAccountConfigurations/{accountId} | Creates a target account configuration for the experiment template. A target account configuration is required when accountTargeting of experimentOptions is set to multi-account. For more information, see experiment options in the Fault Injection Service User Guide. |
| DELETE | /experimentTemplates/{id} | Deletes the specified experiment template. |
| DELETE | /experimentTemplates/{id}/targetAccountConfigurations/{accountId} | Deletes the specified target account configuration of the experiment template. |
| GET | /experimentTemplates/{id} | Gets information about the specified experiment template. |
| GET | /experimentTemplates/{id}/targetAccountConfigurations/{accountId} | Gets information about the specified target account configuration of the experiment template. |
| GET | /experimentTemplates | Lists your experiment templates. |
| GET | /experimentTemplates/{id}/targetAccountConfigurations | Lists the target account configurations of the specified experiment template. |
| PATCH | /experimentTemplates/{id} | Updates the specified experiment template. |
| PATCH | /experimentTemplates/{id}/targetAccountConfigurations/{accountId} | Updates the target account configuration for the specified experiment template. |

### actions
| Method | Path | Description |
|--------|------|-------------|
| GET | /actions/{id} | Gets information about the specified FIS action. |
| GET | /actions | Lists the available FIS actions. |

### experiments
| Method | Path | Description |
|--------|------|-------------|
| GET | /experiments/{id} | Gets information about the specified experiment. |
| GET | /experiments/{id}/targetAccountConfigurations/{accountId} | Gets information about the specified target account configuration of the experiment. |
| GET | /experiments/{id}/resolvedTargets | Lists the resolved targets information of the specified experiment. |
| GET | /experiments/{id}/targetAccountConfigurations | Lists the target account configurations of the specified experiment. |
| GET | /experiments | Lists your experiments. |
| POST | /experiments | Starts running an experiment from the specified experiment template. |
| DELETE | /experiments/{id} | Stops the specified experiment. |

### safetyLevers
| Method | Path | Description |
|--------|------|-------------|
| GET | /safetyLevers/{id} | Gets information about the specified safety lever. |
| PATCH | /safetyLevers/{id}/state | Updates the specified safety lever state. |

### targetResourceTypes
| Method | Path | Description |
|--------|------|-------------|
| GET | /targetResourceTypes/{resourceType} | Gets information about the specified resource type. |
| GET | /targetResourceTypes | Lists the target resource types. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Lists the tags for the specified resource. |
| POST | /tags/{resourceArn} | Applies the specified tags to the specified resource. |
| DELETE | /tags/{resourceArn} | Removes the specified tags from the specified resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a experimentTemplate?" -> POST /experimentTemplates
- "Delete a experimentTemplate?" -> DELETE /experimentTemplates/{id}
- "Delete a targetAccountConfiguration?" -> DELETE /experimentTemplates/{id}/targetAccountConfigurations/{accountId}
- "Get action details?" -> GET /actions/{id}
- "Get experiment details?" -> GET /experiments/{id}
- "Get targetAccountConfiguration details?" -> GET /experiments/{id}/targetAccountConfigurations/{accountId}
- "Get experimentTemplate details?" -> GET /experimentTemplates/{id}
- "Get safetyLever details?" -> GET /safetyLevers/{id}
- "Get targetAccountConfiguration details?" -> GET /experimentTemplates/{id}/targetAccountConfigurations/{accountId}
- "Get targetResourceType details?" -> GET /targetResourceTypes/{resourceType}
- "List all actions?" -> GET /actions
- "List all resolvedTargets?" -> GET /experiments/{id}/resolvedTargets
- "List all targetAccountConfigurations?" -> GET /experiments/{id}/targetAccountConfigurations
- "List all experimentTemplates?" -> GET /experimentTemplates
- "List all experiments?" -> GET /experiments
- "Get tag details?" -> GET /tags/{resourceArn}
- "List all targetAccountConfigurations?" -> GET /experimentTemplates/{id}/targetAccountConfigurations
- "List all targetResourceTypes?" -> GET /targetResourceTypes
- "Create a experiment?" -> POST /experiments
- "Delete a experiment?" -> DELETE /experiments/{id}
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Partially update a experimentTemplate?" -> PATCH /experimentTemplates/{id}
- "Partially update a targetAccountConfiguration?" -> PATCH /experimentTemplates/{id}/targetAccountConfigurations/{accountId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
