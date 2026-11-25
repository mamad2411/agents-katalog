---
name: wechat-article-writer
version: 1.0.0
description: "微信公众号文章写作和排版助手。输入主题+内容大纲→自动生成结构完整、排版精美的公众号文章（WeChat兼容HTML+行内样式），同时可配套调用infographic-generator生成4主题配图。触发词：'公众号文章','写公众号','公众号排版','微信文章','推文'。"

# 技能分类
category: "execution"

# 复杂度标识
complexity: "medium"

# 预计执行时长
typical_duration: "5min"

# 依赖关系
dependencies: []
benefits-from: [infographic-generator]
conflicts-with: []

# 工件配置
output_artifact: "memory/artifacts/wechat-article-writer/"

# 工具权限
allowed-tools:
  - Read
  - Write
  - Bash

# 标签（用于技能推荐）
tags:
  - "公众号文章"
  - "微信排版"
  - "文章生成"
  - "配图生成"
---

# 微信公众号文章排版器

## 触发方式

- 用户说"公众号文章""写公众号""公众号排版""微信文章""推文"时触发
- 用户提供 .md 文件或写作主题+大纲

## 工作流

### Phase 1 — 解析输入

- 如果是 .md 文件路径 → `parseMarkdown(text)` 解析
- 如果用户口述主题+大纲 → 先生成 Markdown 内容，再解析
- 自动推断文章主题（tech/product/warm/zen）

### Phase 2 — 排版渲染

- `wechat-render.js` 渲染结构化 sections → WeChat 兼容 HTML
- 所有样式使用行内 `style=""`，禁止 `<style>` 块、`<script>`、外部 CSS
- 输出：`article.html`（预览版，含 `<img>`） + `article-plain.html`（公众号粘贴版，图片用虚线占位框替换）

### Phase 3 — 配图生成（通过 infographic-generator）

- `buildSectionPageConfigs` 为每个 h2 section 生成独立花园页面配置
- `takeMultiPageScreenshots` 通过 Playwright 截图：竖长（750×1334）+ 宽屏（1200×675 16:9）
- 宽屏图存入 `{theme}/wide/` 子目录
- `buildImageMap` 将宽屏图映射到文章各位置

## Markdown 解析规则

| 输入模式 | 输出类型 |
|----------|----------|
| `一、标题` `二、标题` | h2 |
| `1. 小节` `2. 小节` | h3 |
| `### text` `## text` | h3 / h2 |
| `- 要点` `· 要点` `1. 步骤` | ul |
| `> 引用` | blockquote |
| `**强调**` | strong（强调色） |
| `快速回顾` `一句话总结` `划重点` | highlight |
| `---` `***` | separator |
| `案例N：` / 带冒号短行(8-50字) | h3 |
| 自然段落标题（8-30字、含！，？：、中文/字母开头） | h2 |

## 配图映射规则

| 图片 | 插入位置 |
|------|----------|
| hero | 文章标题下方 |
| section-N | 第 N 个 h2 之后 |
| cta | 文末 |

默认主题：apple（明亮）。可用：linear/apple/stripe/muji。

## 输出目录结构

```
output/
├── article.html             ← 图文混排预览（含真实 <img>）
├── article-plain.html       ← 公众号粘贴版（图片为虚线占位框）
├── 插入指南.md               ← 图片位置对照表
└── screenshots/{theme}/
    ├── {theme}-hero.png     ← 竖长头图
    ├── {theme}-section-N.png ← 竖长章节图
    ├── {theme}-cta.png      ← 竖长尾图
    └── wide/                ← 宽屏版（公众号文章实际引用）
        ├── {theme}-hero-wide.png
        ├── {theme}-section-N-wide.png
        └── {theme}-cta-wide.png
```

## WeChat 约束

- 所有样式行内 `style=""`，无 `<style>` 块、`<script>`、`<iframe>`、事件处理器
- 字体仅系统字体栈
- 颜色用 6 位 hex 不简写
- 图片先上传到微信素材库再插入，本地路径粘贴后丢失

## 文件清单

| 文件 | 角色 |
|------|------|
| `wechat-full.js` | 一站式编排入口（解析→配图→渲染） |
| `wechat-md2html.js` | Markdown 解析器 |
| `wechat-render.js` | WeChat HTML 渲染器 |
| `wechat-themes.json` | 4 种文章主题 |
| `../infographic-generator/generate-garden-page.js` | 配图 HTML 生成（require 依赖） |
| `../infographic-generator/theme-recipes.json` | 配图主题 CSS token |