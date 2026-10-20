---
name: claude-sre-incident-responder
description: Architectural pattern for an automated SRE on-call incident response agent with Claude Agent SDK. Ingests PagerDuty/webhook alerts, investigates logs via MCP, isolates root cause, drafts code fixes, and gates deployment behind human approval.
---

# SRE Incident Responder Agent Architecture

## Overview
An on-call reliability engineering agent that bridges the gap between raw monitoring alerts and pull request resolution while maintaining strict human-in-the-loop safety boundaries.

## Workflow Pipeline
1. **Alert Ingestion:** Webhook trigger from PagerDuty, Datadog, or Slack alerting channels.
2. **Telemetry & Log Investigation:** Connects to monitoring infrastructure via Model Context Protocol (MCP) servers to retrieve error traces and metrics.
3. **Root Cause Isolation:** Formulates failure hypotheses and runs reproducible diagnostics.
4. **Remediation Draft:** Generates a minimal, focused code patch and test reproduction in an isolated branch.
5. **Human Approval Gate:** Posts findings and PR link to Slack/incident channel, pausing execution until an on-call engineer explicitly approves deployment.

```
Alert Trigger -> MCP Log Probe -> Root Cause Diagnostic -> Patch Draft -> Human Gate (Pause)
```
