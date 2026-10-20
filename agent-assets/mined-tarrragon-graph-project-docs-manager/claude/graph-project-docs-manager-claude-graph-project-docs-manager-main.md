# CLAUDE.md

本文件為 Claude Code 在此專案中的開發指導規範。

---

## 0. Behavioral Core Principle

This Claude framework passes information through the ticket system. The reader of any
output or conversation is not necessarily a human — it is often the next session or
another agent. Therefore:

- Do not apologize, praise, encourage, or re-confirm information that is already known.
- When writing code or documentation, do not make assumptions beyond the task at hand.
- If something needs further analysis or adjustment, open a ticket and hand it to the
  next session or agent instead of expanding the current scope.
- Avoid reasoning or complexity that exceeds what the ticket requires.

---

## 1. 專案身份

**專案名稱**: graph_project_docs_manager（專案文件流）

**專案目標**: 專案文件的管理與視覺化。定位近似 Jira / Asana / Trello，
但管理對象不是任務看板，而是文件之間的**因果鏈與型別化邊**
（`PROP → SPEC → UC → Ticket`）。核心價值在於把目前散落於 markdown
frontmatter、只能靠 grep 與人工追溯的關係顯性化、可導航、可視覺化。

**專案類型**: Flutter（macOS 桌面應用程式）

| 項目 | 值 |
|------|------|
| **語言** | Flutter 3.47.1 / Dart 3.13.1（由 FVM 釘選，見 `.fvmrc`） |
| **實作代理人** | parsley-flutter-developer |
| **識別特徵** | `pubspec.yaml`、`.fvmrc` |
| **目標平台** | macOS 12.0+（前期僅此平台；ios/android/linux/windows 目錄保留未啟用） |
| **發布通路** | Developer ID + notarization，**不上架 Mac App Store** |

**啟用的 MCP/Plugin**:

- codegraph - 程式碼知識圖譜
- serena - 語意程式碼操作
- context7 - 套件文件查詢
- github - repo 操作
- zhtw-mcp - 繁體中文用字檢查

**常駐操作授權**：`git push origin main` 已由用戶授權，**不需逐次徵詢**（2026-09-07 裁示）。

授權理由與範圍：worktree 派發守衛（`worktree-commit-before-dispatch-hook.py`）要求目標票的
md 已在 `origin/main`，否則硬擋——逐次徵詢會使每一次 worktree 派發都變成一次中斷。授權範圍
限本專案 `origin/main` 的常規推送；**force push、推送其他 remote、推送非 main 分支仍須確認**。

框架資產的 `sync-push`（推 `tarrragon/claude`）與 `skill-sync push`（推發佈庫）**不在此授權內**
——那兩者影響其他 consumer 專案，屬跨專案動作。

**框架 issue 的觀測與建立**（`section_comment.py` 的 `observe` / `init` / `add` / `update` 自有區段，
含前置的 `dedup` / `show` / `check` / `todo`）已由用戶授權，**不需逐次徵詢**（2026-09-09 裁示）。

生效條件兩項，缺一即回到逐次徵詢：(1) 框架問題的兩條 AND 判準（抽象可攜 + 根源在 `.claude/`
通用資產，見 `.claude/skills/framework-issue/references/escalation-flow.md`）**已在票面逐條套過**，
不是憑印象；(2) **已跑 `dedup`** 且關係判定（重複／切分／引用）有記錄。

授權理由：框架缺陷存在於每一個 consumer 專案，逐次徵詢會使發現停在本地，而本地修會被下次
`sync-pull` 以上游舊版覆蓋且無 canonical 記錄。判準客觀可查，且 observe 可刪。

**本專案是 `component-contract-design` skill 的開發上游**（2026-09-29 用戶裁示）。其他 consumer 回報該 skill 的條文缺口時，除了觀測 canonical issue，也須在 active 版本建實作票、在本專案修正。完成後 sync-push 到 canonical；推送 skill 發佈庫（`skill-sync push`）仍需逐次授權。

