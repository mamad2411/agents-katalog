---
name: infographic-generator
version: 3.0.0
description: "Use when user needs 公众号配图 or wants to generate rich HTML pages with multi-theme screenshots. Triggers: '生成配图', '公众号配图', '帮我做配图', '生成截图', '生成信息图', 'infographic', or when user provides a writing topic + content/outline for visual article images."

# 技能分类
category: "execution"

# 复杂度标识
complexity: "medium"

# 预计执行时长
typical_duration: "5min"

# 依赖关系
dependencies: []
benefits-from: []
conflicts-with: []

# 工件配置
output_artifact: "memory/artifacts/infographic-generator/"

# 工具权限
allowed-tools:
  - Read
  - Write
  - Bash

# 标签（用于技能推荐）
tags:
  - "信息图"
  - "配图生成"
  - "截图生成"
  - "可视化"
---

# 信息图 / 公众号配图生成器

## 概述

一站式配图生成流水线：提供写作主题和内容大纲 → 自动生成精美 HTML 页面（内置 4 种设计风格）→ 自动截图为 PNG 图片。

```
用户: "帮我做配图，主题「XXX」，要点：A / B / C"
   ↓
Phase 1: 解析内容 → 提取标题、sections、关键信息
   ↓
Phase 2: 生成 HTML → 内置 CSS 变量，4 套主题可一键切换
   ↓
Phase 3: 自动截图 → 4 主题 × N 个 section → PNG
   ↓
输出目录: screenshots/{linear,apple,stripe,muji}/
```

## 4 种设计风格

默认全部生成，用户只需挑选喜欢的。

| 风格 | 文件夹 | 配色 | 适合场景 |
|---|---|---|---|
| **暗黑** | `linear/` | 深黑 `#08090A` + 紫色 | 技术类、SaaS、开发者 |
| **明亮** | `apple/` | 纯白 + 蓝色 | 产品发布、品牌宣发 |
| **人文** | `stripe/` | 奶油色 + 赭色 + Georgia 衬线 | 深度长文、人文内容 |
| **侘寂** | `muji/` | 纸白 + 极简去色 | 生活方式、设计美学 |

风格选择规则：
- **未指定** → 4 种全部生成
- "只要暗黑" → 只出暗黑风格
- "要明亮和人文" → 只出这两种

## 使用方式

触发关键词：
- "帮我做配图" / "公众号配图" / "生成截图" / "生成信息图"
- 同时提供写作主题和内容大纲/要点

## 工作流

### Phase 1 — 内容解析

从用户输入中提取：
- 标题（title）—— 文章大标题
- 副标题（subtitle）—— 一句话描述
- 品牌名（brand）—— 用于 nav 和 footer
- Sections —— 每节的结构化内容
- 关键数据 —— 数字/指标（可选）

### Phase 2 — HTML 生成

根据内容生成单文件 HTML：
- 内置 4 套 CSS 主题变量（`theme-recipes.json` 是唯一真相源）
- 页面结构：Hero → 痛点 → 核心要点 → 流程 → 演示 → 场景 → 数据 → CTA → Footer
- 右下角浮动主题切换按钮（4 个圆点）
- 至少 3-5 屏内容以确保截图量充足

### Phase 3 — 自动截图

由 `wechat-full.js` 调用 Playwright 完成多页面截图。

```
screenshots/
├── linear/   (暗黑)
├── apple/    (明亮)
├── stripe/   (人文)
└── muji/     (侘寂)
```

截图参数：750×1334 手机竖屏，2x Retina，全页长截图。

## 文件说明

| 文件 | 用途 |
|---|---|
| `SKILL.md` | 工作流定义 |
| `theme-recipes.json` | 4 套主题 CSS token 定义（唯一真相源） |
| `generate-garden-page.js` | 内容驱动的 HTML 页面生成器 |

## 技术说明

- 依赖：playwright（`npx playwright install chromium`）
- 输出格式：PNG，2x Retina，750×1334
- 主题系统：纯 CSS `:root` + `[data-theme]` 变量，无框架依赖
- 设计配方独立完整，不依赖其他 skill

## 配合其他 skill 使用

- 先分析话题（swot-analysis / first-principles / prompt-enhancer），再用本 skill 生成配图
- 先写文章（wechat-article-writer），再用本 skill 生成配图