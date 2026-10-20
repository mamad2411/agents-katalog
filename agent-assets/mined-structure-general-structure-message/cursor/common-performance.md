---
description: |
  当用户要求"性能优化/慢查询/N+1/JVM 调优/GC"时触发。
  覆盖性能优化原则、常见性能问题、JVM 调优、SQL 优化、监控指标。

triggers:
  - 性能优化
  - 慢查询
  - N+1
  - JVM
  - GC
  - 性能
  - performance
  - 接口太慢
  - 系统太慢

priority: medium
alwaysApply: false
globs: "**/*.java, **/*.sql, changes/**/*.md"

category: performance
stack: _common
role: common
maturity: complete

reads-before-action:
  - wiki/_common/performance.md

related-skills:
  - performance-tuning
  - performance-testing
  - debug-issue

when-to-use: |
  性能调优、慢查询优化、JVM 调优
when-not-to-use: |
  仅功能开发
version: "0.3.0"
since: "2026-08-13"
---

# 性能优化规范

> 完整规范详见 `wiki/_common/performance.md`

## 硬约束（MUST）

- ✅ **MUST** 先测量，后优化（不优化未测量的代码）
- ✅ **MUST** 高频查询字段有索引
- ✅ **MUST** 大表分页用主键范围（不用 OFFSET）
- ✅ **MUST** 批量操作（不循环单条插入）
- ✅ **MUST** 关键指标有监控（响应时间 / QPS / 错误率 / CPU / 内存）

## 禁止（MUST NOT）

- ❌ N+1 查询
- ❌ `SELECT *`
- ❌ 在 WHERE 里对字段做函数操作
- ❌ 在低选择性字段建索引

## 关联

- Wiki：`wiki/_common/performance.md` `wiki/_common/cache-design.md`
- 技能：`performance-tuning` / `performance-testing` / `debug-issue`
