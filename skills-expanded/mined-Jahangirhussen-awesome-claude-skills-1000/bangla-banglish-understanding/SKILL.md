---
name: bangla-banglish-understanding
description: Understand Bangla, Banglish (romanized Bengali), English, and code-switched mixes between them, including typos, informal chat style, and technical Banglish. Use for every message — always active, not just when explicitly triggered.
---

# Bangla / Banglish / English Understanding

Always active. Applies to every user message, not just when Bangla is obviously present.

## Understand

- Pure Bangla (বাংলা script)
- Banglish / romanized Bengali (e.g. "ami ajke website banabo")
- English
- Code-switched mixes (Bangla + English in the same sentence)
- Technical Banglish (e.g. "database er schema banao", "ekta API banao")
- Typos, missing vowels, inconsistent spelling ("kore" / "korbo" / "korlam" variants)
- Short-form / chat-style abbreviations
- Context-dependent phrases where meaning depends on prior conversation

## Rules

1. Infer intended meaning from context — don't get stuck on literal word-by-word parsing.
2. Never complain about spelling, romanization style, or grammar in Banglish.
3. Don't force formal Bangla or English back at the user — match their register (casual stays casual).
4. Preserve technical terms exactly (API, database, schema, component names) — don't translate or "Banglify" them.
5. Reply in whatever mix of Bangla/Banglish/English the user is using, unless caveman mode or another active mode overrides tone.
6. Ask for clarification only when the meaning is genuinely ambiguous (not just because spelling is non-standard) — see [[auto-mode]] guidance on when to stop and ask.
7. Common short forms to recognize: "koro"/"kor" = do, "dew"/"dao" = give, "ache"/"ase" = exist/have, "lagbe" = need, "chai"/"chao" = want, "kivabe" = how, "keno" = why, "ki" = what, "ekhon"/"ekn" = now, "age" = before, "pore" = later, "thik ache" = okay.

## Purpose
Always-on comprehension of Bangla, Banglish, English and mixes so requests are understood correctly.

## When NOT to use
- It does not change the language of replies; reply in the user's language unless told otherwise.
- Not a translation task unless asked.

## Inputs
Any user message.

## Core workflow
1. Detect script and register (Bangla, Banglish, English, mixed).
2. Normalise spelling variants and typos in meaning, not in output.
3. Map technical Banglish to the intended technical request.
4. Act on the request; keep code and identifiers in English.

## Edge cases and failure handling
- Ambiguous Banglish word -> choose the meaning that fits the technical context; ask only if two meanings change the result.
- Transliteration variants (kore/korbo/korlam) -> treat as the same verb with different tense.

## Validation
- Restating the request in one sentence would match what the user meant.

## Output requirements
Correct action on the request; no announcement of the language handling.

## Example
```text
"database er schema banao" -> create a database schema.
```

## Related skills
master-auto-orchestrator
