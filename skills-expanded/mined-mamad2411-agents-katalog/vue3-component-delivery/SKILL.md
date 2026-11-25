---
name: vue3-component-delivery
displayName: Vue 3 组件实现
description: 在 Vue 3 + TypeScript 项目中新增或修改 SFC、组合式逻辑、Element Plus/Sh* 包装组件、表格和页面组件时使用。强调 Composition API、组件契约和最小改动。
triggers: ["Vue组件", "script setup", "Element Plus", "Sh组件", "Vue表格", "Vue页面"]
autoTrigger: true
version: '1.0.0'
---

# Vue 3 组件实现

## 前置检查

1. 读取 `AGENTS.md`，确认 `techStack == frontend-vue3`。
2. 不匹配时跳过本 skill，使用对应前端 profile 或通用前端 skill。

## 工作流

1. 阅读目标 SFC、相邻组件、composables、store、API 和样式。
2. 确认组件边界：props、emits、slots、v-model、权限和加载/异常态。
3. 默认使用 `<script setup lang="ts">`、Composition API 和项目已有封装组件。
4. 新增可复用逻辑前先确认是否已有 composable 或公共工具。
5. 修改公共组件时必须核对调用点，避免破坏外部契约。

## Vue 专项检查

- `modelValue` 与 `update:modelValue` 是否匹配。
- `change` 是否只代表用户交互，不被程序化归一化误触发。
- 模板组件命名和事件命名是否符合项目风格。
- watch/computed 是否存在重复请求或频繁重算。
- 表格和大列表是否避免全量刷新与重渲染。

## 输出要求

说明组件契约是否变化；如无变化，明确“外部调用契约不变”。
