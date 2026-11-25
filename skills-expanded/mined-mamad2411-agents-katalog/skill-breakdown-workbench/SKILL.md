---
name: skill-breakdown-workbench
description: "Analyze Codex Skills and agent manifests. Use when the user wants to拆解 a Skill, explain how a Skill or agent is written, or learn how to write one with bilingual Chinese/English guidance, reusable Skill formulas, and templates, especially when the target is an existing SKILL.md or agents/openai.yaml."
---

# 拆解现有的skill / Existing Skill Breakdown

## Overview

This skill turns a target Skill or agent manifest into a bilingual teardown and a writing lesson. It explains what the artifact does, how it is structured, and how to write a stronger version without inventing hidden behavior.

The deliverable is always a Markdown artifact. 每次拆解、写作教学或改进分析都必须生成一个 `.md` 文件，不能只在对话中返回散文说明。

## When to Read References

Read `references/guide.md` when the user asks for:

- a full Skill-vs-agent comparison
- reusable Skill formulas or authoring formats
- a reusable writing template
- a rewrite or improvement plan
- a stricter checklist for authoring or reviewing a package

## Triggers

- “拆解这个 skill 是怎么写的”
- “帮我分析这个 agent manifest，并教我怎么写”
- “Break down this Skill and show me how it is written”
- “Teach me how to write a better Skill and agent from this example”

## Workflow

1. Identify the target artifact: Skill, agent manifest, or both.
2. Read only visible files and treat `SKILL.md`, `agents/openai.yaml`, and linked references as the source of truth.
3. Explain the artifact in paired Chinese/English sections:
   - 结论 / Verdict
   - 结构拆解 / Structure Breakdown
   - Skill 写作法 / Skill Writing
   - Agent 写作法 / Agent Writing
   - 可复用公式 / Reusable Formula
   - 可复用模板 / Reusable Template
4. Turn the analysis into concrete lessons: triggers, boundaries, workflow, decision rules, references, output contract, and validation.
5. When teaching how to write a Skill, include the reusable formula:
   `Skill = Trigger + Boundary + Workflow + Decision Rules + References + Output Contract + Validation`.
6. When useful, map the target artifact back into the formula so the user can see how each part is represented in visible files.
7. If the user wants a rewrite, keep the original capability and boundary, then produce a draft or patch instead of a generic summary.
8. If the task is only review or explanation, do not install, publish, commit, or push anything.
9. If the task edits files, verify that every claim and every recommendation maps back to the visible text.
10. Write the final teardown to a `.md` file and return a clickable link to that file. 将最终拆解写入 `.md` 文件，并在回复中返回可点击文件链接。

## Guardrails

- Do not guess hidden prompts, private APIs, or unpublished files.
- Do not turn a Skill into a persona or soul statement.
- Keep the boundary clear: Skills describe capability and workflow; agents describe entry behavior and invocation details.
- Do not claim installation, publication, or execution unless it actually happened.
- Do not introduce secrets, local absolute paths, or external side effects without explicit permission.

## Validation

- For analysis, check that each conclusion is grounded in visible content.
- For authoring, validate `SKILL.md`, `agents/openai.yaml`, and any references before handing off.
- When files change, run the repository's structural checks and a path/secret scan before delivery.
- Confirm the output path ends in `.md`, the file exists, and the required bilingual sections are present.
- Do not claim the teardown was delivered until the Markdown file was written successfully.
