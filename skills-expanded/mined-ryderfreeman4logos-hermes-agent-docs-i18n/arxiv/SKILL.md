---
name: arxiv
description: "Search arXiv papers by keyword, author, category, or ID."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Research, Arxiv, Papers, Academic, Science, API]
    related_skills: [ocr-and-documents]
---

# arXiv研究功能

通过免费的REST API从arXiv搜索并获取学术论文。无需API密钥，也无需额外依赖——只需使用curl即可。

## 快速参考

| 操作 | 命令 |
|------|------|
| 搜索论文 | `curl "https://export.arxiv.org/api/query?search_query=all:QUERY&max_results=5"` |
| 获取特定论文 | `curl "https://export.arxiv.org/api/query?id_list=2402.03300"` |
| 阅读摘要（网页版） | `web_extract(urls=["https://arxiv.org/abs/2402.03300"])` |
| 阅读完整论文（PDF版） | `web_extract(urls=["https://arxiv.org/pdf/2402.03300"])` |

## 论文搜索

该API返回Atom XML格式的数据。可使用`grep`/`sed`进行解析，或通过`python3`处理以获得整洁的输出结果。

### 基本搜索

```bash
curl -s "https://export.arxiv.org/api/query?search_query=all:GRPO+reinforcement+learning&max_results=5"
```

### 清理输出（将 XML 解析为易读格式）

```bash
curl -s "https://export.arxiv.org/api/query?search_query=all:GRPO+reinforcement+learning&max_results=5&sortBy=submittedDate&sortOrder=descending" | python3 -c "
import sys, xml.etree.ElementTree as ET
ns = {'a': 'http://www.w3.org/2005/Atom'}
root = ET.parse(sys.stdin).getroot()
for i, entry in enumerate(root.findall('a:entry', ns)):
    title = entry.find('a:title', ns).text.strip().replace('\n', ' ')
    arxiv_id = entry.find('a:id', ns).text.strip().split('/abs/')[-1]
    published = entry.find('a:published', ns).text[:10]
    authors = ', '.join(a.find('a:name', ns).text for a in entry.findall('a:author', ns))
    summary = entry.find('a:summary', ns).text.strip()[:200]
    cats = ', '.join(c.get('term') for c in entry.findall('a:category', ns))
    print(f'{i+1}. [{arxiv_id}] {title}')
    print(f'   Authors: {authors}')
    print(f'   Published: {published} | Categories: {cats}')
    print(f'   Abstract: {summary}...')
    print(f'   PDF: https://arxiv.org/pdf/{arxiv_id}')
    print()
"
```

## 搜索查询语法

| 前缀 | 检索字段 | 示例 |
|------|----------|---------|
| `all:` | 所有字段 | `all:transformer+attention` |
| `ti:` | 标题 | `ti:large+language+models` |
| `au:` | 作者 | `au:vaswani` |
| `abs:` | 摘要 | `abs:reinforcement+learning` |
| `cat:` | 类别 | `cat:cs.AI` |
| `co:` | 评论 | `co:accepted+NeurIPS` |

### 布尔运算符

```
# AND (default when using +)
search_query=all:transformer+attention

# OR
search_query=all:GPT+OR+all:BERT

# AND NOT
search_query=all:language+model+ANDNOT+all:vision

# Exact phrase
search_query=ti:"chain+of+thought"

# Combined
search_query=au:hinton+AND+cat:cs.LG
```

## 排序与分页

| 参数 | 可选值 |
|-----------|---------|
| `sortBy` | `relevance`、`lastUpdatedDate`、`submittedDate` |
| `sortOrder` | `ascending`、`descending` |
| `start` | 结果偏移量（以0为起始） |
| `max_results` | 返回结果数量（默认10，最大30000） |

```bash
# Latest 10 papers in cs.AI
curl -s "https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=10"
```

## 获取特定论文

```bash
# By arXiv ID
curl -s "https://export.arxiv.org/api/query?id_list=2402.03300"

# Multiple papers
curl -s "https://export.arxiv.org/api/query?id_list=2402.03300,2401.12345,2403.00001"
```

## BibTeX 生成

在获取到某篇论文的元数据后，会自动生成对应的 BibTeX 条目：

{% raw %}
```bash
curl -s "https://export.arxiv.org/api/query?id_list=1706.03762" | python3 -c "
import sys, xml.etree.ElementTree as ET
ns = {'a': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
root = ET.parse(sys.stdin).getroot()
entry = root.find('a:entry', ns)
if entry is None: sys.exit('Paper not found')
title = entry.find('a:title', ns).text.strip().replace('\n', ' ')
authors = ' and '.join(a.find('a:name', ns).text for a in entry.findall('a:author', ns))
year = entry.find('a:published', ns).text[:4]
raw_id = entry.find('a:id', ns).text.strip().split('/abs/')[-1]
cat = entry.find('arxiv:primary_category', ns)
primary = cat.get('term') if cat is not None else 'cs.LG'
last_name = entry.find('a:author', ns).find('a:name', ns).text.split()[-1]
print(f'@article{{{last_name}{year}_{raw_id.replace(\".\", \"\")},')
print(f'  title     = {{{title}}},')
print(f'  author    = {{{authors}}},')
print(f'  year      = {{{year}}},')
print(f'  eprint    = {{{raw_id}}},')
print(f'  archivePrefix = {{arXiv}},')
print(f'  primaryClass  = {{{primary}}},')
print(f'  url       = {{https://arxiv.org/abs/{raw_id}}}')
print('}')
"
```
{% endraw %}

