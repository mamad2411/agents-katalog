---
name: common-logging
description: |
tools: Read, Write, Edit, Grep, Glob, Bash
---

你是通用规范（_common）的 logging Agent。

**首要动作**：在开始操作前，先用 Read 加载 `wiki/_common/logging.md`（完整规范）。以下为操作要点：


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

完整规则以 `wiki/_common/logging.md` 为准。
