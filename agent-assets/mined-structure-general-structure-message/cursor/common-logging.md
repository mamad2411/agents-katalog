---
description: |
  当用户要求"写日志/加日志/日志规范/打日志"时触发。
  覆盖日志级别、MDC traceId、脱敏、日志格式。

triggers:
  - 写日志
  - 加日志
  - 日志规范
  - 打日志
  - log
  - logging
  - 日志

priority: medium
alwaysApply: false
globs: "**/*.java, **/*.ts, **/*.vue, **/application*.yaml, **/logback*.xml"

category: logging
stack: _common
role: common
maturity: complete

reads-before-action:
  - wiki/_common/logging.md
  - wiki/_common/observability.md

related-skills:
  - coding
  - monitoring-setup

when-to-use: |
  编写日志代码、配置日志框架
when-not-to-use: |
  仅查看日志
version: "0.3.0"
since: "2026-08-13"
---

# 日志规范

> 完整规范详见 `wiki/_common/logging.md` + `wiki/_common/observability.md`

## 硬约束（MUST）

- ✅ **MUST** 用 slf4j（`log.info` / `log.warn` / `log.error`）
- ✅ **MUST** 关键流程含 `traceId`（用 MDC）
- ✅ **MUST** 业务异常 `log.warn`（不打堆栈）
- ✅ **MUST** 系统异常 `log.error`（打堆栈）
- ✅ **MUST** 日志脱敏（密码 / 密钥 / Token / 身份证 / 手机号）

## 禁止（MUST NOT）

- ❌ 用 `System.out.println`
- ❌ 用 `printStackTrace()`
- ❌ 打印敏感信息
- ❌ 在循环里打日志（影响性能）

## 关联

- Wiki：`wiki/_common/logging.md` `wiki/_common/observability.md`
- 技能：`coding` / `monitoring-setup`
