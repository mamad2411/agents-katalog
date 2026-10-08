---
name: frontend-spec-report
description: "規格開發完成報告技能：當完成表單驗證、狀態管理、資料流等規格實作後，產生標準化報告時使用。回報前檢查：PM 規格驗證規則實作、同步/非同步/跨欄位驗證器、錯誤訊息語系檔、Signal 狀態管理、TypeScript 編譯。報告包含：檔案清單、表單欄位清單（型別/必填/驗證）、驗證器清單、語系檔更新、PM 規格對照。適用於規格實作結束、交付文件、PM 驗收準備。"
---

# 前端規格實作回報

表單驗證與業務邏輯實作完成後的標準化回報格式。

## 回報前檢查

- [ ] 所有 PM 規格中的驗證規則已實作
- [ ] 同步/非同步/跨欄位驗證器正確實作
- [ ] 錯誤訊息已加入語系檔
- [ ] 表單狀態使用 Signal 管理
- [ ] 無 TypeScript 編譯錯誤

## 輸出模板

````markdown
## 規格實作完成報告

### 📁 檔案清單

- {component-name}.component.ts
- {component-name}.component.html
- shared/validators/{validator-name}.validators.ts (if applicable)
- i18n/zh-TW.json

### 📋 表單欄位清單

| 欄位名稱 | 型別   | 必填  | 驗證規則     |
| -------- | ------ | ----- | ------------ |
| {field}  | {type} | ✅/❌ | {validators} |

### ✅ 驗證器清單

| 驗證器名稱 | 類型             | 適用欄位 | 錯誤訊息 Key |
| ---------- | ---------------- | -------- | ------------ |
| {name}     | sync/async/cross | {fields} | {i18nKey}    |

### 🌐 語系檔更新

```json
{ "validation": { "{key}": "{message}" } }
```
````

### 🔍 PM 規格對照

| 規格項目 | 實作狀態 | 備註   |
| -------- | -------- | ------ |
| {item}   | ✅/⚠️/❌ | {note} |

### ⚠️ 問題回報

{issues or "無問題"}

```

## 狀態說明

- ✅ 已完成：完全符合規格
- ⚠️ 部分完成：有調整或需確認
- ❌ 未完成：需進一步處理
```
