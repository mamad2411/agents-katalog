---
name: common-concurrency
description: |
tools: Read, Write, Edit, Grep, Glob, Bash
---

你是通用规范（_common）的 concurrency Agent。

**首要动作**：在开始操作前，先用 Read 加载 `wiki/_common/concurrency.md`（完整规范）。以下为操作要点：


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

完整规则以 `wiki/_common/concurrency.md` 为准。
