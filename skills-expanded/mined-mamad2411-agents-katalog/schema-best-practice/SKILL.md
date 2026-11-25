---
name: schema-best-practice
description: 使用 Zod Schema 替代传统 DTO，定义表结构 Schema 与业务视图 Schema，支持类型推导、运行时校验与前后端契约共享。适用于 Service、Repository、Controller 各层的数据结构规范化。
---

# Schema 最佳实践

本 Skill 用于指导在 tRPC + Drizzle ORM 架构中，以 Zod Schema 替代传统 DTO，统一各层的数据结构定义与校验。

## 使用说明

1. 阅读 [Schema 最佳实践指南](references/schema-best-practice-guide.md)，了解两种 Schema 类型及各层使用规范
2. 使用 [检查清单](references/checklist.md) 验证生成或重构的 Schema 是否符合规范

## 核心概念

| Schema 类型                                   | 用途                                                                                                                                   | 所在层             |
| --------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| 表结构 Schema（`{TableName}Schema`）          | 以 Zod 显式描述单张表字段；**DAO 层直接用 Drizzle 的 `$inferInsert`/`$inferSelect`，此 Schema 仅在 Service 层需要 Zod 校验时按需使用** | Service 层（可选） |
| 业务视图 Schema（Business View）              | 描述前端/API 所需聚合数据，替代 DTO                                                                                                    | Service 层         |
| 输入 Schema（`{Action}{Feature}InputSchema`） | 描述写操作输入，供 Repository 使用                                                                                                     | Repository 层      |

## 关键规范

- **DAO 层不使用 Zod Schema**：DAO 直接使用 Drizzle 的 `$inferInsert` / `$inferSelect` 类型推断
- **不使用传统 DTO 类**：Service/Controller 层统一用声明式 Zod Schema 定义结构
- **一个文件只导出一个 Schema**：每个 Schema 定义在独立文件中，文件名即 Schema 名（PascalCase），同文件同时导出对应 `z.infer<>` 类型
- **业务视图 Schema** 由 Service 层组装，不在 Repository 中构建
- **Repository 只返回关键标识**（`{ id: number }`），完整视图在 Service 拼装
- **Schema 命名约定**：
  - 表结构（可选）：`{TableName}Schema`
  - 业务视图：`{Feature}WithXxxSchema`
  - 输入：`{Action}{Feature}InputSchema`
