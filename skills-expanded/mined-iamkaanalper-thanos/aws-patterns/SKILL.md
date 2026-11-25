---
name: aws-patterns
description: Lambda best practices, S3 event patterns, SQS/SNS fanout, DynamoDB access patterns, and serverless AWS architectures for reliable, cost-effective, observable systems. Grok-native with Production Contract.
when-to-use: When building or reviewing serverless or AWS-heavy backend features, especially in swarms with infra or backend tracks.
---

# AWS Patterns Skill

Reusable, production-grade patterns for AWS serverless and managed services. Focus on the primitives that actually matter for reliability, cost, and speed of delivery.

## When to Use
- Designing Lambda + API Gateway + S3/DynamoDB backends.
- Event-driven flows with SQS, SNS, EventBridge, Kinesis.
- Cost optimization or scaling concerns on AWS.
- Before any significant AWS infra work in a swarm (Phase 2/3).

## Core Patterns

### 1. Lambda + API Gateway (with proper cold start and auth handling)
- Use Provisioned Concurrency only for p99 latency critical paths.
- Always have a dead-letter queue or error topic.
- Auth via Cognito or IAM, never custom in every function.

### 2. S3 Event + Lambda (idempotent processing)
- Key design must include enough info to reprocess.
- Use S3 Inventory + Athena for large bucket audits instead of listing everything.
- Lifecycle policies from day 1.

### 3. SQS/SNS Fanout for Decoupling
- SNS for broadcast, SQS for reliable consumption.
- Dead-letter queue + redrive policy on every queue.
- Visibility timeout tuned to processing time + buffer.

### 4. DynamoDB Access Patterns (single-table where it makes sense)
- Design GSI for access patterns, not just "add index later".
- Use transactions only for true multi-item atomicity.
- On-demand vs provisioned based on predictability.

### 5. Observability & Cost Guardrails
- X-Ray + structured logs + custom metrics always.
- Budgets + anomaly detection + tagging for every resource.
- Savings Plans / Reserved for stable workloads.

## Integration with Grok Ported System
- Use with devops-expert / aws-expert agent for implementation.
- Fire on_infra_change hook when applying these patterns at scale.
- Record friction in compound when a pattern caused surprise cost or latency.
- Pre-flight: "Have we modeled the access patterns and cost at 10x?"

## Production Contract
- Pre-Flight: read current AWS bill, existing architecture, compliance requirements.
- Ledger for any multi-service or migration effort.
- Handoff must include cost model, failure modes, and observability.
- Friction + compound feed for every "this pattern bit us in prod".

These patterns come from years of real AWS production pain. Use them so you don't have to learn the hard way.