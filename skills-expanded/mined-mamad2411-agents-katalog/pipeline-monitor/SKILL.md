---
name: pipeline-monitor
description: >
  監控 ETL pipeline 執行歷史、成功/失敗率、各資料源新鮮度。
  觸發詞: pipeline 狀態, ETL 健康, pipeline monitor, extraction log,
  pipeline health, ETL status, 抓取狀態, 資料來源狀態, pipeline history
---

# Pipeline Monitor

查詢 `extraction_log` 和各資料表，評估 ETL pipeline 的健康狀態。

## Step 1: Pipeline 執行歷史 + 資料源狀態

```bash
cd "D:/VScode_project/NLP data for trading" && python -c "
import sqlite3
from datetime import datetime, date

conn = sqlite3.connect('data/data.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

print('=' * 70)
print('  PAM Pipeline Monitor')
print('=' * 70)

# --- 1. Extraction Log Summary ---
print('\n## 1. ETL Extraction Log\n')
c.execute('SELECT COUNT(*) FROM extraction_log')
total = c.fetchone()[0]
if total > 0:
    c.execute('''
        SELECT status, COUNT(*) as cnt,
               AVG(extracted_count) as avg_extracted,
               AVG(confidence) as avg_conf
        FROM extraction_log
        GROUP BY status
    ''')
    print(f'  Total extractions: {total}')
    for r in c.fetchall():
        avg_e = f'{r[\"avg_extracted\"]:.1f}' if r['avg_extracted'] else '0'
        avg_c = f'{r[\"avg_conf\"]:.3f}' if r['avg_conf'] else 'N/A'
        print(f'  {r[\"status\"]:15s}: {r[\"cnt\"]:4d} runs | Avg extracted: {avg_e} | Avg confidence: {avg_c}')

    # Success rate
    c.execute('SELECT COUNT(*) FROM extraction_log WHERE status = \"success\"')
    success = c.fetchone()[0]
    rate = success / total * 100 if total > 0 else 0
    print(f'\n  Success Rate: {success}/{total} = {rate:.1f}%')
    if rate < 80:
        print('  [WARN] Success rate below 80%!')

    # Recent extractions
    print('\n  Recent 10 extractions:')
    c.execute('''
        SELECT source_type, source_url, status, extracted_count,
               confidence, error_message, created_at
        FROM extraction_log
        ORDER BY created_at DESC
        LIMIT 10
    ''')
    for r in c.fetchall():
        err = f' | ERR: {r[\"error_message\"][:50]}' if r['error_message'] else ''
        src = (r['source_url'] or 'N/A')[:40]
        print(f'  {r[\"created_at\"]} | {r[\"source_type\"]:15s} | {r[\"status\"]:10s} | {r[\"extracted_count\"]:3d} recs | conf={r[\"confidence\"]:.2f}{err}')
else:
    print('  [INFO] extraction_log is empty - pipeline has not been run yet')

# --- 2. Data Source Freshness ---
print('\n## 2. Data Source Freshness\n')

sources = [
    ('Congress Trades (ETL)', 'congress_trades', 'created_at'),
    ('AI Discovery', 'ai_intelligence_signals', 'timestamp'),
    ('SEC Form 4', 'sec_form4_trades', 'created_at'),
    ('Signal Quality Scores', 'signal_quality_scores', 'scored_at'),
    ('Alpha Signals', 'alpha_signals', 'created_at'),
    ('Enhanced Signals', 'enhanced_signals', 'updated_at'),
    ('Convergence', 'convergence_signals', 'detected_at'),
    ('Sector Rotation', 'sector_rotation_signals', 'created_at'),
    ('Portfolio Positions', 'portfolio_positions', 'created_at'),
    ('Social Posts', 'social_posts', 'fetched_at'),
]

for label, table, date_col in sources:
    try:
        c.execute(f'SELECT COUNT(*) as cnt, MAX([{date_col}]) as latest FROM [{table}]')
        r = c.fetchone()
        latest = r['latest'] or 'Never'
        cnt = r['cnt']
        status = '[OK]' if cnt > 0 else '[EMPTY]'
        print(f'  {status} {label:30s}: {cnt:6d} rows | Latest: {str(latest)[:19]}')
    except Exception as e:
        print(f'  [ERR] {label:30s}: {e}')

# --- 3. Source Type Breakdown ---
print('\n## 3. ETL Source Breakdown\n')
c.execute('''
    SELECT source_format, COUNT(*) as cnt,
           AVG(extraction_confidence) as avg_conf
    FROM congress_trades
    GROUP BY source_format
''')
rows = c.fetchall()
if rows:
    for r in rows:
        fmt = r['source_format'] or 'Unknown'
        conf = f'{r[\"avg_conf\"]:.3f}' if r['avg_conf'] else 'N/A'
        print(f'  {fmt:20s}: {r[\"cnt\"]:4d} trades | Avg confidence: {conf}')

# --- 4. Recommendations ---
print('\n## 4. Recommendations\n')
c.execute('SELECT MAX(created_at) FROM congress_trades')
last_load = c.fetchone()[0]
if last_load:
    try:
        parts = str(last_load)[:10].split('-')
        load_date = date(int(parts[0]), int(parts[1]), int(parts[2]))
        age = (date.today() - load_date).days
        if age > 3:
            print(f'  [ACTION] Data is {age} days old. Run: python run_etl_pipeline.py --days 7')
        elif age > 1:
            print(f'  [INFO] Data is {age} days old. Consider running ETL soon.')
        else:
            print(f'  [OK] Data is fresh ({age} day(s) old)')
    except:
        pass

c.execute('SELECT COUNT(*) FROM social_posts')
if c.fetchone()[0] == 0:
    print('  [ACTION] Social media not configured. Set APIFY_API_TOKEN in .env')

c.execute('SELECT COUNT(*) FROM signal_performance')
if c.fetchone()[0] == 0:
    print('  [ACTION] Signal tracking not started. Run: python -m src.signal_tracker')

print('\n' + '=' * 70)
conn.close()
"
```

## Filtered Views

- **Failed extractions only**: Add `WHERE status != 'success'`
- **By source type**: Add `WHERE source_type LIKE '%senate%'`
- **Recent N days**: Add `WHERE created_at >= date('now', '-N days')`

## Output Format

Present in Traditional Chinese with:
- Pipeline health score
- Source freshness table
- Failed extraction details
- Actionable recommendations
