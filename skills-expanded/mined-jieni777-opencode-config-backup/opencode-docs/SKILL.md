---
name: opencode-docs
description: "OpenCode官方技术支持文档技能 - 提供配置、MCP服务器、插件、工具等完整文档"
trigger_keywords: "OpenCode文档、配置帮助、MCP服务器、插件使用、工具配置、技术支持"
auto_activate: true
priority: 5
---

# OpenCode 官方文档技能

## 直接触发指令

当用户请求以下内容时自动激活此技能：
- "OpenCode配置帮助"
- "MCP服务器配置"
- "插件使用方法"
- "工具配置指导"
- "技术支持文档"

## 文档概述

本技能提供 OpenCode 官方文档的完整知识，包括配置、MCP服务器、插件、工具等各个方面。

## 核心文档内容

### 1. 配置格式 (Config)

OpenCode 支持 JSON 和 JSONC (JSON with Comments) 格式：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "theme": "opencode",
  "model": "anthropic/claude-sonnet-4-5",
  "autoupdate": true
}
```

**配置加载顺序**：
1. 远程配置 (.well-known/opencode) - 组织默认值
2. 全局配置 (~/.config/opencode/opencode.json) - 用户偏好
3. 项目配置 (opencode.json) - 项目特定设置

### 2. MCP 服务器 (MCP Servers)

**本地 MCP 服务器配置**：
```json
{
  "mcp": {
    "my-local-mcp": {
      "type": "local",
      "command": ["npx", "-y", "my-mcp-command"],
      "enabled": true
    }
  }
}
```

**远程 MCP 服务器配置**：
```json
{
  "mcp": {
    "my-remote-mcp": {
      "type": "remote",
      "url": "https://my-mcp-server.com",
      "headers": {
        "Authorization": "Bearer MY_API_KEY"
      }
    }
  }
}
```

### 3. 插件系统 (Plugins)

**插件配置**：
```json
{
  "plugin": ["opencode-helicone-session", "opencode-wakatime"]
}
```

**插件加载位置**：
- 全局插件：`~/.config/opencode/plugins/`
- 项目插件：`.opencode/plugins/`

### 4. 工具管理 (Tools)

**禁用工具**：
```json
{
  "tools": {
    "write": false,
    "bash": false
  }
}
```

**权限控制**：
```json
{
  "permission": {
    "edit": "ask",
    "bash": "ask"
  }
}
```

### 5. 模型配置 (Models)

**模型设置**：
```json
{
  "model": "anthropic/claude-sonnet-4-5",
  "small_model": "anthropic/claude-haiku-4-5"
}
```

**提供商选项**：
```json
{
  "provider": {
    "anthropic": {
      "options": {
        "timeout": 600000,
        "setCacheKey": true
      }
    }
  }
}
```

### 6. 环境变量替换

```json
{
  "model": "{env:OPENCODE_MODEL}",
  "provider": {
    "anthropic": {
      "options": {
        "apiKey": "{file:~/.secrets/anthropic-key}"
      }
    }
  }
}
```

## 常见配置示例

### 完整配置示例

```json
{
  "$schema": "https://opencode.ai/config.json",
  "theme": "opencode",
  "model": "anthropic/claude-sonnet-4-5",
  "small_model": "anthropic/claude-haiku-4-5",
  "autoupdate": true,
  "mcp": {
    "my-mcp": {
      "type": "local",
      "command": ["npx", "-y", "my-mcp-command"],
      "enabled": true
    }
  },
  "plugin": ["opencode-mem"],
  "tools": {
    "write": true,
    "bash": true
  },
  "permission": {
    "edit": "allow",
    "bash": "ask"
  }
}
```

### 插件开发示例

```javascript
// .opencode/plugins/my-plugin.js
export const MyPlugin = async ({ project, client, $, directory, worktree }) => {
  return {
    "tool.execute.before": async (input, output) => {
      if (input.tool === "read" && output.args.filePath.includes(".env")) {
        throw new Error("Do not read .env files")
      }
    },
  }
}
```

## 故障排除

### 配置验证

- 使用 `$schema` 进行自动验证
- 检查 JSON 语法正确性
- 验证路径和环境变量

### MCP 服务器问题

**常见错误**：
- 命令路径错误
- 依赖缺失
- 端口冲突

**解决方案**：
```bash
# 检查 MCP 服务器状态
opencode mcp list

# 调试特定服务器
opencode mcp debug my-mcp
```

### 插件问题

**安装失败**：
- 检查网络连接
- 验证包名正确
- 查看日志文件

```bash
# 查看插件日志
ls ~/.cache/opencode/logs/
```

## 最佳实践

### 配置管理

1. **全局配置**：用户级偏好设置
2. **项目配置**：项目特定需求
3. **环境变量**：敏感信息分离

### 安全性

- 使用环境变量存储 API 密钥
- 设置适当的权限控制
- 定期审查配置

### 性能优化

- 禁用不需要的工具
- 合理设置超时时间
- 使用压缩功能

## 资源链接

- **官方文档**: https://opencode.ai/docs/
- **GitHub**: https://github.com/anomalyco/opencode
- **Discord**: https://opencode.ai/discord
- **配置架构**: https://opencode.ai/config.json

## 快速参考

### 配置优先级
1. 远程配置 (最低优先级)
2. 全局配置
3. 项目配置 (最高优先级)

### 工具调用格式
```
use the tool-name tool with arg1: "value1" and arg2: "value2"
```

### 插件开发
- 使用 TypeScript 获得类型安全
- 遵循事件驱动架构
- 提供清晰的错误处理