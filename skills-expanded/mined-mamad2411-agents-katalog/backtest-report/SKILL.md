---
name: backtest-report
description: >
  執行回測分析並生成績效報告。當使用者想查看策略表現、hit rate、alpha 績效、
  MAE/MFE 分析時使用。觸發詞: 回測, backtest, alpha分析, 績效追蹤,
  signal performance, 回測報告, backtest report, 策略績效, 勝率, hit rate
---

# Backtest Report

從 `data/data.db` 查詢回測相關資料，生成績效分析報告。

## Step 1: 更新信號績效數據 (可選)

如果使用者要求最新數據，先執行信號追蹤器:

```bash
cd "D:/VScode_project/NLP data for trading" && python -m src.signal_tracker
```

## Step 2: 綜合績效查詢

```bash
cd "D:/VScode_project/NLP data for trading" && python -c "
import sqlite3, os
conn = sqlite3.connect('data/data.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

print('=' * 70)
print('  PAM 回測績效報告')
print('=' * 70)

# --- Alpha Signals 總覽 ---
print('\n## Alpha Signals 總覽\n')
c.execute('SELECT COUNT(*) as total, AVG(expected_alpha_5d) as avg_5d, AVG(expected_alpha_20d) as avg_20d, AVG(confidence) as avg_conf, AVG(signal_strength) as avg_str FROM alpha_signals')
r = c.fetchone()
if r and r['total'] > 0:
    print(f'  總信號數: {r[\"total\"]}')
    print(f'  平均預期 Alpha 5d:  {r[\"avg_5d\"]:.4f}' if r['avg_5d'] else '  平均預期 Alpha 5d:  N/A')
    print(f'  平均預期 Alpha 20d: {r[\"avg_20d\"]:.4f}' if r['avg_20d'] else '  平均預期 Alpha 20d: N/A')
    print(f'  平均信心度: {r[\"avg_conf\"]:.4f}' if r['avg_conf'] else '  平均信心度: N/A')
    print(f'  平均信號強度: {r[\"avg_str\"]:.4f}' if r['avg_str'] else '  平均信號強度: N/A')
else:
    print('  [WARN] alpha_signals 表無資料')

# --- Direction 分布 ---
print('\n## Direction 分布\n')
c.execute('SELECT direction, COUNT(*) as cnt, AVG(signal_strength) as avg_str, AVG(expected_alpha_20d) as avg_a20 FROM alpha_signals GROUP BY direction')
for r in c.fetchall():
    avg_a = f'{r[\"avg_a20\"]:.4f}' if r['avg_a20'] else 'N/A'
    print(f'  {r[\"direction\"]:8s} | {r[\"cnt\"]:4d} signals | Avg Strength: {r[\"avg_str\"]:.4f} | Avg Alpha 20d: {avg_a}')

# --- Signal Performance (實際績效追蹤) ---
print('\n## 實際績效追蹤 (signal_performance)\n')
c.execute('SELECT COUNT(*) FROM signal_performance')
sp_count = c.fetchone()[0]
if sp_count > 0:
    c.execute('''
        SELECT COUNT(*) as total,
               SUM(CASE WHEN hit_5d = 1 THEN 1 ELSE 0 END) as hit5,
               SUM(CASE WHEN hit_20d = 1 THEN 1 END) as hit20,
               AVG(actual_alpha_5d) as avg_aa5,
               AVG(actual_alpha_20d) as avg_aa20,
               AVG(max_favorable_excursion) as avg_mfe,
               AVG(max_adverse_excursion) as avg_mae
        FROM signal_performance
    ''')
    r = c.fetchone()
    total = r['total']
    hit5 = r['hit5'] or 0
    hit20 = r['hit20'] or 0
    print(f'  已追蹤信號: {total}')
    print(f'  5d Hit Rate:  {hit5}/{total} = {hit5/total*100:.1f}%')
    print(f'  20d Hit Rate: {hit20}/{total} = {hit20/total*100:.1f}%')
    print(f'  平均實際 Alpha 5d:  {r[\"avg_aa5\"]:.4f}' if r['avg_aa5'] else '  平均實際 Alpha 5d:  N/A')
    print(f'  平均實際 Alpha 20d: {r[\"avg_aa20\"]:.4f}' if r['avg_aa20'] else '  平均實際 Alpha 20d: N/A')
    print(f'  平均 MFE (最大有利偏移): {r[\"avg_mfe\"]:.4f}' if r['avg_mfe'] else '  平均 MFE: N/A')
    print(f'  平均 MAE (最大不利偏移): {r[\"avg_mae\"]:.4f}' if r['avg_mae'] else '  平均 MAE: N/A')
    if r['avg_mfe'] and r['avg_mae'] and r['avg_mae'] != 0:
        print(f'  MFE/MAE Ratio: {abs(r[\"avg_mfe\"]/r[\"avg_mae\"]):.2f}')
else:
    print('  [INFO] signal_performance 表尚無資料，請先執行: python -m src.signal_tracker')

# --- Fama-French 三因子回測 ---
print('\n## Fama-French 三因子回測 (fama_french_results)\n')
c.execute('SELECT COUNT(*) FROM fama_french_results')
ff_count = c.fetchone()[0]
if ff_count > 0:
    c.execute('''
        SELECT direction,
               COUNT(*) as cnt,
               AVG(ff3_car_5d) as ff3_5,
               AVG(ff3_car_20d) as ff3_20,
               AVG(ff3_car_60d) as ff3_60,
               AVG(mkt_car_5d) as mkt_5,
               AVG(mkt_car_20d) as mkt_20,
               AVG(r_squared) as avg_r2
        FROM fama_french_results
        GROUP BY direction
    ''')
    for r in c.fetchall():
        print(f'  [{r[\"direction\"]}] (n={r[\"cnt\"]})')
        ff5 = f'{r[\"ff3_5\"]*100:.2f}%' if r['ff3_5'] else 'N/A'
        ff20 = f'{r[\"ff3_20\"]*100:.2f}%' if r['ff3_20'] else 'N/A'
        ff60 = f'{r[\"ff3_60\"]*100:.2f}%' if r['ff3_60'] else 'N/A'
        m5 = f'{r[\"mkt_5\"]*100:.2f}%' if r['mkt_5'] else 'N/A'
        m20 = f'{r[\"mkt_20\"]*100:.2f}%' if r['mkt_20'] else 'N/A'
        print(f'    FF3 CAR:  5d={ff5}  20d={ff20}  60d={ff60}')
        print(f'    MKT CAR:  5d={m5}  20d={m20}')
        print(f'    Avg R-squared: {r[\"avg_r2\"]:.4f}' if r['avg_r2'] else '    Avg R-squared: N/A')
else:
    print('  [INFO] fama_french_results 表尚無資料，請執行: python run_fama_french_backtest.py')

# --- 按議員分組績效 ---
print('\n## 議員績效 Top 10 (by signal count)\n')
c.execute('''
    SELECT politician_name, chamber, COUNT(*) as cnt,
           AVG(signal_strength) as avg_str,
           AVG(expected_alpha_20d) as avg_a20,
           politician_grade
    FROM alpha_signals
    GROUP BY politician_name
    ORDER BY cnt DESC
    LIMIT 10
''')
rows = c.fetchall()
if rows:
    print(f'  {\"議員\":20s} | {\"院別\":6s} | {\"信號數\":>6s} | {\"Avg強度\":>8s} | {\"Avg Alpha20d\":>12s} | {\"等級\":4s}')
    print('  ' + '-' * 68)
    for r in rows:
        a20 = f'{r[\"avg_a20\"]:.4f}' if r['avg_a20'] else 'N/A'
        grade = r['politician_grade'] or 'N/A'
        ch = r['chamber'] or '?'
        print(f'  {r[\"politician_name\"]:20s} | {ch:6s} | {r[\"cnt\"]:6d} | {r[\"avg_str\"]:8.4f} | {a20:>12s} | {grade:4s}')

# --- 按板塊分組績效 ---
print('\n## 板塊績效 (sector_rotation_signals)\n')
c.execute('SELECT COUNT(*) FROM sector_rotation_signals')
sr_count = c.fetchone()[0]
if sr_count > 0:
    c.execute('''
        SELECT sector, etf, direction, signal_strength, momentum_score,
               expected_alpha_20d, trades, politician_count, rotation_type
        FROM sector_rotation_signals
        ORDER BY signal_strength DESC
        LIMIT 10
    ''')
    for r in c.fetchall():
        ea = f'{r[\"expected_alpha_20d\"]:.4f}' if r['expected_alpha_20d'] else 'N/A'
        print(f'  {r[\"sector\"]:20s} ({r[\"etf\"]}) | {r[\"direction\"]} | Str={r[\"signal_strength\"]:.3f} | Mom={r[\"momentum_score\"]:.3f} | Alpha20d={ea} | {r[\"rotation_type\"]}')
else:
    print('  [INFO] sector_rotation_signals 表尚無資料')

# --- Win/Loss Summary ---
print('\n## Win/Loss 比率 (基於 expected_alpha_20d)\n')
c.execute('''
    SELECT
        COUNT(*) as total,
        SUM(CASE WHEN expected_alpha_20d > 0 THEN 1 ELSE 0 END) as positive,
        SUM(CASE WHEN expected_alpha_20d <= 0 THEN 1 ELSE 0 END) as negative
    FROM alpha_signals
    WHERE expected_alpha_20d IS NOT NULL
''')
r = c.fetchone()
if r and r['total'] > 0:
    pos = r['positive'] or 0
    neg = r['negative'] or 0
    print(f'  Positive Alpha: {pos} ({pos/r[\"total\"]*100:.1f}%)')
    print(f'  Negative Alpha: {neg} ({neg/r[\"total\"]*100:.1f}%)')
    print(f'  Win/Loss Ratio: {pos/neg:.2f}' if neg > 0 else '  Win/Loss Ratio: inf')

print('\n' + '=' * 70)
print('  報告結束')
print('=' * 70)
conn.close()
"
```

## Filtered Queries

根據使用者需求調整查詢:

- **特定議員**: 在 `alpha_signals` 查詢加 `WHERE politician_name LIKE '%name%'`
- **特定 Ticker**: 加 `WHERE ticker = 'XXXX'`
- **日期範圍**: 加 `WHERE created_at >= '2026-01-01'`
- **高信心度**: 加 `WHERE confidence >= 0.7`
- **特定板塊**: 在 `sector_rotation_signals` 查詢加 `WHERE sector = 'Technology'`

## Output Format

將結果整理為繁體中文 Markdown 報告，包含:
- 績效摘要表格
- 關鍵指標 (hit rate, alpha, MFE/MAE ratio)
- 議員/板塊排名
- 改善建議 (基於數據中的 pattern)
