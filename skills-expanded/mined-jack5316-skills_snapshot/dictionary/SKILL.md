---
name: dictionary
description: Search Longman Dictionary of Contemporary English (LDOCE) for word meaning, etymology (origin), and corpus examples. Use when user asks to look up a word, check definition, etymology, or /dictionary.
---

# Dictionary Skill (/dictionary)

Look up words in the Longman Dictionary of Contemporary English (LDOCE) — your favorite dictionary. Returns meaning, etymology (origin), and examples from the corpus.

## Quick Start

```bash
python3 _scripts/dictionary.py hello
```

## Options

- `word` (required): The word to look up
- `--save`: Save result to vault as `Atlas/Dictionary - WORD.md`
- `--no-save`: Print only (default)

## Examples

```bash
# Look up a word (print to terminal)
python3 _scripts/dictionary.py hello

# Look up and save to vault
python3 _scripts/dictionary.py "etymology" --save

# Phrasal verb or multi-word
python3 _scripts/dictionary.py "run out" --save
```

## Output

- **Terminal**: Formatted markdown with:
  - Headword, pronunciation (IPA), part of speech
  - **Meanings** — definitions with example sentences
  - **Etymology (Origin)** — word source and history
  - **Examples from the Corpus** — real usage examples
  - Variants (e.g., British spellings)
- **Saved note**: `Atlas/Dictionary - WORD.md` (when using `--save`)

## Source

Uses the [Pearson LDOCE API](https://api.pearson.com/v2/dictionaries) — no API key required.
