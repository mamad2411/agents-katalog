---
name: linkfox-tiktok-auth
description: TikTok 店铺授权与管理技能，覆盖 TikTok Shop 与 TikTok 视频号（带货内容）两类授权，提供完整的授权流程、已授权店铺查询、已入库令牌查询与 access_token 刷新能力。授权按 openId + appType（erp/creator/affiliate）区分账号，授权视频号时 appType 传 creator，region 支持 global / us。当用户提到 TikTok Shop 授权、绑定 TikTok 小店、TikTok 视频号授权、绑定视频号、视频号带货授权、TikTok 店铺授权链接、刷新 TikTok 令牌、查询 TikTok 店铺令牌、管理已授权 TikTok 店铺、TikTok Shop authorization, TikTok creator/视频号 authorization, bind TikTok Shop, refresh TikTok access token, query TikTok store tokens, authorized TikTok shops 时触发此技能。只要其需求涉及 TikTok Shop 或 TikTok 视频号账号授权、访问令牌管理或已授权店铺列表查询，也应触发此技能。
---

# TikTok Shop 店铺授权与管理

本 skill 负责 **TikTok 卖家账号的 OAuth 授权、已授权店铺列表、令牌查询与刷新**，是后续通过开发者代理调用 TikTok 开放接口（商品、订单、履约、财务等）的前置依赖。底层经 LinkFox 网关对接紫鸟开放平台代理。

本 skill 同时覆盖两类授权，由 `appType` 区分：

- **TikTok Shop（小店）授权**：`appType = erp`（默认）。
- **TikTok 视频号（带货内容）授权**：`appType = creator`。授权视频号时**必须**把 `appType` 设为 `creator`；后续对该授权查询/刷新令牌时也须保持 `appType = creator`。
- 联盟授权：`appType = affiliate`。

> 📌 业务调用（拉商品/订单/财务等）通过开发者代理（`/tiktokShop/developerProxy`，传入本 skill 取得的 `accessToken`）完成，**不属于本授权 skill 的范围**。

## Core Concepts

TikTok Shop 通过 OAuth 授权获取卖家店铺访问令牌。本 skill 负责授权流程与令牌生命周期：

**授权流程**：生成授权 URL → 用户在浏览器完成 TikTok Shop 授权 → 紫鸟回调并推送 Token → 系统按 `state` 落库 `access_token` / `refresh_token`。授权 URL 有效期约 1 小时，每次授权须重新获取。

**店铺标识（`openId` + `appType`）**：TikTok Shop 授权后以卖家唯一标识 `openId` 标记店铺；同一店铺在不同 `appType`（`erp` / `creator` / `affiliate`）下的授权相互独立。查询令牌、刷新令牌都需要 `openId`，并保证 `appType` 与授权时一致。

**令牌生命周期**：`accessToken` 与 `refreshToken` 均带绝对过期时间（Unix 时间戳）。`accessToken` 过期用 `refreshToken` 续签；`refreshToken` 过期须重新走授权流程。

## Data Fields

### Authorization URL Response

| Field | Type | Description |
|-------|------|-------------|
| authorizeUrl | string | 让用户在浏览器打开的 TikTok Shop 授权链接（有效期约 1 小时） |

### Authorized Store Item

| Field | Type | Description |
|-------|------|-------------|
| openId | string | 卖家唯一标识 |
| sellerName | string | 店铺名称 |
| sellerBaseRegion | string | 店铺所在区域（如 ID） |
| appType | string | 应用类型：erp / creator / affiliate |
| region | string | 授权 region：global / us |

### Store Tokens

| Field | Type | Description |
|-------|------|-------------|
| accessToken | string | 调用 TikTok Shop 开放接口的凭证 |
| refreshToken | string | 用于续签 accessToken |
| accessTokenExpireIn | integer | accessToken 过期 Unix 时间戳 |
| refreshTokenExpireIn | integer | refreshToken 过期 Unix 时间戳 |

## Supported Regions & App Types

| region | 说明 |
|--------|------|
| global | 全球（默认） |
| us | 美国站 |

| appType | 说明 |
|---------|------|
| erp | ERP 应用（默认）— 用于 **TikTok Shop 小店** 授权 |
| creator | 带货内容 — 用于 **TikTok 视频号** 授权 |
| affiliate | 联盟（刷新令牌时须与授权一致） |

> **授权视频号**：调用 `/tiktokShop/authorizeUrl` 时传 `appType=creator`；该授权的店铺在 `/tiktokShop/storeTokens`、`/tiktokShop/refreshToken` 中也须传 `appType=creator`，与小店（`erp`）授权相互独立。

