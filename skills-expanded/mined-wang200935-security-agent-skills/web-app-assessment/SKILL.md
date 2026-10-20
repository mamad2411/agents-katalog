---
name: web-app-assessment
description: Web应用渗透测试 — 针对Web应用的完整渗透流程，含技术栈识别、目录枚举、认证测试、输入验证、逻辑漏洞。Use when performing
  authorized penetration testing, CTF, or security assessment tasks related to web-pentest.
version: 1.0.0
license: MIT
platforms:
- linux
- macos
- windows
metadata:
  hermes_origin: import
  upstream_source_path: /skills/specialized/web-pentest/SKILL.md
  upstream_original_name: web-pentest
tags:
- red-teaming
- penetration-testing
- security
- imported
related_skills:
- pentest-workflow
- pentest-quick-checklist
- pentest-tool-setup
- ctf-web-attacks
---

# Web 应用渗透测试 Skill

针对 Web 应用的专项渗透测试流程，覆盖从信息收集到漏洞验证的完整链路。

**需要更深入的 Web 安全知识？** 使用 `-web-security-advanced` Skill，包含完整的注入攻击族、协议安全、Playbook 等。

## 1. 技术栈识别
- 使用 fetch 工具获取 HTTP 响应头
- 使用 chrome-devtools 工具分析前端技术
- 识别后端框架和 CMS

## 2. 目录枚举
- 常见目录：/admin, /api, /upload, /config, /backup
- 敏感文件：robots.txt, sitemap.xml, .env, .git/HEAD
- API 文档：/swagger, /docs, /api-docs
- **🛑 Vue.js/React SPA catch-all 陷阱**：SPA 對所有不存在的路徑返回 HTTP 200 + 相同的 SPA shell（Content-Length 一致，如 1075 bytes）。不可僅依賴 status code 判斷端點存在！判別方法：對多個路徑同時記錄 Content-Length，若 `/admin`, `/admin/login`, `/admin/pages`, `/admin/whatever`, `/.env` 全部返回相同大小 → 全是 SPA catch-all。真實 API 端點（如 `/api/index_data.php`）會返回不同的 Content-Length 和 JSON body。Python 框架（Flask/Django）也有類似行為：所有不存在路徑返回相同大小 (~2800-3000 bytes) 的自訂 404 頁面。

## 3. 认证测试
- 默认凭据测试
- 暴力破解检测
- 会话管理缺陷
- JWT 安全测试

## 4. 输入验证测试
- SQL 注入
- XSS（反射/存储/DOM）
- SSRF
- LFI/RFI
- 命令注入
- 文件上传

## 5. 逻辑漏洞测试
- 越权访问（水平/垂直）
- 业务逻辑绕过
- 竞态条件
- 支付逻辑漏洞

## 6. 客户端存取控制测试（JS 逆向）

**重点：客户端 JS 验证不等於安全防護。** 許多應用使用 JavaScript 做密碼驗證或 URL 編碼，但伺服器端未實作對應的存取控制。

### 6.1 識別客戶端驗證模式
- 檢查 HTML 中 onclick/oncontextmenu 屬性是否包含 `checkPermit`、`checkAuth` 等自訂函數
- 擷取 `<script src>` 引用的 JS 檔案（`curl http://target/index.js`）
- 分析 JS 中的編碼/解碼邏輯（搜尋 `charCodeAt`、`fromCharCode`、`eval(function(p,a,c,k...`）

### 6.2 逆向自訂編碼演算法
- 將 JS 編碼邏輯逐行翻譯為 Python
- 特別注意 regex 中 `.` vs `\d` 的捕獲群組差異（常見陷阱：`(\d+)\.\d(\d+)` 中間的 `\d` 不捕獲）
- 先用一個已知樣本驗證解碼結果（確認輸出像合法 URL）
- 批次解碼所有發現的編碼值

### 6.3 繞過客戶端驗證
- 解碼後直接 curl/wget 目標 URL — 測試伺服器端是否有對應保護
- 若 200 回應：確認存取控制僅存在於客戶端 = Critical 漏洞
- 若 302/403：伺服器端有部分保護，進一步測試 session 驗證

### 6.4 HTML 註解資訊洩漏
- 始終檢查 `<!-- ... -->` 中的內容
- 常見洩漏：伺服器內部路徑（`D:\video\`）、IP、設定值、除錯資訊
- 將所有註解內容記錄到目標畫像中

## 7. 输出
- Web 渗透报告
- PoC 脚本

## 参考文档

- `references/js-reverse-engineering.md` — JS 編碼逆向工程技術（分段數字、線性密鑰、Packer 混淆）
- `references/03-web-security-integrated.md` — Web 安全整合参考
- `references/web-injection.md` — 注入攻击详细参考
- `references/web-logic-auth.md` — 认证与逻辑漏洞
- `references/web-modern-protocols.md` — 现代协议安全

## Hermes 使用適配

- 來源為  專案技能，已匯入 Hermes 本地 skill。僅在**已授權**滲透測試、CTF、內部安全評估或防禦驗證範圍內使用。
- 原文若提到 `fetch`，在 Hermes 中優先使用 `web_extract`、`browser` 或 `terminal(curl/HTTPie)` 取得真實回應。
- 原文若提到 `python_execute`，在 Hermes 中使用 `execute_code` 或 `terminal(python3 ...)`；計算、編碼、hash、PoC 驗證必須用工具實測，不靠猜。
- 原文若提到 MCP/Burp/adb/frida/jadx/chrome_devtools 等外部工具：先確認本機是否安裝或可用；不可用時以 Hermes 現有 `web`、`browser`、`terminal`、`file`、`vision` 工具替代，並明確標註限制。
- 下一次滲透任務中，先載入 `-pentest-flow` 做總路由，再依場景載入本系列專項 skill（例如 `-web-security-advanced`、`-osint-recon`、`-rapid-checklist`）。

## 來源與維護

- 原始 skill 已保存於 `references/upstream-skill.md`；README/LICENSE 已保存於 `references/`。
