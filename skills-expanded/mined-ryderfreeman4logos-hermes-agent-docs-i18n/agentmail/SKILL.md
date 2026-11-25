---
name: agentmail
description: Use when an agent needs AgentMail CLI email inboxes.
version: 1.0.0
author: Haakam Aujla (Haakam21), AgentMail
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Email, CLI, AgentMail, Communication]
    homepage: https://agentmail.to
prerequisites:
  commands: [agentmail]
required_environment_variables:
  - name: AGENTMAIL_API_KEY
    prompt: AgentMail API key (starts with am_)
    help: "Create one at https://console.agentmail.to — or run the CLI self-signup flow in references/signup.md to obtain a key without one."
    required_for: "authenticating the agentmail CLI; not needed before self-signup"
    optional: true
---

# AgentMail 技能

AgentMail 为智能体提供专属的邮箱收件箱，用于发送邮件、接收回复、完成邮件验证码流程以及处理传入邮件循环。该功能适用于智能体自身的邮箱收件箱，而非用户现有的 IMAP/SMTP 邮箱。

请优先使用 `agentmail` CLI 工具。仅在框架要求使用 MCP 工具时才使用 MCP，而在 CLI 缺少特定操作时才使用 REST 接口。

## 适用场景

- 智能体需要拥有属于自己的电子邮件地址。
- 任务涉及邮件验证码流程、回复、主题串、标签或附件处理。
- 智能体需要通过 webhook 或 WebSocket 方式接收传入邮件。

## 先决条件

- 需要通过 `terminal` 工具来运行命令。
- 需要安装 CLI 工具：

```bash
npm install -g agentmail-cli@latest
```

- 导出 API 密钥：

```bash
export AGENTMAIL_API_KEY="am_..."
```

还没有 API 密钥？请访问 [signup.md](references/signup.md) 进行注册。

## 如何运行

当其他命令或脚本需要获取 ID 时，请使用 `--format json` 参数。

```bash
agentmail inboxes list --format json
```

## 快速参考

- [AgentMail 代理参考文档](https://agentmail.md)：托管版文档。
- [AgentMail](https://agentmail.to)：产品介绍页面。
- [控制台](https://console.agentmail.to)：API 密钥与账户管理。
- [文档中心](https://docs.agentmail.to)：完整的产品文档。
- [signup.md](references/signup.md)：自助注册及 OTP 验证流程。
- [core.md](references/core.md)：收件箱、消息、对话线程、标签与附件相关说明。
- [webhooks.md](references/webhooks.md)：发送至公共 HTTPS 服务器的事件处理。
- [websockets.md](references/websockets.md)：发送至本地代理进程的事件处理。
- [mcp.md](references/mcp.md)：MCP 集成指南。

## 操作步骤

1. 安装 `agentmail-cli@latest`，并通过 `agentmail inboxes list --format json` 命令进行验证。
2. 若尚未拥有 API 密钥，请按照 [signup.md](references/signup.md) 完成注册。
3. 对于收件箱管理、发送消息、读取消息、回复消息、转发消息、添加标签、创建对话线程以及处理附件等操作，可参考 [core.md](references/core.md)。
4. 仅在轮询方式无法满足需求时，才使用 [webhooks.md](references/webhooks.md) 或 [websockets.md](references/websockets.md)。

## 常见误区

- 建议优先使用 `AGENTMAIL_API_KEY` 而非 `--api-key`。
- 绝对不要在提示词、日志、URL 或已提交的文件中泄露 `AGENTMAIL_API_KEY`。
- 在需要重试创建操作时，应使用稳定的 `client_id` 值。
- 若存在相关字段，建议优先使用 `extracted_text` 或 `extracted_html` 作为大语言模型的输入数据。
- 应对 `message.received` 事件做出响应，而非代理发送的消息。

## 验证方法

```bash
agentmail inboxes list --format json
```
