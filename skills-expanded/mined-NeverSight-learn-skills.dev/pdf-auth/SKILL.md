---
name: pdf-auth
version: 1.0.0
description: "pdf-cli 认证模块：登录、登出与账号状态管理。使用邮箱密码登录获取 token、查看当前登录状态和用户信息、退出登录清除本地凭证。当用户需要登录、查看账号信息、或退出登录时使用。"
metadata:
  requires:
    bins: ["pdf-cli"]
  cliHelp: "pdf-cli auth --help"
---

# auth

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../pdf-shared/SKILL.md`](../pdf-shared/SKILL.md)，其中包含认证、配置、错误处理**

## Core Concepts

- **Token**: 登录后获取的 JWT 令牌，存储在 `~/.config/pdf-cli/config.json`，用于后续 API 请求认证
- **DeviceID**: 设备唯一标识，首次使用时自动生成 UUID 并持久化，随每次请求发送
- **ClientType**: 客户端类型标识，固定为 `cli`

## 命令概览

| 命令 | 说明 | 需要登录 |
|------|------|----------|
| [`login`](references/pdf-auth-login.md) | 使用邮箱密码登录 | 否 |
| [`status`](references/pdf-auth-status.md) | 查看登录状态和用户信息 | 否（未登录时提示） |
| [`logout`](references/pdf-auth-logout.md) | 退出登录，清除本地 token | 否 |

## 快速开始

```bash
# 登录
pdf-cli auth login --email you@example.com
# 输入密码（交互式）

# 查看状态
pdf-cli auth status

# 退出
pdf-cli auth logout
```

## Important Notes

- 登录使用 JSON POST 请求，密码通过交互式终端输入，不支持命令行参数传递
- 登录时自动生成 deviceId（如果不存在），并随请求发送
- token 过期后需要重新登录
- logout 会同时通知服务端并清除本地 token
