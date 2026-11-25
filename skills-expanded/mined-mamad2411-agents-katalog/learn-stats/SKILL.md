---
name: learn-stats
description: Report spaced-repetition statistics: total facts, overdue count, retention rate, active decks, and facts added this week. Use when the user says "stats", "estatísticas", "como está meu aprendizado", "/learn-stats", or wants a dashboard of their learning loop.
---

# Learn Stats

Reads `workspace/learning/facts/` and `workspace/learning/.state/review-log.jsonl` to produce a markdown stats report.

## Trigger

User wants a snapshot of their learning loop health.

## Workflow

### Step 1 — Read facts

1. Read all `.md` files in `workspace/learning/facts/`
2. Parse frontmatter of each file
3. Get today's date (YYYY-MM-DD)
4. Compute:
   - `total` = count of all fact files
   - `overdue` = count where `next_review <= today`
   - `active_decks` = count of unique `deck` values across all facts
   - `added_this_week` = count where `created >= today - 7 days`

If `workspace/learning/facts/` does not exist or is empty:
> "Nenhum fato encontrado. Use /learn-capture para adicionar fatos primeiro."
> Stop here.

### Step 2 — Read review log

1. Read `workspace/learning/.state/review-log.jsonl` line by line (each line is a JSON object)
2. If the file does not exist or is empty: `total_reviews = 0`, `retention_rate = "N/A"`
3. If it exists:
   - `total_reviews` = count of all log entries
   - `good_easy_count` = count where `grade == "good"` OR `grade == "easy"`
   - `retention_rate` = `round(good_easy_count / total_reviews * 100)%`

### Step 3 — Output report

Print in markdown, in **pt-BR**:

```markdown
## 📊 Learning Loop — Stats

| Métrica             | Valor        |
|---------------------|--------------|
| Total de fatos      | {total}      |
| Vencidos hoje       | {overdue}    |
| Taxa de retenção    | {retention_rate} ({good_easy_count}/{total_reviews} revisões) |
| Decks ativos        | {active_decks} |
| Adicionados (7 dias)| {added_this_week} |

**Data:** {today YYYY-MM-DD}
```

If `overdue > 0`:
> 💡 Use `/learn-review` para revisar os fatos vencidos.

If `total < 10`:
> 💡 Use `/learn-capture` para adicionar mais fatos (meta v0: 20 fatos em 2 semanas).

### Step 4 (optional) — List overdue facts

If `overdue > 0` and `overdue <= 10`, list them:

```
### Fatos vencidos
- `{filename}` (deck: {deck}, venceu: {next_review})
  > {Retrieval Q — first 80 chars}
```

## Constraints

- **Read-only.** Do NOT modify any file.
- Do NOT write to review-log.jsonl.
- If log is missing (user hasn't reviewed yet), show `N/A` for retention — do not error.
- Round retention_rate to nearest integer (no decimal places).
