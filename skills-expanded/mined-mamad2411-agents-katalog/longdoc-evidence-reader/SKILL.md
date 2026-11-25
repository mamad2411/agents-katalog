---
name: longdoc-evidence-reader
description: 在使用者要閱讀超長 PDF、規格文件或大型程式碼庫並回收證據時使用。常見觸發像「讀這份長 PDF」「幫我從 codebase 找證據」「整理可追溯引用」。輸出證據摘要與引用鏈；不適合短文快速摘要或純自由發揮。
version: 2026.3.31
homepage: https://github.com/AllanYiin/skills/tree/main/skills/longdoc-evidence-reader
license: MIT
metadata: {"author":"Allan Yiin","language":"zh-TW","category":"research","short-description":"長文件切片搜尋、證據彙整與可追溯閱讀工作流程","openclaw":{"emoji":"🔍"}}
---

# Longdoc Evidence Reader

## Purpose

這個 skill 用來處理「內容太長，不能靠一次讀完就可靠回答」的任務。它會先把長文件、PDF 或大型程式碼庫切成可搜尋的單位，再透過程式化搜尋、篩選與驗證，整理出可追溯的證據鏈，而不是直接憑印象摘要。

## Scope

### In scope
- 超長 PDF、法規、研究報告、規格文件與大型 codebase 的切片閱讀與證據整理。
- 需要頁碼、段落、檔案路徑、函式位置等可追溯引用的任務。
- 先縮小搜尋空間，再做局部語意判讀與整合。

### Out of scope
- 全文很短、可以直接讀完的文件。
- 只要自由摘要、心得或創意改寫，不要求證據鏈的任務。
- 任務核心是外部背景研究、文件重寫或 spec 整理。

## Primary use cases (2-3)

1) **從超長 PDF 找可引用證據**
- Trigger examples: 「讀這份 300 頁 PDF，找資料治理證據」「整理這份法規裡所有罰則頁碼」
- Expected result: 回覆包含結論、頁碼/段落定位與證據摘要。

2) **從大型程式碼庫找實作證據**
- Trigger examples: 「幫我從 codebase 找 auth flow 證據」「定位 rate limit 實作在哪裡」
- Expected result: 回覆包含檔案路徑、函式/模組位置與相關片段。

3) **整理跨多來源的可追溯證據鏈**
- Trigger examples: 「把長規格裡所有限制整理成清單」「比對多份文件中的相互矛盾處」
- Expected result: 保留來源差異與未解決缺口，不硬湊單一答案。

## Workflow overview

1. 先把來源切成可搜尋的 chunks，保留頁碼、檔名、路徑或其他定位資訊。
2. 用程式化方法縮小範圍：關鍵字、檔名、regex、結構欄位、抽樣與統計。
3. 只在需要語意判讀時才對候選片段做局部 LLM 分析。
4. 將證據整理成可追溯格式：來源位置、引用內容、重點、與問題的關聯。
5. 最後輸出答案時，優先保留證據鏈、限制與未證實缺口。

## Routing boundaries

- Neighboring skills / workflows:
  - `concept-alignment`：先整理背景知識與外部脈絡。
  - `technical-documentation-writer`：下一步是把證據改寫成文件。
  - `spec-organizer`：下一步是把發現整理成規格與驗收條件。
- Negative triggers:
  - 「幫我摘要這篇短文」
  - 「先上網查背景再開始」
  - 「幫我把文件重寫清楚」
- Handoff rule: 一旦任務重點從「找證據」轉成「寫文件、寫 spec 或做背景研究」，就應交給鄰近 skill。

## Language coverage

- Primary language(s): 繁體中文、英文。
- Mixed-language trigger phrases: PDF evidence、codebase evidence、page citation、traceability、repo search、spec evidence。
- Locale-specific wording risks: 使用者說「摘要」不一定等於證據閱讀；若沒有引用需求，通常不該啟動本 skill。

## Success criteria

### Quantitative (targets)
- 輸出必須包含可回指的位置資訊，如頁碼、段落、檔案路徑或 section header。
- 長文任務要先縮小搜尋空間，再進行局部語意分析。
- 找不到證據時要明確標示缺口，不得用推測補洞。

### Qualitative
- 回覆是 evidence-first，不是 vibe-first。
- 能區分已確認證據、衝突證據與待查缺口。
- 對使用者來說可直接回頭核對來源。

## Instructions

### Step 0: Confirm the evidence task
- 先確認問題是否真的需要長文證據閱讀，而不是一般摘要或外部研究。
- 若來源是 PDF、repo 或多份文件，先列出可用的切片單位與定位欄位。

### Step 1: Build a searchable context
- PDF 用頁或固定字數切片；repo 用檔案、模組或函式邊界切片。
- 每個 chunk 都要保留定位資訊，例如頁碼、檔名、路徑或 section header。
- 若環境允許，可使用 `scripts/load_pdf.py`、`scripts/load_codebase.py`、`scripts/context_store.py`。

### Step 2: Shrink the search space before summarizing
- 先用關鍵字、檔名、regex、欄位值或簡單統計縮小範圍。
- 不要一開始就把全部 chunk 丟進同一輪語意總結。
- 若需要候選召回，可使用 `scripts/bm25_index.py` 作為輕量輔助。

### Step 3: Extract evidence, not vibes
- 對候選片段逐一記錄：來源位置、關鍵引用、它回答了什麼問題、還缺什麼。
- 若片段彼此矛盾，明確保留差異與未解決處，不要硬湊一致說法。
- 若需要遞迴式局部判讀，可參考 `scripts/rlm_runner.py`、`scripts/rlm_repl.py` 與 `references/rlm_concepts.md`。

### Step 4: Deliver with traceability
- 最終輸出至少包含：結論、證據摘要、來源定位、已知限制。
- 若使用者要求精確引用，優先提供頁碼、檔案路徑或段落定位。
- 找不到證據時要直接說明，不要用推測補洞。

## Testing plan

### Should trigger
- 「讀這份 300 頁 PDF，整理跟資料治理有關的證據」
- 「幫我從這個 repo 找出和 auth flow 有關的實作證據」
- 「把這份長規格裡所有 rate limit 規則整理成可引用清單」

### Should not trigger
- 「幫我摘要這篇兩頁文章」
- 「先查 MCP 最近有哪些重大變化」
- 「幫我把這份說明文件重寫清楚」

### Functional tests
- 結果必須能回指到來源位置，而不是只有結論。
- 長文任務應先縮小搜尋空間，再做局部語意分析。
- 若證據不足，應明確標示缺口，而不是輸出看似完整的答案。

## Distribution notes

- Packaging: 由宿主或 registry 的標準 SKILL 發佈流程處理；若在本 repo 維護，再使用 repo 根目錄的打包腳本。
- Repo-level README belongs *outside* this skill folder.

## References

- `references/rlm-paper-cheatsheet.md`
- `references/rlm_concepts.md`
- `references/rlm_design_notes.md`
- `references/system_prompts.md`
- `scripts/load_pdf.py`
- `scripts/load_codebase.py`
- `scripts/bm25_index.py`
- `scripts/demo_cli.py`
  - 本地端到端示範入口；適合快速驗證 PDF / repo 問答流程是否可跑通。
- `scripts/rlm_providers.py`
  - `rlm_runner.py` / `demo_cli.py` 使用的 provider adapter；要替換模型供應商時先看這支。
- `scripts/rlm_runner.py`