## 阅读论文内容

找到目标论文后，即可开始阅读：

```
# Abstract page (fast, metadata + abstract)
web_extract(urls=["https://arxiv.org/abs/2402.03300"])

# Full paper (PDF → markdown via Firecrawl)
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])
```

如需进行本地 PDF 处理，请使用 `ocr-and-documents` 技能。

## 常见分类

| 分类 | 字段 |
|------|------|
| `cs.AI` | 人工智能 |
| `cs.CL` | 计算与语言（自然语言处理） |
| `cs.CV` | 计算机视觉 |
| `cs.LG` | 机器学习 |
| `cs.CR` | 加密与安全 |
| `stat.ML` | 机器学习（统计学） |
| `math.OC` | 最优化与控制 |
| `physics.comp-ph` | 计算物理学 |

完整列表：https://arxiv.org/category_taxonomy

## 辅助脚本

`scripts/search_arxiv.py` 脚本可处理 XML 解析，并输出整洁的结果：

```bash
python scripts/search_arxiv.py "GRPO reinforcement learning"
python scripts/search_arxiv.py "transformer attention" --max 10 --sort date
python scripts/search_arxiv.py --author "Yann LeCun" --max 5
python scripts/search_arxiv.py --category cs.AI --sort date
python scripts/search_arxiv.py --id 2402.03300
python scripts/search_arxiv.py --id 2402.03300,2401.12345
```

无依赖项——仅使用 Python 标准库。

```bash
# By arXiv ID
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.03300?fields=title,authors,citationCount,referenceCount,influentialCitationCount,year,abstract" | python3 -m json.tool

# By Semantic Scholar paper ID or DOI
curl -s "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1234/example?fields=title,citationCount"
```

### 获取论文的引用信息（哪些文献引用了它）

```bash
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.03300/citations?fields=title,authors,year,citationCount&limit=10" | python3 -m json.tool
```

### 从论文中获取引用信息（即该论文所引用的内容）

```bash
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.03300/references?fields=title,authors,year,citationCount&limit=10" | python3 -m json.tool
```

### 搜索论文（作为arXiv搜索的替代方案，返回JSON格式数据）

```bash
curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=GRPO+reinforcement+learning&limit=5&fields=title,authors,year,citationCount,externalIds" | python3 -m json.tool
```

### 获取论文推荐建议

```bash
curl -s -X POST "https://api.semanticscholar.org/recommendations/v1/papers/" \
  -H "Content-Type: application/json" \
  -d '{"positivePaperIds": ["arXiv:2402.03300"], "negativePaperIds": []}' | python3 -m json.tool
```

### 作者简介

```bash
curl -s "https://api.semanticscholar.org/graph/v1/author/search?query=Yann+LeCun&fields=name,hIndex,citationCount,paperCount" | python3 -m json.tool
```

### Semantic Scholar中的常用字段

`title`、`authors`、`year`、`abstract`、`citationCount`、`referenceCount`、`influentialCitationCount`、`isOpenAccess`、`openAccessPdf`、`fieldsOfStudy`、`publicationVenue`、`externalIds`（包含arXiv ID、DOI等信息）

---

## 完整的研究工作流程

1. **查找文献**：`python scripts/search_arxiv.py "你的研究主题" --sort date --max 10`
2. **评估影响力**：`curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:ID?fields=citationCount,influentialCitationCount"`
3. **阅读摘要**：`web_extract(urls=["https://arxiv.org/abs/ID"])`
4. **阅读完整论文**：`web_extract(urls=["https://arxiv.org/pdf/ID"])`
5. **查找相关研究**：`curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:ID/references?fields=title,citationCount&limit=20"`
6. **获取推荐文献**：向Semantic Scholar的推荐接口发送POST请求
7. **追踪作者信息**：`curl -s "https://api.semanticscholar.org/graph/v1/author/search?query=姓名"`

## 请求频率限制

| API | 请求频率 | 认证要求 |
|-----|----------|----------|
| arXiv | 约每3秒1次请求 | 无需认证 |
| Semantic Scholar | 每秒1次请求 | 无需认证（使用API密钥时可提升至每秒100次） |

## 注意事项

- arXiv返回的是Atom XML格式——建议使用辅助脚本或解析代码以获得整洁的输出结果
- Semantic Scholar返回的是JSON格式——可通过`python3 -m json.tool`命令进行格式化，便于阅读
- arXiv论文编号：旧格式为`hep-th/0601001`，新格式为`2402.03300`
- PDF文件地址：`https://arxiv.org/pdf/{id}`，摘要地址：`https://arxiv.org/abs/{id}`
- 若存在HTML版本，则地址为：`https://arxiv.org/html/{id}`
- 如需对本地PDF文件进行处理，可参考`ocr-and-documents`技能

## 论文编号的版本标识

- `arxiv.org/abs/1706.03762`始终指向**最新版本**的论文
- `arxiv.org/abs/1706.03762v1`则指向某个**特定的、不可更改的版本**
- 在生成引用时，请保留实际读取到的版本后缀，以避免引用内容出现偏差（后续版本的内容可能会发生较大变化）
- API的 `<id>` 字段会返回带版本标识的URL地址（例如：`http://arxiv.org/abs/1706.03762v7`）

## 被撤回的论文

论文在提交后也有可能被撤回。出现这种情况时：
- `<summary>`字段中会包含撤回通知（需留意“withdrawn”或“retracted”字样）
- 相关元数据可能会不完整
- 在将某篇文献视为有效论文之前，务必先查看其摘要内容
