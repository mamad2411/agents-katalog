---
name: google-workspace
description: "Gmail, Calendar, Drive, Docs, Sheets via gws CLI or Python."
version: 1.2.0
author: Nous Research
license: MIT
platforms: [linux, macos, windows]
required_credential_files:
  - path: google_token.json
    description: Google OAuth2 token (created by setup script)
  - path: google_client_secret.json
    description: Google OAuth2 client credentials (downloaded from Google Cloud Console)
metadata:
  hermes:
    tags: [Google, Gmail, Calendar, Drive, Sheets, Docs, Contacts, Email, OAuth]
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills: [himalaya]
---

# Google Workspace

通过Hermes管理的OAuth机制以及轻量级的CLI封装层，可支持Gmail、Calendar、Drive、Contacts、Sheets和Docs等服务。当安装了`gws`后，该智能体将使用它作为执行后端以实现更广泛的Google Workspace功能覆盖；否则则回退到内置的Python客户端实现。

## 参考资料

- `references/gmail-search-syntax.md` — Gmail搜索操作符（如is:unread、from:、newer_than:等）
- `references/daily-brief.md` — 每日/晨间简报流程：日程安排、冲突检测、会议准备以及来自Gmail和Calendar的紧急邮件处理。当用户请求晨间简报、会议准备或查询“我的日程有哪些？有哪些邮件需要处理？”时即可加载该文档。

## 脚本

- `scripts/setup.py` — OAuth2配置文件（只需运行一次即可完成授权）
- `scripts/google_api.py` — 兼容性封装CLI。在条件允许的情况下，它会优先使用`gws`来执行操作，同时保持与Hermes现有的JSON输出格式一致。

## 首次设置

整个设置过程完全无需交互——您可以一步步引导设置，使其能够在CLI、Telegram、Discord或任何其他平台上正常运行。

首先定义一个快捷指令：

```bash
GSETUP="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/setup.py"
```

### 第0步：检查是否已完成配置

```bash
$GSETUP --check
```

如果输出 `AUTHENTICATED`，则可直接跳至“使用方法”——设置已完成。

### 第一步：需求评估——询问用户的需求

在开始 OAuth 设置之前，需向用户提出两个问题：

**问题 1：“您需要哪些 Google 服务？仅电子邮件，还是还需要日历/云端硬盘/表格/文档？”**

- **仅电子邮件** → 他们完全不需要此功能。建议使用 `himalaya` 功能——它可使用 Gmail 应用密码（设置 → 安全性 → 应用密码）进行配置，设置时间仅需2分钟，且无需 Google Cloud 项目。请加载 `himalaya` 功能并按照其说明进行设置。

- **电子邮件 + 日历** → 可继续使用当前功能，但在认证时需使用 `--services email,calendar` 参数，这样同意界面只会显示他们实际需要的权限范围。

- **仅日历/云端硬盘/表格/文档** → 仍可使用当前功能，但需指定更具体的 `--services` 参数，如 `calendar,drive,sheets,docs`。

- **需要完整工作区访问权限** → 仍可使用当前功能，直接使用默认的 `all` 权限集合。

**问题 2：“您的 Google 账户是否使用了高级保护功能（登录时需硬件安全密钥）？如果您不确定，那很可能没有——因为这是需要您主动启用的功能。”**

- **否/不确定** → 按常规流程设置即可，继续下一步。
- **是** → 在执行第4步之前，其工作区管理员必须将 OAuth 客户端 ID 添加到组织的允许应用列表中。请提前告知用户这一点。

### 第二步：创建 OAuth 凭证（仅需一次，约5分钟）

告知用户：

