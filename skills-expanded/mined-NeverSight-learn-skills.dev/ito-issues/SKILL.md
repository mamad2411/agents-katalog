---
name: ito-issues
description: 從 PRD 拆出垂直 slice 任務清單，深度探索 codebase 後生成含驗收條件與 size 標籤的可執行任務，迭代確認後存至本地 Markdown 或推送為 GitHub sub-issues。適用於 PRD 完成後需拆任務或轉 GitHub issues 時。不適用於撰寫 PRD、直接實作功能、修改或關閉已建立的 GitHub issues。
---

# ito-issues

## 概覽

將完成的 PRD 拆成可執行垂直 slice，結合 codebase 深度探索產出有實際檔案脈絡的任務清單，使用者確認後選擇存至本地或開成 GitHub sub-issues。

## 使用時機

- PRD 已完成，需要拆成可由 agent 或開發者逐一執行的具體任務
- 需要將任務轉換成 GitHub sub-issues，並設定原生 blocked-by 依賴關係
- 使用者說「幫我拆任務」、「把 PRD 轉成 issues」、「task breakdown」

**不應使用的情況：** 撰寫或修改 PRD、直接實作功能、純技術架構討論、修改或關閉已建立的 GitHub issues。

## 核心流程

### 步驟 1：讀取 PRD

依 arg 格式自動判斷輸入來源：

- arg 為數字或 issue URL → `gh issue view <number> --comments`
- arg 為檔案路徑 → 讀取本地 Markdown 檔案
- 無 arg → 從對話內容讀取 PRD 描述

### 步驟 2：深度探索 codebase

PRD 讀取後，**必定**執行全面探索：

1. 現有目錄結構與模組邊界
2. PRD 提到的功能是否已有部分實作
3. 相關資料模型、API、元件的現有 pattern
4. 可能受影響的檔案與依賴鏈

使用 ast-grep 查找結構性 pattern，搭配 find 掌握目錄全貌。

### 步驟 3：識別依賴圖

整理各模組間的依賴關係，確認實作順序（以下為通用範例，依實際 codebase 架構調整）：

```
資料 schema
    │
    ├── API 資料模型 / 型別
    │       │
    │       ├── API endpoints
    │       │       │
    │       │       └── Frontend API client
    │       │               │
    │       │               └── UI 元件
    │       │
    │       └── 驗證邏輯
    │
    └── Seed data / migrations
```

實作順序由下往上：先建底層基礎，再往上層延伸。

### 步驟 4：生成計畫草稿

每個任務需貫穿所有需要的層（schema、API、UI、tests），完成後可獨立 demo 或驗證，避免水平切割（例：「建完整 DB schema」後才「建完整 API」）。

以探索結果產出計畫文件，結構依序為：

1. **架構決策**：探索後發現的關鍵架構決策與理由
2. **⚠️ 待確認清單**：PRD 與現有 codebase 有衝突或模糊的點
3. **任務清單**：垂直 slice 任務，穿插 Checkpoint

讀取 `assets/task-template.md`，依其格式填寫每個任務（標題、描述、驗收條件、Blocked by、預計碰的檔案、Size）。草稿可暫標 XL 表示任務過大需再拆，最終確認前必須拆完。S/M 是 agent 執行效果最佳的範圍。

### 步驟 5：草稿迭代確認

呈現完整草稿，詢問使用者：

- 有無 XL 任務須再拆（確認後才可進入步驟 6）
- 粒度是否合理（太粗 / 太細）
- 依賴關係是否正確
- ⚠️ 待確認的衝突點如何處理
- 需要合併或拆分哪些 slice

反覆調整至使用者確認，再進入步驟 6。

### 步驟 6：存至本地 Markdown

確認後存至 `docs/ito-temp/tasks/[主題].md`。

### 步驟 7：推 GitHub（選擇性）

詢問使用者是否推送至 GitHub。若是，先讀取 `references/github-api.md` 取得 mutation 範例，再依下列順序執行：

**必須按依賴順序建立 issues**，blockers 先建，才能拿到真實 issue 號碼填入後續的 blocked-by。

1. **確認 parent issue**：有提供 issue 號碼則直接使用。未提供則詢問是否建立新的 PRD parent issue，確認後用 `gh issue create` 建立
2. 每個 issue 用 `gh issue create`，title 格式為 `[#<parent>] Task title`，加上 `Task` 和對應 size label（`size/xs`、`size/s`、`size/m`、`size/l`）
3. 用 `gh api graphql` 執行 `addSubIssue` 將 task issue 掛到 parent
4. 用 `gh api graphql` 執行 `addBlockedBy` 設定依賴關係

## 常見合理化藉口

| 合理化藉口 | 實際情況 |
|-----------|---------|
| 「PRD 很清楚，不需要探索 codebase」 | 不探索就無法填 files touched，任務停在抽象層，agent 執行時才發現衝突 |
| 「先全部建成 issues，有問題再改」 | GitHub issues 建了不易批次修改，草稿迭代才是正確的確認時機 |
| 「依賴關係很直觀，不用標 Blocked by」 | 隱性依賴在任務多時必出錯，addBlockedBy 的原生關係在 GitHub 上才可視化 |
| 「這個 slice 有點大但還好」 | XL 任務讓 agent 中途迷失，應直接拆成 M 才能可靠執行 |

## 警訊

- 跳過 codebase 探索直接生成任務清單
- 任務之間沒有 Blocked by 關係，但描述裡有「完成後」、「接著」等字眼
- 出現水平切割（「建所有 schema」、「建所有 API」）
- Size 全部標 M，沒有思考拆分可能性
- 推 GitHub 時沒有按依賴順序建立 issues，導致 issue 號碼無法正確填入
- 對既有 issue 執行修改或關閉操作，包含 parent issue

## 錯誤處理

- 若 `gh api graphql` 執行 `addSubIssue` 失敗，確認 parent issue 的 node_id 是否正確後重試；若仍失敗，改以 issue body 補充「Parent: #N」作為 fallback。
- 若 `gh api graphql` 執行 `addBlockedBy` 失敗，在被 block 的 issue body 補上「Blocked by: #N」，並顯示警告提醒使用者手動確認依賴關係是否正確設定。
- 若 PRD 描述與 codebase 有明確衝突，在草稿的 ⚠️ 待確認清單標記，不自行決策，迭代確認時由使用者處理。
- 若使用者確認推 GitHub 但 repo 不存在或無寫入權限，停止並顯示錯誤，本地 Markdown 仍保留。

## 驗證

- [ ] 每個任務有標題、描述、至少兩條驗收條件、Blocked by、預計碰的檔案、Size
- [ ] 無 XL 任務（已拆或已標注原因）
- [ ] 推 GitHub 時 issues 依依賴順序建立，Blocked by 關係已用 `gh api graphql` 設定
- [ ] ⚠️ 待確認清單的衝突點已在迭代確認時由使用者處理

## 延伸參考

- `references/github-api.md`：addSubIssue 與 addBlockedBy 的 GraphQL mutation 範例
- `assets/task-template.md`：本地 Markdown 中單一任務的格式模板
