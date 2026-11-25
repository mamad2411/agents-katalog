---
name: article-translator
description: Translate articles, essays, blog posts, threads, and other longer-form prose between any pair of languages while preserving the author's voice, register, and rhetorical structure. Use this whenever the user asks to translate, localize, render, or "give me in [language]" any text longer than a few paragraphs — news articles, op-eds, essays, blog posts, longreads, newsletters, technical writeups, conference transcripts, Twitter/X threads, or non-fiction excerpts. Trigger even when the user does not say the word "translate" explicitly — for example "I need this in English for our investors", "rewrite this for a Russian audience", or "make this readable to a German reader" all count. Do not use for single sentences, UI strings, code-only inputs, or short slogans — those are too small to benefit from this workflow.
version: 0.2.0
---

# Article Translator

A workflow for translating long-form prose with fidelity, consistency, and a preserved authorial voice. Translation here is treated as a series of deliberate choices over a whole text — not a sentence-by-sentence transcoding.

## When to use

Input is more than ~3 paragraphs of prose bound for another language. Out of scope: UI copy, code, single sentences, tweet-sized fragments, song lyrics, metered poetry (verse translation needs a different toolkit), legal contracts (specialized terminology and disclaimers).

## Core workflow at a glance

1. **Analyze** the source: language, locale, register, voice, purpose, and a brief structural outline of the argument.
2. **Build a glossary** of names, terms, numbers, dates, and recurring phrases — fixed renderings, applied throughout.
3. **Decide strategy** on idioms, units, punctuation, and format preservation.
4. **Translate** in paragraph-sized semantic units (Phase 4).
5. **Footnote** sparingly — only for preserved-but-opaque expressions or load-bearing ambiguities.
6. **Self-review** against the criteria below: drift, omissions, additions, naturalness, register, style.

**Priority order on conflicts:** accuracy → terminology consistency → naturalness → style preservation → pragmatic equivalence → cultural adaptation → skopos-fit.

**Calibrate depth to the text.** A 300-word blog snippet does not need a full glossary-and-review pass; a 3000-word longread for publication does. Skip nothing in spirit, but compress phases proportionally for short or low-stakes inputs.

**Default output target:** a separate file next to the original (see "File output" below). The chat reply summarizes; it does not paste the translation back.

## Guiding criteria

The output should satisfy all of these criteria together. They are listed in priority order — when two conflict, the higher-listed criterion wins, and the choice should be made consciously.

1. **Accuracy.** Every proposition in the source must be present in the target. Nothing added, nothing dropped. Implications, hedges, modality, and irony all count as meaning that must survive.
2. **Terminological consistency.** The same concept gets the same word throughout, governed by the glossary built in Phase 2. Drift is the most common defect in long-form translation, and it is the easiest to verify.
3. **Naturalness.** The result must read as if originally written in the target language. If a native reader would never phrase it that way, rewrite. "Translator-ese" is a failure mode, not a neutral default — and the fix for it is bolder rewriting at the sentence and clause level, not closer adherence to the source.
4. **Style and register preservation.** Academic stays academic, casual stays casual. Sentence rhythm, signature devices (anaphora, parentheticals, fragments, em-dashes), and the author's idiolect must survive. Resist the urge to "clean up" deliberate quirks.
5. **Pragmatic equivalence.** Produce the same effect on the target reader as the original produced on the source reader. A joke must remain funny; a polemic must remain pointed.
6. **Cultural appropriateness.** Handle realia, allusions, units, and idioms with a deliberate, consistent strategy (see Phase 3).
7. **Fit-to-purpose (skopos).** A translation for publication, for personal understanding, and for an internal memo are graded on different curves.

When naturalness and literal accuracy conflict, naturalness usually wins — unless the user has explicitly asked for a literal or scholarly rendering. When terminology consistency and naturalness conflict, prefer consistency for nouns and domain terms; allow variation for pronouns and connective tissue.

## Workflow

Translation moves through six phases: **analyze → glossary → strategy → translate → footnotes → review**. Do not skip phases. For very short inputs the phases can be compressed but never collapsed entirely.

### Phase 1 — Analyze the source

Before writing a single word of translation, read the whole text and note:

- **Source language**, including any dialect or regional markers.
- **Target language and locale** (en-US vs en-GB, pt-BR vs pt-PT, zh-CN vs zh-TW, etc.). Confirm with the user if ambiguous.
- **Genre and subgenre** — op-ed, technical tutorial, personal essay, news report, marketing copy, etc.
- **Register** — formal, neutral, conversational, slangy, academic.
- **Authorial voice and signature devices.** Be specific: "frequent em-dashed asides", "very short paragraphs", "favors latinate vocabulary", "drops articles for punch", "alternates long analytical sentences with one-line zingers". These notes will steer Phase 4.
- **Intended audience** of the original.
- **Purpose / skopos** — what is this text trying to do (inform, persuade, entertain, sell, document)?
- **Cultural anchoring** — is the text steeped in a specific time and place? How transparent will its references be to the target audience?
- **Structural outline.** Briefly map the argument: main thesis in one sentence, the role of each section (setup, evidence, counter-argument, payoff), and any recurring motifs or callbacks. This map is for internal use during Phase 4 — it prevents losing the logical thread when translating section by section.

