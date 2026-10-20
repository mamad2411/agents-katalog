---
name: obsidian-para-wiki
description: "在 PARA 結構的 Obsidian vault 中建立並維護個人 LLM 知識庫。Raw 素材存於 Resources/llm-wiki/raw/，編譯後的文章存於 Resources/llm-wiki/wiki/，全程使用 Obsidian wikilink（與 Quartz shortest 模式相容）。支援 Ingest、Query、Lint 三大操作，並能從 0-inbox/ 擷取素材、寫入 daily note 的 Logs 區。觸發詞：加入知識庫、匯入到 wiki、ingest to wiki、我對 X 知道什麼、查詢知識庫、檢查 wiki、整理知識庫、PARA wiki、obsidian wiki、個人知識庫。"
---

# Obsidian PARA Wiki

在 PARA 結構的 Obsidian vault 中維護個人 LLM 知識庫。靈感來自 Karpathy：「LLM 寫 wiki，人類讀 wiki」。

與原版 karpathy-llm-wiki 的差異：

- 使用 PARA 的 `Resources/` 作為沙盒，不污染既有結構
- 所有連結採用 Obsidian wikilink shortest 格式，與 Quartz 發佈相容
- 支援從 `0-inbox/` 擷取素材，以 Obsidian CLI `move` 搬檔以保留 wikilink 完整性
- 每次 Ingest 在今日 daily note 的 `# Logs` section 追加一行記錄

## 固定路徑

```
<vault-root>/
├── 0-inbox/
│   └── daily/YYYY-MM-DD.md         # Daily note，ingest 後追加 Logs
├── Resources/
│   └── llm-wiki/
│       ├── raw/                    # 原始素材（不可修改）
│       │   └── <topic>/YYYY-MM-DD-slug.md
│       └── wiki/                   # 編譯後文章（AI 全權維護）
│           ├── index.md
│           ├── log.md
│           └── <topic>/
│               └── <article>.md
```

`wiki/` 僅支援一層 topic 子目錄，不再往下嵌套。

## 初始化

僅在第一次 Ingest 觸發。檢查 `Resources/llm-wiki/` 下的結構，只建立缺少的部分，從不覆寫既有檔案：

- `Resources/llm-wiki/raw/`（含 `.gitkeep`）
- `Resources/llm-wiki/wiki/`（含 `.gitkeep`）
- `Resources/llm-wiki/wiki/index.md` — 標題 `# Knowledge Base Index`，空 body
- `Resources/llm-wiki/wiki/log.md` — 標題 `# Wiki Log`，空 body

若 Query 或 Lint 找不到結構，告訴使用者「請先執行一次 ingest 初始化 wiki」。**不要自動建立**。

---

## Wikilink 規則（重要）

本 skill 產出的所有連結**一律使用 Obsidian wikilink shortest 格式**。Quartz 在 `shortest` 模式下以檔名查找唯一匹配，帶路徑前綴的連結會產生錯誤 URL。

- ✅ `[[article-name]]`
- ✅ `[[article-name|Display Title]]`
- ❌ `[[wiki/llm/article-name]]`（路徑前綴破壞 Quartz）
- ❌ `[[llm/article-name]]`
- ❌ `[text](../../raw/llm/file.md)`（標準 MD 連結）

**同名消歧義**：只有當兩個不同 topic 目錄下出現同名檔案時，才允許用 `[[topic/article-name|Display]]`。

**Raw 引用**：使用 wikilink，省略副檔名，例如 `[[2026-04-12-mistral-7b-paper]]`。

**表格內 wikilink**：markdown 表格的 `|` 與 wikilink 的 `|`（display text 分隔符）衝突，需將後者寫成 `\|`，例如 `[[article\|Title]]`。

---

## Ingest

抓取來源並編譯進 wiki。兩種入口：

### 入口 A：URL 或使用者貼上的內容

1. 用可用的 web/file 工具取得內容；若無法抓取，請使用者直接貼上
2. 跳到「Fetch」

### 入口 B：從 `0-inbox/` 擷取

1. 讀取使用者指定的 `0-inbox/<file>.md`
2. 跳到「Fetch」
3. Compile 完成後，處理原始 inbox 檔：
   - 預設行為：用 Obsidian CLI 搬到 `Archives/inbox-processed/<file>.md`
     ```
     /Applications/Obsidian.app/Contents/MacOS/Obsidian move path="0-inbox/<file>.md" to="Archives/inbox-processed/<file>.md"
     ```
   - 若使用者偏好直接刪除，依其指示刪除
