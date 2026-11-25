---
name: arabic-writing
description: >-
  Write and translate natural, grammatically correct Arabic — Modern Standard Arabic
  plus Egyptian, Levantine, Gulf, and Maghrebi dialects — that avoids machine-translation
  tells. Use whenever producing Arabic prose: writing original Arabic, translating into
  Arabic (especially from English), or editing/proofreading Arabic for grammar, spelling
  (hamza, ة/ه, ى/ي), agreement, collocations, punctuation, register, or naturalness. Use
  even when the user only asks to "say this in Arabic" or pastes Arabic text to fix.
license: MIT
---

# Writing natural, correct Arabic

This skill helps you produce Arabic that a native editor would accept: grammatically
correct, idiomatic, free of typos, and free of the tell-tale signs of machine translation.
The single biggest failure mode is **translationese** — transferring English structure
word-for-word instead of re-composing the meaning in Arabic. Translate ideas, not words.

## Workflow

1. **Pick the register and dialect.** Default to **Modern Standard Arabic (MSA / الفصحى)**
   for anything formal: news, documents, legal/medical text, UI body copy, subtitles. Use a
   **dialect** (Egyptian, Levantine, Gulf, Maghrebi) or light "white Arabic" only when the
   context is conversational, marketing, social, or the user asks for it. When unsure, ask
   which dialect/market — never silently mix dialect into formal MSA. See
   [register-and-style.md](references/register-and-style.md).
2. **Compose, don't transfer.** Read the whole source sentence, understand the meaning, then
   write it the way an Arabic speaker would — usually a verb-first sentence with the right
   collocation — rather than mapping English word order and prepositions.
3. **Self-check** every output against the two checklists below before returning it.
4. **Open the relevant reference file** whenever you are unsure about a specific rule. The
   reference files hold the detail; this page is just the map.

## Top correctness checklist (apply to every Arabic output)

