---
name: managed-streaming-for-kafka
description: "Managed Streaming for Kafka API skill. Use when working with Managed Streaming for Kafka for clusters, api, configurations. Covers 52 endpoints."
version: 1.0.0
generator: lapsh
---

# Managed Streaming for Kafka
API version: 2018-11-14

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /v1/compatible-kafka-versions -- verify access
3. POST /v1/clusters/{clusterArn}/scram-secrets -- create first scram-secrets

## Endpoints

52 endpoints across 10 groups. See references/api-spec.lap for full details.

### clusters
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/clusters/{clusterArn}/scram-secrets | Associates one or more Scram Secrets with an Amazon MSK cluster. |
| POST | /v1/clusters | Creates a new MSK cluster. |
| DELETE | /v1/clusters/{clusterArn} | Deletes the MSK cluster specified by the Amazon Resource Name (ARN) in the request. |
| DELETE | /v1/clusters/{clusterArn}/policy | Deletes the MSK cluster policy specified by the Amazon Resource Name (ARN) in the request. |
| GET | /v1/clusters/{clusterArn} | Returns a description of the MSK cluster whose Amazon Resource Name (ARN) is specified in the request. |
| PATCH | /v1/clusters/{clusterArn}/scram-secrets | Disassociates one or more Scram Secrets from an Amazon MSK cluster. |
| GET | /v1/clusters/{clusterArn}/bootstrap-brokers | A list of brokers that a client application can use to bootstrap. |
| GET | /v1/clusters/{clusterArn}/policy | Get the MSK cluster policy specified by the Amazon Resource Name (ARN) in the request. |
| GET | /v1/clusters/{clusterArn}/operations | Returns a list of all the operations that have been performed on the specified MSK cluster. |
| GET | /v1/clusters | Returns a list of all the MSK clusters in the current Region. |
| GET | /v1/clusters/{clusterArn}/nodes | Returns a list of the broker nodes in the cluster. |
| GET | /v1/clusters/{clusterArn}/scram-secrets | Returns a list of the Scram Secrets associated with an Amazon MSK cluster. |
| GET | /v1/clusters/{clusterArn}/client-vpc-connections | Returns a list of all the VPC connections in this Region. |
| PUT | /v1/clusters/{clusterArn}/client-vpc-connection | Returns empty response. |
| PUT | /v1/clusters/{clusterArn}/policy | Creates or updates the MSK cluster policy specified by the cluster Amazon Resource Name (ARN) in the request. |
| PUT | /v1/clusters/{clusterArn}/reboot-broker | Reboots brokers. |
| PUT | /v1/clusters/{clusterArn}/nodes/count | Updates the number of broker nodes in the cluster. |
| PUT | /v1/clusters/{clusterArn}/nodes/type | Updates EC2 instance type. |
| PUT | /v1/clusters/{clusterArn}/nodes/storage | Updates the EBS storage associated with MSK brokers. |
| PUT | /v1/clusters/{clusterArn}/connectivity | Updates the cluster's connectivity configuration. |
| PUT | /v1/clusters/{clusterArn}/configuration | Updates the cluster with the configuration that is specified in the request body. |
| PUT | /v1/clusters/{clusterArn}/version | Updates the Apache Kafka version for the cluster. |
| PUT | /v1/clusters/{clusterArn}/monitoring | Updates the monitoring settings for the cluster. You can use this operation to specify which Apache Kafka metrics you want Amazon MSK to send to Amazon CloudWatch. You can also specify settings for open monitoring with Prometheus. |
| PATCH | /v1/clusters/{clusterArn}/security | Updates the security settings for the cluster. You can use this operation to specify encryption and authentication on existing clusters. |
| PUT | /v1/clusters/{clusterArn}/storage | Updates cluster broker volume size (or) sets cluster storage mode to TIERED. |

### api
| Method | Path | Description |
|--------|------|-------------|
| POST | /api/v2/clusters | Creates a new MSK cluster. |
| GET | /api/v2/clusters/{clusterArn} | Returns a description of the MSK cluster whose Amazon Resource Name (ARN) is specified in the request. |
| GET | /api/v2/operations/{clusterOperationArn} | Returns a description of the cluster operation specified by the ARN. |
| GET | /api/v2/clusters/{clusterArn}/operations | Returns a list of all the operations that have been performed on the specified MSK cluster. |
| GET | /api/v2/clusters | Returns a list of all the MSK clusters in the current Region. |

