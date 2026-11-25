---
name: pitfall-record
description: Record a pitfall or lesson learned in the postmortem log
allowed-tools: Read, Edit, Glob
---

# 踩坑紀錄

將踩坑經驗記錄到 postmortem log。

## 使用方式
```
/pitfall-record <category> <title>
```

## 參數
- `$0`: 分類（build / runtime / deploy / test / process）
- `$1`: 標題
- `$ARGUMENTS`: 完整描述

## 執行步驟

1. 讀取現有 postmortem log：
!`cat .knowledge/postmortem-log.md 2>/dev/null | tail -20 || echo "尚無踩坑紀錄"`

2. 計算到期日：紀錄日期 + 14 天，格式為 YYYY-MM-DD。

3. 在 `.knowledge/postmortem-log.md` 末尾 append：

```markdown
### {日期} — $1

| 項目 | 內容 |
|------|------|
| 分類 | $0 |
| 問題 | {問題描述} |
| 原因 | {根本原因} |
| 解法 | {解決方式} |
| 預防 | {未來如何避免} |
| 狀態 | open |
| 到期日 | {日期+14天, YYYY-MM-DD 格式} |
```

4. 如果涉及通用規則，建議是否需更新 CLAUDE.md 或公司規範。
