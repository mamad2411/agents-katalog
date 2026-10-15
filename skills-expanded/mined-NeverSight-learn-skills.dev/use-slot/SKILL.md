---
name: use-slot
description: "Applies Vue's simplest slot syntax (v-slot shorthand #). Use when writing or modifying Vue templates that consume components with slots. Trigger even if user just says 'pass content to component' or 'use component slot'. Enforces # usage and prevents deprecated v-slot:/slot-scope syntax."
---

# Vue 简易插槽使用指南

此技能指导你以最简单、最现代的方式使用 Vue 组件的插槽，即统一使用 `v-slot` 的简写形式（`#`）。

## 核心原则

1. **始终使用简写 `#`**：彻底放弃使用 `v-slot:`，统一替换为 `#`。
2. **默认插槽简写**：在使用默认插槽时，由于参数默认为 `default`，直接使用 `#` 即可（如 `#="{ item }"`）。不需要写成 `#default="{ item }"`。
3. **独占默认插槽的简写**：如果组件**只提供了一个默认插槽**（即没有其他具名插槽），应直接将 `#` 或解构属性写在组件标签上（例如 `<my-component #="{ item }">`），这是官方支持且最简洁的写法。
4. **混合插槽的最简写法**：如果组件同时包含默认插槽和具名插槽：
   - **无作用域参数**：对于不需要接收参数的默认插槽，最简方式是**完全省略 `<template>` 标签**，直接将内容写在组件内部（即隐式默认插槽：所有顶层非 `<template>` 节点都会被隐式地视为默认插槽的内容）。
   - **有作用域参数**：必须使用 `<template #="{ item }">` 包裹，切勿在组件标签上直接写 `#`。

## 工作流检查清单

在使用带有插槽的组件时：
- [ ] 确认组件提供的是具名插槽、默认插槽还是作用域插槽。
- [ ] 具名插槽使用 `<template #slot-name>`。
- [ ] 作用域插槽使用 `<template #="slotProps">` 或 `<template #slot-name="slotProps">`。
- [ ] 适用时，优先使用 ES6 解构语法提取作用域插槽的属性（例如 `#="{ item }"`）。
- [ ] **独占默认插槽特例**：如果只有默认插槽，直接在组件上使用 `<my-component #="{ item }">`。
- [ ] **隐式默认插槽**：在混合插槽中，如果默认插槽无作用域参数，直接省略 `<template>` 标签，将内容直接写在组件内部（顶层非 `<template>` 节点即为默认插槽内容）。
- [ ] 确保组件标签使用的是 `kebab-case`（如 `<my-component>`，符合代码规范）。
- [ ] **代码自检 (Validation)**：生成代码后，务必进行自检：确认没有遗留 `v-slot:`，且没有在混合插槽的情况下把 `#` 直接挂载到组件标签上。

## 常见陷阱 (Gotchas)

**Bad vs Good 快速对比**：
- ❌ 错误：`<template v-slot:header>` 或 `<template #default="props">`
- ✅ 正确：`<template #header>` 或 `<template #="props">`

- **混用简写和全写**：不要在同一个模板中混用 `v-slot:` 和 `#`，请统一使用 `#`。
- **混合插槽的错误挂载**：当有多个插槽时，绝对不要把 `#` 挂载在组件标签本身上，这会导致编译错误或作用域混乱。此时必须老老实实使用 `<template>`。
- **应用于原生元素**：绝对不要将 `#name` 挂载到原生 HTML 元素（如 `<div>`）上，它只能用于组件或 `<template>`。
- **废弃语法**：绝对不要使用已废弃的 `slot` 或 `slot-scope` 属性。

## 深入了解与代码示例

如果你需要查看不同场景下的具体代码示例（如独占默认插槽、复杂解构、无渲染组件等），请立即使用读取工具读取以下参考文件：
[[references/slot-details.md]]
