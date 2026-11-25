---
name: db-design
description: 当需要基于 API 设计和需求文档，设计数据库 Schema（实体、关系、索引、迁移策略）时使用
---

# 数据库设计

## 概述

基于 API 设计和需求文档设计数据库 Schema，产出后端开发可直接消费的 `db-schema.md`。这一步只做设计决策，不写代码。

**核心原则：** 从接口契约反推实体，从查询场景反推索引。不做"全量建表再看用不用"的设计。

## 适用场景

**必须使用：**

- 新模块需要创建数据库表
- 已有模块需要新增或修改表结构
- API 设计中引用了尚未存在的实体
- 需要设计表之间的关系和索引

**例外情况（需征询开发者）：**

- 只是查询已有表，不涉及 Schema 变更
- 使用第三方服务存储，不涉及本地数据库
- 数据库设计由 DBA 团队独立负责

## 铁律

```text
EVERY ENTITY MUST TRACE BACK TO AN API OR REQUIREMENT - NO SPECULATIVE TABLES
```

硬约束：

- 每个实体必须能映射到至少一个 API 或 REQ
- 每个索引必须有明确的查询场景支撑
- 字段类型选择必须考虑接口响应类型的对应关系
- 字段命名必须与项目既有的命名约定一致

## 违反后果

如果 `db-schema.md` 不存在、实体与 API 设计不一致，或索引没有查询场景支撑，当前数据库设计视为未完成；`module-dev` 不应启动。

## 执行流程

### 第 1 步：LOAD - 读取设计上下文

优先读取以下信息：

- `.ai/missions/{missionId}/config.json`：确认 `projectRoot`、`backend.orm`、`backend.database`、`backend.moduleName`、`backend.moduleRoot`
- `.ai/missions/{missionId}/apiDesign/api-design.md`：API 设计，明确需要哪些实体
- `.ai/missions/{missionId}/reqDocs/req.md`：需求文档，确认业务规则
- `{projectRoot}/.ai/docs/backend-context.md`：确认 ORM 类型、Entity 基类、命名约定
- 已有的数据库实体和迁移文件（优先在 `projectRoot/backend.moduleRoot` 下定位实体）
- `.ai/missions/{missionId}/dbDesign/db-schema.md`：如存在，增量更新

必须先确认：

- 项目使用的 ORM 和数据库类型
- 是否存在 Entity 基类（如含 `id`、`createdAt`、`updatedAt`、`deletedAt` 的基类）
- 项目表名和字段名的命名约定
- 当前项目的实体主要落在哪个源码根目录；若 `backend.moduleRoot` 缺失，按 `src/modules` 兜底

**至少执行：**

- `test -f ".ai/missions/{missionId}/config.json"`
- `test -f ".ai/missions/{missionId}/apiDesign/api-design.md" || true`
- `find "{projectRoot}/{backend.moduleRoot}" -name "*.entity.ts" -maxdepth 5 | sort`

### 第 2 步：ENTITY - 设计实体结构

针对每个需要的实体：

1. 从 API 设计中的响应字段反推 Entity 字段
2. 从 DTO 的请求参数确认可写字段
3. 补充数据库层面的字段：主键、时间戳、软删除、版本号
4. 确认字段类型和约束

字段类型映射参考（以 TypeORM + MySQL/PostgreSQL 为例）：

| 接口类型 | 数据库类型             | 说明                      |
| -------- | ---------------------- | ------------------------- |
| string   | varchar(N) / text      | 根据长度选择              |
| number   | int / bigint / decimal | 根据精度选择              |
| boolean  | tinyint / boolean      | 根据数据库选择            |
| Date     | datetime / timestamp   | 根据时区需求选择          |
| enum     | tinyint / varchar      | 建议用 tinyint + 常量映射 |
| string[] | json / 关联表          | 根据查询需求选择          |

### 第 3 步：RELATION - 设计实体关系

确认实体之间的关系：

| 关系类型 | 设计要点                           |
| -------- | ---------------------------------- |
| 一对一   | 确认主表和从表、外键位置、是否级联 |
| 一对多   | 确认外键字段、是否需要反向引用     |
| 多对多   | 确认中间表名、是否需要额外字段     |
| 自引用   | 确认 parent_id 和层级结构          |

规则：

- 外键命名使用 `{ref_table}_id` 格式
- 必须声明 `onDelete` 行为（`CASCADE` / `SET NULL` / `RESTRICT`）
- 多对多中间表如果有额外字段，应设计为独立实体

### 第 4 步：INDEX - 设计索引

针对每个索引必须写清：

- 查询场景：哪个 API 的哪个查询条件需要这个索引
- 索引类型：BTREE / UNIQUE / FULLTEXT
- 索引字段：单字段 / 复合索引的字段顺序

规则：

- 每个有 `WHERE` 条件的查询场景都应检查是否需要索引
- 复合索引的字段顺序应与查询条件匹配
- 不盲目加索引；只在有明确场景时建索引
- 联合唯一约束必须写清业务含义

### 第 5 步：MIGRATION - 规划迁移策略

确认：

- 本次是新建表还是修改已有表
- 如果是修改，需要考虑数据迁移
- 是否有不兼容的变更（如删字段、改类型）
- 回滚方案

### 第 6 步：OUTPUT - 写入数据库设计文档

将结果写入 `.ai/missions/{missionId}/dbDesign/db-schema.md`，格式以 `../../references/doc-templates/db-schema-doc-template.md` 为准。

## 速查表

| 阶段      | 关键活动                  | 完成标准                     |
| --------- | ------------------------- | ---------------------------- |
| LOAD      | 读取 API 设计和项目上下文 | ORM 和命名约定明确           |
| ENTITY    | 设计实体字段和类型        | 每个字段都有类型和约束       |
| RELATION  | 设计实体关系              | 关系类型、外键和级联行为明确 |
| INDEX     | 设计索引                  | 每个索引都有查询场景支撑     |
| MIGRATION | 规划迁移策略              | 迁移类型和风险明确           |
| OUTPUT    | 写入 `db-schema.md`       | 下游 step 可直接消费         |

## 常见借口

| 借口                         | 现实                                      |
| ---------------------------- | ----------------------------------------- |
| "先全量建表，用不到的后面删" | 废弃字段和表会变成维护负担                |
| "索引后面看性能再加"         | 上线后加索引会锁表，事先规划更安全        |
| "类型用 varchar 万能"        | 滥用 varchar 会影响索引性能和数据校验     |

## 危险信号 - 立即停下来

- 你设计了一个没有任何 API 使用的实体
- 你没有确认 ORM 类型就开始写 Entity 字段
- 你加了一个没有查询场景的索引
- 你设计了多对多关系但没有定义中间表

## 参考文档

| 主题               | 文件                                                       |
| ------------------ | ---------------------------------------------------------- |
| 通用规则           | `../../references/rules/common-rules.md`                   |
| 数据库设计文档模板 | `../../references/doc-templates/db-schema-doc-template.md` |
| NestJS 代码规则    | `../../references/rules/nestjs-code-rules.md`              |

## 集成关系

- **直接上游：** `api-design`
- **可选上游：** `project-context-build` 的 `backend-context.md`
- **直接下游：** `module-dev`
