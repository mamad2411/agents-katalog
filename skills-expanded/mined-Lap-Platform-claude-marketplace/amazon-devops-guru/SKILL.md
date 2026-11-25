---
name: amazon-devops-guru
description: "Amazon DevOps Guru API skill. Use when working with Amazon DevOps Guru for channels, insights, accounts. Covers 31 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon DevOps Guru
API version: 2020-12-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /accounts/health -- verify access
3. POST /accounts/overview -- create first overview

## Endpoints

31 endpoints across 14 groups. See references/api-spec.lap for full details.

### channels
| Method | Path | Description |
|--------|------|-------------|
| PUT | /channels | Adds a notification channel to DevOps Guru. A notification channel is used to notify you about important DevOps Guru events, such as when an insight is generated.  If you use an Amazon SNS topic in another account, you must attach a policy to it that grants DevOps Guru permission to send it notifications. DevOps Guru adds the required policy on your behalf to send notifications using Amazon SNS in your account. DevOps Guru only supports standard SNS topics. For more information, see Permissions for Amazon SNS topics. If you use an Amazon SNS topic that is encrypted by an Amazon Web Services Key Management Service customer-managed key (CMK), then you must add permissions to the CMK. For more information, see Permissions for Amazon Web Services KMS–encrypted Amazon SNS topics. |
| POST | /channels | Returns a list of notification channels configured for DevOps Guru. Each notification channel is used to notify you when DevOps Guru generates an insight that contains information about how to improve your operations. The one supported notification channel is Amazon Simple Notification Service (Amazon SNS). |
| DELETE | /channels/{Id} | Removes a notification channel from DevOps Guru. A notification channel is used to notify you when DevOps Guru generates an insight that contains information about how to improve your operations. |

### insights
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /insights/{Id} | Deletes the insight along with the associated anomalies, events and recommendations. |
| GET | /insights/{Id} | Returns details about an insight that you specify using its ID. |
| POST | /insights | Returns a list of insights in your Amazon Web Services account. You can specify which insights are returned by their start time and status (ONGOING, CLOSED, or ANY). |
| POST | /insights/search | Returns a list of insights in your Amazon Web Services account. You can specify which insights are returned by their start time, one or more statuses (ONGOING or CLOSED), one or more severities (LOW, MEDIUM, and HIGH), and type (REACTIVE or PROACTIVE).   Use the Filters parameter to specify status and severity search parameters. Use the Type parameter to specify REACTIVE or PROACTIVE in your search. |

### accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /accounts/health | Returns the number of open reactive insights, the number of open proactive insights, and the number of metrics analyzed in your Amazon Web Services account. Use these numbers to gauge the health of operations in your Amazon Web Services account. |
| POST | /accounts/overview | For the time range passed in, returns the number of open reactive insight that were created, the number of open proactive insights that were created, and the Mean Time to Recover (MTTR) for all closed reactive insights. |
| GET | /accounts/health/resource-collection/{ResourceCollectionType} | Returns the number of open proactive insights, open reactive insights, and the Mean Time to Recover (MTTR) for all closed insights in resource collections in your account. You specify the type of Amazon Web Services resources collection. The two types of Amazon Web Services resource collections supported are Amazon Web Services CloudFormation stacks and Amazon Web Services resources that contain the same Amazon Web Services tag. DevOps Guru can be configured to analyze the Amazon Web Services resources that are defined in the stacks or that are tagged using the same tag key. You can specify up to 500 Amazon Web Services CloudFormation stacks. |

### anomalies
| Method | Path | Description |
|--------|------|-------------|
| GET | /anomalies/{Id} | Returns details about an anomaly that you specify using its ID. |
| POST | /anomalies/insight/{InsightId} | Returns a list of the anomalies that belong to an insight that you specify using its ID. |

### event-sources
| Method | Path | Description |
|--------|------|-------------|
| POST | /event-sources | Returns the integration status of services that are integrated with DevOps Guru as Consumer via EventBridge. The one service that can be integrated with DevOps Guru is Amazon CodeGuru Profiler, which can produce proactive recommendations which can be stored and viewed in DevOps Guru. |
| PUT | /event-sources | Enables or disables integration with a service that can be integrated with DevOps Guru. The one service that can be integrated with DevOps Guru is Amazon CodeGuru Profiler, which can produce proactive recommendations which can be stored and viewed in DevOps Guru. |

### feedback
| Method | Path | Description |
|--------|------|-------------|
| POST | /feedback | Returns the most recent feedback submitted in the current Amazon Web Services account and Region. |
| PUT | /feedback | Collects customer feedback about the specified insight. |

