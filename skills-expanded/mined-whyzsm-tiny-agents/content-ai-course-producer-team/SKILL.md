---
name: content-ai-course-producer-team
description: "AI师傅课程制作专家。用于基于教学需求和原始内容，快速做门AI一对一互动课。来源于 WorkBuddy 内容创作卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/内容创作/content-ai-course-producer"
  workbuddy_card: "AI师傅课程制作专家"
  workbuddy_category: "内容创作"
---

# AI师傅课程制作专家

Use this skill as the routing entry point for AI师傅课程制作专家 work. It packages the WorkBuddy 内容创作 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `content-ai-course-producer-intake`
- `content-ai-course-producer-strategy`
- `content-ai-course-producer-execution`
- `content-ai-course-producer-quality`
- `content-ai-course-producer-measurement`
- `content-ai-course-producer-handoff`

## Output

Produce only the deliverables relevant to the request. For a full AI师傅课程制作专家 package, assemble the output set described in `references/workflow.md`.
