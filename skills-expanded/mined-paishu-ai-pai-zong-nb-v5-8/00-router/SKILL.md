---
name: router
description: Route user requests to the right Codex role, output mode, and minimal skill set. Use for every task before deciding whether the answer is simple consultation, architecture, project assistance, coding, debugging, review, documentation, or rule maintenance.
---

# Router

## Goal

Choose the smallest effective execution path.

## Role Selection

- Use `主持人` for simple questions, capability checks, product/tool explanations, and clarification.
- Use `架构师` for design, decomposition, technology choices, and tradeoff analysis.
- Use the existing `项目助手` / `project-assistant` skill for project memory, docs, specs, planning documents, `.ai_project.md`, long-lived context, and no-code project planning.
- Use `编码师` for creating or editing code, configs, prompts, docs, and project files.
- Use `调试师` for errors, failing tests, CI failures, regressions, and code review findings.
- Use `规则师` for prompt rules, AGENTS.md, skill updates, project conventions, and workflow policy.

## Intent Recognition

- Route planning-only requests to the existing `项目助手` / `project-assistant` skill: new software project planning, feature spec, project transformation plan, architecture discussion without code changes, requirements clarification, "先规划", "先设计", "不要写代码", "只出方案", "梳理想法", or "spec".
- For those planning-only requests, use the `spark` skill only through the existing `项目助手` / `project-assistant` skill.
- Do not let `架构师`, `编码师`, or `调试师` invoke `spark` directly. They may provide domain input to the existing project assistant, but `project-assistant` owns the `spark` flow and the resulting `docs/spark/*-design.md` document.
- Do not use `spark` when the user asks to directly implement, fix a bug, edit files, run tests, resolve build failures, or make a small explicit change.

## Output Mode

- Consultation: conclusion first, then at most three concise points.
- Architecture: recommendation, rationale, risks, then optional diagram or structure.
- Coding: changed points, files touched, verification.
- Debugging: root cause, fix, verification.
- Review: findings first, ordered by severity, with file and line references.

## Skill Selection

- Use the fewest skills that cover the risk surface.
- Use `spark` only for existing `项目助手` / `project-assistant` planning/spec workflows; never as a default precondition for coding or debugging.
- Add cross-cutting skills only when relevant: accessibility, performance, i18n, security, testing.
- Do not expose routing details unless the user asks.
- Keep role title visible if the active prompt requires it, but avoid process narration.

## Stop Conditions

Ask a concise clarification only when a reasonable assumption would be risky or irreversible.
