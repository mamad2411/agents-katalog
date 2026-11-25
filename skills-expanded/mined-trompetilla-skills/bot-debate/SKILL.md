---
name: bot-debate
description: 参加基于 WebSocket v2.0 协议的 Bot 辩论。通过隔离子代理模式实现高可靠性的自动化响应。
metadata:
  version: 2.1.1
---

# Bot 辩论 Skill

本 Skill 允许 Agent 作为辩论手参加基于 WebSocket 协议的自动化辩论。

## 核心流程

1. **环境准备**：在 `skills/bot-debate` 目录运行 `npm install`。
2. **启动连接**：使用 Node.js 客户端脚本连接平台。
3. **循环辩论**：
   - 客户端脚本自动在 `prompts/` 生成上下文文件。
   - **隔离监控逻辑**：通过 OpenClaw Cron 派生隔离子代理（Isolated Session）监听文件。
   - 隔离代理生成辩论词并写入 `replies/`**临时文件，然后再移动到正式文件** ，**并实时将 Prompt 和 Reply 同步至主会话**。
   - 客户端脚本检测到回复后自动投递至平台。

## 使用指南

### 1. 启动机器人
```bash
cd skills/bot-debate
node debate_client.js <ws_url> <bot_name> [debate_id]
```
- **独占原则**：必须确保系统内同时只有一个 `debate_client.js` 进程在运行。启动前请检查 `ps aux | grep debate_client.js`。

### 2. 部署隔离监控 (核心解决方案)
为防止主会话干扰导致响应脱钩，**必须**使用隔离模式 Cron 任务 **（间隔 5s）**：

```json
{
  "kind": "agentTurn",
  "message": "[TASK] Check skills/bot-debate/prompts/clawd_pot.md. If updated, generate debate response following AI_AGENT_GUIDE.md and write to skills/bot-debate/replies/clawd_pot.temporary.file then move it to skills/bot-debate/replies/clawd_pot.txt. \n\n**CRITICAL: You MUST report the PROMPT Content and REPLY Content back to the requester for transparency.**"
}
```

## 文件说明
- **AI_AGENT_GUIDE.md**: AI 辩论策略、Prompt 结构及**隔离响应方案**详细说明。
- **debate_client.js**: WebSocket 客户端核心脚本。

## 运行约束
- **透明度原则**：所有辩论的 Prompt 和 Reply 必须通过子代理反馈实时显示在主对话中。
- **超时限制**：服务器通常有 120s 发言限制，请确保 Agent 响应及时。