**目前由本專案擔任 `.claude/` 框架的主控方**（2026-10-13 用戶裁示，首例：flutter_balance 回報的逾時孤兒 `flutter_tester`）。
這是現行安排，不是固定角色：主控方由用戶指定，日後可改由其他專案擔任，改派時以用戶的新裁示為準並更新本段。
現行安排下，其他 consumer 只開 framework issue，不改框架內容；只有涉及 SKILL 的部分，才由該 consumer 自己推送 SKILL 更新。
分析、修法與 `.claude/` 實作在主控方由用戶指定的 session 負責。
理由：同一時間只有一個主控方，避免各 consumer 各自修改框架而分叉。

**仍不在授權內**：`sync-push` 與 `skill-sync push`（同上段理由，那是改資產本體不是留一則可刪的觀測）、
改他人 owner 的區段或 issue body、其他 remote 與其他 repo、以 `create_issue.py` 新開 issue
（上段「建立」指 `init`／`add` 建立區段 comment，不含新開 issue；新開須逐次授權，例：#111）。

---

## 2. 核心價值

@.claude/rules/core/quality-baseline.md

---

## 3. 規則系統

@.claude/rules/README.md

---

## 4. Skill 指令

可用 skill 由平台在 session 啟動時列出（含名稱與用途描述）。專案自訂的指令對照表與分類見 `.claude/pm-rules/skill-index.md`，需要依分類查找或確認某指令是否存在時 Read。

---

## 5. 方法論參考

方法論索引見 `.claude/pm-rules/methodology-index.md`（按需 Read）。該檔為查表用途——尋找特定主題的方法論、或確認某方法論是否已存在時才需讀取，非每回合必需。

---

## 6. 技術選型與架構決策

已定案項目（v0.1.0 基礎架構）：

| 面向 | 選擇 | 理由 |
|------|------|------|
| Flutter 版本管理 | FVM 釘選 3.47.1 | 釘具體版號而非 channel，確保跨機器與 CI 行為一致 |
| 尺寸系統 | `flutter_screenutil`，設計基準 1280×800 | 等同預設視窗尺寸，開發時所見即 1:1 |
| 防跑版主力 | macOS `minSize` 960×640 + 約束式佈局 | ScreenUtil 只做等比縮放，**不**阻止 overflow |
| 多語系 | Flutter 官方 ARB，繁中為樣板語系 | 生成產物 `lib/l10n/app_localizations*.dart` 刻意入庫 |
| 檔案存取 | **App Sandbox 關閉** | 開發者工具需執行專案內 doc CLI；實測沙盒下 python3 被 xcrun shim 拒絕、使用者安裝 binary 為 Operation not permitted |
| 測試策略 | 雙層（`test/` 契約 + `integration_test/` 行為） | 內層針對「改錯無編譯期徵兆」的跨語言常數 |

**已補完的原待決項**：schema 消費方式定為讀 `tracking_schema.json`（PROP-002）；
security-scoped bookmark 實作已移除（PROP-001）；狀態管理定為 Riverpod、
矩陣渲染委派 `two_dimensional_scrollables`、持久化為路徑字串
（`docs/tech-decisions.md` 的補記段「2026-08-26：Stage 4 技術維度定案」；
注意該檔另有一個編號不同的 `## 4. 資料來源`，兩者不是同一處）。

**執行期 log 已裁決**（W1-013，補記段「2026-08-27：執行期 log 的裁決」）：
structured log 維持延後（重評條件與 tripwire 不變）；但全域錯誤攔截三層不在延後
範圍，須立即建立（W1-016）。**錯誤的載體是畫面不是檔案**——App 層失敗轉為
SPEC-001 既有的阻擋狀態或損壞標記。原待決記「Stage 5 明示不寫」是轉述失真，
原文為「延後」且附重評條件，兩者決策語意不同。

**`tracking_schema.json` 缺席的下界策略已定案為降級**（W1-035，補記段
「2026-09-03：型別表缺席時降級而非拒絕」）：「無可消費的型別表」為顯式關卡不自動降級，
使用者按「以 App 內建型別表檢視」後以 build 內嵌的 JSON 副本解析，六畫面皆可進入，
只渲染 established 12 條邊、每畫面常駐降級徽章；`VERSION` 高於內建表產生版本時不提供。
規格在 SPEC-001 v1.5 §1 與 SPEC-003 v1.7 §3.1／§5。

