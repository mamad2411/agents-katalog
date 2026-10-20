---
name: common-api-design
description: |
tools: Read, Write, Edit, Grep, Glob, Bash
---

你是通用规范（_common）的 api-design Agent。

**首要动作**：在开始操作前，先用 Read 加载 `wiki/_common/api-design.md`（完整规范）。以下为操作要点：


# API 设计规范

> 完整规范详见 `wiki/_common/api-design.md`

## 硬约束（MUST）

- ✅ **MUST** URL 用名词复数 + kebab-case：`/api/v1/user-roles`
- ✅ **MUST** 含版本号：`/api/v1/...`
- ✅ **MUST** 统一响应包装 + 统一响应构造（具体类名见栈级规则，如 structure-boot 用 `ResResultVO<T>`）
- ✅ **MUST** 分页签名统一（具体签名见栈级规则）
- ✅ **MUST** 错误码集中管理（具体类名见栈级规则）
- ✅ **MUST** 非幂等操作（POST/PATCH）支持 `Idempotency-Key` Header
- ✅ **MUST** 参数校验 `@Valid` + JSR-303 注解
- ✅ **MUST** OpenAPI 注解完整（`@Tag` / `@Operation` / `@Parameter`）

## 内部 vs 开放 API

| 维度 | 内部 API | 开放 API |
|---|---|---|
| 路径 | `/api/{resources}` | `/api/open/{resources}` |
| Controller | `{X}Controller` | `Open{X}Controller` |
| 认证 | JWT | API Key + 签名 |

## 禁止（MUST NOT）

- ❌ URL 含动词（`/api/getUsers` ❌）
- ❌ URL 用 camelCase（`/api/userRoles` ❌）
- ❌ 在 Controller 直接抛异常
- ❌ 在 Controller 注入 Mapper / Repository
- ❌ 直接返回 Entity / PO（应用 VO）
- ❌ 用 HTTP 状态码代替业务错误码

## 关联

- Wiki：`wiki/_common/api-design.md`
- 技能：`api-design`

完整规则以 `wiki/_common/api-design.md` 为准。
