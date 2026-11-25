---
name: zx-present
description: 演讲铸造器（Outline-Faithful）。基于 org-mode/Markdown outline 层级 1:1 视觉化呈现：色块大字、ultra-bold 错位，原文不动只做美化。支持 black/red/yellow 主题和 --cyber 终端风格。Use when user says '讲这个', 'present', '做成演讲', '呈现一下', '铸成演示', '做个 slides', '标语流', '宣言体', 'slogan', 'manifesto', '按 outline 美化'. 输出单文件 HTML 到 ~/Downloads/.
user_invocable: true
version: '3.0.0'
---

# zx-present: 演讲铸造器

把 outline 铸成色块。它是视觉化渲染器，不是内容重写器。

## 这不是什么

- 不是 manifesto 提炼器：不抽「那句话」，不重组顺序
- 不是高桥流：不把所有内容削到单字
- 不是企业 PPT：不做规整版式、图标和装饰页

## 这是什么

*Outline -> 视觉化渲染器*：

- 输入：org-mode 文件、Markdown 文件、粘贴 outline、纯文本
- 输出：slogan-style HTML，1:1 保留 outline 结构
- 不抽提、不重写、不浓缩，只决定怎么把这一行或这一节渲染为页面

核心哲学：*Outline 是真理。Skill 是渲染器。*

铁律：

- 标题不改字
- 段落不改字
- 列表项不改字
- 表格不改结构
- 顺序不重排

唯一允许的「动」是物理分页：一段太长拆成多页，并保持视觉一致性。

## 参数

| 参数 | 说明 |
|---|---|
| `-r` / `--theme=red` | 红色主题，适合分享、宣言、keynote |
| `-b` / `--theme=black` | 黑色主题，适合沉思、论证、笔记 |
| `-y` / `--theme=yellow` | 黄色主题，适合反讽、警觉、批判 |
| `--cyber` | 黑底绿字 cyber-hacker 风 |

优先级：显式参数 > `#+filetags:` 推断 > 默认 black。

## Theme 推断

| filetags 含 | theme | 调性 |
|---|---|---|
| `:share:` `:talk:` `:manifesto:` `:keynote:` | red | 宣言、号召 |
| `:essay:` `:think:` `:learn:` `:note:` | black | 沉思、论证 |
| `:critique:` `:warn:` `:rant:` | yellow | 反讽、警觉 |
| 都没有 | black | 默认沉思调 |

## Org/Markdown -> 页面映射

### 标题层级

| 元素 | 页面 |
|---|---|
| `* 一级标题` / `# 一级标题` | emphasis 封面页 |
| `** 二级标题` / `## 二级标题` | theme 页，大字标题独占一页 |
| `*** 三级标题`+ | theme 页，字号降一档 |

### 内容元素

| 元素 | 页面行为 |
|---|---|
| 段落 | theme 页，按句号、换行、字数分页 |
| 列表项 | theme 页，每项一行，indent 按嵌套深度 |
| 表格 | 单页或多页，保留表格结构 |
| `*强调*` / `**强调**` | 自动高亮 |
| `~code~` / `=code=` / 反引号代码 | 自动高亮 |
| 引用 `> ...` | theme 页，indent 1 |
| 分隔符 `-----` | emphasis 休止页 |
| `#+begin_example` 或 fenced code | pre 页，monospace 渲染 |

## 分页规则

| 情形 | 拆法 |
|---|---|
| 段落 <= 30 字 | 单页 |
| 段落 30-80 字，含多句 | 每句一页 |
| 段落 > 80 字 | 按约 30 字一页拆，加 `...` 续标 |
| 列表 <= 4 项 | 单页展示 |
| 列表 5-8 项 | 拆 2 页，每页 3-4 项 |
| 列表 > 8 项 | 多页，每页约 4 项 |
| 表格 <= 6 行 | 单页 |
| 表格 > 6 行 | 多页，每页保留表头 |

拆完后扫一遍：同源拆分的页要像同一种东西，字号、缩进、底色都对齐。

## 视觉规范

色板：

```css
--c-black:  #1A1A1A;
--c-red:    #E63956;
--c-yellow: #FFD400;
--c-white:  #FFFFFF;
--c-gold:   #FFE082;
```

字体栈：

```css
"Helvetica Neue", "Arial Black", "PingFang SC", "Heiti SC", -apple-system, sans-serif
font-weight: 900
```

排版：

- 左对齐，不居中
- 页面垂直居中
- 大字撑屏
- 行内允许高亮，但 emphasis 页不做行内高亮
- 页脚保留页码和 subtitle，小而冷静

## JSON Schema

生成 `SLIDES_JSON` 时使用：

```jsonc
{
  "theme": "black|red|yellow|cyber",
  "title": "演讲标题",
  "subtitle": "副标题或日期",
  "slides": [
    {
      "lines": [
        {
          "indent": 0,
          "chunks": [
            { "t": "句子前段" },
            { "t": "高亮词", "hl": true },
            { "t": "句子后段" }
          ]
        }
      ]
    },
    {
      "emphasis": true,
      "lines": []
    },
    {
      "preTitle": "diagram",
      "pre": "..."
    }
  ]
}
```

## 执行

1. 获取内容：文件路径 -> 读取；粘贴 -> 直接用；URL -> 获取正文
2. 解析 outline：识别标题、列表、表格、强调、代码块、example 块
3. 推断 theme
4. 按映射规则生成 slides 数组
5. 读取 `assets/slogan_template.html`
6. 替换占位符：
   - `{{TITLE}}`
   - `{{SUBTITLE}}`
   - `{{THEME}}`
   - `{{SLIDES_JSON}}`
7. 写入 `~/Downloads/{name}.html`
8. 报告文件路径和翻页键：`->` `<-` `Space` `F` `Home` `End`

## 禁区

- 不抽 manifesto
- 不写新句子
- 不重排顺序
- 不删内容
- 不放图片或图标，色块就是图
- 不用过渡动画，硬切
- 不混用多个 theme
- 不擅自加 emphasis，只有一级标题、首末页、`-----` 是 emphasis
