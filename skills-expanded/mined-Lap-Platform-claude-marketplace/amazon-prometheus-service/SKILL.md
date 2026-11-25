---
name: amazon-prometheus-service
description: "Amazon Prometheus Service API skill. Use when working with Amazon Prometheus Service for workspaces, scrapers, scraperconfiguration. Covers 26 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Prometheus Service
API version: 2020-08-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /scraperconfiguration -- verify access
3. POST /workspaces/{workspaceId}/alertmanager/definition -- create first definition

## Endpoints

26 endpoints across 4 groups. See references/api-spec.lap for full details.

### workspaces
| Method | Path | Description |
|--------|------|-------------|
| POST | /workspaces/{workspaceId}/alertmanager/definition | The CreateAlertManagerDefinition operation creates the alert manager definition in a workspace. If a workspace already has an alert manager definition, don't use this operation to update it. Instead, use PutAlertManagerDefinition. |
| POST | /workspaces/{workspaceId}/logging | The CreateLoggingConfiguration operation creates a logging configuration for the workspace. Use this operation to set the CloudWatch log group to which the logs will be published to. |
| POST | /workspaces/{workspaceId}/rulegroupsnamespaces | The CreateRuleGroupsNamespace operation creates a rule groups namespace within a workspace. A rule groups namespace is associated with exactly one rules file. A workspace can have multiple rule groups namespaces. Use this operation only to create new rule groups namespaces. To update an existing rule groups namespace, use PutRuleGroupsNamespace. |
| POST | /workspaces | Creates a Prometheus workspace. A workspace is a logical space dedicated to the storage and querying of Prometheus metrics. You can have one or more workspaces in each Region in your account. |
| DELETE | /workspaces/{workspaceId}/alertmanager/definition | Deletes the alert manager definition from a workspace. |
| DELETE | /workspaces/{workspaceId}/logging | Deletes the logging configuration for a workspace. |
| DELETE | /workspaces/{workspaceId}/rulegroupsnamespaces/{name} | Deletes one rule groups namespace and its associated rule groups definition. |
| DELETE | /workspaces/{workspaceId} | Deletes an existing workspace.   When you delete a workspace, the data that has been ingested into it is not immediately deleted. It will be permanently deleted within one month. |
| GET | /workspaces/{workspaceId}/alertmanager/definition | Retrieves the full information about the alert manager definition for a workspace. |
| GET | /workspaces/{workspaceId}/logging | Returns complete information about the current logging configuration of the workspace. |
| GET | /workspaces/{workspaceId}/rulegroupsnamespaces/{name} | Returns complete information about one rule groups namespace. To retrieve a list of rule groups namespaces, use ListRuleGroupsNamespaces. |
| GET | /workspaces/{workspaceId} | Returns information about an existing workspace. |
| GET | /workspaces/{workspaceId}/rulegroupsnamespaces | Returns a list of rule groups namespaces in a workspace. |
| GET | /workspaces | Lists all of the Amazon Managed Service for Prometheus workspaces in your account. This includes workspaces being created or deleted. |
| PUT | /workspaces/{workspaceId}/alertmanager/definition | Updates an existing alert manager definition in a workspace. If the workspace does not already have an alert manager definition, don't use this operation to create it. Instead, use CreateAlertManagerDefinition. |
| PUT | /workspaces/{workspaceId}/rulegroupsnamespaces/{name} | Updates an existing rule groups namespace within a workspace. A rule groups namespace is associated with exactly one rules file. A workspace can have multiple rule groups namespaces. Use this operation only to update existing rule groups namespaces. To create a new rule groups namespace, use CreateRuleGroupsNamespace. You can't use this operation to add tags to an existing rule groups namespace. Instead, use TagResource. |
| PUT | /workspaces/{workspaceId}/logging | Updates the log group ARN or the workspace ID of the current logging configuration. |
| POST | /workspaces/{workspaceId}/alias | Updates the alias of an existing workspace. |