1. **Non-human plurals take feminine-singular agreement.** الكتبُ **جديدةٌ** ("the books are
   new"), السياراتُ **سريعةٌ** — not جُدُد/سريعات. This is the #1 error. (→ grammar.md)
2. **Verb–subject order changes agreement.** Verb *before* subject (VSO, the neutral order)
   stays **singular** and agrees only in gender: **ذهب** الطلابُ / **ذهبت** الطالباتُ. Subject
   *before* verb (SVO) takes **full** agreement: الطلابُ **ذهبوا**. (→ grammar.md)
3. **Iḍāfa (الإضافة):** the first noun (مضاف) takes **no ال and no tanwin**; the second is
   genitive. كتابُ الطالبِ, not الكتابُ الطالبِ. No adjective between the two parts. (→ grammar.md)
4. **Adjectives follow the noun and agree on all four axes:** gender, number, case,
   definiteness. البنتُ الكبيرةُ (both definite) vs البنتُ كبيرةٌ ("the girl is big"). (→ grammar.md)
5. **Numbers 3–10 reverse gender** (polarity) and take a plural genitive noun: ثلاثةُ رجالٍ,
   ثلاثُ فتياتٍ. 11–99 take a singular accusative (tamyīz): عشرون كتابًا. (→ grammar.md)
6. **Hamza** sits on the seat of the **strongest vowel** (kasra ئ > damma ؤ > fatha أ > sukūn
   ء): رئيس، مسؤول، سأل، شيء. Distinguish wasl (bare ا) from qatʿ (أ/إ) with the و-test. (→ orthography.md)
7. **ة vs ه** (add a suffix: /t/ → ة, /h/ → ه) and **ى vs ي** (trace the root; على the
   preposition vs عليّ the name). (→ orthography.md)
8. **Use Arabic punctuation glyphs** ، ؛ ؟ (not , ; ?). No space before a mark, one after.
   In lists, repeat **و** instead of using commas. (→ orthography.md)
9. **Default to undiacritized text;** add ḥarakāt only to remove genuine ambiguity, but always
   keep a meaning-distinctive shadda (درس vs درّس). Never use kashida (ـــ) to pad. (→ orthography.md)
10. **Right collocations and prepositions.** اتخذ قرارًا (not عمل قرارًا), أثّر **في** (not على
    in formal MSA), حصل **على**. (→ collocations.md, translationese.md)

## The AI-Arabic "smell test" (avoid these tells)

If your draft contains several of these, it reads as machine-made. Fix each:

- **من قبل + passive** → use the active voice and name the agent. ✗ تمت مراجعة الخطة من قبل
  اللجنة → ✓ راجعت اللجنةُ الخطة.
- **قام/قم بـ + verbal noun** → use the single verb. ✗ قام بزيارة → ✓ زار. ✗ قم بإدخال كلمة
  المرور → ✓ أدخِل كلمة المرور (or the noun إدخال… for a UI label).
- **الخاص بك for every "your"** → use the attached suffix. ✗ الحساب الخاص بك → ✓ حسابك.
- **Overused يتم / تمّ** as an all-purpose passive → prefer a real verb or the internal
  passive. ✗ يتم استخدام الأداة → ✓ تُستخدَم الأداة.
- **حيث as a catch-all "where/which/whereby"** → use الذي/التي, إذ, لأنّ, بحيث, or بينما, and
  reserve حيث for an actual place/locus.
- **The copular calque "الهدف من … هو …"** → front the verb. ✓ يهدف هذا البحث إلى…
- **Agreement that drifts over distance** (a feminine/plural subject far from its verb
  defaulting to masculine) — re-check agreement across the whole sentence.
- **Connector over-explicitation** — stacking بالإضافة إلى ذلك، علاوة على ذلك، من ناحية أخرى.
  Native Arabic links clauses with و / فـ / ثم; use heavier connectors sparingly and precisely.
- **Doubled كلما** ("the more… the more") → use it once: كلما أعطيتَ، أخذت.

## Where to look (reference files)

| Read this when… | File |
|---|---|
| Anything about grammar: word order, case (إعراب), agreement, iḍāfa, numbers | [references/grammar.md](references/grammar.md) |
| Spelling: hamza, ة/ه, ى/ي, ا/أ, tanwin, punctuation, typos, diacritics | [references/orthography.md](references/orthography.md) |
| Removing MT/AI tells; English→Arabic structural pitfalls | [references/translationese.md](references/translationese.md) |
| Choosing the natural Arabic verb/phrase instead of a calque | [references/collocations.md](references/collocations.md) |
| Register choice, connectors, naturalness, tone/transcreation | [references/register-and-style.md](references/register-and-style.md) |
| Names, transliteration, numerals, dates, currency/units, bidi | [references/conventions.md](references/conventions.md) |
| Writing in Egyptian Arabic | [references/dialects/egyptian.md](references/dialects/egyptian.md) |
| Writing in Levantine Arabic | [references/dialects/levantine.md](references/dialects/levantine.md) |
| Writing in Gulf Arabic | [references/dialects/gulf.md](references/dialects/gulf.md) |
| Writing in Maghrebi Arabic | [references/dialects/maghrebi.md](references/dialects/maghrebi.md) |

## Register / dialect decision guide

- **MSA (الفصحى):** legal, medical, academic, official, news, manuals, B2B docs, subtitles,
  and most UI body text. The safe default.
- **Dialect or "white Arabic":** ads, social posts, voiceover, chat, conversational UX, or
  whenever the user names a market/dialect. Pick the dialect for the target country; do not
  ship one Arabic for all 22 countries.
- **Never** leak dialect lexis or grammar (e.g. عايز، بدّي، مش، بيكتب، هيروح) into formal MSA,
  and never mix two dialects in one piece. Keep one register and one dialect throughout.

When proofreading existing Arabic, read [orthography.md](references/orthography.md) and
[grammar.md](references/grammar.md) and report fixes in pass order: hamza → ة/ه and ى/ي →
tanwin → spacing → punctuation → agreement → consistency.
