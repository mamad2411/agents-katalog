---
name: i18n-tone-adapt
version: 1.0.0
description: Adapt tone and formality across languages so the message fits the target audience and channel.
author: matrixx0070
tags: [tone, formality, register, audience]
capabilities: []
---

## When to use

Use this when a faithful translation is correct but the tone is wrong for the audience — too stiff for a youth app, too casual for a legal notice, or using the wrong formality pronoun. It tunes register, politeness level, warmth, and voice while preserving meaning. Often runs as a pass after `i18n-translate`.

**Not for:** first-pass meaning translation (use `i18n-translate`), unit/date/culture adaptation (use `i18n-localize`), term lists (use `i18n-glossary`), or captions (use `i18n-subtitle`).

## Method

1. Define the audience and channel: who reads this, where, and what relationship (peer, customer, authority)? This sets the target register.
2. Identify the target language's formality system: T/V pronouns (tu/vous, du/Sie), honorifics (Japanese keigo), verb politeness levels. Decision point: pick the level that matches the relationship, and apply it consistently.
3. Adjust lexical warmth: contractions, exclamations, emoji, slang for casual; full forms, hedges, and measured verbs for formal.
4. Preserve the core message and any legal commitments — tone changes wording, never meaning or obligations.
5. Decision point: if the source mixes registers (casual body, formal disclaimer), keep the split intentionally rather than flattening it.
6. Read aloud in the target: does it sound like the intended speaker to the intended listener?

## Example

Source meaning (EN): "Your subscription will renew tomorrow."

Formal (de, to a business customer): "Wir möchten Sie darüber informieren, dass sich Ihr Abonnement morgen verlängert." (uses "Sie", measured phrasing)

Casual (de, to a consumer app user): "Kleiner Hinweis: dein Abo verlängert sich morgen!" (uses "du", light and friendly)

Same fact, two registers — pronoun and warmth chosen for each audience.

## Pitfalls

- **Wrong formality pronoun.** Using "du"/"tu" with an authority figure (or "Sie"/"vous" with a teen app) reads as rude or cold.
- **Inconsistent register.** Sliding between formal and casual within one message feels unstable and untrustworthy.
- **Tone change that alters obligation.** Softening "must" to "might want to" in a legal or safety notice is a meaning bug, not a tone edit.
- **Copying source emoji/slang blindly.** Casual markers don't map 1:1 across cultures; over-familiarity can offend.

## Output format

```
Audience: <who>   Channel: <where>   Target register: <formal | neutral | casual>
Formality system: <T/V pronoun | honorific level>

--- Adapted text ---
<text at the chosen register>

--- Tone notes ---
- Pronoun/politeness: <choice>
- Warmth markers kept/removed: <...>
```
