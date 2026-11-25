---
name: speckit-to-tc
description: 從 GitHub Spec Kit / SDD 規格文件（Jira ticket description / spec.md / api.md）一鍵草擬 BB+WB TC markdown 草稿，套 14 欄結構，自動歸位到指定 repo 對應目錄。當使用者提到「speckit close 了寫 TC / 從 spec 草 TC / 把這張規格 ticket 變 TC / draft TC from this spec」，或在 Jira 偵測到「speckit 規格制定」ticket close 時觸發。配套：test-review（審草稿）、test-master（深度設計）、tc-to-pytest（草稿 → pytest 三件套）。
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Write, Edit, Bash, mcp__atlassian__getJiraIssue
argument-hint: "[JIRA 票號 / spec 檔路徑 / ticket URL]"
---

# speckit-to-tc

> ⚙️ **執行前先讀 [`modules/config-loader.md`](./modules/config-loader.md)**。
> 啟用條件：`config.speckit.enabled = true`。

> 💡 **第一次聽到 Spec Kit / SDD？** 先看 [`concept-zh.md`](./concept-zh.md) 中文入門導讀（5 分鐘搞懂「為什麼規格寫好可以一鍵變 TC」）。

## 適用場景

- ✅ Jira 上一個「spec 規格制定」ticket 剛 close
- ✅ 使用者手上有一份 `spec.md` / `api.md`，想快速產第一稿 TC
- ✅ 從規格 docx / wireframe 提煉 description 後想轉 TC

## 不適用場景

- ❌ spec 仍未定稿（要等 ticket close / spec freeze 後才跑）
- ❌ 純自動化腳本生成 → 用 `test-automation`
- ❌ 已有完整 TC、想升級 → 用 `test-review` + `test-master`

## Phase 1: 取得 spec 來源

依 argument 類型判斷輸入：

| 輸入 | 動作 |
|------|------|
| Jira 票號（如 `{{JIRA_PROJECT_KEY}}-XXXX`）| 用 `mcp__atlassian__getJiraIssue` 或 curl + Atlassian PAT 抓 description |
| 本地 spec 檔（如 `<repo>/feature/spec.md`）| 用 Read 直接讀 |
| ticket URL | 從 URL 抽 key 然後同上 |
| 沒給 → 互動式詢問 | 「請給我 ticket key / spec 檔路徑 / 直接貼 spec 內容」 |

**抓 Jira description 的標準 curl**：
```bash
curl -s -G "{{JIRA_INSTANCE_URL}}/rest/api/3/issue/<KEY>" \
  --data-urlencode "fields=summary,description,parent,status,assignee,attachment" \
  -u "$ATLASSIAN_EMAIL:$ATLASSIAN_TOKEN" \
  -H "Accept: application/json"
```

**處理 ADF 格式 description**：Atlassian description 通常是 Atlassian Document Format JSON。先轉成 markdown／plain text 再給後續分析。簡易處理：遞迴拉 `text` 欄位。

## Phase 2: 功能歸位（決定輸出路徑）

從 `config.speckit.feature_routing` 讀路徑對應規則：

```json
{
  "speckit": {
    "enabled": true,
    "repo_root": "~/Desktop/your-spec-repo",
    "feature_routing": [
      { "keywords": ["集章", "stamp", "NFC"], "path": "love/stamp/", "epic": "{{JIRA_PROJECT_KEY}}-XXXX" },
      { "keywords": ["健康", "步數", "health", "HealthKit"], "path": "peace/health/", "epic": "{{JIRA_PROJECT_KEY}}-YYYY" },
      { "keywords": ["錢包", "wallet", "payment"], "path": "love/wallet/", "epic": "{{JIRA_PROJECT_KEY}}-ZZZZ" }
    ],
    "fallback": "ask_user"
  }
}
```

依 summary / description 關鍵字 match `feature_routing[].keywords`，決定 `<repo_root>/<path>` 為輸出目錄；都不 match → 跳出問使用者。

**檔案命名**：`tc-be-{KEY}-draft.md`（如 `tc-be-{{JIRA_PROJECT_KEY}}-1234-draft.md`）
**狀態 metadata**：`Draft v0.1 — pending review`

## Phase 3: 讀既有上下文（Cross-reference）

**必讀（如存在）**：
- 同目錄 `spec.md`（產品規格）
- 同目錄 `api.md`（API 契約）
- repo 根 `tc-index.md`（命名規則 + Drive folder + 既有 TC）
- 同目錄已上 Sheet 的 TC markdown

