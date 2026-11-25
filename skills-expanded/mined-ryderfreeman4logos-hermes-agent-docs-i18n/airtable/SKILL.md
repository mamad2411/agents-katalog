---
name: airtable
description: Airtable REST API via curl. Records CRUD, filters, upserts.
version: 1.1.0
author: community
license: MIT
platforms: [linux, macos, windows]
prerequisites:
  env_vars: [AIRTABLE_API_KEY]
  commands: [curl]
metadata:
  hermes:
    tags: [Airtable, Productivity, Database, API]
    homepage: https://airtable.com/developers/web/api/introduction
---

# Airtable — 基础库、表格与记录

您可以使用 `terminal` 工具配合 `curl` 直接调用 Airtable 的 REST API。无需 MCP 服务器、OAuth 流程或 Python SDK，仅需 `curl` 以及个人访问令牌即可。

## 先决条件

1. 在 https://airtable.com/create/tokens 创建一个**个人访问令牌（PAT）**（此类令牌以 `pat...` 开头）。
2. 至少授予以下权限范围：
   - `data.records:read` — 读取行数据
   - `data.records:write` — 创建/更新/删除行数据
   - `schema.bases:read` — 列出基础库与表格
3. **重要提示：** 在同一令牌设置界面中，将您需要访问的每个基础库添加到令牌的**访问权限**列表中。个人访问令牌的权限是针对特定基础库设置的——在错误的基础库上使用的有效令牌将会返回 `403` 错误。
4. 将该令牌存储在 `${HERMES_HOME:-~/.hermes}/.env` 文件中（或通过 `hermes setup` 命令设置）。
   ```
   AIRTABLE_API_KEY=pat_your_token_here
   ```

> 注意：旧版的 `key...` API 密钥已于 2024 年 2 月被弃用。目前仅支持 PAT 和 OAuth 令牌。

## API 基础知识

- **端点地址：** `https://api.airtable.com/v0`
- **认证标头：** `Authorization: Bearer $AIRTABLE_API_KEY`
- **所有请求**均采用 JSON 格式（POST/PATCH/PUT 请求的正文需设置 `Content-Type: application/json`）。
- **对象标识符规则：** 数据库标识为 `app...`，表格标识为 `tbl...`，记录标识为 `rec...`，字段标识为 `fld...`。这些标识符永不更改，但名称可以变更。在自动化脚本中建议优先使用标识符。
- **速率限制：** 每个数据库每秒最多 5 次请求。若收到 `429` 错误码，需暂缓请求；单个数据库的突发请求量也会受到限制。

数据库的 curl 请求格式：
```bash
curl -s "https://api.airtable.com/v0/$BASE_ID/$TABLE?maxRecords=5" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python -m json.tool
```

`-s` 选项可隐藏 curl 的进度条——请在每次调用时都保留该选项，以确保 Hermes 能获得整洁的工具输出。如需生成易读的 JSON 格式，可通过 `python -m json.tool`（始终可用）或 `jq`（如已安装）进行转换。

## 字段类型（请求体格式）

| 字段类型 | 写入格式 |
|---|---|
| 单行文本 | `"Name": "hello"` |
| 长文本 | `"Notes": "multi\nline"` |
| 数字 | `"Score": 42` |
| 复选框 | `"Done": true` |
| 单选选项 | `"Status": "Todo"`（除非设置了 `typecast: true`，否则该选项名称必须已存在） |
| 多选选项 | `"Tags": ["urgent", "bug"]` |
| 日期 | `"Due": "2026-04-01"` |
| 时间戳（UTC） | `"At": "2026-04-01T14:30:00.000Z"` |
| URL / 邮箱 / 电话号码 | `"Link": "https://…"` |
| 附件 | `"Files": [{"url": "https://…"}]`（由 Airtable 自动获取并重新托管） |
| 关联记录 | `"Owner": ["recXXXXXXXXXXXXXX"]`（记录 ID 的数组形式） |
| 用户 | `"AssignedTo": {"id": "usrXXXXXXXXXXXXXX"}` |

在创建/更新请求体的最顶层添加 `"typecast": true`，即可让 Airtable 自动转换数值类型（例如即时创建新的单选选项，或将 `"42"` 转换为数字 `42`）。

## 常用查询

### 列出当前令牌可访问的数据库
```bash
curl -s "https://api.airtable.com/v0/meta/bases" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python -m json.tool
```

### 查看某个数据库的表列表及结构信息
```bash
curl -s "https://api.airtable.com/v0/meta/bases/$BASE_ID/tables" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python -m json.tool
```
在执行数据修改操作之前，请先使用此功能——它可确认确切的字段名称与编号，针对可选字段显示 `options.choices` 列表，并标明主键字段的名称。

