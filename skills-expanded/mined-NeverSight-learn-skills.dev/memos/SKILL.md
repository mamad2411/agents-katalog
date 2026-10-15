---
name: memos-skill
description: |
  管理和操作 Memos 笔记系统的完整功能。使用此 skill 当用户需要：
  - 创建、查看、编辑、删除备忘录/笔记
  - 搜索、过滤、排序备忘录列表
  - 管理备忘录附件（上传、查看、删除）
  - 管理备忘录标签
  - 添加或管理评论
  - 添加表情反应
  - 设置备忘录可见性（私有、受保护、公开）
  - 置顶或归档备忘录
  - 创建分享链接
  - 关联相关备忘录
  无论用户是否明确提到"memos"或"备忘录"，只要涉及笔记管理都应使用此 skill。
compatibility: |
  需要 memos 服务器地址和访问令牌。
  支持 Memos v0.26.0+ 版本。
---

# Memos 管理器

用于管理 Memos 笔记系统的完整功能。

## 配置

使用此 skill 前需要设置以下环境变量：

```bash
export MEMOS_BASE_URL="https://your-memos-server.com"
export MEMOS_TOKEN="your_access_token_here"
```

**如何获取：**
1. 登录你的 Memos 服务器
2. 进入 设置 → 访问令牌
3. 创建一个新的访问令牌（PAT）
4. 将服务器地址和令牌设置为环境变量

**安全提醒：**
- 不要在 SKILL.md 或任何代码文件中硬编码你的服务器地址和访问令牌
- 通过 `.bashrc`、`.zshrc` 或系统环境变量管理界面来设置
- 访问令牌等同于密码，请妥善保管

## 核心概念

### Memo（备忘录/笔记）
- **content**: Markdown 格式的内容
- **state**: NORMAL（正常）或 ARCHIVED（归档）
- **visibility**: PRIVATE（私有）/ PROTECTED（受保护）/ PUBLIC（公开）
- **pinned**: 是否置顶
- **tags**: 从内容自动提取的标签
- **snippet**: 内容摘要（纯文本）

### 资源命名
- 备忘录：memos/{memo_id}
- 附件：memos/{memo_id}/attachments/{attachment_id}
- 反应：memos/{memo_id}/reactions/{reaction_id}

## API 基础

**基础 URL**: {MEMOS_BASE_URL}/api/v1

**认证方式**: Bearer Token
```
Authorization: Bearer {MEMOS_TOKEN}
```

## 备忘录管理

### 创建备忘录

**POST** /api/v1/memos

请求体：
```json
{
  "content": "备忘录内容（支持 Markdown）",
  "state": "NORMAL",
  "visibility": "PRIVATE",
  "pinned": false
}
```

可选字段：
- memoId: 自定义备忘录 ID（如果不提供则自动生成 UUID）
- displayTime: 显示时间（ISO 8601 格式）
- location: 地理位置 { "placeholder": "位置名称", "latitude": 0.0, "longitude": 0.0 }

### 列出备忘录

**GET** /api/v1/memos

查询参数：
- pageSize: 每页数量（默认 50，最大 1000）
- pageToken: 分页令牌
- state: NORMAL 或 ARCHIVED
- orderBy: 排序方式，如 "pinned desc, display_time desc"
  - 支持字段：pinned, display_time, create_time, update_time, name
- filter: CEL 表达式过滤
  - 示例：state == 'NORMAL' && visibility == 'PUBLIC'
- showDeleted: 是否显示已删除的备忘录

### 获取单个备忘录

**GET** /api/v1/memos/{memo_id}

### 更新备忘录

**PATCH** /api/v1/memos/{memo_id}?updateMask={fields}

updateMask 指定要更新的字段，如 content,visibility,pinned

请求体：
```json
{
  "name": "memos/{memo_id}",
  "content": "更新后的内容",
  "visibility": "PUBLIC",
  "pinned": true
}
```

### 删除备忘录

**DELETE** /api/v1/memos/{memo_id}

