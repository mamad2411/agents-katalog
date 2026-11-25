---
name: msk-inspect-cluster
description: Inspect Amazon MSK cluster type, broker topology, Kafka version, networking, storage, authentication, encryption, monitoring, configuration, and environment context. Use as the primary entry point for an Amazon MSK Provisioned, Express, or Serverless cluster when the investigation scope is not yet known.
---

# Inspect Cluster

1. Read `.digital-platform-ai/kafka-aws.yaml`, service metadata, environments, and relevant instructions.
2. Resolve AWS account, region, cluster ARN/name, cluster type, and consuming applications.
3. Inspect broker/serverless topology, Kafka version, VPC/subnets, security groups, authentication, encryption, storage, monitoring, and configuration.
4. Identify whether the issue is capacity, broker/storage, networking, authentication, topic/partition, producer, consumer, connector, replication, or integration related.
5. Route to focused `msk-*` skills.
6. Do not modify production resources unless explicitly authorized.

## Output
- Cluster Context
- Topology and Configuration
- Security/Network State
- Scope Assessment
- Recommended Next Skill
