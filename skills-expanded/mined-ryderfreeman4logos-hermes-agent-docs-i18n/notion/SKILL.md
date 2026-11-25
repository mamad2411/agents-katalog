---
name: notion
description: "Notion API + ntn CLI: pages, databases, markdown, Workers."
version: 2.0.0
author: community
license: MIT
platforms: [linux, macos, windows]
prerequisites:
  env_vars: [NOTION_API_KEY]
metadata:
  hermes:
    tags: [Notion, Productivity, Notes, Database, API, CLI, Workers]
    homepage: https://developers.notion.com
---

# Notion

可通过两种方式与 Notion 进行交互。两种方式均使用相同的集成令牌——请根据实际可用情况选择。

◆ **`ntn` CLI** — Notion 官方命令行工具。语法更为简洁，支持单行文件上传，是 Workers 功能的必备工具。截至 2026 年 5 月仅支持 macOS 和 Linux 系统（Windows 支持功能“即将推出”）。**安装时默认选用此方式。**
◆ **HTTP + curl** — 在所有系统上均可使用，包括 Windows。当未安装 `ntn` 时，**会自动回退至此默认方式。**

## 设置

### 1. 获取集成令牌（两种方式均需）

1. 访问 https://notion.so/my-integrations 创建一个集成账户
2. 复制 API 密钥（以 `ntn_` 或 `secret_` 开头）
3. 将其存储在 `${HERMES_HOME:-~/.hermes}/.env` 文件中：
   ```
   NOTION_API_KEY=ntn_your_key_here
   ```
4. 在 Notion 中与集成服务**共享目标页面/数据库**：进入页面菜单，选择“...”→“连接至”→对应的集成服务名称。若未执行此操作，即使页面确实存在，API 也会返回 404 错误。

### 2. 安装 `ntn`（macOS/Linux 系统的推荐安装路径）

```bash
# Recommended
curl -fsSL https://ntn.dev | bash

# Or via npm (needs Node 22+, npm 10+)
npm install --global ntn

ntn --version    # verify
```

**无需执行 `ntn login` 操作——可直接使用集成令牌。** 该方式支持无界面运行，无需浏览器即可使用。
```bash
export NOTION_API_TOKEN=$NOTION_API_KEY      # ntn reads NOTION_API_TOKEN
export NOTION_KEYRING=0                       # don't try to use the OS keychain
```

请将这些导出内容添加到您的 shell 配置文件中（或 `${HERMES_HOME:-~/.hermes}/.env` 文件中），这样每个会话都能自动继承这些设置。

### 3. 运行时选择路径

```bash
if command -v ntn >/dev/null 2>&1; then
  # use ntn
else
  # fall back to curl
fi
```

Windows 用户：在原生 `ntn` 版本发布之前，请完全跳过第 2 步——路径 B 即可正常使用。如果您希望立即获得更便捷的 CLI 体验，可在 WSL2 环境中安装 `ntn`。

## API 基础知识

所有 HTTP 请求都必须包含 `Notion-Version: 2025-09-03` 这一字段，`ntn` 会自动处理此项设置。在此版本中，用户所称的“数据库”在 API 中被称作**数据源**。

## 路径 A — `ntn` CLI（推荐，适用于 macOS / Linux）

### 原始 API 调用（即 curl 的简写形式）
```bash
ntn api v1/users                                  # GET
ntn api v1/pages parent[page_id]=abc123 \         # POST with inline body
  properties[title][0][text][content]="Notes"
ntn api v1/pages/abc123 -X PATCH archived:=true   # PATCH; := is non-string (bool/num/null)
```

语法说明：  
- `key=value` — 字符串类型字段  
- `key[nested]=value` — 嵌套对象字段  
- `key:=value` — 类型化赋值（布尔值、数字、null、数组）  

### 搜索功能
```bash
ntn api v1/search query="page title"
```

### 查看页面元数据
```bash
ntn api v1/pages/{page_id}
```

### 以 Markdown 格式读取页面（适配智能体使用）
```bash
ntn api v1/pages/{page_id}/markdown
```

### 以块的形式读取页面内容
```bash
ntn api v1/blocks/{page_id}/children
```

### 从 Markdown 创建页面
```bash
ntn api v1/pages \
  parent[page_id]=xxx \
  properties[title][0][text][content]="Notes from meeting" \
  markdown="# Agenda

- Q3 roadmap
- Hiring"
```

### 使用 Markdown 修补页面内容
```bash
ntn api v1/pages/{page_id}/markdown -X PATCH \
  markdown="## Update

Shipped the prototype."
```

