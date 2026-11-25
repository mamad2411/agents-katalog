---
name: longform-writing-process
description: 在使用者要把零散想法推進成長文初稿、審稿與完稿流程時使用。常見觸發像「幫我寫長文」「做多輪審稿」「把草稿修成可發表文章」。輸出 draft、review 與修訂記錄；不適合只要一小段文案或 PRD。
version: 2026.3.31
homepage: https://github.com/AllanYiin/skills/tree/main/skills/longform-writing-process
license: MIT
metadata: {"author":"Allan Yiin","language":"zh-TW","category":"writing","short-description":"長文寫作、改寫、多人評審與小編修訂工作流程","openclaw":{"emoji":"✍️"}}
---

# Longform Writing Process

## Purpose

這個 skill 用來把零散筆記、口頭需求或半成品草稿，推進成可發表的長文。核心不是一次寫完，而是先做概念對齊，再產出初稿、安排評審、回收意見，最後由小編整合成較穩定的完稿。

## Scope

### In scope
- 部落格文章、評論、分析稿、白皮書草稿與長篇說明文的完整寫作流程。
- 需要多輪審稿、角色評審、修訂追蹤與查核的寫作任務。
- 從寫作契約、草稿、review rounds 到 final draft 的流程化交付。

### Out of scope
- 只要一小段文案、Email、社群貼文或單次潤稿。
- PRD、技術 spec、README、runbook、投影片內容規劃。
- 使用者明確只要快速短稿、不想跑多輪寫作流程。

## Primary use cases (2-3)

1) **把零散筆記推進成長文初稿**
- Trigger examples: 「幫我把這些筆記整理成一篇文章」「先做出長文草稿」
- Expected result: 先產出寫作契約與 Draft v0，讓後續 review 有明確載體。

2) **多輪審稿與修訂追蹤**
- Trigger examples: 「這篇文章要做兩輪審稿」「請幫我安排 reviewer 角色」
- Expected result: 每輪 review 都有角色差異、必修/可選修改與整合記錄。

3) **先查核再成文**
- Trigger examples: 「先查資料再寫分析稿」「有些數據要核對後再下筆」
- Expected result: 在寫作前完成必要查核，並保留主要來源與限制。

## Workflow overview

1. 萃取寫作規格：目的、受眾、語氣、篇幅、成功標準與禁區。
2. 先做概念對齊與必要查核，建立知識邊界與主要來源。
3. 產出 Draft v0，先形成可評審的載體。
4. 逐一切換評審角色做 Round 1，回收必修與可選修改。
5. 由小編整合意見、補資料、重寫結構，產出 Draft v1。
6. 再做 Round 2 聚焦審稿，最後輸出完稿與參考資料。

## Routing boundaries

- Neighboring skills / workflows:
  - `concept-alignment`：任務先要做背景研究與概念對齊。
  - `technical-documentation-writer`：輸出是技術文件而不是長文論述。
  - `humanize-text`：內容已完成，只需要自然化與去機器味。
  - `spec-organizer`：需求本質是產品或工程規格。
- Negative triggers:
  - 「幫我寫 README」
  - 「潤一下這段貼文」
  - 「幫我整理 PRD」
- Handoff rule: 若主要產物不是長文，而是文件、spec、簡報或短文案，就不應硬用本流程。

## Language coverage

- Primary language(s): 繁體中文、英文。
- Mixed-language trigger phrases: draft、review round、whitepaper、analysis essay、editorial review、fact check。
- Locale-specific wording risks: 使用者說「文章」有時其實指文件或貼文，需先用寫作契約確認產物類型。

## Success criteria

### Quantitative (targets)
- 必須先有寫作契約，再進入草稿與審稿。
- 每輪評審都要逐角色輸出，而不是只有彙總評論。
- Final draft 應保留主要來源、限制與修訂脈絡。

### Qualitative
- 流程清楚可追蹤，不是一次性自由發揮。
- 能平衡內容結構、事實查核與文字可讀性。
- reviewer feedback 有被具體採納或明確拒絕。

## Instructions

### Step 0: Lock the writing contract
- 先整理文章要解決什麼讀者問題、給誰看、用什麼語氣、成功標準是什麼。
- 若資訊不足，用最小風險假設補上，但要明示假設邊界。

### Step 1: Align facts before drafting
- 題目若涉及可變動事實、數據、政策、法規、人物職稱或事件進度，先做查核。
- 保留主要來源清單，避免寫到後面才補引用。
- 查核結果若不穩或彼此衝突，要先說清楚，不要直接寫死單一路徑。

### Step 2: Draft for review
- 先產出 Draft v0，重點是讓評審有東西可看，不求一次完美。
- 結構預設包含：導語、主體論點、反方或限制、結論與下一步。
- 每節都要能對應到寫作契約，不要只堆素材。

### Step 3: Run review rounds with clear roles
- 評審要逐一進場，每個角色都要給出：必修、可選強化點、具體改動指令。
- 先完成逐評審輸出，再整理當回合總結；不要直接用總結取代角色差異。
- 角色設定可參考 `references/role-factory-snippets.md`。

### Step 4: Edit with traceability
- 小編要維護意見追蹤紀錄：來源角色、意見摘要、處理動作、改動位置、未採納理由。
- Draft v1 與 Final 都應是完整文章，不要夾帶零碎註解。
- 最後再做自然化與段落銜接，不要在早期為了文采犧牲結構。

## Testing plan

### Should trigger
- 「幫我把這些筆記整理成一篇可發表長文」
- 「這篇文章要做兩輪審稿再完稿」
- 「先查資料，再寫出一篇分析稿」

### Should not trigger
- 「幫我寫 README」
- 「把這段貼文潤得自然一點」
- 「幫我整理 PRD」

### Functional tests
- 必須先有寫作契約，再進入草稿與審稿。
- 評審要逐角色輸出，不能只剩一份大雜燴總結。
- 完稿應保留來源、限制與主要修訂脈絡。

## Distribution notes

- Packaging: 由宿主或 registry 的標準 SKILL 發佈流程處理；若在本 repo 維護，再使用 repo 根目錄的打包腳本。
- Repo-level README belongs *outside* this skill folder.

## References

- `references/output-template.md`
- `references/role-factory-snippets.md`
- `references/text_humanization_guidelines.md`
