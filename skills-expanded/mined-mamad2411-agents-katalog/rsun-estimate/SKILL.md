---
name: rsun-estimate
description: 容晟科技專案估價。當用戶說「幫我估價」「估一下這個」「做報價」「幫我算工時」「estimate」「報價單」時使用。執行完整 SOP：需求分析 → **歷史校準（rsun-citation MCP）** → 市場研究 → 架構設計 → WBS 工作包 → 人月計算 → 產出 Google Sheets 估價文件並存入 Drive。
user-invocable: true
allowed-tools: "Bash(cat *) Bash(ls *) Bash(python3 *) Read WebSearch mcp__b89b62b2-20e1-4f51-a5b1-23e8a243c958__create_file mcp__b89b62b2-20e1-4f51-a5b1-23e8a243c958__search_files mcp__b89b62b2-20e1-4f51-a5b1-23e8a243c958__list_recent_files mcp__rsun-citation__search_citation mcp__rsun-citation__get_unit mcp__rsun-citation__list_by_type mcp__rsun-citation__find_backlinks mcp__rsun-citation__query_recent_metrics"
---

# 容晟科技專案估價 SOP

## 資料資產位置

- **SOP 完整說明**：`/Users/ezonelai/Projects/TRACKER/docs/estimate/ESTIMATE_SOP.md`
- **費率卡**：`/Users/ezonelai/Projects/TRACKER/docs/estimate/rate_card.md`
- **WBS 範例**：`/Users/ezonelai/Projects/TRACKER/docs/estimate/wbs_examples.md`
- **Drive 估價範本**：`00_專案估價單範本`（Google Drive，ID: `1ipUFadpbfm4xUyC5l_OQUwa6LMbayUdPMh_CiyzKJIc`）

開始前，先讀取上述資料資產作為背景知識。

---

## 執行步驟

### Step 1｜需求分析（5 分鐘內完成）

閱讀或詢問用戶取得以下資訊：
- **功能需求**：列出所有功能點，依模組分類
- **非功能需求**：效能、安全性、擴展性、裝置/瀏覽器支援
- **技術限制**：指定語言/框架、既有系統整合、資料遷移
- **排除範圍**：明確記錄不做的事
- **時程期望**：客戶期望的交付時間

如有不清楚的需求，**先詢問用戶**再繼續，不可假設。

輸出：**功能清單表格**（模組 / 功能點 / 優先級）

---

### Step 2｜歷史校準（**必跑**，先查容晟過去實績）

**在做任何市場研究前，先向 rsun-citation MCP 查詢歷史同類案的實際值**。這是估準率迴圈的輸入端——只有回看過去才知道自己過去估偏了多少。

呼叫順序（並行呼叫效率最好）：
1. **METRIC 統計校準（推薦先呼叫）** — `query_recent_metrics(category="<本案 cluster: crm/cms/booking/erp/ai>", top_n=5, days=365)`
   → 直接回傳統計（avg / median / std_dev variance_pct）+ 自動 `recommendation` 字串給 Buffer 調整建議
2. 最相似 CASE（實做過的專案） — `search_citation(query="...", type="case", limit=5)`
3. 實績 METRIC 全文搜（補 #1 找不到的 free-text）— `search_citation(query="...", type="metric", limit=5)`
4. 可套用 MOD（production 模組可降工時） — `search_citation(query="...", type="mod", limit=5)`
5. 相關 ADR / SOP / GOTCHA（已累積的決定和陷阱） — `search_citation(query="...", type="adr")`、`list_by_type(type="sop")`

**輸出 Step 2 報告**（寫進估價單附註）：

```
📚 歷史校準 baseline
  query_recent_metrics(crm)：sample_count=5, avg_variance_pct=+18%, median +15%, std 8%
    → recommendation: "歷次同類案平均超估 18%，建議下調工時 18% 並維持 Buffer 1.2"
  最相似 CASE：CASE-RSUN-CRM (MM=0.75, NT$90k, 滿意 8/10)
  METRIC 實績：actuals 120hr / 估 160hr → variance -25%
  可套用 MOD：MOD-CRM-ACTIVITY (production, 複雜度 S)
  相關 ADR：ADR-001 (Cookie Auth), ADR-007 (Static Deploy)
  相關 GOTCHA：GOTCHA-CSRF-001（此類案常見陷阱）
  → 本案工時調整建議：基準 120hr × MOD 折減 0.8 × variance 校準 0.82 × Buffer 1.2 = 95hr
```

**重要**：Step 4 WBS Buffer 倍數必須參考 Step 2 的 `recommendation` 結果：
- avg_variance_pct > +20% → Buffer 維持 1.2 但工時下調 X%
- avg_variance_pct < -20% → Buffer 上調至 1.5 + 工時上調 X%
- sample_count < 3 → 採保守 Buffer 1.3（樣本不足）
- 絕對值 ≤ 20% → 採標準 Buffer 1.2

