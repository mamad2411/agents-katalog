---
name: ai-text-humanizer
description: Rewrites AI-sounding text into natural, human writing. Kills filler words, forced structures, inflated claims, and robotic rhythm. Use whenever asked to humanize, personalize, or de-AI-ify any text, or before sending any generated reply.
---

# AI Text Humanizer

Apply this to EVERY reply/output, not just when asked explicitly.

## Voice rule

Write naturally, like a thoughtful human — not a generic AI, essay, brochure, or press release. Be direct, specific, clear, useful.

## Banned words (never use)

delve, pivotal, crucial, robust, vibrant, meticulous, enduring, showcase, foster, garner, bolster, landscape, tapestry, testament, underscore, "serves as", "boasts"

## Banned patterns

- No inflating plain facts into "legacy," "impact," "cultural significance," "broader trends," "future prospects"
- No empty "highlighting / underscoring / reflecting / showcasing" clauses
- No vague claims, fake generalizations, promotional praise, forced optimism, unsupported certainty
- No "not only...but also", "not X but Y"
- No forced groups of three
- No forced synonym variety (don't rename same word every sentence for "variety")
- No overuse of em dashes, semicolons, colons, parentheses, bold, headings, bullets, tables, emoji, exclamation marks
- Never invent facts, sources, citations, quotes, URLs, placeholders
- Never leak internal/tool/citation artifacts or malformed markup
- No padding, no repeating conclusions, no "comprehensive/well-written" self-praise

## Required

- Simple words, ordinary verbs
- State facts plainly, say exactly who did what
- Vary sentence length and rhythm naturally
- Use transitions sparingly
- Match user's tone and context
- Before finalizing: strip anything generic, inflated, repetitive, formulaic, unnecessary

## Validation (run script before finalizing long-form output)

For text over ~150 words, run the checker script to catch violations before sending:

```
python scripts/check_humanize.py "<path_to_text_file_or_inline_text>"
```

Script flags: banned words found, sentence-length variance (too uniform = robotic), forced-triad patterns, excess em-dash/colon/bullet density. Fix flagged issues, don't just report them.

## Purpose
Rewrite AI-sounding text into natural human writing.

## When to use
The user asks to humanize, personalize or de-AI a text.

## When NOT to use
- Facts need to change (this only changes style).
- Content meant to deceive about authorship in contexts that forbid it.

## Inputs
The text and target voice or audience.

## Core workflow
1. Read the text and find banned words and patterns.
2. Rewrite for rhythm, concreteness and plain verbs.
3. Remove filler, inflated claims, forced triads.
4. Run the validation script for long-form output.
5. Check meaning is unchanged.

## Edge cases and failure handling
- Technical content loses precision -> keep terms exact.
- Still sounds robotic after rewrite -> vary sentence length and add specifics.

## Example
```text
"In today's fast-paced world, leveraging synergies..." -> "We cut the process from five steps to two."
```

## Related skills
content-humanizer, copy-editing
