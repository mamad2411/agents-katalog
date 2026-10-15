---
name: pdf-shared
version: 1.0.0
description: "pdf-cli 共享基础：配置、认证、输出格式、错误处理，以及基于 baseURL 的主业务与 core/tools 工具链路。首次使用、处理认证问题、查看全局选项时使用。"
metadata:
  requires:
    bins: ["pdf-cli"]
  cliHelp: "pdf-cli --help"
---

# pdf-cli 共享规则

本技能指导你如何通过 pdf-cli 操作 PDF 翻译与工具资源，以及有哪些注意事项。

## 服务与配置

pdf-cli 当前主要通过 `baseURL` 访问后端服务。

| 场景 | 接口前缀 | 认证方式 |
| ------ | ------ | ------ |
| auth / translate / user / member / other | 普通业务接口 | `token` + `deviceId` + `clientType` header |
| tools | `core/tools/*` | 复用登录态，通过主服务链路调用 |

配置文件位于 `~/.config/pdf-cli/config.json`，包含 token、deviceId、baseURL、toolURL 等字段。当前 tools 命令实际使用 `baseURL` 下的 `core/tools/*` 接口。

## 认证

### 登录

```bash
pdf-cli auth login --email you@example.com
```

### 登录状态检查

```bash
pdf-cli auth status
```

### 退出登录

```bash
pdf-cli auth logout
```

### 认证规则

- 大部分命令需要先登录。
- tools 命令执行前同样应确保已登录。
- 未登录时执行需认证的命令会提示 `请先执行 pdf-cli auth login`。
- deviceId 首次使用时自动生成并持久化。

## 全局参数

| 参数 | 说明 | 默认值 |
| ------ | ------ | ------ |
| `--format <type>` | 输出格式：`json`、`table`、`pretty` | `pretty` |
| `--output <path>` | 输出到文件路径 | 终端输出 |

## 输出格式

- `pretty`: 人类可读的格式化输出。
- `json`: JSON 格式，适合程序解析。
- `table`: 表格格式，适合列表数据。

## 错误处理

### 退出码

| 退出码 | 含义 |
| ------ | ------ |
| 0 | 成功 |
| 1 | 参数错误 |
| 2 | 认证错误 |
| 3 | API 错误 |
| 4 | 网络错误 |
| 5 | 配置错误 |
| 6 | 内部错误 |

### 常见错误处理

- 未登录: 执行 `pdf-cli auth login --email xxx`。
- token 过期: 重新登录。
- 网络错误: 检查网络连接和服务地址配置。
- API 错误: 查看错误消息中的具体原因。

## tools 异步任务规则

- tools 命令会走 `core/tools/*` 的异步任务链路。
- 提交任务后使用 `queryKey` 查询状态。
- `tools job status` 与 `tools job download` 主参数是 `--query-key`。
- `--job-id` 仅保留兼容，不再作为主文档术语。
