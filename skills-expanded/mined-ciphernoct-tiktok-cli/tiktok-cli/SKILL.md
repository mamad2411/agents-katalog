---
name: tiktok-cli
description: TikTok 评论运营 CLI — 搜索/视频详情/评论(含嵌套回复)/发表评论回复/点赞/删除/视频下载/用户主页/关注请求/通知，含长串关联缓存（按 aweme_id/uid 内联 sec_uid/cover 等长串，避免污染上下文）。Bridge Framework（油猴 + WebSocket）。
---

# TikTok 评论运营 CLI Skill

> 适用版本: v0.3 · 最后更新: 2026-08-19 · 维护者: Yht20927 · 参考实现: douyin-cli

## 项目本质

通过 **Bridge Server + 油猴脚本** 架构，让 CLI 驱动浏览器在 `tiktok.com` 页面上下文发起 API 调用。

```
cli.js ──HTTP──▶ Bridge Server(:19423) ──WS/Poll──▶ 油猴(tiktok.user.js) ──fetch──▶ tiktok.com/api/...
```

所有请求由**用户自己的浏览器**发出（自带 Cookie + 登录态 + 页面 webmssdk 签名），无需管理密码或 Token。

## 前置条件

- Node.js >= 18，首次 `npm install`
- 浏览器 + Tampermonkey，安装 `scripts/tiktok.user.js`
- 打开 `tiktok.com` 任一页面（读接口游客态可用；写接口需登录）
- `cp config.example.json config.json`（首次，`bridge.token` 自动生成）
- 启动 Bridge Server：`node server.js`（默认 `127.0.0.1:19423`）

验证：`node cli.js diag` → 看 `bridge.connected: true` 及 `seeds`（msToken/verifyFp/odinId/login/writesReady）。写操作以 `writesReady: ok` 为准（login/csrf 可能因 HttpOnly 显示 guest/missing 但实际已登录）。

## 命令速查

### 读接口（✅ 实测）

```bash
node cli.js search <keyword> [--offset N] [--count N]   # 搜索视频
node cli.js detail <aweme_id>                            # 视频详情（含 stats/作者）
node cli.js get <aweme_id> [--all --depth N --count N --new --since <ts> --fresh]  # 顶级评论(含嵌套回复)
node cli.js replies <cid> <aweme_id> [--all --fresh]     # 单条评论的回复
# --fresh / --no-cache：绕过页面 _respCache 强制拉取最新（发布评论后验证用）
node cli.js user <uniqueId|userId>                       # 用户主页信息
node cli.js user-posts <secUid|uniqueId|userId> [--count N]  # 用户主页作品
node cli.js following-requests [--count N]               # 关注请求列表（登录态才有数据）
node cli.js notices                                      # 通知列表（登录态才有数据）
```

### 写接口（需登录）

```bash
node cli.js post <aweme_id> "内容" [--reply-to <cid>]    # 发表评论 / 回复
node cli.js like <aweme_id> <cid> [--unlike]             # 点赞/取消点赞评论
node cli.js delete <aweme_id> <cid>                      # 删除评论（本人）
```

### 下载与缓存

```bash
node cli.js download <aweme_id> [--out <dir>] [--cover]  # 下载视频(页面fetch+base64落盘)，--cover 抽帧封面
node cli.js cache <aweme_id|uid>                          # 查回缓存里的完整长串(cover/play_addr/sec_uid)
```

### 诊断

```bash
node cli.js diag   # 连接 + 签名种子 + 登录态 + SecSDK 头状态 + 缓存
```

通用选项：`--raw`（原始输出）`--no-log`（不记录审计）。

## 关键机制（务必理解）

### 1. 签名由页面 webmssdk 自动追加

TikTok 每次 `/api/` 请求末尾会由页面 webmssdk 自动追加 `X-Dynosaur` / `msToken` / `X-Bogus` / `X-Gnarly` 四个签名参数。**自己构造 URL 时绝不能预置**（否则重复签名，`comment/list` 严格校验直接拒收返回空）。`baseQuery` 只发中性参数，签名交给页面。

### 2. 写操作需要 SecSDK 反爬头

评论/点赞/删除（POST）需 `x-secsdk-csrf-token` + 一组 `tt-ticket-guard-*` 头（ECDSA ticket-guard 签名）。油猴脚本已内置采集（fetch init + XHR setRequestHeader 钩子）与回放。缺这些头时 TikTok 会返回假 `cid` 但评论**静默丢弃**（非真成功）。

