---
name: md2pdf
description: |
  将 Markdown(.md) 文件转换为 PDF 文档。当用户提及 markdown to pdf、md 转 pdf、导出 pdf、生成 pdf 文档、markdown 文件转换、批量转换 markdown、代码高亮 pdf、中文 markdown 转 pdf，或任何需要将 .md 文件转为 pdf 格式的场景时，立即使用此 skill。基于 WeasyPrint 轻量方案，支持5种精美模板和智能中文排版。
---

# Markdown 转 PDF

使用 jmaupetit/md2pdf 将 Markdown 文档转换为专业排版的 PDF。

## 技术方案

- **核心引擎**: WeasyPrint（纯 Python，无需 Chromium）
- **模板系统**: CSS + Jinja2 支持
- **代码高亮**: Pygments
- **中文支持**: 自动检测 + 多字体回退

## 安装

### 1. 运行环境检查

```bash
# 进入技能目录
<skill-path>/scripts/setup.sh
```

此脚本会检查并自动安装：
- Python 3.10+
- md2pdf CLI 工具
- WeasyPrint 依赖
- 系统中文字体

### 2. 手动安装

```bash
# 安装 md2pdf
pip install "md2pdf[cli]" --break-system-packages

# 安装中文字体（Ubuntu/Debian）
sudo apt install fonts-noto-cjk fonts-wqy-microhei

# 安装中文字体（macOS）
brew install font-noto-sans-cjk
```

## 快速开始

### 基础转换

```bash
# 转换单个文件（输出到同目录）
md2pdf -i document.md

# 指定输出文件
md2pdf -i document.md -o output.pdf
```

### 使用模板

```bash
# 使用内置模板
md2pdf --css <skill-path>/templates/chinese-modern.css -i document.md

# 可用模板：
# - default: 基础样式
# - modern: 现代风格
# - code-highlight: 代码高亮
# - chinese-default: 中文基础
# - chinese-modern: 中文现代（推荐）
```

### 批量转换

```bash
# 使用批量转换脚本
python3 <skill-path>/scripts/batch_convert.py "*.md"

# 递归转换目录
python3 <skill-path>/scripts/batch_convert.py ./docs/

# 使用指定模板
python3 <skill-path>/scripts/batch_convert.py "*.md" --template chinese-modern

# 指定输出目录
python3 <skill-path>/scripts/batch_convert.py "*.md" --output-dir ./output/

# 使用 8 个并行进程
python3 <skill-path>/scripts/batch_convert.py "**/*.md" --workers 8
```

## 模板系统

### 内置模板

| 模板名 | 描述 | 适用场景 |
|--------|------|----------|
| **default.css** | 基础样式 | 通用文档 |
| **modern.css** | 现代风格 | 报告、专业文档 |
| **code-highlight.css** | 代码高亮 | 技术文档、教程 |
| **chinese-default.css** | 中文基础 | 中文通用文档 |
| **chinese-modern.css** | 中文现代 | 中文报告、论文 |

### 模板位置

所有模板位于 `<skill-path>/templates/` 目录

### 自动模板选择

批量转换脚本会智能选择模板：
- 检测到中文内容 → 自动使用中文模板
- 检测到代码块 → 优先使用代码高亮模板
- 默认 → 使用 modern 模板

## 中文支持

### 字体优先级

系统会按以下优先级选择中文字体：
1. Noto Sans/Serif CJK SC
2. Source Han Sans/Serif SC
3. WenQuanYi Micro Hei/Zen Hei
4. Microsoft YaHei / SimHei / SimSun
5. 系统默认字体

### 安装中文字体

```bash
# Ubuntu/Debian
sudo apt install fonts-noto-cjk fonts-wqy-microhei fonts-wqy-zenhei

# macOS
brew install font-noto-sans-cjk font-noto-serif-cjk

# 查看已安装的中文字体
fc-list :lang=zh | head -20
```

### 中文排版优化

- 自动首行缩进（2字符）
- 优化的行高（1.8-1.85）
- 合适的字间距
- 中文标点处理

## 高级用法

### 使用 frontmatter

在 Markdown 文件开头添加 YAML 配置：

```markdown
---
title: 文档标题
author: 作者姓名
date: 2024-01-01
---

# 正文内容
```

### Markdown 扩展

```bash
# 启用表格支持
md2pdf --extras tables -i document.md

# 启用代码围栏
md2pdf --extras fenced_code -i document.md

# 启用多个扩展
md2pdf --extras tables --extras fenced_code -i document.md
```

