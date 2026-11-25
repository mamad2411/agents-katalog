---
name: xurl
description: "X/Twitter via xurl CLI: raw post search, posting, DM, media."
version: 1.1.3
author: xdevplatform + openclaw + Hermes Agent
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [xurl]
metadata:
  hermes:
    tags: [twitter, x, social-media, xurl, official-api]
    homepage: https://github.com/xdevplatform/xurl
    upstream_skill: https://github.com/openclaw/openclaw/blob/main/skills/xurl/SKILL.md
---

# xurl — 通过官方 CLI 访问 X（Twitter）API

`xurl` 是 X 开发者平台专为 X API 提供的官方命令行工具。它既支持针对常见操作的快捷命令，也允许以原始的 curl 风格直接访问任何 v2 接口。所有命令都会将结果以 JSON 格式输出到标准输出流中。

该工具可用于以下操作：
- 发布、回复、引用或删除帖子
- 搜索原始帖子（包含可直接操作的帖子 ID 的完整 JSON 数据），以及查看时间线与提及内容
- 点赞、转发、收藏帖子
- 关注、取消关注、屏蔽或静音用户
- 发送私信
- 上传媒体文件（图片和视频）
- 以原始格式访问任何 X API v2 接口
- 多应用/多账户工作流管理

该工具已取代旧版的 `xitter` 工具（后者基于第三方 Python CLI 开发）。`xurl` 由 X 开发者平台团队维护，支持带自动刷新功能的 OAuth 2.0 PKCE 认证方式，且支持的 API 功能范围更为广泛。

---

## 密钥安全（强制要求）

在智能体/大型语言模型会话中使用时必须遵守的严格规则：

- **绝不可**读取、打印、解析、总结、上传或向大型语言模型传递 `~/.xurl` 文件中的内容。
- **绝不可**要求用户在聊天界面中粘贴凭证或访问令牌。
- 用户必须自行在其本地机器上填写 `~/.xurl` 文件中的密钥信息。在 Docker 环境中，该文件所在路径必须是 Hermes 工具子进程能够识别的 `~` 路径；具体说明请参见下方的 Docker 相关提示。
- **绝不可**在智能体会话中推荐或执行包含内联密钥的认证命令。
- **绝不可**在智能体会话中使用 `--verbose` / `-v` 参数——这可能会导致认证头信息或令牌泄露。
- 若需验证凭证是否存在，仅可使用命令：`xurl auth status`。
在代理命令中禁止使用以下标志（这些命令不支持内联密钥）：
`--bearer-token`、`--consumer-key`、`--consumer-secret`、`--access-token`、`--token-secret`、`--client-id`、`--client-secret`

应用程序凭据的注册及轮换必须由用户在代理会话之外手动完成。完成凭据注册后，用户需通过 `xurl auth oauth2` 命令进行身份验证，该操作同样需要在代理会话之外执行。生成的令牌会以 YAML 格式存储在 `~/.xurl` 文件中，且每个应用程序拥有独立的令牌。OAuth 2.0 令牌会自动刷新。

---

## 安装

请选择一种安装方式。在 Linux 系统上，使用 shell 脚本或 `go install` 命令最为简便。

```bash
# Shell script (installs to ~/.local/bin, no sudo, works on Linux + macOS)
curl -fsSL https://raw.githubusercontent.com/xdevplatform/xurl/main/install.sh | bash

# Homebrew (macOS)
brew install --cask xdevplatform/tap/xurl

# npm
npm install -g @xdevplatform/xurl

# Go
go install github.com/xdevplatform/xurl@latest
```

验证：

```bash
xurl --help
xurl auth status
```

如果已安装 `xurl`，但 `auth status` 显示没有应用或令牌，用户需要手动完成认证——详情请参见下一节。

---

## 一次性用户设置（由用户在代理程序外部执行）

这些步骤必须由用户亲自操作，而非由代理程序执行，因为其中涉及机密信息的粘贴。只需引导用户操作此部分内容，切勿代其执行。

