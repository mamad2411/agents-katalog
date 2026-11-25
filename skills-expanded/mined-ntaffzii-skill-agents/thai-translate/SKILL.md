---
name: thai-translate
description: Use this skill for any task translating between English and Thai where tone, register, or pronoun choice matters — not just literal word substitution. Trigger on "แปลเป็นไทย", "แปลเป็นอังกฤษ", "translate to Thai", "translate to English", "EN-TH", "TH-EN", or any translation request involving Thai. If the source text is purely technical/machine-readable (e.g. translating a JSON key, a code comment with no audience), plain literal translation is fine and this skill's register guidance doesn't apply.
---

# Thai ⇄ English Translation

## Overview

English "you" and "I" are register-neutral; Thai is not. A literal translator maps "you" to คุณ everywhere, but a Thai speaker chooses among คุณ/ท่าน/พี่/น้อง/เธอ (and drops the pronoun entirely in many sentences) based on relative age, social distance, and formality — getting this wrong doesn't just sound stiff, it can read as rude or oddly intimate. This skill is the register/pronoun decision layer on top of translation, not a dictionary.

## When to use

- แปล EN → TH หรือ TH → EN ที่มีบริบทของความสัมพันธ์ระหว่างผู้พูด-ผู้ฟัง (ลูกค้า, เพื่อนร่วมงาน, ผู้บังคับบัญชา, คนแปลกหน้า)
- แปลเอกสารที่ต้องคง tone (ทางการ/กึ่งทางการ/กันเอง)
- Translating dialogue, marketing copy, or correspondence where "who is speaking to whom" changes the correct pronoun and sentence-final particle
- Deciding whether a literal translation of an idiom will land, or needs a Thai-native equivalent instead

## When NOT to use

- Machine-readable text with no human register (code, JSON keys, log messages) — plain literal translation is correct here, don't add pronouns or particles that don't belong
- The task is really `thai-government-form` (formal letter salutation hierarchy) or `thai-customer-service` (apology-ladder register for support replies) — those skills have more specific register rules than general translation guidance; use them instead when the context matches

## Core knowledge

**Pronoun choice for "you" (2nd person)** — pick by relationship, not by default:

| Thai | Register / relationship |
|---|---|
| คุณ | Neutral-polite default between adults who aren't close — safest default for a stranger or professional context without a clearer signal |
| ท่าน | High formal/respectful — addressing someone senior, a customer in very formal business writing, or in official documents |
| พี่ / น้อง | Used when relative age is known and the relationship is warm/informal — พี่ to someone older, น้อง to someone younger; wrong direction reads as presumptuous or oddly casual |
| เธอ | Informal, used among peers or by an older speaker to a clearly younger one; too casual for a stranger or professional context |
| Name / title + name | Common substitute for "you" in Thai — often more natural than any pronoun, especially in professional writing |

**Pronoun choice for "I" (1st person)**: ผม (male, standard-polite), ดิฉัน (female, formal-polite), ฉัน (informal, either gender in casual writing, traditionally more female-coded in spoken use), เรา (informal "we/I", common in casual spoken Thai). Match the assumed speaker's gender/formality from context; if unknown, default to a gender-neutral phrasing or ask rather than guessing wrong in a formal document.

**Sentence-final politeness particles**: ครับ (male speaker, polite) / ค่ะ, คะ (female speaker, polite: ค่ะ for statements, คะ for questions) — dropping these in written Thai reads as blunt or curt in contexts where politeness is expected (customer-facing text, formal writing). Not needed in neutral/technical writing.

**Classifiers (ลักษณนาม)**: Thai requires a classifier word when counting nouns — "3 books" is หนังสือ 3 เล่ม, not หนังสือ 3. Omitting the classifier or using the wrong one (each noun category has its own) is a common literal-translation error.

**Idioms**: translate for meaning, not word-for-word. A literal translation of an English idiom into Thai (or vice versa) frequently produces something grammatical but meaningless to a native reader — when an idiom doesn't have a natural Thai/English equivalent, paraphrase the underlying meaning instead of forcing a literal match.

## Common mistakes

1. Mapping "you" to คุณ unconditionally, ignoring that ท่าน/พี่/น้อง/name-substitution may be more correct for the actual relationship.
2. Using the wrong-direction พี่/น้อง (calling an older person น้อง, or a younger person พี่).
3. Dropping ครับ/ค่ะ in a context that calls for spoken-register politeness (e.g. a customer-facing chat reply).
4. Omitting or misusing a ลักษณนาม (classifier) when translating a counted noun into Thai.
5. Translating an idiom word-for-word instead of finding the equivalent meaning.
6. Keeping English sentence structure/word order in Thai output instead of restructuring for natural Thai syntax (Thai is more topic-comment and drops pronouns more freely than English).
7. Using ฉัน/เรา in a formal written document where ดิฉัน/ผม (or avoiding the pronoun and using a title) would be expected.

## Known limitations

- Register choice depends on context this skill can't always infer (exact relationship, company culture, regional norms) — when the relationship is ambiguous and the document is formal or customer-facing, default to the safest neutral-polite option (คุณ / ครับ-ค่ะ) and flag the choice to the user rather than guessing at a warmer register.
- This skill covers general register/pronoun mechanics, not specialized terminology (legal, medical, technical) — domain-specific vocabulary should still be verified against a subject-matter glossary.
