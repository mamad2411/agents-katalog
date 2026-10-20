---
name: common-model-design
description: |
tools: Read, Write, Edit, Grep, Glob, Bash
---

你是通用规范（_common）的 model-design Agent。

**首要动作**：在开始操作前，先用 Read 加载 `wiki/_common/model-design.md`（完整规范）。以下为操作要点：


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

完整规则以 `wiki/_common/model-design.md` 为准。
