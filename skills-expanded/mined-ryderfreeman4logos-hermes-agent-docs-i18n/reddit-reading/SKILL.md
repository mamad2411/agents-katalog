---
name: reddit-reading
description: "Read Reddit: subreddits, search, threads, users. No browser."
version: 1.0.0
author: Teknium (teknium1), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Reddit, Social Media, Research, Discussions, Community]
    related_skills: [rss-feeds, grounded-citations, blocked-page-recovery, xurl]
---

# Reddit 阅读技能

该技能可从常规访问途径失效的服务器或无头机器上读取 Reddit 内容——包括子版块列表、站点或子版块搜索结果、包含评论的完整帖子以及用户活动记录。但它不会发布内容、投票，也不会以用户身份登录。此功能的设计灵感来源于 [Agent Reach](https://github.com/Panniantong/Agent-Reach) 中针对不同平台的后端路由机制。

## 适用场景

- “r/LocalLLaMA 对 X 有什么看法？”、“查找关于 Y 的 Reddit 帖子”、“总结这个 Reddit 帖子”的内容，以及“用户 u/someone 最近发布了什么”。
- 用户分享的任何 `reddit.com` 地址。由于服务器 IP 会遇到 403 错误或“证明你是人类”的限制，`web_extract`、`browser_navigate` 以及 `.json` 接口均无法使用；而该技能则是可行的解决方案。
- 不适用于发布内容、投票、发送消息或任何需要用户登录的操作。

## 先决条件

**无需任何前提条件。** 不需要 Reddit 账户、登录信息、Cookie 或 API 密钥。默认的后端为 Reddit 的公共 Atom 订阅源（`.rss` 接口），这是 Reddit 仍会向非居民 IP 提供的唯一无需认证的访问途径。不过该接口的访问频率被限制在每 IP 每分钟约一次，且返回的数据较为简略（没有评分信息，仅包含顶级评论），对于少量查询来说已经足够。

**可选升级方案（仍无需用户登录）：** 若需要持续使用或获取完整数据，可前往 https://www.reddit.com/prefs/apps 注册一个免费的“脚本”类型应用，然后将该应用对应的两个配置值添加到 `~/.hermes/.env` 文件中。

```
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
```

这是一次应用注册操作，而非登录：该脚本使用仅限应用的`client_credentials`授权方式，绝不依赖用户名、密码或浏览器Cookie，也不会以用户身份进行操作。当同时设置好这两个参数时，它会自动切换到OAuth API模式（支持每分钟约100次请求，查看评分、嵌套评论及`num_comments`信息）；若这些参数缺失或被拒绝，它则会回退到匿名数据源，并通过标准错误流输出相应提示。

| | 匿名数据源（默认） | OAuth应用凭证 |
|---|---|---|
| 设置步骤 | 无需操作 | 需进行1分钟的应用注册，并配置两个`.env`文件中的参数 |
| 请求频率限制 | 每IP地址每分钟约1次请求 | 每分钟约100次请求 |
| 数据内容 | 帖文内容及顶级评论，不包含评分信息 | 嵌套评论、评分及评论数量 |
| 是否以用户身份操作 | 否 | 否 |

## 运行方式

通过终端运行相应命令，并指定与技能相关的脚本路径：

```bash
python3 scripts/reddit.py doctor                                  # which backend, current rate-limit window
python3 scripts/reddit.py sub LocalLLaMA --sort hot --limit 15
python3 scripts/reddit.py search "hermes agent" --sub LocalLLaMA --sort new
python3 scripts/reddit.py thread https://www.reddit.com/r/x/comments/abc123/slug/ --limit 40
python3 scripts/reddit.py user spez --limit 10
python3 scripts/reddit.py --json search "topic"                  # machine-readable
```

## 快速参考

所有命令在两种后端上均可使用；脚本会自动选择后端，无需手动传递任何参数。

| 需求 | 命令 | 匿名模式 | OAuth模式 |
|---|---|---|---|
| 子版块首页 | `sub NAME --sort hot\|new\|top\|rising [--time week]` | ✔ | ✔ |
| 搜索整个Reddit平台 | `search "q" --sort relevance\|new\|top\|comments` | ✔ | ✔ |
| 搜索特定子版块 | `search "q" --sub NAME` | ✔ | ✔ |
| 阅读帖子及评论 | `thread URL --limit N` | ✔ 仅支持顶级帖子，无评分信息 | ✔ 支持嵌套帖子，有评分信息 |
| 查看用户发布的帖子/评论 | `user NAME` | ✔ | ✔ |
| 后端状态与速率限制查询 | `doctor` | ✔ | ✔ |

## 操作步骤

① 若当前会话尚未调用 `doctor` 命令，则需为每个任务执行一次——该命令可告知您当前使用的后端以及匿名模式的使用剩余时间。

② 在执行操作前先规划好调用顺序。匿名模式下，每个IP每分钟大约只能发送**一次请求**；脚本会在收到429错误提示后暂停等待，待限制重置后再尝试一次。因此，若需发送5次请求，大约需要5分钟时间。建议使用一次 `search --sub` 命令替代多次 `sub` 命令，同时阅读单个帖子内容而非整个子版块列表。

③ 对于“社区在讨论什么”这类问题，应仔细阅读帖子正文（通过 `thread` 命令获取），而不要仅查看标题；因为列表仅显示每篇帖子的前约300个字符。

④ 在将查询结果用于报告时，请引用永久链接（即 `url` 字段）而非列表页面地址；`grounded-citations` 工具会像处理其他来源一样记录这些URL。

⑤ 如果用户需要持续访问 Reddit（如进行监控或发起超过约10次请求），应立即让其注册应用凭证（见前提条件），而非强行突破速率限制。需明确告知用户：这只是免费的注册流程，无需将 Hermes 登录到他们的账户中。绝不要索要 Reddit 密码或浏览器 Cookie。

## 常见问题

- 对于数据中心 IP，`www.reddit.com/…/.json`、`api.reddit.com` 以及 `old.reddit.com` 会返回 403 错误，或仅显示空白的“欢迎来到 Reddit”页面。切勿尝试使用这些地址，也不得伪造浏览器 User-Agent（同样会导致 403 错误）。
- `r.jina.ai` 以及 `browser_navigate` 工具也会遇到相同的限制（“被网络安全机制阻止”/人工验证）。虽然 `blocked-page-recovery` 的 Wayback 接口仍可找回已被归档的**旧**帖子，但无法获取最新内容。
- 匿名帖子源仅包含帖文及最顶层的评论（Reddit 对此类源的显示条目数有限制）；评分功能及回复嵌套功能仅支持通过 OAuth 访问。
- Reddit 对帖子源的“限制”仅具有建议性质——无论你请求多少条内容，实际获得的数量通常在 5 到 25 条之间。
- 绝不要将 `REDDIT_CLIENT_SECRET` 粘贴到聊天记录或日志中；该脚本仅会从环境变量中读取此密钥。
- 不要通过循环重试或添加代理来“解决”429 错误；速率限制是针对每个 IP 的，且脚本已自动等待过了规定的时间窗口。如果连续出现多次 429 错误，则说明该任务需要使用应用凭证。

## 验证方法

运行 `python3 scripts/reddit.py doctor` 命令会输出 `anonymous_feed: ok` 及相应的 `x-ratelimit-reset` 值；而执行 `sub announcements --limit 1` 命令则可获取包含 `reddit.com/r/announcements/comments/` 地址的一条记录。在已配置好认证信息的情况下，`doctor` 命令会显示 `active_backend: oauth`，同时 `thread …` 的输出结果会以数值形式呈现各项评分。