> 您需要一个 Google Cloud OAuth 客户端。此操作只需设置一次即可：
>
> 1. 创建或选择一个项目：
>    https://console.cloud.google.com/projectselector2/home/dashboard
> 2. 在 API 库中启用所需的 API：
>    https://console.cloud.google.com/apis/library
>    需要启用的 API 包括：Gmail API、Google Calendar API、Google Drive API、
>    Google Sheets API、Google Docs API 以及 People API。
> 3. 在此处创建 OAuth 客户端：
>    https://console.cloud.google.com/apis/credentials
>    选择“Credentials”→“Create Credentials”→“OAuth 2.0 Client ID”。
> 4. 应用类型选择“Desktop app”，然后点击“Create”。
> 5. 如果该应用仍处于测试阶段，请在此处将用户的 Google 账户添加为测试用户：
>    https://console.cloud.google.com/auth/audience
>    选择“Audience”→“Test users”→“Add users”。
> 6. 下载 JSON 文件，并告知我该文件的路径。
>
> 关于 Hermes CLI 的重要提示：如果文件路径以 `/` 开头，请勿仅将纯路径作为单独的消息发送到 CLI 中，因为这可能会被误认为是斜杠命令。应将其放在句子中一并发送，例如：
> `The JSON file path is: ~/Downloads/client_secret_....json`
>
> 一旦他们提供了路径：

```bash
$GSETUP --client-secret /path/to/client_secret.json
```

如果他们粘贴的是原始的客户端 ID/客户端密钥值而非文件路径，你需要为他们手动创建一个有效的桌面端 OAuth JSON 文件，并将其保存在明确指定的位置（例如 `~/Downloads/hermes-google-client-secret.json`），之后再使用 `--client-secret` 参数指定该文件来运行命令。

### 第 3 步：获取授权 URL

使用第 1 步中选择的服务集。示例：

```bash
$GSETUP --auth-url --services email,calendar --format json
$GSETUP --auth-url --services calendar,drive,sheets,docs --format json
$GSETUP --auth-url --services all --format json
```

该操作会返回一个包含 `auth_url` 字段的 JSON 数据，同时会将该完整 URL 保存至 `~/.hermes/google_oauth_last_url.txt` 文件中。

此步骤的代理规则如下：
- 提取 `auth_url` 字段，并以单行形式将该完整 URL 发送给用户。
- 告知用户在授权通过后，浏览器在访问 `http://localhost:1` 时很可能会失败，这是正常现象。
- 要求用户从浏览器地址栏复制整个重定向后的 URL。
- 如果用户遇到 `Error 403: access_denied` 错误，请直接引导其访问 `https://console.cloud.google.com/auth/audience`，自行添加为测试用户。

### 第 4 步：交换验证码

用户可以粘贴类似 `http://localhost:1/?code=4/0A...&scope=...` 的 URL，也可以仅粘贴验证码字符串，两种方式均可。`--auth-url` 步骤会在本地存储临时的待处理 OAuth 会话，这样即便在无头系统中，`--auth-code` 步骤也能随后完成 PKCE 验证码交换流程：

```bash
$GSETUP --auth-code "THE_URL_OR_CODE_THE_USER_PASTED" --format json
```

如果由于验证码已过期、已被使用，或是来自旧版本的浏览器标签页，导致使用 `--auth-code` 参数失败，系统现在会返回一个全新的 `fresh_auth_url`。此时应立即将新的网址发送给用户，要求他们仅通过最新的浏览器重定向功能进行尝试。

### 第 5 步：验证

```bash
$GSETUP --check
```

应输出 `AUTHENTICATED`。设置已完成——从现在起令牌将自动刷新。

### 备注

- 令牌存储在 `~/.hermes/google_token.json` 中，并会自动刷新。
- 待处理的 OAuth 会话状态/验证信息会暂时保存在 `~/.hermes/google_oauth_pending.json` 中，直至交换完成。
- 若已安装 `gws`，`google_api.py` 会指向同一个 `~/.hermes/google_token.json` 凭证文件。用户无需再执行单独的 `gws auth login` 操作。
- 如需撤销授权：` $GSETUP --revoke`

## 使用方法

所有命令均通过 API 脚本处理。可将 `GAPI` 设置为简写形式：

```bash
GAPI="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/google_api.py"
```

### Gmail