**跨邊界驗證是正交屬性，不是新測試層**（W3-081，補記段「2026-09-08：跨邊界驗證形態
定案，本專案三呼叫點現況盤點」）：`測試策略`列的雙層（`test/` 契約 + `integration_test/`
行為）描述自動化分層基礎設施，本身不變——本專案三個跨邊界呼叫點（`MacosScanNotifier`／
`WorkspaceRepository`／`gap_report_screen._openItem`）的 App 端邏輯軌本就落在這兩層
之內，未新增第三層；但三者的平台端事實軌（實機驗證）全數零覆蓋，且僅
`MacosScanNotifier` 有承接票（`0.1.0-W3-078`），另兩處尚待 PM 裁決是否開票。

**改 schema 匯出的框架票之合併閘門**：同批同步內嵌副本、合併前跑 `test/unit/schema`，見 `docs/tech-decisions.md` 補記段「2026-10-12 — 改 schema 匯出的框架票之合併閘門」。

**現行待決**（每一項都是版本規劃的前置，見 `docs/system-layer.md` §6 與各 `docs/spec/{domain}/domain-map.md` §6）：

- **UC → Ticket 在上游 17 條語意邊中無對應邊**。追溯視圖（UC-04）承諾的
  四層鏈，第三跳沒有資料來源
- **Domain 視圖的列**：2026-10-06 用戶裁決列取 `DomainBundle` 節點，`0.5.0-W1-070.3` 已把
  單檔 domain-map 拆為每個 domain 一份 `docs/spec/{domain}/domain-map.md`（跨 domain 內容在
  `docs/system-layer.md`）。格的來源已定案（`0.1.0-W3-341`，經 WRAP
  改定，2026-09-14）：`FlowStep` 新增 `traverses` 欄位——步驟直接觸及的 domain
  清單（0..n，欄位必存在，純畫面步驟為空），對應系統層 §1.4「貫穿」；
  事件推導類覆蓋率均低於 21% 已排除。schema 修改由 `0.1.0-W3-346` 在本專案
  直接進行，回填前須先補 domain-map 兩處缺口（`0.1.0-W3-347`）
- 空殼判準：「破洞分類」「預估耗時」「資源上限」（「App 已知範圍」已於
  2026-09-23 定案為「JSON 產生版本不高於 App 內建版本」，見 `docs/spec/schema/domain-map.md` §6；規格追修由
  `0.2.0-W1-040` 承接；「間接依賴」已於 2026-10-07 定案為沿依賴邊往下游不限跳數可達，見 `docs/system-layer.md` §6）
  （「預估耗時」欄的去留候選已收束於 `docs/system-layer.md` §6）
- 泳道布局演算法已定案（2026-10-07 用戶裁決）：列依分層固定 8 列、主線依 `next` 而分支插起點後、
  前向直線與回指弧線、純畫面步驟另立「畫面」列；見 `docs/spec/layout/domain-map.md` §6
- domain 名稱權威寫法已定案（2026-10-07 用戶裁決）：以 `DomainBundle` 的 `domain` 為準（小寫加連字號，
  受 id_pattern 約束）；`traverses` 改寫為宣告字面（`0.5.0-W1-090`），`doc validate` 檢查
  `traverses` 與 `depends_on_domains` 的值必須已宣告（`0.5.0-W1-091`）；App 精確比對。列首顯示 `domain` 原值，
  只有「畫面」列（`presentation`，App 自身詞彙）走 i18n（2026-10-08 用戶裁決，`0.5.0-W1-106`，取代原「顯示名由 i18n 取」）
- 跨畫面「首次可見／再次可見」生命週期偵測基礎設施未設計（SPEC-003 §3.5
  再次可見自動重掃，見 `docs/system-layer.md` §6）
- 編輯能力與 git 邊層級歷史已定案但未落為提案與規格；編輯能力落為規格前的
  四項子決策（規格檔路徑指名、寫入前閘門判準、structured log 延後理由重估、
  樂觀更新可觀測時刻）已收束於 `docs/system-layer.md` §6，trigger 為 `1.0.0-W3-553`（1.0 規劃票）
- 0.1 之後的版號規則與 wave 切法

---

## 7. 專案文件

### 任務追蹤