### scrapers
| Method | Path | Description |
|--------|------|-------------|
| POST | /scrapers | The CreateScraper operation creates a scraper to collect metrics. A scraper pulls metrics from Prometheus-compatible sources within an Amazon EKS cluster, and sends them to your Amazon Managed Service for Prometheus workspace. You can configure the scraper to control what metrics are collected, and what transformations are applied prior to sending them to your workspace. If needed, an IAM role will be created for you that gives Amazon Managed Service for Prometheus access to the metrics in your cluster. For more information, see Using roles for scraping metrics from EKS in the Amazon Managed Service for Prometheus User Guide. You cannot update a scraper. If you want to change the configuration of the scraper, create a new scraper and delete the old one. The scrapeConfiguration parameter contains the base64-encoded version of the YAML configuration file.  For more information about collectors, including what metrics are collected, and how to configure the scraper, see Amazon Web Services managed collectors in the Amazon Managed Service for Prometheus User Guide. |
| DELETE | /scrapers/{scraperId} | The DeleteScraper operation deletes one scraper, and stops any metrics collection that the scraper performs. |
| GET | /scrapers/{scraperId} | The DescribeScraper operation displays information about an existing scraper. |
| GET | /scrapers | The ListScrapers operation lists all of the scrapers in your account. This includes scrapers being created or deleted. You can optionally filter the returned list. |

### scraperconfiguration
| Method | Path | Description |
|--------|------|-------------|
| GET | /scraperconfiguration | The GetDefaultScraperConfiguration operation returns the default scraper configuration used when Amazon EKS creates a scraper for you. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | The ListTagsForResource operation returns the tags that are associated with an Amazon Managed Service for Prometheus resource. Currently, the only resources that can be tagged are workspaces and rule groups namespaces. |
| POST | /tags/{resourceArn} | The TagResource operation associates tags with an Amazon Managed Service for Prometheus resource. The only resources that can be tagged are workspaces and rule groups namespaces.  If you specify a new tag key for the resource, this tag is appended to the list of tags associated with the resource. If you specify a tag key that is already associated with the resource, the new tag value that you specify replaces the previous value for that tag. |
| DELETE | /tags/{resourceArn} | Removes the specified tags from an Amazon Managed Service for Prometheus resource. The only resources that can be tagged are workspaces and rule groups namespaces. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a definition?" -> POST /workspaces/{workspaceId}/alertmanager/definition
- "Create a logging?" -> POST /workspaces/{workspaceId}/logging
- "Create a rulegroupsnamespace?" -> POST /workspaces/{workspaceId}/rulegroupsnamespaces
- "Create a scraper?" -> POST /scrapers
- "Create a workspace?" -> POST /workspaces
- "Delete a rulegroupsnamespace?" -> DELETE /workspaces/{workspaceId}/rulegroupsnamespaces/{name}
- "Delete a scraper?" -> DELETE /scrapers/{scraperId}
- "Delete a workspace?" -> DELETE /workspaces/{workspaceId}
- "List all definition?" -> GET /workspaces/{workspaceId}/alertmanager/definition
- "List all logging?" -> GET /workspaces/{workspaceId}/logging
- "Get rulegroupsnamespace details?" -> GET /workspaces/{workspaceId}/rulegroupsnamespaces/{name}
- "Get scraper details?" -> GET /scrapers/{scraperId}
- "Get workspace details?" -> GET /workspaces/{workspaceId}
- "List all scraperconfiguration?" -> GET /scraperconfiguration
- "List all rulegroupsnamespaces?" -> GET /workspaces/{workspaceId}/rulegroupsnamespaces
- "List all scrapers?" -> GET /scrapers
- "Get tag details?" -> GET /tags/{resourceArn}
- "List all workspaces?" -> GET /workspaces
- "Update a rulegroupsnamespace?" -> PUT /workspaces/{workspaceId}/rulegroupsnamespaces/{name}
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Create a alia?" -> POST /workspaces/{workspaceId}/alias
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
