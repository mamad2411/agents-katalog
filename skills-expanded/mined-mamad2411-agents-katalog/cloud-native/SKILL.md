---
name: cloud-native
description: Cloud-native development patterns, containerization, and serverless architecture.
---

# Cloud-Native Development

Build scalable, resilient cloud-native applications.

## Core Principles
1. **Microservices**: Small, independent, replaceable services
2. **Containerization**: Docker/OCI containers for portability
3. **Declarative**: Infrastructure as code, desired state
4. **DevOps**: CI/CD, automation, observability
5. **Resilience**: Fault tolerance, graceful degradation
6. **Scalability**: Horizontal scaling, stateless design

## Container Patterns
- **Sidecar**: Auxiliary container (logging, monitoring, proxy)
- **Init Container**: Setup before main app
- **Ambassador**: External service proxy
- **Adapter**: Interface normalization
- **Multi-container Pods**: Shared network and storage

## 12-Factor App
1. Codebase: One codebase, many deploys
2. Dependencies: Explicit declaration
3. Config: Environment variables
4. Backing Services: Attached resources
5. Build/Release/Run: Separate stages
6. Processes: Stateless, share-nothing
7. Port Binding: Self-contained HTTP service
8. Concurrency: Process scaling
9. Disposability: Fast startup, graceful shutdown
10. Dev/Prod Parity: Similar environments
11. Logs: Event streams
12. Admin Tasks: One-off processes

## Serverless
- **AWS Lambda**: Function as a service, layers, provisioned concurrency
- **Cloudflare Workers**: Edge compute, KV, Durable Objects
- **Vercel/Netlify**: Next.js/Nuxt deployment, edge functions
- **Durable Functions**: Stateful serverless (Azure)

## Service Mesh
- **Istio**: Traffic management, security, observability
- **Linkerd**: Lightweight, Rust-based
- **Consul Connect**: Service discovery + mesh
- Patterns: Circuit breaker, retry, timeout, canary

## Resilience Patterns
- **Circuit Breaker**: Fail fast when downstream is down
- **Bulkhead**: Isolate resource pools
- **Timeout**: Never wait forever
- **Retry with Backoff**: Exponential, jittered
- **Rate Limiting**: Protect services from overload
- **Graceful Degradation**: Partial functionality when degraded
