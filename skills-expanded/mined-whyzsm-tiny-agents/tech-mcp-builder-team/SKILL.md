---
name: tech-mcp-builder-team
description: "MCP构建专家。用于精通 Model Context Protocol 设计实现。来源于 WorkBuddy 技术卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/技术/tech-mcp-builder"
  workbuddy_card: "MCP构建专家"
  workbuddy_category: "技术"
---

# MCP构建专家

Use this skill as the routing entry point for MCP构建专家 work. It packages the WorkBuddy 技术 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `tech-mcp-builder-intake`
- `tech-mcp-builder-strategy`
- `tech-mcp-builder-execution`
- `tech-mcp-builder-quality`
- `tech-mcp-builder-measurement`
- `tech-mcp-builder-handoff`

## Output

Produce only the deliverables relevant to the request. For a full MCP构建专家 package, assemble the output set described in `references/workflow.md`.
