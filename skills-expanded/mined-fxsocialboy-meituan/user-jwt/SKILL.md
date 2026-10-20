---
name: user-jwt
description: Get user JWT token or username for ByteCloud CN or I18N regions. Use when the user needs a JWT token, username for API authentication, debugging requests, or accessing ByteCloud services.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# 获取用户 JWT Token / 用户名

> **何时使用**: 当需要获取用户的 JWT Token 或用户名，用于 API 认证、调试请求或访问 ByteCloud 服务时使用此工具。

## 功能说明

通过 `gdpa-cli` 获取当前登录用户的 JWT Token 或用户名。支持中国区（cn）和国际区（i18n）两个区域。

## 前置条件

需要先登录对应区域的 ByteCloud 账号：

```bash
# 登录所有区域
gdpa-cli login

# 或登录指定区域
gdpa-cli login cn
gdpa-cli login i18n
```

## 使用方法

### 获取 JWT Token

```bash
# 获取中国区 JWT
gdpa-cli login -p cn

# 获取国际区 JWT
gdpa-cli login -p i18n
```

`-p` 是 `--print-jwt` 的简写，输出当前用户指定区域的 JWT Token（纯文本，可直接使用）。

### 获取用户名

```bash
# 获取中国区用户名
gdpa-cli login -u cn

# 获取国际区用户名
gdpa-cli login -u i18n
```

`-u` 是 `--print-user` 的简写，输出当前登录用户的用户名（纯文本）。

### 获取 AccessToken

```bash
# 获取中国区 AccessToken
gdpa-cli login -a cn

# 获取国际区 AccessToken
gdpa-cli login -a i18n
```

## 参数说明

| 参数 | 简写 | 说明 | 可选值 |
|------|------|------|--------|
| `--print-jwt` | `-p` | 打印指定区域的 JWT | `cn`, `i18n` |
| `--print-user` | `-u` | 打印指定区域的用户名 | `cn`, `i18n` |
| `--print-access-token` | `-a` | 打印指定区域的 AccessToken | `cn`, `i18n` |

## 使用场景

### 1. 直接获取 JWT 并赋值给变量

```bash
JWT_TOKEN=$(gdpa-cli login -p cn)
```

### 2. 获取当前用户名

```bash
USER_NAME=$(gdpa-cli login -u cn)
```

### 3. 用于 HTTP 请求认证

```bash
curl -H "Authorization: Bearer $(gdpa-cli login -p i18n)" https://api.example.com/resource
```

## 注意事项

1. JWT Token 有有效期，过期后需要重新登录获取
2. 如果未登录或 Token 已过期，命令会自动触发登录流程
3. 输出内容为纯文本字符串，不包含额外格式或换行