### 查询数据库（数据源）
```bash
ntn api v1/data_sources/{data_source_id}/query -X POST \
  filter[property]=Status filter[select][equals]=Active
```

对于包含排序、多个过滤条件或复合逻辑的复杂查询，可通过管道符传递 JSON 数据：
```bash
echo '{"filter": {"property": "Status", "select": {"equals": "Active"}}, "sorts": [{"property": "Date", "direction": "descending"}]}' | \
  ntn api v1/data_sources/{data_source_id}/query -X POST --json -
```

### 文件上传功能（一句话总结——CLI领域的重大突破）
```bash
ntn files create < photo.png
ntn files create --external-url https://example.com/photo.png
ntn files list
```

与三步HTTP流程（创建上传 → PUT字节数据 → 获取引用）相比。

### 有用的环境变量
| 变量 | 效果 |
|---|---|
| `NOTION_API_TOKEN` | 认证令牌（优先于钥匙串使用）——请将其设置为您的集成令牌 |
| `NOTION_KEYRING=0` | 使用位于`~/.config/notion/auth.json`中的基于文件的凭据，而非操作系统的钥匙串 |
| `NOTION_WORKSPACE_ID` | 跳过工作空间选择提示 |

## 方案B — HTTP + curl（跨平台，Windows默认方案）

所有请求均遵循以下模式：

```bash
curl -s -X GET "https://api.notion.com/v1/..." \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json"
```

在 Windows 系统上，Windows 10 及更高版本自带的 `curl` 工具可直接使用。PowerShell 用户则可以使用 `Invoke-RestMethod` 命令。
```bash
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "page title"}'
```

### 查看页面元数据
```bash
curl -s "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"
```

### 以 Markdown 格式读取页面（更适配智能体）

相比块级 JSON，该格式更易于输入至模型中。

```bash
curl -s "https://api.notion.com/v1/pages/{page_id}/markdown" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"
```

### 以块状格式读取页面内容（当需要结构化处理时）
```bash
curl -s "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"
```

### 从 Markdown 创建页面

`POST /v1/pages` 接受一个名为 `markdown` 的请求体参数。

```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"page_id": "xxx"},
    "properties": {"title": [{"text": {"content": "Notes from meeting"}}]},
    "markdown": "# Agenda\n\n- Q3 roadmap\n- Hiring\n\n## Decisions\n- Ship MVP Friday"
  }'
```

### 使用 Markdown 修补页面内容
```bash
curl -s -X PATCH "https://api.notion.com/v1/pages/{page_id}/markdown" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"markdown": "## Update\n\nShipped the prototype."}'
```

### 在数据库中创建页面（带类型属性）
```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "xxx"},
    "properties": {
      "Name": {"title": [{"text": {"content": "New Item"}}]},
      "Status": {"select": {"name": "Todo"}}
    }
  }'
```

### 查询数据库（数据源）
```bash
curl -s -X POST "https://api.notion.com/v1/data_sources/{data_source_id}/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"property": "Status", "select": {"equals": "Active"}},
    "sorts": [{"property": "Date", "direction": "descending"}]
  }'
```

### 创建数据库
```bash
curl -s -X POST "https://api.notion.com/v1/data_sources" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"page_id": "xxx"},
    "title": [{"text": {"content": "My Database"}}],
    "properties": {
      "Name": {"title": {}},
      "Status": {"select": {"options": [{"name": "Todo"}, {"name": "Done"}]}},
      "Date": {"date": {}}
    }
  }'
```

### 更新页面属性
```bash
curl -s -X PATCH "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"Status": {"select": {"name": "Done"}}}}'
```

### 向页面添加模块块
```bash
curl -s -X PATCH "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Hello from Hermes!"}}]}}
    ]
  }'
```

### 文件上传（三步流程）
```bash
# 1. Create upload
curl -s -X POST "https://api.notion.com/v1/file_uploads" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"filename": "photo.png", "content_type": "image/png"}'

# 2. PUT bytes to the upload_url returned above
curl -s -X PUT "{upload_url}" --data-binary @photo.png

# 3. Reference {file_upload_id} in a page/block payload
```

## 属性类型

数据库项常用的属性格式如下：

- **标题：** `{"title": [{"text": {"content": "..."}}]}`
- **富文本：** `{"rich_text": [{"text": {"content": "..."}}]}`
- **单选：** `{"select": {"name": "选项名"}}`
- **多选：** `{"multi_select": [{"name": "A"}, {"name": "B"}]}`
- **日期：** `{"date": {"start": "2026-01-15", "end": "2026-01-16"}}`
- **复选框：** `{"checkbox": true}`
- **数字：** `{"number": 42}`
- **URL：** `{"url": "https://..."}`
- **邮箱：** `{"email": "user@example.com"}`
- **关联关系：** `{"relation": [{"id": "page_id"}]}`

