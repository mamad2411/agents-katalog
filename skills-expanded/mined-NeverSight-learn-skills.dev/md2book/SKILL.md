---
name: md2book
description: 将 Markdown 格式的书籍转换为专业排版的 PDF 电子书，支持智能分页、中文完美渲染、精美装帧设计和多种视觉主题
trigger: 用户要求将 Markdown 转 PDF、制作 PDF 电子书、书籍导出 PDF、md转pdf、生成pdf、markdown转pdf、书籍排版、制作书籍PDF
---

# Markdown to Professional PDF Book Converter

将 Markdown 格式的技术书籍/教程转换为专业排版的 PDF 电子书。

## 何时使用

- 用户提供 Markdown 文件路径，要求转为 PDF
- 用户提到"导出 PDF"、"生成电子书"、"制作 PDF"
- 用户需要书籍级别的排版输出

## 快速命令

```bash
node scripts/md2book.js <input.md>
node scripts/md2book.js <input.md> --theme <minimal|academic|playful>
node scripts/md2book.js <input.md> --output <path.pdf>
node scripts/md2book.js <input.md> --verbose
```

## 完整工作流程

### Phase 1: 检查输入

1. 确认用户提供了 Markdown 文件路径
2. 检查文件是否存在
3. 检查文件是否有 YAML frontmatter（title, author, date 等）
4. 如果没有 frontmatter，询问用户补充关键信息（书名、作者）

### Phase 2: 确认参数

向用户确认：
- **主题风格**（默认 minimal）：
  - `minimal` — 极简科技风（大量留白，黑白灰，适合技术书）
  - `academic` — 经典学术风（衬线字体，暖色纸张，稳重专业）
  - `playful` — 活泼插画风（色彩丰富，渐变装饰）
- **输出路径**（默认与 MD 文件同级目录）
- **是否需要目录**（默认生成）

### Phase 3: 执行转换

```bash
cd /Users/bytedance/Documents/CC/huashu/huashu-bookwriter-skill
node scripts/md2book.js <input.md> --theme <theme> --verbose
```

### Phase 4: 验证输出

1. 检查 PDF 文件是否生成
2. 验证以下项目：
   - [ ] 封面正常渲染（书名、作者可见）
   - [ ] 版权页包含完整信息
   - [ ] 目录生成正确
   - [ ] 每个 `#` 章节从新页面开始
   - [ ] 中文无乱码
   - [ ] 页码连续
   - [ ] 代码块/表格未被截断
3. 如果有问题，检查错误日志并修复

## 输入文件格式

Markdown 文件应包含 YAML frontmatter：

```yaml
---
title: 书名
subtitle: 副标题（可选）
author: 作者名
publisher: 出版社（可选）
version: v1.0
date: 2026-04-10
isbn: 978-0-000000-00-0（可选）
description: 一句话简介
---

# 第一章 引言

正文内容...

## 1.1 概述

更多内容...
```

### 支持的 Markdown 特性

- 标准 GFM（表格、代码块、列表）
- 代码语法高亮（highlight.js）
- Callout 提示框：`[!INFO]`, `[!TIP]`, `[!WARNING]`, `[!DANGER]`
- 图片和图注
- 引用块
- 自动目录生成

## 视觉主题说明

### minimal（极简科技风）
- 纯白背景，黑白灰色调
- 思源宋体正文 + 黑体标题
- 简洁的装饰线条
- 适合：技术文档、编程教程

### academic（经典学术风）
- 暖色纸张质感背景
- 深红色强调色
- 经典衬线字体
- 适合：理论著作、学术专著

### playful（活泼插画风）
- 渐变彩色封面
- 圆角卡片设计
- 丰富的色彩变化
- 适合：入门教程、科普读物

## 故障排查

### 中文显示为方框
- 检查系统是否安装了思源宋体或宋体
- macOS 自带 Songti SC 和 STSong
- 可在 `references/font-guide.md` 中查看字体配置

### Playwright 浏览器未安装
```bash
cd /Users/bytedance/Documents/CC/huashu/huashu-bookwriter-skill/scripts
npx playwright install chromium
```

### 依赖未安装
```bash
cd /Users/bytedance/Documents/CC/huashu/huashu-bookwriter-skill/scripts
npm install
```

### PDF 内容为空
- 检查 Markdown 文件编码是否为 UTF-8
- 使用 `--verbose` 查看转换日志
- 检查 frontmatter 格式是否正确

### Chromium 浏览器找不到
- 脚本会自动检测 `~/Library/Caches/ms-playwright/` 下的 Chromium
- 如果未安装，运行 `npx playwright install chromium`
- 确认安装后重新运行转换命令

## 相关文件

- `scripts/md2book.js` — 主转换脚本
- `scripts/package.json` — 依赖配置
- `assets/styles/book.css` — 书籍核心样式（分页、页眉页脚）
- `assets/styles/typography.css` — 中文字体排版
- `assets/styles/components.css` — 表格/代码块/引用/Callout 样式
- `assets/styles/themes/` — 三套视觉主题（minimal, academic, playful）
- `references/font-guide.md` — 字体配置参考
