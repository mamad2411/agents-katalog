---
name: design-brand-and-art-direction
description: "Build and review frontend brand aesthetic, moodboards, visual direction, imagery style, color and typography personality against documented audience, identity and design constraints."
---

# Brand and art direction

## Scope

Use this specialist when the actual task involves brand issues. Check documented brand/system decisions before prescribing changes. Do not conflate taste with accessibility standards or make assumptions from screenshots alone.

Affecting category: **brand**. Related governing principles: unity, emphasis. Route from `design-diagnose` or `design-review` when observations match this category, or load directly during a focused implementation.

## Procedure

- **mood-without-intent**: Record audience/task, 3–5 desired attributes, accepted brand constraints and counterexamples. Verify: Stakeholders identify intended qualities using unlabeled screens rather than logo alone.
- **creative-brief-ambiguity**: Curate a small annotated reference set; identify invariant palette/type/image constraints, and unacceptable cues. Verify: Prototype selection can be justified against explicit attributes and task outcomes.
- **cross-surface-brand-drift**: Connect brand rules to semantic tokens, component patterns and illustration guidance with clear ownership. Verify: Blind brand-recognition comparison across surfaces and documented exceptions.

Read `references/playbook.md` for exact discriminating checks, implementation examples, tradeoffs and acceptance tests. Keep the fix within the existing component architecture. Report original observation, selected recipe and evidence. For usability, engage `ux-*`; for normative accessibility, engage `wcag-*`.
