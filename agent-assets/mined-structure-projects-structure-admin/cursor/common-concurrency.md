---
description: |
  当用户要求"并发/线程池/异步/锁/线程安全"时触发。
  覆盖共享可变状态、线程池配置、异步处理、幂等设计、并发集合、锁。

triggers:
  - 并发
  - 线程池
  - 异步
  - 锁
  - 线程安全
  - concurrency
  - thread
  - async
  - synchronized

priority: medium
alwaysApply: false
globs: "**/*.java, changes/**/*.md"

category: concurrency
stack: _common
role: common
maturity: complete

reads-before-action:
  - wiki/_common/concurrency.md

related-skills:
  - coding
  - debug-issue

when-to-use: |
  使用多线程、异步处理、并发设计
when-not-to-use: |
  仅单线程操作
version: "0.3.0"
since: "2026-08-13"
---

# 并发编程规范

> 完整规范详见 `wiki/_common/concurrency.md`

## 硬约束（MUST）

- ✅ **MUST** 用线程池（禁止 `new Thread()`）
- ✅ **MUST** 线程池设合理 core / max / queue + 线程名前缀 + 拒绝策略
- ✅ **MUST** 用有界队列（不用无界 LinkedBlockingQueue 默认值）
- ✅ **MUST** 共享计数用 `AtomicInteger` / `LongAdder`
- ✅ **MUST** 并发集合用 `ConcurrentHashMap` / `CopyOnWriteArrayList`
- ✅ **MUST** 并发场景幂等（数据库唯一约束 / Redis SETNX / Idempotency-Key）

## 禁止（MUST NOT）

- ❌ 在单例 Bean 中用可变实例字段
- ❌ 用 `static` 可变字段共享状态
- ❌ 在 Controller / Service 用成员变量存请求级状态
- ❌ 在 `@Transactional` 方法内调用 `@Async`（事务失效）

## 关联

- Wiki：`wiki/_common/concurrency.md`
- 技能：`coding` / `debug-issue`
