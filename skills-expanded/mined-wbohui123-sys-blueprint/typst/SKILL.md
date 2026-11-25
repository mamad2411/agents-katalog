---
name: typst
description: 用 Typst 排版并导出 PDF。
disable-model-invocation: true
---

# Typst

用 `typst --version` 确认可用，`typst fonts` 查看当前可用字体。

## 用法

```bash
typst compile 稿.typ 出.pdf      # 出 PDF
typst watch 稿.typ 出.pdf        # 改一次自动重编（长活，走后台任务）
```

## 最小可用模板（中文，确认字体后使用）

```typst
#set text(font: "Songti SC", size: 11pt, lang: "zh")
#set page(margin: 2.5cm, numbering: "1")
#set par(justify: true, first-line-indent: 2em)

= 标题

正文。

== 小标题

- 列表一
- 列表二

#table(
  columns: 2,
  [表头甲], [表头乙],
  [内容一], [内容二],
)
```

## 坑

- 中文选用当前可用、包含所需汉字的字体；模板中的 `Songti SC` 按 `typst fonts` 结果替换，编译后检查缺字。
- **它出不了 Word。** 要 docx 走 pandoc。
- 语法跟 LaTeX / Markdown 都不一样，**别凭印象写**。不确定就先编译一个最小文件试。
