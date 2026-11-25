---
name: rsun-status
description: 掃描容晟科技全部專案狀態。當用戶說「檢查所有專案」「查一下各專案」「project status」「各站狀態」「早安」「morning」時使用。輸出 git 狀態、未推 commit、NEXT_SESSION 待辦，以及客戶 PM 進度。
user-invocable: true
allowed-tools: "Bash(git *) Bash(cat *) Bash(ls *) Bash(python3 *) Read Grep"
---

# 容晟科技全專案狀態掃描

掃描分兩個區塊：**A. 技術 Repo 狀態** + **B. 客戶 PM 進度**

---

## A. 技術 Repo 掃描

掃描以下 7 個核心 repo，輸出結構化狀態報表。

| Repo | 路徑 | 部署 |
|------|------|------|
| TRACKER | ~/Projects/TRACKER | Cloudflare Pages → rsun-tracker.pages.dev |
| rsun-worker | ~/Projects/rsun-worker | Cloudflare Workers（wrangler deploy）|
| rsun-dashboard | ~/Projects/rsun-dashboard | Vercel → app.rsun.me |
| ceyan-web | ~/Projects/ceyan-web | Vercel → ceyan.ronsunai.tw |
| askai | ~/Projects/askai | Vercel → askai.vercel.app |
| aiclass | ~/Projects/aiclass | Vercel → aiclass.vercel.app |
| ronsunai-web | ~/Projects/ronsunai-web | Vercel → ronsunai.tw |
| horizen | ~/Projects/horizen | Fly.io（ESG 法規情報平台·先見明）|

### 執行步驟（每個 repo）

1. `git -C ~/Projects/<repo> log --oneline -3` — 最近 3 筆 commit
2. `git -C ~/Projects/<repo> status --short` — 未 commit 的變更（只顯示前 8 行）
3. `git -C ~/Projects/<repo> cherry -v origin/main 2>/dev/null | head -5` — 已 commit 但未 push
4. 讀取 `~/Projects/<repo>/docs/NEXT_SESSION.md` 最後 30 行，提取 `[ ]` 待辦項目

### 輸出格式（每個 repo）

```
### rsun-worker  ⚡ Cloudflare Workers
最新 commit：<message>（<date>）
未 commit：<N 個檔案 / 無>
未 push：<N 筆 / 無>
待辦：
  - [ ] <NEXT_SESSION 最高優先待辦，最多 3 條>
```

### A 區塊總結表格

```
| 專案 | 未 commit | 未 push | 阻礙 |
```

---

## B. 客戶 PM 進度掃描

掃描 `~/Projects/TRACKER/clients/*/project-state.json`，輸出每個客戶的 PM 狀態。

### 執行步驟

用以下 Python 命令一次讀取並格式化所有客戶狀態：

```bash
python3 -c "
import json, os, glob
from datetime import date, datetime

today = date.today()
files = sorted(glob.glob(os.path.expanduser('~/Projects/TRACKER/clients/*/project-state.json')))

PHASE_EMOJI = {0:'🔍', 1:'📋', 2:'🤝', 3:'🎨', 4:'⚙️', 5:'🚀', 6:'🔧', -1:'⏸️', -2:'✅'}
HEALTH_EMOJI = {'on-track':'🟢', 'waiting':'🟡', 'at-risk':'🔴', 'blocked':'⛔'}
MILESTONE_LABELS = {
  'lean_canvas':'LC', 'prd':'PRD', 'estimate':'估', 'proposal_sent':'提案',
  'contract_signed':'合約', 'kickoff':'開工', 'adr_001':'ADR',
  'first_sprint_done':'Sprint1', 'staging_deployed':'Staging',
  'client_uat':'UAT', 'delivered':'交付'
}

alerts = []
for f in files:
    try:
        s = json.load(open(f))
        ph = s.get('phase', 0)
        pe = PHASE_EMOJI.get(ph, '❓')
        he = HEALTH_EMOJI.get(s.get('health','on-track'), '🟡')
        
        # 里程碑進度
        ms = s.get('milestones', {})
        done = [MILESTONE_LABELS[k] for k,v in ms.items() if v and k in MILESTONE_LABELS]
        todo = [MILESTONE_LABELS[k] for k,v in ms.items() if not v and k in MILESTONE_LABELS]
        ms_str = '✅' + ' '.join(done) if done else ''
        ms_todo = '⬜' + ' '.join(todo[:3]) if todo else ''
        
        # Sprint 進度
        st = s.get('stories_total', 0)
        sd = s.get('stories_done', 0)
        sp = s.get('sprint', 0)
        sprint_str = f'Sprint {sp}: {sd}/{st} stories' if st > 0 else f'Sprint {sp}'
        
        # 客戶更新預警
        nu = s.get('next_client_update', '')
        update_str = ''
        if nu:
            nd = datetime.strptime(nu, '%Y-%m-%d').date()
            diff = (nd - today).days
            if diff < 0:
                update_str = f'⚠️ 客戶更新已逾期 {-diff} 天！'
                alerts.append(f\"{s['name']}: 客戶更新逾期 {-diff} 天\")
            elif diff <= 2:
                update_str = f'🔔 客戶更新 {diff} 天後（{nu}）'
            else:
                update_str = f'📅 下次更新：{nu}（{diff} 天後）'
        
        print(f\"\"\"
{'='*50}
{he} {s['name']} [{s.get('client_contact','')}]
  階段：{pe} Phase {ph} — {s.get('phase_label','')}
  {sprint_str}
  {ms_str}  {ms_todo}
  {update_str}
  備注：{s.get('health_note', '')}
  更新：{s.get('updated_at', 'unknown')}\"\"\")
    except Exception as e:
        print(f'  ❌ {f}: {e}')

if alerts:
    print()
    print('🚨 需要立即處理：')
    for a in alerts:
        print(f'  → {a}')
"
```

### B 區塊輸出格式

```
==================================================
🟡 Apex Gold 澳洲房產官網 [Jamie]
  階段：🤝 Phase 2 — 提案 & 合約
  Sprint 0
  ✅ PRD 估 提案  ⬜ 合約 開工 ADR
  📅 下次更新：2026-04-28（5 天後）
  備注：等候 Jamie 決定方案，v4 提案已送出
  更新：2026-04-23
```

---

## 完整輸出結構

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 技術 Repo 狀態
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[各 repo 區塊]

| 專案 | 未 commit | 未 push | 阻礙 |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 客戶 PM 進度
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[各客戶 PM 狀態區塊]

🚨 需要立即處理：（如有逾期或告警）
```

---

## 注意事項

- TRACKER 和 rsun-worker 未部署（wrangler/CF Pages）和未 push（git）是兩件事，都要標出
- TRACKER 部署指令：`cd ~/Projects/TRACKER && npx wrangler pages deploy . --project-name rsun-tracker --commit-dirty=true`
- 如果 NEXT_SESSION.md 不存在，標「無 NEXT_SESSION」
- 阻礙欄：如果 NEXT_SESSION 裡有「等 SLP」「等統編」「等金鑰」等關鍵字，標出來
- `project-state.json` 不存在的客戶資料夾，標「無 PM 狀態」
- **客戶更新逾期** → 列入「需要立即處理」，優先於技術待辦
- 不要自動 commit 或 push，只報告
