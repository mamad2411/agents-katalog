---
name: data-academic-journal-selection-team
description: "学术选刊顾问团 v3.0。用于学术选刊专家团，并行双管道架构，中文刊和外文刊各自独立分析学科匹配、期刊情报与安全检测，输出冲稳保分层投稿策略。来源于 WorkBuddy 数据智能卡片，并转换为 Codex 可安装的专家团入口格式。"
metadata:
  source: "workbuddy-expert-center/数据智能/data-academic-journal-selection"
  workbuddy_card: "学术选刊顾问团 v3.0"
  workbuddy_category: "数据智能"
---

# 学术选刊顾问团 v3.0

Use this skill as the routing entry point for 学术选刊顾问团 v3.0 work. It packages the WorkBuddy 数据智能 expert-team card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, source material, business or legal boundary, data/file scope, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata and available marketplace candidates, not from a hidden expert-detail prompt.
5. Return concrete deliverables, verification evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `manuscript-profiling`
- `cn-journal-matching`
- `sci-ssci-matching`
- `journal-risk-check`
- `submission-strategy`
- `cover-letter-pack`

## Output

Produce only the deliverables relevant to the request. For a full 学术选刊 package, assemble the output set described in `references/workflow.md`.
