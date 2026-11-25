---
name: amazonmq
description: "AmazonMQ API skill. Use when working with AmazonMQ for brokers, configurations, tags. Covers 23 endpoints."
version: 1.0.0
generator: lapsh
---

# AmazonMQ
API version: 2017-11-27

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /v1/broker-engine-types -- verify access
3. POST /v1/brokers -- create first brokers

## Endpoints

23 endpoints across 5 groups. See references/api-spec.lap for full details.

### brokers
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/brokers | Creates a broker. Note: This API is asynchronous. To create a broker, you must either use the AmazonMQFullAccess IAM policy or include the following EC2 permissions in your IAM policy. ec2:CreateNetworkInterface This permission is required to allow Amazon MQ to create an elastic network interface (ENI) on behalf of your account. ec2:CreateNetworkInterfacePermission This permission is required to attach the ENI to the broker instance. ec2:DeleteNetworkInterface ec2:DeleteNetworkInterfacePermission ec2:DetachNetworkInterface ec2:DescribeInternetGateways ec2:DescribeNetworkInterfaces ec2:DescribeNetworkInterfacePermissions ec2:DescribeRouteTables ec2:DescribeSecurityGroups ec2:DescribeSubnets ec2:DescribeVpcs For more information, see Create an IAM User and Get Your Amazon Web Services Credentials and Never Modify or Delete the Amazon MQ Elastic Network Interface in the Amazon MQ Developer Guide. |
| POST | /v1/brokers/{broker-id}/users/{username} | Creates an ActiveMQ user. Do not add personally identifiable information (PII) or other confidential or sensitive information in broker usernames. Broker usernames are accessible to other Amazon Web Services services, including CloudWatch Logs. Broker usernames are not intended to be used for private or sensitive data. |
| DELETE | /v1/brokers/{broker-id} | Deletes a broker. Note: This API is asynchronous. |
| DELETE | /v1/brokers/{broker-id}/users/{username} | Deletes an ActiveMQ user. |
| GET | /v1/brokers/{broker-id} | Returns information about the specified broker. |
| GET | /v1/brokers/{broker-id}/users/{username} | Returns information about an ActiveMQ user. |
| GET | /v1/brokers | Returns a list of all brokers. |
| GET | /v1/brokers/{broker-id}/users | Returns a list of all ActiveMQ users. |
| POST | /v1/brokers/{broker-id}/promote | Promotes a data replication replica broker to the primary broker role. |
| POST | /v1/brokers/{broker-id}/reboot | Reboots a broker. Note: This API is asynchronous. |
| PUT | /v1/brokers/{broker-id} | Adds a pending configuration change to a broker. |
| PUT | /v1/brokers/{broker-id}/users/{username} | Updates the information for an ActiveMQ user. |

### configurations
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/configurations | Creates a new configuration for the specified configuration name. Amazon MQ uses the default configuration (the engine type and version). |
| GET | /v1/configurations/{configuration-id} | Returns information about the specified configuration. |
| GET | /v1/configurations/{configuration-id}/revisions/{configuration-revision} | Returns the specified configuration revision for the specified configuration. |
| GET | /v1/configurations/{configuration-id}/revisions | Returns a list of all revisions for the specified configuration. |
| GET | /v1/configurations | Returns a list of all configurations. |
| PUT | /v1/configurations/{configuration-id} | Updates the specified configuration. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/tags/{resource-arn} | Add a tag to a resource. |
| DELETE | /v1/tags/{resource-arn} | Removes a tag from a resource. |
| GET | /v1/tags/{resource-arn} | Lists tags for a resource. |

### broker-engine-types
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/broker-engine-types | Describe available engine types and versions. |

### broker-instance-options
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/broker-instance-options | Describe available broker instance options. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a broker?" -> POST /v1/brokers
- "Create a configuration?" -> POST /v1/configurations
- "Delete a broker?" -> DELETE /v1/brokers/{broker-id}
- "Delete a tag?" -> DELETE /v1/tags/{resource-arn}
- "Delete a user?" -> DELETE /v1/brokers/{broker-id}/users/{username}
- "Get broker details?" -> GET /v1/brokers/{broker-id}
- "List all broker-engine-types?" -> GET /v1/broker-engine-types
- "List all broker-instance-options?" -> GET /v1/broker-instance-options
- "Get configuration details?" -> GET /v1/configurations/{configuration-id}
- "Get revision details?" -> GET /v1/configurations/{configuration-id}/revisions/{configuration-revision}
- "Get user details?" -> GET /v1/brokers/{broker-id}/users/{username}
- "List all brokers?" -> GET /v1/brokers
- "List all revisions?" -> GET /v1/configurations/{configuration-id}/revisions
- "List all configurations?" -> GET /v1/configurations
- "Get tag details?" -> GET /v1/tags/{resource-arn}
- "List all users?" -> GET /v1/brokers/{broker-id}/users
- "Create a promote?" -> POST /v1/brokers/{broker-id}/promote
- "Create a reboot?" -> POST /v1/brokers/{broker-id}/reboot
- "Update a broker?" -> PUT /v1/brokers/{broker-id}
- "Update a configuration?" -> PUT /v1/configurations/{configuration-id}
- "Update a user?" -> PUT /v1/brokers/{broker-id}/users/{username}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