4. 使用 Obsidian CLI 的前提是 Obsidian 在背景執行且啟用了 command line interface。無法使用時改用檔案系統 `mv` 並警告使用者手動檢查 wikilink

### Fetch（寫入 `raw/`）

1. **選 topic 子目錄**：先掃 `Resources/llm-wiki/raw/` 看有哪些既有 topic，能沿用就沿用；只有真的不同的主題才新建目錄
2. **檔名**：`YYYY-MM-DD-descriptive-slug.md`
   - Slug 從標題萃取，kebab-case，最多 60 字元
   - 發布日未知 → 省略日期前綴（`descriptive-slug.md`），metadata 的 Published 欄位設為 `Unknown`
   - 檔名衝突 → 加數字後綴（`slug-2.md`）
3. **內容**：保留原文，清理格式噪音（多餘空白、HTML 殘留、導覽列），不改寫意見
4. **Metadata**：見 `references/raw-template.md`

初次寫入檔案沒有既存 wikilink 指向它，直接用 Write 工具即可，不需要經過 Obsidian CLI。

### Compile（寫入 `wiki/`）

判斷新內容歸屬：

- **與既有文章核心論點一致** → 合併進該文章，在 Sources/Raw 欄位加入新來源，更新受影響段落
- **全新概念** → 在最相關的 topic 建立新文章，檔名以概念命名（不是 raw 檔名）
- **橫跨多個 topic** → 放在最相關的目錄，用 See Also wikilink 交叉引用

上述並非互斥。同一來源可能既合併進某篇、又催生出一篇新文章。

**事實衝突處理**：若新來源與既有內容衝突，加上來源標註（誰說什麼）。合併時在該篇內部註記；若衝突內容散在不同文章，兩邊都註記並交叉連結。

文章格式見 `references/article-template.md`。要點：

- `Sources`：作者、組織或刊物名 + 日期，分號分隔
- `Raw`：用 wikilink 指向 raw 檔，省略副檔名，分號分隔，例：`[[2026-04-12-mistral-7b]]; [[2026-04-12-llama3-report]]`
- `Updated`：知識內容最後變動的日期

### Cascade Updates

主文章完成後，檢查漣漪影響：

1. 掃同 topic 目錄下其他文章是否受新來源影響
2. 掃 `wiki/index.md` 其他 topic 是否有相關概念的文章
3. 每個實質受影響的文章都更新，並刷新 Updated 日期

Archive 頁**從不** cascade 更新（它們是時間點快照）。

### Post-Ingest

**更新 `wiki/index.md`**：為每個動過的文章新增或更新條目。新 topic 區段需附一行說明。Updated 反映知識內容變動時間，非檔案 mtime。格式見 `references/index-template.md`。

**追加 `wiki/log.md`**：

```
## [YYYY-MM-DD] ingest | <primary article title>
- Updated: <cascade-updated article title>
- Source: 0-inbox/<file>.md        # 僅入口 B 時附上
```

沒有 cascade 更新時省略 `- Updated:` 行。

**寫入今日 daily note**：

1. 檢查 `0-inbox/daily/YYYY-MM-DD.md` 是否存在
2. 存在時，在 `# Logs` section 下追加一行：
   ```
   - Ingested [[article-slug|Article Title]] to llm-wiki
   ```
   若同時有多篇更新，每篇追加一行
3. Daily note 不存在時**跳過**，不要自動建立（daily note 是使用者自己的 capture 流程）
4. `# Logs` section 裡若只有預設的 `-` placeholder，先替換它再追加

---

## Query

搜尋 wiki 並回答問題。觸發範例：

- 「我對 X 知道什麼？」
- 「總結 wiki 裡所有關於 Y 的內容」
- 「根據我的 wiki 比較 A 和 B」

### 步驟

1. 讀 `Resources/llm-wiki/wiki/index.md` 定位相關文章
2. 讀那些文章並綜合答案
3. **優先引用 wiki 內容**，而非 AI 自己的訓練知識。引用時用 wikilink：`[[article-slug|Article Title]]`
4. 把答案輸出在對話中，除非使用者要求存檔，否則不寫檔

### Archiving

使用者明確要求把答案存到 wiki 時：

