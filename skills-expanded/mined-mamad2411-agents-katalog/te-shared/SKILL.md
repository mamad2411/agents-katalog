---
name: te-shared
version: 1.0.0
description: "TE CLI 基础：认证配置、全局参数、错误处理、安全约束"
metadata:
  requires:
    bins: ["te-cli"]
  cliHelp: "te-cli --help"
---

# te-shared

TE CLI (`te-cli`) 是 ThinkingEngine 数据分析平台的命令行工具，供 AI Agent 和人类用户使用。

## 认证

使用前必须先认证。认证优先级：

1. 环境变量 `TE_TOKEN`（最高优先，适合 CI/脚本）
2. 缓存 token（`~/.te-cli/tokens.json`，20 小时有效）
3. macOS 自动从 Chrome 提取（仅 macOS）

### 认证命��

```bash
# macOS 自动认证（从 Chrome 提取 token）
te-cli auth login

# 手动设置 token
te-cli auth set-token <token>

# 查看认证状态
te-cli auth status

# 登出
te-cli auth logout
```

### 多环境支持

```bash
# 指定 host
te-cli auth login --host ta-staging.example.com
te-cli auth set-token <token> --host ta-staging.example.com

# 配置默认 host
te-cli config set defaultHost ta-staging.example.com
```

## 全局参数

所有命令支持以下全局参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--host <host>` | TE 实例地址 | 配置中的 defaultHost 或 ta.thinkingdata.cn |
| `--format <json\|table>` | 输出格式 | json |
| `--jq <expr>` | jq 过滤表达式 | - |
| `--dry-run` | 只显示请求，不执行 | false |
| `--yes` | 跳过 write 操作确认 | false |

## 输出格式

### JSON（默认）

```json
{
  "ok": true,
  "data": { ... }
}
```

### Table

```bash
te-cli meta +list-events -p 1 --format table
```

### jq 过滤

```bash
te-cli meta +list-events -p 1 --jq '.events[].eventName'
```

## 错误处理

错误输出到 stderr，格式：

```json
{
  "ok": false,
  "error": {
    "type": "auth | api | validation | config",
    "message": "...",
    "hint": "..."
  }
}
```

退出码：成功 `0`，错误 `1`。

## 安全约束

- `risk: read` 的命令直接执行
- `risk: write` 的命令需要确认，除非传入 `--yes`
- 使用 `--dry-run` 可以预览将要发送的请求

## 命令结构

```bash
te-cli <domain> +<command> [flags]
te-cli api <METHOD> <PATH> [--params] [--data]
```

域：`meta`（元数据）、`analysis`（分析）、`audience`（受众）、`operation`（运营）
