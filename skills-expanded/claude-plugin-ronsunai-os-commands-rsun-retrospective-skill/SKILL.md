---
name: rsun-retrospective
description: Sprint 或專案結束後的復盤 SOP。比對估值 vs 實際工時、分析偏差原因、產出 WBS 校準建議，形成持續改善的估準率迴圈。當用戶說「復盤」「retro」「案子結束了」「這案子學到什麼」時使用。
user-invocable: true
allowed-tools: "Read Write Bash(cat * ls *)"
---

# rsun-retrospective — 專案 / Sprint 復盤

復盤的核心目的：**讓下一次估價更準、讓下一次執行更順**。不是在追責，而是在校準。

**適用時機：**
- 每個 Sprint 結束後（2 週一次）
- 專案交付後（必跑）
- 估價偏差超過 30% 時（緊急校準）

---

## 執行步驟（4 個區塊）

### Block 1：數字比對（10 分鐘）

收集以下資料，沒有數字就無法改善：

```
專案名稱：[名稱]
Sprint / 交付期間：[開始日] → [結束日]

估價工時 vs 實際工時：
| 模組 / 工作包 | 估計工時 | 實際工時 | 偏差 | 偏差率 |
|-------------|---------|---------|------|-------|
| [模組 1] | Xhr | Xhr | +/-Xhr | +/-X% |
| [模組 2] | Xhr | Xhr | +/-Xhr | +/-X% |
| 合計 | Xhr | Xhr | +/-Xhr | +/-X% |

估計報價 vs 實際成本：
- 報給客戶：NT$XXX,XXX
- 實際內部成本：NT$XXX,XXX
- 毛利率：X%（目標 > 45%）
```

> 資料來源：`/rsun-capture-metric` 回填記錄 + git log（實際工作天數）

### Block 2：三個核心問題（20 分鐘）

#### 2.1 做得好的事（Keep）
什麼事情進行順利，下次要繼續保持？
- 技術決策（哪個 ADR 做對了）
- 流程（什麼步驟讓開發加速）
- 溝通（哪次客戶溝通特別順）
- 工具（哪個 skill / 工具節省了時間）

#### 2.2 需要改進的事（Improve）
什麼事情讓我們變慢或品質下降？
- 需求不清楚導致的返工（→ 改善 PRD / User Stories）
- 技術選型錯誤（→ 改善 sysdesign / ADR 流程）
- 估價偏差（→ 分析偏差類型）
- 客戶溝通卡點（→ 改善節奏或模板）

#### 2.3 下次要不同做的事（Change）
具體的行動承諾，必須有人負責：

| 改變項目 | 具體行動 | 負責人 | 時間 |
|---------|---------|-------|------|
| [問題] | [下次怎麼做] | [誰] | [何時前] |

### Block 3：WBS 校準分析（15 分鐘）

這是最有長遠價值的部分——把偏差轉化成未來估價的校準參數。

#### 偏差分類

```
偏差類型 A — 需求模糊（Scope Creep）
  症狀：實際工時 > 估計，原因是需求在開發中變動
  校準：加強 PRD 的 Scope Boundary，Out of Scope 要更明確
  → 下次這類功能 Buffer × 1.3（原本 × 1.2 調整）

偏差類型 B — 技術低估（Technical Underestimate）
  症狀：某類工作包（如第三方 API 整合）持續低估
  校準：這類工作包的基準工時上調 20-30%
  → 例：「第三方金流整合」從 M 等級（16-40hr）改為 L 等級起算（40hr+）

偏差類型 C — 外部等待（External Dependency）
  症狀：工時實際沒多，但 calendar time 拉長（等客戶提供資料 / API key）
  校準：加入「外部等待 Buffer」在 calendar 規劃中，工時估價不需調整
  → PRD 的 Step 7 相依風險要更詳細列出

偏差類型 D — 過度樂觀（Optimism Bias）
  症狀：整體持續低估 10-20%，沒有特定原因
  校準：整體加一個「樂觀偏差補正」× 1.1 到所有工作包
```

