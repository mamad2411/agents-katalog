---
name: rsun-architect
description: 權變式架構合成。當需要為某個模組類別（CRM / CMS / ERP / dashboard / auth / ui / chart / db / ai 等）寫一份「對應某個客戶情境」的完整架構藍圖時使用。讀 N 個 OSS 借鑑來源（cluster brief）+ 客戶情境矩陣（contingency-matrix），由我（Opus）親自寫 variant 藍圖（不外包給弱模型）。Triggered by 「架構藍圖」/「設計 rsun-X 模組」/「組架構」/「寫 variant」/「權變設計」/`/rsun-architect [category]`。
user-invocable: true
allowed-tools: "Read Write Bash Grep Glob"
---

# rsun-architect — 權變式架構合成

整合自 Fred Fiedler「權變理論」(Contingency Theory) 與 Lawrence & Lorsch 組織設計：
**沒有單一最佳架構**，最佳設計取決於客戶情境變數（auditability / multi-tenancy / latency budget / compliance / team size / data volume / customization）。

這份 skill 的目的：**給定一個 module 類別 + 一個客戶情境，由 Opus 親自寫一份高品質的 variant 架構藍圖**。

---

## 使用情境

| 觸發 | 動作 |
|------|------|
| 「設計 rsun-crm 給 apex-gold 用」 | `/rsun-architect crm` → 選 apex-gold-esg variant |
| 「我想看 cms 在 4 個 profile 下分別長怎樣」 | `/rsun-architect cms` × 4 次 |
| 「ui 累積夠多 OSS 借鑑了，幫我寫一份」 | `/rsun-architect ui` |
| 「現在哪些 cat 可以動工？」 | 直接呼叫 MCP `list_ready_categories` |

---

## 三層資料結構（已建立）

```
Layer 1：原始候選
  knowledge/nodes/modules/candidates/oss-{slug}.md   (60+ 個 GitHub trending 萃取)

Layer 2：cluster brief（Tier 2 結構化萃取，Gemini Flash 寫）
  knowledge/architecture/cluster-briefs/{cat}-brief.md
    含：共同 entity / 命名分歧 / 各家絕招 / multi-tenant 適性 / license 風險

Layer 3：contingency matrix（手寫 + Opus 維護）
  knowledge/architecture/contingency-matrix.md
    定義 4 個典型客戶 profile：
      - apex-gold-esg：強稽核 / 強多租 / ESG 法遵
      - rsun-dashboard-internal：速度優先 / 弱多租 / SMB
      - legal-single-tenant：強加密 / 單租部署 / 律所
      - fortune-teller-d2c：edge cache / 高並發 / D2C

Layer 4：variant blueprints（這 skill 寫）
  knowledge/architecture/blueprints/rsun-{cat}/variants/{client_id}.md
```

---

## 工作流（Opus 在這 skill 裡親自執行）

### Step 1：盤點當下可動工的 category

呼叫 MCP rsun-architect：
```
list_ready_categories({min_borrow: 2})
```

回傳每個 category 的 borrow_count / has_brief / existing_variants。
顯示給用戶：「目前 X cat 可以動工，已有 Y variants，你想動哪個？」

### Step 2：確定要動的 category

- 若用戶在 prompt 中已指定（如 `/rsun-architect crm`），跳到 Step 3
- 若沒指定，列 ready cat → 用戶選

### Step 3：取材料

平行呼叫（同一個 message 內）：
```
get_cluster_brief({category: "crm"})
get_candidates({category: "crm", verdict: "BORROW", min_fit: 5})
list_existing_variants({category: "crm"})
list_client_profiles()
```

把 brief + candidates 的關鍵內容讀進腦袋。

### Step 4：選 variant 的客戶情境

- 顯示 4 個 profile（list_client_profiles 回傳）
- 顯示 existing_variants（已寫過的）
- 問用戶：「這次寫哪個 variant？(apex-gold-esg / rsun-dashboard-internal / legal-single-tenant / fortune-teller-d2c / 自定義)」

若用戶選「自定義」→ 引導用戶填 7 個 constraint（auditability / multi_tenancy / compliance / latency_budget / team_size / data_volume / customization），先寫進 contingency-matrix.md 再繼續。

### Step 5：取該 client profile 的完整約束

```
get_client_profile({client_id: "apex-gold-esg"})
```

讀 yaml_block 取得：constraints / architecture_bias / preferred_stack / risks。

### Step 6：**骨架 + Agent + 終審 三段式分工**（v2 — 2026-04-25 起）

**核心判斷力是 Opus 的，但「結構化填充」交給 Sonnet — 這樣才符合 token 經濟。**

工作分工（依序執行）：