讀完之後應該知道：
- 這個 ticket 對應哪個功能模組
- 既有 spec / api 已涵蓋什麼
- 之前該團 TC 用過什麼 ID 命名規則
- 該團是 Web / Native / Flutter / BE-only？

## Phase 4: 草擬 TC

### 結構（14 欄 A-N，跟通用模板對齊）

| 欄 | 名稱 | 範例值 |
|---|------|--------|
| A | ID | `BB-{FEATURE}-001` / `WB-{FEATURE}-W001` |
| B | Phase | `Feature Done` |
| C | 測試結果 | `Not Run` |
| D | 測試結論 | (留空) |
| E | 測試標題 | 「批次上傳 PNG 檔名對應 ID 成功」 |
| F | 測試分類 | 9 種黑箱 / 6 種白箱（見下） |
| G | 優先度 | P0 / P1 / P2 |
| H | 平台 | Web / iOS / Android / Both / BE-only |
| I | 前置條件 | 「CMS 已登入；批次包 ZIP < 10MB」 |
| J | 步驟 | 編號列點 |
| K | 預期結果 | **可驗證**，不能寫「應該正確」 |
| L | 自動化建議 | Y / N + 工具 |
| M | 備註 | 對應 spec 章節 / pytest test_name |
| N | 留空 | (Sheet 用) |

### 黑箱 / 白箱判定原則（分類鐵律，下面 9+6 種分類都要服從這條）

- **黑箱（BB）**：前置條件、步驟都必須是**一般使用者看得懂、操作得到**的——不需要任何第三方工具查看或測試（不用 Postman/curl/adb/Charles/mitmproxy/Instruments/Xcode Debug/資料庫直查/log 檢視等）。
- **白箱（WB）**：只要是**API 相關測試**，或**需要用到第三方工具**才能執行/驗證的，都歸類白箱。前置條件跟步驟都要**明確寫出用什麼工具測試**。
- **判定順序**：先問「一般使用者不靠任何工具，照著步驟能不能重現、看得懂前置條件？」——能 → 黑箱；不能（需要工具介入或屬 API/內部狀態層級）→ 白箱。
- **為什麼要固定**：這條分類標準跟 spec 內容脫鉚，spec 中途修正時只需要新增/調整對應 TC 內容，不需要重新判斷既有整份 TC 的黑白箱歸屬。
- 下面兩組分類是這條原則的具體案例化（例如「效能」黑箱角度是使用者感知/loading秒數、白箱角度是 cold start/TTFB 需工具量測），遇到不在清單內的新案例時回到上面的判定順序自行判斷，不要卡住。

### ⚠️ 反漂移規則：下面 9+6 種是「思考用的覆蓋checklist」，不是可以直接寫進 Column F 的值

**這點很重要，2026-07-17 發現既有 Sheet 已經因為這個混淆漂移出至少 9 個未受管理的分類**（含「邊界測試」vs「異常/邊界測試」這種近似重複）：下面 9 種黑箱 / 6 種白箱是幫你想「這個功能該覆蓋哪些測試角度」的**概念清單**，但實際寫入 Google Sheet「測試分類」欄（Column F）的字串，**只能是 `config.test_case_format.categories` 這個固定白名單裡的值**（目前黑箱只有 3 種：冒煙-Feature Done / 功能測試 / 異常/邊界測試；白箱 6 種：API 驗證測試 / 內部狀態驗證 / 並發安全測試 / 記憶體測試 / Sentry 診斷測試 / JS Bridge 測試），或目標 Sheet 現有出現過的值。

**映射規則**：
- 黑箱概念分類 4~9（錯誤處理/生命週期/跨平台相容性/端對端/效能/a11y）在固定清單裡沒有對應分類時，**force-fit 進「功能測試」或「異常/邊界測試」**（依內容判斷哪個更貼近），不要另創「相容性測試」「端對端測試」「無障礙測試」這種新名詞。
- 白箱概念分類的「效能基準」「安全」若無法對應到既有的「Sentry 診斷測試」「JS Bridge 測試」等分類，同樣 force-fit 進語意最接近的既有分類（例如並發/資源類 → 並發安全測試或記憶體測試；資安類的寫法見「資安必檢 9 類」）。
- **用備註欄（Column M）保留真實測試意圖**（例如寫「效能角度：冷啟動時間」），不要犧牲精確度去硬套分類——分類欄要固定不變，細節放備註。
- 每次要寫入既有 Sheet 前，先讀該 Sheet「測試分類」欄現有值當有效範圍；若真的判斷需要擴充固定清單，要先跟使用者確認，並同步更新 config + Sheet `status` tab 的統計公式，不能悄悄新增。

