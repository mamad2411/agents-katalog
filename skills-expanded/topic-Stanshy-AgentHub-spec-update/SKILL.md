---
name: spec-update
description: 規範文件更新 SOP — 版本號遞增 + 變更記錄 + 影響範圍通知
allowed-tools: Read, Edit, Glob, Grep, Bash
---

# 規範文件更新

修改任何 `.knowledge/specs/` 下的規範文件時，**必須透過此 skill 執行**，確保版本號遞增、變更有記錄、相關任務被通知。

## 使用方式
```
/spec-update <spec-file> <變更摘要>
```

## 參數
- `$0`: 規範文件路徑（如 `.knowledge/specs/api-design.md`）
- `$ARGUMENTS`: 完整參數（含變更摘要）

## 執行步驟

### STEP 1 — 讀取目標規範文件
讀取 `$0`，確認：
- 當前版本號（文件標題或頂部 metadata 中的 `vX.Y`）
- 文件結構與現有內容

---

### ⛔ STEP 2 — 確認變更範圍
說明本次變更：
- **變更內容**：新增 / 修改 / 刪除了什麼
- **影響範圍**：哪些模組、API、功能受影響
- **向後相容性**：是否有 breaking change

輸出：
```
📋 變更摘要
規範文件：$0
當前版本：vX.Y
變更類型：[新增欄位 / 修改行為 / 刪除功能 / 其他]
影響範圍：[描述]
Breaking change：[是 / 否]
```

> ✋ 確認變更範圍正確後再繼續。

---

### STEP 3 — 執行變更
對 `$0` 進行實際修改。

---

### ⛔ STEP 4 — 遞增版本號
在規範文件頂部更新版本號：
- Minor change（新增、修改）：`vX.Y` → `vX.Y+1`
- Breaking change：`vX.Y` → `vX+1.0`

在文件頂部加入變更記錄（若無 Changelog 區塊則新增）：
```markdown
## Changelog

### vX.Y+1 — {YYYY-MM-DD}
{變更摘要}
```

> ✋ 確認版本號已遞增、變更記錄已寫入後再繼續。

---

### STEP 5 — 更新 file-index.md
找到 `.knowledge/file-index.md`，更新對應規範文件的版本標註：
```markdown
| `.knowledge/specs/api-design.md` | API 設計規格 vX.Y+1（🔴 規範） |
```

---

### STEP 6 — 掃描受影響任務
!`find .tasks -name "*.md" 2>/dev/null | xargs grep -l "api-design\|data-model\|feature-spec" 2>/dev/null | head -10`

列出目前 `in_progress` 或 `assigned` 狀態、且與本規範相關的任務。

---

### STEP 7 — 輸出通知

```
✅ 規範更新完成

規範文件：$0
版本：vX.Y → vX.Y+1
file-index 已更新：✅

受影響的進行中任務：
- T3: {名稱} (in_progress → 需確認是否受影響)
- T5: {名稱} (assigned → 執行前請重新閱讀規範)

建議動作：
1. 通知相關 L2 Agent 重新讀取規範後繼續執行
2. 若有 breaking change，請 L1 確認已完成任務是否需要返工
```
