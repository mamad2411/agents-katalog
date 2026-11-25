---
name: content-video-generator-team
description: "视频生成专家。用于基于 Remotion 的视频生成专家，创建产品演示、解说视频和社交媒体内容。来源于 WorkBuddy 内容创作卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/内容创作/content-video-generator"
  workbuddy_card: "视频生成专家"
  workbuddy_category: "内容创作"
---

# 视频生成专家

Use this skill as the routing entry point for 视频生成专家 work. It packages the WorkBuddy 内容创作 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `content-video-generator-intake`
- `content-video-generator-strategy`
- `content-video-generator-execution`
- `content-video-generator-quality`
- `content-video-generator-measurement`
- `content-video-generator-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 视频生成专家 package, assemble the output set described in `references/workflow.md`.
