---
name: md-to-codelab-html
description: 'Converts one or more markdown (*.md) source files into a complete, self-contained single-page HTML codelab. Outputs a Google Codelabs-style layout: numbered step sidebar, dynamic screenshot/image injection (referenced by name in markdown, automatically resolved from image files), syntax-highlighted code blocks, info/warning callout boxes, and responsive navigation. Use when: generating a codelab tutorial page, building step-by-step guide HTML, converting tutorial markdown to HTML, inserting screenshots into codelab layout, building training material HTML pages.'
argument-hint: 'Source markdown file(s) and optional image assets (e.g., "lab-instructions.md 圖一.png 圖二.png")'
---

# Markdown → Codelab HTML 產生器

## 用途

將一或多份 Markdown 來源檔轉換成單頁自包含的 HTML 教學頁面，樣式仿照 [Google Codelabs](https://codelabs.developers.google.com/) 排版：

- 左側固定步驟導覽列（編號 + 步驟標題）
- 主要內容區（各步驟全文）
- 動態圖片注入（以圖片名稱作為 key，自動對應同目錄的圖片檔）
- 語法上色程式碼區塊（含右上角一鍵複製按鈕）
- 資訊 / 警告 callout 框
- 頁底上一步 / 下一步按鈕

---

## 輸入慣例（Markdown 撰寫規則）

詳見 [Markdown 語法參考](./references/markdown-conventions.md)。

### 步驟標題

使用 `## 步驟名稱` 作為 H2，每個 H2 自動成為一個步驟，並顯示在側邊欄。

```markdown
## 1. 概覽
## 2. 環境準備
## 3. 建立 Agent
```

### 圖片注入

在 `.md` 中以標準 Markdown 圖片語法標示，圖片名稱（不含副檔名）即為 key：

```markdown
![圖一](圖一)
![系統架構圖](系統架構圖)
```

生成時，Agent 搜尋同目錄下 `圖一.*`（任意副檔名）的檔案：
- **找到** → 產生 `<img src="圖一.png" ...>` 並附上名稱作為圖說
- **找不到** → 產生佔位區塊 `⬛ 待補圖：圖一`，以警示黃框呈現

### Callout 框

| Markdown | 渲染結果 |
|----------|---------|
| `> **NOTE:** 說明文字` | 藍色資訊框 |
| `> **WARNING:** 說明文字` | 橘色警告框 |
| `> **IMPORTANT:** 說明文字` | 紅色重要框 |
| `> **TIP:** 說明文字` | 綠色提示框 |

---

## 執行程序

> **重要：採用兩階段流程。**
> - **第一階段**：根據來源內容生成詳細完整教學 Markdown，儲存至 `docs/instruction-preview.md`，並請使用者確認。
> - **第二階段**：使用者確認後，依據 `docs/instruction-preview.md` 執行 HTML 轉換，輸出 `index.html`。

---

## 第一階段：生成教學內容預覽

### Step 1：收集來源

1. 確認使用者提供的 `.md` 來源檔路徑（可多個，例如 `instruction.md`、`outlines.md`）
2. 讀取所有來源檔內容，作為教學內容生成的素材

### Step 2：生成詳細完整教學 Markdown

根據來源內容，生成一份詳細、完整、可直接作為 Codelab 輸入的教學 Markdown 文件，需包含：

1. **H1 標題**：教學名稱（作為 Codelab 主標題）
2. **H2 步驟**：每個 `##` 自動成為一個 Codelab 步驟，需包含完整實作說明
3. **程式碼範例**：各步驟附上對應的完整可執行程式碼區塊（含語言標記）
4. **圖片佔位**：以 `![圖名](圖名)` 標記待補圖片位置
5. **Callout 框**：重要提示、警告、操作注意事項以 blockquote callout 格式標示
6. **表格**：關鍵指標、比較資訊以 Markdown 表格呈現

### Step 3：儲存預覽檔案

將生成的完整教學 Markdown 儲存至：

```
docs/instruction-preview.md
```

### Step 4：請使用者確認

輸出以下確認提示，**等待使用者確認後再繼續**：

```
✅ 教學內容已生成並儲存至 docs/instruction-preview.md
請確認內容是否符合需求，確認後回覆「確認」以繼續生成 HTML。
```

---

## 第二階段：HTML 轉換（使用者確認後執行）

### Step 5：收集圖片資源

1. 掃描同目錄下所有圖片檔（`*.png`、`*.jpg`、`*.gif`、`*.webp`、`*.svg`），建立 `圖片名稱 → 路徑` 對照表
2. 來源 Markdown 固定使用 `docs/instruction-preview.md`

### Step 6：解析 Markdown

按照下列順序解析 `docs/instruction-preview.md`：

1. **H1**（`#`）→ Codelab 標題 + `<head><title>`
2. **H2**（`##`）→ 各步驟（`<section id="step-N">`）
3. **H3**（`###`），**H4**（`####`）→ 步驟內子標題
4. **圖片語法** `![名稱](名稱)` → 對照表替換為 `<img>` 或佔位框
5. **Blockquote callout** → 依前綴轉換為對應 callout CSS class
6. **程式碼圍欄** ` ```language ` → `<pre><code class="language-{lang}">` + highlight.js + 右上角「複製」按鈕（點擊後顯示「✓ 已複製」）
7. **表格** → `<table class="codelab-table">`
8. **有序 / 無序清單** → `<ol>` / `<ul>`
9. **行內格式**（`**bold**`、`` `code` ``、`*italic*`）→ 對應 HTML 標籤

### Step 7：套用 HTML 模板

使用 [HTML 基礎模板](./assets/template.html) 組合最終輸出：

1. 填入 `{{TITLE}}`、`{{AUTHOR}}`、`{{DATE}}`（從 H1 下方 Frontmatter 或檔頭取得）
2. 產生側邊欄步驟清單（`<nav>`）
3. 逐步填入 `<section>` 內容
4. 替換所有圖片 key → `<img>` 或佔位框
5. 渲染 callout 框

### Step 8：驗證輸出

檢查下列項目後輸出最終 HTML 檔（`index.html`）：

- [ ] 所有 `![圖名](圖名)` 均已替換（無殘留原始語法）
- [ ] 有佔位框的圖片列出警告清單，提示使用者補圖
- [ ] HTML 語法合法（標籤正確閉合）
- [ ] 側邊欄步驟數量與 `<section>` 數量一致
- [ ] 標題 `<title>` 與 H1 一致

### Step 5：輸出

- 預設輸出至與第一個 `.md` 同目錄，檔名為 `<md-basename>.html`
- 若有多個 `.md` 則合併為單一 HTML 頁面，標題取第一個 `.md` 的 H1

---

## 圖片佔位框錯誤回報（格式）

生成完成後，若有未解析圖片，在 chat 回覆中列出：

```
⚠️ 以下圖片未找到對應檔案，已插入佔位框：
  - 圖一（在步驟 2）
  - 系統架構圖（在步驟 3）
請補充對應圖片後重新執行，或手動替換佔位框。
```

---

## 範例呼叫

```
/md-to-codelab-html lab-instructions.md 圖一.png 圖二.png 系統架構圖.png
```

```
/md-to-codelab-html src/chapter1.md src/chapter2.md --images src/images/
```
