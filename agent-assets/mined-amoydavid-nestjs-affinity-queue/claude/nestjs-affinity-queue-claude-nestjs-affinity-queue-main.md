# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个 NestJS 队列插件工作空间，实现基于身份标识的强制亲和性调度的分布式任务处理系统。核心特性是确保相同 `identifyTag` 的任务按顺序在同一个 Worker 中处理，避免并发冲突。

## 架构设计

### 三层架构
1. **应用接口层 (QueueService)**: 统一入口，负责任务提交
2. **调度节点 (Scheduler)**: 中央调度器，监听待调度队列，根据亲和性算法分配任务
3. **工作节点 (Workers)**: 执行具体业务逻辑，从专属执行队列消费任务

### 核心概念
- **identifyTag**: 任务分组的身份标识 (如企业ID、用户ID)
- **强制亲和性**: 相同 identifyTag 的任务必须在同一个 Worker 中按顺序处理
- **批次控制**: 通过 maxBatchSize 防止单一身份垄断资源

## 工作空间结构

```
packages/
├── nestjs-affinity-queue/    # 核心插件包 (发布到 NPM)
│   ├── src/
│   │   ├── common/           # 通用接口、DTO、工具
│   │   ├── config/           # 配置模块
│   │   ├── scheduler/        # 调度器实现 (选举机制 + 处理器)
│   │   ├── worker/           # 工作节点实现
│   │   ├── queue.module.ts   # 模块入口
│   │   ├── queue.service.ts  # 任务提交服务
│   │   └── index.ts          # 公共 API 导出
│   └── package.json
└── example/                  # 示例应用
    ├── src/
    ├── ecosystem.config.js   # PM2 集群配置
    └── test-*.sh            # 各种测试脚本
```

## 常用开发命令

### 工作空间级别 (根目录)
```bash
# 安装依赖
pnpm install

# 构建所有包
pnpm build

# 测试所有包  
pnpm test

# 代码检查
pnpm lint

# 格式化代码
pnpm format

# 启动示例应用开发模式
pnpm dev:example

# 构建核心插件
pnpm build:plugin
```

### 核心插件开发 (packages/nestjs-affinity-queue/)
```bash
# 构建
pnpm build

# 监听构建
pnpm build:watch

# 测试
pnpm test

# 监听测试
pnpm test:watch

# 代码检查
pnpm lint
```

### 示例应用 (packages/example/)
```bash
# 开发模式
pnpm dev

# 生产构建
pnpm build

# 启动生产版本
pnpm start:prod

# 测试
pnpm test
```

## 部署和测试

### Redis 依赖
系统需要 Redis 作为消息队列和状态存储：
```bash
# Docker 启动 Redis
docker run -d -p 6379:6379 redis:7-alpine

# 或本地 Redis
redis-server
```

### PM2 集群部署
```bash
# 构建应用
pnpm build

# 启动集群 (1个调度器 + N个Worker)
cd packages/example
pm2 start ecosystem.config.js

# 查看状态
pm2 status
pm2 logs
```

### 测试脚本
example 目录包含多个测试脚本：
- `test-affinity.sh` - 亲和性调度测试
- `test-multi-queue.sh` - 多队列测试
- `test-election.sh` - 选举机制测试
- `test-suite.sh` - 完整测试套件

## 配置系统

### 环境变量
- `APP_ROLE`: 'SCHEDULER' | 'WORKER' | 'BOTH'
- `REDIS_URL`: Redis 连接地址
- `MAX_BATCH_SIZE`: Worker 批次大小限制
- `SCHEDULER_INTERVAL`: 调度器轮询间隔

### 模块配置
QueueModule 支持三种配置方式：
1. `forRoot(options)` - 同步配置，全局单例
2. `forRootAsync(options)` - 异步配置，支持依赖注入
3. `forFeature(options)` - 特性配置，支持多实例

## 技术栈

- **框架**: NestJS 10+
- **队列**: BullMQ + Redis
- **类型**: TypeScript 5+
- **包管理**: pnpm 8+
- **进程管理**: PM2
- **测试**: Jest

## 核心服务

### QueueService
任务提交的统一入口，提供 `add(task)` 方法将任务推送到待调度队列。

### SchedulerProcessor  
调度器核心逻辑，实现强制亲和性算法：
1. 检查是否有 Worker 正在处理相同 identifyTag
2. 如有且批次未满，分配给该 Worker
3. 如无，分配给空闲 Worker
4. 否则保持等待

### WorkerService
工作节点管理，负责：
- 监听专属执行队列
- 根据任务类型路由到处理器
- 批次完成后自动解除绑定

### SchedulerElectionService
分布式选举机制，确保集群中只有一个调度器实例运行。

## 开发注意事项

1. **状态管理**: 所有 Worker 状态存储在 Redis 中，支持跨进程访问
2. **选举机制**: 使用分布式锁实现调度器选举，防止脑裂
3. **错误处理**: 任务失败会保留在队列中，支持重试
4. **性能优化**: 调度器使用非阻塞轮询，避免队头阻塞
5. **批次控制**: maxBatchSize 防止单一身份长期占用资源