#### 6.1 Opus 寫骨架（Section 0 / 1 / 9）
這 3 段是「**判斷力核心**」，Opus 親寫，**不可外包**：
- **Section 0 (TL;DR)** — 與其他 variant 的核心差異定位、核心取捨、預算上下界
- **Section 1 (情境約束)** — 7 dim constraints + 2-3 條 architecture_bias 與如何回應
- **Section 9 (不適用此 variant 的情境)** — 權變思路的本質，明確列至少 1 個其他 profile 為何不適合

把骨架寫到 `/tmp/{variant}-skeleton.md`。

#### 6.2 Agent(Sonnet) 寫血肉（Section 2-8）
用 Agent tool（`subagent_type: general-purpose`，預設 Sonnet）派工，prompt 必含：
1. **必讀檔案清單** — 骨架路徑 / 同 module 已寫的另一個 variant 路徑 / contingency-matrix profile / cluster brief
2. **Section 2-8 的具體要求** — 每段格式對齊已存在 variant、明確標出「vs 另一 variant 的差異」、命名空間沿用、code block 風格、表格欄位
3. **WBS 規範** — 1 MM = 160 hr / mid-dev NT$120k/MM / Senior NT$180k/MM / Buffer 1.3 / 毛利 1.8x，要求 agent 自驗工時加總
4. **輸出位置** — `/tmp/{variant}-meat.md`（Agent 直接 Write，不要 inline 回傳給 Opus）

#### 6.3 Opus 終審 + 組裝
- 讀 Agent 寫的 meat
- 抽查：命名一致 / 工時加總對得起 / 與骨架定位無矛盾 / 無 OSS 直接抄錄痕跡
- 組裝順序：frontmatter → 骨架 (Section 0/1) → meat (Section 2-8) → 骨架 Section 9 → 防呆檢查
- 用 Bash + cat 落檔到正式位置

**為什麼這樣分？** 骨架是「我下哪些判斷」（Opus 不可替代）；血肉是「把判斷實作成 schema/API/UI/WBS」（結構化填充，Sonnet 等同水準）。實測：較全程 Opus 親寫節省 ~75% output token，品質可控。

---

### 8 段內容規格（不論誰寫都要遵守）

藍圖必須包含 **8 個段落**（用 markdown 寫，不要 JSON）：

```markdown
# rsun-{category} 架構藍圖 — {client_id} variant

## 0. TL;DR
2-3 句話：這個 variant 的核心取捨是什麼，相比其他 variant 強在哪、捨棄什麼。

## 1. 情境約束（從 contingency-matrix 抓）
條列 7 個 constraint + 此情境最關鍵的 2-3 個 architecture_bias，明確標出「這份藍圖如何回應」。

## 2. OSS 借鑑取捨表
從 cluster brief 的 unfair_designs 中挑「適合本情境」的 3-5 個設計。
| 借鑑來源 | 偷的設計 | 為何適合本情境 | 不採用部分 |

## 3. 統一命名空間（防多 repo 變數打架）
這份 variant 的核心 entity 命名（容晟版 PascalCase + snake_case）。
- 主資料模型：`Rsun{Cat}Xxx`
- DB table：`rsun_{cat}_xxx`
- API：`/api/rsun-{cat}/...`
列 5-8 個核心 entity，標明「為什麼這個命名（vs OSS 各家分歧）」

## 4. 資料模型（drizzle schema 草稿）
3-5 個 table，每張 4-8 欄。標出：
- tenant_id 處理方式（強隔離 / 弱隔離 / 無）
- audit 欄位（created_at / updated_at / created_by / version）
- 此情境特有欄位（如 apex-gold 要 audit_log_id 引用）

## 5. API 端點（Hono + REST）
5-10 條端點。每條標 method / path / 用途 / 此情境的 quirk（如 apex 寫入要同 transaction 寫 audit_log）。

## 6. UI 組件（侘寂風）
3-5 個主要頁面/組件。標明此情境的 UX 取捨（apex 強調表單嚴謹 vs fortune-teller 強調樂觀 UI）。

## 7. WBS + 工時（容晟標準）
| 工作包 | 複雜度 | 技能 | 工時 (hr) | MM |
6-10 個工作包。最後一行小計：
**合計：X hr / Y MM / NT$Z（mid-dev × 1.3 buffer × 毛利 1.8x）**

## 8. 風險 & 緩解（針對本情境）
3-5 條，每條一句緩解。聚焦「這個情境特有的風險」。

## 9. 不適用此 variant 的情境
明確列「這份藍圖**不**適合用在哪幾個 profile 上，為什麼」。
這是權變思路的關鍵 — 一個藍圖必須知道自己的邊界。
```

### Step 7：落檔

```
save_blueprint({
  category: "crm",
  variant: "apex-gold-esg",
  content: "<完整 markdown>",
  summary: "強稽核 + 強多租 + ESG 法遵 — 適合政府案 / 上市公司"
})
```

