---
name: content-book-coauthor-team
description: "图书联合创作者。用于与作者深度协作，帮助规划书籍结构和内容，达到出版级品质。来源于 WorkBuddy 内容创作卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/内容创作/content-book-coauthor"
  workbuddy_card: "图书联合创作者"
  workbuddy_category: "内容创作"
---

# 图书联合创作者

Use this skill as the routing entry point for 图书联合创作者 work. It packages the WorkBuddy 内容创作 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `content-book-coauthor-intake`
- `content-book-coauthor-strategy`
- `content-book-coauthor-execution`
- `content-book-coauthor-quality`
- `content-book-coauthor-measurement`
- `content-book-coauthor-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 图书联合创作者 package, assemble the output set described in `references/workflow.md`.