1. 在 https://developer.x.com/en/portal/dashboard 创建或打开一个应用
2. 将重定向 URI 设置为 `http://localhost:8080/callback`
3. 复制该应用的客户端 ID 和客户端密钥
4. 在本地注册该应用（由用户操作）：
   ```bash
   xurl auth apps add my-app --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET
   ```
5. 验证身份（指定 `--app` 选项可将令牌绑定到您的应用）：
   ```bash
   xurl auth oauth2 --app my-app
   ```
（这将打开浏览器，进入 OAuth 2.0 PKCE 流程。）

如果在进行 OAuth 后的 `/2/users/me` 查询时，X 返回 `UsernameNotFound` 错误或 403 状态码，请直接传入您的账号标识（适用于 xurl v1.1.0 及更高版本）：
   ```bash
   xurl auth oauth2 --app my-app YOUR_USERNAME
   ```
这会将令牌绑定到您的账号标识，同时跳过已失效的 `/2/users/me` 接口调用。  
6. 将该应用设置为默认值，以便所有命令均使用它：
   ```bash
   xurl auth default my-app
   ```
7. 验证：
   ```bash
   xurl auth status
   xurl whoami
   ```

此后，该智能体无需额外设置即可使用以下任何命令，且OAuth 2.0令牌会自动刷新。

> **常见误区：** 如果在 `xurl auth oauth2` 命令中省略了 `--app my-app`，OAuth令牌将被保存到内置的 `default` 应用配置中——而该配置并不包含客户端ID或客户端密钥。即便OAuth流程看似已成功，命令仍会因认证错误而失败。遇到此情况，请重新运行 `xurl auth oauth2 --app my-app` 以及 `xurl auth default my-app`。

> **Docker HOME路径的误区：** 在官方的Hermes Docker部署结构中，`/opt/data` 被视为 `HERMES_HOME`，但Hermes工具的子进程会将 `/opt/data/home` 视为 `HOME`。这意味着对于由Hermes运行的 `xurl` 命令而言，`~/.xurl` 实际指向的是 `/opt/data/home/.xurl`，而非 `/opt/data/.xurl`。请使用相同的 `HOME` 路径来执行用户配置相关操作：
> ```bash
> HOME=/opt/data/home xurl auth apps add my-app --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET
> HOME=/opt/data/home xurl auth oauth2 --app my-app YOUR_USERNAME
> HOME=/opt/data/home xurl auth default my-app YOUR_USERNAME
> HOME=/opt/data/home xurl auth status
> ```
> 如果执行 `HOME=/opt/data xurl auth status` 可以正常运行，但执行 `HOME=/opt/data/home xurl auth status` 却显示没有应用或令牌，那是因为Hermes工具的调用无法获取到相应的凭证。

---

## 快速参考

| 操作 | 命令 |
| --- | --- |
| 发布内容 | `xurl post "Hello world!"` |
| 回复 | `xurl reply POST_ID "Nice post!"` |
| 引用 | `xurl quote POST_ID "My take"` |
| 删除帖子 | `xurl delete POST_ID` |
| 阅读帖子 | `xurl read POST_ID` |
| 搜索帖子 | `xurl search "QUERY" -n 10` |
| 查看当前用户身份 | `xurl whoami` |
| 查询用户信息 | `xurl user @handle` |
| 主页时间线 | `xurl timeline -n 20` |
| 被提及记录 | `xurl mentions -n 10` |
| 点赞/取消点赞 | `xurl like POST_ID` / `xurl unlike POST_ID` |
| 转发/撤销转发 | `xurl repost POST_ID` / `xurl unrepost POST_ID` |
| 收藏/取消收藏 | `xurl bookmark POST_ID` / `xurl unbookmark POST_ID` |
| 查看收藏列表/点赞记录 | `xurl bookmarks -n 10` / `xurl likes -n 10` |
| 关注/取消关注 | `xurl follow @handle` / `xurl unfollow @handle` |
| 正在关注的账号/关注者数量 | `xurl following -n 20` / `xurl followers -n 20` |
| 封禁/解封 | `xurl block @handle` / `xurl unblock @handle` |
| 静音/取消静音 | `xurl mute @handle` / `xurl unmute @handle` |
| 发送私信 | `xurl dm @handle "message"` |
| 查看私信列表 | `xurl dms -n 10` |
| 上传媒体文件 | `xurl media upload path/to/file.mp4` |
| 查询媒体文件状态 | `xurl media status MEDIA_ID` |
| 列出已授权应用 | `xurl auth apps list` |
| 移除应用 | `xurl auth apps remove NAME` |
| 设置默认应用 | `xurl auth default APP_NAME [USERNAME]` |
| 每次请求指定应用 | `xurl --app NAME /2/users/me` |
| 查询认证状态 | `xurl auth status` |

