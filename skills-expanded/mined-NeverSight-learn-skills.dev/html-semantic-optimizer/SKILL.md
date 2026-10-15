---
name: html-semantic-optimizer
description: HTML语义化优化工具，将通用HTML标签（div、span）自动转换为语义化HTML5标签（header、nav、main、article、button等）。基于CSS类名智能识别元素语义角色，支持自定义规则配置。
---

# HTML 语义化优化工具

将通用HTML标签自动转换为语义化HTML5标签，提升代码可访问性和SEO友好性。

## 快速开始

### 安装依赖

```bash
pip install beautifulsoup4 lxml
```

### 命令行使用

```bash
# 优化单个文件
python scripts/optimize.py input.html -o output.html

# 试运行（预览结果）
python scripts/optimize.py input.html --dry-run

# 使用自定义规则
python scripts/optimize.py input.html --rules custom_rules.json

# 批量处理目录
python scripts/batch_optimize.py /path/to/html/files/ -o /output/dir/

# 批量处理（递归子目录）
python scripts/batch_optimize.py /path/to/html/files/ --recursive -o /output/dir/
```

### Python API 使用

```python
from html_optimizer import optimize_html

# 使用默认规则
result = optimize_html('<div class="btn">点击</div>')
# 输出: <button class="btn" type="button">点击</button>

# 自定义规则
from html_optimizer import RuleEngine, DOMTransformer

rules = [
    {"name": "侧边栏", "keywords": ["sidebar"], "target_tag": "aside", "priority": 8}
]

engine = RuleEngine(rules)
transformer = DOMTransformer(engine)
result = transformer.transform(html_content)
```

## 工作原理

工具通过分析元素的CSS类名，匹配预定义规则，将通用标签转换为对应的HTML5语义标签：

| 关键词 | 目标标签 | 示例 |
|--------|----------|------|
| `btn`, `button` | `<button>` | `<div class="btn">` → `<button>` |
| `link`, `nav-link` | `<a>` | `<div class="link">` → `<a>` |
| `header`, `top-bar` | `<header>` | `<div class="header">` → `<header>` |
| `nav`, `navbar` | `<nav>` | `<div class="nav">` → `<nav>` |
| `footer`, `bottom` | `<footer>` | `<div class="footer">` → `<footer>` |
| `main`, `content` | `<main>` | `<div class="main">` → `<main>` |
| `article`, `post` | `<article>` | `<div class="article">` → `<article>` |
| `sidebar`, `aside` | `<aside>` | `<div class="sidebar">` → `<aside>` |
| `section` | `<section>` | `<div class="section">` → `<section>` |

## 目录结构

```
html-semantic-optimizer/
├── SKILL.md                    # 技能说明文档
├── requirements.txt            # 依赖列表
├── html_optimizer.py           # 核心模块（规则引擎 + DOM转换器）
├── example_rules.json          # 示例规则配置
└── scripts/
    ├── optimize.py             # 单个文件优化脚本
    └── batch_optimize.py       # 批量处理脚本
```

## 配置规则

### 默认规则

脚本内置了9条默认规则，涵盖常见的语义化场景。

### 自定义规则

创建JSON文件定义自定义规则（参考 `example_rules.json`）：

```json
{
  "rules": [
    {
      "name": "侧边栏",
      "keywords": ["sidebar", "aside", "sidenav"],
      "target_tag": "aside",
      "priority": 8
    },
    {
      "name": "文章卡片",
      "keywords": ["card", "post-card"],
      "target_tag": "article",
      "priority": 7
    }
  ]
}
```

### 规则字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | 字符串 | 规则标识名称 |
| `keywords` | 字符串数组 | 匹配关键词列表（正则表达式，不区分大小写） |
| `target_tag` | 字符串 | 目标HTML标签 |
| `priority` | 整数 | 优先级（数值越大优先级越高） |

使用 `--rules` 参数加载自定义规则，同名规则会覆盖默认规则。

## 核心模块

### RuleEngine（规则引擎）

```python
from html_optimizer import RuleEngine

engine = RuleEngine()
engine.load_from_file('rules.json')
rule = engine.find_matching_rule(['main-header', 'container'])
```

### DOMTransformer（DOM转换器）

```python
from html_optimizer import RuleEngine, DOMTransformer

engine = RuleEngine(rules)
transformer = DOMTransformer(engine)
result = transformer.transform(html_content)
```

**自动处理：**
- 跳过 `<script>`、`<style>`、`<html>`、`<body>` 等特殊标签
- 为 `<button>` 添加 `type="button"`
- 为 `<a>` 添加 `href="#"`
- 保留所有原始属性

### 便捷函数

```python
from html_optimizer import optimize_html

# 一行代码完成优化
result = optimize_html(html_content)
```

## 批量处理

```bash
# 处理单个目录
python scripts/batch_optimize.py ./html_files/ -o ./optimized/

# 递归处理子目录
python scripts/batch_optimize.py ./html_files/ --recursive -o ./optimized/

# 并行处理（4个进程）
python scripts/batch_optimize.py ./html_files/ -o ./optimized/ --workers 4

# 试运行模式
python scripts/batch_optimize.py ./html_files/ -o ./optimized/ --dry-run
```

## 注意事项

1. **备份原始文件** - 转换前备份重要文件
2. **使用试运行模式** - `--dry-run` 预览结果而不保存
3. **测试自定义规则** - 先在测试文件上验证规则效果
4. **规则优先级** - 高优先级规则优先匹配

## 依赖

- Python 3.6+
- beautifulsoup4 >= 4.9.0
- lxml >= 4.6.0

安装命令：
```bash
pip install -r requirements.txt
```
