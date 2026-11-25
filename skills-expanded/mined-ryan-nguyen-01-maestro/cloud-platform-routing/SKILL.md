---
name: cloud-platform-routing
description: Use when a task touches AWS, Azure, cloud architecture, IAM/RBAC, serverless, queues, event buses, object storage, cloud databases, observability, cloud cost, infrastructure-as-code, cloud migration, cloud deployment, or multi-cloud service ownership.
category: security
---

# Cloud Platform Routing

Use this local skill to route cloud work to the right provider and service skills. It is not a replacement for AWS or Azure service skills; it is the mandatory selector and guardrail.

## Activation evidence

Apply this skill when task or code mentions AWS, Azure, cloud, serverless, Lambda, Azure Functions, SQS, EventBridge, SNS, SES, CloudWatch, IAM, Cognito, S3, DynamoDB, CloudFormation, Azure Service Bus, Event Grid, Azure Monitor, Application Insights, KQL, Key Vault, Entra ID, Azure Kubernetes, Azure Cost, Terraform, Bicep, ARM, Kubernetes, Docker, or cloud migration.

## Operating rules

- Identify provider first: AWS, Azure, multi-cloud, or unknown.
- Identify service ownership before implementation: compute, messaging, storage, database, identity, observability, cost, network, secrets, or deployment.
- Do not mix AWS and Azure primitives unless project brain confirms multi-cloud architecture.
- Treat IAM/RBAC, secrets, network exposure, public buckets, public queues, and webhook endpoints as security-sensitive.
- Prefer least privilege and scoped managed identity/role patterns.
- For infrastructure changes, document blast radius, rollback path, environment, state ownership, and deployment order.
- For queues/event buses, document retry, DLQ, ordering, idempotency, poison message handling, and observability.
- For cloud cost changes, document expected cost drivers and monitoring/budget controls.
- External skill aws-cloud-services was installed with Critical/High risk. Use it only as reference after safer service-level skills are insufficient.

## AWS skill routing

- General AWS service work: aws-cloud-services only when service-level skills do not cover the task.
- Serverless compute: lambda.
- Queueing: sqs.
- Event bus and schedules: eventbridge.
- Identity and permissions: iam, cognito.
- Object storage: s3.
- NoSQL database: dynamodb.
- Monitoring/logs/alarms: cloudwatch.
- IaC templates: cloudformation, terraform-knowledge-patch.
- Containers: docker, kubernetes-knowledge-patch, azure-kubernetes only when Azure AKS is in scope.

## Azure skill routing

- General cloud architecture: cloud-solution-architect plus microsoft-docs.
- Functions/serverless: azure-functions.
- Cost: azure-cost plus cost-optimization.
- Logs and queries: kql.
- Existing Azure stack skills already available in this repository should be preferred when present: azure-enterprise-infra-planner, azure-kubernetes, azure-quotas, azure-upgrade, microsoft-foundry.
- Azure GitHub Copilot repo skills such as azure-ai, azure-observability, azure-compute, azure-messaging, azure-cloud-migrate, and azure-hosted-copilot-sdk timed out during installation. Do not list them as installed unless a future install succeeds.
