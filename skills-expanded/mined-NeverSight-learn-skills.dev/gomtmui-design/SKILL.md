---
name: gomtmui-design
description: Use when 对 gomtmui 页面和组件进行编写、重构或设计对齐，尤其是列表视图、Next.js page、route query、筛选表单与数据库列表 RPC 参数需要保持一致时。
---

本技能文档按照功能、组件、页面等方式在 `references` 目录下进行详细描述。

使用方式：

1. 当需要编辑或重构具体页面/组件时，先找对应 `references` 文档。
2. 如果是列表页，优先阅读 `references/列表视图.md`。
3. 列表页必须优先遵守 route-state 与列表 RPC 参数一致的规则，而不是先发明前端专属筛选状态。
4. Next.js page 语法应跟随当前仓库约定，例如 `searchParams: Promise<...>` 后 `await searchParams`。

- [列表视图规格](references/列表视图.md)
