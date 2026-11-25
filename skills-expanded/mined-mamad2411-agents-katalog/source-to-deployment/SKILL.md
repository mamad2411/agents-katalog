---
name: source-to-deployment
description: CI/CD pipeline design, container configuration, deployment strategy selection, infrastructure-as-code, and dependency/supply chain management. Use when setting up pipelines, choosing between deployment strategies (blue/green, canary, rolling, feature flags), evaluating Dockerfile or container configuration, reviewing IaC (Terraform, Pulumi, CloudFormation), diagnosing pipeline failures, adding a new package dependency, or evaluating supply chain security. Does not cover application-level performance or security code review (see performance-engineering and security-engineering).
---

# Source to Deployment

The pipeline from committed code to running production software. Each stage is a feedback loop — the value is in how quickly it surfaces a problem, not in how many steps it has.

For CI/CD pipeline patterns see [cicd-patterns.md](cicd-patterns.md).
For container and runtime signals see [container-signals.md](container-signals.md).
For deployment strategy trade-offs see [deployment-strategies.md](deployment-strategies.md).
For infrastructure-as-code signals see [iac-signals.md](iac-signals.md).
For dependency hygiene, version pinning, vulnerability scanning, SBOM, and supply chain attack signals see [dependency-management.md](dependency-management.md).

## The core question

Before adding a pipeline stage, ask: **what failure does this stage catch, and how fast does it catch it?**

A stage that catches nothing, or catches it too slowly to be useful, is cost without benefit. Pipelines accrete stages. Every stage adds latency and maintenance surface. The right question is not "should we add a lint step?" but "what would we catch with a lint step that we are not catching with a faster feedback mechanism?"

## Fast feedback before slow feedback

Order stages from fastest-and-cheapest to slowest-and-most-expensive:

1. Static analysis and lint — seconds, no infrastructure needed
2. Unit tests — seconds to low minutes, no external dependencies
3. Integration tests — minutes, require real dependencies (database, queue)
4. Build and package — minutes
5. End-to-end / acceptance tests — minutes to tens of minutes
6. Deploy to staging — minutes plus environment spin-up
7. Deploy to production — controlled, with rollback ready

Do not run integration tests before unit tests. Do not deploy before tests pass. The ordering is not convention — it is cost control.

## CI/CD is not a deployment mechanism

CI/CD gives fast, high-confidence signal that a change is safe to ship. Deployment strategies (blue/green, canary, feature flags) control blast radius once the change is already in production. Conflating them leads to pipelines that are over-engineered for feedback and under-engineered for rollback.

## The fallacy of "if it passes CI it is correct"

CI validates what the tests cover. It does not validate what the tests do not cover. A green build is a necessary condition for shipping, not a sufficient one. The coverage gap is a design problem, not a CI problem.
