---
name: travel-category-pointer
description: "Pointer to a library of 1 specialized Travel skills. Use when working on travel-related tasks."
risk: none
---

# Travel Capability Library 🎯

This is a **pointer skill**. The 1 specialized Travel skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **travel-planner** — 旅行/行程规划需求时使用:规划去某地旅行、X天X城、带老人孩子、自驾、假期安排等。产出逐日行程表、预算估算(经济/舒适/奢华三档)、交通住宿建议、景点美食清单。必须先问预算,预算未确认只输出问题清单;事实数据带来源和查询日期。

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/travel/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/travel`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