若 rsun-citation 無法呼叫（MCP server 未啟動或 index 不存在），**必須告知用戶**並手動查閱 `knowledge/citation-index.json`，**不可跳過此步驟**。

---

### Step 3｜市場研究與難度校準（同類競品參考）

針對主要功能模組，進行：
1. 同類產品調研（WebSearch：找同類 SaaS 的功能範圍）
2. 技術難度評估：
   - 是否有成熟套件可用？（降低工時）
   - 是否有未知第三方整合？（加 Risk Buffer）
   - 是否涉及 AI/ML 自研？（高度不確定，加 ×1.5）
3. 識別**高風險工作包**（標記 ⚠️）

**把 Step 2 歷史校準與 Step 3 市場研究交叉對照**：若市場範圍大於歷史實做 >30%，要麼調大工時、要麼建議削減範圍。

---

### Step 4｜架構設計與模組清單

根據需求與技術難度，產出：
- 系統架構（前端 / 後端 / DB / 第三方服務）
- 模組清單（最多 8 個主模組）
- 每個模組的主要技術選型

格式：
```
模組清單
├── M1: 用戶系統（Auth、角色權限）
├── M2: 核心業務模組
├── M3: 資料報表
├── ...
└── M8: 部署與維運
```

---

### Step 5｜WBS 工作包拆解

**複雜度等級定義**（讀取 rate_card.md 確認最新費率）：

| 等級 | 描述 | 工時 | Buffer |
|------|------|------|--------|
| S | 靜態頁面、基礎 CRUD、簡單 UI | 4–16 hr | ×1.2 |
| M | 中型功能、標準 API 串接、表單驗證 | 16–40 hr | ×1.2 |
| L | 複雜業務邏輯、第三方深度整合、多角色權限 | 40–80 hr | ×1.3 |
| XL | 架構設計、AI 模組、核心引擎 ⚠️ | 80–160 hr | ×1.5 |

**輸出格式**：

```
模組 M1：用戶系統
├── 工作包 1.1｜登入/註冊 UI｜S｜Junior｜8hr × 1.2 = 9.6hr
├── 工作包 1.2｜OAuth 第三方登入｜M｜Mid｜24hr × 1.2 = 28.8hr
├── 工作包 1.3｜RBAC 角色權限系統｜L｜Senior｜60hr × 1.3 = 78hr
模組小計：116.4 hr = 0.73 MM

...（所有模組）

專案總工時：XXX hr
總人月：X.XX MM
```

---

### Step 6｜人月成本計算

讀取 `/Users/ezonelai/Projects/TRACKER/docs/estimate/rate_card.md` 取得最新費率。

標準公式：
```
1 MM = 160 hr

內部成本 = Σ（工作包工時 × 對應人員月薪 ÷ 160）

報價（含稅前）= 內部成本 × 毛利倍數
  - 標準專案：×1.8
  - 緊急/短期：×2.0
  - 長期合作/重複客戶：×1.5

稅金 = 報價 × 5%
總報價 = 報價 + 稅金

付款分期：
  - 簽約款 30%：簽約時
  - 開發款 40%：開發完成
  - 驗收款 30%：驗收通過
```

---

### Step 7｜產出估價文件

1. **建立 Google Sheets**（存入 Drive）：
   - 搜尋 Drive 範本 `00_專案估價單範本`
   - 用 `create_file` 建立新的 Sheets 並填入 WBS 明細
   - 命名格式：`[客戶名稱]-[專案名稱]-估價單-[YYYYMM]`

2. **輸出摘要**給用戶（純文字，方便複製）：
   ```
   === 估價摘要 ===
   專案名稱：XXX
   總工時：XXX hr（含 Buffer）
   總人月：X.XX MM
   內部成本：NT$XXX,XXX
   對客戶報價（稅前）：NT$XXX,XXX
   稅金 5%：NT$XX,XXX
   總報價：NT$XXX,XXX

   付款分期：
   - 簽約款 NT$XXX,XXX（30%）
   - 開發款 NT$XXX,XXX（40%）
   - 驗收款 NT$XXX,XXX（30%）

   Drive 估價單：[連結]
   ```

3. 詢問用戶是否需要 PDF 報價單或 PPTX 提案簡報。

---

## 注意事項

- **Step 2 歷史校準是新流程的核心**，不可跳過，這是「估準率迴圈」的關鍵輸入端
- **不可跳過 Step 3 市場研究**，對工時校準影響最大
- **模糊需求必須追問**，不可假設功能範圍
- **高風險項目（⚠️）必須加 ×1.5 Buffer** 並在報價說明中標注
- 若客戶給的時程比合理工期短 30% 以上，**主動告知風險並建議縮減範圍**
