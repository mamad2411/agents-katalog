---
name: rsun-kickoff
description: 合約簽訂後、開發正式啟動前的 Project Kickoff SOP。涵蓋第一週環境設定、ADR-001 建立、角色分工、客戶溝通節奏、第一個 Sprint 目標設定。當用戶說「要開始這個案子了」「客戶簽了」「kickoff 要怎麼做」時使用。
user-invocable: true
allowed-tools: "Read Write Bash(ls * mkdir *)"
---

# rsun-kickoff — 專案啟動 SOP

合約簽完後的第一週，是整個專案氛圍的基調。開好頭，後面才順。

**啟動條件確認：**
- [ ] 合約已簽訂
- [ ] 簽約款已收（30%）
- [ ] PRD 已確認（功能範圍對齊）
- [ ] 估價 WBS 已完成

---

## Day 1-2：行政與環境設定

### 建立專案資料夾結構

```bash
# Drive 資料夾
My Drive/容晟科技/客戶專案/[客戶名]-[專案名]/
├── 00_PRD_[名稱].gdoc          ← 已有
├── 01_估價單_[名稱].gsheet      ← 已有
├── 02_ADR/                      ← 新建
├── 03_設計稿/                   ← 新建（Figma 連結）
├── 04_週報/                     ← 新建
├── 05_驗收紀錄/                 ← 新建
└── 09_合約.pdf                  ← 存入
```

### Git Repository 初始化

```bash
# 建立 repo（GitHub / GitLab）
git init [專案名]
git commit -m "chore: project kickoff — [客戶名] [專案名]"

# Branch 策略（依規模選擇）
小型（1-2 人）：main + feature branches
標準（3-5 人）：main + develop + feature/[ticket] branches
```

### 環境設定清單

```
開發環境：
  □ .env.example 建立（列出所有需要的環境變數）
  □ 本地開發環境跑起來（npm run dev / yarn dev）
  □ README.md 有 Setup 說明

Staging 環境：
  □ Vercel / CF Pages preview 設定完成
  □ Staging DB 建立（獨立，不混 Production）
  □ 環境變數設定完成

CI/CD：
  □ GitHub Actions / Vercel 自動部署設定
  □ main → production，develop → staging

第三方服務：
  □ 列出所有需要的 API Key / 帳號
  □ 確認哪些需要客戶提供（開一張清單給客戶）
```

---

## Day 2-3：ADR-001 建立（奠定技術基礎）

第一個 ADR 永遠是「主要技術棧確認」：

```markdown
# ADR-001: 確認技術棧與架構模式

**狀態：** Accepted
**日期：** YYYY-MM-DD
**專案：** [客戶名] — [專案名]
**決策者：** [姓名]

## 背景

[簡述專案規模、用戶數、主要功能、時程限制]

## 考慮選項

[依 /rsun-sysdesign 的決策框架，列出考慮的選項]

## 決定

前端：[Next.js 15 / React / Vue]
後端：[Next.js API Routes / Express / Hono]
資料庫：[PostgreSQL / MongoDB]
部署：[Vercel / CF Pages / Fly.io]
架構模式：[Modular Monolith / Monolith]
AI（如有）：[LLM Provider + RAG / 無]

## 後果

✅ 變得更容易：[...]
⚠️ 變得更困難：[...]
📋 新約束：[...]
```

> 存入 `docs/adr/ADR-001-tech-stack.md`，更新 `docs/adr/README.md`

---

## Day 3-4：角色分工 + 溝通節奏確認

### 容晟內部分工

```markdown
## 角色分工

| 角色 | 負責人 | 職責 |
|------|-------|------|
| PM | [名字] | 客戶溝通、PRD 維護、Sprint 規劃 |
| Tech Lead | [名字] | 架構決策、ADR、Code Review |
| Frontend | [名字] | UI 開發 |
| Backend | [名字] | API、DB、Business Logic |
| QA | [名字 / 共同負責] | 對照 Acceptance Criteria 測試 |
```

### 客戶溝通節奏

**每週必做：**
```
週一：發本週 Sprint 目標給客戶（一封 Email / LINE）
週五：發本週進度報告 + 下週計畫（有截圖更好）
```

**每兩週：**
```
Sprint Review：Demo 給客戶看，確認方向沒跑掉
```