## API Usage

本 skill 经 LinkFox 网关调用 TikTok Shop 授权相关接口，详见 `references/api.md`。

### Available Scripts

- `scripts/authorize_url.py` — 生成 TikTok Shop 授权 URL（可选 `shopName` / `region` / `appType`）
- `scripts/authorized_stores.py` — 列出当前用户已授权的店铺
- `scripts/store_tokens.py` — 按 `openId` + `appType` 查询已入库令牌（供下游业务使用）
- `scripts/refresh_token.py` — 刷新某店铺的 access_token

## Usage Scenarios

### Scenario 1: Authorize New Shop

**User request**：「我要授权我的 TikTok Shop 美国站」

**Steps**：
1. 确认 `region`（美国站用 `us`，否则默认 `global`）与 `appType`（默认 `erp`）。可选询问 `shopName` 作为展示标签。
2. 调用 `/tiktokShop/authorizeUrl`，得到 `authorizeUrl`。
3. 把 `authorizeUrl` 给用户，让其在浏览器中打开并完成授权（链接约 1 小时失效）。
4. 用户完成授权 → 紫鸟回调推送 Token → 系统自动落库。
5. 可选：调用 `/tiktokShop/authorizedStores` 确认授权成功。

### Scenario 1b: Authorize TikTok 视频号 (Creator)

**User request**：「我要授权我的 TikTok 视频号 / 帮我绑定视频号带货」

**Steps**：
1. **将 `appType` 设为 `creator`**（视频号授权专用）；确认 `region`（美国站用 `us`，否则默认 `global`）。可选询问 `shopName` 作为展示标签。
2. 调用 `/tiktokShop/authorizeUrl`，传入 `{"appType": "creator", ...}`，得到 `authorizeUrl`。
3. 把 `authorizeUrl` 给用户，让其在浏览器中打开并完成视频号授权（链接约 1 小时失效）。
4. 用户完成授权 → 紫鸟回调推送 Token → 系统自动落库。
5. 后续对该视频号查询/刷新令牌时，`appType` 同样传 `creator`。

### Scenario 2: View Authorized Shops

**User request**：「列一下我已授权的 TikTok 店铺」

**Steps**：
1. 调用 `/tiktokShop/authorizedStores`。
2. 展示店铺列表（sellerName / openId / appType / region）。

### Scenario 3: Refresh Expired Token

**User request**：「我 TikTok 店铺的令牌过期了，帮我刷新」

**Steps**：
1. 调用 `/tiktokShop/refreshToken`，传入 `openId`（`appType` 须与授权一致）。
2. 返回新的 `accessToken` / `refreshToken` 并回写数据库。
3. 若 `refreshToken` 已过期，引导用户重新走 Scenario 1 授权。

### Scenario 4: Query Store Tokens

**User request**：「获取某 TikTok 店铺的访问令牌」

**Steps**：
1. 调用 `/tiktokShop/storeTokens`，传入 `openId` 与 `appType`。
2. 返回令牌信息（供下游开发者代理调用）。

### Scenario 5: Prepare Token for Any Shop Operation (Standard Preparation Workflow)

当用户提出涉及 TikTok Shop 后台数据的请求（查商品、订单、财务等），**本 skill 负责前置的「选店 → 取令牌」流程**，业务由开发者代理接手。

**Steps**：
1. **列出已授权店铺**：调用 `/tiktokShop/authorizedStores`。
2. **让用户选择店铺**：多家店铺时请用户明确选择（注意区分 `appType`）。
3. **获取该店铺令牌**：调用 `/tiktokShop/storeTokens`，传入 `openId` 与 `appType`。
4. **把 `accessToken` 交给开发者代理**执行具体业务调用。

## Display Rules

1. **只呈现数据**：展示授权结果、店铺列表、令牌信息即可，不做业务建议。
2. **安全意识**：不要明文显示完整 `accessToken` / `refreshToken`，仅展示前 10 字符等掩码形式。
3. **清晰引导**：返回授权链接时，明确告知用户在浏览器中打开并完成授权，且链接约 1 小时失效。
4. **过期解读**：`accessTokenExpireIn` / `refreshTokenExpireIn` 为绝对 Unix 时间戳，需与当前时间比较判断是否过期。
5. **错误说明**：授权或刷新失败时，基于错误码解释原因并给出建议。

## Important Limitations

