---
name: oauth-flow-test
description: OAuth 2.0 / OIDC / SSO 登入流程測試專屬流程。覆蓋 authorization code + PKCE、token 刷新、access/refresh token 過期、refresh token 輪替、登出/撤銷、多 IdP（Google / Apple / Facebook / 企業 SSO）、deep link 重導、state/nonce CSRF 防護、scope/consent、silent renew、錯誤路徑（拒絕授權 / code 過期）。整合 iOS（ASWebAuthenticationSession）/ Android（Custom Tabs + AppAuth）/ Web（redirect + PKCE）/ BE（token 驗簽）。當使用者提到「OAuth / OIDC / SSO / 登入流程測試 / token 刷新 / refresh token / PKCE / 授權碼 / 第三方登入 / Google 登入 / Apple 登入 / single sign-on / token 過期 / 授權測試」時觸發。配套：security-scan（token 漏洞）、compliance-test（同意/個資）、test-automation（登入 UI test）、offline-mode-test（token 刷新斷線）、bug-report。
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
argument-hint: "[--provider=google|apple|azure-ad] [--flow=auth-code-pkce|refresh|logout] [--platform=ios|android|web]"
---

# oauth-flow-test

> ⚙️ **執行前先讀 [`modules/config-loader.md`](./modules/config-loader.md)**。

## 為什麼需要這個 skill

登入是每個 app 的入口，也是最容易出**安全 + 體驗雙重災難**的地方：token 沒刷新被登出、refresh token 沒輪替被重放、PKCE 沒做被攔截、深連結重導被劫持。`test-master` 規劃功能 TC 時很難涵蓋 OAuth 的狀態機與安全細節。

> 登入流程是高風險域，但 29 個 skill 沒有專門處理 OAuth/OIDC 狀態機與安全驗證的——本 skill 補這個缺口。

→ 本 skill 系統性產出 **OAuth 流程 + 安全 + 邊界** 測試。

## 適用場景

- ✅ 有第三方登入 / 企業 SSO / 自建 OAuth server
- ✅ token 刷新 / session 管理出過包
- ✅ 安全稽核要求驗證 OAuth 實作（PKCE / state / 撤銷）
- ✅ 多 IdP 並存要驗一致行為

## 不適用場景

- ❌ token 本身的程式漏洞掃描 — 用 `security-scan`
- ❌ 同意/個資合規 — 用 `compliance-test`
- ❌ 純功能登入（不碰 OAuth 狀態機）— 用 `test-master`

## 核心測試場景

| # | 場景 | 驗什麼 | 常見 bug |
|---|------|--------|---------|
| 1 | **Auth code + PKCE** | code_verifier/challenge 正確、code 一次性 | 公開 client 沒 PKCE → code 被攔可換 token |
| 2 | **Token 刷新** | access 過期用 refresh 換新、無感續期 | 過期直接登出、refresh 沒用上 |
| 3 | **Refresh token 輪替** | 用過的 refresh 立即失效（防重放） | 舊 refresh 還能用 → 重放風險 |
| 4 | **登出 / 撤銷** | 本地清 token + server 撤銷 + IdP session | 只清本地，server token 仍有效 |
| 5 | **state / nonce** | 防 CSRF / 重放，回呼比對 | 不驗 state → 授權碼注入 |
| 6 | **deep link 重導** | 回呼 URL 只被本 app 接、不被劫持 | 其他 app 攔截 redirect |
| 7 | **scope / consent** | 只取必要 scope、同意可撤回 | over-scope、無撤回 |
| 8 | **錯誤路徑** | 拒絕授權 / code 過期 / 網路中斷的優雅處理 | crash / 卡在白畫面 |
| 9 | **多 IdP 一致** | Google / Apple / SSO 行為一致 | 某 provider 漏處理 |

## 工具對應