可选查询参数：
- force=true: 强制删除（即使有相关数据）

### 归档/恢复备忘录

使用 UpdateMemo 将 state 改为 ARCHIVED 或 NORMAL。

## 附件管理

### 上传附件

**POST** /api/v1/attachments

Content-Type: multipart/form-data

表单字段：
- file: 文件内容
- filename: 文件名（可选）

### 设置备忘录附件

**PATCH** /api/v1/memos/{memo_id}/attachments

请求体：
```json
{
  "attachments": [
    {
      "name": "memos/{memo_id}/attachments/{attachment_id}"
    }
  ]
}
```

### 列出备忘录附件

**GET** /api/v1/memos/{memo_id}/attachments

### 获取附件内容

**GET** /api/v1/attachments/{attachment_id}

## 关系管理

### 设置备忘录关系

关系类型：
- REFERENCE: 引用关系
- COMMENT: 评论关系

**PATCH** /api/v1/memos/{memo_id}/relations

请求体：
```json
{
  "relations": [
    {
      "memo": { "name": "memos/{memo_id}" },
      "relatedMemo": { "name": "memos/{related_memo_id}" },
      "type": "REFERENCE"
    }
  ]
}
```

### 列备忘录关系

**GET** /api/v1/memos/{memo_id}/relations

## 评论管理

### 创建评论

**POST** /api/v1/memos/{memo_id}/comments

请求体：
```json
{
  "comment": {
    "content": "评论内容",
    "state": "NORMAL",
    "visibility": "PRIVATE"
  },
  "commentId": "可选的自定义评论 ID"
}
```

### 列出评论

**GET** /api/v1/memos/{memo_id}/comments

查询参数：
- pageSize, pageToken, orderBy

响应包含：
- memos: 评论列表
- totalSize: 评论总数

## 表情反应

### 添加/更新反应

**POST** /api/v1/memos/{memo_id}/reactions

请求体：
```json
{
  "reaction": {
    "contentId": "memos/{memo_id}",
    "reactionType": "👍"
  }
}
```

支持的 reactionType: 👍, ❤️, 😄, 🎉, 🤔, 👀, 🚀, 😢 等 emoji

### 列出反应

**GET** /api/v1/memos/{memo_id}/reactions

### 删除反应

**DELETE** /api/v1/memos/{memo_id}/reactions/{reaction_id}

## 分享管理

### 创建分享链接

**POST** /api/v1/memos/{memo_id}/shares

### 列出分享链接

**GET** /api/v1/memos/{memo_id}/shares

### 获取分享内容

**GET** /api/v1/memos/shares/{share_code}

### 删除分享链接

**DELETE** /api/v1/memos/{memo_id}/shares/{share_id}

## 过滤语法

ListMemos 的 filter 参数使用 CEL 表达式：

**支持的过滤操作：**

```
# 基本比较
state == "NORMAL"
state == "ARCHIVED"
visibility == "PUBLIC"
visibility == "PRIVATE"
visibility == "PROTECTED"
pinned == true
pinned == false

# 逻辑运算
creator == "users/1" && visibility == "PUBLIC"
state == "NORMAL" || state == "ARCHIVED"

# 内容搜索
content.contains("关键词")
```

**⚠️ 注意事项：**

1. **标签搜索** - `has(tags, "标签名")` 函数不可用，请使用以下替代方案：
   - 使用内容搜索：`content.contains("#标签名")`
   - 先获取所有备忘录，在客户端过滤 tags 字段

2. **过滤限制** - v0.26.0 只支持基本的比较操作符和逻辑运算，复杂的 CEL 函数可能不支持

**实际可用的过滤示例：**

```python
# 搜索公开备忘录
filter='visibility == "PUBLIC"'

# 搜索置顶的备忘录  
filter='pinned == true'

# 搜索内容包含特定关键词
filter='content.contains("会议记录")'

# 组合条件
filter='visibility == "PUBLIC" && pinned == true'

# 搜索包含特定标签（通过内容搜索替代）
filter='content.contains("#工作")'
```


