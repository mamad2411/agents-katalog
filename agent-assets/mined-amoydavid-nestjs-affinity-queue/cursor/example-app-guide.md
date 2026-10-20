---
description: 
globs: 
alwaysApply: false
---
# 示例应用指南

## 示例应用概览
[packages/example/](mdc:packages/example) 是一个完整的示例应用，演示如何使用 nestjs-affinity-queue 插件。

## 应用结构

### 核心文件
- [packages/example/src/app.module.ts](mdc:packages/example/src/app.module.ts): 主模块，配置队列插件
- [packages/example/src/app.controller.ts](mdc:packages/example/src/app.controller.ts): API 控制器，提供任务提交接口
- [packages/example/src/app.service.ts](mdc:packages/example/src/app.service.ts): 应用服务
- [packages/example/src/task-handler.service.ts](mdc:packages/example/src/task-handler.service.ts): 任务处理器，定义具体的任务处理逻辑

### 部署配置
- [packages/example/ecosystem.config.js](mdc:packages/example/ecosystem.config.js): PM2 集群配置文件

### 测试脚本
- [packages/example/test-simple-worker.sh](mdc:packages/example/test-simple-worker.sh): 简单 Worker 测试
- [packages/example/test-parallel.sh](mdc:packages/example/test-parallel.sh): 并行处理测试
- [packages/example/test-affinity.sh](mdc:packages/example/test-affinity.sh): 亲和性测试
- [packages/example/test-worker-logs.sh](mdc:packages/example/test-worker-logs.sh): Worker 日志测试
- [packages/example/test-suite.sh](mdc:packages/example/test-suite.sh): 完整测试套件

## 快速开始

### 1. 启动应用
```bash
# 开发模式
pnpm dev:example

# 生产模式
pnpm build
cd packages/example
pnpm start:prod
```

### 2. 使用 PM2 集群部署
```bash
cd packages/example
pm2 start ecosystem.config.js
```

### 3. 测试 API
```bash
# 提交单个任务
curl -X POST http://localhost:3000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "type": "send-email",
    "identifyTag": "company-123",
    "payload": {
      "to": "user@example.com",
      "subject": "欢迎邮件"
    }
  }'

# 批量添加测试任务
curl -X POST "http://localhost:3000/tasks/batch?count=20&companies=3"

# 查看队列状态
curl http://localhost:3000/queue/stats
```

## 环境变量配置
- `APP_ROLE`: 应用角色 (SCHEDULER | WORKER | BOTH)
- `MAX_BATCH_SIZE`: Worker 最大批次大小
- `REDIS_URL`: Redis 连接地址

## 测试场景
1. **亲和性测试**: 验证相同 `identifyTag` 的任务按顺序处理
2. **并行处理**: 验证不同 `identifyTag` 的任务可以并行处理
3. **批次控制**: 验证批次大小限制功能
4. **集群部署**: 验证 PM2 集群环境下的功能
