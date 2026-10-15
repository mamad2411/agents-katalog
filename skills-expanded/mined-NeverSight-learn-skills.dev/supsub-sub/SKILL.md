---
name: supsub-sub
version: 0.1.5
description: SupSub 订阅管理 —— 列出 / 添加 / 删除订阅源（微信公众号 MP、网站 WEBSITE、推特 X），浏览某个已订阅源里的文章列表（支持翻页），以及把某个源整源标记为已读。匹配「列出我的订阅」「我订阅了哪些」「取消订阅某个号」「订阅某个公众号 / 网站」「看某个订阅里有哪些文章」「某公众号最近的未读文章」「添加 / 删除订阅源」「看更早的文章 / 翻页」「这个号我读完了 / 整源标记已读」。⚠️ 已读只有**整源**一档（`mark-read --all`，不可逆）：文章没有「详情 / 阅读」这一步，故不支持单篇标记已读。⚠️ 也匹配**用主体名指代自己订阅源**的浏览句式：「看一下最近 X 的内容」「X 最近有什么」「X 更新了吗」「读读 X」—— 遇到这类请求先 `supsub sub list` 比对 X 是不是已订阅的源名（包含匹配、忽略大小写），命中就用 `sub contents` 拉该源内容，**不要**当成全站关键词搜索；没命中则直接改用 supsub-search 执行全站搜索（**不要反问用户要不要搜**）。⚠️ 本 skill 里 `--type X` 专指推特/Twitter 平台账号；用户口语「订阅 X」「X 公众号」中的字母 X 往往只是占位、代指某个具体账号，并不等于 `--type X`。⚠️ 动词判别：本 skill 只认「订阅 / 订阅了」；用户说「关注 / 关注了 / 我关注了哪些 / 我的关注点」时走 supsub-focus（关注点），不是本 skill。⚠️ 不用于跨订阅搜索文章关键词（走 supsub-search），也不用于「发现一个新的公众号」（走 supsub-mp）。
---

# supsub-sub Skill

List, add, remove subscription sources, and browse the articles inside each source. Sources are typed `MP`（微信公众号）、`WEBSITE`（网站）或 `X`（推特 / Twitter 平台账号）。

## ⚠️ 关于字母「X」的歧义（务必先读）

本文档里 `X` 有两种**完全不同**的含义，不要混淆：

1. **`--type X`** —— 这是一个真实的 sourceType 枚举值，专指 **推特 / Twitter / X 平台账号**。
2. **占位符 X** —— 用户口语里说「订阅 X」「取消订阅 X」「X 公众号最近的文章」时，这里的 X 通常只是一个占位代号，代指**某个具体账号**（可能是公众号、网站，也可能就是名字里带 X），**与推特无关**。

判定规则：

- 只有当用户**明确提到「推特 / Twitter / X 平台」**时，才使用 `--type X`。
- 用户说「订阅 X」「X 公众号」「看 X 的文章」而没有提到推特平台时，**不要**据此推断 `--type X`；这里的 X 是占位符，应按其真实类型（多为 `MP` 或 `WEBSITE`）处理。

## Prerequisites

- 安装：`curl -fsSL https://raw.githubusercontent.com/SupSub-AI/supsub-cli/master/scripts/install.sh | bash`（native 安装，装到 `~/.local`、支持后台自动更新）；或包管理器 `npm i -g @supsub/cli` / `pnpm add -g @supsub/cli`
- 已登录：`supsub auth status` 显示 Authenticated（首次使用先 `supsub auth login`）
- **未授权（exit 2 / UNAUTHORIZED）时不要止步于「你未登录」**：直接运行 `supsub auth login` 为用户打开浏览器授权（命令会自动打开浏览器并阻塞等待授权，请用足够长的超时，如 10 分钟；用户只需在浏览器点确认，无需在终端输入任何内容），授权成功后重试原命令。无浏览器 / 无头环境再回退为提示用户 `SUPSUB_NO_BROWSER=1 supsub auth login`。

## Commands

### List subscriptions

```
supsub sub list [--type <MP|WEBSITE|X>]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--type` | — (all) | 过滤来源类型：`MP`（公众号）/ `WEBSITE`（网站）/ `X`（推特） |

Each row includes: `sourceId`, `sourceType`, `name`, `img`, `description`, `unreadCount`。表格模式下 `类型` 列会把 sourceType 显示为中文：`MP`→公众号、`WEBSITE`→网站、`X`→推特。