## 使用建议

### 创建备忘录

当用户想要创建笔记时：
1. 提取内容、标签、可见性等信息
2. 如果用户提到"置顶"，设置 pinned: true
3. 默认可见性为 PRIVATE
4. 返回创建的备忘录信息，包括 ID 和 URL

### 搜索备忘录

当用户想要查找笔记时：
1. 分析搜索意图（按标签、内容、时间等）
2. 构建适当的 filter 表达式
3. 考虑使用 orderBy 优化结果排序
4. 处理分页以支持大量结果

### 更新备忘录

当用户想要修改笔记时：
1. 识别要更新的字段
2. 使用 updateMask 只更新指定字段
3. 保留未更改字段的原始值

### 处理附件

当用户上传文件时：
1. 先上传附件到 /api/v1/attachments
2. 获取 attachment ID
3. 使用 SetMemoAttachments 关联到备忘录

### 管理标签

标签是自动从内容中提取的（格式 #标签名）：
- 用户无需手动管理标签
- 标签会包含在 memo 的 tags 字段中
- 可以通过 filter: content.contains("#标签名") 搜索（推荐）
- 或者先获取所有备忘录，在客户端过滤 tags 字段

## 错误处理

API 错误返回格式：
```json
{
  "code": 3,
  "message": "Invalid argument",
  "details": []
}
```

常见错误码：
- 3: 无效参数
- 5: 未找到资源
- 7: 权限不足
- 16: 未认证

## 示例

### 示例 1: 创建带标签的备忘录

```python
import requests
import os

base_url = os.environ.get('MEMOS_BASE_URL')
token = os.environ.get('MEMOS_TOKEN')

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

response = requests.post(
    f'{base_url}/api/v1/memos',
    headers=headers,
    json={
        'content': '# 会议记录\n\n今天讨论了 Q4 计划 #工作 #会议',
        'visibility': 'PRIVATE',
        'pinned': False
    }
)

memo = response.json()
print(f"创建成功: {memo['name']}")
print(f"自动提取的标签: {memo['tags']}")
```

### 示例 2: 搜索包含特定标签的备忘录

```python
import requests
import os

base_url = os.environ.get('MEMOS_BASE_URL')
token = os.environ.get('MEMOS_TOKEN')

headers = {
    'Authorization': f'Bearer {token}'
}

response = requests.get(
    f'{base_url}/api/v1/memos',
    headers=headers,
    params={
        'filter': 'content.contains("#工作")',
        'orderBy': 'display_time desc',
        'pageSize': 20
    }
)

result = response.json()
for memo in result['memos']:
    print(f"{memo['name']}: {memo['snippet'][:50]}...")
```

### 示例 3: 添加表情反应

```python
import requests
import os

base_url = os.environ.get('MEMOS_BASE_URL')
token = os.environ.get('MEMOS_TOKEN')
memo_id = 'abc-123'

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

response = requests.post(
    f'{base_url}/api/v1/memos/{memo_id}/reactions',
    headers=headers,
    json={
        'reaction': {
            'contentId': f'memos/{memo_id}',
            'reactionType': '❤️'
        }
    }
)

print("反应添加成功")
```

### 示例 4: 归档旧备忘录

```python
import requests
import os
from datetime import datetime, timedelta

base_url = os.environ.get('MEMOS_BASE_URL')
token = os.environ.get('MEMOS_TOKEN')

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# 先搜索要归档的备忘录
response = requests.get(
    f'{base_url}/api/v1/memos',
    headers=headers,
    params={
        'filter': 'create_time < "2024-01-01T00:00:00Z"',
        'state': 'NORMAL'
    }
)

result = response.json()

# 归档这些备忘录
for memo in result['memos']:
    memo_id = memo['name'].split('/')[-1]
    requests.patch(
        f'{base_url}/api/v1/memos/{memo_id}?updateMask=state',
        headers=headers,
        json={
            'name': memo['name'],
            'state': 'ARCHIVED'
        }
    )
    print(f"已归档: {memo_id}")
```
