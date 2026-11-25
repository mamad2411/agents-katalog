---
name: component-library-weaver
description: >-
  Use when weaving new components into the 187web design system and ensuring palette and atomic-scale conformance.
model_adapter: gemini
system_instruction: >-
  Scan the current design system. Ensure all new components inherit the 187web color palette (Abyssal Black #080808 / Widow Red #FF0000) and match the atomic design scale.
---

> **Gemini adapter:** Load as a system instruction. The distilled system instruction is in the YAML frontmatter; the full skill reference follows. Source: [`../../.claude/skills/component-library-weaver/SKILL.md`](../../.claude/skills/component-library-weaver/SKILL.md).

# Component Library Weaver

**Suite:** 187web Ecosystem v2. Parent index:
[`187web-ecosystem`](../187web-ecosystem/SKILL.md).

This skill injects the `component-library-weaver` directive from the 187web Master Prompt Manifest.
Load it when the task matches the triggers below.

## When to use this

- The task is an explicit Layer-4 viral/elegant web or agent prompt.

## Directive

> Scan the current design system. Ensure all new components inherit the 187web color palette (Abyssal Black #080808 / Widow Red #FF0000) and match the atomic design scale.

## Neuro-toxin profile

| Param | Value |
|-------|-------|
| toxicity | 0.2 |
| lethality | max |

## Pairs with

- [`187webdev-design-system`](../187webdev-design-system/SKILL.md) — Atomic design system

This skill is part of the 187web manifest Layer-4 prompt library.

