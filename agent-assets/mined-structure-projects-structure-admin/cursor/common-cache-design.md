---
description: |
  当用户要求"用缓存/写缓存/Redis/缓存穿透/缓存击穿/缓存雪崩/分布式锁"时触发。
  覆盖缓存策略、三大问题防护、Redis 使用规范、分布式锁。

triggers:
  - 缓存
  - cache
  - redis
  - 缓存穿透
  - 缓存击穿
  - 缓存雪崩
  - 分布式锁
  - 缓存策略

priority: medium
alwaysApply: false
globs: "**/*.java, **/*.yaml, **/*.yml, changes/**/*.md"

category: cache-design
stack: _common
role: common
maturity: complete

reads-before-action:
  - wiki/_common/cache-design.md

related-skills:
  - coding
  - debug-issue

when-to-use: |
  使用 Redis 缓存、设计缓存策略、实现分布式锁
when-not-to-use: |
  仅查询缓存
version: "0.3.0"
since: "2026-08-13"
---

# 缓存设计规范

> 完整规范详见 `wiki/_common/cache-design.md`

## 硬约束（MUST）

- ✅ **MUST** 默认用 Cache-Aside 策略
- ✅ **MUST** 所有 key MUST 设 TTL（禁止 `-1` 永不过期）
- ✅ **MUST** key 命名用 `<业务>:<实体>:<id>` 格式，全小写，`:` 分隔
- ✅ **MUST** 防穿透：缓存空值 或 布隆过滤器
- ✅ **MUST** 防击穿：互斥锁（SETNX）或 逻辑过期
- ✅ **MUST** 防雪崩：TTL 加随机值
- ✅ **MUST** 用生态封装的缓存 / Redis 模板（具体类名见栈级规则，如 structure-boot 用 `DataScopeRedisTemplate`）
- ✅ **MUST** 分布式锁：SET NX EX + UUID value + Lua 释放

## 禁止（MUST NOT）

- ❌ 裸用 `RedisTemplate` / `CacheManager`
- ❌ 用 `SETNX` + `EXPIRE` 两条命令做分布式锁（非原子）
- ❌ 在缓存层存放生产 Secrets
- ❌ 先删缓存再写 DB（应先写 DB 再删缓存）

## 关联

- Wiki：`wiki/_common/cache-design.md`
- 技能：`coding` / `debug-issue`