### 自定义 CSS

```bash
# 使用自定义 CSS 文件
md2pdf --css /path/to/custom.css -i document.md
```

### 查看所有选项

```bash
md2pdf --help
```

## 批量转换脚本详解

### 功能特点

- **并行处理**: 默认4个并发进程
- **自动检测**: 智能识别中文内容和代码块
- **进度显示**: 实时显示转换进度
- **错误处理**: 继续处理其他文件
- **glob 支持**: 支持 `**/*.md` 递归模式

### 使用示例

```bash
# 列出所有可用模板
python3 <skill-path>/scripts/batch_convert.py --list-templates

# 转换当前目录所有 md 文件
python3 <skill-path>/scripts/batch_convert.py "*.md"

# 递归转换项目文档
python3 <skill-path>/scripts/batch_convert.py "./docs/**/*.md"

# 使用特定模板并指定输出目录
python3 <skill-path>/scripts/batch_convert.py "*.md" \
  --template code-highlight \
  --output-dir ./pdf-output/

# 禁用自动检测，强制使用默认模板
python3 <skill-path>/scripts/batch_convert.py "*.md" --no-auto-detect

# 传递额外参数给 md2pdf
python3 <skill-path>/scripts/batch_convert.py "*.md" \
  --md-arg '--extras' \
  --md-arg 'pymdownx.emoji'
```

## 故障排除

### 问题：md2pdf 命令未找到

**解决方案**：
```bash
# 重新安装
pip install "md2pdf[cli]" --break-system-packages

# 或使用 Python 模块方式
python3 -m md2pdf -i document.md
```

### 问题：中文显示为方框或乱码

**原因**：缺少中文字体

**解决方案**：
```bash
# Ubuntu/Debian
sudo apt install fonts-noto-cjk fonts-wqy-microhei

# macOS
brew install font-noto-sans-cjk

# 检查可用字体
fc-list :lang=zh
```

### 问题：WeasyPrint 导入错误

**原因**：缺少系统依赖

**解决方案**：
```bash
# Ubuntu/Debian
sudo apt install libpango1.0-dev libcairo2-dev libffi-dev

# macOS
brew install pango cairo
```

### 问题：PDF 生成失败

**排查步骤**：
1. 检查 Markdown 语法是否正确
2. 检查 CSS 文件路径是否正确
3. 检查是否有图片路径错误
4. 查看详细错误信息：`md2pdf -i doc.md 2>&1`

### 问题：样式不生效

**原因**：CSS 选择器或路径问题

**解决方案**：
- 确保 CSS 文件存在且可读
- 检查 CSS 语法是否正确
- 使用绝对路径指定 CSS 文件

## 依赖要求

### Python 包
- md2pdf >= 3.0
- WeasyPrint >= 60
- markdown >= 3.5
- pygments >= 2.20
- python-frontmatter >= 1.1

### 系统依赖
- Python 3.10+
- Pango（文本渲染）
- Cairo（图形渲染）
- 中文字体（可选但推荐）

## 示例工作流

### 1. 准备环境
```bash
# 检查环境
<skill-path>/scripts/setup.sh
```

### 2. 编写文档
```markdown
---
title: 项目文档
author: 张三
date: 2024-01-01
---

# 项目概述

这是一份中文技术文档...

## 代码示例

```python
print("Hello, World!")
```

## 表格

| 功能 | 状态 |
|------|------|
| 功能A | 完成 |
| 功能B | 进行中 |
```

### 3. 转换文档
```bash
# 使用中文现代模板
md2pdf --css <skill-path>/templates/chinese-modern.css -i project.md
```

### 4. 批量处理
```bash
# 转换整个文档库
python3 <skill-path>/scripts/batch_convert.py "./docs/**/*.md" \
  --template chinese-modern \
  --output-dir ./output/
```

## 注意事项

1. **图片路径**: 确保 Markdown 中的图片路径正确，建议使用相对路径
2. **中文字体**: 转换中文文档前建议安装 Noto CJK 或 Source Han 字体
3. **内存使用**: 批量转换大文件时，可适当减少 workers 数量
4. **CSS 优先级**: 自定义 CSS 会覆盖模板中的同名样式

## 参考资料

- [md2pdf GitHub](https://github.com/jmaupetit/md2pdf)
- [WeasyPrint 文档](https://doc.courtbouillon.org/weasyprint/)
- [Markdown 扩展](https://python-markdown.github.io/extensions/)
