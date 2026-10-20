---
name: distributed-systems-architect
description: "Distributed systems: microservices, event-driven design, data consistency, fault tolerance, multi-region, observability. Use when designing or reviewing distributed architecture."
version: 1.0.0
platforms: [linux, macos]
---

# Distributed Systems Architect

## Overview

Distributed Systems Architect is the skill of designing high-scale, high-availability, geographically distributed system architectures. While the `architecture-planner` handles foundational full-stack architectures, this skill addresses the unique complexities of distributed environments: partial failures, network unreliability, consistency-availability trade-offs (CAP/PACELC), eventual consistency, distributed transactions, and multi-region operations.

**Core Principle:** IN A DISTRIBUTED SYSTEM, EVERYTHING RUNS SIMULTANEOUSLY AND EVERYTHING BREAKS SIMULTANEOUSLY. THE ARCHITECT DESIGNS BY ACCEPTING THIS REALITY, NOT BY DENYING IT.

Key differences from the `architecture-planner`:
- **Starts with the Fallacies of Distributed Computing** — systematically refutes assumptions that the network is reliable, latency is zero, or bandwidth is infinite.
- **CAP/PACELC Theorem** — treats every storage decision as a deliberate consistency-availability trade-off that must be documented.
- **Partial Failure** — ensures that if a service crashes, the rest of the system continues to function gracefully.
- **Eventual Consistency** — defines clear eventual consistency strategies where instant strong consistency is impossible or costly.
- **Multi-region** — extends beyond a single data center to geographical distribution and disaster recovery.

## Iron Laws (NEVER Violate)

1. **The network is unreliable — every call can fail** — Do not write code without defining a timeout, retry strategy, and circuit breaker for every inter-service call.
2. **Every write operation must be idempotent** — If the same request is received twice, it must produce the same result. This is the only way retries are safe.
3. **Know the CAP/PACELC trade-off and document it** — For every datastore selection: CP or AP? Why? What is the behavior under each failure mode?
4. **Never start with distributed transactions (2PC)** — Attempt Saga, Outbox, and eventual consistency first. Two-Phase Commit (2PC) is a last resort.
5. **Each service owns its own database** — NO direct access to another service's database. Access must occur exclusively through APIs or event streams.
6. **Observability is not retrofitted; it is part of the design** — Distributed tracing, structured logging, and metrics aggregation are designed alongside the architecture.
7. **A single point of failure can crash the entire system** — Every component must have redundancy, a failover strategy, and a recovery plan.

## When To Use

**USE WHEN:**
- The system will be divided into 3+ independent services.
- The system expects 1000+ concurrent users or 10K+ RPS.
- Geographical distribution is required (multi-region, multi-AZ).
- Zero-downtime deployment is a hard requirement.
- Data consistency vs. availability trade-offs are critical (e.g., finance, e-commerce, healthcare).
- Different services require different database technologies (polyglot persistence).
- Parts of the system are developed by separate teams.

**DO NOT USE (use `architecture-planner` instead):**
- A monolith is sufficient and scale is not an issue.
- There are fewer than 3 services.
- The team has fewer than 5 people (microservices coordination overhead > benefit).
- The domain is simple (basic CRUD).
- There is no requirement for zero-downtime or multi-region deployment.

## The Fallacies of Distributed Computing

Every distributed system design begins by systematically refuting these 8 fallacies:

| # | Fallacy | Reality | Architectural Countermeasure |
|---|---------|--------|------------------------------|
| 1 | The network is reliable | Packets get lost, switches fail, cables break | Retry + timeout on EVERY call |
| 2 | Latency is zero | The speed of light imposes physical limits: NY↔London ~70ms min | Async communication, caching, CDN |
| 3 | Bandwidth is infinite | Network congestion and throttling are real | Backpressure, rate limiting, pagination |
| 4 | The network is secure | MITM, DNS spoofing, BGP hijacking are real threats | mTLS, service mesh, zero trust |
| 5 | Topology doesn't change | Services scale up/down, IPs change dynamically | Service discovery, health checking |
| 6 | There is one administrator | Each team has its own deployment and configuration | Federation, API gateway, contract testing |
| 7 | Transport cost is zero | Serialization/deserialization consumes significant CPU | Binary protocols (Protobuf, Avro), schema evolution |
| 8 | The network is homogeneous | Nodes and links have varying speeds and reliabilities | Adaptive timeout, latency-aware routing |

## Design Workflow (10 Phases)

Work through these phases in order. Each phase has a mandatory output before advancing to the next.
See [REFERENCE.md](REFERENCE.md) for the full per-phase YAML templates, worked examples, and decision trees.

| Phase | Name | Key Output |
|-------|------|------------|
| 1 | Domain Analysis and Service Decomposition | Bounded context map, service boundary decisions (DDD) |
| 2 | Communication Architecture | Sync vs. async decision per call, protocol choice, timeout/retry/circuit-breaker config |
| 3 | Data Consistency Strategy | CAP/PACELC choice per store, Saga/Outbox/CQRS/Event Sourcing selection |
| 4 | Resilience and Fault Tolerance | Per-service resilience stack: timeout, retry, circuit breaker, bulkhead, rate limiter |
| 5 | Data Architecture | Per-service database selection, partitioning, read replicas, connection pooling |
| 6 | Event Architecture | Kafka topic design, schema registry, Avro event schema, retention policy |
| 7 | API Gateway and Service Discovery | Gateway routing, cross-cutting concerns (auth, rate-limit), health check config |
| 8 | Observability | Distributed tracing (OpenTelemetry), golden-signals metrics, structured logging, SLOs |
| 9 | Security Architecture | Defense-in-depth layers, zero trust, secrets rotation, STRIDE threat model |
| 10 | Deployment and Operational Architecture | Blue/green + canary pipeline, rollback triggers, K8s manifests, capacity + cost model |

