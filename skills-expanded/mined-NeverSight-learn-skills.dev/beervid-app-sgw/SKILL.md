---
name: beervid-app-sgw
description: >
  TikTok/TikTok Shop 应用服务集成指南。涵盖 OAuth 授权（TT + TTS 双平台）、Token 生命周期管理、
  视频上传与发布、发布成功后的视频数据查询（TT 视频信息、TTS 带货表现）、队列定时刷新策略、
  商品查询、Webhook 回调的完整流程与最佳实践。
  当用户需要：集成 TT/TTS OAuth 授权、处理账号绑定与 token 刷新、上传视频到 TT/TTS、创建发布任务、
  发布后查询视频数据或带货表现、设计队列定时刷新机制、接收 webhook 事件、设计相关数据库表结构、处理接口错误时，使用此 skill。
  即使用户只提到 TikTok 授权、视频发布、账号管理、OSS 上传、webhook 投递、视频数据查询中的任何一个环节，也应触发。
---

# TTS App Manager 集成 Skill

面向第三方客户端集成 tt-manager 服务的完整指南。

## 平台约束速查

两条核心规则决定了整个系统的接口选择和账号使用：

| 规则 | 说明 |
|------|------|
| **TT 账号 → TT 功能** | 视频上传（OSS 中转）、视频发布（`tt_direct`）、视频数据查询（insight）必须使用 `platform: 'tt'` 的授权账号 |
| **TTS 账号 → TTS 功能** | 视频上传（TTS API 中转）、挂车视频发布（`tts_direct`）、商品查询、带货表现查询必须使用 `platform: 'tts'` 的授权账号 |

**不要混用**——所有需要 `authorizedAccountId` 的接口都会校验账号平台归属，`PLATFORM_MISMATCH` 或 `INVALID_ACCOUNT` 是最常见的集成错误。

## 核心流程总览

### 1. OAuth 授权 → 获取授权账号 ID

```
POST /open-api/v1/{tt|tts}/auth/link  →  获得 authorizeUrl
 ↓ 用户浏览器跳转授权
GET /callbacks/{tt|tts}/oauth         →  302 回调客户端，state 含账号信息
```

- TT 授权返回：`{ id, openId, username, platform: 'tt' }`
- TTS 授权返回：`{ id, openId, username, platform: 'tts' }`
- `id` 即后续接口中的 `authorizedAccountId`

> 详细流程、state 双层含义、正确/错误示例见 → [OAuth 授权流程](references/oauth-authorization.md)

### 2. 视频上传

| 平台 | 上传路径 | 返回值 |
|------|---------|--------|
| TT | 生成 uploadToken → `POST /open-api/v1/upload/tt-video` | `ossUrl` |
| TTS | 生成 uploadToken → `POST /open-api/v1/upload/tts-video` | `videoFileId` |

### 3. 视频发布

| 平台 | 接口 | 关键参数 |
|------|------|---------|
| TT | `POST /open-api/v1/tt/videos/publish` | `authorizedAccountId` + `ossUrl` + `caption` |
| TTS | `POST /open-api/v1/tts/videos/publish` | `authorizedAccountId` + `videoFileId` + `productId` + `productTitle` |

两者都需要 `Idempotency-Key` header，异步执行。

### 4. 状态查询

```
GET /open-api/v1/publish-tasks/:publishTaskId
```

状态流转：`created → submitted → published / failed`

### 5. 视频数据查询（发布成功后）

发布成功后 `upstreamVideoId` 有值，可查询视频详情与数据表现：

| 平台 | 接口 | 数据内容 |
|------|------|---------|
| TT | `GET /open-api/v1/tt/videos?authorizedAccountId=&videoIds=` | 视频基本信息（缩略图、分享链接等） |
| TTS | `GET /open-api/v1/tts/videos/performances?authorizedAccountId=&videoIds=&startTimeGe=&endTimeLe=` | 带货表现（GMV、订单数、CTR 等，T-1 延迟） |

**推荐使用队列定时刷新**数据，而非一次性查询。发布状态 30s 起步指数退避，TT 视频数据每 4-6 小时，TTS 表现数据每天 1 次。

> 完整端到端流程、代码示例与队列刷新策略见 → [发布工作流](references/publish-workflow.md)

## 鉴权速查

| 路径 | 鉴权方式 |
|------|---------|
| `/admin-api/*` | `Authorization: Bearer <ADMIN_API_TOKEN>` |
| `/open-api/*`（除 upload） | `X-Api-Key: <apiKey>` |
| `/open-api/v1/upload/*` | `X-Upload-Token: <uploadToken>`（10 分钟有效） |
| `/callbacks/*` | 无（按模块策略处理） |

## 错误处理速查

| 场景 | 错误码 | HTTP | 处理建议 |
|------|--------|------|---------|
| 账号平台不匹配 | `PLATFORM_MISMATCH` / `INVALID_ACCOUNT` | 400 | 检查 authorizedAccountId 对应的平台 |
| Token 过期需重新授权 | `TT_REAUTH_REQUIRED` | 401 | 引导用户重新走 OAuth 流程 |
| Token 正在刷新 | `TOKEN_REFRESH_IN_PROGRESS` | 503 | 等待后重试（指数退避） |
| 发布幂等命中 | 无错误，返回 202 | 202 | 检查返回的已有任务状态 |
| Upload Token 过期 | `UPLOAD_TOKEN_EXPIRED` | 401 | 重新生成 uploadToken |

> 完整错误码与处理策略见 → [错误处理](references/error-handling.md)

## 数据模型速查

核心表关系：

```
apps 1---* app_account_bindings *---1 authorized_accounts
                                      1---1 account_tokens
                                      *---1 publish_tasks
apps 1---* app_webhooks
publish_tasks 1---* publish_status_events
publish_tasks 1---* webhook_deliveries
```

> 完整设计理念与扩展建议见 → [数据库设计](references/database-design.md)

## 参考文档索引

| 文件 | 内容 |
|------|------|
| [API 接口文档](references/api-reference.md) | 全部接口的请求/响应格式、参数说明、错误码 |
| [OAuth 授权](references/oauth-authorization.md) | 授权链接调用、回调接收、业务 state 透传、正确/错误示例 |
| [发布工作流](references/publish-workflow.md) | 授权→上传→发布→查询的端到端流程、幂等策略、轮询/Webhook |
| [错误处理](references/error-handling.md) | 完整错误码表、重试策略、常见错误排查 |
| [数据库设计](references/database-design.md) | 表结构说明、设计原则、索引策略、扩展建议 |
