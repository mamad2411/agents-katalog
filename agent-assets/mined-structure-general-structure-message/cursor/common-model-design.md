---
description: |
  当用户要求"新建实体/设计模型/建表/加字段/Entity/PO/DTO/VO"时触发。
  覆盖模型分层（Entity/PO/DTO/VO/Query）、审计字段、命名规范、转换规范。

triggers:
  - 新建实体
  - 设计模型
  - 建表
  - 加字段
  - Entity
  - PO
  - DTO
  - VO
  - Query
  - model

priority: medium
alwaysApply: false
globs: "**/*Entity.java, **/*PO.java, **/*DTO.java, **/*VO.java, **/*Query.java, changes/**/*.md, docs/**/*.md"

category: model-design
stack: _common
role: common
maturity: complete

reads-before-action:
  - wiki/_common/model-design.md

related-skills:
  - model-design
  - database-design

when-to-use: |
  新建模型类、加字段、设计数据表、设计四层模型
when-not-to-use: |
  仅阅读现有模型
version: "0.3.0"
since: "2026-08-13"
---

# 模型设计规范

> 完整规范详见 `wiki/_common/model-design.md`

## 模型分层（MUST）

| 层 | 命名 | 位置 | 持久化注解 |
|---|---|---|---|
| **Entity** | `{X}Entity` | `domain` | ❌ 不含 |
| **PO** | `{X}PO` | `repository-mybatis` | ✅ 含 `@TableName` / `@TableId` / `@TableLogic` |
| **DTO** | `{X}DTO` | `common` | ❌ 不含 |
| **VO** | `{X}VO` | `common` | ❌ 不含 |
| **Query** | `{X}Query` | `common` | ❌ 不含 |

## 硬约束（MUST）

- ✅ **MUST** 区分 Entity / PO / DTO / VO / Query 五层模型
- ✅ **MUST** 含审计字段：`id` / `tenant_id` / `create_by` / `update_by` / `create_time` / `update_time` / `is_deleted` / `state`
- ✅ **MUST** 金额字段用 `BIGINT`（精确到分）
- ✅ **MUST** Entity 用 `@Data + @Builder + @NoArgsConstructor + @AllArgsConstructor`
- ✅ **MUST** PO 含 `@TableName` / `@TableId(type=AUTO)` / `@TableLogic`
- ✅ **MUST** Entity ↔ PO 转换在 `MybatisPlusDelegate` 显式实现 `toEntity` / `toPo`
- ✅ **MUST** 主键用 `BIGINT AUTO_INCREMENT`（除非分库分表）

## 禁止（MUST NOT）

- ❌ Entity 上加 `@TableId` / `@TableLogic` 等持久化注解
- ❌ Service / Controller 直接返回 PO 或 Entity（应用 VO）
- ❌ Service 层注入 Mapper / PO
- ❌ 跨服务直接读数据库（应用 Feign）
- ❌ 用 `Date` 类型（应用 `LocalDateTime`）

## 关联

- Wiki：`wiki/_common/model-design.md`
- 技能：`model-design` / `database-design`
