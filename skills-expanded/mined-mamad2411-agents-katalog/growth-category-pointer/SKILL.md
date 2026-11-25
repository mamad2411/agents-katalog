---
name: growth-category-pointer
description: "Pointer to a library of 3 specialized Growth skills. Use when working on growth-related tasks."
risk: none
---

# Growth Capability Library 🎯

This is a **pointer skill**. The 3 specialized Growth skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **indexing-issue-auditor** — High-level technical SEO and site architecture auditor. Invoke to scan local or live environments for indexing, crawl budget, and structural errors.
- **linkedin-profile-optimizer** — High-intent expert for LinkedIn profile checks and SEO optimization. Silently audits and rewrites profiles, delivering only the finished, ready-to-paste result.
- **social-post-writer-seo** — Social Media Strategist and Content Writer. Creates clear, engaging social media posts for Instagram, LinkedIn, and Facebook.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/growth/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/growth`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
