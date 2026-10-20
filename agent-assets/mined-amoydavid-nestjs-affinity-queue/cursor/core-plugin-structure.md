---
description: 
globs: 
alwaysApply: false
---
# 核心插件包结构

## 插件包概览
[packages/nestjs-affinity-queue/](mdc:packages/nestjs-affinity-queue) 是核心插件包，提供完整的亲和队列功能。

## 目录结构

### 入口文件
- [packages/nestjs-affinity-queue/src/index.ts](mdc:packages/nestjs-affinity-queue/src/index.ts): 插件的主入口，导出所有公共 API

### 核心模块
- [packages/nestjs-affinity-queue/src/queue.module.ts](mdc:packages/nestjs-affinity-queue/src/queue.module.ts): 主模块，整合调度器和 Worker
- [packages/nestjs-affinity-queue/src/queue.service.ts](mdc:packages/nestjs-affinity-queue/src/queue.service.ts): 队列服务，提供任务提交接口

### 调度器模块
- [packages/nestjs-affinity-queue/src/scheduler/scheduler.module.ts](mdc:packages/nestjs-affinity-queue/src/scheduler/scheduler.module.ts): 调度器模块
- [packages/nestjs-affinity-queue/src/scheduler/scheduler.processor.ts](mdc:packages/nestjs-affinity-queue/src/scheduler/scheduler.processor.ts): 调度处理器，实现核心调度算法

### Worker 模块
- [packages/nestjs-affinity-queue/src/worker/worker.module.ts](mdc:packages/nestjs-affinity-queue/src/worker/worker.module.ts): Worker 模块
- [packages/nestjs-affinity-queue/src/worker/worker.processor.ts](mdc:packages/nestjs-affinity-queue/src/worker/worker.processor.ts): Worker 处理器，执行具体任务
- [packages/nestjs-affinity-queue/src/worker/worker.service.ts](mdc:packages/nestjs-affinity-queue/src/worker/worker.service.ts): Worker 服务，管理 Worker 状态
- [packages/nestjs-affinity-queue/src/worker/worker.manager.ts](mdc:packages/nestjs-affinity-queue/src/worker/worker.manager.ts): Worker 管理器
- [packages/nestjs-affinity-queue/src/worker/worker.factory.ts](mdc:packages/nestjs-affinity-queue/src/worker/worker.factory.ts): Worker 工厂

### 配置模块
- [packages/nestjs-affinity-queue/src/config/config.ts](mdc:packages/nestjs-affinity-queue/src/config/config.ts): 配置管理
- [packages/nestjs-affinity-queue/src/config/config.schema.ts](mdc:packages/nestjs-affinity-queue/src/config/config.schema.ts): 配置模式验证

### 通用接口和 DTO
- [packages/nestjs-affinity-queue/src/common/interfaces/task.interface.ts](mdc:packages/nestjs-affinity-queue/src/common/interfaces/task.interface.ts): 任务接口定义
- [packages/nestjs-affinity-queue/src/common/interfaces/worker-state.interface.ts](mdc:packages/nestjs-affinity-queue/src/common/interfaces/worker-state.interface.ts): Worker 状态接口
- [packages/nestjs-affinity-queue/src/common/dtos/task.dto.ts](mdc:packages/nestjs-affinity-queue/src/common/dtos/task.dto.ts): 任务 DTO

## 使用方式
```typescript
import { QueueModule } from 'nestjs-affinity-queue';

@Module({
  imports: [
    QueueModule.forRoot({
      role: 'BOTH', // SCHEDULER | WORKER | BOTH
      workerOptions: {
        maxBatchSize: 5,
      },
    }),
  ],
})
export class AppModule {}
```
