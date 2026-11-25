---
name: tech-software-workshop-team
description: "软件工坊专家团。用于把软件想法推进到可生产交付，串联产品评审、代码审查、安全审计、QA测试、设计系统一致性和调试运维。来源于 WorkBuddy 技术工程卡片，并转换为 Codex 可安装的专家团入口格式。"
metadata:
  source: "workbuddy-expert-center/technical-engineering/tech-software-workshop"
  workbuddy_card: "软件工坊专家团"
---

# 软件工坊专家团

Use this skill as the routing entry point for 软件工坊专家团 work. It packages the WorkBuddy 技术工程 expert-team card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target system, repository or cloud scope, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from the visible 技术工程 card metadata; no full expert-detail prompt was present in the local marketplace cache.
5. Return concrete deliverables, verification evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `product-review`
- `code-review`
- `security-audit`
- `qa-testing`
- `design-system`
- `debug-operations`

## Output

Produce only the deliverables relevant to the request. For a full 软件工坊 package, assemble the output set described in `references/workflow.md`.
