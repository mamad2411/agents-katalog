---
name: here-now
description: Publish sites to {slug}.here.now and store files in Drives.
version: 1.15.3
author: here.now
license: MIT
prerequisites:
  commands: [curl, file, jq]
platforms: [macos, linux]
metadata:
  hermes:
    tags: [here.now, herenow, publish, deploy, hosting, static-site, web, share, URL, drive, storage]
    homepage: https://here.now
    requires_toolsets: [terminal]
---

# here.now

here.now 允许智能体在云端驱动器中发布网站并存储私有文件。

该功能可用于完成以下两项任务：

- **网站发布**：将网站和文件发布到 `{slug}.here.now` 地址。
- **文件存储**：在云端文件夹中保存智能体的私有文件。

## 当前文档

**在回答有关 here.now 的功能、特性或工作流程的问题之前，请先阅读最新文档：**

→ **https://here.now/docs**

建议在以下情况下阅读文档：
- 对话中首次涉及 here.now 相关内容时
- 用户询问操作方法时
- 用户询问哪些功能可用、受支持或被推荐使用时
- 在告知用户某项功能不受支持之前

以下主题需要参考最新文档（不可仅依赖本地技能库中的内容）：
- 云端驱动器及共享功能
- 自定义域名
- 支付及支付限制机制
- 分支创建功能
- 代理路由与服务变量
- 文件路径与链接处理
- 使用限制与配额设置
- 单页应用路由
- 错误处理与解决方案
- 功能可用性

**若文档内容与实际 API 行为存在差异，请以实际 API 行为为准。**

如果文档加载失败或超时，则继续参考本地技能库的内容以及实际 API/脚本的输出结果。对于实时操作，建议优先遵循实际 API 的行为规范。

## 需求条件

- 必需的二进制文件：`curl`、`file`、`jq`
- 可选的环境变量：`$\HERENOW_API_KEY`
- 可选的 Drive 令牌变量：`$\HERENOW_DRIVE_TOKEN`
- 可选的凭据文件：`~/.herenow/credentials`
- 技能辅助脚本路径：
  - 用于发布站点的脚本：`${HERMES_SKILL_DIR}/scripts/publish.sh`
  - 用于私有 Drive 存储的脚本：`${HERMES_SKILL_DIR}/scripts/drive.sh`

## 创建站点

```bash
PUBLISH="${HERMES_SKILL_DIR}/scripts/publish.sh"
bash "$PUBLISH" {file-or-dir} --client hermes
```

会输出该站点的实时网址（例如 `https://bright-canvas-a7k2.here.now/`）。

其内部处理流程分为三步：创建/更新 -> 上传文件 -> 完成配置。只有当“完成配置”步骤成功后，站点才会正式上线。

若未使用 API 密钥，则会生成一个**匿名站点**，且该站点在 24 小时后失效。
而使用已保存的 API 密钥，则可创建永久性的站点。

**文件结构：** 对于 HTML 站点，请将 `index.html` 文件放置在发布目录的根目录中，而非子目录内。该目录的内容即构成站点的根目录。例如，应在存在 `my-site/index.html` 的 `my-site/` 目录下进行发布——切勿发布包含 `my-site/` 的上层文件夹。

您也可以直接发布不包含 HTML 的原始文件。单个文件会自动生成丰富的预览器（支持图片、PDF、视频、音频格式）；多个文件则会自动生成带文件夹导航功能的目录列表以及图片画廊。

## 更新现有站点

```bash
PUBLISH="${HERMES_SKILL_DIR}/scripts/publish.sh"
bash "$PUBLISH" {file-or-dir} --slug {slug} --client hermes
```

在更新匿名站点时，该脚本会自动从 `.herenow/state.json` 中加载 `claimToken`。如需覆盖此值，可传递 `--claim-token {token}` 参数。

进行需要身份验证的更新时，则必须使用已保存的 API 密钥。

## 使用驱动器

当用户希望为代理文件提供私有云存储空间时，可使用驱动器：这些文件包括文档、上下文信息、内存数据、计划内容、资源文件、媒体资料、研究素材、代码，以及任何无需以网站形式公开即可长期保存的内容。

每个已登录账户都拥有一个名为 “My Drive” 的默认驱动器。

```bash
DRIVE="${HERMES_SKILL_DIR}/scripts/drive.sh"
bash "$DRIVE" default
bash "$DRIVE" ls "My Drive"
bash "$DRIVE" put "My Drive" notes/today.md --from ./notes/today.md
bash "$DRIVE" cat "My Drive" notes/today.md
bash "$DRIVE" share "My Drive" --perms write --prefix notes/ --ttl 7d
```

在代理之间进行数据传递时，请使用作用域限定的 Drive 令牌。若收到包含 `herenow_drive` 的共享块，需将其 `token` 作为 `Authorization: Bearer <token>` 的值用于调用 `api_base`，同时需遵循现有的 `pathPrefix` 规则，并在写入操作时保留 ETags。当 `pathPrefix` 设为 `null` 时，表示具有对整个 Drive 的访问权限。若该技能支持 `drive.sh`，则优先使用它；否则请直接调用列出的 API 操作。