### 黑箱分類（9 種思考角度，每類 N 條依風險評估——寫入 Sheet 時仍要套上面的反漂移規則）

1. **冒煙-Feature Done**：F1/F2/F3/F4 四階段 smoke
2. **功能測試**：happy path / 變體
3. **異常/邊界測試**：空值 / 超長 / 特殊字元 / 大檔
4. **錯誤處理**：401 / 403 / 500 / 網路斷
5. **生命週期**：背景前景切換 / 殺 App / 殺 process
6. **跨平台 / 相容性**：OS 版本 / 機型 / 主流瀏覽器
7. **端對端**：跨模組整合
8. **效能（黑箱角度）**：使用者感知（loading 不過 N 秒）
9. **a11y**：字級放大 / VoiceOver / TalkBack / 對比 / 觸控目標 / Reduce Motion

### 白箱分類（6 種）

1. **API 驗證**：endpoint / status code / schema / 邊界
2. **效能基準**：cold start / TTFB / 60fps
3. **安全**：見下方「資安必檢 9 類」，每份 TC 都要逐類判斷
4. **記憶體**：leak / OOM / image cache 上限
5. **並發**：race condition / TSAN / Isolate 安全
6. **內部狀態**：狀態機 / 快取一致性

### 資安必檢 9 類（每份 TC 都要逐類判斷，不能只寫「沒登入回 401」）

> 2026-11-23 加。原本「安全」只有一行，實際寫出來的 TC 幾乎只有「沒登入回 401」，越權、同時送出、儲存型 XSS 常常整類漏掉。

草擬時對每一類問「這個功能有沒有這種入口」：有，就至少寫 1 條 TC；沒有，就在 Phase 6 的「資安覆蓋」寫一行不適用的原因。**不可以默默跳過。**

| # | 類別 | 什麼時候適用 | TC 要驗什麼 |
|---|---|---|---|
| 1 | 認證 | 需要登入的 API | 不帶、過期、竄改的 token／cookie → 401，沒有資料被讀到或寫入 |
| 2 | 水平越權（IDOR） | 路徑、query、body 有資源 id、會員識別碼、訂單編號 | 用 A 帳號登入、帶 B 帳號的 id 去讀、改、刪 → 拒絕，不能回 200；列表 API 改篩選參數也撈不到別人的資料。要準備兩個測試帳號 |
| 3 | 垂直越權（角色權限） | 後台有不同角色，或 API 只給特定角色用 | 低權限角色（例如唯讀）直接呼叫寫入、管理 API → 403。前端藏按鈕不算數，要直接打 API |
| 4 | 同時送出（race condition） | 一次性或有數量上限的動作：兌換、領取、集點、核銷、扣款、使用代碼、扣庫存 | 同一個請求「同時」送 10～20 次 → 只成功 1 次，數量不超扣、紀錄不重複。跟「用過再送一次被擋」不一樣，後者擋不住同時送 |
| 5 | 輸入注入 | 查詢、篩選、排序、搜尋參數，或會組進查詢的欄位 | 塞 SQL 片段、NoSQL 運算子（如 `{"$ne": null}`）、超長字串、控制字元 → 4xx，不能 500，回應不帶 SQL、stack trace 等內部細節 |
| 6 | 儲存型 XSS／HTML 內容 | 可以存自由文字或 HTML、之後在另一端顯示的欄位（例如後台編輯、前台顯示的公告、說明、名稱） | 存入 `<script>`、`<img src=x onerror=...>`、`javascript:` 連結 → 寫入時被清掉，或顯示端照文字顯示不執行。寫入端、顯示端都要驗；規格有寫由哪一端負責清，就照規格判斷 |
| 7 | 檔案上傳與匯出 | 上傳圖片、Excel、CSV，或匯出檔案 | 副檔名跟內容不符、超過大小上限、檔名含 `../`、xlsx／csv 儲存格以 `=` `+` `-` `@` 開頭（公式注入）→ 被擋或安全處理；匯出檔不能讓公式在使用者電腦上執行 |
| 8 | 敏感資料外洩 | 回應、錯誤訊息、匯出檔會帶個資或憑證 | 不回密碼、token；身分證、手機、卡號照規格遮罩；錯誤訊息不帶內部細節 |
| 9 | 繞過前端限制 | 前端有擋的規則：數量上限、金額不能負數、狀態不能跳步驟 | 直接打 API 送前端不允許的值 → 後端也擋 |

