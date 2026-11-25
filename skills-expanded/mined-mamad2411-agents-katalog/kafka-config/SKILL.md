---
name: kafka-config
description: |
  Use when configuring Apache Kafka for production deployments.
  Triggers: "configure Kafka", "create Kafka topics", "optimize Kafka performance",
  "Kafka security setup", "Strimzi configuration", "Kafka consumer/producer config".
  NOT for: Kafka administration tasks, monitoring setup, or Kafka Connect configuration.
---

# Kafka Config

## Overview

Generates production-ready Kafka configurations for topics, consumers, and producers with appropriate performance tuning and security settings based on environment, deployment platform, and message volume requirements.

## Quick Start

To generate Kafka configurations, provide:
1. **Environment**: local, staging, production
2. **Deployment platform**: strimzi, confluent, redpanda, self-hosted
3. **Message volume**: low (<1K/sec), medium (1-10K/sec), high (>10K/sec)
4. **Retention period**: Days to retain messages
5. **Security requirements**: none, tls, sasl-scram, sasl-ssl

**Example requests:**
- "Configure Kafka topics for production with medium traffic"
- "Generate Strimzi topic config with TLS security"
- "Create consumer config for high-volume event processing"

## Configuration Workflow

### 1. Topic Configuration (Strimzi)

Use `assets/topic-template.yaml` as base. Key calculations:

**Partitions**: Based on message volume
- Low: 3 partitions
- Medium: 6 partitions
- High: 12 partitions

**Replication**: Based on environment
- Local: 1 replica
- Staging: 2 replicas
- Production: 3 replicas

**Retention**: Convert days to milliseconds (days × 86400000)

**min.insync.replicas**: Always replicas - 1 (ensures durability)

### 2. Consumer Configuration

Use `assets/consumer-config-template.py`. Key tuning:

**max_poll_records**: Based on volume
- Low: 100
- Medium: 500
- High: 1000

**Always set**:
- `enable_auto_commit: False` (manual commit for reliability)
- `auto_offset_reset: "earliest"` (process all messages)

### 3. Producer Configuration

Use `assets/producer-config-template.py`. Key tuning:

**batch_size**: Based on volume
- Low: 1024 bytes
- Medium: 16384 bytes
- High: 32768 bytes

**Always set**:
- `acks: "all"` (wait for all replicas)
- `retries: 3` (automatic retry on failure)
- `compression_type: "gzip"` (reduce network usage)

### 4. Security Configuration

When security requirements include TLS or SASL:

**For TLS**: Use `assets/kafka-user-template.yaml` with `type: tls`
**For SASL-SCRAM**: Use `type: scram-sha-512`
**For SASL-SSL**: Combine both TLS listener and SCRAM authentication

Add appropriate ACLs for topic access control (Read, Write, Describe operations).

## Performance Tuning Matrix

Refer to `references/performance-matrix.md` for detailed tuning guidelines.

Quick reference:

| Volume | Partitions | Replication | Batch Size | max_poll_records |
|--------|-----------|-------------|------------|------------------|
| Low    | 3         | 2           | 1024       | 100              |
| Medium | 6         | 3           | 16384      | 500              |
| High   | 12        | 3           | 32768      | 1000             |

## Security Patterns

For detailed security configurations, see `references/security-patterns.md`.

Common patterns:
- **Development**: No security (none)
- **Staging**: TLS only
- **Production**: SASL-SSL with ACLs

## Resources

### scripts/
- `generate_kafka_config.py` - Main configuration generator with CLI interface
- `calculate_performance_params.py` - Performance parameter calculations

### references/
- `performance-matrix.md` - Detailed performance tuning guidelines
- `security-patterns.md` - Security configuration patterns and examples

### assets/
- `topic-template.yaml` - Strimzi KafkaTopic template
- `kafka-user-template.yaml` - Strimzi KafkaUser template with ACLs
- `producer-config-template.py` - Python producer configuration
- `consumer-config-template.py` - Python consumer configuration