### Step 8：刷圖譜 + 提示下一步

```bash
cd ~/Projects/TRACKER && python3 scripts/build-knowledge.py
```

問用戶：
- 寫下一個 variant？（顯示尚未寫的 profile）
- 換 category？
- 為這個 variant 開估價單？（呼叫 /rsun-estimate）

---

## 重要約束

1. **Step 6 走三段式分工**：Opus 寫骨架 (Section 0/1/9) → Agent(Sonnet) 寫血肉 (Section 2-8) → Opus 終審組裝。**禁止**全程 Opus 親寫（浪費 token）；**禁止**全程外包 Sonnet（喪失判斷力把關）；**禁止**外包給 Gemini Flash / Llama 等弱模型寫藍圖（CRM/權變思路他們扛不住，會跳針）。
2. **Step 6.2 Agent 派工 prompt 必含**：骨架路徑、同 module 已寫 variant 路徑（給格式對齊基準）、cluster brief 路徑、contingency-matrix profile、WBS 規範、輸出到 `/tmp/{variant}-meat.md` 而非 inline 回傳。
3. **Step 6 一定要讀完 cluster brief + 至少 3 個原始候選**（Opus 在寫骨架前必須真的讀），不能只看 brief 蜻蜓點水。
4. **Step 9 強制寫**「不適用此 variant 的情境」— 這是權變思路的本質，不能省。骨架就要寫好，不能丟給 Agent。
5. **WBS 工時用容晟標準**：1 MM = 160 hr，mid-dev NT$120k/MM，Senior NT$180k/MM，Buffer 1.3，毛利 1.8x。Agent 寫完 WBS 後 Opus 必須抽查加總。
6. **multi-tenant 處理一定要明確**：強隔離（per-tenant DB）/ 弱隔離（tenant_id col）/ 無（per-customer deploy）— 三選一寫死。骨架就要決定。
7. **新增 variant 時必對照已存在 variant**：Section 3 命名空間沿用、Section 5 標「禁區端點」、Section 7 在註腳列工時對比。權變思路不只是「寫不一樣」，而是「明確標差異」。

---

## 如何擴充客戶情境

當客戶情境不在現有 4 個 profile 內：

1. 引導用戶填 7 個 constraint
2. 用戶確認後，我（Opus）寫一個新的 yaml block 進 `knowledge/architecture/contingency-matrix.md`
3. commit 該變更
4. 繼續 Step 5 流程

---

## 防呆檢查（在 Step 6 結束時跑）

寫完 markdown 後，自我檢查：
- [ ] 8 個段落都齊全（包含「9. 不適用此 variant」）
- [ ] 命名空間統一（沒從 A repo 偷 Activity、從 B 偷 Task 並存）
- [ ] tenant 處理明確（不是「之後再決定」）
- [ ] WBS 工時數字加總對得起小計
- [ ] 至少引用 3 個 OSS 來源（不是憑空想）
- [ ] 不適用情境至少列 1 個（不能說「適用所有情境」— 那不是權變）

任一不過 → 重寫該段。

---

## 與其他 skill 的關係

- **`/rsun-sysdesign`** — 處理「**全新**系統的整體架構選型」（你有 7 Phase 框架）。本 skill 是「**單一 module** 的多 variant 設計」。互補。
- **`/rsun-adr`** — 寫完 variant 後，每個重大技術選型補一個 ADR，落入 `docs/adr/`。
- **`/rsun-estimate`** — variant 的 WBS 可直接餵進估價 SOP，產出 PDF 報價。
- **`/rsun-prd`** — 在更早階段（PRD 確認後才有資格進 architect 階段）。

順序建議：`/rsun-prd` → `/rsun-sysdesign`（巨觀架構）→ `/rsun-architect`（單模組 variant）→ `/rsun-adr`（記決策）→ `/rsun-estimate`（出價）。

---

## 常見錯誤與避免

| 錯誤 | 為什麼錯 | 正解 |
|------|---------|------|
| 寫一份「萬用 rsun-crm」塞給所有客戶 | 違反權變理論 | 必選一個 client_id 寫 variant |
| 借鑑 8 個 repo 但變數名亂混 | 違反命名統一原則 | 走 cluster brief 的 naming_divergence 段，挑一個容晟版 |
| 用 Gemini Flash 寫藍圖然後 Opus 微調 | 浪費這 skill | Opus 親寫，原料才是 Flash 萃的 |
| 跳過 Step 9（不適用情境）| 失去自我邊界意識 | 強制寫，至少 1 條 |
| WBS 拍腦袋 | 不可估價 | 每個工作包對齊容晟 WBS 標準（複雜度 S/M/L/XL） |