```bash
# 列出全部订阅
supsub sub list

# 仅看公众号
supsub sub list --type MP

# 仅看网站
supsub sub list --type WEBSITE

# 仅看推特（X 平台账号）
supsub sub list --type X

# 导出 JSON
supsub sub list -o json
```

JSON shape: `{"success":true,"data":[{"sourceType":"MP","sourceId":12345,"name":"...","img":"...","description":"...","unreadCount":3}, ...]}`

---

### Add a subscription

`sub add` 有两条互斥入口，对应两种"拿到的 ID 形态"：

```
# A) 全局搜索 / 已收录源 → 用内部正整数 sourceId
supsub sub add --source-id <id> --type <MP|WEBSITE|X> [--group <gid>]...

# B) mp search 发现的微信原生公众号 → 用 base64 字符串 mpId
supsub sub add --mp-id <mpId> [--type MP] [--group <gid>]...
```

| Flag | Required | Description |
|------|----------|-------------|
| `--source-id` | 二选一 | 信息源 ID（正整数）。来自 `supsub search` / `supsub sub list` 的 `sourceId` |
| `--mp-id` | 二选一 | 公众号 mpId（base64 字符串）。来自 `supsub mp search` 返回结果 |
| `--type` | 见说明 | `--source-id` 模式必填，取 `MP` / `WEBSITE` / `X`（推特）；`--mp-id` 模式可省，传了必须是 `MP` |
| `--group` | no | 分组 ID（数字，可重复指定多个） |

> **互斥**：`--source-id` 与 `--mp-id` 必须恰好二选一。同时给 / 都不给都会抛 `INVALID_ARGS`。
>
> 两条路径走的是不同 endpoint：`--source-id` → `POST /api/subscriptions`（已收录源订阅）；`--mp-id` → `POST /api/mps`（按微信原生 ID 把新公众号纳入并订阅）。

```bash
# 路径 A：sub list / search 看到的内部 sourceId（公众号）
supsub sub add --source-id 12345 --type MP

# 路径 A：网站 + 多分组
supsub sub add --source-id 67890 --type WEBSITE --group 1 --group 2

# 路径 A：推特账号（用户明确说要订阅某个 Twitter / X 平台账号时）
supsub sub add --source-id 24680 --type X

# 路径 B：mp search 拿到的 mpId（base64）
supsub sub add --mp-id "MzkyNTYzODk0NQ=="

# 路径 B + 分组
supsub sub add --mp-id "MzkyNTYzODk0NQ==" --group 3

# JSON 输出
supsub sub add --source-id 12345 --type MP -o json
```

JSON shape: `{"success":true,"data":{"message":"..."}}`

> `--source-id` 必须是正整数（非数字 → `INVALID_ARGS`）；`--mp-id` 是字符串，不做格式校验，由后端裁决；`--group` 接受多个数字 ID，非数字会报 `INVALID_ARGS` (exit 64)。

---

### Remove a subscription

```
supsub sub remove --source-id <id> --type <MP|WEBSITE|X>
```

| Flag | Required | Description |
|------|----------|-------------|
| `--source-id` | yes | 信息源 ID（正整数） |
| `--type` | yes | `MP`（公众号）/ `WEBSITE`（网站）/ `X`（推特） |

> ⚠️ **退订是破坏性操作，执行前必须向用户二次确认**：复述源名称（从 `sub list` 取），获得明确同意后才执行。
> 与 mark-read 一样，**CLI 不会再问一次**——把命令交给用户自己在终端跑时，不要说「执行后会提示确认」。
>
> ⚠️ **退订会连带把该源移出它所在的全部分组**（实测：订阅并入组后退订，`group subs` 返回空）。
> 分组本身不受影响。重新订阅**不会**自动恢复原来的分组归属，需要再跑一次 `group add-sub`。
> 因此用户说「先退订，回头再订回来」时，要提醒他分组归属会丢。

```bash
# 取消订阅某个公众号（需用户确认后执行）
supsub sub remove --source-id 12345 --type MP

# 取消订阅某个网站
supsub sub remove --source-id 67890 --type WEBSITE -o json

# 取消订阅某个推特账号
supsub sub remove --source-id 24680 --type X
```

