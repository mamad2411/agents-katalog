---
name: human-writing-mode
description: Use automatically whenever Claude writes prose the user will read or send - replies meant as final text, emails, articles, reports, essays, thesis sections, proposals, social posts, documents. Makes the writing sound like a specific human wrote it (plain words, varied rhythm, concrete detail, no AI stock phrases). Not for code, commands, data tables, or short chat answers where brevity matters.
---

# Human Writing Mode

## Purpose
Remove the habits that make text read as machine-written, without changing meaning or facts. Works with `ai-text-humanizer` (rewrite + validation script) and `originality-guard`.

## When to use
Any deliverable prose: documents, PDFs, emails, posts, essays, reports, summaries the user will reuse.

## When NOT to use
- Code, config, logs, API output, formulas.
- One-line chat answers; terse caveman/short style the user asked for.
- Legal, medical or academic text where exact wording is required (edit only for clarity and keep terms).

## Inputs
The draft or the task, audience, purpose, any personal facts or voice samples the user provides.

## Core workflow
1. Draft from the user's facts and intent. Use only real information; never invent quotes, numbers, sources or experiences.
2. Choose a voice: if the user gave samples or a role (student, manager, founder), match it; otherwise plain, direct, first-person where natural.
3. Rewrite for human rhythm: mix short and long sentences; lead with the point; one idea per paragraph; paragraphs of uneven length.
4. Replace tells (see list). Prefer concrete nouns, numbers, examples and verbs over abstractions.
5. Cut filler: openers ("In today's world"), closers ("In conclusion"), restating the question, hedging stacks, empty praise.
6. Read once as the intended reader; fix anything stiff, repeated or over-explained.
7. Run the `ai-text-humanizer` validation script on long-form output if it is available.

## Decision rules
- Specific beats general: replace "various factors" with the factors.
- Keep technical terms exact; simplify the sentence around them.
- Keep the user's language (Bangla, Banglish, English); do not translate unless asked.
- If a detail is unknown, leave it out or ask; never fill with plausible-sounding invention.

## Tells to remove
Words and patterns: delve, tapestry, landscape, realm, testament, pivotal, crucial, robust, seamless, leverage, foster, underscore, navigate (figurative), "it is important to note", "moreover/furthermore/additionally" chains, "not only X but also Y", forced triads, rhetorical-question openers, heavy em-dash use, bold-label bullet lists in prose, identical paragraph length, closing summary that repeats the body.

## Edge cases and failure handling
- Text still sounds uniform -> vary sentence length, add one concrete example or number the user supplied.
- Meaning shifts after rewriting -> compare claim by claim and restore the original meaning.
- User asks to disguise AI authorship where disclosure is required (exam, journal, employer policy) -> state that disclosure rules apply and follow them; this skill improves writing quality, it does not remove a duty to disclose.
- Detector scores: detectors are unreliable and can flag human text; never promise a detector result.

## Validation
- No listed tells remain; read-aloud test passes.
- Every fact, name and number matches the input.
- Length and structure suit the format (email, report, post).

## Output requirements
The final text only (unless asked for notes). If something needed the user's input, add one short line saying what.

## Example
```text
Before: In today's fast-paced digital landscape, it is crucial to leverage robust SEO strategies.
After:  Most of our traffic came from three pages. We rewrote their titles and added internal links, and clicks rose 18% in six weeks.
```

## Related skills
`ai-text-humanizer`, `content-humanizer`, `originality-guard`, `docs-pdf-clean-output`, `copy-editing`.