```bash
# Search (returns JSON array with id, from, subject, date, snippet)
$GAPI gmail search "is:unread" --max 10
$GAPI gmail search "from:boss@company.com newer_than:1d"
$GAPI gmail search "has:attachment filename:pdf newer_than:7d"

# Read full message (returns JSON with body text)
$GAPI gmail get MESSAGE_ID

# Send
$GAPI gmail send --to user@example.com --subject "Hello" --body "Message text"
$GAPI gmail send --to user@example.com --subject "Report" --body "<h1>Q4</h1><p>Details...</p>" --html
$GAPI gmail send --to user@example.com --subject "Hello" --from '"Research Agent" <user@example.com>' --body "Message text"

# Reply (automatically threads and sets In-Reply-To)
$GAPI gmail reply MESSAGE_ID --body "Thanks, that works for me."
$GAPI gmail reply MESSAGE_ID --from '"Support Bot" <user@example.com>' --body "Thanks"

# Labels
$GAPI gmail labels
$GAPI gmail modify MESSAGE_ID --add-labels LABEL_ID
$GAPI gmail modify MESSAGE_ID --remove-labels UNREAD
```

### 日历功能

```bash
# List events (defaults to next 7 days)
$GAPI calendar list
$GAPI calendar list --start 2026-03-01T00:00:00Z --end 2026-03-07T23:59:59Z

# Create event (ISO 8601 with timezone required)
$GAPI calendar create --summary "Team Standup" --start 2026-03-01T10:00:00-06:00 --end 2026-03-01T10:30:00-06:00
$GAPI calendar create --summary "Lunch" --start 2026-03-01T12:00:00Z --end 2026-03-01T13:00:00Z --location "Cafe"
$GAPI calendar create --summary "Review" --start 2026-03-01T14:00:00Z --end 2026-03-01T15:00:00Z --attendees "alice@co.com,bob@co.com"

# Delete event
$GAPI calendar delete EVENT_ID
```

### 驱动功能

```bash
# Search existing files
$GAPI drive search "quarterly report" --max 10
$GAPI drive search "mimeType='application/pdf'" --raw-query --max 5

# Get metadata for a single file
$GAPI drive get FILE_ID

# Upload a local file (auto-detects MIME type)
$GAPI drive upload /path/to/report.pdf
$GAPI drive upload /path/to/image.png --name "Logo.png" --parent FOLDER_ID

# Download (binary files download as-is; Google-native files export to a
# sensible default — Docs→pdf, Sheets→csv, Slides→pdf, Drawings→png)
$GAPI drive download FILE_ID
$GAPI drive download DOC_ID --output ~/doc.pdf
$GAPI drive download DOC_ID --export-mime text/plain --output ~/doc.txt

# Create a folder
$GAPI drive create-folder "Reports"
$GAPI drive create-folder "Q4" --parent FOLDER_ID

# Share
$GAPI drive share FILE_ID --email alice@example.com --role reader
$GAPI drive share FILE_ID --email alice@example.com --role writer --notify
$GAPI drive share FILE_ID --type anyone --role reader        # anyone with link
$GAPI drive share FILE_ID --type domain --domain example.com --role reader

# Delete — defaults to trash (reversible). Use --permanent to skip the trash.
$GAPI drive delete FILE_ID
$GAPI drive delete FILE_ID --permanent
```

### 联系方式

```bash
$GAPI contacts list --max 20
```

### 表格功能

```bash
# Create a new spreadsheet
$GAPI sheets create --title "Q4 Budget"
$GAPI sheets create --title "Inventory" --sheet-name "Stock"

# Read
$GAPI sheets get SHEET_ID "Sheet1!A1:D10"

# Write
$GAPI sheets update SHEET_ID "Sheet1!A1:B2" --values '[["Name","Score"],["Alice","95"]]'

# Append rows
$GAPI sheets append SHEET_ID "Sheet1!A:C" --values '[["new","row","data"]]'
```

### 文档资料

