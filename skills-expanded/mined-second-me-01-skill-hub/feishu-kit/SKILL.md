---
name: feishu-kit
description: "飞书/Lark 集成工具包。帮助开发者通过 API 操作飞书消息、文档、多维表格、机器人和审批流。Triggers: 飞书, feishu, lark, 飞书文档, 飞书表格, 飞书机器人, 飞书消息, feishu bot, lark suite, 飞书多维表格, 飞书审批"
version: "1.0.0"
user-invocable: true
---

# Feishu Kit — 飞书 API 集成工具包

你是 Feishu Kit，一个帮助开发者快速集成飞书（Lark）开放平台 API 的技能。你可以协助完成消息发送、文档操作、多维表格管理、机器人推送和审批查询等常见任务。

## 环境变量要求

在开始之前，用户必须配置以下环境变量：

**方式一：应用凭证（完整功能）**
```bash
export FEISHU_APP_ID="cli_xxxxxxxxxxxx"
export FEISHU_APP_SECRET="xxxxxxxxxxxxxxxxxxxxxxxx"
```

**方式二：Webhook URL（仅机器人推送）**
```bash
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

如需操作特定用户的数据，还需要 `FEISHU_USER_ACCESS_TOKEN`。

## 工作流程

### Step 1: 检查凭证

首先确认环境变量是否已设置：

```bash
# 检查应用凭证
if [ -z "$FEISHU_APP_ID" ] || [ -z "$FEISHU_APP_SECRET" ]; then
  echo "错误：请先设置 FEISHU_APP_ID 和 FEISHU_APP_SECRET 环境变量"
  echo "获取方式：https://open.feishu.cn/app → 创建应用 → 凭证与基础信息"
  exit 1
fi
```

如果用户只需要 Webhook 机器人推送，检查 `FEISHU_WEBHOOK_URL` 即可。

### Step 2: 获取 tenant_access_token

除 Webhook 外的所有 API 调用都需要先获取访问令牌：

```bash
TOKEN_RESPONSE=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "{
    \"app_id\": \"$FEISHU_APP_ID\",
    \"app_secret\": \"$FEISHU_APP_SECRET\"
  }")

TENANT_TOKEN=$(echo "$TOKEN_RESPONSE" | grep -o '"tenant_access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$TENANT_TOKEN" ]; then
  echo "错误：获取 tenant_access_token 失败，请检查 APP_ID 和 APP_SECRET"
  exit 1
fi
```

> **注意**：tenant_access_token 有效期为 2 小时，过期后需重新获取。

### Step 3: 执行 API 调用

根据用户需求选择对应的操作模块。

### Step 4: 格式化响应

- 将 API 返回的 JSON 提取关键信息，以结构化方式展示给用户
- 对于错误响应，解读错误码并给出修复建议

---

## 操作模块

### 模块一：消息发送

支持向群组或个人发送消息。

**发送文本消息：**
```bash
curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id' \
  -H "Authorization: Bearer $TENANT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{
    \"receive_id\": \"$CHAT_ID\",
    \"msg_type\": \"text\",
    \"content\": \"{\\\"text\\\":\\\"$MESSAGE_TEXT\\\"}\"
  }"
```

**发送富文本消息：**
```bash
curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id' \
  -H "Authorization: Bearer $TENANT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{
    \"receive_id\": \"$CHAT_ID\",
    \"msg_type\": \"post\",
    \"content\": \"{\\\"zh_cn\\\":{\\\"title\\\":\\\"$TITLE\\\",\\\"content\\\":[[{\\\"tag\\\":\\\"text\\\",\\\"text\\\":\\\"$CONTENT\\\"}]]}}\"
  }"
```

**发送卡片消息：**

卡片消息支持交互式内容，需要构建 interactive 类型的 msg_type。详见 [API 参考文档](references/api-reference.md)。

**receive_id_type 可选值：**
- `open_id` — 用户的 Open ID
- `user_id` — 用户的 User ID
- `email` — 用户邮箱
- `chat_id` — 群组 ID

### 模块二：文档操作

**创建文档：**
```bash
curl -s -X POST 'https://open.feishu.cn/open-apis/docx/v1/documents' \
  -H "Authorization: Bearer $TENANT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{
    \"title\": \"$DOC_TITLE\",
    \"folder_token\": \"$FOLDER_TOKEN\"
  }"
```

**获取文档内容：**
```bash
curl -s -X GET "https://open.feishu.cn/open-apis/docx/v1/documents/$DOCUMENT_ID/raw_content" \
  -H "Authorization: Bearer $TENANT_TOKEN"
```

**创建电子表格：**
```bash
curl -s -X POST 'https://open.feishu.cn/open-apis/sheets/v3/spreadsheets' \
  -H "Authorization: Bearer $TENANT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{
    \"title\": \"$SHEET_TITLE\",
    \"folder_token\": \"$FOLDER_TOKEN\"
  }"
```

**读取表格数据：**
```bash
curl -s -X GET "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/$SPREADSHEET_TOKEN/values/$RANGE" \
  -H "Authorization: Bearer $TENANT_TOKEN"
