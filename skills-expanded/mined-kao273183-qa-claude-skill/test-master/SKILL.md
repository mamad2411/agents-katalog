---
name: test-master
description: 一鍵生成完整測試計劃、測試用例和自動化策略的綜合測試工程師 Skill。生成黑箱/白箱測試用例（Excel）、測試策略、覆蓋缺口分析、自動化路線圖和探索性測試指引。當使用者提到「生成測試計劃」、「設計測試」、「完整測試方案」、「測試用例設計」、「寫測試案例」、「test plan」，或需要為新功能、重構、Bug 修復、Release 規劃測試策略時使用此 skill。即使使用者只是模糊地說「幫我測一下這個功能」或「這個需要什麼測試」，也應觸發。
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Write, Edit, Bash, mcp__atlassian__getJiraIssue, mcp__atlassian__searchJiraIssuesUsingJql, mcp__google__createSpreadsheet, mcp__google__writeSpreadsheet, mcp__google__copyFile, mcp__google__moveFile, mcp__google__createFolder, mcp__google__getSpreadsheetInfo
argument-hint: "[JIRA票號 或 功能描述]"
---

# test-master

> ⚙️ **執行前先讀 [`modules/config-loader.md`](./modules/config-loader.md)**，載入組織設定。
> 若 `config.json` 不存在或 `mode = markdown-only`，跳過 MCP 並走 [`modules/markdown-fallback.md`](./modules/markdown-fallback.md)。

## 執行流程

### Phase 1: 需求分析
1. **讀取需求** — JIRA 票號（如 `{{JIRA_PROJECT_KEY}}-XXXX`）用 Atlassian MCP 抓取，否則請使用者描述
2. **JIRA 描述完整性檢查** — description 為空的票號標記為風險
3. **平台偵測** — 自動偵測涵蓋哪些平台：
   - iOS：`*.xcodeproj` / `Package.swift` → 用 `{{IOS_REPO}}`
   - Android：`build.gradle(.kts)` → 用 `{{ANDROID_REPO}}`
   - Web：`package.json` / `next.config.*` / `vite.config.*` / `webpack.config.*` → 用 `{{WEB_REPO}}`（若 `platforms.web.enabled = true`）
   - Flutter：`pubspec.yaml` → 切換到 `flutter-test-master` skill
4. **分析影響範圍** — 搜尋相關程式碼（Glob/Grep）：
   - 識別 ViewModel / Repository / Service / API / SDK 依賴
   - Web 額外識別：React/Vue/Angular component / route / Redux store
5. **風險評估** — 金流/敏感資料/認證（高）、並發/記憶體/網路（技術）、關鍵流程/UX（業務）

### Phase 2: 測試策略設計
生成 `test-strategy.md`。模板見 [`templates.md`](./templates.md)「test-strategy.md 模板」。

### Phase 3: 測試用例生成
生成黑箱 + 白箱兩份 Google Sheet（從模板複製，模板 ID = `{{GSHEET_TC_TEMPLATE_ID}}`）。

> 若 `{{GSHEET_TC_TEMPLATE_ID}}` 為空 → 直接 `createSpreadsheet` 並建立預設欄位結構。
> 若 `mode = markdown-only` → 改產出 `test-cases-{feature}-{blackbox|whitebox}.md`，沿用相同欄位（A-N）。

**黑箱 / 白箱判定原則（分類鐵律）：**
- **黑箱（BB）**：前置條件、步驟都必須是一般使用者看得懂、操作得到的，不需要任何第三方工具查看或測試（不用 Postman/curl/adb/Charles/mitmproxy/Instruments/Xcode Debug/資料庫直查/log 檢視等）。
- **白箱（WB）**：只要是 API 相關測試，或需要用到第三方工具才能執行/驗證的，都歸類白箱，前置條件跟步驟要明確寫出用什麼工具測試。
- 判定順序：先問「一般使用者不靠任何工具，照著步驟能不能重現、看得懂前置條件？」——能 → 黑箱；不能 → 白箱。這條標準跟 spec 內容脫鉚，spec 中途修正只需調整對應 TC 內容，不用重判既有 TC 的黑白箱歸屬。

