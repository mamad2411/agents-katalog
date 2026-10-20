---
name: reliability-category-pointer
description: "Pointer to a library of 14 specialized Reliability skills. Use when working on reliability-related tasks."
risk: none
---

# Reliability Capability Library 🎯

This is a **pointer skill**. The 14 specialized Reliability skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **application-performance-performance-optimization** — Optimize end-to-end application performance with profiling, observability, and backend/frontend tuning. Use when coordinating performance optimization across the stack.
- **datadog-automation** — Automate Datadog tasks via Rube MCP (Composio): query metrics, search logs, manage monitors/dashboards, create events and downtimes. Always search tools first for current schemas.
- **distributed-debugging-debug-trace** — You are a debugging expert specializing in setting up comprehensive debugging environments, distributed tracing, and diagnostic tools. Configure debugging workflows, implement tracing solutions, and establish troubleshooting practices for development and production environments.
- **distributed-tracing** — Implement distributed tracing with Jaeger and Tempo for request flow visibility across microservices.
- **incident-responder** — Expert SRE incident responder specializing in rapid problem resolution, modern observability, and comprehensive incident management.
- **observability-engineer** — Build production-ready monitoring, logging, and tracing systems. Implements comprehensive observability strategies, SLI/SLO management, and incident response workflows.
- **on-call-handoff-patterns** — Effective patterns for on-call shift transitions, ensuring continuity, context transfer, and reliable incident response across shifts.
- **pagerduty-automation** — Automate PagerDuty tasks via Rube MCP (Composio): manage incidents, services, schedules, escalation policies, and on-call rotations. Always search tools first for current schemas.
- **postmortem-writing** — Comprehensive guide to writing effective, blameless postmortems that drive organizational learning and prevent incident recurrence.
- **sentry-automation** — Automate Sentry tasks via Rube MCP (Composio): manage issues/events, configure alerts, track releases, monitor projects and teams. Always search tools first for current schemas.
- **server-management** — Server management principles and decision-making. Process management, monitoring strategy, and scaling decisions. Teaches thinking, not commands.
- **service-mesh-expert** — Expert service mesh architect specializing in Istio, Linkerd, and cloud-native networking patterns. Masters traffic management, security policies, observability integration, and multi-cluster mesh con
- **slo-implementation** — Framework for defining and implementing Service Level Indicators (SLIs), Service Level Objectives (SLOs), and error budgets.
- **tool-use-guardian** — FREE — Intelligent tool-call reliability wrapper. Monitors, retries, fixes, and learns from tool failures. Auto-recovers from truncated JSON, timeouts, rate limits, and mid-chain failures.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/reliability/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/reliability`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
