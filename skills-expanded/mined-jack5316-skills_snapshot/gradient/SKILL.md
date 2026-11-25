---
name: gradient
description: Gradient descent inspired iterative refinement - gradually improve ideas, text, and solutions through multiple refinement cycles. Use when you want to iteratively improve something, get constructive critique, compare versions, or progressively enhance your work.
---

# Gradient Skill

Iteratively refines ideas, text, and solutions through multiple improvement cycles. Inspired by gradient descent — small targeted steps toward a goal.

## Usage

```bash
python3 _scripts/gradient.py --file draft.md --refine
python3 _scripts/gradient.py --text "My idea" --iterations 3
```

## Options

- `--text TEXT` — Text to refine directly
- `--file FILE` — File to read content from
- `--refine` — Single refinement iteration
- `--iterations N` — Number of refinement cycles
- `--critique` — Provide feedback without rewriting
- `--compare FILE` — A/B comparison of two versions
- `--enhance` — Focus on specific aspects (`--aspects clarity depth practicality`)
- `--progressive` — Iterate until convergence
- `--goal TEXT` — Goal for the refinement
- `--save` — Save output to vault

## Output

`Sources/Gradient - [topic] - YYYY-MM-DD.md`
