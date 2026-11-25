---
name: ito-explain
description: 探索 codebase 並回答「X 是怎麼運作的？」問題，產出結構化架構說明。適用於使用者說「解釋 X」、「X 怎麼運作」、「想了解 X 的架構」或輸入 /ito-explain 時。不適用於實作、撰寫或修改程式碼。
---

# ito-explain

## 概覽

探索 codebase，回答「X 是怎麼運作的？」類型的問題，以資深工程師上手新模組的深度產出結構化說明。

## 使用時機

- 使用者說「解釋一下 X 怎麼運作」、「X 的架構是什麼」、「帶我了解 X」
- 使用者輸入 `/ito-explain [問題]`

**不應使用的情況：** 需要直接實作、撰寫或修改程式碼的任務。

## 核心流程

### 步驟 1：理解問題、評估複雜度

解析問題範圍：

- 單一 module 或小型 utility（「X function 怎麼運作？」）→ **simple**，跳至步驟 2b
- 跨多個檔案或服務的子系統、全架構概覽、跨切面 feature → **complex**，進入步驟 2a

問題模糊時，陳述自己的解讀後直接開始探索，讓使用者事後導正，不先詢問確認。

### 步驟 2a：平行探索（complex 問題）

將問題分解為 2–4 個互不重疊的探索角度（例：資料模型 / 渲染流程 / scroll 基礎設施）。

在**同一則訊息**中一次平行 spawn 全部唯讀 codebase 探索 subagent，每個 subagent 的 prompt：讀取 `references/explorer-prompt.md`，填入原始問題與各自的探索角度後傳入

探索 subagent 回傳後進入步驟 3。

### 步驟 2b：直接解釋（simple 問題）

Spawn 單一通用推理 subagent，prompt：讀取 `references/explainer-prompt.md`，填入原始問題（無 explorer 輸入）後傳入。（explainer 模板已指示 agent 於無 explorer 輸入時自行探索 codebase）

完成後跳至步驟 4。

### 步驟 3：彙整（complex 問題）

所有探索 subagent 回傳後，spawn 單一通用推理 subagent，prompt：讀取 `references/explainer-prompt.md`，填入所有探索 subagent 輸出後傳入

完成後進入步驟 4。

### 步驟 4：呈現與存檔

呈現說明（可輕微潤飾，不大幅改寫）。

說明結束後詢問使用者是否存檔：

> 說明已完成。是否儲存為 markdown 檔案？（若含流程圖，終端機無法直接渲染）

若使用者同意，請使用者指定路徑，或預設存至 `docs/ito-temp/[主題]-explain.md`。

## 輸出格式

完整規格詳見 `references/explainer-prompt.md`。概覽：依問題性質取捨概覽、核心概念、運作方式、相關位置、注意事項等段落，不必全數輸出；以使用者提問的語言輸出。

## 常見合理化藉口

| 合理化藉口 | 實際情況 |
|---|---|
| 「問題看起來簡單，直接回答就好」 | 不探索 codebase 直接回答，說明可能與實際實作不符 |
| 「parallel explorers 浪費資源，用單一 agent 跑 complex 問題就夠了」 | 單一 agent 在大型子系統容易遺漏角度，平行探索覆蓋率明顯更高 |
| 「沒有圖也看得懂」 | 多元件互動或資料轉換流程，圖比文字省讀者 30 秒 |
| 「不用問存檔，直接輸出就好」 | 說明本身就有留存價值，不詢問等於讓使用者自己去複製貼上 |

## 警訊

- simple / complex 判斷前未解析問題範圍
- complex 問題的 explorer agent 未在同一則訊息中一次 spawn
- 說明結束後未詢問存檔
- 說明與 codebase 實際結構不符（未經探索直接生成）

## 驗證

- [ ] 問題範圍已評估，路由正確（simple / complex）
- [ ] Complex 問題的 explorer agent 已平行 spawn
- [ ] 說明涵蓋原始問題的所有主要角度
- [ ] 已詢問使用者是否存檔

## 延伸參考

- `references/explorer-prompt.md`：explorer agent 的 prompt 模板，步驟 2a spawn 時讀取
- `references/explainer-prompt.md`：explainer / synthesizer agent 的 prompt 模板，步驟 2b 與步驟 3 spawn 時讀取
