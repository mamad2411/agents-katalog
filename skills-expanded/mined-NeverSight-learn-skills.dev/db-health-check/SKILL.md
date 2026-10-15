---
name: db-health-check
description: >
  深度資料庫健康檢查，驗證資料品質、新鮮度、一致性。當使用者想檢查系統狀態、
  資料是否正常、有無異常時使用。觸發詞: 資料健康, db health, 資料品質,
  data quality, health check, 資料檢查, 資料庫狀態, 系統狀態, 資料診斷
---

# DB Health Check

對 `data/data.db` 執行全面健康檢查，涵蓋 row counts、新鮮度、NULL rate、orphan records、重複偵測、表間一致性。

## 執行完整健康檢查

```bash
cd "D:/VScode_project/NLP data for trading" && python -c "
import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('data/data.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

score = 100
issues = []
today = datetime.now().strftime('%Y-%m-%d')

print('=' * 80)
print('  PAM 資料庫健康檢查報告')
print(f'  檢查時間: {datetime.now().strftime(\"%Y-%m-%d %H:%M:%S\")}')
print('=' * 80)

# ============================================================
# 1. 所有表 Row Count + 最新時間戳
# ============================================================
print('\n## 1. 表格統計 (Row Count + 最新紀錄)\n')

tables_ts = {
    'congress_trades': 'created_at',
    'extraction_log': 'created_at',
    'sec_form4_trades': 'created_at',
    'signal_quality_scores': 'scored_at',
    'convergence_signals': 'detected_at',
    'politician_rankings': 'updated_at',
    'alpha_signals': 'created_at',
    'enhanced_signals': 'updated_at',
    'sector_rotation_signals': 'created_at',
    'portfolio_positions': 'created_at',
    'rebalance_history': 'created_at',
    'signal_performance': 'evaluated_at',
    'fama_french_results': 'created_at',
    'social_posts': 'created_at',
    'social_signals': 'created_at',
    'ai_intelligence_signals': 'timestamp',
    'senate_trades': 'created_at',
    'house_trades': 'created_at',
    'risk_assessments': 'assessed_at',
}

print(f'  {\"Table\":30s} | {\"Rows\":>8s} | {\"Latest\":20s} | Status')
print('  ' + '-' * 80)

for table, ts_col in tables_ts.items():
    try:
        c.execute(f'SELECT COUNT(*) FROM [{table}]')
        count = c.fetchone()[0]
        try:
            c.execute(f'SELECT MAX([{ts_col}]) FROM [{table}]')
            latest = c.fetchone()[0] or 'N/A'
        except:
            latest = 'N/A'
        status = '[OK]'
        if count == 0:
            status = '[EMPTY]'
            issues.append(f'{table}: 表為空')
            score -= 2
        print(f'  {table:30s} | {count:8d} | {str(latest):20s} | {status}')
    except Exception as e:
        print(f'  {table:30s} | {\"MISSING\":>8s} | {\"N/A\":20s} | [MISSING]')
        issues.append(f'{table}: 表不存在')
        score -= 3

# ============================================================
# 2. 資料新鮮度 (congress_trades)
# ============================================================
print('\n## 2. 資料新鮮度\n')
try:
    c.execute('SELECT MAX(transaction_date) as max_td, MAX(filing_date) as max_fd, MAX(created_at) as max_ca FROM congress_trades')
    r = c.fetchone()
    max_td = r['max_td'] or 'N/A'
    max_fd = r['max_fd'] or 'N/A'
    max_ca = r['max_ca'] or 'N/A'
    print(f'  最新 transaction_date: {max_td}')
    print(f'  最新 filing_date:      {max_fd}')
    print(f'  最新 created_at:       {max_ca}')

    if max_td != 'N/A':
        try:
            td_date = datetime.strptime(max_td[:10], '%Y-%m-%d')
            days_old = (datetime.now() - td_date).days
            print(f'  資料延遲天數: {days_old} 天')
            if days_old > 14:
                issues.append(f'congress_trades 資料已 {days_old} 天未更新')
                score -= 10
                print('  [WARN] 資料超過 14 天未更新!')
            elif days_old > 7:
                issues.append(f'congress_trades 資料已 {days_old} 天未更新')
                score -= 5
                print('  [WARN] 資料超過 7 天未更新')
            else:
                print('  [OK] 資料新鮮度正常')
        except ValueError:
            print(f'  [WARN] 無法解析日期格式: {max_td}')
except Exception as e:
    print(f'  [ERROR] 查詢失敗: {e}')
    score -= 10

# ============================================================
# 3. 重要欄位 NULL Rate
# ============================================================
print('\n## 3. 重要欄位 NULL Rate\n')

null_checks = [
    ('congress_trades', ['politician_name', 'ticker', 'transaction_type', 'transaction_date', 'data_hash']),
    ('alpha_signals', ['ticker', 'politician_name', 'direction', 'signal_strength', 'confidence']),
    ('signal_quality_scores', ['politician_name', 'ticker', 'sqs', 'grade']),
    ('enhanced_signals', ['ticker', 'politician_name', 'enhanced_strength', 'pacs_score']),
]

for table, columns in null_checks:
    try:
        c.execute(f'SELECT COUNT(*) FROM [{table}]')
        total = c.fetchone()[0]
        if total == 0:
            continue
        print(f'  [{table}] (total: {total})')
        for col in columns:
            try:
                c.execute(f'SELECT COUNT(*) FROM [{table}] WHERE [{col}] IS NULL')
                null_count = c.fetchone()[0]
                rate = null_count / total * 100
                status = '[OK]' if rate < 5 else '[WARN]' if rate < 20 else '[FAIL]'
                if rate >= 5:
                    issues.append(f'{table}.{col} NULL rate: {rate:.1f}%')
                    score -= min(5, int(rate / 10))
                print(f'    {col:25s}: {null_count:5d} NULL ({rate:5.1f}%) {status}')
            except:
                print(f'    {col:25s}: [COLUMN MISSING]')
        print()
    except:
        pass

# ============================================================
# 4. Orphan Records 檢查
# ============================================================
print('\n## 4. Orphan Records (孤立紀錄)\n')

# alpha_signals.trade_id -> congress_trades.id
try:
    c.execute('''
        SELECT COUNT(*) FROM alpha_signals
        WHERE trade_id IS NOT NULL
        AND trade_id NOT IN (SELECT id FROM congress_trades)
    ''')
    orphan_alpha = c.fetchone()[0]
    status = '[OK]' if orphan_alpha == 0 else '[WARN]'
    if orphan_alpha > 0:
        issues.append(f'alpha_signals 有 {orphan_alpha} 筆 orphan records (trade_id 無對應)')
        score -= 5
    print(f'  alpha_signals -> congress_trades: {orphan_alpha} orphans {status}')
except Exception as e:
    print(f'  alpha_signals -> congress_trades: [ERROR] {e}')

# signal_quality_scores.trade_id -> congress_trades.id
try:
    c.execute('''
        SELECT COUNT(*) FROM signal_quality_scores
        WHERE trade_id IS NOT NULL
        AND trade_id NOT IN (SELECT id FROM congress_trades)
    ''')
    orphan_sqs = c.fetchone()[0]
    status = '[OK]' if orphan_sqs == 0 else '[WARN]'
    if orphan_sqs > 0:
        issues.append(f'signal_quality_scores 有 {orphan_sqs} 筆 orphan records')
        score -= 5
    print(f'  signal_quality_scores -> congress_trades: {orphan_sqs} orphans {status}')
except Exception as e:
    print(f'  signal_quality_scores -> congress_trades: [ERROR] {e}')

# signal_performance.signal_id -> alpha_signals.id
try:
    c.execute('''
        SELECT COUNT(*) FROM signal_performance
        WHERE signal_id IS NOT NULL
        AND signal_id NOT IN (SELECT id FROM alpha_signals)
    ''')
    orphan_sp = c.fetchone()[0]
    status = '[OK]' if orphan_sp == 0 else '[WARN]'
    if orphan_sp > 0:
        issues.append(f'signal_performance 有 {orphan_sp} 筆 orphan records')
        score -= 3
    print(f'  signal_performance -> alpha_signals: {orphan_sp} orphans {status}')
except Exception as e:
    print(f'  signal_performance -> alpha_signals: [ERROR] {e}')

# ============================================================
# 5. 重複偵測 (data_hash)
# ============================================================
print('\n## 5. 重複偵測 (data_hash uniqueness)\n')

for table in ['congress_trades', 'sec_form4_trades', 'social_posts']:
    try:
        c.execute(f'SELECT COUNT(*) FROM [{table}]')
        total = c.fetchone()[0]
        if total == 0:
            print(f'  {table}: [EMPTY]')
            continue
        c.execute(f'SELECT data_hash, COUNT(*) as cnt FROM [{table}] GROUP BY data_hash HAVING cnt > 1')
        dupes = c.fetchall()
        dupe_count = len(dupes)
        dupe_rows = sum(r['cnt'] - 1 for r in dupes) if dupes else 0
        status = '[OK]' if dupe_count == 0 else '[WARN]'
        if dupe_count > 0:
            issues.append(f'{table} 有 {dupe_count} 組重複 hash ({dupe_rows} 多餘筆)')
            score -= 5
        print(f'  {table:25s}: {dupe_count} duplicate groups ({dupe_rows} extra rows) {status}')
    except Exception as e:
        print(f'  {table:25s}: [ERROR] {e}')

# ============================================================
# 6. 表間一致性
# ============================================================
print('\n## 6. 表間一致性\n')

try:
    c.execute('SELECT COUNT(*) FROM congress_trades')
    ct_count = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM signal_quality_scores')
    sqs_count = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM alpha_signals')
    as_count = c.fetchone()[0]

    coverage_sqs = (sqs_count / ct_count * 100) if ct_count > 0 else 0
    coverage_alpha = (as_count / ct_count * 100) if ct_count > 0 else 0

    print(f'  congress_trades:       {ct_count:6d} rows')
    print(f'  signal_quality_scores: {sqs_count:6d} rows (coverage: {coverage_sqs:.1f}%)')
    print(f'  alpha_signals:         {as_count:6d} rows (coverage: {coverage_alpha:.1f}%)')

    if coverage_sqs < 80 and ct_count > 0:
        issues.append(f'SQS coverage only {coverage_sqs:.1f}% of trades')
        score -= 3

    # Enhanced vs Alpha
    c.execute('SELECT COUNT(*) FROM enhanced_signals')
    es_count = c.fetchone()[0]
    if as_count > 0:
        enh_coverage = es_count / as_count * 100
        print(f'  enhanced_signals:      {es_count:6d} rows (coverage: {enh_coverage:.1f}% of alpha)')
    else:
        print(f'  enhanced_signals:      {es_count:6d} rows')

    # Portfolio vs Alpha
    c.execute('SELECT COUNT(DISTINCT ticker) FROM alpha_signals')
    alpha_tickers = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM portfolio_positions')
    port_count = c.fetchone()[0]
    print(f'  portfolio_positions:   {port_count:6d} rows (from {alpha_tickers} unique alpha tickers)')
except Exception as e:
    print(f'  [ERROR] 一致性檢查失敗: {e}')

# ============================================================
# 7. 日期合理性
# ============================================================
print('\n## 7. 日期合理性\n')

try:
    c.execute(\"SELECT COUNT(*) FROM congress_trades WHERE transaction_date > date('now', '+1 day')\")
    future = c.fetchone()[0]
    c.execute(\"SELECT COUNT(*) FROM congress_trades WHERE transaction_date < '2020-01-01'\")
    old = c.fetchone()[0]
    status_f = '[OK]' if future == 0 else '[WARN]'
    status_o = '[OK]' if old == 0 else '[WARN]'
    if future > 0:
        issues.append(f'congress_trades 有 {future} 筆未來日期')
        score -= 5
    if old > 0:
        issues.append(f'congress_trades 有 {old} 筆 2020 年以前的日期')
        score -= 2
    print(f'  未來日期 (transaction_date > today): {future} {status_f}')
    print(f'  過舊日期 (transaction_date < 2020):  {old} {status_o}')
except Exception as e:
    print(f'  [ERROR] {e}')

# ============================================================
# 8. Chamber 分布
# ============================================================
print('\n## 8. Chamber 分布\n')
try:
    c.execute('SELECT chamber, COUNT(*) as cnt FROM congress_trades GROUP BY chamber')
    for r in c.fetchall():
        print(f'  {(r[\"chamber\"] or \"NULL\"):10s}: {r[\"cnt\"]} trades')
except:
    pass

# ============================================================
# SUMMARY
# ============================================================
score = max(0, score)
if score >= 90:
    grade = 'A (Excellent)'
elif score >= 75:
    grade = 'B (Good)'
elif score >= 60:
    grade = 'C (Fair)'
elif score >= 40:
    grade = 'D (Poor)'
else:
    grade = 'F (Critical)'

print('\n' + '=' * 80)
print(f'  健康評分: {score}/100 ({grade})')
print('=' * 80)

if issues:
    print('\n  問題清單:')
    for i, issue in enumerate(issues, 1):
        print(f'    {i}. {issue}')
else:
    print('\n  [OK] 未發現問題!')

print()
conn.close()
"
```

## 特定檢查

根據使用者需求執行特定檢查:

- **只看 row counts**: 簡化為 Step 1 查詢
- **特定表**: 修改查詢只看指定表
- **修復建議**: 針對發現的問題提供 SQL 修復指令
- **歷史趨勢**: 比較 `extraction_log` 中的歷次 ETL 執行結果

## 常見修復指令

```sql
-- 刪除重複 hash
DELETE FROM congress_trades WHERE rowid NOT IN (
    SELECT MIN(rowid) FROM congress_trades GROUP BY data_hash
);

-- 清除孤立的 alpha_signals
DELETE FROM alpha_signals WHERE trade_id NOT IN (
    SELECT id FROM congress_trades
);

-- 重新執行 SQS 評分
-- python -m src.signal_scorer

-- 重新執行 Alpha 信號
-- python -m src.alpha_signal_generator
```

## Output Format

以繁體中文輸出，包含:
- 8 項檢查結果 (附 [OK]/[WARN]/[FAIL] 標記)
- 健康評分 (0-100) 和等級 (A-F)
- 問題清單 + 修復建議
