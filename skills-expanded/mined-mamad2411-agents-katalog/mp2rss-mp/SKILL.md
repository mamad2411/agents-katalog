---
name: mp2rss-mp
version: 0.1.0
description: 微信公众号订阅与文章管理（基于把公众号转成 RSS 的 Mp2rss 服务）—— 订阅 / 列出 / 取消订阅微信公众号，查询某个公众号的历史文章，按关键词模糊搜索已订阅源。匹配「订阅这个公众号 <文章 URL>」「把这个公众号转成 RSS」「订阅 <mp.weixin.qq.com/s/...>」「我订阅了哪些公众号」「列一下我的公众号 RSS」「这个公众号最近发了什么」「<某公众号> 的历史文章」「拉一下 <某公众号> 这个号的文章」「取消订阅 <某公众号>」「把 <某公众号> 从订阅里删了」「搜一下我订阅的公众号 <某关键词>」「mp2rss mp list / search / subscribe / remove / articles」。订阅时传入的是公众号「任意一篇文章的 URL」（mp.weixin.qq.com/s/...），不是公众号名字本身。⚠️ 只处理「微信公众号」语义；用户说「X 账号 / 推特 / xUserId / 长文 articles / 推文 posts」之类应当路由到 mp2rss-x，不要进来。
---

# mp2rss-mp Skill

通过 Mp2rss CLI 管理微信公众号订阅与文章 —— 订阅 / 列出 / 取消订阅微信公众号，按 mpId 查询单个公众号的历史文章。

## Prerequisites

- `mp2rss` 二进制已安装（参考 `mp2rss-auth` 的 Prerequisites）
- 已登录：`mp2rss auth status` 显示 `loggedIn: true`（首次使用先跑 `mp2rss auth login`）

## Commands

### List subscriptions

```
mp2rss mp list [-q <keyword>] [-p <page>] [--page-size <n>] [-o json]
```

| Flag | Default | Description |
|------|---------|-------------|
| `-q, --query` | — | 按公众号名模糊搜索 |
| `-p, --page` | 1 | 页码 |
| `--page-size` | 20 | 每页条数（最大 50） |
| `-o, --output` | table | `table` / `json` |

```bash
mp2rss mp list
mp2rss mp list -q 财经
mp2rss mp list -p 2 --page-size 50
mp2rss mp list -o json | jq '.items[].mpName'
```

JSON shape:
```json
{
  "items": [
    {
      "sourceType": "mp",
      "mpId": 123456,
      "mpName": "某公众号",
      "mpAvatarUrl": "https://...",
      "createdAt": 1705000000000,
      "mpLastArticleAt": 1705000050000
    }
  ],
  "total": 42,
  "page": 1,
  "pageSize": 20
}
```

---

### Search subscriptions

```
mp2rss mp search <keyword> [-p <page>] [--page-size <n>] [-o json]
```

`mp2rss mp list -q <keyword>` 的语法糖，flag 集与输出与 `list` 一致。

```bash
mp2rss mp search 财经
mp2rss mp search 财经 -o json
```

---

### Subscribe a WeChat MP

```
mp2rss mp subscribe <article-url> [-o json]
```

⚠️ **传入的是文章 URL**（`https://mp.weixin.qq.com/s/...`），不是公众号名、不是二维码、也不是公众号主页链接。从公众号任意一篇文章里复制链接即可，Mp2rss 会从该文章解析出所属公众号并把整个公众号订阅到你的 Feed。

```bash
mp2rss mp subscribe https://mp.weixin.qq.com/s/abcDEFghIJKlmnop
mp2rss mp subscribe https://mp.weixin.qq.com/s/abc -o json
```

JSON shape:
```json
{
  "ok": true,
  "articleUrl": "https://mp.weixin.qq.com/s/..."
}
```

---

### Unsubscribe

```
mp2rss mp remove <mpId> [-y] [-o json]
```

按 mpId 取消订阅。`-y` 跳过交互式确认（适合脚本调用）。

```bash
mp2rss mp remove 123456
mp2rss mp remove 123456 -y
mp2rss mp remove 123456 -y -o json
```

JSON shape:
```json
{
  "ok": true,
  "mpId": 123456
}
```

mpId 从 `mp2rss mp list -o json` 的 `items[].mpId` 获取。

---

### List articles of a MP

```
mp2rss mp articles <mpId> [-p <page>] [--page-size <n>] [-o json]
```

按公众号 mpId 查历史文章。

| Flag | Default | Description |
|------|---------|-------------|
| `-p, --page` | 1 | 页码 |
| `--page-size` | 100 | 每页条数（最大 100） |
| `-o, --output` | table | `table` / `json` |

```bash
mp2rss mp articles 123456
mp2rss mp articles 123456 -p 2 --page-size 100
mp2rss mp articles 123456 -o json | jq '.items[].title'
```

JSON shape:
```json
{
  "items": [
    {
      "mpId": 123456,
      "articleId": "article-id",
      "title": "文章标题",
      "summary": "文章摘要",
      "coverImageUrl": "https://...",
      "originalUrl": "https://mp.weixin.qq.com/s/...",
      "contentMarkdown": "# Markdown 正文",
      "publishedAt": 1705000000000,
      "updatedAt": 1705000010000
    }
  ]
}
```

⚠️ 文章列表**没有分页字段**（无 `total` / `page` / `pageSize`）；`items` 为空即视为本页结束。

---

## Agent Usage Notes

- 解析批量输出统一加 `-o json`
- **`mpId` 是数字（int64）**：JavaScript / jq 解析时注意精度，必要时用字符串模式读取
- 时间字段均为 unix 毫秒数（number）
- 字段命名统一 camelCase：`mpId` / `mpName` / `mpAvatarUrl` / `mpLastArticleAt` / `articleId` / `originalUrl` / `contentMarkdown` / `publishedAt`
- **订阅参数最常犯的错**：用户说「订阅这个公众号 <X>」时，`<X>` 必须是 `mp.weixin.qq.com/s/...` 文章链接。识别不到合法文章 URL 时应**先反问用户索要任意一篇文章链接**，而不是直接尝试
- 取消订阅前应先 `mp2rss mp list -q <name>` 确认 mpId，避免误删
- 文章列表无分页字段，依赖 `--page-size` 控制单次返回上限（最大 100）；分页继续查下一页用 `-p`
- 错误 JSON 形态：`{"error":{"message":"...","code":<int>}}`；`code` 优先用 HTTP 状态码（来自上游），否则回退到 CLI exit code（参数 / 鉴权类错误）
- Exit codes：`0` 成功；`1` 通用错误（网络）；`2` 参数错误；`3` 鉴权失败 → 引导用户跑 `mp2rss auth login`（参考 `mp2rss-auth` skill）；`4` 资源不存在（mpId 错或文章 URL 已失效）；`5` 上游不可用
