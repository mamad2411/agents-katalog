---
name: creative-category-pointer
description: "Pointer to a library of 3 specialized Creative skills. Use when working on creative-related tasks."
risk: none
---

# Creative Capability Library 🎯

This is a **pointer skill**. The 3 specialized Creative skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **article-illustrations** — Generate hand-drawn 16:9 article illustrations with the Grav character IP, sparse annotations, and absurd but clear visual metaphors.
- **liuguang-banlan-ui** — Builds two parameterized UI modes—流光溢彩白 (iridescent white) and 五彩斑斓黑 (colorful black)—with OKLCH, WebGL/CSS fallback, vision gating, screenshot QA, and total/per-color intensity reports. Use when a UI request names either mode or needs measured color parameters.
- **modellix** — Integrate the Modellix API/CLI for async AI image, video, and speech generation or transcription (model run --wait, task download).

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/creative/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/creative`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
