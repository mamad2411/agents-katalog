---
name: system-status
description: >
  PAM 系統整體狀態總覽 — 一鍵查看 DB 狀態、最新 pipeline 執行結果、信號數量、
  VIX 體制、投組狀態、待處理告警。每日早晨開盤前檢查用。
  觸發詞: 系統狀態, system status, 早安, morning check, 開盤前, 今日狀態,
  dashboard, 系統總覽, PAM status, 狀態報告
---

# System Status - PAM Morning Check

一鍵查看 PAM 系統全貌，適合每日開盤前使用。

## Step 1: 系統總覽

```bash
cd "D:/VScode_project/NLP data for trading" && python -c "
import sqlite3, json, os
from datetime import datetime, date

conn = sqlite3.connect('data/data.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

today = date.today().isoformat()
print('=' * 70)
print(f'  PAM System Status - {today}')
print('=' * 70)

# --- 1. Pipeline 最後執行 ---
print('\n[1] Pipeline Status')
c.execute('SELECT MAX(created_at) FROM congress_trades')
last_etl = c.fetchone()[0] or 'Never'
c.execute('SELECT MAX(created_at) FROM alpha_signals')
last_signal = c.fetchone()[0] or 'Never'
c.execute('SELECT MAX(updated_at) FROM enhanced_signals')
last_enhance = c.fetchone()[0] or 'Never'
print(f'  Last ETL:        {last_etl}')
print(f'  Last Signals:    {last_signal}')
print(f'  Last Enhanced:   {last_enhance}')

# --- 2. DB Table Counts ---
print('\n[2] Database Summary')
tables = {
    'congress_trades': 'Trades', 'alpha_signals': 'Alpha Signals',
    'enhanced_signals': 'Enhanced', 'convergence_signals': 'Convergence',
    'portfolio_positions': 'Portfolio', 'sector_rotation_signals': 'Sector Rotation',
    'rebalance_history': 'Rebalance Actions', 'sec_form4_trades': 'SEC Form 4',
    'social_posts': 'Social Posts', 'politician_rankings': 'Rankings',
}
for t, label in tables.items():
    try:
        c.execute(f'SELECT COUNT(*) FROM [{t}]')
        cnt = c.fetchone()[0]
        print(f'  {label:22s}: {cnt:>6d}')
    except:
        print(f'  {label:22s}: [N/A]')

# --- 3. Latest Trades ---
print('\n[3] Latest Trades (last 5)')
c.execute('''
    SELECT politician_name, ticker, transaction_type, amount_range,
           transaction_date, filing_date
    FROM congress_trades
    ORDER BY filing_date DESC, created_at DESC
    LIMIT 5
''')
for r in c.fetchall():
    ticker = r['ticker'] or '(no ticker)'
    print(f'  {r[\"filing_date\"]} | {r[\"politician_name\"]:20s} | {ticker:6s} | {r[\"transaction_type\"]:10s} | {r[\"amount_range\"]}')

# --- 4. Top Alpha Signals ---
print('\n[4] Top 5 Alpha Signals (by strength)')
c.execute('''
    SELECT ticker, politician_name, direction, signal_strength,
           expected_alpha_20d, has_convergence
    FROM alpha_signals
    ORDER BY signal_strength DESC
    LIMIT 5
''')
for r in c.fetchall():
    conv = ' *CONV*' if r['has_convergence'] else ''
    a20 = f'{r[\"expected_alpha_20d\"]:.3f}' if r['expected_alpha_20d'] else 'N/A'
    print(f'  {r[\"ticker\"]:6s} | {r[\"politician_name\"]:20s} | {r[\"direction\"]:5s} | Str={r[\"signal_strength\"]:.3f} | A20d={a20}{conv}')

# --- 5. Portfolio Overview ---
print('\n[5] Portfolio (top 10 by weight)')
c.execute('''
    SELECT ticker, sector, weight, conviction_score, expected_alpha
    FROM portfolio_positions
    ORDER BY weight DESC
    LIMIT 10
''')
total_weight = 0
for r in c.fetchall():
    ea = f'{r[\"expected_alpha\"]:.3f}' if r['expected_alpha'] else 'N/A'
    print(f'  {r[\"ticker\"]:6s} | {(r[\"sector\"] or \"?\"):18s} | W={r[\"weight\"]:5.2f}% | Conv={r[\"conviction_score\"]:5.1f} | Alpha={ea}')
    total_weight += r['weight']
print(f'  Total weight (top 10): {total_weight:.1f}%')

# --- 6. Convergence Alerts ---
print('\n[6] Active Convergence Signals')
c.execute('SELECT ticker, direction, politician_count, score, politicians FROM convergence_signals ORDER BY score DESC')
rows = c.fetchall()
if rows:
    for r in rows:
        print(f'  {r[\"ticker\"]:6s} | {r[\"direction\"]:5s} | {r[\"politician_count\"]} politicians | Score={r[\"score\"]:.2f}')
        print(f'    -> {r[\"politicians\"]}')
else:
    print('  No active convergence signals')

# --- 7. Sector Rotation ---
print('\n[7] Sector Rotation Signals')
try:
    c.execute('SELECT sector, etf, direction, signal_strength, rotation_type FROM sector_rotation_signals ORDER BY signal_strength DESC')
    for r in c.fetchall():
        print(f'  {r[\"sector\"]:18s} ({r[\"etf\"]}) | {r[\"direction\"]} | Str={r[\"signal_strength\"]:.3f} | {r[\"rotation_type\"]}')
except:
    print('  [N/A]')

# --- 8. Recent Rebalance Actions ---
print('\n[8] Latest Rebalance Actions')
try:
    c.execute('SELECT ticker, action, new_score, score_delta, reason FROM rebalance_history ORDER BY created_at DESC LIMIT 5')
    for r in c.fetchall():
        delta = f'{r[\"score_delta\"]:+.1f}' if r['score_delta'] else 'N/A'
        print(f'  {r[\"action\"]:10s} {r[\"ticker\"]:6s} | Score={r[\"new_score\"]:.1f} (delta={delta}) | {(r[\"reason\"] or \"\")[:60]}')
except:
    print('  [N/A]')

print('\n' + '=' * 70)
print('  Status: OPERATIONAL')
print('=' * 70)
conn.close()
"
```

## Step 2: VIX Regime Check (Optional)

If user wants current VIX:

```bash
cd "D:/VScode_project/NLP data for trading" && python -c "
try:
    import yfinance as yf
    vix = yf.Ticker('^VIX')
    hist = vix.history(period='5d')
    if not hist.empty:
        current = hist['Close'].iloc[-1]
        prev = hist['Close'].iloc[-2] if len(hist) > 1 else current
        change = current - prev
        if current < 14: zone = 'ULTRA LOW (cautious)'
        elif current <= 16: zone = 'GOLDILOCKS (optimal)'
        elif current <= 20: zone = 'MODERATE'
        elif current <= 30: zone = 'HIGH (reduce exposure)'
        else: zone = 'EXTREME (risk-off)'
        print(f'VIX: {current:.2f} ({change:+.2f}) | Zone: {zone}')
    else:
        print('VIX: Unable to fetch')
except Exception as e:
    print(f'VIX: Error - {e}')
"
```

## Output Format

Present as a concise morning briefing in Traditional Chinese, highlighting:
- Any signals that need immediate attention
- Portfolio changes since last check
- VIX regime and market conditions
- Recommended actions for the day
