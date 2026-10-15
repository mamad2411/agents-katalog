---
name: project-reader
description: 项目结构分析技能。用于快速理解陌生前端/全栈项目的技术栈、目录结构和模块依赖关系。通过分层阅读工作流，从框架检测到依赖分析，逐步深入理解项目架构。适用于需要接手新项目、分析代码库、或进行技术调研的场景。
---

# Project Reader

## Overview

Project Reader 是一个项目结构分析技能，能够自动检测前端/全栈项目的技术栈、分析目录结构、解析模块依赖关系，并生成可读性强的分析报告。通过分层阅读工作流，帮助开发者快速理解陌生项目的架构设计。

## When to Use

在以下场景中应使用此技能：

- **接手新项目**：需要快速了解项目的技术栈和代码结构
- **技术调研**：评估某个项目的技术方案或代码质量
- **代码审查**：分析项目的依赖关系和模块组织
- **重构准备**：了解现有项目的架构以便进行合理的重构
- **学习示例**：通过分析开源项目学习最佳实践

## Quick Start

### 基本使用

```bash
# 进入技能目录
cd /home/luckxp/.agents/skills/project-reader

# 生成完整的项目分析报告
python scripts/generate_report.py /path/to/project

# 指定输出文件
python scripts/generate_report.py /path/to/project -o report.md
```

### 分层分析

如需更精细的控制，可以逐层运行分析脚本：

```bash
# 第 1 层：框架检测
python scripts/detect_framework.py /path/to/project

# 第 2 层：目录结构分析
python scripts/analyze_structure.py /path/to/project

# 第 3 层：依赖关系分析
python scripts/analyze_dependencies.py /path/to/project
```

## Layered Reading Workflow

Project Reader 采用分层阅读工作流，从宏观到微观逐步深入理解项目。

### 第 1 层：框架检测

运行 `detect_framework.py` 获取项目的基础技术信息：

- **框架类型**：React、Vue、Angular、Next.js、Nuxt、Svelte、SvelteKit、Gatsby、Remix
- **UI 库**：Material UI、Ant Design、Radix UI、Chakra UI、Element Plus、Vuetify、Tailwind CSS、Styled Components
- **构建工具**：Vite、Webpack、Turbopack、Rollup、Parcel、esbuild
- **包管理器**：npm、yarn、pnpm、bun
- **入口文件**：识别应用的启动入口
- **项目元信息**：名称、版本、描述、可用脚本

### 第 2 层：目录结构分析

运行 `analyze_structure.py` 了解项目的组织方式：

- **目录树**：递归生成项目的目录结构（最大深度 5 层）
- **文件类型分布**：统计各类型文件数量（JavaScript、TypeScript、Vue、Python 等）
- **关键目录**：识别项目中的重要目录（src、components、hooks、utils、services 等）
- **配置文件**：列出项目配置文件（tsconfig.json、vite.config.js、.eslintrc 等）

### 第 3 层：依赖关系分析

运行 `analyze_dependencies.py` 深入理解模块之间的关联：

- **模块依赖图**：提取所有文件中的 import/require 语句
- **核心模块**：按引用次数排序，识别被最频繁使用的模块
- **循环依赖**：检测项目中存在的循环依赖问题
- **模块列表**：列出项目中所有的模块路径

### 第 4 层：模块内容阅读

在完成前三层分析后，根据生成的报告：

1. 识别核心模块和关键文件
2. 从入口文件开始阅读，理解应用启动流程
3. 查看关键目录的组织方式
4. 分析核心模块的实现逻辑

## Scripts

### detect_framework.py

框架检测脚本，用于识别项目的基础技术栈。

```bash
python scripts/detect_framework.py /path/to/project
```

**输出示例：**

```json
{
  "framework": "Next.js",
  "ui_library": "Tailwind CSS",
  "build_tool": "Vite",
  "package_manager": "pnpm",
  "dependencies": ["next", "react", "react-dom", "tailwindcss", ...],
  "entry_points": ["src/app/layout.tsx", "src/app/page.tsx"],
  "project_name": "my-next-app",
  "project_version": "1.0.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  }
}
```

**检测范围：**
- 9 种主流前端框架
- 8 种 UI 库/样式方案
- 6 种构建工具
- 4 种包管理器

### analyze_structure.py

目录结构分析脚本，生成项目的目录树和文件统计。

```bash
python scripts/analyze_structure.py /path/to/project
```

**输出包含：**
- 完整的目录树结构（JSON 格式）
- 文件类型分布统计
- 关键目录识别结果
- 配置文件列表

### analyze_dependencies.py

依赖关系分析脚本，提取和分析模块间的引用关系。

```bash
python scripts/analyze_dependencies.py /path/to/project
```

**输出包含：**
- 每个文件的依赖列表
- 按使用频率排序的核心模块
- 检测到的循环依赖
- 所有模块的完整列表

**支持的文件类型：**
- JavaScript (.js, .jsx)
- TypeScript (.ts, .tsx)
- Vue (.vue)
- Python (.py)

### generate_report.py

报告生成脚本，整合上述三个脚本的输出，生成 Markdown 格式的分析报告。

```bash
# 输出到标准输出
python scripts/generate_report.py /path/to/project

# 输出到文件
python scripts/generate_report.py /path/to/project -o report.md
```

**报告内容包括：**
- 项目概述（名称、路径、版本、描述）
- 框架信息（框架、UI 库、构建工具、包管理器）
- 目录结构（目录树、文件类型分布、关键目录）
- 依赖分析（模块统计、核心模块、循环依赖）

## Resources

### references/common_patterns.md

常见项目结构模式参考文档，包含：

- React 项目标准结构
- Next.js 项目结构（App Router 和 Pages Router）
- Vue 项目标准结构
- 常见目录模式对比
- 关键配置文件说明

### 目录结构

```
project-reader/
├── SKILL.md                   # 技能文档
├── scripts/                   # 分析脚本
│   ├── detect_framework.py   # 框架检测
│   ├── analyze_structure.py  # 目录结构分析
│   ├── analyze_dependencies.py # 依赖关系分析
│   └── generate_report.py    # 报告生成
├── references/                # 参考资料
│   └── common_patterns.md    # 项目结构模式
└── assets/                    # 静态资源（预留）
```

---

*使用 Project Reader 技能时，建议从 Quick Start 开始，根据需要逐步深入到分层阅读工作流的各个层级。*