- **黑白箱**：照上面的判定鐵律。大部分要直接打 API → 白箱；但「在後台表單存入 `<script>`，到前台看會不會執行」不用工具 → 黑箱。
- **分類欄**：不新增「資安測試」分類。第 4 類寫「並發安全測試」，其他白箱寫「API 驗證測試」、黑箱寫「異常/邊界測試」；備註欄加 `資安：越權` 這類標記，方便之後篩選統計。
- **優先度**：牽涉金額、點數、庫存、個資的第 2、3、4、8 類 → P0；其他至少 P1。
- **預期結果**：規格沒寫的狀態碼不要自己定死，寫成「拒絕（4xx），不能 200 或 500，資料沒有外洩或被改」。判 Failed 看規格，以及資料有沒有真的外洩或被改。
- **執行範圍**：只在 dev／UAT、用測試帳號跑；不碰正式站；同時送出保持小量，不做壓力測試；上傳用小樣本檔。

### a11y 強制 4 條（每份 TC 都要）

> 若 `config.workflow.auto_a11y_pairing = true` 才強制。

- 字級放大 iOS（Dynamic Type 最大）
- 字級放大 Android（fontScale 最大）
- VoiceOver / TalkBack 讀取順序
- 觸控目標 ≥ 44×44 pt / 48×48 dp + 對比度

### BE-only 功能特化

如果 ticket 是 BE API（如「[BE][CMS] 基礎 API」），白箱占比拉高：
- BB 30% / WB 70%
- 平台欄全 `BE-only`
- 自動化建議全 `Y`（套 pytest-api-kit）
- 對齊 `tc-to-pytest` skill

## Phase 5: 寫檔

1. 寫到 `tc-be-{KEY}-draft.md`，放對應目錄（依 `feature_routing` 決定）
2. 開頭 metadata block：

```markdown
---
ticket: {{JIRA_PROJECT_KEY}}-XXXX
spec_source: <repo>/feature/spec.md (§3 入口頁)
draft_version: v0.1
draft_date: 2026-MM-DD
status: pending review
output_target: Google Sheet（待人工搬上去）或 mode=markdown-only 下保留 .md
generated_by: speckit-to-tc skill
---
```

3. 兩段：`## Black-box (BB)` + `## White-box (WB)`，每條 TC 用 markdown table
4. 最後一段 `## 設計依據` 列出參考的 spec 章節

## Phase 6: 後續建議（stdout 印給使用者）

```
✅ 草擬完成 → tc-be-{{JIRA_PROJECT_KEY}}-XXXX-draft.md
- BB N 條（其中 a11y N 條）
- WB N 條（其中 BE API 驗證 N 條）
- 主要 cover：[列 3-5 個 highlight]
- 資安覆蓋：適用 N 類（第 1、2、4…類，共 N 條）／不適用 N 類（每類一行原因，例：第 7 類，這個功能沒有上傳）
- 未 cover / 不確定：[列 spec 沒講清楚的議題]

下一步建議：
1. 你 review 草稿（uncovered 議題回 PM 釐清）
2. 跑 test-review 對草稿打分（找 critical/major 缺口）
3. 通過後人工搬到 Google Sheet（命名照 tc-index.md 規範）
4. 對應 BE API 部分跑 tc-to-pytest
```

## ⚠️ 安全護欄

- ✅ 只 Write 到 `tc-be-{KEY}-draft.md`，**不動其他檔**
- ❌ 不主動上 Google Sheet（draft only，使用者手動搬，或啟用 `sheet-md-sync` 自動同步）
- ❌ 不主動 commit / push（draft 留著等 review）
- ❌ 不要編造 spec 沒寫的功能（uncovered 就標 uncovered）
- ⚠️ ADF 解析失敗時 fallback to plain text 而不是亂猜

## 配套整合

- 跑完後使用者通常會手動跑 `test-review`（自動）或 `test-master --mode=deep`（升級）
- 要把草稿正式上 Sheet → 用 `sheet-md-sync` skill（如已建）
- BE API 部分要轉 pytest → 用 `tc-to-pytest` skill

## 設定依賴

| 設定 Key | 用途 | 缺值時行為 |
|---------|------|-----------|
| `speckit.enabled` | 啟用此 skill | skill 不啟用 |
| `speckit.repo_root` | 草稿輸出 repo root | 互動式詢問 |
| `speckit.feature_routing` | 功能歸位規則 | fallback 詢問使用者 |
| `jira.instance_url` | 抓 Jira ticket | 改用 spec 檔路徑 |
| `workflow.auto_a11y_pairing` | a11y 強制 4 條 | 改為可選 |

## 範例

詳見 [`examples.md`](./examples.md)
