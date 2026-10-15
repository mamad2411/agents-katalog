---
name: literature-reader
description: 阅读、分析并总结学术文献（PDF论文），生成结构化的文献概要笔记。核心能力：论文元信息提取、研究问题识别、方法论梳理、实验结果分析、个人评价生成，以及多篇文献横向对比。支持中英文论文、单篇精读与批量文献综述。当用户提供 PDF 论文文件、要求阅读文献、总结论文、文献综述、论文概要、论文精读、paper summary、paper review、读论文、读 paper、帮我看看这篇论文、分析这篇文章、这篇论文讲了什么、论文的方法是什么、帮我做文献笔记、批量读论文、对比这几篇论文时使用此 skill。处理 .pdf 格式文件。
metadata:
  author: huziyu
  version: 1.1.0
compatibility: 需要 macOS 或 Linux 环境。Cursor 内置 Read 工具可直接读取 PDF，大多数场景无需额外依赖。当 Read 工具无法正常处理 PDF 时，备选方案需 Python 3 和 pdfplumber 库，详见 references/pdf-extract.md。
---

# Literature Reader — 文献阅读与概要生成

## 指令

### Step 1: 获取 PDF 内容

**首选方式：** 使用 Cursor 内置 Read 工具直接读取 PDF 文件。

```
Read tool → path: "/path/to/paper.pdf"
```

Read 工具会自动将 PDF 转换为文本。如果 PDF 过大被截断，分段读取：

```
Read tool → path: "/path/to/paper.pdf", offset: 1, limit: 200
Read tool → path: "/path/to/paper.pdf", offset: 201, limit: 200
```

**备选方式：** 若 Read 工具无法读取 PDF（返回空内容、乱码、严重截断），或遇到扫描件、复杂排版等情况，请查阅 [PDF 文本提取指南](references/pdf-extract.md) 使用备选提取脚本。

快速使用：

```bash
pip3 install pdfplumber  # 首次使用需安装
python3 ~/.cursor/skills/literature-reader/scripts/extract_pdf.py "/path/to/paper.pdf" --output /tmp/paper_text.txt
```

预期输出：终端显示 `Extracted text saved to: /tmp/paper_text.txt`，随后用 Read 工具读取该文件。完整参数说明、判断标准和故障排查见 [references/pdf-extract.md](references/pdf-extract.md)。

### Step 2: 内容分析

按以下维度逐一分析提取到的文本：

1. **元信息提取** — 标题、作者、机构、发表年份、期刊/会议
2. **研究问题识别** — 论文试图回答什么问题，解决什么痛点
3. **方法论梳理** — 使用了什么研究方法、技术路线、实验设计
4. **核心贡献归纳** — 论文的主要创新点和学术贡献（通常在 Introduction 末尾或 Abstract 中明确列出）
5. **实验与结果** — 关键实验设置、数据集、指标、定量结果
6. **局限性与未来方向** — 作者承认的不足、提出的后续工作

### Step 3: 生成文献概要

使用模板生成结构化输出。模板见 [summary-template.md](references/summary-template.md)。

输出格式为 Markdown 文件，文件名建议：`[第一作者姓氏]_[年份]_[关键词缩写].md`

### Step 4: 质量检查

生成概要后进行自查：

- [ ] 元信息（标题、作者、年份）是否准确
- [ ] 研究问题是否清晰表述
- [ ] 方法描述是否抓住了核心技术路线而非细枝末节
- [ ] 核心贡献是否与论文 Abstract/Introduction 一致
- [ ] 关键数据和结论是否有具体数值支撑
- [ ] 个人评价是否客观且有理有据

## 特殊场景处理

### 批量文献阅读

当用户提供多篇论文时：

1. 逐篇按上述流程处理
2. 在最后额外输出一份 **横向对比表**，包含：标题、年份、方法、数据集、核心指标、主要贡献
3. 简要说明各论文之间的关系（互补/竞争/递进）

横向对比表模板见 [summary-template.md](references/summary-template.md) 底部。

### 特定章节深读

当用户只关心论文某一部分（如方法论、实验结果）时：

1. 仅展开该部分的详细分析
2. 其余部分保持一句话概述
3. 对关键公式、算法伪代码进行解读

### 中文论文

中文论文使用中文输出概要。对中文论文中引用的英文术语，保留原文并在括号内标注，如：注意力机制（Attention Mechanism）。

## 输出规范

- 文献概要长度：1000–2000 字（视论文复杂度调整）
- 语言：与论文语言一致，或遵从用户指定语言
- 格式：Markdown，使用清晰的层级标题
- 关键术语首次出现时标注英文原文
- 数据和结论必须标注出处章节（如 "见 Table 3" "Section 4.2"）

## 示例

### 示例 1：单篇论文精读

用户说：「帮我读一下这篇论文 /Users/me/papers/attention.pdf」
操作：
1. 使用 Read 工具读取 PDF 内容
2. 按 Step 2 维度逐一分析
3. 按模板生成完整文献概要
结果：输出结构化的 Markdown 概要文件

### 示例 2：批量对比

用户说：「对比一下这三篇论文 /papers/a.pdf /papers/b.pdf /papers/c.pdf」
操作：
1. 逐篇读取并生成概要
2. 输出横向对比表
3. 分析论文间的互补/递进/竞争关系
结果：三份独立概要 + 一份横向对比分析

### 示例 3：章节深读

用户说：「这篇论文的方法部分具体是怎么做的？」
操作：
1. 读取 PDF 并定位方法论章节
2. 详细解读技术路线、关键公式和算法
3. 其余章节一句话概述
结果：聚焦方法论的深度分析

## 故障排查

### Read 工具读取 PDF 为空或乱码
原因：PDF 为扫描件（图片格式）或使用了特殊编码
解决方案：改用备选提取脚本，详见 [PDF 文本提取指南](references/pdf-extract.md)

### PDF 内容被截断
原因：PDF 页数过多，单次读取超出限制
解决方案：
1. 使用 Read 工具分段读取，每次 200 行，直到覆盖全部内容
2. 或使用备选提取脚本的 `--pages` 参数按范围提取，详见 [references/pdf-extract.md](references/pdf-extract.md)

### pdfplumber 安装失败或脚本报错
详见 [PDF 文本提取指南 - 故障排查](references/pdf-extract.md) 中的完整排查步骤
