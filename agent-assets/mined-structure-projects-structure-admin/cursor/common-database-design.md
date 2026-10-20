---
description: |
  当用户要求"设计表/加字段/写迁移/改表结构/设计索引"时触发。
  覆盖数据库表设计、索引策略、SQL 规范、Flyway 迁移。

triggers:
  - 设计表
  - 加字段
  - 写迁移
  - 改表结构
  - 设计索引
  - table
  - schema
  - migration
  - 索引
  - DDL
  - Flyway

priority: medium
alwaysApply: false
globs: "**/db/migration/**/*.sql, **/*Mapper.java, **/*Mapper.xml, changes/**/*.md"

category: database-design
stack: _common
role: common
maturity: complete

reads-before-action:
  - wiki/_common/database-design.md

related-skills:
  - database-design
  - model-design

when-to-use: |
  新建数据表、修改表结构、添加索引、编写迁移脚本
when-not-to-use: |
  仅查询数据
version: "0.3.0"
since: "2026-08-13"
---

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
