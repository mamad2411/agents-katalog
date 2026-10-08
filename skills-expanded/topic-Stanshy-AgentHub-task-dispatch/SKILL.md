---
name: task-dispatch
description: Boss dispatches tasks — auto-create .tasks/ files and record in dev-plan
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# 任務下達

老闆在 Session 中下達任務指令，自動建立 `.tasks/sprint-{N}/` 並記錄到 dev-plan。

## 使用方式
```
/task-dispatch $ARGUMENTS
```

## 輸入格式

```
任務: T3 — 移除 19 個服務
指派: backend-architect
優先級: P0
依賴: T2
預估: 2h
驗收標準:
- 19 個服務檔案已刪除
- 保留 14 個核心服務
- typecheck 通過
```

支援批次（用 `---` 分隔多個任務）。

## 執行步驟

1. **解析 `$ARGUMENTS`**，提取：
   - 任務 ID + 名稱（如 `T3 — 移除 19 個服務`）
   - 指派對象（agent-id）
   - 優先級（P0/P1/P2，預設 P1）
   - 依賴（可選，如 `T2`）
   - 預估工時（可選，如 `2h`）
   - 驗收標準（checkbox list）

2. **取得真實時間（必要，不可跳過）**：
!`node -e "console.log(new Date().toISOString())"`
   > ⚠️ **禁止自行編造時間**。Agent 不知道真實時間，必須透過上述指令取得。將輸出存為變數 `$NOW` 供後續步驟使用（用於 `建立時間` 和事件紀錄的 timestamp）。

3. **讀取當前 Sprint 的 dev-plan**：
!`ls -t proposal/sprint*-dev-plan.md 2>/dev/null | head -1`

4. **偵測當前專案名稱**（從 CLAUDE.md 或 dev-plan 標題提取）

5. **為每個任務建立 `.tasks/sprint-{N}/{ID}-{kebab-case}.md`**，使用以下格式：

> **⚠️ Sprint 子目錄規則**：
> - 從 dev-plan 標題或 Sprint 資訊判斷當前 Sprint 編號
> - 建立目錄：`mkdir -p .tasks/sprint-{N}`
> - 任務檔案路徑範例：`.tasks/sprint-1/T3-remove-services.md`
> - **禁止** 直接放在 `.tasks/` 根目錄（會導致跨 Sprint ID 衝突）

### 欄位格式規範（系統解析依賴）

| 欄位 | 格式 | 範例 | 說明 |
|------|------|------|------|
| ID | `TN` | `T1`, `T3` | T + 數字 |
| Sprint | `Sprint N` | `Sprint 1` | **必須此格式**，系統靠名稱比對 DB 中的 Sprint UUID |
| 狀態 | 英文小寫 | `created` | 合法值：created/assigned/in_progress/in_review/blocked/done |
| 優先級 | `P0`/`P1`/`P2` | `P0` | — |
| 建立時間 | ISO 8601 | `2026-03-26T12:00:00.000Z` | — |
| 依賴 | 逗號分隔 ID | `T1,T3` | 無依賴填 `—` |
| 並行組 | 字母或 `—` | `A` | 同組任務可並行；循序任務填 `—` |

```markdown
# {任務名稱}

| 欄位 | 值 |
|------|-----|
| ID | {ID} |
| 專案 | {專案名} |
| Sprint | Sprint {N} |
| 指派給 | {agent-id} |
| 優先級 | {P0/P1/P2} |
| 狀態 | assigned |
| 依賴 | {依賴任務 ID，無則填 —} |
| 並行組 | {A/B/C... 或 —} |
| 預估 | {預估工時，無則填 —} |
| 建立時間 | $NOW |
| 開始時間 | — |
| 完工時間 | — |

---

## 任務描述

{從指令中提取的任務說明}

## 驗收標準

- [ ] {逐項列出}

---

## 事件紀錄

### $NOW — 建立任務（assigned）
由老闆透過 /task-dispatch 派工
```

6. **更新 dev-plan 第 6 節任務表**（append 新任務行）：
```
| {ID} | {說明} | {負責} | {依賴} | {預估} |
```

7. **輸出摘要**：
```
✅ 已建立 N 個任務：
- T3: 移除 19 個服務 → backend-architect (P0, 依賴 T2)
- T4: ...
```
