---
name: pitfall-resolve
description: Mark a pitfall record as resolved in the postmortem log
allowed-tools: Read, Edit, Grep
---

# 踩坑解決

將踩坑紀錄標記為已解決。

## 使用方式
/pitfall-resolve <title-keyword>

## 參數
- `$ARGUMENTS`: 踩坑標題關鍵字（用來搜尋對應紀錄）

## 執行步驟

1. 讀取 `.knowledge/postmortem-log.md`
2. 搜尋包含 `$ARGUMENTS` 的踩坑紀錄
3. 將該紀錄的「狀態」從 `open` 改為 `resolved`
4. 確認修改完成
