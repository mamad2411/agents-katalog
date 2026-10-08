---
name: task-start
description: Mark a task as in_progress when agent begins working
allowed-tools: Read, Edit, Glob, Bash
---

# 任務開始

Agent 開始執行任務時呼叫，將狀態從 `assigned` 改為 `in_progress`。

## 使用方式
```
/task-start <task-id>
```

## 參數
- `$0`: 任務 ID（如 `T5`）

## 執行步驟

1. 找到對應的任務檔案（支援 Sprint 子目錄）：
   使用 Glob tool 搜尋 `.tasks/**/$0-*.md`，若無結果再搜尋 `.tasks/**/$0.md`。
   取得檔案路徑後用 Read tool 讀取內容。

> 任務檔案可能在 `.tasks/sprint-{N}/T5-xxx.md`，不再只在 `.tasks/` 根目錄。

2. **取得真實時間（必要，不可跳過）**：
!`node -e "console.log(new Date().toISOString())"`
   > ⚠️ **禁止自行編造時間**。Agent 不知道真實時間，必須透過上述指令取得。將輸出存為變數 `$NOW` 供後續步驟使用。

3. 更新找到的任務檔案：
   - 將 `| 狀態 | ... |` 改為 `| 狀態 | in_progress |`
   - 將 `| 開始時間 | ... |` 改為 `| 開始時間 | $NOW |`
   - **若 `開始時間` 已有非 `—` 的值，不覆蓋**（代表曾被 blocked 後恢復，保留首次開始時間）
   - **若找不到 `| 開始時間 |` 欄位**，在 `| 建立時間 |` 行之後插入 `| 開始時間 | $NOW |`

4. **依賴檢查（必要）**：
   - 讀取任務檔的 `| 依賴 |` 欄位
   - 若不為 `—`，使用 Glob tool 逐一找到依賴任務檔，確認其 `| 狀態 |` = `done`
   - 任一依賴狀態非 `done` → 輸出 block 訊息並停止：
     ```
     ⛔ $0 無法開始：依賴 {T?} 狀態為 {狀態}，尚未完成
     ```
   - 全部 done → 繼續

5. **事件紀錄（必要，不可跳過）**：在 `## 事件紀錄` 區塊底部 append：
   ```
   ### $NOW — 狀態變更 → in_progress
   開始執行任務
   ```

6. **Git Branch 處理**：
   讀取任務檔的 `| 並行組 |` 欄位：

   **若 `並行組 = —`（循序任務）：**
   - 確認當前 branch 為 `sprint-{N}`（從任務檔 Sprint 欄位取 N）
   - 若不在正確 branch，切換：`git checkout sprint-{N}`
   - 輸出：`📌 循序任務，在 sprint-{N} 直接開發`

   **若 `並行組 = A/B/C...`（並行任務）：**
   - 從任務標題產生 slug（小寫 kebab-case，最長 30 字元）
   - 從 sprint-{N} 建立 task branch：
     ```bash
     git checkout sprint-{N}
     git checkout -b task/s{N}-$0-{slug}
     ```
   - 輸出：`🌿 並行任務，已建立 branch: task/s{N}-$0-{slug}`

7. 輸出確認：
```
▶️ $0 狀態已更新為 in_progress
```
