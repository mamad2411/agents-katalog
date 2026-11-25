---
name: aws-serverless
description: "Use when designing, debugging or reviewing Lambda, API Gateway, SQS, SNS, EventBridge or Step Functions code and configuration: cold starts and INIT billing, Lambda Layers, packaging and shared dependencies, deployment package size, concurrency, runtime choice, Powertools, logging and tracing, alarms, retries and DLQs, payload limits, or choosing HTTP API or REST API, Lambda or Step Functions, Lambda or ECS. Not for creating a new service from a template (creating-aws-projects)."
---

# AWS Serverless

## Quick Reference

| Topic | Reference File | Key Insight |
|-------|---------------|-------------|
| Lambda internals | `references/lambda-patterns.md` | Cold start happens per concurrent execution, not just once |
| Lambda Layers | `references/lambda-patterns.md` | Binaries, custom runtimes and Powertools; NOT a package manager |
| Observability | `references/lambda-powertools.md` | Structured JSON logs; choose tracing deliberately (X-Ray SDK is in maintenance) |
| Monitoring/alarms | `references/monitoring.md` | Alert on symptoms (errors, latency), not causes (CPU) |
| Event-driven | `references/event-driven.md` | Single Lambda vs Step Functions decision; Standard/Express/Hybrid; Saga pattern |
| API Gateway | `references/api-gateway.md` | HTTP API ~70% cheaper; use REST API only for WAF/caching/usage plans |

## Critical Anti-Patterns

### Lambda
- **Don't** assume cold start is "just the first request" — it happens per concurrent execution
- **Don't** use Lambda Layers as a package manager. When asked whether shared libraries belong in a layer, answer with three points:
  1. **Layers are for** binary dependencies (FFmpeg, ImageMagick), custom runtimes (LLRT, Bun) and AWS-provided layers (Powertools). Ordinary pip or npm libraries such as `requests` or `pydantic` are not layer candidates. Each function bundles what it imports, from a lockfile.
  2. **A layer has costs.** It adds a mount and initialization step to every cold start, and INIT is billed since August 2025. It also breaks local development, hides the libraries from vulnerability scanners that read the function package, has no semantic versioning, and counts toward the limit of 5 layers per function.
  3. **Shared code is not a size problem.** If a package is too large, bundle and tree-shake it, or use a container image. Don't move libraries into a layer to make it smaller.
- **Don't** call Lambda synchronously from Lambda — use SQS, SNS, or Step Functions
- **Don't** set user-facing API timeout to 30s ; use async for long operations

### Observability
- **Don't** log unstructured text: set `logging_config { log_format = "JSON" }` and use the language's logger, or Powertools Logger. Set the log level in one place, not in both
- **Don't** add the X-Ray SDK or Powertools Tracer to new functions by default: it is in maintenance mode. Use active tracing, or a tested OpenTelemetry layer
- **Don't** call CloudWatch API synchronously for metrics — use Powertools Metrics (EMF format)
- **Don't** alert on resource utilization (CPU, memory) — alert on user-impacting symptoms

### Event-Driven
- **Don't** set SQS visibility timeout shorter than Lambda timeout — set it to 6× Lambda timeout
- **Don't** omit a DLQ — always pair queues with a DLQ and alarm on it
- **Don't** use Lambda to transport data between services — use direct integrations; reserve Lambda for transforming data

> "Use Lambda to transform data, not to transport data between services." — Jérôme Van Der Linden

## Decision Frameworks

### Lambda vs Step Functions
| Use Lambda When | Use Step Functions When |
|-----------------|------------------------|
| Single operation < 15 mins | Workflow with multiple steps |
| Simple request-response | Need retry/error handling per step |
| Stateless processing | Long-running or human-in-loop |
| | Visual workflow debugging needed |

### Lambda vs ECS
| Use Lambda When | Use ECS When |
|-----------------|--------------|
| Execution < 15 minutes | Long-running processes |
| Bursty, unpredictable traffic | Steady, high-volume traffic |
| Cold start acceptable | Sub-100ms latency required |
| Pay-per-invocation preferred | Need GPU or special hardware |

## Cost questions

For prices, use the AWS Pricing MCP server (`awslabs.aws-pricing-mcp-server`). Its [README](https://github.com/awslabs/mcp/tree/main/src/aws-pricing-mcp-server) has the setup. Prices in this skill are dated examples, not quotes.

---

## Version Matrix

| Feature | AWS GA | Supported Runtimes |
|---------|--------|--------------------|
| SnapStart | Nov 2021 (Java); Oct 2024 (Python, .NET) | Java 11+, Python 3.12+, .NET 8+ — not Node, Ruby, or container images |

---

## Reference Loading Strategy

Load references based on what the user is asking:

1. **Cold starts, memory tuning, concurrency, Layers** → `references/lambda-patterns.md`
2. **Logging, tracing, metrics, Powertools setup** → `references/lambda-powertools.md`
3. **CloudWatch alarms, dashboards, alerting strategy** → `references/monitoring.md`
4. **SQS, SNS, EventBridge, Step Functions, Saga** → `references/event-driven.md`
5. **API Gateway (HTTP vs REST, going-live checklist, WAF, X-Ray, security)** → `references/api-gateway.md`