If anything about target locale, audience, or purpose is genuinely ambiguous, ask the user **one focused question** before proceeding. Do not ask just to seem thorough.

### Phase 2 — Build the glossary

Before any translation, scan the full source and extract a glossary. The glossary is the single most effective defense against drift — the most common quality defect in long-form translation.

**Default behavior:**
- Texts >800 words with recurring proper nouns, technical terms, or leitmotifs → build a glossary.
- Texts <800 words with only a handful of unique terms → light glossary inline (just the few items that matter), or skip if the text has no repeating terms at all.
- Any text where the user asks for a quick rendering → judgment call; lean toward a minimal glossary covering just proper nouns and the 3-5 most repeated terms.

A glossary is not a bureaucratic ritual. It exists to prevent the same concept from being rendered three different ways across a long text. If the text has nothing to drift on, skip it.

**Always extract:**

- **Proper nouns** — people, places, organizations, products, publications. Decide once on transliteration vs. translation vs. preserving original script. Note whether to give the full name on first mention and a short form afterward.
- **Technical and domain terms** — pick the target-language equivalent and use it consistently.
- **Recurring phrases or leitmotifs** — if the author deliberately repeats a phrase (a coinage, a refrain, a key concept), preserve the repetition with a single fixed rendering.
- **Numbers, dates, measurements** — decide on format (1,000 vs 1.000; 5 km vs 3.1 mi; ISO dates vs locale dates) and whether to convert units. Be consistent.
- **Acronyms** — spell out on first mention with the original in parentheses, or use the target-language standard form if one exists.
- **Titles of works** — use the official translated title if one exists; otherwise transliterate or translate with the original in parentheses on first mention.
- **Quotations from third sources** — locate the canonical published translation if it exists; otherwise translate faithfully and flag the passage in the translator's notes.

**Glossary format:**

| Source | Target | Notes |
|---|---|---|
| [original term] | [chosen rendering] | [rationale, only when non-obvious] |

For long texts or texts with heavy domain terminology, **show the glossary to the user before starting the translation** and ask whether to proceed. For shorter texts (under ~1000 words), include the glossary inline at the top of the response and move on.

### Phase 3 — Strategy decisions

State the policy — briefly to yourself, and to the user when asked — for:

- **Domestication vs foreignization.** How much to adapt cultural references. Default to a middle stance: preserve names and culturally specific concepts, but unpack opaque references with a brief in-text clarification or a footnote.
- **Idioms and set expressions.** Apply this priority order:
  1. If the target language has a natural equivalent idiom → use it.
  2. If no equivalent but the figurative meaning carries clearly → paraphrase plainly. Do not invent a clunky calque just to mirror the original's figurativeness.
  3. If the expression is culturally or stylistically load-bearing (a famous quote, an allusion the author is clearly building meaning from, a phrase that is itself the point) → keep it (transliterated or rendered literally) and add a **footnote** explaining it.
  4. Never invent a target-language idiom that does not actually exist just to "match" the source's idiomatic register.
- **Units, dates, currencies.** Convert (e.g., miles → km, °F → °C) only when the original is communicating a sense of magnitude that the target audience would otherwise miss. Otherwise preserve and let context carry.
- **Punctuation and typography.** Switch to target-language conventions: en-dash and em-dash usage, «guillemets» vs "quotes" vs „lower-upper", spaces before punctuation (French), non-breaking spaces, ellipsis style, etc.
- **Paragraph and section structure.** Preserve. Do not merge or split paragraphs except to avoid genuinely unidiomatic results.

### Phase 4 — Translate in coherent units

**Translate in paragraph-sized or larger semantic units, never sentence-by-sentence.** Sentence-atomic translation preserves source syntax at the cost of argumentative flow, repetition, and cohesion — it is the second most common quality defect.

For each paragraph (or natural semantic unit):

1. Read the whole unit in the source.
2. Identify its function in the larger argument: claim, evidence, transition, aside, punchline, scene-setting.
3. Render it in the target language as a native writer would, preserving that function and the rhythm.
4. Apply the glossary consistently for every term.
5. Check the seam with the previous paragraph — does the cohesion connect cleanly (anaphora, "however", "by contrast", pronoun references)? Adjust if not.

Sentence boundaries can shift. Two short source sentences may merge in the target; one long source sentence may split. Do this only when it produces a more natural result, not as a default move.

**Style preservation tactics:**

- Match sentence-length distribution where possible — don't smooth a deliberately jagged style into uniform medium-length sentences.
- Preserve fragments, one-word paragraphs, em-dashes, parentheticals — these are usually deliberate authorial moves.
- Match density of clauses, not just word count.
- If the source uses repetition for emphasis, keep the repetition. Synonym variation that the source did not have is an addition.
- Resist the urge to "improve" the original. The author's quirks are the style.

### Phase 5 — Footnotes