## API 密钥存储

发布脚本会从以下来源读取 API 密钥（按顺序优先匹配）：

1. `--api-key {key}` 参数（仅适用于 CI/脚本环境——交互式使用时请避免使用）
2. `$HERENOW_API_KEY` 环境变量
3. `~/.herenow/credentials` 文件（推荐代理使用）

如需存储密钥，请将其写入该凭证文件中：

```bash
mkdir -p ~/.herenow && echo "{API_KEY}" > ~/.herenow/credentials && chmod 600 ~/.herenow/credentials
```

**重要提示**：收到 API 密钥后，请立即将其保存——请亲自运行上述命令，切勿让用户手动操作。在交互式会话中，请避免通过 CLI 参数（如 `--api-key`）传递该密钥；使用凭证文件才是更推荐的存储方式。

切勿将凭证文件或本地状态文件（如 `~/.herenow/credentials`、`.herenow/state.json`）提交到版本控制系统中。

## 获取 API 密钥

若要将匿名（24小时有效）站点升级为永久站点：

1. 请用户提供其电子邮件地址。
2. 请求一个一次性登录码：

```bash
curl -sS https://here.now/api/auth/agent/request-code \
  -H "content-type: application/json" \
  -d '{"email": "user@example.com"}'
```

3. 告诉用户：“请查看您的收件箱，查看此处发送的登录码，然后将其粘贴到这里。”
4. 验证该代码并获取 API 密钥：

```bash
curl -sS https://here.now/api/auth/agent/verify-code \
  -H "content-type: application/json" \
  -d '{"email":"user@example.com","code":"ABCD-2345"}'
```

5. 请自行保存返回的 `apiKey`（无需让用户来操作此步骤）：

```bash
mkdir -p ~/.herenow && echo "{API_KEY}" > ~/.herenow/credentials && chmod 600 ~/.herenow/credentials
```

## 状态文件

每次创建或更新站点后，脚本都会将相关数据写入工作目录下的 `.herenow/state.json` 文件中：

```json
{
  "publishes": {
    "bright-canvas-a7k2": {
      "siteUrl": "https://bright-canvas-a7k2.here.now/",
      "claimToken": "abc123",
      "claimUrl": "https://here.now/claim?slug=bright-canvas-a7k2&token=abc123",
      "expiresAt": "2026-02-18T01:00:00.000Z"
    }
  }
}
```

在创建或更新站点之前，您可以查看此文件以获取之前的站点标识符。请将 `.herenow/state.json` 视为仅用于内部缓存的文件。切勿将此本地文件路径作为 URL 使用，也不得将其用作认证模式、有效期或声明 URL 的权威来源。

## 应向用户说明的内容

对于已发布的站点：

- 始终提供当前脚本运行所生成的 `siteUrl`。
- 查看脚本标准错误输出中的 `publish_result.*` 行内容，以此确定认证模式。
- 当 `publish_result.auth_mode=authenticated` 时，告知用户该站点为**永久性**存储在他们的账户中，无需提供声明 URL。
- 当 `publish_result.auth_mode=anonymous` 时，告知用户该站点**24 小时后过期**。如果 `publish_result.claim_url` 不为空且以 `https://` 开头，可提供该声明 URL 以便用户永久保存。同时需提醒用户，声明令牌仅会发放一次且无法恢复。
- 绝对不要建议用户通过查看 `.herenow/state.json` 来获取声明 URL 或认证状态。

对于 Drive 存储：

- 不要将 Drive 文件描述为公开 URL。
- 告知用户，除非使用带有限定范围的令牌进行共享，否则 Drive 内容为私密状态。
- 在与其他代理共享访问权限时，建议优先使用 `pathPrefix` 范围较窄且有效期较短的限定范围令牌。

## publish.sh 参数选项

| 标志                   | 描述                                  |
| ---------------------- | -------------------------------------------- |
| `--slug {slug}`        | 更新现有站点而非创建新站点                 |
| `--claim-token {token}`| 为匿名更新覆盖声明令牌                   |
| `--title {text}`       | 查看器标题（非 HTML 站点使用）             |
| `--description {text}` | 查看器描述                             |
| `--ttl {seconds}`      | 设置过期时间（仅限已认证用户使用）           |
| `--client {name}`      | 用于归属标识的 Agent 名称（例如 `hermes`）    |
| `--base-url {url}`     | API 基础 URL（默认值：`https://here.now`）    |
| `--allow-nonherenow-base-url` | 允许向非默认的 `--base-url` 发送认证信息   |
| `--api-key {key}`      | 覆盖 API 密钥（优先使用凭证文件）           |
| `--spa`                | 启用单页应用路由（对未知路径返回 index.html） |
| `--forkable`           | 允许他人复制此站点                         |

## 除 publish.sh 之外的功能

如需执行 Drive 相关操作，请使用 `drive.sh` 或 Drive API。如需管理账户及站点更广泛的功能——包括删除、元数据、密码、支付、域名、用户名、链接、变量、代理路由、复制等功能——请参阅最新文档：

→ **https://here.now/docs**

完整文档：https://here.now/docs
