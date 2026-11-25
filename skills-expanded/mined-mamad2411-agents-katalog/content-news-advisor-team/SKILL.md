---
name: content-news-advisor-team
description: "资讯顾问。用于懂你的资讯顾问，基于隐式画像精选新闻，说明每条资讯与你的关系。来源于 WorkBuddy 内容创作卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/内容创作/content-news-advisor"
  workbuddy_card: "资讯顾问"
  workbuddy_category: "内容创作"
---

# 资讯顾问

Use this skill as the routing entry point for 资讯顾问 work. It packages the WorkBuddy 内容创作 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `content-news-advisor-intake`
- `content-news-advisor-strategy`
- `content-news-advisor-execution`
- `content-news-advisor-quality`
- `content-news-advisor-measurement`
- `content-news-advisor-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 资讯顾问 package, assemble the output set described in `references/workflow.md`.
