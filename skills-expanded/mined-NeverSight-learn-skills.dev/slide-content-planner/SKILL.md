---
name: slide-content-planner
description: 在使用者要規劃投影片內容、故事線與逐頁重點時使用。常見觸發像「做簡報大綱」「規劃 pitch deck」「整理逐頁訊息」。輸出逐頁內容規劃與視覺元素表；不直接製作 PPTX 或 SVG。
version: 2026.3.31
homepage: https://github.com/AllanYiin/skills/tree/main/skills/slide-content-planner
license: MIT
metadata: {"author":"Allan Yiin","language":"zh-TW","category":"presentation","short-description":"投影片內容規劃、證據整理與視覺版面編排流程"}
---

# Slide Content Planner

## Purpose

把「做一份吸睛、可落地製作的簡報」拆成可重複執行的規劃流程。交付物固定包含：
1) 【信息抽取】供使用者確認（或在 /autorun 下以假設值標註）。
2) 【投影片內容規劃】逐頁：標題、單頁核心訊息、支撐論點/證據、建議講稿與轉場。
3) 【視覺元素規劃表】逐頁：關鍵視覺元素、色塊安排、視覺動線、圖示/圖表建議與資料來源需求。

## Scope

### In scope
- 依使用者輸入（與附件內容）完成簡報的「內容架構」與「逐頁內容規劃」。
- 以第一性原理反推：簡報根本目的、受眾期待、說服與共鳴設計。
- 同步規劃每頁視覺化重點（避免只寫文字）。
- 如缺乏背景知識或需數據/新聞支撐：可上網查證並在規劃中標註資料來源需求。

### Out of scope
- 不在未被要求時直接產出最終 PPTX/SVG 成品。
- 不處理實作層面的 SVG 產出、PPTX 匯出與檔案打包；這類製作與交付工作交給 `pptx-maker`。

## Primary use cases (2-3)

1) **新簡報：從零產出逐頁內容規劃**
- Trigger examples: 「幫我規劃一份關於 X 的簡報」「我要做投影片大綱，受眾是…」「請做一份含封面與 Q&A 的簡報內容規劃」
- Expected result: 交付「信息抽取」+「逐頁內容規劃」+「視覺元素規劃表」，頁數符合需求（或合理自動配置），且每頁都有可視覺化的重點。

2) **/run：逐步工作流程（需中途確認）**
- Trigger examples: 「/run\n主題：…」「請用 /run 跑流程」
- Expected result: 先輸出【信息抽取】並請使用者確認；確認後再輸出下一階段（內容規劃→視覺元素表）。

3) **/autorun：一次完成（不中斷請示）**
- Trigger examples: 「/autorun\n主題：…」「不要問我，直接給最終規劃」
- Expected result: 在同一回合完成所有交付物；對缺失資訊以明確假設值標註，並在最後列出需要使用者補充/修正的欄位清單。


## Workflow overview

1) 信息抽取（填齊 6 欄位 + 附件/限制）
2) 簡報根本目的與受眾期待（1-2 段）
3) 投影片內容規劃（逐頁：封面→內文→結尾→Q&A；不需目錄頁）
4) 視覺意象衍生（至少 3 種）
5) 視覺元素規劃表（逐頁完成；標註資料來源需求）
6) QA：檢查是否有「文字堆疊、視覺疲勞、缺乏證據、缺封面/Q&A」等問題

## Routing boundaries

- Neighboring skills / workflows:
  - `pptx-maker`：真正要把內容落成 PPTX、SVG 或修改既有 deck。
  - `technical-documentation-writer`：輸出是文件而不是簡報。
  - `concept-alignment`：任務先要做背景知識與重大事件整理。
- Negative triggers:
  - 「把這份 PPTX 的字改成 18pt」
  - 「把這批 SVG 轉成 PPTX」
  - 「幫我做一張海報」
- Handoff rule: 一旦任務從內容規劃轉成投影片製作或檔案修改，就交給 `pptx-maker`。

## Language coverage

