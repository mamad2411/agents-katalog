---
name: 51pm-login
description: 51PM项目管理系统登录技能。帮助用户完成Token认证登录。当用户说"登录51PM"、"51pm登录"、"配置token"、"设置认证"、"怎么登录"、"需要登录"等与登录认证相关的场景时使用。
metadata:
  requires:
    bins: ["51pm"]
  cliHelp: "51pm login --help"
---

# 51PM 登录认证

> `51pm` 是51PM项目管理系统的命令行工具，所有操作通过执行 `51pm` 命令完成。

## 登录命令

```bash
51pm login --token <TOKEN>
```

### 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| --token | string | 认证Token（可选，不传则进入交互式输入） |

### Token 获取方式

1. 在浏览器中打开 51PM 前端页面并登录
2. 按 F12 打开开发者工具
3. 切换到 Application -> Local Storage
4. 找到 `oauthToken` 字段，复制其值

### 使用示例

```bash
# 直接传入 token
51pm login --token eyJhbGciOiJIUzI1NiIs...

# 交互式输入（会提示输入 token）
51pm login
```

## 行为策略

- 登录成功后 token 保存在 `~/.51pm_cli/token.json`
- 其他命令（如 task list）返回"未登录"或"Token已过期"时，提示用户重新执行 `51pm login`
- **AI Agent 调用时推荐使用 --token 参数直接传入**，避免交互式输入
