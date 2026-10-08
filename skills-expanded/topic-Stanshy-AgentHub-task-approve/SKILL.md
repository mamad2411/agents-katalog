---
name: task-approve
description: Mark a task as done after L1 review passes
allowed-tools: Read, Edit, Glob, Bash
---

# 任務審核通過

L1 Review 通過後呼叫，將狀態從 `in_review` 改為 `done`。

## 使用方式
```
/task-approve <task-id> [備註]
```

## 參數
- `$0`: 任務 ID（如 `T5`）
- `$ARGUMENTS`: 完整參數（含備註）

## 格式規範（系統解析依賴，務必遵守）

### .tasks/ 狀態欄位
| 狀態值 | 說明 |
|--------|------|
| `done` | L1 審核通過 |

### dev-plan 第 10 節「結果」欄位（第 3 欄）
| 結果值 | 對應系統狀態 | 說明 |
|--------|-------------|------|
| `✅ 完成` | done | 審核通過 |

## 執行步驟

1. 找到對應的任務檔案（支援 Sprint 子目錄）：
使用 Glob tool 搜尋 `.tasks/**/$0-*.md`，若無結果再搜尋 `.tasks/**/$0.md`。
   取得檔案路徑後用 Read tool 讀取內容。

> 任務檔案可能在 `.tasks/sprint-{N}/T5-xxx.md`，不再只在 `.tasks/` 根目錄。

2. **取得真實時間（必要，不可跳過）**：
!`node -e "console.log(new Date().toISOString())"`
   > ⚠️ **禁止自行編造時間**。Agent 不知道真實時間，必須透過上述指令取得。將輸出存為變數 `$NOW` 供後續步驟使用。

3. 更新找到的任務檔案：
   - 將 `| 狀態 | ... |` 改為 `| 狀態 | done |`
   - 將 `| 完工時間 | ... |` 改為 `| 完工時間 | $NOW |`
   - **若找不到 `| 完工時間 |` 欄位**，在 `| 建立時間 |` 行之後插入 `| 完工時間 | $NOW |`

4. **事件紀錄（必要，不可跳過）**：在 `## 事件紀錄` 區塊底部 append：
   ```
   ### $NOW — 狀態變更 → done
   L1 審核通過。{備註}
   ```

5. **Git Merge（並行任務）/ 確認（循序任務）**：
   讀取任務檔的 `| 並行組 |` 欄位：

   **若 `並行組 = —`（循序任務）**：
   - code 已在 sprint-{N}，無需 merge
   - 輸出：`📌 循序任務，code 已在 sprint-{N}`

   **若 `並行組 = A/B/C...`（並行任務）**：
   - 取得 sprint 編號（從任務檔 Sprint 欄位）
   - 執行 merge：
     ```bash
     git checkout sprint-{N}
     git merge --no-ff task/s{N}-$0-{slug} -m "feat($0): {任務標題}"
     git branch -d task/s{N}-$0-{slug}
     ```
   - 若 merge 有衝突 → 停止，列出衝突檔案，由人工解決後繼續
   - 輸出：`🔀 task/s{N}-$0-{slug} 已 merge 進 sprint-{N}，branch 已刪除`

6. 找到當前 dev-plan：
   使用 Glob tool 搜尋 `proposal/sprint*-dev-plan.md`，取最新一份用 Read tool 讀取。

7. 在 dev-plan 第 10 節「任務完成紀錄」表格，找到對應任務行並更新：
```
| $0 | {YYYY-MM-DD} | ✅ 完成 | {備註} |
```

8. 輸出確認：
```
✅ $0 審核通過，狀態已更新為 done
```