备注：
- `POST_ID` 也支持完整的 URL（例如 `https://x.com/user/status/1234567890`）——xurl 会自动提取其中的 ID。
- 用户名无论是否以 `@` 开头均可使用。

---

## 命令详情

### 发布内容

```bash
xurl post "Hello world!"
xurl post "Check this out" --media-id MEDIA_ID
xurl post "Thread pics" --media-id 111 --media-id 222

xurl reply 1234567890 "Great point!"
xurl reply https://x.com/user/status/1234567890 "Agreed!"
xurl reply 1234567890 "Look at this" --media-id MEDIA_ID

xurl quote 1234567890 "Adding my thoughts"
xurl delete 1234567890
```

### 阅读与搜索

`xurl search` 会以您已认证的账户身份查询 X 指数，并返回原始的帖子数据——包括帖子 ID、发布者以及完整文本内容——从而让您能够立即对这些内容进行操作（回复、点赞、转发、引用）。当您需要的是实际的帖子内容，而非关于某个主题的汇总答案时，可使用此功能。

```bash
xurl read 1234567890
xurl read https://x.com/user/status/1234567890

xurl search "golang"
xurl search "from:elonmusk" -n 20
xurl search "#buildinpublic lang:en" -n 15
```

对于 X 篇文章，建议使用原始 API 模式，而非 `read` 快捷指令。`xurl read` 需要帖子 ID 或帖子 URL；请勿在 `/2/tweets/...` 接口路径前加上 `read`。通过该指令获取 `article` 推文字段，并从 JSON 响应中提取 `data.article.plain_text` 数据。

```bash
xurl --app APP_NAME '/2/tweets/2057909493250539891?expansions=author_id,attachments.media_keys,referenced_tweets.id&tweet.fields=created_at,lang,public_metrics,context_annotations,entities,possibly_sensitive,conversation_id,in_reply_to_user_id,referenced_tweets,article'
```

### 用户、时间线与提及记录

```bash
xurl whoami
xurl user elonmusk
xurl user @XDevelopers

xurl timeline -n 25
xurl mentions -n 20
```

### 任务执行

```bash
xurl like 1234567890
xurl unlike 1234567890

xurl repost 1234567890
xurl unrepost 1234567890

xurl bookmark 1234567890
xurl unbookmark 1234567890

xurl bookmarks -n 20
xurl likes -n 20
```

### 社交关系图谱

```bash
xurl follow @XDevelopers
xurl unfollow @XDevelopers

xurl following -n 50
xurl followers -n 50

# Another user's graph
xurl following --of elonmusk -n 20
xurl followers --of elonmusk -n 20

xurl block @spammer
xurl unblock @spammer
xurl mute @annoying
xurl unmute @annoying
```

### 直接消息

```bash
xurl dm @someuser "Hey, saw your post!"
xurl dms -n 25
```

### 媒体文件上传

```bash
# Auto-detect type
xurl media upload photo.jpg
xurl media upload video.mp4

# Explicit type/category
xurl media upload --media-type image/jpeg --category tweet_image photo.jpg

# Videos need server-side processing — check status (or poll)
xurl media status MEDIA_ID
xurl media status --wait MEDIA_ID

# Full workflow
xurl media upload meme.png                  # returns media id
xurl post "lol" --media-id MEDIA_ID
```

## 直接调用 API

