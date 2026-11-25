---
name: zach-md-html
description: |
  已降级的 Markdown→HTML 兼容转换器。仅当用户明确要求“使用 zach-md-html”、或明确说“不要重组内容，只把现成 Markdown 机械转换成 HTML/套用旧主题”时使用。不要因为用户只说“输出成 HTML”“生成 HTML 报告”“把日常报告做成 HTML”“数据报告/交付报告”而触发；这些任务应由模型从原始资料直接组织并生成自包含 HTML。此 Skill 不负责数据可视化、工作面、自由设计、万物转 md、html 转 md 或 md 转 docx。
disable-model-invocation: true
---

# zach-md-html（兼容模式）

> 状态：**Deprecated / 非默认入口**
> 2026-07-15 起，日常报告和正式交付默认由模型从原始资料直接生成 HTML，不再先写 Markdown 再套模板。

## 保留它解决什么问题

只解决一种低成本兼容需求：

> 已经有一份结构确定的 Markdown；不需要重新分析、重组或可视化；只想快速得到一个可离线打开的 HTML。

这是一项机械转换能力，不是报告设计能力。

## 何时使用

仅在以下条件同时成立时使用：

1. 输入已经是现成 Markdown 文件；
2. 用户明确不需要重组内容；
3. 用户接受旧主题只改善字体、宽度、目录、表格和基础阅读体验；
4. 用户明确点名本 Skill，或明确要求机械转换。

## 何时不要使用

以下场景不要调用本 Skill：

- 用户只说“输出成 HTML”“生成 HTML 报告”；
- 日报、周报、分析报告、调研报告、方案、复盘或正式交付；
- 内容包含需要解释的数据、指标、比较、趋势或证据链；
- 需要摘要区、指标卡、图表、折叠证据、交互或打印交付；
- 需要根据内容重新安排信息层级；
- PDF / DOCX / PPTX / XLSX / URL 转 Markdown；
- HTML 转 Markdown；
- Markdown 转 DOCX；
- dashboard、workspace、free-design 或其他设计型页面。

这些任务应交给模型或对应的专业 Skill，从原始内容直接生成最终产物。

## 执行方式

优先直接使用稳定的 default 主题，不使用未实现的 workspace / free-design 声明。

```bash
python3 scripts/md_to_html.py input.md --theme report -o output.html
```

主题只按既有 Markdown 的阅读形态选择：

| 主题 | 适合 |
|---|---|
| `report` | 表格较多的既有报告 |
| `reading` | 纯文字长文 |
| `interactive` | 很长且需要目录导航的文档 |
| `article` | 普通文章 |
| `wechat` | 公众号富文本预览 |

不要调用 `--scene` 或 `--free-design`。当前脚本不会真正实现对应工作面，只会降级到默认渲染。

## 验收

转换后至少确认：

1. HTML 文件真实生成且可打开；
2. 标题、表格、链接和关键数字没有丢失；
3. 本地图片路径可用，或按需要嵌入；
4. 输出只是忠实转换，没有声称完成数据可视化或报告重构。

## 遗留资源边界

目录中的 `any_to_md.py`、`html_to_md.py`、`md_to_docx.py`、workspace/free-design references 和旧示例仅为历史兼容资源，不再由本 Skill 路由。不要据此扩大触发范围。

如这些遗留资源后续确认没有外部依赖，再单独清理；本次退役不删除脚本，以免破坏旧调用。
