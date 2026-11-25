---
name: task-status
description: Update task status and append event log in .tasks/ file
allowed-tools: Read, Edit, Glob
---

# 任務狀態更新

任意角色更新任務狀態（中間狀態），自動追加事件紀錄。

## 使用方式
```
/task-status {task-id} {new-status} {備註（可選）}
```

## 範例
```
/task-status T3 in_progress L1 分派給 backend-architect 執行
/task-status T5 blocked 等待 T4 完成
/task-status T7 assigned 已分派給 frontend-developer
```

## 合法狀態（系統解析依賴，務必使用英文小寫值）

| 狀態值 | 說明 | 系統對應 |
|--------|------|---------|
| `created` | 已建立，尚未分配 | created |
| `assigned` | 已分配，尚未開始 | assigned |
| `in_progress` | 進行中 | in_progress |
| `in_review` | 審查中 | in_review |
| `blocked` | 被阻塞 | blocked |
| `done` | 完成（建議改用 /task-done） | done |
| `rejected` | 被退回 | rejected |

> **禁止**使用中文狀態值（如「進行中」）或自定義值。
> 系統解析器 `normalizeStatus()` 可容忍 `✅ 完成` / `🔄 進行中` 等 emoji 前綴格式，
> 但 `.tasks/` 檔案的狀態欄位**必須使用純英文值**。

## 執行步驟

1. **解析參數**：從 `$ARGUMENTS` 提取 task-id、new-status、備註

2. **找到任務檔案**（支援 Sprint 子目錄）：
   使用 Glob tool 搜尋 `.tasks/**/$0-*.md`，若無結果再搜尋 `.tasks/**/$0.md`。
   取得檔案路徑後用 Read tool 讀取內容。

> 任務檔案可能在 `.tasks/sprint-{N}/T3-xxx.md`，不再只在 `.tasks/` 根目錄。

3. **取得真實時間（必要，不可跳過）**：
!`node -e "console.log(new Date().toISOString())"`
   > ⚠️ **禁止自行編造時間**。Agent 不知道真實時間，必須透過上述指令取得。將輸出存為變數 `$NOW` 供後續步驟使用。

4. **更新狀態欄位**：將 `| 狀態 | xxx |` 修改為 `| 狀態 | {new-status} |`

5. **事件紀錄（必要，不可跳過）**：在 `## 事件紀錄` 區塊底部 append：
```markdown
### $NOW — 狀態變更 → {new-status}
{備註}
```

6. **完成提示**：
   - 如果 new-status 是 `done`，提示用戶改用 `/task-done`（因為 done 需要同步更新 dev-plan 第 10 節）
   - 否則輸出確認訊息：`✅ {task-id} 狀態已更新為 {new-status}`
