---
name: siyuan
description: Query and edit a SiYuan knowledge base via its API.
version: 1.0.0
author: FEUAZUR
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [SiYuan, Notes, Knowledge Base, PKM, API]
    related_skills: [obsidian, notion]
    homepage: https://github.com/siyuan-note/siyuan
prerequisites:
  env_vars: [SIYUAN_TOKEN]
  commands: [curl, jq]
required_environment_variables:
  - name: SIYUAN_TOKEN
    prompt: SiYuan API token
    help: "Settings > About in SiYuan desktop app"
  - name: SIYUAN_URL
    prompt: SiYuan instance URL (default http://127.0.0.1:6806)
    required_for: remote instances
---

# SiYuan Note API

您可以通过 curl 调用 [SiYuan](https://github.com/siyuan-note/siyuan) 内核 API，对自托管知识库中的块和文档进行搜索、读取、创建、更新及删除操作。无需任何额外工具，只需拥有 curl 工具和 API 令牌即可。

## 前提条件

1. 安装并运行 SiYuan（桌面版或 Docker 版）
2. 获取您的 API 令牌：**设置 > 关于 > API 令牌**
3. 将该令牌保存在 `${HERMES_HOME:-~/.hermes}/.env` 文件中：
   ```
   SIYUAN_TOKEN=your_token_here
   SIYUAN_URL=http://127.0.0.1:6806
   ```
如果未进行设置，`SIYUAN_URL` 的默认值为 `http://127.0.0.1:6806`。

## API 基础知识

所有 SiYuan API 调用均采用 **带 JSON 数据体的 POST 请求**。每个请求都遵循以下格式：

```bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/..." \
  -H "Authorization: Token $SIYUAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"param": "value"}'
```

响应内容为结构如下的 JSON 格式：
```json
{"code": 0, "msg": "", "data": { ... }}
```
`code: 0` 表示操作成功。其他任何值均代表错误——请查看 `msg` 字段以获取详细信息。

**ID 格式：** SiYuan ID 的格式为 `20210808180117-6v0mkxr`（14位时间戳 + 7位字母数字组合）。

## 快速参考

| 操作 | 接口地址 |
|------|----------|
| 全文搜索 | `/api/search/fullTextSearchBlock` |
| SQL 查询 | `/api/query/sql` |
| 读取块内容 | `/api/block/getBlockKramdown` |
| 读取子块 | `/api/block/getChildBlocks` |
| 获取路径 | `/api/filetree/getHPathByID` |
| 获取属性 | `/api/attr/getBlockAttrs` |
| 列出笔记本 | `/api/notebook/lsNotebooks` |
| 列出文档 | `/api/filetree/listDocsByPath` |
| 创建笔记本 | `/api/notebook/createNotebook` |
| 创建文档 | `/api/filetree/createDocWithMd` |
| 追加块内容 | `/api/block/appendBlock` |
| 更新块内容 | `/api/block/updateBlock` |
| 重命名文档 | `/api/filetree/renameDocByID` |
| 设置属性 | `/api/attr/setBlockAttrs` |
| 删除块内容 | `/api/block/deleteBlock` |
| 删除文档 | `/api/filetree/removeDocByID` |
| 导出为 Markdown 格式 | `/api/export/exportMdContent` |

## 常见操作

### 搜索（全文）

```bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/search/fullTextSearchBlock" \
  -H "Authorization: Token $SIYUAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "meeting notes", "page": 0}' | jq '.data.blocks[:5]'
```

### 搜索（SQL）

直接查询区块数据库。仅 SELECT 语句是安全的。

```bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/query/sql" \
  -H "Authorization: Token $SIYUAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"stmt": "SELECT id, content, type, box FROM blocks WHERE content LIKE '\''%keyword%'\'' AND type='\''p'\'' LIMIT 20"}' | jq '.data'
```

常用字段包括：`id`、`parent_id`、`root_id`、`box`（笔记本编号）、`path`、`content`、`type`、`subtype`、`created`、`updated`。

### 读取块内容

以 Kramdown（类似 Markdown 的格式）返回块内容。

```bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/getBlockKramdown" \
  -H "Authorization: Token $SIYUAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"id": "20210808180117-6v0mkxr"}' | jq '.data.kramdown'
```

### 阅读子块内容

```bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/getChildBlocks" \
  -H "Authorization: Token $SIYUAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"id": "20210808180117-6v0mkxr"}' | jq '.data'
```

### 获取人类可读的路径

```bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/filetree/getHPathByID" \
  -H "Authorization: Token $SIYUAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"id": "20210808180117-6v0mkxr"}' | jq '.data'
```

### 获取块属性

```bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/attr/getBlockAttrs" \
  -H "Authorization: Token $SIYUAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"id": "20210808180117-6v0mkxr"}' | jq '.data'
```

### 列出笔记本

```bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/notebook/lsNotebooks" \
  -H "Authorization: Token $SIYUAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}' | jq '.data.notebooks[] | {id, name, closed}'
```

### 列出笔记本中的文档

```bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/filetree/listDocsByPath" \
  -H "Authorization: Token $SIYUAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"notebook": "NOTEBOOK_ID", "path": "/"}' | jq '.data.files[] | {id, name}'
```

### 创建文档

```bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/filetree/createDocWithMd" \
  -H "Authorization: Token $SIYUAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "notebook": "NOTEBOOK_ID",
    "path": "/Meeting Notes/2026-03-22",
    "markdown": "# Meeting Notes\n\n- Discussed project timeline\n- Assigned tasks"
  }' | jq '.data'
```

### 创建笔记本

```bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/notebook/createNotebook" \
  -H "Authorization: Token $SIYUAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "My New Notebook"}' | jq '.data.notebook.id'
```

### 向文档追加内容块

```bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/appendBlock" \
  -H "Authorization: Token $SIYUAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "parentID": "DOCUMENT_OR_BLOCK_ID",
    "data": "New paragraph added at the end.",
    "dataType": "markdown"
  }' | jq '.data'
```

此外，还提供以下接口：`/api/block/prependBlock`（参数相同，用于在块的开头插入内容）以及 `/api/block/insertBlock`（使用 `previousID` 而非 `parentID`，用于在指定块之后插入内容）。

### 更新块内容

```bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/updateBlock" \
  -H "Authorization: Token $SIYUAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "BLOCK_ID",
    "data": "Updated content here.",
    "dataType": "markdown"
  }' | jq '.data'
```

### 重命名文档

```bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/filetree/renameDocByID" \
  -H "Authorization: Token $SIYUAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"id": "DOCUMENT_ID", "title": "New Title"}'
```

### 设置块属性

自定义属性必须以 `custom-` 作为前缀：

```bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/attr/setBlockAttrs" \
  -H "Authorization: Token $SIYUAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "BLOCK_ID",
    "attrs": {
      "custom-status": "reviewed",
      "custom-priority": "high"
    }
  }'
```

### 删除块

```bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/deleteBlock" \
  -H "Authorization: Token $SIYUAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"id": "BLOCK_ID"}'
```

要删除整个文档：请使用 `/api/filetree/removeDocByID`，并传入参数 `{"id": "DOC_ID"}`。
要删除笔记本：请使用 `/api/notebook/removeNotebook`，并传入参数 `{"notebook": "NOTEBOOK_ID"}`。

### 将文档导出为 Markdown 格式

```bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/export/exportMdContent" \
  -H "Authorization: Token $SIYUAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"id": "DOCUMENT_ID"}' | jq -r '.data.content'
```

## 块类型

SQL 查询中常见的 `type` 值：

| 类型 | 描述 |
|------|-------------|
| `d` | 文档（根块） |
| `p` | 段落 |
| `h` | 标题 |
| `l` | 列表 |
| `i` | 列表项 |
| `c` | 代码块 |
| `m` | 数学公式块 |
| `t` | 表格 |
| `b` | 引用块 |
| `s` | 超级块 |
| `html` | HTML 块 |

## 常见陷阱

- **所有接口均为 POST 请求**——即使是只读操作也是如此。请勿使用 GET 请求。
- **SQL 安全性**：仅可使用 SELECT 查询。INSERT/UPDATE/DELETE/DROP 等操作存在风险，绝不可发送。
- **ID 格式验证**：ID 需符合 `YYYYMMDDHHmmss-xxxxxxx` 的格式，其他格式的 ID 均需被拒绝。
- **错误响应处理**：在处理 `data` 之前，务必先检查响应中的 `code != 0`。
- **大型文档**：块内容及导出结果可能体积巨大。建议在 SQL 查询中使用 `LIMIT` 限制数据量，并通过 `jq` 工具提取所需内容。
- **笔记本 ID**：在操作特定笔记本时，需先通过 `lsNotebooks` 获取其 ID。

## 替代方案：MCP 服务器

如果您更倾向于使用原生集成而非 curl，可以安装 SiYuan MCP 服务器：

```yaml
# In ~/.hermes/config.yaml under mcp_servers:
mcp_servers:
  siyuan:
    command: npx
    args: ["-y", "@porkll/siyuan-mcp"]
    env:
      SIYUAN_TOKEN: "your_token"
      SIYUAN_URL: "http://127.0.0.1:6806"
```