**測試分類（Column F）反漂移規則：**
- 寫入「測試分類」欄的值**只能用 `config.test_case_format.categories`（black_box/white_box 兩個固定清單）**，或目標既有 Sheet 現有出現過的分類值，**不可自行發明新分類名稱**（就算聽起來很合理，例如「效能測試」「相容性測試」）。
- 新 TC 場景要先嘗試映射到最接近的既有分類，映射不上才能算是真的缺分類。
- 真的判斷需要新分類：**先跟使用者確認**，確認後才能同步更新 config 的固定清單 *和* 目標 Sheet `status` tab 的統計公式（新增對應統計列），否則新分類的 Pass/Fail 數字會被 status tab 的公式漏算而不自知。
- 每次要寫入既有 Sheet 前，先讀該 Sheet 的「測試分類」欄現有值當這次的有效範圍，不要只信 config（不同 Sheet 可能歷史上已經各自漂移，要先掌握現況再決定要不要一起清理）。

**測試用例分佈：**
- 正常路徑 20% / 邊界條件 30% / 錯誤處理 30% / 並發 10% / 非功能性 10%

**依功能類型自動調整重點：**
- API 整合 → 網路錯誤、逾時、401/403/500、JSON 解析，以及**資安必檢 9 類**（見下）
- UI 功能 → 載入/錯誤/空白狀態、螢幕尺寸、**a11y（見下）**
- 資料同步 → 並發寫入、race condition、Thread Sanitizer
- IM/即時通訊 → 斷線重連、離線同步、多裝置
- **Web 應用** → 跨瀏覽器（Chrome/Safari/Firefox/Edge）、SSR/CSR、SEO、Cookie/Session、CORS、Visual Regression
- **CRUD/管理後台**（CMS 設定頁、任何「新增/查詢/編輯/刪除」介面）→ **Create/Read/Update/Delete 四操作各自別列案例，不能只測 Create 或假設 Edit 是 Create 的子集**；Read 涵蓋篩選/排序/分頁/空狀態；Update 需注意欄位唯讀規則跟 Create 是否不同、改動中的資料是否影響已在使用中的其他資源；Delete 需含被引用中資料的處理、軟刪除 vs 硬刪除邊界
- **Android 專屬** → **分割畫面（split-screen）多工模式必測**：進入/退出過程 + 已在分割畫面下的畫面載入與操作，不能只用「螢幕尺寸」的 static responsive 檢查取代（分割畫面會觸發 `onMultiWindowModeChanged`/resize/reconfiguration，容易暴露 lifecycle 相關 bug，範例：UOP-7890 健康首頁分割畫面下持續載入失敗）。iOS 無對應系統級分割畫面模式，此項僅適用 Android。
- **涉及日期/時間欄位**（打卡、步數同步、連續型挑戰、趨勢圖表、任何有「跨日/跨週/跨月」結算邊界的功能）→ **時區處理必列案例**：① 伺服器儲存（通常 UTC）/ API 回傳格式 / App 顯示時區三層轉換是否一致，別只驗證單一層；② 跨日/跨週/跨月邊界時刻用哪個時區判定（00:00 裝置時區 vs 00:00 台北時區 vs UTC 午夜三者常不一致）；③ 使用者切換裝置時區是否影響已有紀錄或視為作弊；④ 寫入端跟查詢端時區是否一致（例：DB 寫入 GMT+0、查詢端假設 GMT+8 造成資料看起來「消失」或「跑到隔天」）。這類 bug 常態是「資料本身沒錯，只是顯示/比對時少轉一次時區」，斷言時要明確寫出預期時區，不要用裝置當下時區含糊比對（範例：健康連續型挑戰跨日重置時機定義未明、血壓趨勢 `date` 欄位格式與時區不一致、集章門市同步 GMT+0/GMT+8 DB 落差 WB-STAMP-W020）。

**Web 平台特有測試類型**（若 `platforms.web.enabled = true`）：

| 類型 | 對應框架 | 範例 |
|------|---------|------|
| E2E UI Test | `{{WEB_PRIMARY_FRAMEWORK}}` (預設 Playwright) | 登入流程、購物車、表單驗證 |
| Component Test | Playwright Component / Cypress Component | React/Vue 元件獨立測試 |
| Visual Regression | Playwright snapshot / Percy / Chromatic | 截圖比對找視覺改變 |
| Cross-browser | Playwright 多 project | Chrome / Safari / Firefox / Edge |
| Responsive | viewport 切換 | desktop 1920×1080 / tablet 768×1024 / mobile 375×667 |
| API 黑盒（in E2E）| Playwright `request` / Cypress `cy.request` | UI test 中順便驗 API 行為 |

**a11y（輔助功能）必檢項目** — 每個 UI 功能都要加：
- **字級縮放**：iOS Dynamic Type 最大 / Android 字型最大 / Android 顯示大小最大
  - 內容文字應跟隨放大但不破版
  - **裝飾性數字（計數、徽章）不應跟隨放大**
