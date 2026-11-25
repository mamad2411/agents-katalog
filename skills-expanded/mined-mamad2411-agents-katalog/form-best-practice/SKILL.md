---
name: form-best-practice
description: 使用 react-hook-form 管理所有表单状态，结合 shadcn/ui Form 组件与 Zod 校验，禁止使用 useState 或 zustand 直接管理表单字段，实现表单与全局状态的"两棵树"隔离模型。
---

# 表单最佳实践

本 Skill 指导在 TypeScript + React + shadcn/ui + react-hook-form + Zod 架构下，编写符合规范的表单组件。

## 使用说明

1. 阅读 [表单最佳实践指南](references/form-best-practice-guide.md)，了解"两棵树"模型与状态隔离原则
2. 参考 [示例代码](references/examples/GoodFormExample.tsx) 了解标准写法
3. 使用 [检查清单](references/checklist.md) 验证生成或重构的表单组件

## 关键规范

- **react-hook-form 独立管理表单状态**：禁止使用 `useState`、`useReducer` 管理表单字段
- **禁止与 zustand 直接绑定**：表单是独立沙盒，仅在提交时通过副本对外输出数据
- **字段必须通过 FormField 接入**：使用 `render={({ field }) => <Input {...field} />}` 模式
- **初始值深拷贝副本**：`defaultValues` 必须是原始数据的深拷贝，避免双向污染
- **Zod + zodResolver 校验**：必须使用 Zod Schema 定义表单结构并集成到 `useForm`
- **子组件通过 FormProvider 共享上下文**：禁止逐层传递 `control` 或 `register`
