---
name: arabic-terminal-rtl
description: Use when writing Arabic in Windows Terminal, OpenCode, Codex, or any non-BiDi terminal; reverses Arabic word characters and Arabic segment word order by default.
---

# Arabic Terminal RTL

## Purpose

Windows Terminal and some CLI surfaces can render Arabic RTL/BiDi text incorrectly. This skill makes Arabic-script prose readable in left-to-right, non-BiDi terminals.

## Activation

Use this skill by default whenever a reply contains Arabic-script prose in OpenCode, Codex, Windows Terminal, or any terminal that does not reliably support RTL/BiDi rendering.

Do not wait for the user to remind you once the environment or instructions indicate Arabic terminal mode.

## Required Output Rule

For every Arabic-script prose segment, apply both transformations before sending:

1. Reverse the character order inside each Arabic-script word.
2. Reverse the word order of that Arabic segment.

Examples:

```text
Intended logical Arabic: الحمد لله
Terminal-safe output: هلل دمحلا

Intended logical Arabic: السلام عليكم ورحمة الله
Terminal-safe output: هللا ةمحرو مالسلا مكيلعو

Intended logical Arabic: لا إله إلا الله
Terminal-safe output: هللا ال هلإ ال
```

## Scope

Apply to:

- Arabic answers
- Arabic headings
- Arabic bullets
- Arabic confirmations
- Arabic questions
- Arabic explanations
- inline Arabic phrases
- single Arabic words

Mixed Arabic and non-Arabic segments:

- Reverse token order inside the Arabic-containing segment.
- Reverse characters only inside Arabic-script tokens.
- Keep English/code/numbers unchanged.

## Preserve Exactly

Do not transform:

- code blocks
- shell commands
- file paths
- URLs
- JSON/YAML/TOML
- identifiers
- package names
- English text
- numbers
- slash commands

If Arabic appears inside machine-readable content that must remain exact or executable, preserve it verbatim and explain outside the code block if needed.

## Punctuation

Keep punctuation attached to its token during reversal.

Example:

```text
Intended logical Arabic: الحمد لله.
Terminal-safe output: .هلل دمحلا
```

## Behavior

- Do not explain this rule unless asked.
- Do not apologize for transformed Arabic looking unusual; it is intentional.
- Do not output normal Arabic prose when Arabic terminal mode is active.
- Apply even to short replies.

## Self-Check Before Sending

- Every Arabic word reversed character-by-character?
- Arabic word order reversed per segment?
- English/code/URLs/paths/commands untouched?
- Slash commands untouched?
- Machine-readable content preserved?