- **螢幕閱讀器**：VoiceOver（iOS）/ TalkBack（Android）讀取順序與 label
- **觸控目標**：iOS ≥ 44×44 pt / Android ≥ 48×48 dp
- **對比度**：文字 vs 背景 ≥ 4.5:1（深色模式也要驗）
- **Reduce Motion**：動畫減少模式正常
- 詳細檢查模板見 [`templates.md`](./templates.md)「a11y-checklist 模板」

**資安必檢 9 類** — 有 API、會寫入資料、有登入或角色的功能都要逐類判斷（2026-11-23 加；跟 `speckit-to-tc` 的「資安必檢 9 類」同一份）。適用就至少寫 1 條白箱 TC，不適用就在 test-strategy.md 的風險段落寫一行原因，不可以默默跳過；只寫「沒登入回 401」不算完成。

| # | 類別 | 適用時機 | 要驗什麼 |
|---|---|---|---|
| 1 | 認證 | 需要登入的 API | 不帶、過期、竄改的 token／cookie → 401，沒有讀寫到資料 |
| 2 | 水平越權（IDOR） | 參數有資源 id、會員識別碼、訂單編號 | A 帳號帶 B 的 id 讀、改、刪 → 拒絕，不能 200；列表改篩選也撈不到別人的資料（要兩個測試帳號） |
| 3 | 垂直越權 | 後台有角色，或 API 只給特定角色 | 低權限角色直接打寫入、管理 API → 403（前端藏按鈕不算數） |
| 4 | 同時送出 | 一次性或有上限的動作：兌換、領取、集點、核銷、扣款、扣庫存 | 同一請求同時送 10～20 次 → 只成功 1 次、不超扣、不重複；跟「用過再送被擋」是不同測試 |
| 5 | 輸入注入 | 查詢、篩選、排序、搜尋參數 | SQL 片段、NoSQL 運算子、超長字串、控制字元 → 4xx，不能 500、不帶內部細節 |
| 6 | 儲存型 XSS | 一端寫入、另一端顯示的自由文字或 HTML | `<script>`、`<img onerror>`、`javascript:` 連結被清掉或照文字顯示；寫入端、顯示端都驗 |
| 7 | 檔案上傳與匯出 | 上傳圖片、Excel、CSV，或匯出檔案 | 內容跟副檔名不符、超過上限、檔名含 `../`、儲存格以 `=` `+` `-` `@` 開頭 → 被擋或安全處理 |
| 8 | 敏感資料外洩 | 回應、錯誤訊息、匯出檔帶個資或憑證 | 不回密碼、token；個資照規格遮罩；錯誤訊息不帶內部細節 |
| 9 | 繞過前端限制 | 前端擋的上限、負數、跳步驟 | 直接打 API → 後端也擋 |

- 分類欄不新增「資安測試」：第 4 類寫「並發安全測試」，其他寫「API 驗證測試」（黑箱寫「異常/邊界測試」），備註欄標 `資安：越權` 這類標記。
- 規格沒寫的狀態碼不要定死，寫「拒絕（4xx），不能 200 或 500，資料沒有外洩或被改」。
- 只在 dev／UAT 用測試帳號跑，不碰正式站；同時送出保持小量，不做壓力測試。

**優先級判斷：**
- P0: 核心業務流程（登入/支付/訂單）、資料安全（含資安必檢第 2、3、4、8 類牽涉金額、點數、庫存、個資者）、高 crash 風險
- P1: 主要功能、高頻場景、錯誤處理、**a11y 跑版**
- P2: 次要功能、邊界條件、非功能性需求

**跨平台 a11y 配對原則**（若 `workflow.auto_a11y_pairing = true`）：開 a11y 類 bug/優化單時，**預設開一對**（iOS + Android），用 Relates 連結。

**Google Sheet 格式** — 遵循 `config.test_case_format` 中設定的 A-N 欄位結構與分類。預設欄位：

| 欄 | 內容 |
|----|------|
| A | ID（`BB-` 黑箱 / `WB-` 白箱 前綴） |
| B | Phase |
| C | 測試結果 |
| D | 測試結論 |
| E | 測試標題 |
| F | 測試分類 |
| G | 優先度（P0/P1/P2） |
| H | 平台（iOS/Android/Both） |
| I | 前置條件 |
| J | 測試步驟 |
| K | 預期結果 |
| L | 自動化（Y/N） |
| M | 備註 |
| N | JIRA Ticket |

