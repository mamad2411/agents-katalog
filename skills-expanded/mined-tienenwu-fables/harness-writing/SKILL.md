---
name: harness-writing
description: Use when creating, regenerating, or auditing a repository-specific development harness, contract system, risk router, evidence gate, or project workflow policy.
---

> 🌐 [English version](https://github.com/tienenwu/fables/blob/main/en/harness-writing/SKILL.md) · 繁體中文（正本 / canonical）

# Harness Writing — 生成專案專屬的證據驅動流程

## 核心模型

Harness 是唯一的 orchestration kernel：always-on kernel 只保留路由與不變量，standard／high-risk 細節按需載入；狀態轉移靠風險條件與 claim→evidence 閘門，證據不等於每次都要落 repository artifact。profile 選擇所需狀態；adapter 描述環境能力；契約保存專案判準；domain playbook 提供階段內技術方法。

不變核心不重造，專案參數不杜撰。檔案數只能當輔助訊號；主要依可逆性、爆炸半徑、歧義、外部副作用與可驗證性路由。

## 何時用

- 新專案需要 Harness、契約索引與機械檢查基線。
- 既有專案要導入或重新校準 AI 開發流程。
- 稽核現有 Harness 是否有雙真相、假證據、過度審查或契約污染。
- 不適用：只新增一條已確定的專案契約；直接依既有生命週期修改。

## 生成流程

### 1. 探勘（唯讀）

- 盤點目錄、CI、既有規範、架構整合點、公開介面、正式資源與 release 路徑。
- build/test/lint 指令先判斷副作用；安全者各實跑一次，記耗時、輸出與基線失敗。不確定是否寫正式資源就不跑並明記。
- 盤點能力而非產品名：能否隔離寫入、執行 shell、跑測試、啟動 fresh reviewer、保留 artifact、取得第二模型家族。
- 從真實專案推導 quick 的全部必要條件與 high-risk 絕對升級條件；不以數字加總製造假精確，查無就寫「無」。
- 已有 harness 時修改它，不重新生成第二套。

### 2. 生成 Kernel／Profiles／Adapters

完整讀 `harness-core-template.md` 並填完所有 `{{SLOT}}`。以下不變量不得默刪：

1. 契約先行與指令優先序。
2. 機械檢查先於 AI review。
3. PASS 必須附 claim→evidence；reviewer 自述不是證據。
4. 只在高成本歧義、不可逆選擇或外部副作用消耗使用者注意力。
5. 回歸基線與範圍檢查。
6. 契約 `candidate → active → hardened → deprecated` 生命週期。
7. 無法取得獨立 reviewer 時誠實降級，不假裝雙審。
8. 審查收斂：blocking 才觸發重審；複審延續前輪 reviewer 只裁 delta；已 PASS 且 evidence 未變的 claim 不得重開；迴圈上限兩輪後升級使用者。
9. 證據持久化按 profile 分級：quick 預設只在回覆附證據；standard 有 handoff／稽核／跨 session／residual risk 才落檔；high-risk 完整落檔。
10. 平行化準備只在 plan 有兩個以上工作包時啟用：明列 dependency、writable scope、validation、handoff 與 integration owner；shared contract 未固定或寫入範圍重疊者序列化，quick 不為此增加 artifact。

覺得某項不適用時，在生成報告列出理由交給使用者裁決。

參數先寫成 JSON，再用 `scripts/render_harness.py --template harness-core-template.md --config <config.json> --output <target-repo>` 產生三個 artifact。renderer 只保證欄位完整、slot 全數解析與不覆寫既有檔案；參數真實性仍必須由探勘證據證明。

### 3. 初始契約

- 現有明文規則可建為 `active`；必須附來源與測驗／檢查。
- 從程式碼慣例歸納的規則只能建為 `candidate`，不可因一次觀察直接生效。
- 新專案只建索引、schema 與維護規則；不塞想像中的最佳實務。
- contract candidate 只由使用者糾正、再次觀察、incident／escaped defect、未文件化的重複限制或推翻既有契約的證據觸發；沒有事件就不建立空檔。
- `candidate` 只有在再次觀察、使用者明確裁決或明確事故證據下升 `active`；能低成本機械化再升 `hardened`。

### 4. 接線

- 產出 `.claude/skills/harness/SKILL.md`、`references/pipelines.md` 與 `docs/contracts/README.md`。
- 專案規範只接到 Harness 這個 orchestration 入口；`feature-flow` 等 process skill 作為 profile／階段策略，不建立第二狀態機。
- 需要持久化的產出統一落在 `docs/plans/<slug>/`；quick 預設無 repository artifact。既有路徑可保留相容入口，但必須指定單一 canonical source。

### 5. 驗證交付

- 用 quick、standard、high-risk 各一個情境冒煙路由，核對 quick 零強制落檔、standard 條件式持久化與 high-risk 完整證據。
- 對 renderer 產物執行 `rg '\{\{[^}]+\}\}' .claude/skills/harness docs/contracts`；任何殘留 slot 都阻擋交付。
- 驗證所有機械命令安全且可跑，adapter 沒引用不存在的能力。
- 有獨立 reviewer 能力時：standard 只有在昂貴歧義、shared contract、廣泛 diff 或驗證缺口才加 semantic；high-risk 對實際命中的風險面加 adversarial。沒有時以 fresh read-back／實跑補足並列出限制。
- 交付：檔案清單、探勘證據、基線、risk router、adapter 能力、初始契約狀態、未驗證項目。

## 紅線

- ❌ 用檔案數當唯一風險判準；單檔 migration 仍可能是 high-risk。
- ❌ 兩個相同 prompt／相同證據路徑就宣稱獨立雙審；相關錯誤不會因票數消失。
- ❌ 只有 PASS/REJECT、沒有 claim→evidence 的 verdict。
- ❌ 把「需要 evidence」誤寫成「每個 quick task 都必須建立 evidence.md」。
- ❌ 把一次性現象直接寫成 active 契約。
- ❌ 為了遵守流程同時保留 Harness 與另一套完整 process source of truth。

## references 索引

- `harness-core-template.md`：生成前全文讀取；不可只靠本檔摘要自行重建。
- `references/evaluation-protocol.md`：換模型、校準路由或評估流程成本／成效時讀。
- `references/evaluation-scenarios.json`：行為 gate 的 canonical scenario ID／★ mapping。
- `references/test-scenarios.md`：換模型、修改 risk router／evidence／契約生命週期後，以 fresh session 回歸。
- `scripts/render_harness.py`：驗證 slot 並安全產生三個 canonical artifact。
- `scripts/evaluate_runs.py`：驗證 JSONL 行為紀錄、彙總成效指標並執行 gate。
