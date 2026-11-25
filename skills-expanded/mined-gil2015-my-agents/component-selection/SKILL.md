---
name: component-selection
description: Use when choosing whether frontend UI work should reuse existing components, utilities, hooks, layouts, or create local replacements
---

# Component Selection

## 决策顺序

1. 查项目知识基线。
2. 查同类历史模块摘要。
3. 只在必要时读取 1-2 个相关文件切片。
4. 优先复用全局组件。
5. 再考虑 UI 库或项目封装。
6. 最后才新增本地组件。

## 禁止

- 不直接全量读取复杂历史模块。
- 不重复造已有组件。
- 不用历史模块覆盖当前需求。

## 输出

新增本地组件时，在自检中说明为什么现有组件不满足。
