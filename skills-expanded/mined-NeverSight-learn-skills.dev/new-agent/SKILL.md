---
name: new-agent
description: Generate a Camunda 8 agentic process with AI Agent connector and ad-hoc sub-process. Use when building AI agent workflows with tool calling.
argument-hint: "[agent purpose and tools]"
---

Generate an agentic Camunda 8 BPMN process. Find and read the "Agentic BPMN" section of `camunda-dev-guide.md` for ad-hoc sub-process XML, connector task types, input targets, and `fromAi()` usage.

$ARGUMENTS

Use the **AI Agent Sub-process** pattern (recommended):
1. Create a `bpmn:adHocSubProcess` with `zeebe:taskDefinition type="io.camunda.agenticai:aiagent-job-worker:1"`
2. Add `zeebe:adHoc outputCollection="toolCallResults" outputElement="={id: toolCall._meta.id, name: toolCall._meta.name, content: toolCallResult}"` — **required** for tool result collection
3. Add `zeebe:taskHeaders` with `resultVariable` = `agent`
4. Add tools as activities inside (no incoming flows, no start/end events)
5. Use `fromAi()` in tool input mappings for AI-generated parameters
6. Each tool **must** write output to `toolCallResult` variable (e.g. `resultExpression` → `={toolCallResult: response.body}`)
7. Add `<bpmn:documentation>` to each tool describing what it does
8. Configure `systemPrompt`, `userPrompt`, `modelProvider`, and `authentication.apiKey` (`{{secrets.KEY_NAME}}`)

Tools can also be **sub-processes** for multi-step async patterns:
- Put a service task (action) followed by a catch event (wait) inside a sub-process
- The sub-process is the tool entry point; inner steps are hidden from the agent
- Use this for send+wait, request+callback, or any tool needing async interaction
- See the "Sub-flow Tool Pattern" section in camunda-dev-guide.md

For non-REST connectors as tools, look up their task type and input targets via the Camunda Docs MCP tool.

Save to resources/. Deploy with c8ctl.