#### 累積校準表（每次 retro 後更新）

```markdown
## WBS 校準記錄（累積）

| 工作包類型 | 預設複雜度 | 實際觀察 | 累積校準倍數 |
|-----------|-----------|---------|------------|
| 標準 CRUD UI | S | 準確 | × 1.0 |
| 第三方 API 整合 | M | 持續低估 | × 1.35 |
| 多語系實作 | M | 低估 | × 1.3 |
| AI 功能（RAG / LLM）| XL | 不確定性高 | × 1.5 |
| 資料遷移 / 匯入 | L | 持續低估 | × 1.4 |
| 多角色權限系統 | L | 準確 | × 1.0 |
```

### Block 4：Action Items（5 分鐘）

復盤完必須產出可執行的清單：

```markdown
## Action Items

| # | 行動 | 類型 | 負責人 | 截止日 | 狀態 |
|---|------|------|-------|--------|------|
| 1 | 更新 WBS 校準表（第三方 API 類別）| skill 更新 | Claude | 本週 | [ ] |
| 2 | 在 PRD template 加強 Out of Scope 欄位 | 流程改善 | PM | 下次接案前 | [ ] |
| 3 | 把[客戶名]案的 ADR 寫進知識庫 | 知識管理 | Dev | 本週 | [ ] |
```

---

## 輸出格式

```markdown
# 復盤報告 — [專案名 / Sprint N]

**日期：** YYYY-MM-DD
**參與者：** [名單]

---

## 1. 數字比對

[工時比對表]
[毛利率]

## 2. 回顧分析

### 做得好的事 ✅
- ...

### 需要改進的事 ⚠️
- ...

### 下次要改的事 🔄
| 改變項目 | 行動 | 負責人 | 時間 |
|---------|------|-------|------|

## 3. WBS 校準建議

[偏差分類 + 校準倍數調整建議]

## 4. Action Items

[清單]

---

## 存檔位置

Drive: `My Drive/容晟科技/客戶專案/[客戶名]/09_復盤_[YYYYMM].gdoc`
TRACKER: 更新對應客戶的 notes 欄位（`/rsun-client`）
```

---

## ⚙️ 自動更新 project-state.json（必做）

復盤完成後，**必須更新** `~/Projects/TRACKER/clients/[client-id]/project-state.json`：

```json
{
  "sprint": "[sprint號 + 1]",
  "sprint_start": "YYYY-MM-DD",
  "sprint_end": "YYYY-MM-DD",
  "sprint_goal": "[下個 Sprint 目標]",
  "stories_total": "[累計更新]",
  "stories_done": "[累計完成]",
  "health": "on-track | at-risk | waiting",
  "health_note": "[復盤後的一句摘要]",
  "updated_at": "YYYY-MM-DD"
}
```

如果是**專案最終復盤**（交付完成）：
```json
{
  "phase": 6,
  "phase_label": "維運",
  "milestones": { "delivered": true, "client_uat": true },
  "health": "ok",
  "health_note": "交付完成，進入維運期"
}
```

更新後執行：
```bash
cd ~/Projects/TRACKER && git add clients/[id]/project-state.json && git commit -m "pm([id]): retro sprint [N] — [一句摘要]" && npx wrangler pages deploy . --project-name rsun-tracker --commit-dirty=true
```

---

## 復盤節奏建議

| 頻率 | 觸發條件 | 深度 |
|------|---------|------|
| 每 2 週 | Sprint 結束 | 輕量（Block 1 + Block 2）|
| 每個專案 | 客戶驗收後 | 完整（4 個 Block）|
| 緊急 | 偏差 > 30% | 立即跑 Block 3 + 4 |

---

## 注意事項

- **沒有數字就不算復盤**：感覺型復盤（「大家覺得這次還不錯」）沒有校準價值
- **WBS 校準表要累積**：每次 retro 後更新 `docs/estimate/wbs_examples.md` 的校準備注
- **Action Items 要追蹤**：下次 retro 先回顧上次 Action Items 的執行狀況
