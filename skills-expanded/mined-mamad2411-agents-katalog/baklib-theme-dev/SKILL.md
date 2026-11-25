---
name: baklib-theme-dev
description: >-
  Baklib 站点主题（模板）开发：Liquid 目录与命名、对象与指令/过滤器、静态页 URL、seeds 与迁移；并含「新建主题脚手架」（themes/ 目录与最小文件）与「参考站复刻工作流」（须确认门、质检清单）。在用户编写或修改 .liquid、新建模板、复刻参考站、或排查模板语法与变量时使用；详规见 references/。
---

# Baklib 模板开发

Baklib 站点前台使用 **[Liquid](https://shopify.github.io/liquid/)** 模板（与 Shopify 模板体系相近）。模板作者通过 **对象（变量）**、**指令**（控制逻辑，官方称 Tag）、**过滤器**（转换输出）组合页面。

## 术语

| 术语 | 含义 |
|------|------|
| 对象 | 在 `{{ }}` 中输出的变量或属性，如 `{{ site.name }}` |
| 指令 | 在 `{% %}` 中控制流程；本文称「指令」以免与站点内容「标签」混淆 |
| 过滤器 | 在 `{{ }}` 内用 `\|` 连接，如 `{{ site.pages \| order_by: "-published_at" }}` |

## 工作流（按需阅读）

| 场景 | 文档 |
|------|------|
| 在产品仓库中**新建** `themes/[scope]/[name]/` 并生成最小文件 | [create-theme-scaffold.md](references/create-theme-scaffold.md) |
| **复刻参考网站**（分析、适配、分期落地、质检；多步须先确认） | [website-cloning-workflow.md](references/website-cloning-workflow.md) |

## 文档索引（`references/`）

按需打开下列文件获取完整表格与示例：

| 文件 | 内容 |
|------|------|
| [directory-and-naming.md](references/directory-and-naming.md) | 主题目录、`templates`/`layout`/`snippets`/`statics`/`assets`/`config`/`locales`/`src` 与文件命名 |
| [liquid-tags.md](references/liquid-tags.md) | 页面模板与布局中的自定义指令、`render`、`form_tag`、`track_event`、`paginate_tag`、`query`、`search` 等 |
| [shared-snippets-source.md](references/shared-snippets-source.md) | `{% render '@shared/…' %}` 三枚内置片段与仓库 **`themes/shared/snippets/_*.liquid` 原文一致**，便于复制改写 |
| [objects-and-drops.md](references/objects-and-drops.md) | 全局变量、按场景传入的变量、`site` / `page` / `tag` / `search` / `paginate` 等对象 |
| [filters.md](references/filters.md) | 产品提供的自定义过滤器（含站点扩展） |
| [limits-and-security.md](references/limits-and-security.md) | 主题名规则、分页上限、`strict_filters`、反向代理与路径前缀 |
| [seeds-and-migrations.md](references/seeds-and-migrations.md) | `seeds/` 初始化数据与 `migrations/` 主题迁移 |

## 能力边界

- **说明对象**：面向在 Baklib 站点主题中编写 Liquid 的开发者；**不**描述 Baklib 应用后台或 Rails 实现细节。
- **与标准 Liquid 的关系**：除下列自定义能力外，可使用 [Liquid 标准语法与内置过滤器](https://shopify.github.io/liquid/)。
- **版本差异**：具体站点是否开启登录、搜索、反馈、AI 等功能以租户配置为准；模板中应对空值做判断（如 `{% if current_user %}`）。

## 快速示例

```liquid
{% layout "theme" %}
<h1>{{ site.name }}</h1>
{% for p in site.pages | limit: 5 %}
  <a href="{{ p.path }}">{{ p.link_text }}</a>
{% endfor %}
```
