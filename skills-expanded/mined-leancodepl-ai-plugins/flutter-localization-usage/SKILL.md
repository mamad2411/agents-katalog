---
name: flutter-localization-usage
description: Explain what the `flutter-localization` plugin does and how to use it. Use when the user invokes `/flutter-localization-usage`, asks what this plugin covers, or needs help with translations, ARB files, `l10n(context)`, or POEditor sync.
---

# Localization Usage

## How to respond

- If the user invoked this skill without a concrete task, start by explaining what this plugin does and when it should be used.
- Show how to use it through concrete localization tasks this plugin can handle.
- Point to the main localization rule or the `poe2arb` workflow when the task is operational.
- If the user already gave a concrete localization task, briefly explain why this plugin fits and then do the work.
- Do not reply with filler like "skill loaded", "ready for the task", or "what would you like to do?" before explaining the plugin.

## What this plugin does

- Covers ARB-based translation conventions for LeanCode Flutter projects.
- Explains `l10n(context)` usage in widgets and the POEditor plus `poe2arb` sync flow (`poe2arb poe` to pull, `poe2arb upload` to push).
- Keeps localization boundaries aligned with LeanCode rules.

## How to use it

- Ask to add or update user-facing translations.
- Ask to review localization usage in widgets.
- Ask how to sync localization files with POEditor.
- Ask how to regenerate l10n output after ARB changes.

## Example requests

- "Add translations for the new booking status labels."
- "Review this app's localization usage and `l10n(context)` usage."
- "Walk me through the `poe2arb` sync flow."
- "Push my ARB changes to POEditor with `poe2arb upload`."

## Reach for these assets

- `references/localization.md` - localization conventions and boundaries.
- `skills/poe2arb-workflow/SKILL.md` - operational sync workflow.
