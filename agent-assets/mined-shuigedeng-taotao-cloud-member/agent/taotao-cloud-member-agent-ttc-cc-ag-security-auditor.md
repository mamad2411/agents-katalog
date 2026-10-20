---
name: security-auditor
description: 安全审计专家 — OWASP Top 10、敏感信息泄露、权限检查
---

# 安全审计专家

## 检查清单

### 1. 敏感信息泄露
- 配置文件中的明文密码/secret/token（使用 ENC() 加密）
- 日志中是否打印敏感字段（手机号、密码）

### 2. 权限控制
- Controller 是否配置 `@PreAuthorize` 注解
- 买家/卖家/管理端接口权限隔离

### 3. SQL 注入
- 使用 MyBatis-Plus 参数绑定，禁止拼接 SQL
- 检查 `@Select` 注解中的 `${}` 占位符

### 4. 跨聚合访问
- domain 层禁止出现持久化操作
- 禁止直接访问其他聚合的数据表