**写操作真实门槛 = `diag` 中 `writesReady: ok`（secdk + ticketGuard 齐备）**。`secdk: ok` 说明页面已发出带 SecSDK 头的请求、处于有效登录态。`login`/`csrf` 显示 `guest`/`missing` 多为 HttpOnly cookie 读不到造成的**假阴性**，不代表未登录。

### 2.1 评论可见有传播延迟 + 缓存会掩盖新评论

- 评论发布后约 **2-5 分钟**才出现在 `comment/list`，立即 `get` 看不到属正常。
- 页面 `_respCache` 缓存 `comment/list` 响应；写操作成功后会**自动失效**对应缓存，但若仍怀疑被缓存掩盖，用 **`get <aweme_id> --fresh`** 强制绕过。
- 发布后验证建议：`node cli.js get <aweme_id> --fresh`（等 2-5 分钟再验）。

### 3. 视频下载绕浏览器（CDN TLS 拦截）

视频 CDN 对非浏览器客户端无响应（Node 直连超时），`downloadAddr`(SG CDN) 常 403。下载统一走：页面 `fetch` 拿字节 → base64 回传 → Node 落盘（`playAddr`）。桥 `/api/result` body 上限已放宽到 256MB。

### 4. 长串关联缓存（防上下文污染）

`sec_uid`/`cover`/`avatar`/`play_addr` 等无意义长串已从命令输出剥离，按 `aweme_id`（视频级）/`uid`（用户级）关联缓存到 `logs/cache.json`。`node cli.js cache <aweme_id|uid>` 一次回查「视频字段 + 作者字段」。`desc`/`signature`/`nickname` 等有语义字段保留。

### 5. 响应缓存兜底

fetch 钩子缓存页面自己加载的 `comment/list` 响应，`get`/`replies` 优先命中 —— 页面加载成功 = 签名有效，此路径保证出数据。缓存带 **5 分钟 TTL + 100 条 LRU 上限**；写操作（publish/digg/delete）成功后自动失效对应视频/评论的缓存；`--fresh` 可强制绕过。

## 故障排查

| 症状 | 原因 | 解法 |
|------|------|------|
| `Bridge Server 未启动` | server 没跑 | `node server.js` |
| `diag` `bridge.connected: false` | 油猴没装 / 页面没开 | 装脚本 + 打开 tiktok.com |
| `search`/`get` 返回空/HTML | 签名被拦 / 种子过期 | 刷新 tiktok.com 页面重采种子 |
| `post` 返回 `published` 但评论区看不到 | ① `secdk` 头缺失被静默丢弃 ② 传播延迟(2-5min) ③ `_respCache` 旧缓存 | 先 `diag` 看 `writesReady`；若 `ok` 则等 2-5 分钟，用 `get <aweme_id> --fresh` 强制拉最新验证 |
| `like`/`delete` `status_code=5` | 未登录 | 登录后重试 |
| `diag` `login: guest` / `csrf: missing` | HttpOnly cookie 读不到（假阴性），可能实际已登录 | 以 `writesReady: ok` 为准；页面 UI 能看本人主页即已登录 |
| 写操作仍被静默丢弃 | SecSDK 头缺失/过期 | `diag` 看 `writesReady`，`secdk`/`ticketGuard` 非 `ok` 则刷新页面重采 |
| `download` 无地址 / 403 | `downloadAddr` SG CDN 拦截 | 走 `playAddr`（默认已处理） |
| `cache` 未命中 | 还没跑过读命令 | 先 `search`/`detail`/`get` 填充 |

## 文件结构

| 文件 | 作用 |
|------|------|
| `cli.js` | CLI 入口 |
| `server.js` + `lib/server/` | Bridge Server（registry/ws-hub/router） |
| `lib/client/bridge-client.js` | CLI → Server 的 HTTP 客户端 |
| `lib/commands/` | 命令实现（search/get/replies/post/detail/download/user/user-posts/like/delete/cache/...） |
| `lib/cache/store.js` | 长串关联缓存 |
| `lib/audit.js` | JSON 审计日志 |
| `scripts/tiktok.user.js` | 油猴脚本（页面桥 + 种子采集 + SecSDK 头采集） |
| `scripts/mock-bridge.js` | 离线 mock（无浏览器验证 CLI→Bridge 全链路） |
| `docs/API.md` | 完整接口参考（参数/响应/签名/状态） |
| `datas/` | 抓包样本（HAR / 请求响应） |
| `PROGRESS.md` | 进度与测试记录 |

## 审计日志

所有操作记录到 `logs/audit.json`（sessions → operations → apiCalls），大结果（get/search/replies）落地 `logs/results/*.json`，`--no-log` 跳过。