这些快捷命令涵盖了常见的操作。对于其他需求，可直接通过 curl 风格的方式调用任意 X API v2 接口。

```bash
# GET
xurl /2/users/me

# POST with JSON body
xurl -X POST /2/tweets -d '{"text":"Hello world!"}'

# DELETE / PUT / PATCH
xurl -X DELETE /2/tweets/1234567890

# Custom headers
xurl -H "Content-Type: application/json" /2/some/endpoint

# Force streaming
xurl -s /2/tweets/search/stream

# Full URLs also work
xurl https://api.x.com/2/users/me
```

---

## 全局标志

| 标志 | 缩写 | 描述 |
| --- | --- | --- |
| `--app` | | 使用特定的已注册应用（覆盖默认值） |
| `--auth` | | 强制指定认证类型：`oauth1`、`oauth2` 或 `app` |
| `--username` | `-u` | 指定要使用的 OAuth2 账户（如存在多个账户时使用） |
| `--verbose` | `-v` | **在代理会话中禁止使用**——会导致认证标头泄露 |
| `--trace` | `-t` | 添加 `X-B3-Flags: 1` 追踪标头 |

---

## 流式处理

流式处理端点会自动检测。已知的端点包括：

- `/2/tweets/search/stream`
- `/2/tweets/sample/stream`
- `/2/tweets/sample10/stream`

可使用 `-s` 强制在任何端点上启用流式处理。

---

## 输出格式

所有命令都会以 JSON 格式将结果输出到标准输出。其结构与 X API v2 相同：

```json
{ "data": { "id": "1234567890", "text": "Hello world!" } }
```

错误信息同样以 JSON 格式呈现：

```json
{ "errors": [ { "message": "Not authorized", "code": 403 } ] }
```

## 常见工作流程

### 发布带图片的内容
```bash
xurl media upload photo.jpg
xurl post "Check out this photo!" --media-id MEDIA_ID
```

### 回复对话内容
```bash
xurl read https://x.com/user/status/1234567890
xurl reply 1234567890 "Here are my thoughts..."
```

### 搜索并与目标对象互动
```bash
xurl search "topic of interest" -n 10
xurl like POST_ID_FROM_RESULTS
xurl reply POST_ID_FROM_RESULTS "Great point!"
```

### 查看您的活动记录
```bash
xurl whoami
xurl mentions -n 20
xurl timeline -n 20
```

### 多个应用（凭据已手动预配置）
```bash
xurl auth default prod alice               # prod app, alice user
xurl --app staging /2/users/me             # one-off against staging
```

## 错误处理

- 任何错误都会导致非零的退出码。
- API 错误仍会以 JSON 格式输出到标准输出流，便于您解析。
- 认证错误 → 需要用户在代理会话之外重新运行 `xurl auth oauth2` 命令。
- 需要调用者用户 ID 的命令（如转发、收藏、关注等）会自动通过 `/2/users/me` 获取该信息。若在此过程中发生认证失败，将会表现为认证错误。

## 代理工作流程

1. 验证前置条件：运行 `xurl --help` 和 `xurl auth status`。
2. 在使用 `xurl search` 之前，先确认用户意图。当任务需要真实的帖子内容、已认证的账户信息，或涉及向 X 平台发送内容的操作时，才应使用该命令——因为此时用户希望获取可互动的帖子内容，而不仅仅是某个主题的概要。
3. **检查默认应用是否拥有授权凭证**。解析 `auth status` 的输出结果，默认应用会标有 `▸` 符号。如果默认应用显示为 `oauth2: (none)`，而其他应用拥有有效的 oauth2 用户账户，请告知用户运行 `xurl auth default <that-app>` 来解决问题。这是最常见的配置错误——用户添加了自定义名称的应用，却从未将其设为默认应用，因此 xurl 会一直尝试使用空的“默认”配置文件。
4. 如果完全缺乏授权信息，请立即停止操作，并引导用户前往“一次性用户设置”部分——切勿尝试自行注册应用或传递密钥。
5. 先通过简单的读取操作（如 `xurl whoami`、`xurl user @handle`、`xurl search ... -n 3`）来确认系统是否可正常访问。
6. 在执行任何写入操作（发布帖子、回复、点赞、转发、私信、关注、屏蔽、删除）之前，务必确认目标帖子/用户以及用户的真实意图。
7. 只有 `xurl` 命令的输出结果（或原始的 X API 响应）才能证明确实发生了会改变系统状态的 X 平台操作。绝不可依据搜索结果、概要内容或其他背景信息来判定写入操作已完成。
8. 直接使用 JSON 格式的输出——所有响应都已具备结构化格式。
9. 绝对不要将 `~/.xurl` 文件中的内容重新粘贴到对话中。