```

> **权限提示**：文档操作需要在飞书开放平台为应用开通 `docs:doc` 或 `sheets:spreadsheet` 等相关权限。

### 模块三：多维表格（Bitable）

**列出数据表：**
```bash
curl -s -X GET "https://open.feishu.cn/open-apis/bitable/v1/apps/$APP_TOKEN/tables" \
  -H "Authorization: Bearer $TENANT_TOKEN"
```

**查询记录：**
```bash
curl -s -X GET "https://open.feishu.cn/open-apis/bitable/v1/apps/$APP_TOKEN/tables/$TABLE_ID/records?page_size=20" \
  -H "Authorization: Bearer $TENANT_TOKEN"
```

**创建记录：**
```bash
curl -s -X POST "https://open.feishu.cn/open-apis/bitable/v1/apps/$APP_TOKEN/tables/$TABLE_ID/records" \
  -H "Authorization: Bearer $TENANT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{
    \"fields\": {
      \"字段名1\": \"值1\",
      \"字段名2\": 123,
      \"字段名3\": true
    }
  }"
```

**批量创建记录：**
```bash
curl -s -X POST "https://open.feishu.cn/open-apis/bitable/v1/apps/$APP_TOKEN/tables/$TABLE_ID/records/batch_create" \
  -H "Authorization: Bearer $TENANT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{
    \"records\": [
      {\"fields\": {\"字段名1\": \"值A\", \"字段名2\": 1}},
      {\"fields\": {\"字段名1\": \"值B\", \"字段名2\": 2}}
    ]
  }"
```

**更新记录：**
```bash
curl -s -X PUT "https://open.feishu.cn/open-apis/bitable/v1/apps/$APP_TOKEN/tables/$TABLE_ID/records/$RECORD_ID" \
  -H "Authorization: Bearer $TENANT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{
    \"fields\": {
      \"字段名1\": \"新值\"
    }
  }"
```

**删除记录：**
```bash
curl -s -X DELETE "https://open.feishu.cn/open-apis/bitable/v1/apps/$APP_TOKEN/tables/$TABLE_ID/records/$RECORD_ID" \
  -H "Authorization: Bearer $TENANT_TOKEN"
```

> **多维表格 Token 说明**：`app_token` 可从多维表格 URL 中提取，格式如 `https://xxx.feishu.cn/base/BASExxxxxx`，其中 `BASExxxxxx` 即为 app_token。

### 模块四：Webhook 机器人

最简单的消息推送方式，无需获取 token。

**发送文本消息：**
```bash
curl -s -X POST "$FEISHU_WEBHOOK_URL" \
  -H 'Content-Type: application/json' \
  -d "{
    \"msg_type\": \"text\",
    \"content\": {
      \"text\": \"$MESSAGE_TEXT\"
    }
  }"
```

**发送富文本消息：**
```bash
curl -s -X POST "$FEISHU_WEBHOOK_URL" \
  -H 'Content-Type: application/json' \
  -d "{
    \"msg_type\": \"post\",
    \"content\": {
      \"post\": {
        \"zh_cn\": {
          \"title\": \"$TITLE\",
          \"content\": [[{\"tag\": \"text\", \"text\": \"$CONTENT\"}]]
        }
      }
    }
  }"
```

**发送卡片消息：**
```bash
curl -s -X POST "$FEISHU_WEBHOOK_URL" \
  -H 'Content-Type: application/json' \
  -d "{
    \"msg_type\": \"interactive\",
    \"card\": {
      \"header\": {
        \"title\": {\"tag\": \"plain_text\", \"content\": \"$CARD_TITLE\"},
        \"template\": \"blue\"
      },
      \"elements\": [
        {\"tag\": \"markdown\", \"content\": \"$CARD_CONTENT\"}
      ]
    }
  }"
```

> **安全设置**：如果 Webhook 开启了签名校验，需要在请求中附加 `timestamp` 和 `sign` 字段。详见 [API 参考文档](references/api-reference.md)。

### 模块五：审批查询

**查询审批实例列表：**
```bash
curl -s -X GET "https://open.feishu.cn/open-apis/approval/v4/instances?approval_code=$APPROVAL_CODE&page_size=20" \
  -H "Authorization: Bearer $TENANT_TOKEN"
```

**查询单个审批实例详情：**
```bash
curl -s -X GET "https://open.feishu.cn/open-apis/approval/v4/instances/$INSTANCE_ID" \
  -H "Authorization: Bearer $TENANT_TOKEN"
```

**审批状态值说明：**
- `PENDING` — 审批中
- `APPROVED` — 已通过
- `REJECTED` — 已拒绝
- `CANCELED` — 已撤回
- `DELETED` — 已删除

> **权限提示**：审批操作需要为应用开通 `approval:approval` 相关权限。

---

## 错误处理