### 列出记录（前10条）
```bash
curl -s "https://api.airtable.com/v0/$BASE_ID/$TABLE?maxRecords=10" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python -m json.tool
```

### 获取单条记录
```bash
curl -s "https://api.airtable.com/v0/$BASE_ID/$TABLE/$RECORD_ID" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python -m json.tool
```

### 过滤记录（filterByFormula）
Airtable 公式必须进行 URL 编码。建议使用 Python 标准库来完成该操作，切勿手动编码：
```bash
FORMULA="{Status}='Todo'"
ENC=$(python -c 'import sys, urllib.parse; print(urllib.parse.quote(sys.argv[1], safe=""))' "$FORMULA")
curl -s "https://api.airtable.com/v0/$BASE_ID/$TABLE?filterByFormula=$ENC&maxRecords=20" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python -m json.tool
```

常用的公式模式：
- 精确匹配：`{Email}='user@example.com'`
- 包含内容：`FIND('bug', LOWER({Title}))`
- 多个条件：`AND({Status}='Todo', {Priority}='High')`
- 或关系：`OR({Owner}='alice', {Owner}='bob')`
- 非空值：`NOT({Assignee}='')`
- 日期比较：`IS_AFTER({Due}, TODAY())`

### 排序并选择特定字段
```bash
curl -s "https://api.airtable.com/v0/$BASE_ID/$TABLE?sort%5B0%5D%5Bfield%5D=Priority&sort%5B0%5D%5Bdirection%5D=asc&fields%5B%5D=Name&fields%5B%5D=Status" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python -m json.tool
```
查询参数中的方括号必须进行 URL 编码（即使用 `%5B` / `%5D`）。 

### 使用命名视图
```bash
curl -s "https://api.airtable.com/v0/$BASE_ID/$TABLE?view=Grid%20view&maxRecords=50" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python -m json.tool
```
视图会在服务器端应用其保存的筛选条件与排序规则。

## 常见操作

### 创建记录
```bash
curl -s -X POST "https://api.airtable.com/v0/$BASE_ID/$TABLE" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"fields":{"Name":"New task","Status":"Todo","Priority":"High"}}' | python -m json.tool
```

### 单次调用最多可创建10条记录
```bash
curl -s -X POST "https://api.airtable.com/v0/$BASE_ID/$TABLE" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "typecast": true,
    "records": [
      {"fields": {"Name": "Task A", "Status": "Todo"}},
      {"fields": {"Name": "Task B", "Status": "In progress"}}
    ]
  }' | python -m json.tool
```
批量接口的每次请求最多处理 **10 条记录**。对于需要插入更多数据的情况，建议以每批10条的形式分次处理，并加入短暂的延迟，以此遵守每秒5次请求的限制。

### 更新记录（PATCH操作——合并数据并保留未更改的字段）
```bash
curl -s -X PATCH "https://api.airtable.com/v0/$BASE_ID/$TABLE/$RECORD_ID" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"fields":{"Status":"Done"}}' | python -m json.tool
```

### 通过合并字段进行插入或更新（无需提供 ID）
```bash
curl -s -X PATCH "https://api.airtable.com/v0/$BASE_ID/$TABLE" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "performUpsert": {"fieldsToMergeOn": ["Email"]},
    "records": [
      {"fields": {"Email": "user@example.com", "Status": "Active"}}
    ]
  }' | python -m json.tool
```
`performUpsert` 用于创建合并字段值为空的新记录，同时更新那些合并字段值已存在的记录。非常适合实现幂等同步。

### 删除记录
```bash
curl -s -X DELETE "https://api.airtable.com/v0/$BASE_ID/$TABLE/$RECORD_ID" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python -m json.tool
```

### 单次调用可删除最多10条记录
```bash
curl -s -X DELETE "https://api.airtable.com/v0/$BASE_ID/$TABLE?records%5B%5D=rec1&records%5B%5D=rec2" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python -m json.tool
```

## 分页功能

列表接口每次最多返回**每页100条记录**。如果响应中包含 `"offset": "..."` 字段，需在后续请求中将其传递继续查询。重复此过程，直至该字段不再出现为止：

```bash
OFFSET=""
while :; do
  URL="https://api.airtable.com/v0/$BASE_ID/$TABLE?pageSize=100"
  [ -n "$OFFSET" ] && URL="$URL&offset=$OFFSET"
  RESP=$(curl -s "$URL" -H "Authorization: Bearer $AIRTABLE_API_KEY")
  echo "$RESP" | python -c 'import json,sys; d=json.load(sys.stdin); [print(r["id"], r["fields"].get("Name","")) for r in d["records"]]'
  OFFSET=$(echo "$RESP" | python -c 'import json,sys; d=json.load(sys.stdin); print(d.get("offset",""))')
  [ -z "$OFFSET" ] && break
done
```