**溝通原則：**
- 壞消息要第一時間說，不要等週報
- 需求模糊時，主動召會而非猜測
- 客戶 Scope 擴張時，當下回應（不是默默做）：
  「這個新需求超出原始 PRD 範圍，我確認工時後跟你說是否需要變更單。」

---

## Day 4-5：第一個 Sprint 規劃

### Sprint 0（第一週）目標

第一個 Sprint 不是做功能，是**讓團隊可以平行工作**：

```
Sprint 0 目標：
  □ 環境全員能跑
  □ DB Schema v1 設計完成（ADR 記錄）
  □ API 設計草稿（路由清單）
  □ 前端架構 + Router 設定
  □ 設計稿 Wireframe 完成（關鍵頁面）
  □ 第一個 User Story 的骨架（可以跑，沒有樣式也沒關係）
```

### Sprint 規劃格式

```markdown
## Sprint 1 — [日期範圍]

**Sprint 目標：** [一句話，可以用這句話向客戶說明這週做什麼]

**User Stories：**
| Story | 複雜度 | 估時 | 負責人 | 狀態 |
|-------|-------|------|-------|------|
| [Story 1] | M | 20hr | [人] | Todo |
| [Story 2] | S | 8hr | [人] | Todo |

**Sprint Capacity：**
[人數] × [工作天] × 6hr/天 = [可用工時]
本 Sprint 認領：[工時]（勿超過 80%，留彈性）

**Definition of Done：**
- Code Review 通過
- Acceptance Criteria 測試通過
- 部署到 Staging 可以 Demo
```

---

## Kickoff 會議議程（與客戶）

第一次正式開工會議（建議視訊，30-45 分鐘）：

```
1. 確認 PRD（5 分鐘）
   → 快速過一遍功能範圍，確認 In/Out of Scope

2. 確認聯絡窗口（5 分鐘）
   → 客戶端：誰是 PM？誰做 UAT？誰做最終確認？
   → 容晟端：誰是主要聯絡人？

3. 確認溝通方式（5 分鐘）
   → 日常：[LINE / Email / Slack]
   → 緊急：[手機]
   → Demo / Review：每兩週，[哪一天，幾點]

4. 確認客戶需要提供的東西（10 分鐘）
   → 品牌素材（Logo / 色碼 / 字型）
   → 現有系統的 API / 資料（如有整合）
   → 測試帳號 / 測試資料
   → 第三方服務 API Key（如客戶自有）

5. 時程說明（10 分鐘）
   → 主要 Milestone 說明
   → 何時需要客戶回饋 / 確認（說清楚他們的義務）
```

---

## Kickoff 完成清單（Done Criteria）

這個清單完成，才算真正開工：

```
內部：
  □ Git repo 建立，.env.example 存在
  □ 本地環境全員能跑
  □ Staging 環境部署成功
  □ ADR-001 建立完成
  □ Sprint 0 目標確認
  □ 角色分工書面化

客戶：
  □ Kickoff 會議完成
  □ 聯絡窗口確認
  □ 溝通頻率確認
  □ 客戶需提供項目的清單已發出
  □ 第一次週報發出（本週 Sprint 0 目標）
```

---

## 輸出

執行此 skill 後產出：

1. **Kickoff 清單**（Markdown 格式，供內部追蹤）
2. **給客戶的開工 Email**（介紹流程、聯絡方式、客戶需提供事項）
3. **ADR-001 草稿**（技術棧確認）
4. **Sprint 0 規劃表**（第一週工作目標）

---

## ⚙️ 自動更新 project-state.json（必做）

Kickoff 完成後，**必須更新** `~/Projects/TRACKER/clients/[client-id]/project-state.json`：

```json
{
  "phase": 4,
  "phase_label": "開發",
  "sprint": 1,
  "sprint_start": "YYYY-MM-DD",
  "sprint_end": "YYYY-MM-DD",
  "sprint_goal": "[第一個 Sprint 目標]",
  "milestones": {
    "kickoff": true,
    "adr_001": true
  },
  "health": "on-track",
  "health_note": "Kickoff 完成，開發啟動",
  "updated_at": "YYYY-MM-DD"
}
```

更新後執行：
```bash
cd ~/Projects/TRACKER && git add clients/[id]/project-state.json && git commit -m "pm([id]): kickoff — sprint 1 start" && npx wrangler pages deploy . --project-name rsun-tracker --commit-dirty=true
```