JSON shape: `{"success":true,"data":{"message":"..."}}`

---

### Browse articles in a subscription

```
supsub sub contents --source-id <id> --type <MP|WEBSITE|X> [--unread | --all] [--brief] [--page <n>] [--page-size <n>]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--source-id` | required | 信息源 ID（正整数）。**别名 `--id`**（与 `focus contents --id` 对齐，两个写法等价） |
| `--type` | required | `MP`（公众号）/ `WEBSITE`（网站）/ `X`（推特） |
| `--unread` | (default) | 仅返回未读文章 |
| `--all` | — | 返回全部文章（已读 + 未读） |
| `--brief` | — | 精简输出：只留 `contentId` / `title` / `publishedAt(+Text)` / `isRead` |
| `--page` | 1 | 页码（正整数） |
| `--page-size` | 20 | 每页条数，1-100 |

> ⚠️ `--unread` 与 `--all` **互斥**：同时指定会抛 `INVALID_ARGS`。不传任何一个时，默认行为等价于 `--unread`。

**⚠️ 「最近」不等于「未读」—— 按用户意图选 flag，别让默认值替用户做决定：**

| 用户说法 | 意图 | 用哪个 |
|---|---|---|
| 「看一下最近 X 的内容」「X 最近有什么」「X 讲了什么」「X 更新了吗」 | 按时间看这个源在讲什么 | **`--all`**，`isRead` 只用来**标注**（「其中 3 篇你还没看过」），**不要拿来过滤** |
| 「X 还有什么没看的」「X 的未读」「X 剩几篇没读」 | 明确要未读 | 默认（`--unread`） |
| 说不清 | —— | **`--all`** + 标注哪些未读 |

用默认值应付「看一下最近 X 的内容」会踩这个坑：**该源已经读完时返回空数组**，于是回复「没有内容」——
可用户问的是「最近」，不是「没读的」。只有用户话里出现「未读 / 没看的 / 没读的 / 清未读」才该过滤。

**批量枚举一律加 `--brief`**：默认输出每条都带 `summary` / `coverImage` / `tags`，100 条约 90KB，
足以撑爆工具输出上限被迫落盘；`--brief` 同样 100 条只有约 14KB。只在需要给用户讲内容时才用完整输出。

每行字段：`contentId`, `url`, `title`, `coverImage`, `tags[]`, `summary`, `publishedAt`, `publishedAtText`, `isRead`。
`--brief` 时只有 `contentId`, `title`, `publishedAt`, `publishedAtText`, `isRead`。

> `publishedAt` 是 Unix 秒级时间戳（少数后端版本为字符串），**`publishedAtText` 是 CLI 已格式化好的
> `"YYYY-MM-DD HH:mm"`，直接用即可，不要自己写 `date -r` / 时间戳转换**。排序仍用 `publishedAt`。

```bash
# 默认（未读）—— 看某个公众号里有哪些文章
supsub sub contents --source-id 12345 --type MP

# 全部文章（含已读）
supsub sub contents --source-id 12345 --type MP --all

# 看更早的文章：翻到第 2 页
supsub sub contents --source-id 12345 --type MP --page 2

# 一次多拿一些（上限 100）
supsub sub contents --source-id 12345 --type MP --page-size 100 -o json

# 全部文章 + JSON
supsub sub contents --source-id 12345 --type MP --all -o json
```

JSON shape: `{"success":true,"data":[{"contentId":"...","url":"...","title":"...","coverImage":"...","tags":[...],"summary":"...","publishedAt":<timestamp 或字符串>,"isRead":false}, ...]}`

> `publishedAt` 的原始形态随后端版本而异（Unix 秒数字 / `"YYYY-MM-DD HH:mm:ss"` 字符串），
> **不用自己兼容——直接读 CLI 补好的 `publishedAtText`**（恒为 `"YYYY-MM-DD HH:mm"`）。
>
> 翻页策略：浏览类请求只拉第 1 页并告知总量；「全部 / 统计 / 导出」类请求用 `--page-size 100` 自动循环翻页（返回条数 < page-size 即末页），不要逐页询问用户。详见 `supsub-unread`。

---

### Mark a source as read（整源标记已读）

```
supsub sub mark-read --source-id <id> --type <MP|WEBSITE|X> --all
```

