---
name: mp2rss-x
version: 0.1.0
description: X（Twitter）账号订阅查看与内容拉取（基于把 X 账号转成 RSS 的 Mp2rss 服务）—— 列出已订阅 X 账号、按 xUserId 分页拉推文流（posts）与长文流（articles）。匹配「我订阅了哪些 X 账号」「列一下我的 X 订阅」「这个 X 账号最近发了什么」「拉一下 <xUserId> 的推文」「<xUserId> 的长文」「X 账号 <id> 的 articles」「mp2rss x list / posts / articles」。⚠️ CLI 只暴露读类 3 件套；X 账号的「搜索 / 订阅 / 取消订阅」仅在 Web 控制台（<https://mp2rss.bugcode.dev>）操作，CLI 与 Open API 都没有这些写类端点 —— 用户提这类需求时应引导到 Web 控制台，而不是去找 `x subscribe / x remove / x search`（不存在）。
---

# mp2rss-x Skill

通过 Mp2rss CLI 管理 X（Twitter）信息源的只读访问 —— 列出已订阅 X 账号、按 xUserId 拉推文与长文。

## Prerequisites

- `mp2rss` 二进制已安装（参考 `mp2rss-auth` 的 Prerequisites）
- 已登录：`mp2rss auth status` 显示 `loggedIn: true`（首次使用先跑 `mp2rss auth login`）
- 要操作的 X 账号已在 Web 控制台订阅（CLI 不支持 `subscribe`）

## 范围边界（重要）

| 操作 | CLI 是否支持 | 去哪里做 |
|------|--------------|----------|
| `x list` —— 列已订阅 X 账号 | ✅ | 本 skill |
| `x posts` —— 拉推文流 | ✅ | 本 skill |
| `x articles` —— 拉长文流 | ✅ | 本 skill |
| `x subscribe` —— 订阅新 X 账号 | ❌ | <https://mp2rss.bugcode.dev> Web 控制台 |
| `x remove` —— 取消订阅 X 账号 | ❌ | <https://mp2rss.bugcode.dev> Web 控制台 |
| `x search` —— 搜索 X 账号 | ❌ | <https://mp2rss.bugcode.dev> Web 控制台 |

> 用户说「订阅这个 X 账号」/「把 X 上的 xxx 加进来」/「搜一下 X 上的 xxx」时，**不要尝试构造 `mp2rss x subscribe` 之类的命令**（不存在），直接告诉用户去 Web 控制台操作。

## Commands

### List subscribed X accounts

```
mp2rss x list [-q <keyword>] [-p <page>] [--page-size <n>] [-o json]
```

| Flag | Default | Description |
|------|---------|-------------|
| `-q, --query` | — | 按 displayName / username 模糊搜索（仅 server 支持时生效；不支持时退化为客户端筛 X 项） |
| `-p, --page` | 1 | 页码 |
| `--page-size` | 20 | 每页条数（最大 50） |
| `-o, --output` | table | `table` / `json` |

```bash
mp2rss x list
mp2rss x list -q claude
mp2rss x list -p 2 --page-size 50
mp2rss x list -o json | jq '.items[].xDisplayName'
```

底层调 `GET /open-api/subscriptions?sourceType=x`；若 server 不识别 `sourceType`，CLI 客户端会兜底剔除 mp 项。

JSON shape:
```json
{
  "items": [
    {
      "sourceType": "x",
      "xUserId": "44196397",
      "xUsername": "elonmusk",
      "xDisplayName": "Elon Musk",
      "xAvatarUrl": "https://...",
      "xVerified": true,
      "xLastItemAt": 1705000050000,
      "createdAt": 1705000000000
    }
  ],
  "total": 12,
  "page": 1,
  "pageSize": 20
}
```

---

### List posts (推文流)

```
mp2rss x posts <xUserId> [-p <page>] [--page-size <n>] [-o json]
```

按 `postedAt DESC` 分页拉某个已订阅 X 账号的推文。

| Flag | Default | Description |
|------|---------|-------------|
| `-p, --page` | 1 | 页码 |
| `--page-size` | 20 | 每页条数（最大 50） |
| `-o, --output` | table | `table` / `json` |

