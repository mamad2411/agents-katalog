---
name: trpc-on-demand-query
description: 在不引入 GraphQL 的前提下，为 tRPC 接口添加 include（按需加载关联字段）和 fields（响应字段裁剪）参数，实现接口的选择性查询能力，降低过量数据传输、解析成本与前端类型维护难度。
---

# tRPC 按需查询接口设计规范

本 Skill 指导在 tRPC 架构下，通过标准化的 `include` 和 `fields` 参数，为查询接口添加按需数据加载与字段裁剪能力，无需引入 GraphQL。

## 使用说明

1. 阅读 [按需查询设计指南](references/guide.md)，了解参数设计规范与执行流程
2. 参考 [Router 实现示例](references/RouterExample.ts) 了解完整实现
3. 参考 Schema 定义示例：[BattleSchema.ts](references/SchemaExample/BattleSchema.ts)、[BattleExtendedSchema.ts](references/SchemaExample/BattleExtendedSchema.ts)、[GetBattleInputSchema.ts](references/SchemaExample/GetBattleInputSchema.ts)
4. 使用 [检查清单](references/checklist.md) 验证实现是否符合规范

## 核心规范

- **双参数设计**：`include`（扩展字段加载）+ `fields`（响应裁剪），职责分离
- **三步执行流程**：基础查询 → include 扩展加载 → fields 字段裁剪
- **枚举 include 选项**：使用 `z.enum([...])` 明确声明支持的扩展字段名
- **权限校验**：扩展字段按需进行权限检查（不加载即不暴露）
- **一级限制**：仅支持一级扩展，禁止嵌套 include（如 `user.friends.votes`）
- **降级安全**：`fields` 包含未加载的 include 字段时，静默忽略并记录 warning