| Flag | Required | Description |
|------|----------|-------------|
| `--source-id` | yes | 信息源 ID（正整数） |
| `--type` | yes | `MP` / `WEBSITE` / `X`（推特） |
| `--all` | yes | 确认整源全部标为已读（**不可逆**） |

> ⚠️ **只支持整源已读，没有单篇已读。** 文章没有「详情 / 阅读」这一步，产生不了自然的单篇已读事件，所以 CLI 只保留用户明确表达的「这个号我读完了」。传 `--content-id` 会抛 `INVALID_ARGS`。用户说「把这篇标为已读」时如实说明不支持，并问是否要整源已读。
>
> ⚠️ **`--all` 必填且不可逆**（CLI 无 mark-as-unread）。执行前必须向用户**二次确认**：复述源名称 + 当前未读数（从 `sub list` / `supsub unread` 取），获得明确同意后才执行。
>
> **CLI 不会再问一次**：这条命令没有交互式确认提示，一执行就生效。若把命令交给用户自己在终端跑，
> **不要说「执行后 CLI 会提示确认」**——那是不存在的安全网。

```bash
# 整源已读（需用户确认后执行）
supsub sub mark-read --source-id 12345 --type MP --all -o json
```

JSON shape: `{"success":true,"data":{"message":"已标记该订阅源全部内容为已读（不可逆）"}}`

---

## Agent Usage Notes

- 解析数据时统一用 `-o json`；表格输出有截断、列宽限制，不适合做下游处理。
- 所有 JSON 响应都是 `{"success":true,"data":<payload>}` 结构（来自 `src/ui/output.ts`）。
- `--type` 取值是 `MP` / `WEBSITE` / `X`（CLI 内部会 `toUpperCase`，大小写不敏感）；常见错误是写成 `mp_account` / `wechat` / `rss` / `TWITTER` 会报 `INVALID_ARGS`——**推特只接受 `X`，不接受 `TWITTER`**。
- 再次强调字母「X」的歧义：`--type X` = 推特平台账号。用户口语里「订阅 X」「X 公众号」「看 X 的文章」中的 X 多半是占位符代指某个具体账号，**不要**因为出现字母 X 就传 `--type X`；只有用户明确提到「推特 / Twitter / X 平台」时才用 `--type X`。
- 添加订阅前先想清楚 ID 来源：
  - 来自 `supsub search` / `sub list` 的 **内部正整数** `sourceId` → `sub add --source-id <id> --type ...`
  - 来自 `supsub mp search` 的 **base64 字符串** `mpId` → `sub add --mp-id <mpId>`（type 默认 MP，可省）
  - 不要把 `mp search` 的 `mpId` 强转成数字塞进 `--source-id` —— 那是不同 ID 空间，会被后端拒。
- `sub contents` 默认只看未读 —— **「看一下最近 X 的内容」「这个号有哪些文章」「X 讲了什么」这类按时间浏览的请求一律加 `--all`**，把 `isRead` 当标注而不是过滤条件；只有用户明说「未读 / 没看的」才用默认。
- `sub contents` 默认每页 20 条，用 `--page` / `--page-size`（上限 100）翻页取更早的历史。
- **标记已读只有整源一档**（`mark-read --all`）：没有单篇已读，因为文章没有「详情 / 阅读」这一步。**整源已读不可逆，执行前必须向用户二次确认**。跨源的未读概览与清未读工作流见 `supsub-unread`。
- 分组管理（把这个源加进某个分组、分组里有哪些订阅）见 `supsub-group`；订阅时可直接用 `sub add --group <gid>` 一步入组。
- **重复订阅不是错误**：实测对同一个源再跑一次 `sub add` 返回 `{"success":true,"data":{"message":"订阅成功"}}`，exit `0`（幂等）。不要据此判断"是否已订阅"——要判断请看 `sub list` 或搜索结果里的 `isSubscribed`。**重复退订才会报错**（`订阅不存在`，400 → exit `1`），两者不对称。
- Exit codes：`0` OK，`2` UNAUTHORIZED，`64` INVALID_ARGS（`--type` / `--source-id` / `--group` / `--page` / `--page-size` 校验失败、`--all` 与 `--unread` 互斥、mark-read 未给 `--all` 或误传 `--content-id`），`1` 业务错误（后端 4xx，如源不存在 / 未订阅 / 重复退订），`10` 网络错误，`11` 服务端错误（5xx）。
