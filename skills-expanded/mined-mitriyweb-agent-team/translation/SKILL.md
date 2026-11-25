---
name: translation
description: Translate documentation into the assigned target language.
compatibility: Requires bash, Claude Code
metadata:
  team: localization
  role: localizer
  version: "1.0"
---

## Mission: Contextual & Cultural Translation

The Localizer is responsible for adapting the English source documentation into a target language.
Your goal is to deliver a "Native-level" experience that feels natural, accurate, and culturally relevant.

## Phase 1: Contextual Audit

1. **Review Source Content**: Analyze the English documentation for tone, technical detail, and intended audience.
2. **Variable Mapping**: Identify all i18n placeholders (`{name}`, `{{count}}`) and cross-check with `references/i18n-best-practices.md`.
3. **Glossary Prep**: Synchronize terminology using the project's `references/glossary.md`.

## Phase 2: Linguistic Adaptation

1. **Drafting Translation**: Translate the content while strictly maintaining the "Expert Guide" voice from `references/voice-and-tone.md`.
2. **Cultural Nuance**: Adapt idioms, tone, and examples to be culturally appropriate for the target locale.
3. **Pluralization Handling**: Apply the correct target language rules for all numerical forms (`one`, `few`, `many`).

## Phase 3: UI & Formatting

1. **Space Constraints**: Ensure that translated UI labels (buttons, titles) are concise and don't overflow the interface.
2. **Formatting Preservation**: Maintain all original Markdown formatting (bold, italics, code blocks).
3. **Locale-specific formatting**: Correctly format dates, numbers, and currencies for the target locale.

## Gotchas

- **Placeholder Corruption**: Never modify or translate variable keys inside placeholders.

- **Literal Translation**: Avoid translating literally word-for-word if it results in unnatural phrasing.

- **Tone Drift**: Ensure the voice (e.g., Professional vs. Friendly) matches the English source.

## Validation Loop

The Localizer validates that the translation is linguistically accurate, **culturally natural**, and technically consistent with the original intent.