- Primary language(s): 繁體中文、英文。
- Mixed-language trigger phrases: pitch deck、slide outline、Q&A slide、speaker note、visual direction。
- Locale-specific wording risks: 使用者說「做簡報」有時是要規劃內容，有時是要直接做檔案，需先區分。

## Success criteria

### Quantitative (targets)
- 交付物完整度：100% 含封面與 Q&A，且不含目錄頁。
- 視覺化覆蓋率：100% 內文頁都有至少 1 個清楚的視覺重點（圖示/圖表/資訊圖/結構化模組）。
- 來源標註：凡涉及新聞或數據之頁面，規劃中必有「來源/查證需求」。

### Qualitative
- 架構有敘事張力（問題→洞見→方案→行動），不是條列堆疊。
- 每頁都能「一眼看懂」核心訊息（one-slide one-takeaway）。
- 受眾可做出期望行為改變/觀點更新。
- 線下投影場景若未證實有高亮 LED 且無列印需求，預設採高對比淺色模式與大字級規劃，而不是沿用螢幕導向的深色小字美感。

## Instructions

### Step 0: Confirm inputs
先抽取/確認下列欄位（不足者用「未提供」或合理預設並標註）：
- ✅ 簡報主題
- ✅ 希望受眾改變的行為或理解的觀點
- ✅ 受眾背景（角色/產業/痛點/決策權限）
- ✅ 是否已有預定頁數（若無則自動安排）
- ✅ 觀看與輸出情境（線下投影 / 線上分享 / 高亮 LED / 是否要列印講義）
- ✅ 主色調指定（若無：橙＋灰）
- ✅ 投影片寬高比（預設 16:9）

環境預設：
- 若是實體演講且未確認高亮 LED 與無列印需求，預設規劃成「白/淺灰底 + 深色字」的高對比淺色模式。
- 若是大型實體場地，預設用大字級思維規劃內容：標題約 80-120px，內文/副標至少 32-48px；若塞不下，優先拆頁或刪減，而不是縮字。

模式判定：
- 若使用者以 `/run` 開頭：只做 Step 0 並請對方確認後停止。
- 若以 `/autorun` 開頭：全流程一次完成；缺失資訊以假設值標註。
- 若未指定：仍要先輸出 Step 0（含假設），但不要卡住；直接給「草案版」內容規劃並在結尾列出待確認項。

### Step 1: Define objective (first principles)
用 4 個句子內回答：
- 受眾現在相信/做什麼？為什麼？
- 簡報結束後希望他們相信/做什麼？
- 需要跨越的阻力（認知、成本、風險、組織流程）是什麼？
- 你要用什麼「證據與結構」讓他們願意改變？
- 若受眾已有基礎，不要只排「功能 A / 功能 B / 功能 C」；優先把技術點提升成對比式洞見，例如舊世界 vs 新世界、舊問題 vs 新解法、 deterministic bug vs probabilistic failure。

### Step 2: Build slide-level story
先套兩個守門規則：
- 嚴格執行「3 秒法則」：觀眾應能在 3 秒內讀懂該頁表面的文字。完整句、定義展開與細節推導留給 `Speaker note`。
- 逐頁表面文字只保留巨大數字、關鍵詞、短標籤或圖表標示；若必須寫長句，表示這頁還沒刪乾淨。

產出逐頁規劃（含封面與 Q&A，不需目錄頁）。每頁固定欄位：
- Slide title（≤ 10 字優先）
- One-slide takeaway（1 句話）
- Supporting points（2–4 點，偏結構化；以詞組優先，不寫滿句）
- Evidence needed（數據/案例/新聞/引用；若需上網查證則列出關鍵查詢）
- Speaker note（建議講稿 2–3 句，含轉場）

### Step 3: Derive visual direction
- 先依實體載體決定視覺基底：線下投影預設高對比淺色模式；只有在已確認高亮 LED、環境可控且無列印需求時，才把深色模式當可選項。
- 至少延伸 3 種視覺意象（metaphor/imagery）可貫穿整份簡報。
- 每頁都指定至少 1 個視覺化主角（icon/diagram/chart/table/infographic 模組）。
- 避免連續多頁使用同一種版型造成視覺疲勞（至少 3 種版型輪替）。
- 若觀眾距離遠或場地大，字級與留白優先於細碎裝飾；塞不下時先減字或拆頁，不要退回網頁式小字排版。

