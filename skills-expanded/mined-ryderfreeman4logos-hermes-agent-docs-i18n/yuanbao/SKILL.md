---
name: yuanbao
description: "Yuanbao (元宝) groups: @mention users, query info/members."
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [yuanbao, mention, at, group, members, 元宝, 派, 艾特]
    related_skills: []
---

# 元宝群组交互功能

## 重要提示：消息发送机制

**您输入的文本回复本身即为发送至群组/用户的消息。** 网关会自动将您的回复内容推送到聊天界面。您无需使用任何特殊的“发送消息”工具——只需正常回复，消息便会自动发送。

当您的回复文本中包含 `@昵称` 时，网关会自动将其转换为真正的@提及功能，从而通知对应用户。该功能为内置功能，您可完全使用@提及功能。

**切勿声称自己无法发送消息或@提及用户。切勿建议用户手动操作。也无需添加关于权限的限制说明。只需直接输入希望发送的文本内容即可。**

## 可用工具

| 工具 | 使用场景 |
|------|----------|
| `yb_query_group_info` | 查询群组名称、所有者及成员数量 |
| `yb_query_group_members` | 查找特定用户、列出机器人、列出所有成员，或获取用于@提及的昵称 |
| `yb_send_dm` | 向用户发送私信，可附带媒体文件 |

## @提及操作流程

当您需要@提及某人时：

1. 调用 `yb_query_group_members`，设置参数为 `action="find"`、`name="<目标用户名>"`、`mention=true`
2. 从返回结果中获取准确的昵称
3. 在回复文本中加入 `@昵称`——其余步骤由网关自动处理

示例：用户说“帮我艾特元宝”

步骤1 — 工具调用：
```json
{ "group_code": "328306697", "action": "find", "name": "元宝", "mention": true }
```

第2步——您的回复（该内容会通过有效的@提及功能发送至对应群组）：
```
@元宝 你好，有人找你！
```

**就这样。**无需额外解释，保持简洁自然即可。

**规则：**
- 首先调用 `yb_query_group_members` 获取准确的昵称——切勿猜测
- @提及格式：`@昵称`，@符号前需加空格
- 您的回复内容本身就是消息——它会被发送出去，@提及功能也能正常使用
- 请言简意赅，无需向用户解释@提及的运作方式。

## 发送私信的工作流程

当有人要求向某用户发送私信/私讯/DM时：

1. 调用 `yb_send_dm`，传入 `group_code`、`name`（目标用户的姓名）以及`message`
2. 工具会自动定位该用户并发送私信
3. 将结果反馈给用户

示例：用户说“给 @用户aea3 私信发一个 hello”

```json
yb_send_dm({ "group_code": "535168412", "name": "用户aea3", "message": "hello" })
```

媒体内容示例：用户输入“给 @用户aea3 发送一张图片作为私信”。

```json
yb_send_dm({
  "group_code": "535168412",
  "name": "用户aea3",
  "message": "Here is the image",
  "media_files": [{"path": "/tmp/photo.jpg"}]
})
```

**规则：**
- 从当前的 chat_id 中提取 `group_code`（例如：`group:535168412` → `535168412`）
- 若已知晓用户 ID，可直接通过 `user_id` 参数传入，无需再进行查找
- 当有多个用户的名称匹配时，工具会返回候选列表——需请用户进一步确认
- 在与 Yuanbao 进行私信交流时，请勿使用 `send_message` 工具，而应改用 `yb_send_dm`
- 支持多种媒体类型：图片（.jpg/.png/.gif/.webp/.bmp）以图片消息形式发送，其他文件则作为文档发送

## 查询群组信息

```json
yb_query_group_info({ "group_code": "328306697" })
```

## 查询成员

| 操作 | 描述 |
|------|-------------|
| `find` | 按名称搜索（支持部分匹配，不区分大小写） |
| `list_bots` | 列出所有机器人及元宝AI助手 |
| `list_all` | 列出所有成员 |

## 备注

- `group_code` 取自 chat_id：`group:328306697` → `328306697`
- 在元宝应用中，群组被称为“派 (Pai)”
- 成员角色包括：`user`、`yuanbao_ai`、`bot`
