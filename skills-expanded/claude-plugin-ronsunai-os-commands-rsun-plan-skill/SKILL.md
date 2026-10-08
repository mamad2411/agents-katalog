---
name: rsun-plan
description: GOAP（Goal-Oriented Action Planning）— 把白話文目標自動轉成結構化執行計畫（含 skill chain + sub-agent dispatch + 工時估算 + cap-aware 警告）。觸發詞：「規劃」「plan」「我想做 X 怎麼開始」「幫我排計畫」「白話 → 計畫」「規劃這個案子」。對應 Ruflo SONA 的 GOAP 概念，但靠 LLM + retrieve 過去類似案例（rsun-citation semantic_search）。
user-invocable: true
---

# /rsun-plan — 白話文目標 → 結構化執行計畫

## 為什麼這個 skill

**動機**：容晟有 31 sub-agent + 25+ skill + 場景 A-G chain，但每次新任務 user 說「我想做 X」，Zenya 還要花 5-10 分鐘問清楚 / 對齊 / 排計畫。這個 skill 把這段壓縮成自動產出。

**對標**：Ruflo 的 GOAP（Goal-Oriented Action Planning）— 但他們靠 PDDL planner，我們靠 LLM + retrieve 過去類似 case。

**真實踩雷**：Apex Gold 案 Zenya 沒先對齊 paradigm + 沒讀過去類似案例 → 200+ hr 白寫（見 Anti-pattern F）。`/rsun-plan` Step 1 retrieve 過去 cluster brief / METRIC / DEC，避免重蹈覆轍。

## 何時呼叫

| 情境 | 是否呼叫 |
|---|---|
| 客戶說「想做 ESG 平台 / 房產系統 / CRM」 | ✅ 強制（Phase 0 第一步）|
| 內部要做新 feature / refactor / cleanup | ✅ 推薦 |
| 派 ≥ 3 sub-agent 的批次任務 | ✅ 強制（cap-aware 防撞）|
| 單檔 < 50 行 bug fix | ❌ 不需 |
| 純查詢 / monitoring | ❌ 不需 |

---

## 執行步驟（5 step）

### Step 0 — 意圖分類

把 user 白話 goal 分到 5 類之一：

| 類別 | 關鍵字 | 對應場景 | 預設 chain |
|---|---|---|---|
| **A 客戶交付** | 客戶名 / 提案 / proposal / 報價 / 案子 | 場景 C | `/rsun-grill` → `/rsun-lean-canvas` → `/rsun-prd` → `/rsun-architect` → `/rsun-estimate` → `/rsun-proposal` |
| **B 內部 bug fix** | bug / 修 / fix / 壞 / broken / 不行 | 場景 A | `codebase-onboarding-engineer` → `minimal-change-engineer` → `evidence-collector` → `code-reviewer` |
| **C 客戶 UAT 交付** | 上線 / deploy / 部署 / 交付 / UAT | 場景 D | `reality-checker` → `accessibility-auditor` → `performance-benchmarker` → `security-engineer` → `engineering:deploy-checklist` → `/rsun-deploy` |
| **D 行銷 / 品牌** | 行銷 / SEO / 文案 / 品牌 / 曝光 | 場景 G | `ai-citation-strategist` → `seo-specialist` → `linkedin-content-creator` → `brand-guardian` |
| **E 不確定** | （以上都不像） | — | **反問 user**：「你比較像 [A/B/C/D] 哪個？或我有理解錯嗎？」|

**禁止 hallucinate** — 不可推薦 CLAUDE.md 31-agent 清單外的 sub-agent，也不可推薦 `~/.claude/skills/` 不存在的 skill。

---

### Step 1 — Retrieve 過去類似案例

呼叫 `rsun-citation` MCP 找過去引用單元（ADR / METRIC / DEC / CLUSTER / CASE / MOD）：

```
mcp__rsun-citation__semantic_search(
  query="<user 白話 goal>",
  top_k=5
)
```

> 注意：`semantic_search` 是 Phase 1 新工具（MOD-TRACKER-VECTOR）。
> 若該工具尚未上線，fallback 到 `mcp__rsun-citation__search_citation`（既有關鍵字版）。

**萃取 3 個訊號**：
1. 過去類似客戶案的 paradigm（A/B/C）— 若有，預填進 Step 2
2. 過去工時 METRIC — 校準工時估值
3. 過去踩過的雷（Anti-pattern A-H）— 列入 Step 2 風險區

---

### Step 2 — 產出結構化 plan

**輸出格式**（必填表格）：