### Step 4: Produce “視覺元素規劃表”
使用下列表格欄位（模板見 `references/visual_elements_table_template.md`）：
- 頁碼 / 主題 / 關鍵視覺元素 / 色塊安排 / 視覺動線 / 特殊圖示建議 / 備註（含資料來源需求）
- 若要快速產出空白表骨架，可用 `scripts/make_visual_table.py` 生成初版 markdown 表格。

### Step 5: Finalization and QA
對照 `references/quality_checklist.md` 做自檢，至少涵蓋：
- 有無「只有文字」的頁面
- 封面是否有明確主視覺（不可只放素面文字）
- 是否每頁只有一個核心訊息
- 數據/新聞頁是否規劃了來源註記
- 逐頁表面文字是否能在 3 秒內讀完
- 若為線下投影，是否已預設高對比淺色模式與大字級，而不是沿用深色小字設計

（若使用者下一步要求真正產出 SVG 或 PPTX）
- 明確轉交 `pptx-maker`。
- 若只是要補強視覺方向，可先提供 `references/visual_design_rules.md` 給後續製作階段參考。

## Testing plan

### Triggering tests
- Should trigger:
  - 「幫我規劃一份關於 ESG 的簡報內容」
  - 「投影片大綱：主題是 AI 治理，受眾是董事會」
  - 「/run\n主題：新產品上市策略」
  - 「/autorun\n我要一份 12 頁 pitch deck 規劃」
- Should NOT trigger:
  - 「把這份 PPTX 的字改成 18pt」
  - 「把這批 SVG 轉成 PPTX」
  - 「幫我把 SVG 轉成 PNG」
  - 「介紹一下瑞士風格設計史」
  - 「請幫我做一張海報」

### Functional tests
- Test case: B2B SaaS 產品 pitch（未指定頁數）
  - Given: 主題/受眾/目標行為/限制條件
  - When: 產出內容規劃
  - Then: 自動配置合理頁數；含封面與 Q&A；每頁含視覺化主角；並列出數據/案例需求。

### Performance comparison (optional)
- Baseline (no skill): 容易變成條列堆疊，缺乏逐頁結構與視覺化規劃。
- With skill: 輸出固定欄位與 QA；可直接交給設計/製作流程落地。

## Distribution notes

- Packaging: 由宿主或 registry 的標準 SKILL 發佈流程處理；若在本 repo 維護，再使用 repo 根目錄的打包腳本。
- Repo-level README belongs *outside* this skill folder.

## Troubleshooting

- Symptom: 規劃結果太空泛、沒有證據支撐
  - Cause: 目標行為與受眾痛點未具體化
  - Fix: 回到 Step 1，補上「阻力」與「證據」欄位；必要時上網查證並列來源需求。

- Symptom: 多頁內容重複、視覺疲勞
  - Cause: 沒有輪替版型與視覺化模組
  - Fix: Step 3 增加至少 3 種版型輪替，並在視覺元素表中明確標示。

- Symptom: 頁數爆炸、字太小、觀眾必須低頭讀字
  - Cause: 把講者要說的話直接搬上投影片，或沿用螢幕閱讀的字級假設
  - Fix: 回到 Step 2 執行 3 秒法則，只保留關鍵字與對比；回到 Step 0/3 用大型場地的大字級與高對比淺色模式重排。

## Resources

- `references/quality_checklist.md`
- `references/visual_elements_table_template.md`
- `references/test_plan.md`
  - 觸發與功能測試案例。
- `references/svg_production_rules.md`
  - 後續需要把內容交給 SVG / 投影片製作階段時使用的製作規範。
-（選用）`references/visual_design_rules.md`：若要進入視覺設計階段
- `scripts/make_visual_table.py`
  - 自動產生視覺元素規劃表骨架，避免手動表格格式錯誤。
