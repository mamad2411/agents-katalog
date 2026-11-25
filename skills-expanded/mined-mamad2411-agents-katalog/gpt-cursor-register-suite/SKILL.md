---
name: gpt-cursor-register-suite
description: "GPT/Cursor 账号注册机套件（协议注册 + 接码 OTP + Turnstile 打码 + OpenAI sentinel PoW + TLS 指纹 + Cursor 授权注入与机器ID复位）。触发词：注册机、批量注册、接码、OTP 自动填充、sentinel、tls 指纹、cursor 授权。"
x-alice-class: crack
---

# GPT / Cursor 账号注册机套件

四个上游开源实现的技术合流，抽成可复用的注册机工程骨架。

## 上游来源（均为公开仓库，已实测拉取源码）

| 仓库 | 星 | 语言 | 值得抄的部分 |
|:--|--:|:--|:--|
| `lxf746/any-auto-register` | 3309 | Python | 插件化平台/邮箱/打码/代理五层抽象；11+ 平台注册器；协议+浏览器双执行器；账号池与 Token 续期 |
| `ddCat-main/cursor-auto-register` | 892 | Python | Cursor 专用：SQLite 授权注入、shadow patch 机器指纹、tempmail.plus 接码 |
| `verssache/chatgpt-creator` | 328 | Go | 纯协议 OpenAI 注册全链路（Go）：sentinel PoW、TLS 指纹轮换、并发 worker + 失败重试 |
| `AuuCoder/gptGrok2api` | 262 | Python | OAuth 账号 → OpenAI 兼容 API 网关、账号状态机与调度 |

## 一、OpenAI 纯协议注册链（来自 chatgpt-creator + any-auto-register）

固定端点：

```
baseURL = https://chatgpt.com
authURL = https://auth.openai.com
sentinel = https://sentinel.openai.com/backend-api/sentinel/req
```

注册流（顺序不可换）：

1. `GET https://chatgpt.com/` — 建会话，带 cookie `oai-did=<uuid4>`
2. `GET /api/auth/csrf` → `csrfToken`
3. `POST /api/auth/signin/openai?prompt=login&ext-oai-did=<deviceID>&auth_session_logging_id=<uuid>&screen_hint=login_or_signup&login_hint=<email>`
   body: `callbackUrl=https://chatgpt.com/&csrfToken=<csrf>&json=true` → 返回 `{"url": authorizeURL}`
4. `GET authorizeURL` → 看最终落地路径分流：
   - `create-account/password` → 走注册
   - `email-verification` / `email-otp` → 直接进 OTP 阶段
   - `about-you` → 直接进建档阶段
   - `callback` → 已完
5. `POST auth.openai.com/api/accounts/user/register` body `{"username":email,"password":pwd}`
6. `POST .../api/accounts/email-otp/send` → 轮询邮箱拿 6 位码
7. `POST .../api/accounts/email-otp/validate` body `{"code":otp}`
8. `POST .../api/accounts/create_account` body `{"name":..., "birthdate":"YYYY-MM-DD"}`，头必须带 `openai-sentinel-token: <token>`
9. `GET <continue_url|url|redirect_url>` 收尾回调

每一步之间插 0.2–1.5s 随机延时（`randomDelay`），是过风控的必要动作，不要省。

### sentinel token（关键反爬点）

`sentinel.openai.com/backend-api/sentinel/req` 用 `Content-Type: text/plain;charset=UTF-8`，body `{"p":<requirementsToken>,"id":<deviceID>,"flow":<flow>}`，Referer 必须是 `https://sentinel.openai.com/sentinel/<ver>/frame.html`。

返回 `proofofwork.{required,seed,difficulty}`，若 `required` 则本地算 PoW：

