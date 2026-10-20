---
description: |
  当用户要求"认证/授权/JWT/加密/权限/越权/SQL 注入/XSS/CSRF"时触发。
  覆盖认证授权、密码存储、加密、SQL 注入防护、XSS 防护、越权防护、敏感数据脱敏。

triggers:
  - 认证
  - 授权
  - JWT
  - 加密
  - 权限
  - 越权
  - SQL 注入
  - XSS
  - CSRF
  - security
  - 密码

priority: high
alwaysApply: false
globs: "**/*.java, **/*.ts, **/*.vue, **/application*.yaml, changes/**/*.md"

category: security
stack: _common
role: common
maturity: complete

reads-before-action:
  - wiki/_common/security.md

related-skills:
  - coding
  - expert-review

when-to-use: |
  实现认证 / 授权 / 加密 / 权限控制 / 敏感数据处理
when-not-to-use: |
  仅阅读安全代码
version: "0.3.0"
since: "2026-08-13"
---

# 安全规范

> 完整规范详见 `wiki/_common/security.md`

## 硬约束（MUST）

- ✅ **MUST** 用生态安全框架的认证 / 授权组件（具体组件见栈级规则，如 structure-boot 用 `structure-security`）
- ✅ **MUST** 密码用 BCrypt（强度 ≥ 10）
- ✅ **MUST** 全站 HTTPS
- ✅ **MUST** 用 MyBatis `#{}` 参数化（禁止 `${}` 拼接）
- ✅ **MUST** 敏感接口加权限注解 `@PreAuthorize`
- ✅ **MUST** 水平越权防护：校验当前用户是否有权访问
- ✅ **MUST** 日志脱敏（密码 / 密钥 / Token / 身份证 / 手机号）
- ✅ **MUST** 敏感字段存储加密（AES-256）
- ✅ **MUST** 密钥用环境变量 / Vault / KMS 注入（禁止硬编码）

## 禁止（MUST NOT）

- ❌ 在日志 / 异常消息打印敏感信息（密码 / 密钥 / Token）
- ❌ 在 URL 参数传递 Token / 敏感数据
- ❌ 用 MD5 / SHA1 / 明文存密码
- ❌ 在代码 / 配置文件硬编码密钥
- ❌ 用 CORS `*`（应用白名单）

## 关联

- Wiki：`wiki/_common/security.md`
- 技能：`coding` / `expert-review`
