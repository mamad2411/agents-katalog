---
name: temp-email
description: 當操作或註冊網站需要拋棄式臨時 Email 時使用。自動透過瀏覽器於 Tempail 取得免費臨時信箱、收取驗證信件並自動點擊驗證連結或取得 OTP 驗證碼。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [browser, email, temp-mail, signup, verification, automation]
---

# Temporary Disposable Email Helper

當網頁任務需要 Email 註冊帳號、取得免費額度或收取一次性驗證信件時，使用 `tempail.com` 快速取得 1 小時臨時信箱並完成驗證。

---

## 🛠️ 標準自動化工作流 (Standard Browser Flow)

### 步驟 1：取得臨時信箱地址
```bash
browser open https://tempail.com/en/
browser snapshot -i
```
* 讀取輸入框中的自動生成 Email（例如 `@e31` 顯示 `caspecakke@necub.com`）。
* 同步生成具備特殊字元的隨機密碼（例如 `TempPass892143!`）。

### 步驟 2：前往目標網站填寫註冊表單
```bash
browser open <目標網站註冊網址>
browser snapshot -i
browser fill <email_ref> <temp_email>
browser fill <password_ref> <password>
browser click <submit_ref>
```

### 步驟 3：返回 Tempail 收取驗證信 / 驗證碼
```bash
browser open https://tempail.com/en/
browser snapshot -i
```
1. 檢查收件匣列表（若未出現，點擊 Refresh 或等待 5~10 秒）。
2. 點擊進入新收到的驗證信：
   * **若為驗證連結**：讀取 Email 內文中的驗證 URL（如 `https://.../verify?token=...`），直接調用 `browser open <verification_url>`。
   * **若為 OTP 數字驗證碼**：讀取 4~6 位數驗證碼，返回目標網站填寫送出。
