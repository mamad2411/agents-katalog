---
name: fastevent
description: FastEvent 事件发射器库使用指南。功能强大、类型安全的事件系统，支持层级事件、通配符、执行器、管道、钩子、异步迭代器等高级特性。
---

# FastEvent 技能

功能强大、类型安全的事件发射器库，支持 Node.js 和浏览器环境。

## 快速开始

```typescript
import { FastEvent } from "fastevent";
const events = new FastEvent();

// 订阅事件
events.on("user/login", (message) => {
  console.log(message.payload); // { id: 1 }
});

// 发布事件
events.emit("user/login", { id: 1 });
```

## 核心概念

### 事件消息结构

默认情况下消息结构如下：

```typescript
{
    type: string,      // 事件名称（支持层级）
    payload: any,      // 事件数据
    meta: object       // 元数据（version, timestamp, domain 等）
}
```

### 层级事件与通配符

- `user/*` - 单级匹配（如 `user/login`, `user/logout`）
- `user/**` - 多级匹配（如 `user/profile/update`, `user/settings/theme/change`）,\*\*只能用于未尾
- 支持作用域（Scope）自动添加前缀

### 执行器（Executors）

- `parallel()` - 并行执行（默认）
- `series()` - 串行执行
- `race()` - 竞速，返回最快结果
- `waterfall()` - 瀑布流，结果传递
- `first/last/random/balance()` - 其他策略

### 管道（Pipes）

- `queue()` - 队列处理
- `throttle()` - 节流
- `debounce()` - 防抖
- `timeout()` - 超时
- `retry()` - 重试
- `memorize()` - 缓存

### 高级特性

- **异步迭代器**：`for await (const msg of events.on('event'))`
- **钩子系统**：`onAddBeforeListener`,`onAddAfterListener`, `onBeforeExecuteListener`, `onListenerError` 等
- **继承**：可继承 `FastEvent` 和 `FastEventScope`
- **上下文控制**：自定义监听器的 `this` 指向
- **AbortSignal**：中止异步监听器执行
- **元数据**：多层级元数据合并
- **消息转换**：对监听器接收到的事件消息进行转换，让监听器接收到自定义格式的消息

## 类型安全

```typescript
interface MyEvents {
  "user/login": { id: number };
  "data/update": { value: string };
}
const events = new FastEvent<MyEvents>();
```

## 常用操作

```typescript
// 等待事件
await events.waitFor("user/login", 5000);

// 一次性监听
events.once("startup", handler);

// 移除监听器
const subscriber = events.on("event", handler);
subscriber.off();

// 全局监听
events.onAny((message) => console.log(message.type));

// 作用域
const userScope = events.scope("user");

// 保留事件
events.emit("config/theme", { dark: true }, { retain: true });
// 等待某个事件的触发
await events.waitFor("login");

// 清除所有监听器
events.offAll();
```

## 详细文档

- `references/advanced-patterns.md` - 高级模式（钩子、继承、异步迭代器等）
- `references/executors.md` - 执行器详解
- `references/pipes.md` - 管道详解
- `references/testing.md` - 测试指南
- `references/transform.md` - 对监听器接收到的事件消息进行转换
- `references/index.d.ts` - 类型参考
