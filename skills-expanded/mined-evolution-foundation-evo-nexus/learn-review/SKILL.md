---
name: learn-review
description: Review spaced-repetition facts that are due today. Applies SM-2 algorithm to update interval, ease, and next_review in each fact's frontmatter. Updates review-log.jsonl. Use when the user says "revisar", "review facts", "study", or "/learn-review".
---

# Learn Review

Reviews facts in `workspace/learning/facts/` whose `next_review` date is today or in the past. Applies SM-2 grading and rewrites frontmatter in-place. Records every grade in `workspace/learning/.state/review-log.jsonl`.

## SM-2 Formula (implement exactly as specified)

Given current `reps`, `interval`, `ease`, `lapses`:

**Again (grade 0):**
- `reps = 0`
- `interval = 1`
- `ease = max(1.3, ease - 0.2)` (round to 2 decimal places)
- `lapses = lapses + 1`

**Hard (grade 3):**
- `interval = round(interval * 1.2)`  (minimum 1)
- `ease = max(1.3, ease - 0.15)` (round to 2 decimal places)
- `reps = reps + 1`

**Good (grade 4):**
- If `reps == 0`: `interval = 1`
- Else if `reps == 1`: `interval = 6`
- Else: `interval = round(interval * ease)`  (minimum 1)
- `ease` is unchanged
- `reps = reps + 1`

**Easy (grade 5):**
- Same interval as Good, then additionally: `interval = round(interval * 1.3)` (minimum 1)
- `ease = ease + 0.15` (round to 2 decimal places)
- `reps = reps + 1`

**For all grades:** `next_review = review_date + interval days`

**Ease floor:** 1.3. Never let ease drop below 1.3 regardless of how many Again grades.

## Workflow

### Step 1 — Scan for due facts

1. Read all `.md` files in `workspace/learning/facts/`
2. Parse the frontmatter of each file
3. Get today's date (YYYY-MM-DD)
4. Select facts where `next_review <= today`
5. Sort by `next_review` ascending (oldest due first)
6. Take up to 5 facts (N=5 default)

If no facts are due:
> "Nenhum fato vencido hoje. 🎉 Próxima revisão: {earliest next_review across all facts}."
> Stop here.

If `workspace/learning/facts/` does not exist or is empty:
> "Nenhum fato encontrado. Use /learn-capture para adicionar fatos primeiro."
> Stop here.

### Step 2 — Review loop (one fact at a time)

For each due fact (up to 5):

**2a. Show the question:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 Deck: {deck} | Fato {current}/{total_due_shown}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❓ {Retrieval Q content}

[Pense na resposta antes de prosseguir. Pressione Enter quando pronto.]
```

Wait for the user to confirm they've thought about it (any input is fine).

**2b. Show the answer:**
```
✅ Resposta:
{Fact content}

💡 Por quê importa:
{Why it matters content}
```

**2c. Ask for grade:**
```
Como foi? 
  0 - Again  (errei / não lembrei)
  3 - Hard   (lembrei com dificuldade)
  4 - Good   (lembrei bem)
  5 - Easy   (muito fácil)
```

Wait for the user to enter 0, 3, 4, or 5. Accept also the words "again", "hard", "good", "easy" (case-insensitive).

### Step 3 — Apply SM-2 and update file

For the grade received:

1. Compute `prev_interval = current interval`  
2. Compute `prev_ease = current ease`  
3. Apply SM-2 formula above to get `new_interval`, `new_ease`, `new_reps`, `new_lapses`
4. Compute `new_next_review = today + new_interval days`
5. Rewrite the fact file with updated frontmatter, preserving the body content exactly

**Frontmatter rewrite rules:**
- Update only: `next_review`, `interval`, `ease`, `reps`, `lapses`
- Preserve all other fields unchanged: `id`, `source`, `deck`, `created`
- Preserve the body (everything after the closing `---`) exactly as-is

### Step 4 — Append to review log

Append one JSON line to `workspace/learning/.state/review-log.jsonl` (create file if it doesn't exist, create directory if needed):

```json
{"ts": "{ISO8601_timestamp}", "fact_id": "{id}", "grade": "{again|hard|good|easy}", "prev_interval": {N}, "new_interval": {M}, "prev_ease": {X}, "new_ease": {Y}}
```

Grade string mapping: 0→"again", 3→"hard", 4→"good", 5→"easy"

### Step 5 — Next fact

Continue with the next due fact. After all N facts (or all due facts if < N):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Sessão de revisão concluída!
Revisados: {N} fatos
Resultado: {X} Good/Easy | {Y} Hard | {Z} Again
Próxima revisão: {earliest next_review across all facts}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Verification helper (Grade Good progression)

When testing, the interval sequence for repeated Good grades starting from `reps=0, interval=1, ease=2.5`:

| Review | Grade | reps before | interval before | → reps after | → interval after |
|--------|-------|-------------|-----------------|--------------|-----------------|
| 1st    | Good  | 0           | 1               | 1            | 1               |
| 2nd    | Good  | 1           | 1               | 2            | 6               |
| 3rd    | Good  | 2           | 6               | 3            | 15 (round(6*2.5))|

## Constraints

- Max N=5 facts per session. If more are due, the user can run again.
- ONLY update files in `workspace/learning/facts/` and `workspace/learning/.state/review-log.jsonl`.
- Do NOT modify `deck` metadata files or any file outside these two locations.
- Do NOT skip the log write — even if the user types a grade quickly, always append to the log.
- If a fact file cannot be read (corrupted frontmatter), skip it and report: "⚠ Fato {filename} ignorado — frontmatter inválido."