### configurations
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/configurations | Creates a new MSK configuration. |
| DELETE | /v1/configurations/{arn} | Deletes an MSK Configuration. |
| GET | /v1/configurations/{arn} | Returns a description of this MSK configuration. |
| GET | /v1/configurations/{arn}/revisions/{revision} | Returns a description of this revision of the configuration. |
| GET | /v1/configurations/{arn}/revisions | Returns a list of all the MSK configurations in this Region. |
| GET | /v1/configurations | Returns a list of all the MSK configurations in this Region. |
| PUT | /v1/configurations/{arn} | Updates an MSK configuration. |

### replication
| Method | Path | Description |
|--------|------|-------------|
| POST | /replication/v1/replicators | Creates the replicator. |
| DELETE | /replication/v1/replicators/{replicatorArn} | Deletes a replicator. |
| GET | /replication/v1/replicators/{replicatorArn} | Describes a replicator. |
| GET | /replication/v1/replicators | Lists the replicators. |
| PUT | /replication/v1/replicators/{replicatorArn}/replication-info | Updates replication info of a replicator. |

### vpc-connection
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/vpc-connection | Creates a new MSK VPC connection. |
| DELETE | /v1/vpc-connection/{arn} | Deletes a MSK VPC connection. |
| GET | /v1/vpc-connection/{arn} | Returns a description of this MSK VPC connection. |

### operations
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/operations/{clusterOperationArn} | Returns a description of the cluster operation specified by the ARN. |

### compatible-kafka-versions
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/compatible-kafka-versions | Gets the Apache Kafka versions to which you can update the MSK cluster. |

### kafka-versions
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/kafka-versions | Returns a list of Apache Kafka versions. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/tags/{resourceArn} | Returns a list of the tags associated with the specified resource. |
| POST | /v1/tags/{resourceArn} | Adds tags to the specified MSK resource. |
| DELETE | /v1/tags/{resourceArn} | Removes the tags associated with the keys that are provided in the query. |

### vpc-connections
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/vpc-connections | Returns a list of all the VPC connections in this Region. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a scram-secret?" -> POST /v1/clusters/{clusterArn}/scram-secrets
- "Create a cluster?" -> POST /v1/clusters
- "Create a cluster?" -> POST /api/v2/clusters
- "Create a configuration?" -> POST /v1/configurations
- "Create a replicator?" -> POST /replication/v1/replicators
- "Create a vpc-connection?" -> POST /v1/vpc-connection
- "Delete a cluster?" -> DELETE /v1/clusters/{clusterArn}
- "Delete a configuration?" -> DELETE /v1/configurations/{arn}
- "Delete a replicator?" -> DELETE /replication/v1/replicators/{replicatorArn}
- "Delete a vpc-connection?" -> DELETE /v1/vpc-connection/{arn}
- "Get cluster details?" -> GET /v1/clusters/{clusterArn}
- "Get cluster details?" -> GET /api/v2/clusters/{clusterArn}
- "Get operation details?" -> GET /v1/operations/{clusterOperationArn}
- "Get operation details?" -> GET /api/v2/operations/{clusterOperationArn}
- "Get configuration details?" -> GET /v1/configurations/{arn}
- "Get revision details?" -> GET /v1/configurations/{arn}/revisions/{revision}
- "Get replicator details?" -> GET /replication/v1/replicators/{replicatorArn}
- "Get vpc-connection details?" -> GET /v1/vpc-connection/{arn}
- "List all bootstrap-brokers?" -> GET /v1/clusters/{clusterArn}/bootstrap-brokers
- "List all compatible-kafka-versions?" -> GET /v1/compatible-kafka-versions
- "List all policy?" -> GET /v1/clusters/{clusterArn}/policy
- "List all operations?" -> GET /v1/clusters/{clusterArn}/operations
- "List all operations?" -> GET /api/v2/clusters/{clusterArn}/operations
- "List all clusters?" -> GET /v1/clusters
- "List all clusters?" -> GET /api/v2/clusters
- "List all revisions?" -> GET /v1/configurations/{arn}/revisions
- "List all configurations?" -> GET /v1/configurations
- "List all kafka-versions?" -> GET /v1/kafka-versions
- "List all nodes?" -> GET /v1/clusters/{clusterArn}/nodes
- "List all replicators?" -> GET /replication/v1/replicators
- "List all scram-secrets?" -> GET /v1/clusters/{clusterArn}/scram-secrets
- "Get tag details?" -> GET /v1/tags/{resourceArn}
- "List all client-vpc-connections?" -> GET /v1/clusters/{clusterArn}/client-vpc-connections
- "List all vpc-connections?" -> GET /v1/vpc-connections
- "Delete a tag?" -> DELETE /v1/tags/{resourceArn}
- "Update a configuration?" -> PUT /v1/configurations/{arn}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
