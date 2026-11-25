---
name: notion-mcp-wrapper
description: Notion MCP Server wrapper with health check, auto-reconnect, and fallback
author: Galatea
version: "1.0.0"
openclaw_version: ">=2026.2.0"
---

# notion-mcp-wrapper

为 Notion MCP Server 提供健康检查、自动重连和降级功能的 wrapper。

## 功能特性

- ✅ **健康检查** - 定期检测 MCP server 连接状态
- ✅ **自动重连** - 指数退避策略自动恢复连接
- ✅ **无缝降级** - MCP 失败时自动切换到备用方案
- ✅ **CLI 工具** - 命令行快速诊断和操作

## 安装

```bash
cd ~/.openclaw/workspace/skills/notion-mcp-wrapper
npm install
```

## 使用方法

### 作为 Library 使用

```javascript
const { NotionMCPWrapper } = require('./lib/notion-mcp-wrapper');

const wrapper = new NotionMCPWrapper({
  maxRetries: 5,
  baseDelayMs: 1000
});

// 启动 wrapper
await wrapper.start();

// 执行操作（自动处理失败和降级）
const result = await wrapper.execute('query', { databaseId: 'xxx' });
console.log(result.source); // 'mcp' 或 'fallback'

// 停止 wrapper
await wrapper.stop();
```

### CLI 使用

```bash
# 检查 MCP server 健康状态
npm run health
# 或
node bin/notion-mcp-wrapper health

# 启动 wrapper
npm run start
# 或
node bin/notion-mcp-wrapper start

# 运行集成测试
node bin/notion-mcp-wrapper test
```

### 组件独立使用

```javascript
const { HealthChecker, Reconnector } = require('./lib/notion-mcp-wrapper');

// 仅健康检查
const checker = new HealthChecker();
const health = await checker.checkHealth();
console.log(health.status); // 'healthy' 或 'unhealthy'

// 仅重连逻辑
const reconnector = new Reconnector({ maxRetries: 5 });
const result = await reconnector.reconnect(async () => {
  // 你的重连逻辑
});
```

## 架构

```
┌─────────────────────────────────┐
│     NotionMCPWrapper            │
├─────────────────────────────────┤
│  ┌─────────────┐                │
│  │ HealthChecker│ → 定时 ping   │
│  └─────────────┘                │
│  ┌─────────────┐                │
│  │ Reconnector │ → 指数退避     │
│  └─────────────┘                │
│  ┌─────────────┐                │
│  │ FallbackMgr │ → 自动降级     │
│  └─────────────┘                │
└─────────────────────────────────┘
```

## API 文档

### NotionMCPWrapper

| 方法 | 签名 | 说明 |
|------|------|------|
| `start()` | `() => Promise<{success}>` | 启动 wrapper，自动重连 |
| `execute(operation, params)` | `(string, object) => Promise<result>` | 执行操作，自动降级 |
| `stop()` | `() => Promise<void>` | 停止 wrapper |

### HealthChecker

| 方法 | 签名 | 说明 |
|------|------|------|
| `checkHealth()` | `() => Promise<{status, latency}>` | 检查健康状态 |
| `isHealthy()` | `() => Promise<boolean>` | 快速健康判断 |

### Reconnector

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `maxRetries` | number | 5 | 最大重试次数 |
| `baseDelayMs` | number | 1000 | 基础延迟（毫秒）|
| `maxDelayMs` | number | 30000 | 最大延迟（毫秒）|

## 测试

```bash
npm test
```

测试覆盖率：
- HealthChecker: ✅
- Reconnector: ✅
- FallbackManager: ✅

## 最佳实践

1. **监控集成** - 配合 cron job 定期健康检查
2. **日志记录** - wrapper 会自动输出状态日志
3. **降级策略** - 确保 fallback 方案已配置

## 故障排查

| 问题 | 解决方案 |
|------|----------|
| MCP 连接失败 | 检查 `NOTION_API_KEY` 环境变量 |
| 重连循环 | 增加 `baseDelayMs` 或检查网络 |
| 降级不生效 | 确认 fallback 方法已实现 |

## License

MIT

## Changelog

### v1.0.0
- 初始版本
- 健康检查、自动重连、降级功能
- CLI 工具支持
