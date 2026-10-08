---
name: pre-deploy
description: Pre-deployment checklist for G5 submission
allowed-tools: Read, Bash, Glob, Grep
---

# 預部署檢查

L1 提交 G5（部署就緒）前執行，產生預部署檢查報告。

## 使用方式
```
/pre-deploy [environment]
```

## 參數
- `$0`: 目標環境（staging / production，預設 staging）
- `$ARGUMENTS`: 完整參數

## 自動檢查項

### 1. CI 狀態
- [ ] lint 通過（執行 `npm run lint` 或等效指令）
- [ ] type-check 通過（執行 `npm run typecheck` 或等效指令）
- [ ] 單元測試通過（執行 `npm run test` 或等效指令）
- [ ] build 成功（執行 `npm run build` 或等效指令）

### 2. 環境變數
- [ ] `.env.example` 存在且有內容
- [ ] 所有程式碼中引用的環境變數都在 `.env.example` 中列出
- [ ] production 環境設定已準備（CI workflow / docker-compose）

### 3. 資料庫
- [ ] 所有 migration 已生成（無 pending changes）
- [ ] seed 腳本可執行（如有）

### 4. Docker（如適用）
- [ ] Dockerfile 存在且語法正確
- [ ] docker-compose config 無語法錯誤
- [ ] .dockerignore 排除測試檔案

### 5. 安全
- [ ] 無硬編碼密碼或 API Key（grep 檢查）
- [ ] .env 不在 git 追蹤中

## 手動確認項（列出供 L1 確認）

- [ ] 回滾計畫已準備
- [ ] 監控/告警已設定
- [ ] 相關方已通知上線時間

## 輸出格式

```
# 預部署檢查報告

**環境**: {environment}
**日期**: {today}
**結果**: PASS / FAIL

## 自動檢查
| # | 項目 | 結果 | 備註 |
|---|------|------|------|
| 1 | lint | ✅/❌ | {detail} |
...

## 手動確認（待 L1 勾選）
- [ ] 回滾計畫
- [ ] 監控告警
- [ ] 通知相關方

## 結論
{PASS: 可提交 G5 / FAIL: 需修正以上 ❌ 項目}
```