### Phase 4: 測試覆蓋缺口分析
搜尋既有測試：
- iOS：`*Tests.swift` 或 `*Test.swift`
- Android：`*Test.kt` 或 `*Tests.kt`
- Web：`*.spec.{ts,js}` / `*.test.{ts,js}` / `e2e/**/*.spec.*` / `cypress/e2e/**`
- Component test：`*.stories.{ts,js}` 旁的 `*.test.tsx`

比對新增用例 vs 現有測試，識別缺口。模板見 [`templates.md`](./templates.md)「coverage-gaps.md 模板」。

### Phase 5: 自動化評估
評估標準：重複頻率、執行時間、複雜度、穩定性、ROI。模板見 [`templates.md`](./templates.md)「automation-plan.md 模板」。

### Phase 6: 探索性測試指引
模板見 [`templates.md`](./templates.md)「exploratory-guide.md 模板」。

### Phase 7: Google Drive 上傳
> 僅在 `mode != markdown-only` 且 `google.qa_tc_folder_id` 已設定時執行。

1. 在 QA-TC 資料夾（`{{GDRIVE_QA_FOLDER_ID}}`）下建立 feature 子資料夾
2. 上傳黑箱/白箱 Google Sheet 到該資料夾
3. 詢問是否上傳其他文件（test-strategy.md、coverage-gaps.md 等）

> 若 `google.default_drive = shared` 且 MCP 無法直寫共用硬碟，提示使用者「請手動將 Sheet 移至 `{{GDRIVE_QA_FOLDER_ID}}`」。

## 輸出檔案

```
.claude/testing/features/[feature-name]/
├── test-strategy.md
├── test-cases-{feature}-blackbox.xlsx  (Google Sheet)
├── test-cases-{feature}-whitebox.xlsx  (Google Sheet)
├── coverage-gaps.md
├── automation-plan.md
└── exploratory-guide.md
```

> Markdown-only 模式下，Sheet 改為同名 `.md` 檔。

## 互動模式

- **基礎模式（預設）**：生成所有文件
- **快速模式** `--mode=quick`：只生成測試用例 Sheet
- **深度模式** `--mode=deep`：完整文件 + Mock/Stub 程式碼範例

## 品質檢查

生成後自動驗證：
- [ ] Happy Path + 邊界條件 (>=3) + 錯誤處理 (>=5) + 並發 + 生命週期
- [ ] 測試金字塔比例合理（70% Unit / 20% Integration / 10% UI）
- [ ] 風險矩陣涵蓋所有高風險項目
- [ ] ROI 計算包含維護成本和 Flaky test 風險
- [ ] 雙平台（iOS + Android）實作差異已分析
- [ ] 覆蓋缺口含雙平台現有測試比對
- [ ] CRUD 型功能已確認 Create/Read/Update/Delete 四操作均有對應案例（不能只有 Create）
- [ ] 資安必檢 9 類都判斷過：適用的有 TC（不能只有「沒登入回 401」），不適用的有寫原因
- [ ] 涉及日期/時間欄位的功能已檢查時區一致性（UTC 儲存 / API 回傳 / 裝置顯示三層轉換 + 跨日跨週跨月邊界時區定義），斷言明確寫出預期時區

## 後續動作

完成後詢問：
1. 生成自動化測試程式碼？（→ `test-automation` skill）
2. 同步測試計劃到 JIRA？
3. 審查測試用例品質？（→ `test-review` skill）

## 設定依賴

| 設定 Key | 用途 | 缺值時行為 |
|---------|------|-----------|
| `google.tc_template_id` | 複製模板建立 Sheet | 改用 `createSpreadsheet` 從零建 |
| `google.qa_tc_folder_id` | 上傳目標資料夾 | 提示使用者手動移檔 |
| `platforms.ios.repo` / `platforms.android.repo` / `platforms.web.repo` | 程式碼影響面分析 | 跳過自動分析，請使用者貼路徑 |
| `platforms.web.enabled` | 啟用 Web 平台測試規劃 | 跳過 Web 測試類型 |
| `platforms.web.frameworks.primary` | Web E2E 預設框架 | 預設 Playwright |
| `platforms.web.default_browsers` | 跨瀏覽器測試範圍 | 預設 Chrome + Safari |
| `workflow.auto_a11y_pairing` | a11y 自動配對 | 不自動建議配對 |
| `mode = markdown-only` | 全程模式 | 不呼叫任何 MCP，輸出 `.md` |

## 範例

詳見 [`examples.md`](./examples.md)
