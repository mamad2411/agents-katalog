---
description: 
globs: 
alwaysApply: false
---
# API 参考指南

## 核心 API

### QueueModule
主模块，提供队列功能的入口。

```typescript
import { QueueModule } from 'nestjs-affinity-queue';

@Module({
  imports: [
    QueueModule.forRoot({
      role: 'BOTH', // SCHEDULER | WORKER | BOTH
      workerOptions: {
        maxBatchSize: 5,
      },
      redisOptions: {
        url: 'redis://localhost:6379',
      },
    }),
  ],
})
export class AppModule {}
```

### QueueService
队列服务，提供任务提交接口。

```typescript
import { QueueService, Task } from 'nestjs-affinity-queue';

@Injectable()
export class MyService {
  constructor(private readonly queueService: QueueService) {}

  async addTask(task: Task): Promise<Job> {
    return this.queueService.add(task);
  }
}
```

### Task 接口
任务对象定义。

```typescript
interface Task {
  type: string;           // 任务类型
  identifyTag: string;    // 身份标识
  payload: any;          // 任务数据
}
```

### WorkerState 接口
Worker 状态定义。

```typescript
interface WorkerState {
  workerId: string;                    // Worker ID
  status: 'idle' | 'running';         // 状态
  currentIdentifyTag: string | null;   // 当前处理的标识
  currentBatchSize: number;           // 当前批次大小
}
```

## 配置选项

### QueueModuleOptions
```typescript
interface QueueModuleOptions {
  role: 'SCHEDULER' | 'WORKER' | 'BOTH';
  workerOptions?: {
    maxBatchSize?: number;
    workerId?: string;
  };
  redisOptions?: {
    url?: string;
    host?: string;
    port?: number;
    password?: string;
  };
  queueOptions?: {
    pendingQueueName?: string;
    workerQueuePrefix?: string;
  };
}
```

## 环境变量

### 必需环境变量
- `APP_ROLE`: 应用角色 (SCHEDULER | WORKER | BOTH)

### 可选环境变量
- `MAX_BATCH_SIZE`: Worker 最大批次大小 (默认: 5)
- `REDIS_URL`: Redis 连接地址 (默认: redis://localhost:6379)
- `WORKER_ID`: Worker ID (默认: 自动生成)

## 任务处理器

### 自定义任务处理器
```typescript
import { WorkerService } from 'nestjs-affinity-queue';

@Injectable()
export class MyTaskHandler implements OnModuleInit {
  constructor(private readonly workerService: WorkerService) {}

  async onModuleInit() {
    // 注册任务处理器
    this.workerService.registerHandler('send-email', this.handleSendEmail.bind(this));
    this.workerService.registerHandler('generate-report', this.handleGenerateReport.bind(this));
  }

  async handleSendEmail(payload: any): Promise<void> {
    // 处理发送邮件任务
    console.log('发送邮件:', payload);
  }

  async handleGenerateReport(payload: any): Promise<void> {
    // 处理生成报告任务
    console.log('生成报告:', payload);
  }
}
```

## 监控 API

### 队列状态
```typescript
// 获取队列统计信息
const stats = await queueService.getStats();

// 获取 Worker 状态
const workerStates = await queueService.getWorkerStates();

// 获取待处理任务数量
const pendingCount = await queueService.getPendingCount();
```

## 错误处理

### 任务失败处理
```typescript
// 任务处理器中的错误处理
async handleTask(payload: any): Promise<void> {
  try {
    // 任务处理逻辑
    await this.processTask(payload);
  } catch (error) {
    // 记录错误日志
    this.logger.error('任务处理失败', error);
    
    // 可以选择重新抛出错误以触发重试
    throw error;
  }
}
```

## 部署配置

### PM2 配置示例
```javascript
// ecosystem.config.js
module.exports = {
  apps: [
    {
      name: 'app-scheduler',
      script: 'dist/main.js',
      instances: 1,
      exec_mode: 'fork',
      env: {
        NODE_ENV: 'production',
        APP_ROLE: 'SCHEDULER',
      },
    },
    {
      name: 'app-workers',
      script: 'dist/main.js',
      instances: -1,
      exec_mode: 'cluster',
      env: {
        NODE_ENV: 'production',
        APP_ROLE: 'WORKER',
        MAX_BATCH_SIZE: 10,
      },
    },
  ],
};
```

## 最佳实践

### 任务设计
1. 使用有意义的任务类型名称
2. 合理设计 `identifyTag` 以支持亲和性
3. 保持任务数据简洁

### 性能优化
1. 合理设置 `maxBatchSize`
2. 监控队列长度和 Worker 状态
3. 及时处理失败任务

### 错误处理
1. 在任务处理器中捕获异常
2. 记录详细的错误日志
3. 实现适当的重试机制
