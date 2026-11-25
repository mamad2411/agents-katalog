---
name: paper-zh-to-en
description: Convert Chinese research drafts into polished English LaTeX paragraphs for academic papers. Use when the task is to translate Chinese notes, methods, experiments, or abstract text into clean, publication-style English while preserving equations, variables, and technical meaning.
---

# paper-zh-to-en

Translate Chinese research text into concise English LaTeX prose.

## Do

1. Infer the section role if the user does not specify it.
2. Preserve formulas, variables, dataset names, and method names.
3. Use restrained academic English and default to present tense for methods and conclusions.
4. Escape `%`, `_`, `&` and other LaTeX-sensitive characters when needed.
5. Return an English LaTeX paragraph first, then a brief Chinese literal check if the user wants verification.

## Avoid

- Inventing experimental results or citations.
- Leaving untranslated Chinese phrases.
- Turning the text into bullet lists.
- Using exaggerated marketing language.