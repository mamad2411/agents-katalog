---
name: react-performance
description: React 性能最佳实践（适配 Vite）。frontend-dev 写组件、拉列表、优化卡顿时使用。源自 vercel-labs/agent-skills（react-best-practices）。
disable-model-invocation: false
---

# React 性能（适配 portfolio-site）

> 来源：[vercel-labs/agent-skills · react-best-practices](https://github.com/vercel-labs/agent-skills)（约 2.9 万星）  
> 适配：本项目是 **Vite + React**，下列 **Next.js / RSC 专用**规则默认跳过。

## 优先遵守（对本项目最有用）

### 消除瀑布（Critical）

- 独立请求用 `Promise.all`
- 先做便宜的同步判断，再 `await`
- 只在真正用到的分支里 `await`

### 包体积（Critical）

- 避免 barrel 大包导入；按需直接 import
- 重型组件按需动态导入
- 分析/统计类脚本延后加载

### 客户端数据（Medium-High）

- 列表/详情请求要有加载与错误态
- 同一数据不要重复打接口；可简单缓存或提升到合适父级

### 重渲染（Medium）

- 派生状态在 render 里算，不要多余 `useEffect`
- 不要在组件里再定义子组件
- 输入类交互可考虑 `startTransition` / `useDeferredValue`（若团队已用）

## 对本项目明确跳过

- `server-*`、`next/dynamic`、RSC props 序列化等 Next 专用项（除非以后迁 Next）

## 使用方式

写或改 `frontend/` 组件前扫一遍上表；审查时按 Priority 从高到低提建议。

原文清单：`docs/skill-sources/react-best-practices.md`