## API版本 2025-09-03 — 数据库与数据源的变更

- **数据库现已升级为数据源。** 建议使用 `/data_sources/` 接口进行查询和检索操作。
- **每个数据库包含两个标识符：** `database_id` 和 `data_source_id`。
  - 创建页面时使用 `database_id`：`parent: {"database_id": "..."}`
  - 执行查询时使用 `data_source_id`：`POST /v1/data_sources/{id}/query`
- 搜索结果中，数据库会以 `"object": "data_source"` 的形式呈现，并包含 `data_source_id` 字段。

## Notion Workers（高级功能，需使用 `ntn`）

Workers 是由 Notion 为你托管的 TypeScript 程序。一个 Worker 可以实现以下任意组合的功能：
- **同步功能**——按预定时间间隔（默认为30分钟）从外部 API 获取数据并导入 Notion 数据库。
- **工具功能**——作为可在 Notion 自定义 Agent 中调用的工具使用。
- **Webhook 功能**——接收来自外部服务（如 GitHub、Stripe 等）的 HTTP 事件，并在 Notion 中执行相应操作。

**计划/平台限制：**
- CLI 功能适用于所有套餐。**部署 Workers 需要 Business 或 Enterprise 套餐。**
- 截至2026年5月，`ntn` 仅支持 macOS/Linux 系统。Windows 用户需使用 WSL2 或等待原生支持的推出。
- 2026年8月11日前可免费使用；之后将按 Notion 积分计量收费。

### 最简 Worker 示例

```bash
ntn workers new my-worker      # scaffold
cd my-worker
# Edit src/index.ts
ntn workers deploy --name my-worker
```

`src/index.ts`：
```typescript
import { Worker } from "@notionhq/workers";

const worker = new Worker();
export default worker;

worker.tool("greet", {
  title: "Greet a User",
  description: "Returns a friendly greeting",
  inputSchema: { type: "object", properties: { name: { type: "string" } }, required: ["name"] },
  execute: async ({ name }) => `Hello, ${name}!`,
});
```

### Webhook 功能

```typescript
worker.webhook("onGithubPush", {
  title: "GitHub Push Handler",
  execute: async (events, { notion }) => {
    for (const event of events) {
      // event.body, event.rawBody (for signature verification), event.headers
      console.log("got delivery", event.deliveryId);
    }
  },
});
```

部署完成后，执行 `ntn workers webhooks list` 命令即可查看 Notion 生成的 URL。请将此 URL 视为敏感信息——除非您启用了签名验证，否则任何拥有该 URL 的人都能够发送事件。

### Worker 生命周期相关命令

```bash
ntn workers deploy
ntn workers list
ntn workers exec <capability-key> -d '{"name": "world"}'
ntn workers sync trigger <key>            # run a sync now
ntn workers sync pause <key>
ntn workers env set GITHUB_WEBHOOK_SECRET=...
ntn workers runs list                     # recent invocations
ntn workers runs logs <run-id>
ntn workers webhooks list
```

当需要构建 Worker 时，可使用 `ntn workers new` 命令生成项目模板，在 `src/index.ts` 文件中编写代码，通过 `ntn workers env set` 设置相关密钥，最后进行部署。Notion 的完整 API 文档可见于 https://developers.notion.com/workers。

## Notion 风格的 Markdown（用于 `/markdown` 接口）

在标准 CommonMark 的基础上增加了类似 XML 的标签，用于表示 Notion 特有的块结构。缩进请使用**制表符**。

**CommonMark 之外的块结构：**
```
<callout icon="🎯" color="blue_bg">
	Ship the MVP by **Friday**.
</callout>

<details color="gray">
<summary>Toggle title</summary>
	Children indented one tab
</details>

<columns>
	<column>Left side</column>
	<column>Right side</column>
</columns>

<table_of_contents color="gray"/>
```

**内联格式：**
- 提及内容：`<mention-user url="..."/>`、`<mention-page url="...">标题</mention-page>`、`<mention-date start="2026-05-15"/>`
- 下划线格式：`<span underline="true">文本</span>`
- 颜色格式：`<span color="blue">文本</span>`，或在第一行使用块级格式 `{color="blue"}`
- 数学公式：内联格式为 `$x^2$
