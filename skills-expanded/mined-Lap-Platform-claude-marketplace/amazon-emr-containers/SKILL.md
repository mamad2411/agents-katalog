---
name: amazon-emr-containers
description: "Amazon EMR Containers API skill. Use when working with Amazon EMR Containers for virtualclusters, jobtemplates, securityconfigurations. Covers 23 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon EMR Containers
API version: 2020-10-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /jobtemplates -- verify access
3. POST /jobtemplates -- create first jobtemplates

## Endpoints

23 endpoints across 4 groups. See references/api-spec.lap for full details.

### virtualclusters
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /virtualclusters/{virtualClusterId}/jobruns/{jobRunId} | Cancels a job run. A job run is a unit of work, such as a Spark jar, PySpark script, or SparkSQL query, that you submit to Amazon EMR on EKS. |
| POST | /virtualclusters/{virtualClusterId}/endpoints | Creates a managed endpoint. A managed endpoint is a gateway that connects Amazon EMR Studio to Amazon EMR on EKS so that Amazon EMR Studio can communicate with your virtual cluster. |
| POST | /virtualclusters | Creates a virtual cluster. Virtual cluster is a managed entity on Amazon EMR on EKS. You can create, describe, list and delete virtual clusters. They do not consume any additional resource in your system. A single virtual cluster maps to a single Kubernetes namespace. Given this relationship, you can model virtual clusters the same way you model Kubernetes namespaces to meet your requirements. |
| DELETE | /virtualclusters/{virtualClusterId}/endpoints/{endpointId} | Deletes a managed endpoint. A managed endpoint is a gateway that connects Amazon EMR Studio to Amazon EMR on EKS so that Amazon EMR Studio can communicate with your virtual cluster. |
| DELETE | /virtualclusters/{virtualClusterId} | Deletes a virtual cluster. Virtual cluster is a managed entity on Amazon EMR on EKS. You can create, describe, list and delete virtual clusters. They do not consume any additional resource in your system. A single virtual cluster maps to a single Kubernetes namespace. Given this relationship, you can model virtual clusters the same way you model Kubernetes namespaces to meet your requirements. |
| GET | /virtualclusters/{virtualClusterId}/jobruns/{jobRunId} | Displays detailed information about a job run. A job run is a unit of work, such as a Spark jar, PySpark script, or SparkSQL query, that you submit to Amazon EMR on EKS. |
| GET | /virtualclusters/{virtualClusterId}/endpoints/{endpointId} | Displays detailed information about a managed endpoint. A managed endpoint is a gateway that connects Amazon EMR Studio to Amazon EMR on EKS so that Amazon EMR Studio can communicate with your virtual cluster. |
| GET | /virtualclusters/{virtualClusterId} | Displays detailed information about a specified virtual cluster. Virtual cluster is a managed entity on Amazon EMR on EKS. You can create, describe, list and delete virtual clusters. They do not consume any additional resource in your system. A single virtual cluster maps to a single Kubernetes namespace. Given this relationship, you can model virtual clusters the same way you model Kubernetes namespaces to meet your requirements. |
| POST | /virtualclusters/{virtualClusterId}/endpoints/{endpointId}/credentials | Generate a session token to connect to a managed endpoint. |
| GET | /virtualclusters/{virtualClusterId}/jobruns | Lists job runs based on a set of parameters. A job run is a unit of work, such as a Spark jar, PySpark script, or SparkSQL query, that you submit to Amazon EMR on EKS. |
| GET | /virtualclusters/{virtualClusterId}/endpoints | Lists managed endpoints based on a set of parameters. A managed endpoint is a gateway that connects Amazon EMR Studio to Amazon EMR on EKS so that Amazon EMR Studio can communicate with your virtual cluster. |
| GET | /virtualclusters | Lists information about the specified virtual cluster. Virtual cluster is a managed entity on Amazon EMR on EKS. You can create, describe, list and delete virtual clusters. They do not consume any additional resource in your system. A single virtual cluster maps to a single Kubernetes namespace. Given this relationship, you can model virtual clusters the same way you model Kubernetes namespaces to meet your requirements. |
| POST | /virtualclusters/{virtualClusterId}/jobruns | Starts a job run. A job run is a unit of work, such as a Spark jar, PySpark script, or SparkSQL query, that you submit to Amazon EMR on EKS. |

