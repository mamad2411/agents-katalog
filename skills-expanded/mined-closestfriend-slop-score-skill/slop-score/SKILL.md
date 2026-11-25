---
name: slop-score
description: Run Sam Paech's eqbench Slop Score heuristic against a piece of writing — scores AI "slop" (overused words, slop trigrams, and "not X, but Y" contrast patterns) on a 0–100 scale and flags the specific offending phrases. Use when the user wants to slop-score writing, check a draft for AI-slop / GPT-isms, or get a Paech-style slop readout. Independent of any literary-critic agent or persona.
---

# slop-score

Faithful standalone port of https://eqbench.com/slop-score.html. Reports the composite Slop Score (60% slop words + 25% not-x-but-y + 15% slop trigrams, leaderboard-normalized, `>25 = SLOP`) and the exact flagged phrases. **Flags, does not prescribe** — present the receipts; let the user decide what to cut.

## Invocation

`/slop-score <file-path>` — or paste text to score.

## Workflow

1. **Resolve input.**
   - File path given → use `--file <path>`.
   - Inline/pasted text → write it to a temp file and use `--file`, or pass `--text "<...>"` for short snippets.
   - Nothing given → ask the user for a file path or the text.
2. **Run the engine** from this skill's base directory (provided when the skill is invoked; the script self-resolves its data):
   ```bash
   node <skill-base-dir>/scripts/slop-score.mjs --file "<PATH>" --json
   ```
3. **Parse the JSON** and present three sections:
   - **Headline** — `slop_score`/100, verdict, and the three weighted sub-scores (`components`).
   - **Receipts** — `top_words`, `top_trigrams` (with counts), and `contrast_matches` (the actual sentences).
   - **Flag list** — rank the receipts by contribution; state which phrases drove the score. Do NOT author rewrites or tell the user to delete anything unless they ask.
4. If `stage2_enabled` is `false`, mention once: Stage-2 POS contrast patterns are off; enable with `cd <skill-base-dir> && npm install`.

## Boundaries

- Do not invoke literary-critic agents/personas or add philosophical/authorship interpretation. This skill is mechanical.
- If the user asks for rewrites after seeing flags, that's a separate request they can make to you directly.
