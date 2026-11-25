---
name: wordfreq
description: |
  词频分析助手。当用户需要统计文档词频、生成词云图、提取关键词、分析文本特征与词性分布时触发，支持 Word/PDF/EPUB/TXT/HTML 格式。This skill analyzes document word frequency, generates word clouds and charts, and extracts keywords via TF-IDF. Trigger on "词频""词频统计""词云""高频词""关键词提取""文本分析""分析这份文档的词频""词性分布""共现分析""文档主题"。
version: 1.0.0
author: 涛涛
license: MIT
display-name: 文本词频
category: 评价考情
homepage: https://github.com/ichangting/taotao-skills/tree/main/skills/wordfreq
---

# 词频分析统计技能

## 技能定位

本技能对用户上传的文档进行词频统计分析，输出结构化词频数据与可视化图表，并支持基于 TF-IDF 的关键词提取。适用于文本内容分析、教学材料研究、写作风格分析与文档主题识别。

---

## 支持的文档格式

| 格式 | 扩展名 | 处理方式 |
|------|--------|----------|
| Word 文档 | .docx, .doc | python-docx 提取 |
| PDF 文档 | .pdf | pdfplumber 提取 |
| EPUB 电子书 | .epub | ebooklib 提取 |
| 纯文本 | .txt, .md | 直接读取 |
| HTML 网页 | .html, .htm | BeautifulSoup 提取正文 |

---

## 核心功能

- **文本提取**：从 Word/PDF/EPUB/TXT/HTML 中提取纯文本，保留段落结构。
- **中文分词**：基于 jieba 分词，支持自定义词典与专有名词保护。
- **词频统计**：统计词频与占比，支持词性筛选与停用词过滤。
- **可视化输出**：生成词云图、柱状图、饼图等多种图表。
- **高级分析**：基于 TF-IDF 提取关键词，支持共现分析与主题识别。

---

## 处理流程

> 各步骤的 Python 实现代码见 `references/词频分析脚本参考.md`，停用词表见 `references/停用词表.md`，报告模板见 `references/输出报告模板.md`。

### Step 1: 接收文档

- 接收用户上传的文档，自动识别文档格式
- 确认分析参数（未指定则使用默认值，见"配置参数"）

**完成标准**：文档格式已识别；分析参数（top_n、是否过滤停用词、词性筛选等）已确定。

### Step 2: 文本提取

- 根据文档格式调用对应提取器（Word/PDF/EPUB/TXT/HTML）
- 保留段落结构，过滤页眉页脚、页码等噪音

**完成标准**：提取的纯文本非空；段落结构保留；无页码、页眉等噪音残留。

### Step 3: 中文分词

- 使用 jieba 精确模式对文本分词
- 按需加载自定义词典保护专有名词（人名、地名、机构名、术语）

**完成标准**：分词结果为词语列表；专有名词未被错误切分。

### Step 4: 停用词过滤

- 加载停用词表（`references/停用词表.md`），过滤停用词、标点、单字词、纯数字
- 按 `min_word_length` 与 `pos_filter` 进一步筛选

**完成标准**：过滤后词表不含停用词与标点；词长均 ≥ min_word_length；词性符合 pos_filter 设置。

### Step 5: 词频统计

- 统计每个词出现次数与占比
- 取 Top N 高频词，计算去重词数、平均词长等概览指标

**完成标准**：词频统计表生成；Top N 列表非空且按词频降序；占比之和合理。

### Step 6: 可视化生成

- 按用户启用的图表类型生成词云图、柱状图、饼图等
- 确保中文字体正确加载（缺失字体会显示方框）

**完成标准**：每张图表文件已生成且可正常打开；中文显示无方框；标题与坐标轴清晰。

### Step 7: 输出结果

- 套用 `references/输出报告模板.md` 生成结构化 Markdown 报告
- 嵌入统计概览、Top N 词表、词性分布、可视化图表、关键词与分析建议

**完成标准**：报告包含统计概览表与 Top N 词表；图表链接指向实际文件；分析建议基于数据且不少于 2 条。

---

## 配置参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| top_n | 显示前 N 个高频词 | 50 |
| min_freq | 最小词频阈值 | 2 |
| exclude_stopwords | 是否排除停用词 | 是 |
| wordcloud | 是否生成词云图 | 是 |
| barchart | 是否生成柱状图 | 是 |
| pos_filter | 词性筛选（n 名词/v 动词/a 形容词） | 全部 |
| min_word_length | 最小词长（过滤单字词） | 2 |

---

## 可视化图表类型

| 图表类型 | 说明 | 适用场景 |
|----------|------|----------|
| 词云图 | 词频越高字体越大 | 快速概览高频词 |
| 柱状图 | Top N 高频词 | 精确对比前 N 个词 |
| 饼图 | 词性分布 | 了解词汇构成 |
| 折线图 | 词频分布趋势 | 观察词频衰减规律 |
| 表格 | 完整词频列表 | 详细数据查阅 |

---

## 依赖与安装

- **必装**：`pip install jieba wordcloud matplotlib pandas python-docx pdfplumber ebooklib beautifulsoup4`
- **安装自检**：`python -c "import jieba, wordcloud, matplotlib, pandas, docx, pdfplumber; print('依赖就绪')"`
- **中文字体**：词云与图表需中文字体（如 `simhei.ttf`），缺失会导致中文显示为方框。

---

## 限制说明

1. 扫描版 PDF 需 OCR 支持，准确率可能受影响
2. 古籍文言文分词准确率低于现代文
3. 高度专业化文档需自定义词典以提升分词准确率
4. 超过 10MB 的大文档处理时间较长，敏感文档建议本地处理

---

## 课标对标

- 课标全文与章节锚点：回查 `curriculum-standard/references/义务教育语文课程标准（2022年版）.md`（全仓库单一数据源；2022 版全文 + 行号锚点见 [curriculum-standard](../curriculum-standard/SKILL.md)，词频分析可对标学段要求与学业质量 L735，判断高频词的教学优先级）。

*技能版本：1.0.0*
*适用场景：文本分析、教学研究、内容审核、写作辅助、文献研究*
