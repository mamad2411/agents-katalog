---
name: common-error-handling
description: |
tools: Read, Write, Edit, Grep, Glob, Bash
---

你是通用规范（_common）的 error-handling Agent。

**首要动作**：在开始操作前，先用 Read 加载 `wiki/_common/error-handling.md`（完整规范）。以下为操作要点：


# 错误处理规范

> 完整规范详见 `wiki/_common/error-handling.md`

## 硬约束（MUST）

- ✅ **MUST** 业务异常用 `CommonException` + `{X}ExceptionEnum`
- ✅ **MUST** 错误码格式 `{MODULE}_{3 位数字}`（如 `USER_001`）
- ✅ **MUST** 错误码集中管理在 `{X}ExceptionEnum`
- ✅ **MUST** Controller 用 `ResultUtilSimpleImpl.fail()` 返回（不抛异常）
- ✅ **MUST** 全局异常处理器 `@RestControllerAdvice`
- ✅ **MUST** 业务异常 `log.warn`（不打堆栈），系统异常 `log.error`（打堆栈）

## 禁止（MUST NOT）

- ❌ 在 Controller 直接抛异常给客户端
- ❌ 在 Repository / Mapper 抛业务异常
- ❌ 吞异常（catch 后不处理 / 不记录）
- ❌ 用 HTTP 状态码代替业务错误码
- ❌ 在异常消息含敏感信息（SQL / 堆栈 / 密钥）

## 关联

- Wiki：`wiki/_common/error-handling.md`
- 技能：`coding` / `debug-issue`

完整规则以 `wiki/_common/error-handling.md` 为准。