1. 寫一個新 wiki 頁面，見 `references/archive-template.md`
   - `Sources`：被引用的 wiki 文章，用 wikilink
   - 無 `Raw` 欄位（內容不來自 raw/）
   - 檔名反映查詢主題，例：`transformer-architectures-overview.md`
   - 放在最相關的 topic 目錄
2. **永遠建立新頁**，不合併進既有文章（archive 是綜合答案的快照，不是原始素材）
3. 更新 `wiki/index.md`，Summary 前綴 `[Archived]`
4. 追加 `wiki/log.md`：
   ```
   ## [YYYY-MM-DD] query | Archived: <page title>
   ```

---

## Lint

品質檢查，分兩類權限等級。

### Deterministic Checks（自動修）

**Index 一致性** — 比對 `wiki/index.md` 與實際檔案（排除 `index.md`、`log.md`）：

- 檔案存在但 index 沒列 → 新增條目，Summary 填 `(no summary)`。Updated 取文章 metadata 的 Updated 欄位；沒有時 fallback 到檔案 mtime
- Index 條目指向不存在的檔案 → 標記 `[MISSING]`，**不刪除**，由使用者決定

**Wikilink 解析** — 掃 wiki/ 下所有 .md 檔的 wikilink（body 與 Sources 欄位），排除 index.md 與 log.md（上面已處理）：

- 目標檔案不存在 → 在 wiki/ 搜尋同名檔案
  - 唯一匹配 → 修正連結
  - 零個或多個 → 回報使用者

**Raw 引用** — 文章 `Raw` 欄位的每個 wikilink 必須對應到 raw/ 下的檔案：

- 目標不存在 → 搜尋 raw/，唯一匹配則修正，否則回報

**Quartz shortest 合規** — 掃所有 wikilink，凡是含路徑前綴的：

- `[[wiki/llm/mistral-7b]]`、`[[llm/mistral-7b]]` 等
- 檔名在 vault 內唯一 → 自動改為 `[[mistral-7b]]`
- 有多個同名檔 → 保留但列入警告，建議使用者手動消歧義

**See Also** — 在每個 topic 目錄內：

- 補上明顯缺失的交叉引用
- 移除指向已刪除檔案的連結

### Heuristic Checks（只回報）

這些需要判斷，不自動修：

- 跨文章的事實矛盾
- 被新來源推翻的舊主張
- 缺少衝突標註的分歧來源
- **孤兒 wiki 頁**：沒有任何其他 wiki 文章連到它
- **孤兒 raw 檔**：`raw/` 內的檔案從未被任何 wiki 文章的 `Raw` 欄位引用
- 跨 topic 的潛在交叉引用
- 頻繁被提到卻沒有專屬頁的概念
- Archive 頁引用的源文章自 archive 以來已大幅變動

### Post-Lint

追加 `wiki/log.md`：

```
## [YYYY-MM-DD] lint | <N> issues found, <M> auto-fixed
```

---

## Obsidian CLI 使用守則

- **搬 .md 檔**一律用 Obsidian CLI `move`（自動更新 vault 內所有 wikilink）：
  ```
  /Applications/Obsidian.app/Contents/MacOS/Obsidian move path="<from>" to="<to>"
  ```
- **初次建立檔案**（沒有既存 wikilink 指向它）用 Write 工具即可
- **編輯既有檔案**用 Edit 工具即可（不改動檔名就不會破壞 wikilink）
- 前提：Obsidian app 在背景執行，Settings → General → Advanced → Command line interface 已開啟
- 無法使用時改用檔案系統 `mv`，並警告使用者需手動檢查指向該檔的 wikilink 是否仍正確

---

## Conventions

- 所有連結用 Obsidian wikilink `[[shortest-name]]`，與 Quartz `shortest` 模式相容
- `wiki/` 只支援一層 topic 子目錄
- `raw/` 只支援一層 topic 子目錄，命名與 `wiki/` 的 topic 對齊
- 今日日期用於 `log.md` 條目、`Collected`、`Archived`
- `Updated` 欄位反映知識內容最後變動時間，不是檔案系統 mtime
- `Published` 日期來自來源（不明時填 `Unknown`）
- **Ingest** 更新：`wiki/index.md` + `wiki/log.md` + 今日 daily note 的 `# Logs` section
- **Archive (from Query)** 更新：`wiki/index.md` + `wiki/log.md`
- **Lint** 更新：`wiki/log.md`（修 index 時也更新 `wiki/index.md`）
- **純 Query** 不寫任何檔案
