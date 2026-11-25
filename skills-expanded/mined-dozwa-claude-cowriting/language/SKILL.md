---
name: language
description: Grammar, spelling and punctuation check (EN/DE) with corrected forms and the rule behind each correction. Use when the author asks for proofreading of their text.
---

# Language check

The author allowed corrected forms for **correctness** issues. Read the named passage and output a table:

| Location | Original | Corrected | Rule |
|---|---|---|---|

- Only real errors: grammar, spelling, punctuation, agreement, tense consistency, typography. In German also comma rules and Groß-/Kleinschreibung; in English also article use and hyphenation of compound modifiers.
- Do **not** restyle correct sentences. For style issues (wordiness, unclear reference, nominal style) add a second list "Style hints" with location + rule, **without** a rewrite.
- Leave LaTeX commands, citekeys, labels, math and Markdown syntax untouched.
- Remind the author: language corrections are logged under `language` in the AI log.
