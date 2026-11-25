---
name: artifacts-builder
description: 一套用于使用现代前端 Web 技术（React、Tailwind CSS、shadcn/ui）创建精致、多组件 claude.ai HTML 制品的工具。用于需要状态管理、路由或 shadcn/ui 组件的复杂制品 - 不适用于简单的单文件 HTML/JSX 制品。
license: Complete terms in LICENSE.txt
---

# 制品构建器 (Artifacts Builder)

要构建强大的前端 claude.ai 制品，请遵循以下步骤：
1. 使用 `scripts/init-artifact.sh` 初始化前端仓库
2. 通过编辑生成的代码来开发您的制品
3. 使用 `scripts/bundle-artifact.sh` 将所有代码打包成单个 HTML 文件
4. 向用户展示制品
5. （可选）测试制品

**技术栈**: React 18 + TypeScript + Vite + Parcel (打包) + Tailwind CSS + shadcn/ui

## 设计与风格指南

非常重要：为了避免所谓的“AI 垃圾（AI slop）”，请避免使用过多的居中布局、紫色渐变、统一的圆角和 Inter 字体。

## 快速开始

### 第 1 步：初始化项目

运行初始化脚本以创建一个新的 React 项目：
```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

这将创建一个完全配置好的项目，包含：
- ✅ React + TypeScript (通过 Vite)
- ✅ Tailwind CSS 3.4.1 带有 shadcn/ui 主题系统
- ✅ 路径别名 (`@/`) 已配置
- ✅ 预装 40+ 个 shadcn/ui 组件
- ✅ 包含所有 Radix UI 依赖项
- ✅ Parcel 已配置用于打包 (通过 .parcelrc)
- ✅ Node 18+ 兼容性 (自动检测并固定 Vite 版本)

### 第 2 步：开发您的制品

要构建制品，请编辑生成的文件。参见下文的 **常见开发任务** 获取指导。

### 第 3 步：打包为单个 HTML 文件

要将 React 应用程序打包为单个 HTML 制品：
```bash
bash scripts/bundle-artifact.sh
```

这将创建 `bundle.html` - 一个自包含的制品，其中内联了所有 JavaScript、CSS 和依赖项。此文件可以直接在 Claude 对话中作为制品共享。

**要求**：您的项目根目录中必须有一个 `index.html`。

**脚本的作用**：
- 安装打包依赖项 (parcel, @parcel/config-default, parcel-resolver-tspaths, html-inline)
- 创建支持路径别名的 `.parcelrc` 配置
- 使用 Parcel 构建 (无 source maps)
- 使用 html-inline 将所有资源内联到单个 HTML 中

### 第 4 步：与用户共享制品

最后，在对话中与用户共享打包后的 HTML 文件，以便他们可以将其作为制品查看。

### 第 5 步：测试/可视化制品（可选）

注意：这是一个完全可选的步骤。仅在必要或被请求时执行。

要测试/可视化制品，请使用可用工具（包括其他技能或内置工具，如 Playwright 或 Puppeteer）。一般而言，避免预先测试制品，因为这会增加请求和看到完成制品之间的延迟。稍后测试，在展示制品后，如果被请求或出现问题，再进行测试。

## 参考

- **shadcn/ui 组件**: https://ui.shadcn.com/docs/components