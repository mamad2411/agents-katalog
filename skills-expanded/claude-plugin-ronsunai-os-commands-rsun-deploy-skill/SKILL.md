---
name: rsun-deploy
description: 部署容晟科技專案。當用戶說「deploy」「部署」「wrangler deploy」「push 到 Vercel」時使用。自動判斷當前專案類型，選擇正確的部署方式。
user-invocable: true
allowed-tools: "Bash(git *) Bash(npm *) Bash(npx wrangler *) Bash(vercel *) Read"
---

# 容晟科技部署流程

## 參數

`$ARGUMENTS` — 選填。指定要部署的專案或目標（如「worker」「dashboard」「all」）。若未提供，從當前目錄推導。

## 部署對照表

| 專案 | 類型 | 指令 | 注意事項 |
|------|------|------|---------|
| rsun-worker | Cloudflare Workers | `cd ~/Projects/rsun-worker && npx wrangler deploy` | 不走 Vercel，直接部署 CF |
| rsun-dashboard | Vercel | `git push origin main` | push 後 Vercel 自動觸發 |
| ceyan-web | Vercel | `git push origin main` | push 前確認 npm run build |
| askai | Vercel | `git push origin main` | push 前確認 npm run build |
| aiclass | Vercel | `git push origin main` | push 前確認 npm run build |
| ronsunai-web | Vercel | `git push origin main` | push 前確認 npm run build |
| TRACKER | CF Pages | `cd ~/Projects/TRACKER && npx wrangler pages deploy . --project-name rsun-tracker` | **不走 Vercel**，wrangler pages（≠ wrangler deploy）|

## 執行流程

### Step 1：確認部署目標

根據 `$ARGUMENTS` 或當前 `pwd` 判斷目標專案。

### Step 2：Pre-flight 檢查

對 Next.js 專案（非 rsun-worker）執行：
```bash
git status --short        # 確認沒有意外的未 commit 檔案
git log --oneline -3      # 確認最新 commit 正確
npm run build 2>&1 | tail -20   # Build 必須通過
```

對 rsun-worker 執行：
```bash
grep 'function parsePrefix' src/index.js   # 確認 parsePrefix 存在（關鍵安全檢查）
```

### Step 3：執行部署

- **rsun-worker**：`npx wrangler deploy`，輸出部署 URL 確認
- **Vercel 專案**：`git push origin main`，說明 Vercel 會自動部署
- **TRACKER**：`cd ~/Projects/TRACKER && npx wrangler pages deploy . --project-name rsun-tracker`（CF Pages，非 Vercel）

### Step 4：確認

部署後輸出：
```
✅ 部署完成
- 指令：<執行的指令>
- Production URL：<URL>
- 部署時間：<timestamp>
```

## ⚠️ 禁止事項

- 不可用 `git push --force`
- 不可跳過 build check（除非用戶明確說「跳過 build」）
- rsun-worker 部署前必須確認 `parsePrefix` 函式存在
- 不確定時先問用戶，不要猜測部署目標