### organization
| Method | Path | Description |
|--------|------|-------------|
| POST | /organization/health | Returns active insights, predictive insights, and resource hours analyzed in last hour. |
| POST | /organization/overview | Returns an overview of your organization's history based on the specified time range. The overview includes the total reactive and proactive insights. |
| POST | /organization/health/resource-collection | Provides an overview of your system's health. If additional member accounts are part of your organization, you can filter those accounts using the AccountIds field. |
| POST | /organization/insights | Returns a list of insights associated with the account or OU Id. |
| POST | /organization/insights/search | Returns a list of insights in your organization. You can specify which insights are returned by their start time, one or more statuses (ONGOING, CLOSED, and CLOSED), one or more severities (LOW, MEDIUM, and HIGH), and type (REACTIVE or PROACTIVE).   Use the Filters parameter to specify status and severity search parameters. Use the Type parameter to specify REACTIVE or PROACTIVE in your search. |

### service-integrations
| Method | Path | Description |
|--------|------|-------------|
| GET | /service-integrations | Returns the integration status of services that are integrated with DevOps Guru. The one service that can be integrated with DevOps Guru is Amazon Web Services Systems Manager, which can be used to create an OpsItem for each generated insight. |
| PUT | /service-integrations | Enables or disables integration with a service that can be integrated with DevOps Guru. The one service that can be integrated with DevOps Guru is Amazon Web Services Systems Manager, which can be used to create an OpsItem for each generated insight. |

### cost-estimation
| Method | Path | Description |
|--------|------|-------------|
| GET | /cost-estimation | Returns an estimate of the monthly cost for DevOps Guru to analyze your Amazon Web Services resources. For more information, see Estimate your Amazon DevOps Guru costs and Amazon DevOps Guru pricing. |
| PUT | /cost-estimation | Starts the creation of an estimate of the monthly cost to analyze your Amazon Web Services resources. |

### resource-collections
| Method | Path | Description |
|--------|------|-------------|
| GET | /resource-collections/{ResourceCollectionType} | Returns lists Amazon Web Services resources that are of the specified resource collection type. The two types of Amazon Web Services resource collections supported are Amazon Web Services CloudFormation stacks and Amazon Web Services resources that contain the same Amazon Web Services tag. DevOps Guru can be configured to analyze the Amazon Web Services resources that are defined in the stacks or that are tagged using the same tag key. You can specify up to 500 Amazon Web Services CloudFormation stacks. |
| PUT | /resource-collections | Updates the collection of resources that DevOps Guru analyzes. The two types of Amazon Web Services resource collections supported are Amazon Web Services CloudFormation stacks and Amazon Web Services resources that contain the same Amazon Web Services tag. DevOps Guru can be configured to analyze the Amazon Web Services resources that are defined in the stacks or that are tagged using the same tag key. You can specify up to 500 Amazon Web Services CloudFormation stacks. This method also creates the IAM role required for you to use DevOps Guru. |

### list-log-anomalies
| Method | Path | Description |
|--------|------|-------------|
| POST | /list-log-anomalies | Returns the list of log groups that contain log anomalies. |

### events
| Method | Path | Description |
|--------|------|-------------|
| POST | /events | Returns a list of the events emitted by the resources that are evaluated by DevOps Guru. You can use filters to specify which events are returned. |

### monitoredResources
| Method | Path | Description |
|--------|------|-------------|
| POST | /monitoredResources | Returns the list of all log groups that are being monitored and tagged by DevOps Guru. |

### recommendations
| Method | Path | Description |
|--------|------|-------------|
| POST | /recommendations | Returns a list of a specified insight's recommendations. Each recommendation includes a list of related metrics and a list of related events. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Delete a insight?" -> DELETE /insights/{Id}
- "List all health?" -> GET /accounts/health
- "Create a overview?" -> POST /accounts/overview
- "Get anomaly details?" -> GET /anomalies/{Id}
- "Create a event-source?" -> POST /event-sources
- "Create a feedback?" -> POST /feedback
- "Get insight details?" -> GET /insights/{Id}
- "Create a health?" -> POST /organization/health
- "Create a overview?" -> POST /organization/overview
- "Create a resource-collection?" -> POST /organization/health/resource-collection
- "Get resource-collection details?" -> GET /accounts/health/resource-collection/{ResourceCollectionType}
- "List all service-integrations?" -> GET /service-integrations
- "List all cost-estimation?" -> GET /cost-estimation
- "Get resource-collection details?" -> GET /resource-collections/{ResourceCollectionType}
- "Create a list-log-anomaly?" -> POST /list-log-anomalies
- "Create a event?" -> POST /events
- "Create a insight?" -> POST /insights
- "Create a monitoredResource?" -> POST /monitoredResources
- "Create a channel?" -> POST /channels
- "Create a insight?" -> POST /organization/insights
- "Create a recommendation?" -> POST /recommendations
- "Delete a channel?" -> DELETE /channels/{Id}
- "Create a search?" -> POST /insights/search
- "Create a search?" -> POST /organization/insights/search
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