```bash
# Read
$GAPI docs get DOC_ID

# Create a new Doc (optionally seeded with body text)
$GAPI docs create --title "Meeting Notes"
$GAPI docs create --title "Draft" --body "First paragraph..."

# Append text to the end of an existing Doc
$GAPI docs append DOC_ID --text "Additional content to append"
```

## 输出格式

所有命令均返回 JSON 格式的数据。您可以使用 `jq` 工具进行解析，或直接读取该数据。主要字段如下：

- **Gmail 搜索**：`[{id, threadId, from, to, subject, date, snippet, labels}]`
- **Gmail 获取邮件**： `{id, threadId, from, to, subject, date, labels, body}`
- **Gmail 发送/回复邮件**： `{status: "sent", id, threadId}`
- **日历列表**： `[{id, summary, start, end, location, description, htmlLink}]`
- **创建日历**： `{status: "created", id, summary, htmlLink}`
- **Drive 搜索**： `[{id, name, mimeType, modifiedTime, webViewLink}]`
- **Drive 获取文件信息**： `{id, name, mimeType, modifiedTime, size, webViewLink, parents, owners}`
- **Drive 上传文件**： `{status: "uploaded", id, name, mimeType, webViewLink}`
- **Drive 下载文件**： `{status: "downloaded", id, name, path, mimeType}`
- **Drive 创建文件夹**： `{status: "created", id, name, webViewLink}`
- **Drive 共享文件**： `{status: "shared", permissionId, fileId, role, type}`
- **Drive 删除文件**： `{status: "trashed" | "deleted", fileId, permanent}`
- **联系人列表**： `[{name, emails: [...], phones: [...]}]`
- **Sheets 获取单元格数据**： `[[cell, cell, ...], ...]`
- **创建表格**： `{status: "created", spreadsheetId, title, spreadsheetUrl}`
- **创建文档**： `{status: "created", documentId, title, url}`
- **向文档追加内容**： `{status: "appended", documentId, inserted_at, characters}`

## 规则

1. **在未先获得用户确认之前，绝不可发送邮件、创建/删除日历事件、删除 Drive 文件、共享文件或修改 Docs/Sheets 文档。** 应先展示即将执行的操作内容（收件人、文件 ID、内容及共享权限），并征得用户批准。对于 `drive delete` 操作，建议优先使用默认的回收站处理方式（可恢复），而非 `--permanent` 选项。

2. **首次使用时请检查认证状态** — 运行 `setup.py --check` 命令。若检测失败，需指导用户完成相关设置。

3. **对于复杂的查询需求，请参考 Gmail 搜索语法指南** — 可通过 `skill_view("google-workspace", file_path="references/gmail-search-syntax.md")` 来加载该指南。

4. **日历时间必须标注时区** — 始终使用包含时区偏移的 ISO 8601 格式（例如 `2026-03-01T10:00:00-06:00`）或 UTC 格式（标记为 `Z`）。

5. **请遵守速率限制** — 避免频繁连续调用 API。尽可能采用批量读取的方式。

## 故障排除

| 问题 | 解决方案 |
|---------|----------|
| `NOT_AUTHENTICATED` | 执行上述第2至5步的设置流程 |
| `REFRESH_FAILED` | Token已被撤销或过期——请重新执行第3至5步 |
| `HttpError 403: Insufficient Permission` | 缺少API权限范围——先运行` $GSETUP --revoke`，再重新执行第3至5步 |
| `AUTHENTICATED (partial)` 或 “Token missing scopes” | 若需使用新的写入功能（如Drive的写入/删除、Docs的创建/编辑），需要重新进行授权。请先运行` $GSETUP --revoke`，再重新执行第3至5步以获取升级后的权限范围 |
| `HttpError 403: Access Not Configured` | API尚未启用——用户需在Google Cloud Console中开启该API |
| `ModuleNotFoundError` | 运行` $GSETUP --install-deps`命令 |
| 高级保护机制阻止了授权 | 工作空间管理员必须将相应的OAuth客户端ID加入允许列表 |

## 撤销访问权限

```bash
$GSETUP --revoke
```
