---
name: discord-notify
description: 通过 Discord 向用户手机发送通知。当用户要求在任务完成、条件达成或出现异常时通知自己，使用此 skill。
---

# discord-notify

通过 Discord 向用户手机发送实时通知。

## When to use

**当用户表达以下意图时，使用此 Skill：**
- "完成后通知我"
- "有结果了发消息给我"
- "帮我监控这个，有问题告诉我"
- "跑完了告诉我一声"
- "达成 xxx 条件后通知我"
- "发个提醒/通知到我手机"

**典型场景：**
- 🔔 任务完成通知（脚本跑完、构建完成等）
- 📊 状态监控（网站恢复、服务异常等）
- ⏰ 定时提醒（到点提醒我 xxx）
- 📋 结果汇报（数据处理完了告诉你）

## 环境检测

**首次使用时，AI 应运行检测脚本检查环境配置：**

```bash
cd discord-notify && node check.js
```

检测脚本会检查：
- ✅ 环境变量是否配置
- ✅ 依赖是否安装
- ✅ Bot Token 是否有效
- ✅ User ID 是否有效

**根据检测结果，AI 应指导用户完成配置。**

## 发送通知

```bash
node discord-notify/send.js "通知内容"
```

**支持超长消息**：超过 2000 字符会自动分割发送。

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `DISCORD_BOT_TOKEN` | ✅ | 机器人 Token |
| `DISCORD_USER_ID` | ✅ | 目标用户 ID |
| `HTTPS_PROXY` / `HTTP_PROXY` / `ALL_PROXY` | ❌ | 代理地址（可选） |

## User ID 获取方式

Discord 设置 → 高级 → 开启开发者模式 → 右键自己 → 复制 ID

## 配置步骤

1. **创建 Discord Bot**
   - 访问 https://discord.com/developers/applications
   - 创建 Application → Bot → 复制 Token

2. **邀请 Bot 到服务器**
   - 使用 Bot 的 OAuth2 URL 邀请到你的 Discord 服务器

3. **获取 User ID**
   - Discord 设置 → 高级 → 开启开发者模式
   - 右键点击你的头像 → 复制 ID

4. **配置环境变量**
   ```bash
   export DISCORD_BOT_TOKEN="你的Token"
   export DISCORD_USER_ID="你的ID"
   export HTTPS_PROXY="http://127.0.0.1:1080"  # 可选
   ```

## 返回值

### 成功
```json
{
  "success": true,
  "message": "消息发送成功",
  "chunks": 1,
  "sent": 1
}
```

超长消息会显示分割信息：
```json
{
  "success": true,
  "message": "消息发送成功",
  "chunks": 2,
  "sent": 2,
  "note": "消息已分割为 2 条发送"
}
```

### 失败
```json
{
  "success": false,
  "error": "无法创建私聊频道: 请求参数错误: Invalid Recipient(s)"
}
```

## AI 使用示例

当用户说："帮我跑这个脚本，跑完了告诉我"

AI 应该：
1. 开始执行脚本
2. 等待完成
3. 调用 `node discord-notify/send.js "✅ 脚本执行完成！"`
4. 告诉用户"已通知"

## 目录结构

```
discord-notify/
├── SKILL.md          # Skill 说明文档
├── check.js          # 环境检测脚本
├── send.js           # 发送通知脚本
└── package.json      # 依赖配置
```