### jobtemplates
| Method | Path | Description |
|--------|------|-------------|
| POST | /jobtemplates | Creates a job template. Job template stores values of StartJobRun API request in a template and can be used to start a job run. Job template allows two use cases: avoid repeating recurring StartJobRun API request values, enforcing certain values in StartJobRun API request. |
| DELETE | /jobtemplates/{templateId} | Deletes a job template. Job template stores values of StartJobRun API request in a template and can be used to start a job run. Job template allows two use cases: avoid repeating recurring StartJobRun API request values, enforcing certain values in StartJobRun API request. |
| GET | /jobtemplates/{templateId} | Displays detailed information about a specified job template. Job template stores values of StartJobRun API request in a template and can be used to start a job run. Job template allows two use cases: avoid repeating recurring StartJobRun API request values, enforcing certain values in StartJobRun API request. |
| GET | /jobtemplates | Lists job templates based on a set of parameters. Job template stores values of StartJobRun API request in a template and can be used to start a job run. Job template allows two use cases: avoid repeating recurring StartJobRun API request values, enforcing certain values in StartJobRun API request. |

### securityconfigurations
| Method | Path | Description |
|--------|------|-------------|
| POST | /securityconfigurations | Creates a security configuration. Security configurations in Amazon EMR on EKS are templates for different security setups. You can use security configurations to configure the Lake Formation integration setup. You can also create a security configuration to re-use a security setup each time you create a virtual cluster. |
| GET | /securityconfigurations/{securityConfigurationId} | Displays detailed information about a specified security configuration. Security configurations in Amazon EMR on EKS are templates for different security setups. You can use security configurations to configure the Lake Formation integration setup. You can also create a security configuration to re-use a security setup each time you create a virtual cluster. |
| GET | /securityconfigurations | Lists security configurations based on a set of parameters. Security configurations in Amazon EMR on EKS are templates for different security setups. You can use security configurations to configure the Lake Formation integration setup. You can also create a security configuration to re-use a security setup each time you create a virtual cluster. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Lists the tags assigned to the resources. |
| POST | /tags/{resourceArn} | Assigns tags to resources. A tag is a label that you assign to an Amazon Web Services resource. Each tag consists of a key and an optional value, both of which you define. Tags enable you to categorize your Amazon Web Services resources by attributes such as purpose, owner, or environment. When you have many resources of the same type, you can quickly identify a specific resource based on the tags you've assigned to it. For example, you can define a set of tags for your Amazon EMR on EKS clusters to help you track each cluster's owner and stack level. We recommend that you devise a consistent set of tag keys for each resource type. You can then search and filter the resources based on the tags that you add. |
| DELETE | /tags/{resourceArn} | Removes tags from resources. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Delete a jobrun?" -> DELETE /virtualclusters/{virtualClusterId}/jobruns/{jobRunId}
- "Create a jobtemplate?" -> POST /jobtemplates
- "Create a endpoint?" -> POST /virtualclusters/{virtualClusterId}/endpoints
- "Create a securityconfiguration?" -> POST /securityconfigurations
- "Create a virtualcluster?" -> POST /virtualclusters
- "Delete a jobtemplate?" -> DELETE /jobtemplates/{templateId}
- "Delete a endpoint?" -> DELETE /virtualclusters/{virtualClusterId}/endpoints/{endpointId}
- "Delete a virtualcluster?" -> DELETE /virtualclusters/{virtualClusterId}
- "Get jobrun details?" -> GET /virtualclusters/{virtualClusterId}/jobruns/{jobRunId}
- "Get jobtemplate details?" -> GET /jobtemplates/{templateId}
- "Get endpoint details?" -> GET /virtualclusters/{virtualClusterId}/endpoints/{endpointId}
- "Get securityconfiguration details?" -> GET /securityconfigurations/{securityConfigurationId}
- "Get virtualcluster details?" -> GET /virtualclusters/{virtualClusterId}
- "Create a credential?" -> POST /virtualclusters/{virtualClusterId}/endpoints/{endpointId}/credentials
- "List all jobruns?" -> GET /virtualclusters/{virtualClusterId}/jobruns
- "List all jobtemplates?" -> GET /jobtemplates
- "List all endpoints?" -> GET /virtualclusters/{virtualClusterId}/endpoints
- "List all securityconfigurations?" -> GET /securityconfigurations
- "Get tag details?" -> GET /tags/{resourceArn}
- "List all virtualclusters?" -> GET /virtualclusters
- "Create a jobrun?" -> POST /virtualclusters/{virtualClusterId}/jobruns
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
