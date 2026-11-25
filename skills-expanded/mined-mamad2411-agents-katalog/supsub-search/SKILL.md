---
name: supsub-search
version: 0.1.0
description: SupSub 全文搜索 —— 在订阅源（公众号 / 网站）和文章正文里跨源搜索内容。用户说「搜一下 X 相关的内容 / 文章」「在 supsub 里搜 X」「查 X 相关文章」「全文搜索 X」「找 X 的内容」「search articles/content in SupSub」时使用本 skill。注意：本 skill 用于搜「内容 / 文章 / 订阅源标题」；如果用户想发现一个新的微信公众号本身（拿 mpId 准备订阅），改用 supsub-mp。
---

# supsub-search Skill

全量搜索：在订阅源（公众号、网站）和文章正文里同时搜，可按类型缩小范围。

## Prerequisites

- 安装：`pnpm add -g @supsub/cli`（或 `npm i -g @supsub/cli`）
- 已登录：`supsub auth status` 显示 Authenticated（首次使用先 `supsub auth login`）

## Commands

### Search

```
supsub search <keyword> [--type <ALL|MP|WEBSITE|CONTENT>]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--type` | `ALL` | 搜索范围：`ALL`（源 + 文章）/ `MP`（公众号源）/ `WEBSITE`（网站源）/ `CONTENT`（文章正文） |

`<keyword>` 是位置参数，可以是中文或英文，建议用引号包起来避免 shell 拆分。

```bash
# 全量搜索（默认 ALL：同时搜源 + 文章）
supsub search "RAG"

# 只搜公众号
supsub search "阮一峰" --type MP

# 只搜网站
supsub search "hacker news" --type WEBSITE

# 只搜文章正文
supsub search "向量数据库" --type CONTENT

# JSON
supsub search "MCP 协议" -o json
```

JSON shape: `{"success":true,"data":{"results":[...],"recommendations":[...],"prompts":[...]}}`

`results` 是异质数组，每条形如：

```json
// 源结果（type=MP 或 WEBSITE 时）
{ "type": "SOURCE", "data": { "sourceType": "MP", "sourceId": 12345, "isSubscribed": false, "img": "...", "name": "...", "description": "...", "introduction": "...", "url": "..." } }

// 文章结果（type=CONTENT 时）
{ "type": "CONTENT", "data": { "contentId": "...", "title": "...", "summary": "...", "url": "...", "coverImage": "...", "publishedAt": 1700000000, "sourceId": 12345, "sourceName": "...", "sourceType": "MP", "isSubscribed": false, "keywords": [...], "tags": [...] } }
```

`recommendations` 是后端推荐的相关源（`SourceBasic[]`），`prompts` 是后端给的搜索建议词。

---

## Agent Usage Notes

- 解析结构化结果时统一用 `-o json`：`results[]` 是 `{type, data}` 联合类型，先看 `type` 再访问 `data` 字段。
- `--type ALL`（默认）会同时返回源 + 文章混排；想精确控制结果类型时显式指定 `MP` / `WEBSITE` / `CONTENT`。
- 搜索 + 订阅典型链路：`supsub search "<词>" --type MP -o json` → 取 `data.results[].data.sourceId` → `supsub sub add --source-id <id> --type MP`（参考 `supsub-sub` skill）。
- 搜文章拿全文：`supsub search "<词>" --type CONTENT -o json` 拿到 `contentId` 与 `sourceId`，目前 CLI 没有"按 contentId 取文章详情"命令，需要通过 `supsub sub contents --source-id <id> --type <T>` 在该源内浏览。
- `data.results[].data.isSubscribed` 字段可以判断当前结果是否已经订阅，避免重复 `sub add`。
- CLI 一次最多返回 10 条结果（后端默认 `pageSize=10`），不支持翻页；如果想要更多结果，调整关键词缩小或扩大搜索范围。
- Exit codes：`0` OK，`2` UNAUTHORIZED，`64` INVALID_ARGS（`--type` 不在白名单时），`10`/`11` 网络/服务端错误。
