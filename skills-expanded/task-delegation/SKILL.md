---
name: task-delegation
description: Create task breakdown in dev plan section 6 and generate .tasks/ files
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# 任務拆解與分派

在開發計畫書第 6 節建立任務表，同時產生 `.tasks/sprint-{N}/TN-xxx.md` 檔案。

## 使用方式
```
/task-delegation
```

## 執行步驟

1. 讀取當前 Sprint 的 dev-plan：
!`ls -t proposal/sprint*-dev-plan.md 2>/dev/null | head -1 | xargs cat 2>/dev/null || echo "找不到 dev-plan"`

2. 根據第 3 節（檔案變更清單）和技術方案，拆解任務

3. 更新 dev-plan 第 6 節任務表：
```
| 任務 | 說明 | 負責 | 依賴 | 預估 |
|------|------|------|------|------|
| T1 | ... | backend-architect | — | 1h |
```

4. **取得真實時間（必要，不可跳過）**：
!`node -e "console.log(new Date().toISOString())"`
   > ⚠️ **禁止自行編造時間**。將輸出存為 `$NOW` 供後續步驟使用（建立時間與事件紀錄 timestamp）。

5. 為每個任務建立 `.tasks/sprint-{N}/TN-{kebab-case-name}.md`：

> **⚠️ Sprint 子目錄規則**：任務檔案必須放在對應 Sprint 的子目錄下。
> - Sprint 1 的任務 → `.tasks/sprint-1/T1-xxx.md`
> - Sprint 2 的任務 → `.tasks/sprint-2/T3-xxx.md`
> - 如果目錄不存在，先建立：`mkdir -p .tasks/sprint-{N}`
> - **禁止** 直接放在 `.tasks/` 根目錄（會導致跨 Sprint ID 衝突）

### 格式規範（系統解析依賴，務必遵守）

| 欄位 | 格式 | 說明 |
|------|------|------|
| ID | `TN` | T + 數字，如 T1, T2, T10 |
| Sprint | `Sprint N` | **必須用 `Sprint N` 格式**（如 `Sprint 1`），系統用此名稱對應 DB 中的 Sprint UUID |
| 狀態 | 英文小寫 | 初始值為 `assigned`（L1 拆解時已知指派對象） |
| 優先級 | `P0` / `P1` / `P2` | — |
| 建立時間 | ISO 8601 | 如 `2026-03-26T12:00:00.000Z` |
| 依賴 | 逗號分隔 ID | 如 `T1,T3`，無則填 `—` |

```markdown
# {任務標題}

| 欄位 | 值 |
|------|-----|
| ID | TN |
| 專案 | {專案名} |
| Sprint | Sprint {N} |
| 指派給 | {agent-id} |
| 優先級 | P0/P1 |
| 狀態 | assigned |
| 依賴 | {依賴任務 ID，無則填 —} |
| 預估 | {預估工時，無則填 —} |
| 建立時間 | $NOW |

---

## 任務描述

{詳細描述}

## 驗收標準

- [ ] ...

---

## 事件紀錄

### $NOW — 建立任務（assigned）
由 L1 透過 /task-delegation 建立
```

6. 畫出依賴圖（ASCII art）
