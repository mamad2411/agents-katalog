---
name: repository-best-practice
description: 为跨表事务性写操作创建 Repository 层，封装多张表的写入事务，确保原子性与数据一致性。当需要跨表写入、事务封装或创建包含业务输入 Schema 的 Repository 文件时使用。触发短语："创建repository"、"写repository"。
---

# Repository 最佳实践

Repository 层是跨表、事务性写操作的统一入口，位于 Service 与 DAO 之间。

## 核心分工

| 层级           | 职责                                          |
| -------------- | --------------------------------------------- |
| DAO            | 单表 CRUD，接收可选 `tx` 参数                 |
| **Repository** | 跨表事务性写入，原子性保证                    |
| Service        | 业务编排 + 调用 Repository / DAO 组装数据视图 |

## 使用说明

1. 阅读 [最佳实践指南](references/repository-best-practice-guide.md)，了解架构定位与设计规则
2. 参考 [代码模板](references/template-repository.ts) 了解标准写法
3. 生成或重构 Repository 文件后，使用 [检查清单](references/checklist.md) 逐项验证

## 关键规范

- **只写不读**：Repository 仅负责写入，不负责构建前端视图
- **原子事务**：多表写入必须包裹在同一个 `db.transaction()` 中
- **输入 Schema**：使用 Zod 定义 `XxxInputSchema`，Repository 方法接受经校验的输入对象
- **返回最小标识**：成功后只返回关键 ID（如 `{ id: battleId }`），不返回完整视图
- **命名约定**：文件名 `{feature}Repository.ts`，导出 `export const {Feature}Repository = { ... }`
