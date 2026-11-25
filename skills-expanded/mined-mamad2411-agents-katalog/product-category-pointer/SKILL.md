---
name: product-category-pointer
description: "Pointer to a library of 4 specialized Product skills. Use when working on product-related tasks."
risk: none
---

# Product Capability Library 🎯

This is a **pointer skill**. The 4 specialized Product skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **before-you-build** — Review product risk before coding by checking demand, alternatives, channels, switching costs, and failure signals.
- **idea-autopsy** — Autopsy a business idea before you build it: kill-list check, five hard filters, a free-AI one-prompt test, live ad-market verification, and a verdict with a named kill-pattern.
- **product-decision-agent** — 中文产品决策 Agent。用于需求优先级、Roadmap、增长、留存、运营、数据异常、A/B Test、项目延期和跨团队协作；先判断事实、阶段、核心阻塞与主导机制，再给出下一步、停止清单和切换条件。默认中文，不引用原文或讲历史。
- **shopify-review-triage** — Turn public 1-3-star Shopify App Store review rows into a P0-P3 triage brief: incident risk, repeated friction, pricing confusion, feature requests, and an explicit needs-human-read bucket.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/product/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/product`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