- 配置数组 20 项（screenRes / 时间串 / 4294705152 / nonce / UA / sdk.js / null / null / en-US / en-US,en / 随机 / 导航探针 / 打乱项 / 打乱项 / perfNow / SID / "" / 4|8|12|16 / timeOrigin）
- 循环 `nonce = 0..500000`，`data = base64(json(config))`，`h = FNV1a32(seed + data)`，命中 `h[:len(difficulty)] <= difficulty` 即成功
- 返回 `"gAAAAAB" + data + "~S"`

requirements token 则是 `"gAAAAAC" + base64(json(config))`。

FNV-1a32 带 avalanche 收尾（murmur3 风格），实现见 `scripts/openai_sentinel_pow.py`。

## 二、TLS 指纹与身份轮换

- `bogdanfinn/tls-client`（Go）/ `curl_cffi`（Python `impersonate="safari17_0"` 或 `chrome131`）伪装 ClientHello
- 每个 worker 独立：随机 `deviceID(uuid4)`、随机 Chrome 版本 UA、`sec-ch-ua`/`sec-ch-ua-mobile`/`sec-ch-ua-platform` 三件套必须与 UA 版本自洽
- 显式给 fhttp 客户端塞 cookie，不要依赖自动 jar；`oai-did` 必须等于 deviceID
- 代理：每请求换出口更稳；账号成功率按 `success/(success+fail)` 排序取次，连续 5 次全失败自动禁用

## 三、邮箱接码层

上游用过 9 种通道，按可靠性排序：

1. **Cloudflare 自建 catch-all + tempmail.plus**：自有域名 DNS 指 CF，catch-all 转发到 tempmail.plus 前缀邮箱，再读 `https://tempmail.plus/api/mails?email=<u>@<d>&limit=20&epin=<pin>` 解析 6 位码。可控性最高、无黑名单风险，是 `ddCat-main` 路线。
2. **generator.email 直读**：`GET https://generator.email/<domain>/<user>` 必须显式带 `Cookie: surl=<domain>/<user>`，从 `#email-table div.subj_div_45g45gg` 正则抓 `\d{6}`。域会被 OpenAI 拉黑（`unsupported_email`），实现要带域黑名单自动落盘。
3. **API 类**：MoeMail / TempMail / DDG Email / DuckMail / FreeMail / tempmail.lol / testmail / aitre / cfworker。
4. **本地 MS 池**：`local_ms_pool` / `local_ms_mailbox`。
5. **兜底**：自动拿不到就转人工/前端输入（`pending_verification_codes` 挂起队列 + 180s 超时）。

## 四、Turnstile / 验证码

- **本地 solver**：Camoufox 起本地 Turnstile Solver（默认 8889 端口），health check 30s 超时；首次要 `python3 -m camoufox fetch`
- **云打码**：YesCaptcha / 2Captcha / CapSolver，标准三连：`createTask(TurnstileTaskProxyless, websiteURL, websiteKey)` → `getTaskResult` 轮询 60 次 × 3s → `solution.token`
- Cursor 的 sitekey 是 `0x4AAAAAAAMNIvC45A4Wjjln`
- 提交时 `captchaToken` 与 form 字段一起进 multipart，不要单独放 header

## 五、Cursor 注册链（来自 any-auto-register + ddCat-main）

端点与 Server Action ID（Next.js server action，会随版本变，需从页面 bundle 重新提取）：

```
AUTH   = https://authenticator.cursor.sh
CURSOR = https://cursor.com
ACTION_SUBMIT_EMAIL    = d0b05a2a36fbe69091c2f49016138171d5c1e4cd
ACTION_SUBMIT_PASSWORD = fef846a39073c935bea71b63308b177b113269b7
ACTION_MAGIC_CODE      = f9e8ae3d58a7cd11cccbcdbf210e6f2a6a2550dd
```

请求头固定：`accept: text/x-component`、`next-action: <ACTION_*>`、`origin: AUTH`、`referer: AUTH/sign-up?state=<state>`、`next-router-state-tree: ["",{"children":["(main)",{"children":["(root)",{"children":["(sign-in)",{"children":["__PAGE__",{}]}]}]}]}]`（URL 编码后）。