---

## 故障排除

| 症状 | 原因 | 解决方案 |
| --- | --- | --- |
| OAuth流程成功后出现认证错误 | 令牌被保存到`default`应用（无客户端ID/密钥）而非您指定的应用 | 先执行`xurl auth oauth2 --app my-app`，再执行`xurl auth default my-app` |
| OAuth过程中出现`unauthorized_client`错误 | X控制台中的应用类型设置为“原生应用” | 在用户认证设置中将其更改为“Web应用、自动化应用或机器人” |
| OAuth完成后访问 `/2/users/me` 时出现`UsernameNotFound`或403错误 | X无法从 `/2/users/me` 稳定返回用户名 | 重新运行`xurl auth oauth2 --app my-app YOUR_USERNAME`（需使用xurl v1.1.0+版本），以直接传入用户名标识 |
| 所有请求均返回401错误 | 令牌已过期或默认应用设置错误 | 查看`xurl auth status`——确认带有`▸`符号的应用支持oauth2令牌 |
| 出现`client-forbidden`/`client-not-enrolled`错误 | X平台注册存在问题 | 进入控制台 → 应用 → 管理 → 更改为“按使用量计费”套餐 → 生产环境 |
| 出现`CreditsDepleted`错误 | X API账户余额为0美元 | 前往开发者控制台 → 账单页面购买额度（最低5美元） |
| 上传图片时出现`media processing failed`错误 | 默认分类为`amplify_video` | 添加`--category tweet_image --media-type image/png`参数 |
| X控制台显示两个“Client Secret”值 | 界面缺陷——第一个实际上为客户端ID | 在“密钥与令牌”页面进行确认；真正的客户端ID以`MTpjaQ`结尾 |

---

## 备注

- **速率限制**：X 会对每个接口端点实施速率限制。收到 429 错误时，需等待后重试。写入类接口（如 post、reply、like、repost）的速率限制比读取类接口更为严格。
- **权限范围**：OAuth 2.0 令牌通常会使用较宽泛的权限范围。若执行特定操作时出现 403 错误，往往意味着该令牌缺少相应的权限范围——请让用户重新运行 `xurl auth oauth2` 命令。
- **令牌刷新**：OAuth 2.0 令牌会自动刷新，无需手动操作。
- **多个应用**：每个应用拥有独立的凭证/令牌。可通过 `xurl auth default` 或 `--app` 参数切换当前使用的应用。
- **单个应用内的多个账户**：可使用 `-u / --username` 参数选择特定账户，或通过 `xurl auth default APP USER` 设置默认账户。
- **令牌存储**：令牌以 YAML 格式存储在 `~/.xurl` 文件中。在 Docker 环境下，应使用 Hermes 的子进程 HOME 目录（官方镜像中的路径为 `/opt/data/home`），这样令牌就会保存在 `/opt/data/home/.xurl` 文件中。切勿将此文件的内容读取或上传至大语言模型的上下文环境中。
- **费用说明**：使用 X API 通常需要根据实际使用量付费。许多错误其实源于套餐配置或权限问题，而非代码故障。

---

## 参考来源

- 上游 CLI 工具：https://github.com/xdevplatform/xurl（X 开发者平台团队，Chris Park 等人开发）
- 上游智能体技能文档：https://github.com/openclaw/openclaw/blob/main/skills/xurl/SKILL.md
- Hermes 版本适配：已根据 Hermes 的智能体规范重新格式化，安全约束规则保持不变。
