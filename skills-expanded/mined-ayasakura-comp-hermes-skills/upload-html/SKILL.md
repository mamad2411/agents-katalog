---
name: upload-html
description: 將 HTML 檔案（或整個靜態網站目錄）發布到 GitHub；最終回傳 raw.githack.com 可存取的公開網址。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [github, html, upload, static-site]
---

# Upload HTML — GitHub-backed 靜態網頁發布

將 HTML 檔案（或整個靜態網站目錄）發布到 GitHub；預設直接推到 `git@github.com:AyaSakura-comp/TempHtml.git`，如果使用者已經有其他 repo 權限，也可以指定那個 repo。最終回傳 `raw.githack.com` 可存取的公開網址。

---

## 核心原則

- **不使用 Netlify**。
- 預設使用 `git@github.com:AyaSakura-comp/TempHtml.git`。
- 優先使用使用者已擁有權限的 GitHub repo。
- 以 GitHub repo 作為 source of truth。
- 用 `raw.githack.com` 當最終分享網址。

---

## 1. 前置檢查

```bash
# 確認檔案或資料夾存在
ls /path/to/site
```

- 單一 HTML 檔：保留原檔名，不重新命名成 `index.html`。
- 資料夾：原樣同步到 staging 目錄；若 site 本身需要首頁 entrypoint，則維持原本的 `index.html`。

---

## 2. 發布流程

1. 驗證輸入路徑。
2. 建立暫存 staging 目錄。
3. 把檔案複製進去，保留原檔名。
4. 若使用者提供 repo（`owner/repo`、GitHub URL、或 `git@github.com:owner/repo.git`），就 clone 該 repo 並把 staging 內容同步進去。
5. 否則直接使用預設 repo：`git@github.com:AyaSakura-comp/TempHtml.git`。
6. push 後回傳三個網址：
   - `Repo URL`
   - `Raw URL`（`raw.githubusercontent.com`）
   - `Site URL`（`raw.githack.com`）

---

## 3. 使用方式

```bash
./scripts/upload-html.sh /path/to/index.html
./scripts/upload-html.sh /path/to/site-folder owner/repo
./scripts/upload-html.sh /path/to/site-folder git@github.com:owner/repo.git
```

---

## 4. 常見問題

- repo 已存在但你沒有權限：停下來，先確認 repo 權限。
- 相對路徑資源：請把圖片/CSS/JS 一起放進上傳目錄。
- raw.githack 可能有短暫快取延遲，第一次開啟若 404，等一下再試。
