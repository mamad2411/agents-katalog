---
name: citation-finder
description: 智能文献引用检索工具。根据用户输入的学术文本（如论文Introduction、Discussion等），自动识别需要引用的陈述，并检索相关真实文献提供引用建议。
---

# Citation Finder - 智能文献引用检索

## 功能概述

本工具帮助学术写作者快速找到合适的引用文献。你只需输入文章段落（如 Introduction、Discussion 等），工具会自动：

1. **识别引用需求** - 分析文本中的定义、历史事实、统计数据、分子发现、分类标准等需要引用的陈述
2. **生成检索策略** - 为每个引用需求构建精准的学术检索词
3. **检索真实文献** - 调用 AI4Scholar API 在 Semantic Scholar、PubMed 等平台搜索相关论文
4. **输出引用报告** - 整理推荐文献的完整信息（标题、作者、期刊、DOI、PMID等）

## 适用场景

- 📝 撰写论文 Introduction 时需要支撑背景陈述
- 📊 Results/Discussion 部分需要对比已有研究
- 🔬 介绍研究方法时需要引用技术来源
- 📚 综述文章需要系统梳理领域文献

## 使用方法

### 方式一：Python 脚本直接运行

```bash
# 从文件读取文本
python citation_finder.py --input introduction.txt --output citations.md

# 直接输入文本
python citation_finder.py --text "Glomus tumors are rare perivascular neoplasms..." --output report.md

# 输出 JSON 格式（便于程序处理）
python citation_finder.py --input article.txt --format json --output citations.json
```

### 方式二：作为模块导入使用

```python
from citation_finder import analyze_text_for_citations, search_papers

# 分析文本
text = """你的文章内容..."""
citation_needs = analyze_text_for_citations(text)

# 对每个需求检索文献
for need in citation_needs:
    for query in need.suggested_queries:
        papers = search_papers(query, limit=5)
        # 处理结果...
```

## 支持的引用类型

工具能自动识别以下类型的陈述并提供引用建议：

| 类型 | 识别特征 | 示例 |
|:---|:---|:---|
| **定义/分类** | is defined as, characterized by, classified as | "Glomus tumors are rare perivascular neoplasms..." |
| **历史事实** | first described, since 1950, in 2020 | "since the first description in 1950..." |
| **流行病学** | rare, common, prevalence, incidence | "They arise most often in the distal extremities..." |
| **分子发现** | gene, mutation, fusion, pathway | "Recurrent NOTCH pathway rearrangements..." |
| **分类标准** | WHO classification, criteria, standard | "The current WHO classification defines..." |
| **技术方法** | sequencing, scRNA-seq, single-cell | "Single-cell RNA sequencing now permits..." |
| **临床行为** | indolent, malignant, prognosis | "Most tumors follow an indolent course..." |
| **肿瘤微环境** | tumor microenvironment, TME, stromal | "The TME is increasingly recognized..." |

## 输出格式

### Markdown 报告示例

```markdown
# 文献引用检索报告

## 1. Definition/Classification
**原文**: Glomus tumors are rare perivascular neoplasms that originate from modified smooth-muscle cells of the glomus body.

**推荐引用 (3篇)**:

### 1. Intermediate filament proteins and actin isoforms as markers for soft-tissue tumor differentiation and origin
- **作者**: Schurch W, Skalli O, Lagacé R, et al.
- **期刊**: American Journal of Pathology
- **年份**: 1990
- **被引**: 103次
- **PMID**: 2158236
```

## 配置文件

API 密钥已内置，无需额外配置。如需使用自己的 API 密钥，修改 `citation_finder.py` 中的：

```python
API_KEY = "your-api-key-here"
```

## 依赖要求

- Python 3.7+
- requests

```bash
pip install requests
```

## 注意事项

1. **引用质量**：工具推荐的文献基于算法匹配，建议人工审核确认相关性
2. **高影响力文献**：优先选择被引次数高、发表在权威期刊的文献
3. **最新进展**：对于快速发展的领域，建议补充检索最近1-2年的文献
4. **历史文献**：某些历史性陈述（如"首次报道于1950年"）可能需要查阅经典文献或教科书

## 工作流程图

```
用户输入文本
    ↓
[文本分析] → 识别引用需求（定义/历史/分子/临床等）
    ↓
[生成检索词] → 针对每个需求构建精准查询
    ↓
[API检索] → 调用 AI4Scholar 搜索相关文献
    ↓
[结果整合] → 去重、排序、格式化
    ↓
输出引用报告（Markdown/JSON）
```

## 相关工具

- **ai4scholar**: 底层文献检索 API
- **paper-download**: 下载检索到的 PDF 全文
