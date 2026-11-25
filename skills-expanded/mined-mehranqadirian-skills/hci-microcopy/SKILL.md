---
name: hci-microcopy
description: Writes and reviews the small text in user interfaces: button labels, error messages, empty states, confirmations, toasts, labels, placeholders and tooltips, in English and Persian. Use whenever the user asks for UI text, error wording, button names, onboarding copy or a copy review, sees vague messages like "Something went wrong" or "Are you sure?", or wants consistent, helpful, non-blaming wording, even if they only say "what should this message say?". Lints strings with a script, then rewrites them with a clear pattern.
---

# hci-microcopy

Words are part of the interface. Good microcopy tells people what is happening and what to do next, in a calm voice, without blame. Builds on `hci-foundations` (error recovery, match with the real world, consistency).

```
hci-microcopy/
├── SKILL.md
├── scripts/
│   └── lint_microcopy.py          lint UI strings from JSON, CSV or text (English and Persian)
├── references/
│   └── microcopy-guide.md         principles, patterns for buttons, errors, empty states, confirms, tone, Persian
└── templates/
    └── strings.json               example string table with good copy
```

## When to use

- Writing or rewriting error messages, button labels, empty states, confirmations, toasts, hints
- Auditing an app's text for vague, blaming, technical or inconsistent wording
- Creating a glossary and voice guide
- Preparing strings for translation, including Persian

## Workflow

1. **Collect the strings with context**: id, type (error, button, empty, confirm, toast, success, label, placeholder, tooltip), where it appears and what just happened. Without context, ask for it; copy written blind is guesswork.
2. **Lint**: `python3 scripts/lint_microcopy.py strings.json` (JSON, CSV or `type: text` lines). It flags vague or blaming errors, jargon, missing next steps, generic buttons, "Are you sure?" confirmations, long toasts, filler, ALL CAPS and many exclamation marks, in English and Persian. Add `--strict` to fail on warnings.
3. **Rewrite with patterns**: errors say what happened, why if known and what to do; buttons are verb plus object; confirmations name the object and the consequence (or offer Undo); empty states explain and invite one action; toasts are short. See `references/microcopy-guide.md` for before and after examples.
4. **Keep terms consistent**: one word per concept ("Sign in", never also "Log in"); build a small glossary and apply it everywhere.
5. **Check tone and accessibility**: calm in errors, no humor in failures, links meaningful alone, nothing conveyed by color only, error text tied to its field.
6. **Prepare for localization**: full sentences with placeholders, no concatenation, room for longer text; for Persian write natively with the same pattern and check half spaces and digits (`persian-text-processing`, `hci-rtl-localization`).
7. **Validate**: read aloud, then test with users whether they understand what will happen before they act (`hci-usability-testing`). State that the linter finds patterns, not tone.
8. **Report** each rewrite with the reason and the rule it fixes.

## Rules

- Never blame the user; say what is needed
- Never use "Error", "Something went wrong" or "Invalid input" alone
- Never use "OK", "Submit", "Click here" as the only label of an action
- Prefer Undo to "Are you sure?"; if confirming, name the object and the consequence
- Do not invent product facts, policies or error causes; ask when unknown
- Do not use guilt, false urgency or hidden costs in copy
- Keep brand voice only where it does not reduce clarity

## What to report back

| Field | Content |
|-------|---------|
| Findings | string id, rule, why it hurts users |
| Rewrites | before and after, one line of reasoning each |
| Glossary | the terms chosen |
| Localization notes | placeholders, length, Persian wording |
| Test idea | how to check comprehension with users |

## Related skills

- `hci-foundations`: heuristics on error recovery and matching the real world
- `hci-rtl-localization`: layout and length for translated text
- `persian-text-processing`: half spaces, digits and letters in Persian copy
- `hci-cli-ux`: error messages and help text in terminals
- `hci-usability-testing`: test comprehension with users