| 平台 | 推薦做法 |
|------|---------|
| **iOS** | `ASWebAuthenticationSession`（不要用 WKWebView 收 token）+ Keychain 存 token |
| **Android** | Custom Tabs + AppAuth-Android + EncryptedSharedPreferences / Keystore |
| **Web** | Authorization Code + PKCE（不要 implicit）、token 存記憶體 / httpOnly cookie |
| **BE** | 驗 JWT 簽章 / exp / aud / iss、introspection endpoint |

## 執行流程

### Phase 1: 盤點 IdP + flow
```bash
grep -rniE "oauth|oidc|authoriz|code_verifier|pkce|refresh_token|ASWebAuthentication|AppAuth" . 2>/dev/null | head
# 找 redirect scheme / callback
grep -rniE "redirect_uri|callback|CFBundleURLSchemes|appAuthRedirectScheme" . 2>/dev/null | head
```

### Phase 2: 產流程測試（對 staging IdP，不打 production）

iOS（XCUITest + mock IdP）:
```swift
func testAuthCodePKCEFlow() throws {
    // 1. 觸發登入 → ASWebAuthenticationSession 開
    // 2. mock IdP 回 code（驗 code_challenge 有帶）
    // 3. 換 token（驗帶 code_verifier）
    // 4. 驗 token 存進 Keychain 而非 UserDefaults
}
```

BE（驗 token + 輪替）:
```python
def test_refresh_token_rotation(auth_client):
    r1 = auth_client.refresh(old_refresh)
    assert r1.status == 200
    # 同一個 refresh 再用一次 → 必須失效
    r2 = auth_client.refresh(old_refresh)
    assert r2.status == 401   # 防重放
```

### Phase 3: 安全斷言（每個 flow 必驗）
- PKCE：公開 client **強制** code_challenge（S256，不接受 plain）
- state/nonce：回呼**比對**，不符即拒
- token 儲存：iOS Keychain / Android Keystore，**絕不明文**
- 撤銷：登出後舊 token 打 API → 401
- redirect_uri：**精確比對**（不接受 prefix/wildcard）

### Phase 4: 報告
`oauth-flow-report.md`：9 場景 × 平台 matrix + 安全斷言結果 + 必修（含修法）。

### Phase 5: CI
登入 happy path + token 刷新進 smoke；完整 9 場景 + 安全斷言進 release（接 `smoke-test-analyzer` 分層）。

## ⚠️ 安全護欄

- ❌ **絕不對 production IdP 跑測試**（用 staging / mock IdP）
- ❌ **絕不 log token / code / client_secret**（報告也只存遮蔽值）
- ✅ 公開 client（mobile/SPA）**強制 PKCE**，不接受無 PKCE 或 plain
- ✅ state / nonce 一律驗，redirect_uri 精確比對
- ✅ token 存 Keychain/Keystore，測試驗證不落 UserDefaults/明文
- ✅ refresh token 輪替 + 撤銷後失效，皆有斷言

## ♿ a11y 必檢（本 skill 專屬）

- [ ] 登入 / 同意畫面的按鈕、欄位有 label，VoiceOver / TalkBack 可操作
- [ ] 「用 Apple/Google 登入」按鈕符合各家 a11y 規範（不只圖示）
- [ ] 登入錯誤訊息非僅紅色、附文字，字級放大不破版
- [ ] 第三方授權頁（IdP 託管）至少驗證可鍵盤/讀屏完成

## 設定依賴

| 設定 Key | 用途 | 預設 |
|---------|------|------|
| `oauth_test.providers` | 啟用的 IdP | [] |
| `oauth_test.flows` | 測試的 flow | auth-code-pkce / refresh / logout |
| `oauth_test.idp_base_url` | staging IdP（**禁 production**） | "" |
| `oauth_test.scopes` | 預期 scope | [] |
| `oauth_test.require_pkce` | 公開 client 強制 PKCE | true |

## 範例

詳見 [`examples.md`](./examples.md)
