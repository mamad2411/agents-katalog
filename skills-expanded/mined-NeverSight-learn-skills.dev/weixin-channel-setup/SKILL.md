---
name: weixin-channel-setup
description: 帮助用户快速配置和使用微信通道功能。当用户想要"配置微信"、"连接微信"、"设置微信机器人"、"weixin setup"、"wechat channel"时使用此技能。
---

# 微信通道配置助手

本技能帮助用户快速配置 Qwen Code 的微信通道功能，让 AI 助手通过微信与你交互。

## 快速开始（3 步完成）

### 第 1 步：扫码登录微信

运行以下命令启动微信登录流程：

```bash
qwen channel configure-weixin
```

**操作流程：**

1. 终端会显示二维码 URL
2. 打开该 URL 查看二维码
3. 使用微信扫码并确认登录
4. 等待提示 "Connected to WeChat successfully!"

**保存的信息：**

- Token 和 BaseURL 自动保存到 `~/.qwen/channels/weixin/account.json`
- 你的微信 ID 会自动记录，后续配置需要用到

### 第 2 步：添加到配置文件

编辑 `~/.qwen/settings.json`，添加或更新 `channels` 配置：

```json
{
  "channels": {
    "my-weixin": {
      "type": "weixin",
      "senderPolicy": "allowlist",
      "allowedUsers": ["YOUR_WEIXIN_USER_ID"],
      "sessionScope": "user",
      "cwd": "/path/to/your/project",
      "instructions": "你是一个简洁的编程助手，通过微信回复。保持回答简短。",
      "model": "qwen3.5-plus"
    }
  }
}
```

**获取你的微信 ID：**

```bash
cat ~/.qwen/channels/weixin/account.json | grep userId
```

将输出中的 `userId` 值替换到配置文件的 `allowedUsers` 数组中。

### 第 3 步：启动通道服务

```bash
qwen channel start my-weixin
```

看到 "[Channel] "my-weixin" is running. Press Ctrl+C to stop." 即表示成功！

现在打开微信，找到你的机器人助手，发送消息测试吧。

---

## 配置选项说明

| 选项           | 必填 | 说明                                                               | 示例                    |
| -------------- | ---- | ------------------------------------------------------------------ | ----------------------- |
| `type`         | ✅   | 通道类型，固定为 `"weixin"`                                        | `"weixin"`              |
| `senderPolicy` | ❌   | 访问策略：`allowlist`（白名单）、`open`（公开）、`pairing`（配对） | `"allowlist"`           |
| `allowedUsers` | 推荐 | 允许使用的微信用户 ID 列表                                         | `["o9cq803zPvc..."]`    |
| `sessionScope` | ❌   | 会话范围：`user`（每用户独立）、`single`（全局共享）               | `"user"`                |
| `cwd`          | 推荐 | AI 工作目录                                                        | `"/Users/name/project"` |
| `instructions` | ❌   | 系统指令，控制 AI 行为风格                                         | "保持回答简短"          |
| `model`        | ❌   | 使用的模型                                                         | `"qwen3.5-plus"`        |

---

## 常用管理命令

```bash
# 查看当前配置的通道
qwen channel --help

# 启动微信通道
qwen channel start my-weixin

# 查看微信账号状态
qwen channel configure-weixin status

# 清除微信凭证（重新登录时使用）
qwen channel configure-weixin clear

# 停止通道（Ctrl+C 或 kill 进程）
kill <PID>
```

---

## 故障排查

### 问题 1：扫码后无法连接

**可能原因：**

- 网络问题导致超时
- iLink API 暂时不可用

**解决方案：**

```bash
# 重新运行配置命令
qwen channel configure-weixin
```

### 问题 2：发送消息无响应

**检查清单：**

- [ ] 通道服务是否正在运行（`ps aux | grep "channel start"`）
- [ ] 你的微信 ID 是否在 `allowedUsers` 中
- [ ] `settings.json` 格式是否正确（JSON 语法）

**调试方法：**

```bash
# 查看详细日志
DEBUG=1 qwen channel start my-weixin
```

### 问题 3：想更换微信账号

```bash
# 清除旧凭证
qwen channel configure-weixin clear

# 重新扫码登录
qwen channel configure-weixin
```

---

## 高级用法

### 多用户支持

在 `allowedUsers` 中添加多个微信用户：

```json
{
  "channels": {
    "my-weixin": {
      "type": "weixin",
      "senderPolicy": "allowlist",
      "allowedUsers": ["user1@im.wechat", "user2@im.wechat", "user3@im.wechat"]
    }
  }
}
```

### 开放模式（任何人可用）

⚠️ **警告**：此模式下任何人都可以使用你的机器人，请谨慎开启！

```json
{
  "channels": {
    "my-weixin": {
      "type": "weixin",
      "senderPolicy": "open"
    }
  }
}
```

### 自定义 AI 行为

通过 `instructions` 字段定义 AI 的风格：

```json
{
  "instructions": "你是一个专业的代码审查助手。回答要简洁专业，优先给出解决方案，然后解释原因。"
}
```

---

## 安全注意事项

1. **保护 account.json**：该文件包含你的微信认证 token，权限已设置为 `600`（仅所有者可读写）
2. **不要分享 token**：切勿将 `account.json` 内容分享给他人
3. **定期清理**：长时间不使用时，运行 `configure-weixin clear` 清除凭证

---

## 下一步

- 阅读完整文档：查看 `docs/users/features/channels/overview.md`
- 了解 Telegram 通道：查看 `docs/users/features/channels/telegram.md`
- 探索更多功能：运行 `qwen --help`
