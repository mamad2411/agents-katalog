---
name: content-knowledge-video-creator-team
description: "知识视频创作专家。用于基于深度研究报告，用基德风格创作口语化、反常识的知识视频脚本。来源于 WorkBuddy 内容创作卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/内容创作/content-knowledge-video-creator"
  workbuddy_card: "知识视频创作专家"
  workbuddy_category: "内容创作"
---

# 知识视频创作专家

Use this skill as the routing entry point for 知识视频创作专家 work. It packages the WorkBuddy 内容创作 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `content-knowledge-video-creator-intake`
- `content-knowledge-video-creator-strategy`
- `content-knowledge-video-creator-execution`
- `content-knowledge-video-creator-quality`
- `content-knowledge-video-creator-measurement`
- `content-knowledge-video-creator-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 知识视频创作专家 package, assemble the output set described in `references/workflow.md`.