五步：

1. `GET AUTH/?state=<双层 urlencode 的 {"returnTo":"https://cursor.com/dashboard","nonce":uuid4}>`，从 cookies 取 `state-*` cookie 名
2. `POST AUTH/sign-up` multipart `1_state`, `email`（ACTION_SUBMIT_EMAIL）
3. `POST AUTH/sign-up` multipart `1_state`, `email`, `password`, `captchaToken`（ACTION_SUBMIT_PASSWORD）
4. `POST AUTH/sign-up` multipart `1_state`, `email`, `otp`（ACTION_MAGIC_CODE）→ 从 `location` 头正则 `code=([\w-]+)` 取授权码
5. `GET CURSOR/api/auth/callback?code=<code>&state=<state>` → 从 cookie 取 `WorkosCursorSessionToken`（url 解码后即 access token）

注册完落地：

- **授权注入**：写 `%APPDATA%\Cursor\User\globalStorage\state.vscdb` 的 `itemTable`：`cursorAuth/cachedSignUpType=Auth_0`、`cursorAuth/cachedEmail`、`cursorAuth/accessToken`、`cursorAuth/refreshToken`（key 不存在则 INSERT）。见 `scripts/cursor_auth_inject.py`
- **机器指纹复位**：写 `storage.json` 的 `telemetry.devDeviceId`(uuid4) / `telemetry.machineId`(sha256 32B) / `telemetry.macMachineId`(sha512 64B) / `telemetry.sqmId`(`{UUID大写}`)
- **机器码补丁**：shadow patch 改文件内机器码字段（备份→字节替换→回写），配合随机 MAC
- **本地应用切换**：写 token → 重启 Cursor IDE → 复查 billing/usage

## 六、工程骨架（插件化，抄 any-auto-register）

```
platforms/<name>/{core.py, plugin.py, protocol_mailbox.py, browser_register.py, browser_oauth.py, switch.py}
providers/{mailbox,captcha,sms,proxy}/*.py     # 每类都注册到 registry，可热插拔
core/{base_platform,base_mailbox,base_captcha,base_sms,base_identity,proxy_pool,tls,registry}.py
```

平台声明式能力：`supported_executors=["protocol","headless","headed"]`、`protocol_captcha_order`、`capabilities=["switch_desktop","query_state","generate_link"]`。新平台只要实现 `build_protocol_mailbox_adapter` / `build_browser_registration_adapter`。

并发与重试（chatgpt-creator 的 batch 语义）：worker 池抢 `atomic` 名额，**失败要把名额还回去重试**，直到成功数达标；`unsupported_email` 错误自动把域名写进黑名单。

## 七、脚本清单

| 脚本 | 作用 |
|:--|:--|
| `scripts/openai_sentinel_pow.py` | OpenAI sentinel requirements + PoW token 生成（Go 版移植） |
| `scripts/cursor_protocol_register.py` | Cursor 五步协议注册，返回 access/refresh token |
| `scripts/cursor_auth_inject.py` | Cursor 授权注入 + 机器 ID 复位（跨 Win/mac/Linux） |
| `scripts/mailbox_otp.py` | tempmail.plus + generator.email 双通道取 6 位 OTP |
| `scripts/proxy_pool.py` | 成功率加权轮询代理池，自动禁用连败节点 |

## 八、落地注意

- 上游两个 README 都写了「仅供学习研究」，落库时保留署名，商用需遵守 AGPL-3.0 / 原仓库 LICENSE。
- Server Action ID、sentinel sdk 版本号、Turnstile sitekey 都是会变的硬编码，跑挂先怀疑这三个。
- 不要用同一出口 IP 连续注册；注册失败的域名要落黑名单，否则会一直撞 `unsupported_email`。
- 账号建好后务必走一次 `token_refresh` / 状态机，把失效账号踢出池子，避免网关 401。