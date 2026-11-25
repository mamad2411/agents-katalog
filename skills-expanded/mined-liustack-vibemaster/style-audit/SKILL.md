---
name: style-audit
description: Audit product texts (skills, references, READMEs, rules) against the expression-style disciplines — unexplained coined terms, transliterated loan-words, semicolons, source-citation leaks. Use when asked to 黑话审计 / style audit / 审查表达风格 / check the writing style, or before shipping a batch of skill copy.
---

# style-audit: expression-style audit for product texts

Project-local authoring tool. The shipped product lives in `skills/` — this skill never ships with it.

## Two layers, one ratchet

- **This skill is the judgment layer**: it finds what a script cannot — coined labels without an in-sentence explanation, loan-word nouns minted from foreign material, process traces in product copy.
- **`scripts/check-style.sh` is the mechanical layer**: a banned-term list plus a semicolon check, wired into CI. It only knows what audits have already found.
- **The ratchet**: every term an audit purges gets appended to `BANNED` in `scripts/check-style.sh`, so it can never come back.

## Disciplines to audit against

1. **Plain language** (`rules/plain-language.md`): everyday words over terminology — the test is whether a reader outside the project understands without looking anything up. Coined labels and metaphors must be explained in the same sentence on first use. Foreign material is described in your own words, not transliterated into a pet noun.
2. **Punctuation** (`rules/punctuation.md`): no semicolons in prose. The script catches this — spot-check only.
3. **Content discipline**: no source citations in product copy (no "per X's book", no repo credits), no process traces ("changed because review said"), no invented metaphors.

## Procedure

1. Scope: changed files by default (`git diff --name-only`), or all of `skills/`, `rules/`, `README*` on request. `.zh-CN` translations are held to the same bar.
2. Report each finding as: the term or sentence, a quoted line, why it fails (one clause), and a concrete fix — a plain rewrite or an in-sentence explanation, with exact wording.
3. Err on the side of silence: report only what an outside reader would actually stumble on. Terms explained in place, industry-standard vocabulary (API, spec, TDD, AARRR), and skill or product names are not findings.
4. After fixes land and a term is fully purged, append it to `BANNED` in `scripts/check-style.sh` — in both stacks if it appeared in both.
5. Run `bash scripts/check-style.sh` and confirm green before committing.
