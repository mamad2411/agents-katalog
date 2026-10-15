---
name: alpha-review
description: >
  檢視當前 alpha 信號品質，顯示 top picks 和投資建議。當使用者想看最佳信號、
  信號排名、投資建議時使用。觸發詞: alpha信號, signal review, 信號檢視,
  top picks, 最佳信號, alpha review, 投資信號, 信號排名, 買什麼, 推薦
---

# Alpha Review

從 `data/data.db` 查詢原始與增強 alpha 信號，生成投資信號檢視報告。

## Step 1: Alpha 信號總覽 + Top Picks

```bash
cd "D:/VScode_project/NLP data for trading" && python -c "
import sqlite3
conn = sqlite3.connect('data/data.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

print('=' * 80)
print('  PAM Alpha 信號檢視報告')
print('=' * 80)

# --- 原始 Alpha Signals Top 10 ---
print('\n## 原始 Alpha Signals Top 10 (by signal_strength)\n')
c.execute('''
    SELECT ticker, asset_name, politician_name, chamber, direction,
           transaction_type, signal_strength, confidence, expected_alpha_5d,
           expected_alpha_20d, sqs_score, sqs_grade, has_convergence,
           convergence_bonus, politician_grade, filing_lag_days, created_at
    FROM alpha_signals
    ORDER BY signal_strength DESC
    LIMIT 10
''')
rows = c.fetchall()
if rows:
    for i, r in enumerate(rows, 1):
        conv = ' [CONVERGENCE]' if r['has_convergence'] else ''
        a5 = f'{r[\"expected_alpha_5d\"]:.4f}' if r['expected_alpha_5d'] else 'N/A'
        a20 = f'{r[\"expected_alpha_20d\"]:.4f}' if r['expected_alpha_20d'] else 'N/A'
        cb = f'+{r[\"convergence_bonus\"]:.2f}' if r['convergence_bonus'] else '+0.00'
        grade = r['politician_grade'] or 'N/A'
        sqs_g = r['sqs_grade'] or 'N/A'
        lag = r['filing_lag_days'] if r['filing_lag_days'] is not None else '?'
        print(f'  #{i} {r[\"ticker\"]:6s} ({r[\"asset_name\"] or \"N/A\"})')
        print(f'     Direction: {r[\"direction\"]} | Type: {r[\"transaction_type\"]} | Chamber: {r[\"chamber\"]}')
        print(f'     Politician: {r[\"politician_name\"]} (Grade: {grade})')
        print(f'     Strength: {r[\"signal_strength\"]:.4f} | Confidence: {r[\"confidence\"]:.4f}')
        print(f'     Alpha 5d: {a5} | Alpha 20d: {a20}')
        print(f'     SQS: {r[\"sqs_score\"]:.1f} ({sqs_g}) | Conv Bonus: {cb}{conv}')
        print(f'     Filing Lag: {lag}d | Date: {r[\"created_at\"]}')
        print()
else:
    print('  [WARN] alpha_signals 表無資料')

# --- Enhanced Signals Top 10 ---
print('\n## Enhanced Signals Top 10 (by enhanced_strength)\n')
c.execute('SELECT COUNT(*) FROM enhanced_signals')
es_count = c.fetchone()[0]
if es_count > 0:
    c.execute('''
        SELECT ticker, politician_name, chamber, direction,
               original_strength, enhanced_strength, confidence_v2,
               pacs_score, vix_zone, vix_multiplier,
               social_alignment, social_bonus,
               has_convergence, politician_grade, sqs_score
        FROM enhanced_signals
        ORDER BY enhanced_strength DESC
        LIMIT 10
    ''')
    rows = c.fetchall()
    for i, r in enumerate(rows, 1):
        conv = ' [CONV]' if r['has_convergence'] else ''
        social = f' | Social: {r[\"social_alignment\"]}({r[\"social_bonus\"]:+.2f})' if r['social_alignment'] else ''
        grade = r['politician_grade'] or 'N/A'
        print(f'  #{i} {r[\"ticker\"]:6s} | {r[\"politician_name\"]} ({r[\"chamber\"]}) | {r[\"direction\"]}')
        print(f'     Original: {r[\"original_strength\"]:.4f} -> Enhanced: {r[\"enhanced_strength\"]:.4f} (delta: {r[\"enhanced_strength\"]-r[\"original_strength\"]:+.4f})')
        print(f'     PACS: {r[\"pacs_score\"]:.4f} | VIX: {r[\"vix_zone\"]} ({r[\"vix_multiplier\"]}x) | Conf v2: {r[\"confidence_v2\"]:.4f}')
        print(f'     Grade: {grade} | SQS: {r[\"sqs_score\"]:.1f}{conv}{social}')
        print()
else:
    print('  [INFO] enhanced_signals 表尚無資料，請執行: python -m src.signal_enhancer')

# --- 原始 vs 增強比較 ---
if es_count > 0:
    print('\n## 原始 vs 增強信號差異分析\n')
    c.execute('''
        SELECT
            AVG(original_strength) as avg_orig,
            AVG(enhanced_strength) as avg_enh,
            AVG(confidence_v2) as avg_conf2,
            AVG(pacs_score) as avg_pacs,
            AVG(vix_multiplier) as avg_vix_mult,
            COUNT(*) as total
        FROM enhanced_signals
    ''')
    r = c.fetchone()
    print(f'  總增強信號: {r[\"total\"]}')
    print(f'  平均原始強度:   {r[\"avg_orig\"]:.4f}')
    print(f'  平均增強強度:   {r[\"avg_enh\"]:.4f} (delta: {r[\"avg_enh\"]-r[\"avg_orig\"]:+.4f})')
    print(f'  平均 PACS:      {r[\"avg_pacs\"]:.4f}')
    print(f'  平均 VIX Mult:  {r[\"avg_vix_mult\"]:.4f}')
    print(f'  平均 Conf v2:   {r[\"avg_conf2\"]:.4f}')

    # VIX zone 分布
    print('\n  VIX Zone 分布:')
    c.execute('SELECT vix_zone, COUNT(*) as cnt FROM enhanced_signals GROUP BY vix_zone ORDER BY cnt DESC')
    for r in c.fetchall():
        print(f'    {r[\"vix_zone\"]:15s}: {r[\"cnt\"]} signals')

    # Ranking 差異 (大幅上升/下降的 ticker)
    print('\n  排名大幅變動 (enhanced vs original):')
    c.execute('''
        SELECT ticker, politician_name, original_strength, enhanced_strength,
               (enhanced_strength - original_strength) as delta
        FROM enhanced_signals
        ORDER BY delta DESC
        LIMIT 5
    ''')
    print('    [最大上升]')
    for r in c.fetchall():
        print(f'      {r[\"ticker\"]:6s} ({r[\"politician_name\"]}) | {r[\"original_strength\"]:.4f} -> {r[\"enhanced_strength\"]:.4f} ({r[\"delta\"]:+.4f})')

    c.execute('''
        SELECT ticker, politician_name, original_strength, enhanced_strength,
               (enhanced_strength - original_strength) as delta
        FROM enhanced_signals
        ORDER BY delta ASC
        LIMIT 5
    ''')
    print('    [最大下降]')
    for r in c.fetchall():
        print(f'      {r[\"ticker\"]:6s} ({r[\"politician_name\"]}) | {r[\"original_strength\"]:.4f} -> {r[\"enhanced_strength\"]:.4f} ({r[\"delta\"]:+.4f})')

# --- Direction 分布 ---
print('\n## Direction 分布\n')
c.execute('''
    SELECT direction, COUNT(*) as cnt,
           AVG(signal_strength) as avg_str,
           AVG(confidence) as avg_conf,
           AVG(expected_alpha_20d) as avg_a20
    FROM alpha_signals
    GROUP BY direction
''')
for r in c.fetchall():
    a20 = f'{r[\"avg_a20\"]:.4f}' if r['avg_a20'] else 'N/A'
    print(f'  {r[\"direction\"]:8s} | Count: {r[\"cnt\"]:4d} | Avg Str: {r[\"avg_str\"]:.4f} | Avg Conf: {r[\"avg_conf\"]:.4f} | Avg Alpha 20d: {a20}')

# --- Convergence 信號 ---
print('\n## Convergence 加成信號\n')
c.execute('''
    SELECT ticker, asset_name, direction, COUNT(*) as cnt,
           GROUP_CONCAT(politician_name, ', ') as politicians,
           AVG(signal_strength) as avg_str
    FROM alpha_signals
    WHERE has_convergence = 1
    GROUP BY ticker, direction
    ORDER BY cnt DESC
    LIMIT 10
''')
rows = c.fetchall()
if rows:
    for r in rows:
        print(f'  {r[\"ticker\"]:6s} ({r[\"asset_name\"] or \"N/A\"}) | {r[\"direction\"]} | {r[\"cnt\"]} convergent signals')
        print(f'    Politicians: {r[\"politicians\"]}')
        print(f'    Avg Strength: {r[\"avg_str\"]:.4f}')
        print()
else:
    print('  [INFO] 無 convergence 信號')

# --- Portfolio Positions (目前持倉) ---
print('\n## 目前投組持倉 (portfolio_positions)\n')
c.execute('SELECT COUNT(*) FROM portfolio_positions')
pp_count = c.fetchone()[0]
if pp_count > 0:
    c.execute('''
        SELECT ticker, sector, weight, conviction_score, expected_alpha,
               sharpe_estimate
        FROM portfolio_positions
        ORDER BY weight DESC
        LIMIT 15
    ''')
    print(f'  {\"Ticker\":8s} | {\"Sector\":20s} | {\"Weight\":>7s} | {\"Conviction\":>10s} | {\"Exp Alpha\":>10s} | {\"Sharpe\":>7s}')
    print('  ' + '-' * 75)
    for r in c.fetchall():
        ea = f'{r[\"expected_alpha\"]:.4f}' if r['expected_alpha'] else 'N/A'
        sh = f'{r[\"sharpe_estimate\"]:.2f}' if r['sharpe_estimate'] else 'N/A'
        print(f'  {r[\"ticker\"]:8s} | {(r[\"sector\"] or \"N/A\"):20s} | {r[\"weight\"]:6.2f}% | {r[\"conviction_score\"]:10.1f} | {ea:>10s} | {sh:>7s}')
else:
    print('  [INFO] portfolio_positions 表尚無資料，請執行: python -m src.portfolio_optimizer')

print('\n' + '=' * 80)
print('  報告結束')
print('=' * 80)
conn.close()
"
```

## Filtered Queries

根據使用者需求調整:

- **特定議員**: 加 `WHERE politician_name LIKE '%Pelosi%'`
- **特定 Ticker**: 加 `WHERE ticker = 'NVDA'`
- **只看 LONG**: 加 `WHERE direction = 'LONG'`
- **高強度**: 加 `WHERE signal_strength >= 0.7`
- **有收斂**: 加 `WHERE has_convergence = 1`
- **近期信號**: 加 `WHERE created_at >= date('now', '-7 days')`
- **特定院別**: 加 `WHERE chamber = 'Senate'`

## Output Format

以繁體中文呈現，包含:
- Top Picks 排名 (原始 + 增強)
- Direction 分布分析
- Convergence 信號標註
- 投組持倉對照
- 投資建議摘要