| 文件 | 用途 |
|------|------|
| `docs/todolist.yaml` | 結構化版本索引（Source of Truth） |
| `docs/work-logs/` | 版本工作日誌 |
| `CHANGELOG.md` | 版本變更記錄（**尚未建立**） |
| `docs/work-logs/v{version}/tickets/` | Ticket 文件 |

### 專案文件

> **與 README.md 的分工**：README 面向人類維護者（環境設定、常用指令、
> 專案結構），本檔面向 AI（行為規範、決策脈絡、規則路由）。目的與格式
> 不同，內容重疊屬正常，**不需要對齊或互相涵蓋**。審查時若被報為
> 「兩份索引不對稱」，那是誤判。

| 文件 | 用途 | 現況 |
|------|------|------|
| `docs/proposals/` | PROP 節點 | PROP-001~004，皆 confirmed |
| `docs/spec/{domain}/` | SPEC 節點 | SPEC-001（ui domain） |
| `docs/spec/{domain}/domain-map.md` | DomainBundle 節點，每個 domain 一份（8 個 domain 各一） | 已建立 |
| `docs/system-layer.md` | 系統層：跨 domain 的依賴方向、通道、邊界決策、容錯、待決（非圖節點） | 已建立 |
| `docs/usecases/` | UC 節點（含結構化 flow 區塊） | UC-01~06（FlowStep 數以各 UC 的 flow 區塊為準，不在此寫死） |
| `docs/events/{domain}/` | EVT 節點 | 9 個 |
| `docs/app-use-cases.md` | UC 白名單 SSOT（`doc uc verify` 依此驗證） | 已建立 |
| `docs/proposals-tracking.yaml` | 提案索引 | 已建立 |
| `docs/tech-decisions.md` | 設計決策記錄（append-only，以最後的補記為準） | 已建立 |
| `docs/traceability.yaml` | 四軸追溯矩陣（mappings／domain_bundle_tests／data_contract_tests／runtime_tests，schema 見 `tracking_schema.py`） | 已建立，回填現況與已知缺口見 `0.1.0-W3-076` Solution |

### 上游 schema（唯一權威，禁止另建副本）

`.claude/skills/doc/doc_system/core/tracking_schema.py`
— `GRAPH_NODE_TYPES`（7）、`GRAPH_EDGE_TYPES`（17，established 12 / proposed 5）

三項語意約定：

1. `layer` 是穩定性承諾而非開發進度（`established` 可依賴 / `proposed` 形狀可能變動）。
2. `relatedTo` 語意對稱但儲存單向（`reverse_field: None`），消費端**必須**做
   1-hop symmetric union，只讀單向會漏掉一半的邊。
3. `spawned_tickets` / `children` / `blockedBy` / `relatedTo` 語意不同，
   依 `class` 欄位分層渲染，不可合併。

---

## 8. 里程碑


版本以 `docs/todolist.yaml` 為準。版本可以預先登記：major 起始時規劃其下
固定的 minor 清單（各解決哪些 SPEC），minor 完成後分診一次、依 topic 定下固定
數量的 patch。**不在任何已規劃版本內的項目，須經討論後明確決定延後**，
不以版本標籤代替討論（2026-09-29 決策，見 `docs/tech-decisions.md`）。

| 版本 | 內容 | 狀態 |
|------|------|------|
| 0.0.1 Foundation | macOS 桌面基礎架構、FVM 釘選、雙層測試、多語系 | 完成 |
| 0.0.2 Intake | 設計與選型訪談，產出 PROP×4 / SPEC-001 / UC×6 / 8 domain / EVT×9 | 完成 |
| 0.0.3 Toolkit | markdown 渲染、編輯模型、git 變更記錄三項選型 | ticket 全完成 |

發布通路為 **Developer ID + notarization，不上架 Mac App Store**（PROP-001，
能力決策：沙盒下無法執行 doc CLI 亦無法讀取任意資料夾）。

---

*專案入口文件 - 詳細規則請參考 .claude/rules/ 目錄*

<!--
使用說明：
1. 將此範本複製到專案根目錄
2. 重命名為 CLAUDE.md
3. 填入專案特定資訊（標記 <!-- --> 的區塊）
4. Section 2-5 使用 @ 引用自動載入通用規則
5. 只需客製化 Section 1/6/7/8
6. 驗證所有連結有效
-->