```markdown
## Plan — <task title>

**Paradigm**：A / B / C / E（若 Step 0 屬 A 客戶類）
**對齊 profile**：apex-gold / dashboard-internal / legal-single / d2c-fortune（若有）
**過去類似 case**：<unit_id list>（從 Step 1 取）

| # | Phase | Skill / Agent | 預估工時 | 依賴 | 產出 |
|---|---|---|---|---|---|
| 1 | Discover  | /rsun-grill         | 0.5 hr  | -   | paradigm + 3 keywords |
| 2 | Discover  | /rsun-lean-canvas   | 0.5 hr  | 1   | 9 方格商業確認 |
| 3 | Define    | /rsun-prd           | 2 hr    | 2   | PRD P0/P1/P2 |
| 4 | Architect | /rsun-architect [cat] | 3 hr  | 3   | variant 藍圖 |
| 5 | Estimate  | /rsun-estimate      | 1 hr    | 4   | WBS + 報價 |
| 6 | Deliver   | senior-developer    | 40 hr   | 5   | feature impl |
| 7 | Deliver   | code-reviewer       | 0.5 hr  | 6   | review pass |
| 8 | Deliver   | reality-checker     | 0.5 hr  | 7   | UAT 證據 |
| ...

**總計**：X hr | X MM
**風險**：<list 過去踩過的雷 / Anti-pattern 對照>
```

**工時必含 buffer**：依 ESTIMATE_SOP.md 規則（一般 1.2x、高風險 1.3x、創新 1.5x）。

---

### Step 3 — Cap-aware 警告（**強制**）

讀 `data/claude-code-usage.json` 的 `current_snapshot.weekly_all_models_pct`：

| weekly_pct | 行為 |
|---|---|
| ≥ 90% | 🚫 **拒絕產出 plan**，跟 user 說「weekly cap 已 ≥90%，請等 Sunday 3am 重置或 BYPASS=1 手動跑」|
| 75-90% | ⚠️ **plan 限縮**：max 2 sub-agent + 強制每 Phase 加 checkpoint 注解 |
| 50-75% | ⚠️ plan 可放 max 4 sub-agent + checkpoint 推薦 |
| < 50% | ✅ 正常 — max 6 sub-agent 平行 |

**對照 ADR-009**（cap-aware dispatch）。

---

### Step 4 — Metric 校準（若 Step 1 retrieve 到 METRIC-* 節點）

對每個 Phase，若有相關 METRIC 節點，**用實際工時 override 預設工時**：

```
若 METRIC-CRM-V2-TRACK-A3-20260504 顯示「v2 backend 4 sub-agent 收割 8 hr」
→ Phase「Deliver senior-developer」的 40 hr 校正成 8 hr × buffer 1.2 = 9.6 hr
```

**校準後** plan 加註「（依 METRIC-XXX 校準）」讓 user 知道工時來源。

---

## 輸出範例（白話 goal: "客戶想做 ESG 報告書平台"）

```markdown
## Plan — ESG 報告書平台（客戶案）

**Paradigm**：A: CMS-driven（客戶 demo 期望「好用的後台讓我自己改」）
**對齊 profile**：apex-gold-realestate（強稽核 + 多租 + ESG 法遵）
**過去類似 case**：DEC-CLIENT-PARADIGM-001 / Anti-pattern F（Apex 誤判事件）

| # | Phase | Skill / Agent | 工時 | 依賴 | 產出 |
|---|---|---|---|---|---|
| 1 | Discover | /rsun-grill | 0.5 hr | - | 確認 CMS 而非 SaaS |
| 2 | Discover | /rsun-lean-canvas | 0.5 hr | 1 | 商業確認 |
| 3 | Define | /rsun-prd | 2 hr | 2 | PRD P0/P1/P2 |
| 4 | Architect | /rsun-architect [esg] | 3 hr | 3 | variant 藍圖 |
| 5 | Estimate | /rsun-estimate | 1 hr | 4 | WBS + 報價 |
| 6 | Proposal | /rsun-proposal | 1 hr | 5 | 5 段式提案 |

**總計**：8 hr | 0.05 MM（Discovery + Estimate 階段；不含 Deliver）
**Cap status**：weekly 0% ✅ 安全
**風險**：
- 🚨 **Anti-pattern F 重演風險**：客戶可能說「ESG 諮詢」但實際要房產 listing → Step 1 必擰乾「客戶 demo 想看到什麼」3 次
- ⚠️ ESG 法遵變動快 — 規格定義階段必對 GRI/SASB/CSRDS 標準
```

---

## 不可違反的規則

1. ⚠️ **不准 hallucinate skill/agent name** — 所有引用必對得到實際 file
2. ⚠️ **必走 Step 3 cap-aware** — 不可省略
3. ⚠️ **若 Step 0 屬 E（不確定）→ 反問 user**，不要硬猜
4. ⚠️ **Step 1 找不到類似 case → 註明「無過去引用，工時純估」**，不要假裝有

---

## 對應 ADR / DEC

- ADR-009：cap-aware dispatch（Step 3 來源）
- DEC-CLIENT-PARADIGM-001：A/B/C paradigm 識別（Step 0 來源）
- ESTIMATE_SOP.md：buffer 1.2/1.3/1.5（Step 2 來源）
- Anti-pattern F：客戶 paradigm 誤判（Step 1 風險檢查）

---

## 觸發後行為

讀完此 skill → **立刻**跑 Step 0-4 → 輸出 plan 表格給 user → user 說「動」才開始 dispatch agent / 呼叫 skill。

**禁止**讀完 skill 後直接派工 — Plan 是 review gate。