## Hermes 的典型工作流程

1. **确认身份认证。** 使用以下命令执行请求：`curl -s -o /dev/null -w "%{http_code}\n" https://api.airtable.com/v0/meta/bases -H "Authorization: Bearer $AIRTABLE_API_KEY"`，预期返回状态码为 `200`。
2. **定位数据库。** 可通过上一步列出所有数据库，或者如果令牌中未包含 `schema.bases:read` 权限，则直接让用户提供 `app...` ID。
3. **检查数据结构。** 发送请求 `GET /v0/meta/bases/$BASE_ID/tables`，在修改任何数据之前，将具体的字段名及主键名称缓存到会话中。
4. **先读取再写入。** 对于“根据条件 Y 更新 X”的操作，应先使用 `filterByFormula` 查找对应的 `rec...` ID，然后再执行 `PATCH /v0/$BASE_ID/$TABLE/$RECORD_ID` 操作。切勿猜测记录 ID。
5. **批量写入。** 将多个相关的创建操作合并为一次最多包含 10 条记录的 POST 请求，以避免超出每秒 5 次请求的限制。
6. **不可逆的操作。** 通过 API 无法撤销删除操作。如果用户要求“删除所有 X”，应先反馈筛选条件及记录数量，并在确认后才会执行删除操作。

## 常见陷阱

- **`filterByFormula` 必须进行 URL 编码。** 包含空格或非 ASCII 字符的字段名同样需要编码（例如 `{My Field}` 应转换为 `%7BMy%20Field%7D`）。请使用 Python 标准库中的相关功能进行编码，切勿手动处理编码事宜。
- **响应中会省略空值字段。** 若缺少 `"Assignee"` 键，并不意味着该字段不存在，而只是表示该记录对应的值为空。在判定某个字段缺失之前，请先查看数据结构定义（第 3 步）。
- **PATCH 与 PUT 的区别。** `PATCH` 操作会将提供的字段合并到现有记录中；而 `PUT` 则会完全替换该记录，并清除所有未包含的字段。默认操作方式为 `PATCH`。
- **单选选项必须是已定义的。** 如果字段的选项列表中不存在 “Shipping” 这一选项，却仍写入 `"Status": "Shipping"`，将会触发 `INVALID_MULTIPLE_CHOICE_OPTIONS` 错误；除非设置 `"typecast": true`（该参数会自动创建该选项）。
- **令牌的作用范围以基础表为单位。** 如果某个基础表返回 403 错误，而另一个基础表可以正常使用，那说明该令牌的访问权限列表中未包含前者，并非作用范围或认证问题。此时可引导用户前往 https://airtable.com/create/tokens 为该令牌添加相应权限。
- **速率限制是针对每个基础表，而非每个令牌。** `baseA` 每秒允许 5 次请求，`baseB` 同样每秒允许 5 次请求，这种情况是正常的；但仅 `baseA` 每秒超过 6 次请求就会触发限流。遇到 429 错误时，请查看 `Retry-After` 请求头以了解下次可尝试的时间。

## Hermes 的重要注意事项

- **始终请结合 `curl` 一起使用 `terminal` 工具**。切勿使用 `web_extract`（它无法发送认证头），也避免使用 `browser_navigate`（需要用户界面认证且速度较慢）。  
- 当加载此技能时，`AIRTABLE_API_KEY` 会自动从 `${HERMES_HOME:-~/.hermes}/.env` 中传递给子进程——无需在每次执行 `curl` 命令前重新导出该密钥。  
- **在公式中处理花括号时需格外谨慎**。在 heredoc 内容中，`{Status}` 为字面值；而在 shell 参数中，只要不在 `{...}` 的扩展上下文中，`{Status}` 即可安全使用——但在将其拼接进 URL 之前，应先通过 `python urllib.parse.quote` 对动态字符串进行转义处理。  
- **推荐使用 `python -m json.tool` 进行格式化输出**（该工具始终可用），而非可选的 `jq`。仅当需要过滤或提取特定字段时才使用 `jq`。  
- **分页是针对单页数据的，而非全局范围**。Airtable 对每页数据的限制为 100 条记录，此为硬性规定，无法更改。需通过 `offset` 参数循环查询，直至目标字段不再出现为止。  
- **对于非 2xx 状态码的响应，请查看 `errors` 数组**——Airtable 会返回结构化的错误代码，如 `AUTHENTICATION_REQUIRED`、`INVALID_PERMISSIONS`、`MODEL_ID_NOT_FOUND`、`INVALID_MULTIPLE_CHOICE_OPTIONS` 等，这些代码能明确指示问题所在。
