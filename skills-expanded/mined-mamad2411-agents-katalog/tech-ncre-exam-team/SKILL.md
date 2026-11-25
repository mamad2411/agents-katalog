---
name: tech-ncre-exam-team
description: "计算机等级考试专家团。用于 NCRE 一至四级备考规划、Office、程序设计、数据库、网络安全、练习题、错题分析和模拟考试。来源于 WorkBuddy 技术工程卡片，并转换为 Codex 可安装的专家团入口格式。"
metadata:
  source: "workbuddy-expert-center/technical-engineering/tech-ncre-exam"
  workbuddy_card: "计算机等级考试专家团"
---

# 计算机等级考试专家团

Use this skill as the routing entry point for 计算机等级考试专家团 work. It packages the WorkBuddy 技术工程 expert-team card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target system, repository or cloud scope, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from the visible 技术工程 card metadata; no full expert-detail prompt was present in the local marketplace cache.
5. Return concrete deliverables, verification evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `ncre-level-planning`
- `office-practice`
- `programming-practice`
- `database-practice`
- `network-security-practice`
- `mock-exam-grading`

## Output

Produce only the deliverables relevant to the request. For a full 计算机等级考试 package, assemble the output set described in `references/workflow.md`.
