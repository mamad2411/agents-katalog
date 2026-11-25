---
name: thai-text-processing
description: Use this skill for any task involving Thai word segmentation/tokenization, Unicode normalization of Thai text, Thai-aware sorting/collation, or romanization (Thai script to Latin script). Trigger on "ตัดคำภาษาไทย", "tokenize Thai", "normalize Thai text", "Thai collation", "romanize Thai", "RTGS", "PyThaiNLP". If the task is just reading/writing Thai text without any programmatic string manipulation (segmentation, sorting, comparison), this skill isn't needed — plain text handling is fine.
---

# Thai Text Processing (Segmentation, Normalization, Collation, Romanization)

## Overview

Thai script has no spaces between words within a sentence — `"ฉันรักการเขียนโค้ด".split(" ")` returns the entire string as one token, not a word list, because there is nothing to split on. A model without this skill reaches for whitespace-based tokenization out of habit (it works for English) and silently produces garbage for Thai. This skill flags that failure mode and points to the correct tools — it does not reimplement a Thai tokenizer or transliterator, since both need a maintained dictionary/model to be accurate, not hand-written rules.

## When to use

- ตัดคำภาษาไทยเป็นคำๆ (word segmentation/tokenization) สำหรับ search, NLP, หรือ text analytics
- Normalizing Thai text before comparison, search, deduplication, or storage (Unicode NFC)
- Sorting Thai strings correctly (Thai collation order differs from raw Unicode codepoint order)
- Romanizing Thai text to Latin script (e.g. for a passport-style name, a street sign, or an international form) using the RTGS (Royal Thai General System of Transcription) convention

## When NOT to use

- Plain reading/writing/translating Thai text with no segmentation, sorting, or comparison step involved
- The romanization only needs to be "readable," not standards-compliant (e.g. casual transliteration in a chat) — RTGS precision isn't necessary there

## Core knowledge

**Word segmentation**: Thai does not use spaces between words (spaces mark clause/sentence boundaries, not word boundaries). Segmentation requires a dictionary- or model-based tokenizer — [PyThaiNLP](https://pythainlp.org/) (`pip install pythainlp`, `pythainlp.tokenize.word_tokenize`) is the standard open-source option. This skill does not vendor or reimplement a tokenizer; a hand-rolled rule-based splitter would silently produce wrong word boundaries on real text.

**Unicode normalization (NFC)**: Thai vowels and tone marks are combining Unicode characters. The same visible text can be encoded as a single precomposed codepoint or as a base character plus a combining mark — two strings that look identical can compare unequal, fail a lookup, or break deduplication if they aren't normalized to the same form first. Normalize to **NFC** (`unicodedata.normalize("NFC", text)`, pure Python stdlib, no dependency needed) before comparing, searching, hashing, or storing user-submitted Thai text.

**Collation (sorting)**: Thai alphabetical order is not the same as sorting by raw Unicode codepoint value — vowels that visually appear before their consonant (เ, แ, โ, ใ, ไ) are still ordered by the consonant they attach to, and tone marks/other combining characters sort after the base character rather than by codepoint. A naive `sorted()` on raw strings gives an order a Thai reader won't recognize as alphabetical. Correct collation needs locale-aware sorting (e.g. Python's `locale` module with a Thai locale, or ICU-based collation via a library like `PyICU`) — this skill flags the need, it does not implement a full Thai collation table by hand.

**Romanization (RTGS)**: the Royal Institute's RTGS (Royal Thai General System of Transcription) is Thailand's official Thai-to-Latin transliteration standard, used on road signs and in official documents. It is **not** a simple 1:1 letter-substitution — the same Thai consonant can romanize differently depending on its position in a syllable (initial vs. final), and several distinct Thai sounds collapse to the same Latin letter (RTGS deliberately drops tone marks). Use a maintained implementation (e.g. PyThaiNLP's `romanize()` function) rather than hand-writing substitution rules — the exception list is large enough that an ad hoc mapping will be wrong on real names/addresses often enough to matter.

## Common mistakes

1. Using `.split(" ")` (or any whitespace-based split) as if it segments Thai words — it doesn't, because Thai doesn't use spaces between words.
2. Comparing or deduplicating Thai strings without normalizing to NFC first, causing visually-identical text to be treated as different.
3. Sorting Thai text with a plain codepoint-based `sorted()` and presenting it as "alphabetical order" — a Thai reader will notice it's wrong, particularly around the leading vowels (เ/แ/โ/ใ/ไ).
4. Hand-writing a Thai-to-Latin transliteration table instead of using a maintained RTGS implementation — the exceptions are numerous enough that ad hoc rules produce visibly wrong romanizations on real names.
5. Assuming a segmented word list can be rejoined with spaces to reconstruct "readable" Thai — spaces between every word are not natural Thai writing; only use segmentation output for machine processing (search indexes, NLP pipelines), not for display back to a Thai reader.

## Code

`examples/normalize.py` — pure stdlib NFC normalization, no dependency. Run `python3 normalize.py` for the self-test.

`examples/segmentation.py` — demonstrates the naive-split failure (dependency-free) and wraps PyThaiNLP's tokenizer if installed (`pip install pythainlp`). Run `python3 segmentation.py`; the tokenizer half of the self-test runs only if PyThaiNLP is present, and reports a clear skip message if not.

## Known limitations

- This skill deliberately does not vendor PyThaiNLP or any transliteration table — those are maintained third-party projects with their own update cadence (dictionary coverage, model accuracy); pin and install them as a real dependency in the target project rather than copying code out of this skill.
- Collation is described here, not implemented — there's no dependency-free stdlib equivalent to a full Thai ICU collation table worth hand-rolling.
- RTGS romanization is lossy by design (drops tone information) — it is the *official* transliteration standard, not necessarily the most phonetically precise one; if the task needs tone-preserving phonetic transcription, RTGS is the wrong tool.