## Red Flags — STOP and Rethink

- **Considering a shared database** — You are building a distributed monolith, not microservices. Each service must own its DB.
- **Two-Phase Commit (2PC) is your first choice** — It is a massive performance bottleneck. Attempt Saga patterns instead.
- **No circuit breakers defined** — You are inviting cascading failures where one downed service crashes the entire system.
- **Events lack a schema registry** — You will struggle to parse event schemas 3 months from now. Enforce schema evolution.
- **Logging without Trace IDs** — You cannot trace errors across asynchronous boundaries in a distributed system.
- **"We will add scalability later"** — Scalability does not retroactively fit. Partitioning and sharding must be designed up front.
- **Deploying to a single region** — What happens when that region suffers an outage? Multi-AZ is the minimum; multi-region is preferred.
- **No idempotency keys** — Asynchronous retries will execute duplicate actions. Every state mutation must be idempotent.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The monolith is fine, we will split it later" | Splitting a monolith later is 10x harder than designing modular bounded contexts from day one. |
| "The network is reliable, we are in AWS" | AWS SLAs are typically 99.99%, meaning ~52 minutes of allowed downtime per year. Can your system handle that gracefully? |
| "Two services can share a database, it's the same team" | Teams split and change. Shared databases lead to tight coupling, schema conflicts, and migration logjams. |
| "Event sourcing is too complex, let's just do CRUD" | The audit trail, point-in-time recovery, and simplified debugging of event sourcing will far outweigh its initial complexity. |
| "We have a load balancer, so circuit breakers are optional" | Load balancers drop dead nodes, but if a node is alive and returning slow timeouts, only a circuit breaker prevents systemic exhaustion. |
| "We will add observability once we are in production" | When a production incident occurs, trying to debug without tracing and correlation IDs is practically impossible. |

## Your Human Partner's Signals You're Doing It Wrong

**Requires Architectural Decision:**
- Cases where the CAP/PACELC trade-off is business-critical (strong consistency vs. high availability).
- Deciding to deviate from the ideal design due to severe budget constraints.
- Choosing between high multi-region infrastructure costs vs. acceptable downtime risks.

**Requires Domain Knowledge:**
- Bounded context boundaries are fuzzy due to lack of a domain expert.
- Navigating regulatory details (PCI-DSS, HIPAA, GDPR) that exceed technical expertise.
- Business decisions regarding integration protocols with legacy external systems.

## Related Skills

- **architecture-planner** — Foundational full-stack architecture. Runs BEFORE or TOGETHER WITH Distributed Systems Architect.
- **epic-orchestrator** — Orchestration of large-scale distributed projects. Implements the architecture produced by this skill.
- **performance-engineer** — Core Web Vitals and N+1 optimizations. In distributed systems: network latency, serialization cost, connection pooling.
- **security-reviewer** — OWASP Top 10. In distributed systems: mTLS, service mesh security, zero trust.
- **devops-release-engineer** — CI/CD and deployment. In distributed systems: blue/green, canary, multi-region deploy.
- **chaos-engineer** — Chaos engineering. Mandatory for distributed systems: network partition, AZ failure, region failure testing.
- **cloud-security-auditor** — CIS Benchmarks. In distributed systems: IAM policy, security group, VPC audit.
- **observability-pro** — OpenTelemetry, Prometheus, structured logging. The observability backbone of distributed systems.
- **postgres-pro** — PostgreSQL optimization. In distributed systems: partitioning, sharding, read replicas, connection pooling.
- **docker-k8s-pro** — Kubernetes. The deployment platform for distributed systems.
- **terraform-pro** — Infrastructure as Code. Multi-AZ, multi-region environments.

## Verification

**Domain and Service Design:**
- [ ] Ubiquitous language is explicitly defined for all bounded contexts.
- [ ] Service boundaries are optimized around transaction volumes and team capacities.
- [ ] Each service owns its database (absolutely no shared databases).
- [ ] Anti-corruption layers are defined for external/legacy system integrations.

**Communication and Data:**
- [ ] Sync/async communication pattern is documented for every inter-service call.
- [ ] Timeout, retry, and circuit breaker policies are defined for every endpoint.
- [ ] CAP/PACELC trade-offs are documented per datastore.
- [ ] Saga, Outbox, or Event Sourcing consistency strategies are mapped.
- [ ] All state mutations are designed to be idempotent.

**Infrastructure:**
- [ ] Multi-AZ deployment is active (minimum 3 AZs).
- [ ] Multi-region strategy is detailed (active-passive or active-active).
- [ ] Service discovery and health checks are configured.
- [ ] API gateway handles JWT validation, global rate limiting, and structured routing.

**Observability:**
- [ ] Distributed tracing is active across all services.
- [ ] Structured logging is formatted in JSON containing valid trace correlation IDs.
- [ ] Golden signals dashboard is configured in Prometheus/Grafana.
- [ ] SLOs are defined and burn-rate alert rules are deployed.

**Security:**
- [ ] mTLS is enforced for all inter-service communications.
- [ ] Zero trust is implemented: each service validates its own incoming authentication and authorization.
- [ ] Automated secrets rotation is set up.
- [ ] STRIDE threat modeling is completed per service boundary.

**Operations:**
- [ ] CI/CD pipeline supports blue/green and canary deployments.
- [ ] Automated rollback triggers have been tested.
- [ ] Capacity planning and complete cost models are calculated.
- [ ] Chaos testing (e.g., node shutdown, network latency injection) is scheduled.
