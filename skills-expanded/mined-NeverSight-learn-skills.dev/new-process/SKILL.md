---
name: new-process
description: Generate a deployable Camunda 8 BPMN process file. Use when creating or modifying BPMN workflows.
argument-hint: "[process description]"
---

Generate a deployable Camunda 8 BPMN file. Find and read `camunda-dev-guide.md` for Zeebe-specific patterns. For agentic processes with AI agents and ad-hoc sub-processes, use `/new-agent` instead.

If the process uses non-REST connectors (Slack, Kafka, SendGrid, etc.), look up their task type and input targets via the Camunda Docs MCP tool or at https://docs.camunda.io/docs/components/connectors/out-of-the-box-connectors/

$ARGUMENTS

Save to resources/. Deploy with c8ctl. If deployment fails, fix based on the error and retry.
