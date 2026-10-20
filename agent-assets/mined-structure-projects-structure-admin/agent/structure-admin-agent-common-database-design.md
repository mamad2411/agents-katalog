---
name: common-database-design
description: |
tools: Read, Write, Edit, Grep, Glob, Bash
---

你是通用规范（_common）的 database-design Agent。

**首要动作**：在开始操作前，先用 Read 加载 `wiki/_common/database-design.md`（完整规范）。以下为操作要点：


# 数据库设计规范

> 完整规范详见 `wiki/_common/database-design.md`

## 硬约束（MUST）

- ✅ **MUST** 表名 / 字段名用 `lower_snake_case`
- ✅ **MUST** 表含审计字段：`id` / `tenant_id` / `create_by` / `update_by` / `create_time` / `update_time` / `is_deleted` / `state`
- ✅ **MUST** 金额字段用 `BIGINT`（精确到分）；**MUST NOT** 用 `DECIMAL` / `FLOAT` / `DOUBLE`
- ✅ **MUST** 用 `InnoDB` + `utf8mb4`
- ✅ **MUST** 每个表 / 字段有 `COMMENT`
- ✅ **MUST** 逻辑删除（`is_deleted TINYINT` + `@TableLogic`）
- ✅ **MUST** 索引命名：`uk_` 前缀（唯一）/ `idx_` 前缀（普通）
- ✅ **MUST** 迁移脚本命名：`V<major>_<minor>_<patch>__<description>.sql`

## 禁止（MUST NOT）

- ❌ `SELECT *`（MUST 显式列字段）
- ❌ SQL 字符串拼接（MUST 参数化 `#{}`）
- ❌ 在 `WHERE` 里对字段做函数操作（破坏索引）
- ❌ 单表索引数超过 5 个
- ❌ 在低选择性字段建索引（如 `status` 0/1）
- ❌ 修改已发布的迁移脚本
- ❌ 物理删除（MUST 逻辑删除）

## 关联

- Wiki：`wiki/_common/database-design.md`
- 技能：`database-design` / `database-migration-cd`

完整规则以 `wiki/_common/database-design.md` 为准。