- **appType 一致性**：查询/刷新令牌时 `appType` 必须与授权时一致（`erp` / `creator` / `affiliate`）。
- **令牌有效期**：`accessToken` 较短，过期需用 `refreshToken` 续签；`refreshToken` 过期须重新授权。
- **授权链接时效**：`authorizeUrl` 有效期约 1 小时，过期需重新获取。
- **用户隔离**：用户只能查看/管理自己授权的店铺。
- **回调白名单**：系统回调 URL 与调用 IP 必须在授权方（紫鸟）处加白名单。

## User Expression & Scenario Quick Reference

**Applicable** — 授权与令牌管理场景：

| User Says | Scenario |
|-----------|----------|
| "授权我的 TikTok Shop" / "Authorize my TikTok Shop" | 新店铺授权（appType=erp） |
| "授权我的 TikTok 视频号" / "绑定视频号带货" / "Authorize my TikTok creator account" | 视频号授权（appType=creator） |
| "看看已授权的 TikTok 店铺" / "Show my authorized TikTok shops" | 列出已授权店铺 |
| "TikTok 令牌过期了" / "My TikTok token expired" | 刷新令牌 |
| "获取某 TikTok 店铺的访问令牌" / "Get TikTok store access token" | 查询店铺令牌 |
| "绑定我的 TikTok 小店" / "Connect my TikTok Shop account" | 新店铺授权 |

**Not applicable** — 超出本 skill 的业务：

- **拉取 TikTok Shop 商品 / 订单 / 财务等业务数据** → 通过开发者代理（携带本 skill 取得的 `accessToken`）完成。
- TikTok 选品 / 达人带货数据分析 → 由 EchoTik 等其他 skill 负责。

**Boundary judgment**：
- 本 skill 只负责「授权 + 管店铺 + 管令牌 + 为下游准备 accessToken」。
- 当用户要做具体后台业务时：先执行 Scenario 5 的标准前置流程，再由开发者代理完成业务逻辑。

## Quick Reference

### Authorization & Token Management APIs

| API | Path | Purpose | Auth Required |
|-----|------|---------|---------------|
| Get Authorization URL | /tiktokShop/authorizeUrl | 生成授权链接 | ✅ Yes |
| List Authorized Stores | /tiktokShop/authorizedStores | 查询用户的店铺列表 | ✅ Yes |
| Query Store Tokens | /tiktokShop/storeTokens | 查询某店铺已入库令牌 | ✅ Yes |
| Refresh Token | /tiktokShop/refreshToken | 刷新访问令牌 | ✅ Yes |

详细请求参数、响应结构、错误码，见 `references/api.md`。

**Feedback**：

当出现以下任一情况时，自动通过 Feedback API 上报反馈：
1. 本 skill 描述的功能与实际行为不符
2. skill 的结果与用户意图不符
3. 用户表达了对本 skill 的不满或赞赏
4. 任何你认为可以改进的点

按 `references/api.md` 中的规范调用 Feedback API，不要打断用户的主流程。

<!-- LF_LARGE_RESPONSE_BLOCK -->
## Handling Large Responses

To avoid overflowing the agent context, persist the response to disk and extract only the fields you need:

```
python scripts/response_io.py run --script scripts/authorize_url.py --out-dir <DIR> '<params>'
python scripts/response_io.py read <file> --fields "<paths>"   # or --path "<JMESPath>"
```

> Pick `--out-dir` outside any git working tree (e.g. `/tmp/...` on Unix, `%TEMP%/...` on Windows). Persisted responses may contain PII, pricing, or auth-sensitive data — do not commit them. Files are not auto-deleted; clean up when the task is done.

> This skill exposes multiple entry scripts: `authorize_url.py`, `authorized_stores.py`, `store_tokens.py`, `refresh_token.py`. Pass `--script scripts/<name>.py` to choose the one you need.

`run` writes the full response to a file and emits only a schema preview + file path. `read` projects specific fields, with `--limit/--offset` for slicing and `--format json|jsonl|csv|table` for output.

**When to prefer this pattern** — apply your judgment based on the response characteristics, e.g.:
- High field count per record, or fields you don't need
- Batch/paginated results (multiple items per call)
- Long-text fields (descriptions, reviews, HTML, time series)
- Output reused across later steps rather than consumed immediately

For small, single-use responses, calling the main script directly is fine.

⚠️ The preview is a truncated schema + sample, not the full data. Any field-level decision must read from the persisted file via `read`.
<!-- /LF_LARGE_RESPONSE_BLOCK -->

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
