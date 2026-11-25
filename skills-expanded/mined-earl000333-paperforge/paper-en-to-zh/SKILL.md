---
name: paper-en-to-zh
description: Translate English LaTeX paper fragments into readable Chinese for fast understanding. Use when the task is to directly translate technical paper text, strip distracting LaTeX shell commands, and preserve terminology without doing stylistic rewriting.
---

# paper-en-to-zh

Translate English LaTeX paper text into direct Chinese explanation.

## Do

1. Remove `\cite{}`, `\ref{}`, `\label{}` and similar indexing commands when they do not affect meaning.
2. Keep technical terms stable and preserve model names, datasets, and variables.
3. Convert equations into readable Chinese descriptions when that improves comprehension.
4. Stay close to the source structure so the user can map the translation back to the original sentence.

## Avoid

- Polishing or strengthening the author's claims.
- Hiding original awkwardness if the source sentence is awkward.
- Expanding abbreviations unless the user explicitly asks.