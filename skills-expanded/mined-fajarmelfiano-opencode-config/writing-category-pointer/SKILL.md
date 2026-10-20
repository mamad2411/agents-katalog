---
name: writing-category-pointer
description: "Pointer to a library of 5 specialized Writing skills. Use when working on writing-related tasks."
risk: none
---

# Writing Capability Library 🎯

This is a **pointer skill**. The 5 specialized Writing skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **bulletmind** — Convert input into clean, structured, hierarchical bullet points for summarization, note-taking, and structured thinking.
- **email-issue-fixer** — Fix small email mistakes without touching the writer's voice, and strip tracking parameters from links on request. Always returns the corrected draft plus a change list.
- **short** — Rewrite the previous response more briefly while preserving the substance.
- **tech-writing-proofread** — Proofreads English technical writing for typos, grammar, punctuation, terminology consistency, jargon, and structure; returns an itemized Original → Suggestion → Reason list without rewriting the document. Use when asked to proofread or polish a technical doc, README, or blog draft.
- **unslop** — Post-process AI-generated text through the unslop CLI to strip AI writing patterns before publishing

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `read` to load its `SKILL.md` from the vault:
   `/home/melfiano/.config/opencode/skill-libraries/writing/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `/home/melfiano/.config/opencode/skill-libraries/writing`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
