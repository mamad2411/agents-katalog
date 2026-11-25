---
name: content-viral-topic-planner-team
description: "爆款选题策划专家。用于投热点出爆款，基于心法预筛和多形态产出，做公众号视频号小红书 H5 通吃的选题策划。来源于 WorkBuddy 内容创作卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/内容创作/content-viral-topic-planner"
  workbuddy_card: "爆款选题策划专家"
  workbuddy_category: "内容创作"
---

# 爆款选题策划专家

Use this skill as the routing entry point for 爆款选题策划专家 work. It packages the WorkBuddy 内容创作 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `content-viral-topic-planner-intake`
- `content-viral-topic-planner-strategy`
- `content-viral-topic-planner-execution`
- `content-viral-topic-planner-quality`
- `content-viral-topic-planner-measurement`
- `content-viral-topic-planner-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 爆款选题策划专家 package, assemble the output set described in `references/workflow.md`.
