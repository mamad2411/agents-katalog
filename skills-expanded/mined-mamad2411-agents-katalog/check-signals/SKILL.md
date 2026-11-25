---
name: check-signals
description: Query and display recent AI trading signals from the database. Use when the user wants to review latest intelligence signals, check impact scores, or see what the AI discovery engine has found for congressional trading activity.
---

# Check Signals

Query the `ai_intelligence_signals` table in `data/data.db` and present results.

## Default Query (latest 20 signals)

```bash
python -c "
import sqlite3, os
conn = sqlite3.connect('data/data.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute('''
    SELECT source_type, source_name, ticker, impact_score, sentiment,
           recommended_execution, timestamp, logic_reasoning
    FROM ai_intelligence_signals
    ORDER BY timestamp DESC
    LIMIT 20
''')
rows = c.fetchall()
if not rows:
    print('No signals found.')
else:
    for r in rows:
        exe = r['recommended_execution'] or 'N/A'
        ticker = r['ticker'] or 'N/A'
        score = r['impact_score'] or 0
        print(f\"[{r['timestamp']}] {r['source_name']} | {ticker} | Score: {score} | {r['sentiment']} | {exe}\")
        if r['logic_reasoning']:
            print(f\"  -> {r['logic_reasoning'][:120]}\")
        print()
conn.close()
"
```

## Filtered Queries

Adapt the query based on user request:

- **By politician**: Add `WHERE source_name LIKE '%name%'`
- **High impact only**: Add `WHERE impact_score >= 8`
- **By ticker**: Add `WHERE ticker = 'XXXX'`
- **OPEN signals only**: Add `WHERE recommended_execution = 'OPEN'`
- **Date range**: Add `WHERE timestamp >= '2025-01-01'`

## Output Format

Present results as a markdown table with columns:
| Time | Politician | Ticker | Score | Sentiment | Action | Reasoning |