Use translator footnotes sparingly. Each footnote interrupts reading, so the bar is high. Use them only when one of these holds:

- A source expression was preserved (rather than adapted) and the target reader cannot decode it without help.
- A cultural reference is load-bearing for the argument and not self-explanatory in the target context.
- A genuine ambiguity in the source had to be resolved in one direction, and the user might want to know.

**Format:**

- Mark in text with a superscript number or `[1]` after the relevant phrase.
- Collect notes at the end of the translation under a heading like `**Translator's notes**` or its target-language equivalent.
- Each note is one or two sentences. No mini-essays.

Do not footnote things the target reader can easily look up, or things with an obvious target-language equivalent — that is avoidance of the actual translation work, not service to the reader. Aim for fewer than ~1% of words requiring footnotes. If more, rethink the cultural adaptation strategy.

Never silently drop a difficult passage or paraphrase it past recognition. If a passage is genuinely ambiguous, resolve it one way and footnote the ambiguity.

### Phase 6 — Self-review before delivering

Run an explicit pass against the criteria. This is not optional — it is where most defects are caught.

- **Drift check.** For each glossary entry, confirm the chosen rendering was used every time the source term appears. Search the target text for unintended variants. Drift typically starts around the 60–70% mark of a long text — check there first.
- **Omission check.** Walk through the source paragraph by paragraph; confirm every proposition is present in the target.
- **Addition check.** Did any clarification or interpretation get smuggled in that the source did not have? If yes, either remove it or move it to a footnote.
- **Naturalness check.** Mentally read the target aloud. Any sentence that sounds translated should be rewritten.
- **Register check.** Sample 3–4 sentences from different parts of the text — do they all sit in the same register?
- **Style check.** Pick one paragraph from source and target. Same rhythm? Same density of clauses? Same use of dashes, parentheticals, fragments?

## Output structure

Default output, in this order:

1. **Glossary** — for texts over ~800 words, or shorter texts with dense domain terminology. Mark the section so the user can skip or collapse it.
2. **Translation** — full text in the target language, mirroring the source's structure (headings, paragraphs, lists, blockquotes, code blocks all preserved).
3. **Translator's notes** — only if footnotes were used or non-obvious decisions were made.
4. **Decision log** — optional, 2–4 lines, only when significant judgment calls were made that the user might want to know about. Examples: "Converted miles to km because the article relies on a sense of distance"; "Kept «гласность» untranslated with a footnote because glasnost carries historical weight that 'openness' loses".
5. **Flags for review** — optional, for long or technically dense texts. A short list of specific passages where the source was ambiguous and you had to choose an interpretation, terms where you were unsure of the target-language convention, or cultural references whose adaptation you'd want a second opinion on. Cite the passage by quoting 3–5 source words and stating the choice. Skip this section if there is nothing genuine to flag — do not manufacture flags for symmetry.

For shorter texts, drop sections 1, 4, and 5 unless they would actually help the user.

## File output

By default, save the translation as a separate file next to the original. Override only when the user explicitly asks for inline output.

**Source is an uploaded or referenced file** (e.g., `/path/to/article.md`):

- Write the translation to a new file in the same directory as the original, mirroring the original's extension where possible.
- Name it `<original-basename>-<target-lang>.<ext>`, using a two-letter language code (en, ru, de, fr, es, pt, zh, ja, etc.). Example: `article.md` → `article-en.md`. If the original already carries a language code (`article-ru.md`), swap it (`article-en.md`) rather than appending.
- Place the glossary, footnotes, and translator's notes inside the same file, in the order described in "Output structure" above. Do not split into multiple files unless the user asks.
- In the chat reply, point the user to the new file path and surface what needs attention — the glossary if substantial, decisions worth flagging, ambiguities resolved — without pasting the full translation back into chat.
- For complex source formats (`.docx`, `.pdf`, `.pptx`), use the corresponding document-creation skill, or ask the user whether a plain `.md` output is acceptable instead.

**Source was pasted directly into the chat** (no file path to anchor to):

- Produce the translation inline in the structure described in "Output structure".
- If the result is long (>~2000 words), offer to save it to a file — but do not save automatically without asking, since there is no original location to put it next to.

**Inline output is correct (not the file default) when:**

- The user explicitly asks for it ("just paste it here", "show it in chat", "in the response").
- The text is very short (under ~200 words) and a file would be overkill.
- The user is iterating on a specific passage or sentence rather than translating a whole document.

## Formatting and special cases

Mechanical formatting rules (headings, links, code, tables, YAML front matter,
HTML embeds) and special-case playbooks (embedded quotations, mixed-language
sources, headlines and pull quotes, very long texts >5000 words) live in
`references/formatting.md`. Read it before Phase 4 whenever the source is
anything richer than plain paragraphs. The one rule that never bends: when in
doubt about a syntactic element, leave it verbatim — breaking the document's
rendering is worse than under-translating an attribute value.

## Final note

Every translation choice should be defensible against the criteria above. When in doubt, prefer the rendering that a thoughtful native reader of the target language — one who also knows the source language — would call "obviously the right way to put it".