```bash
mp2rss x posts 44196397
mp2rss x posts 44196397 -p 2 --page-size 50
mp2rss x posts 44196397 -o json | jq '.items[].content'
```

JSON shape:
```json
{
  "items": [
    {
      "postId": "1234567890",
      "content": "推文正文",
      "media": [{"url": "https://...", "type": "image"}],
      "retweetedPost": null,
      "quotedPost": null,
      "threadPosts": [],
      "postedAt": 1705000000000
    }
  ],
  "total": 87,
  "page": 1,
  "pageSize": 20
}
```

字段说明：
- `media` —— 推文附带的图片 / 视频，`type` 取值如 `image` / `video`
- `retweetedPost` / `quotedPost` —— 原始推文的嵌套对象（可能为 `null`）
- `threadPosts` —— 同一作者的线程后续推文（可能为空数组）
- 未订阅的 `xUserId` 返回 404 `X account is not subscribed`（exit code `4`）

---

### List articles (长文流)

```
mp2rss x articles <xUserId> [-p <page>] [--page-size <n>] [-o json]
```

按 `publishedAt DESC` 分页拉某个已订阅 X 账号的长文（X Articles）。

| Flag | Default | Description |
|------|---------|-------------|
| `-p, --page` | 1 | 页码 |
| `--page-size` | 20 | 每页条数（最大 50） |
| `-o, --output` | table | `table` / `json` |

```bash
mp2rss x articles 44196397
mp2rss x articles 44196397 -p 2 --page-size 50
mp2rss x articles 44196397 -o json | jq '.items[].title'
```

JSON shape:
```json
{
  "items": [
    {
      "url": "https://x.com/.../article/...",
      "title": "长文标题",
      "description": "长文摘要",
      "contentMarkdown": "# Markdown 正文（可能为 null）",
      "coverUrl": "https://...",
      "publishedAt": 1705000000000
    }
  ],
  "total": 3,
  "page": 1,
  "pageSize": 20
}
```

- 未订阅的 `xUserId` 返回 404 `X account is not subscribed`（exit code `4`）
- `contentMarkdown` 是上游推送的 markdown 原文，可能为 `null`

---

## Agent Usage Notes

- **`xUserId` 是字符串**（X 平台原生数字 ID，序列化为 string），不要按 number 解析；`mp2rss mp` 那边的 `mpId` 才是 int64
- 解析批量输出统一加 `-o json`
- 时间字段均为 unix 毫秒数（number）：`createdAt` / `xLastItemAt` / `postedAt` / `publishedAt`
- 字段命名统一 camelCase：`xUserId` / `xUsername` / `xDisplayName` / `xAvatarUrl` / `xVerified` / `xLastItemAt` / `sourceType` / `postId` / `coverUrl` / `contentMarkdown`
- **不存在的子命令**：`x subscribe` / `x remove` / `x search` —— 用户提相关需求时直接引导去 Web 控制台 <https://mp2rss.bugcode.dev>，不要去 CLI 里找替代命令
- `x posts` / `x articles` **都带分页元数据**（`total` / `page` / `pageSize`）—— 这一点与 `mp articles`（无分页字段）不同，按 `total` 判断是否还有下一页即可
- `--page-size` 三个命令一致上限 50；超过会返回 `参数错误`（exit code `2`）
- `x list -q <kw>` 的 `-q` 走服务端模糊搜索 displayName / username；若服务端不识别，CLI 会退化为按 `sourceType=x` 客户端过滤（即 `-q` 失效，但不会报错）
- 拿到 `xUserId` 的常规链路：先跑 `mp2rss x list -o json` 从 `items[].xUserId` 取，再喂给 `x posts` / `x articles`
- 错误 JSON 形态：`{"error":{"message":"...","code":<int>}}`；`code` 优先用 HTTP 状态码（来自上游），否则回退到 CLI exit code（参数 / 鉴权类错误）
- Exit codes：`0` 成功；`1` 通用错误（网络）；`2` 参数错误（含 `--page-size` 越界）；`3` 鉴权失败 → 引导用户跑 `mp2rss auth login`（参考 `mp2rss-auth` skill）；`4` 资源不存在（`xUserId` 未订阅或不存在）；`5` 上游不可用