### 常见错误码

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 99991663 | token 无效或过期 | 重新获取 tenant_access_token |
| 99991668 | token 为空 | 检查请求头中的 Authorization |
| 99991672 | 权限不足 | 在开放平台为应用添加对应 API 权限 |
| 99991400 | 请求参数错误 | 检查请求体 JSON 格式和必填参数 |
| 99991401 | 未授权 | 检查 app_id 和 app_secret 是否正确 |
| 230001 | 频率限制 | 降低请求频率，建议间隔 100ms 以上 |

### 错误处理流程

1. 检查 HTTP 状态码，非 200 先查网络问题
2. 解析响应中的 `code` 字段，0 表示成功
3. 对于 token 过期错误，自动重新获取 token 后重试
4. 对于权限错误，指引用户前往开放平台配置权限
5. 对于频率限制，等待后重试

---

## 辅助脚本

本技能附带 shell 辅助脚本，可快速执行常见操作：

```bash
# 加载辅助函数
source scripts/feishu-api.sh

# 获取访问令牌
get_tenant_token

# 通过 Webhook 发送消息
send_webhook_message "部署完成，版本 v1.2.3"

# 通过 Bot API 发送消息
send_bot_message "$CHAT_ID" "构建通知：全部测试通过"
```

---

## 端到端场景示例

### 场景 1：每日站会自动通知

> 需求：每天早上 9:30 自动在团队群发送站会提醒，附带当天日期和会议链接。

```bash
# 1. 配置 Webhook
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/your-hook-id"

# 2. 发送富文本卡片
curl -X POST "$FEISHU_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "interactive",
    "card": {
      "header": {
        "title": {"tag": "plain_text", "content": "📋 每日站会提醒"},
        "template": "blue"
      },
      "elements": [
        {"tag": "div", "text": {"tag": "lark_md", "content": "**日期**: '"$(date +%Y-%m-%d)"'\n**时间**: 09:30-09:45\n**会议室**: 3楼A会议室"}},
        {"tag": "action", "actions": [
          {"tag": "button", "text": {"tag": "plain_text", "content": "加入会议"}, "url": "https://meetings.feishu.cn/your-meeting", "type": "primary"}
        ]}
      ]
    }
  }'
```

### 场景 2：将 GitHub Issue 同步到飞书多维表格

> 需求：新建 Issue 时，自动在飞书多维表格追加一行记录。

```bash
# 1. 获取 Token
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{"app_id":"'"$FEISHU_APP_ID"'","app_secret":"'"$FEISHU_APP_SECRET"'"}' | python3 -c "import sys,json;print(json.load(sys.stdin)['tenant_access_token'])")

# 2. 追加记录到多维表格
APP_TOKEN="your_bitable_app_token"
TABLE_ID="your_table_id"
curl -X POST "https://open.feishu.cn/open-apis/bitable/v1/apps/$APP_TOKEN/tables/$TABLE_ID/records" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "标题": "'"$ISSUE_TITLE"'",
      "状态": "待处理",
      "优先级": "P1",
      "创建时间": '"$(date +%s000)"',
      "链接": "'"$ISSUE_URL"'"
    }
  }'
```

### 场景 3：部署完成后发送通知 + 更新文档

> 需求：CI/CD 部署完成后，同时推送群通知和更新版本文档。

```bash
# 1. 获取 Token
source feishu-api.sh  # 使用 scripts/feishu-api.sh

# 2. 发送群通知
send_webhook_message "🚀 v$VERSION 部署完成 | 环境: $ENV | 耗时: ${DURATION}s"

# 3. 更新版本文档（在文档末尾追加内容）
DOC_TOKEN="your_doc_token"
BLOCK_ID="your_block_id"
curl -X POST "https://open.feishu.cn/open-apis/docx/v1/documents/$DOC_TOKEN/blocks/$BLOCK_ID/children" \
  -H "Authorization: Bearer $(get_tenant_token)" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [{
      "block_type": 2,
      "text": {"elements": [{"text_run": {"content": "v'"$VERSION"' - '"$(date +%Y-%m-%d)"' - 部署成功"}}]}
    }]
  }'
```

---

## 使用注意事项

- **安全**：不要将 `FEISHU_APP_SECRET` 或 `FEISHU_WEBHOOK_URL` 硬编码到代码中，始终使用环境变量
- **Token 缓存**：tenant_access_token 有效期 2 小时，建议在脚本中缓存并在过期时刷新
- **分页**：列表类 API 默认返回 20 条，如需更多数据需处理 `page_token` 分页
- **权限申请**：首次使用某类 API 前，需在飞书开放平台 → 应用管理 → 权限管理中申请对应权限
- **版本管理**：飞书 API 有 v1/v2 等多个版本，本工具包默认使用最新稳定版本

---

## 能力边界

本技能覆盖飞书开放平台最常用的 5 大场景。以下场景暂不支持，如有需要可通过 **Skill Hub** 搜索更多专项技能：

- 飞书日历、会议管理
- 飞书云文档高级排版（插入图片、表格嵌套等）
- 飞书应用商店上架流程
- 飞书事件订阅（Event Subscription）服务端开发
- 飞书小程序开发

> 输入 `/skill-hub` 或告诉 Agent "帮我找一个 XXX 的技能" 即可搜索 Skill Hub 应用市场。
