---
name: academic-citation-database
description: Local citation vector database — PDF text extraction → sentence embedding → vector similarity search for automatic citation matching
tool_type: python
primary_tool: chromadb + sentence-transformers + jieba
---

# Local Citation Vector Database

本地引文向量数据库——实现"文段→论文"的自动溯源引用。

## Architecture

```
PDF入库：
  论文 PDF
    → 标准解析（doc-parser/parse_pdf.py）
    → 结构化文本（段落 + 句子边界保留）
    → jieba 分句 + 清洗
    → BGE-small-zh 嵌入（384维）
    → 写入 Chroma 向量库
    → 每条向量关联：BibTeX key + PDF路径 + 原文片段

写作匹配：
  用户文段 / 选中文字
    → jieba 分词
    → BGE-small-zh 嵌入
    → 向量相似度 Top-K
    → 返回匹配结果（原文 + 论文信息 + BibTeX key）
    → 用户确认 → 插入 [@citekey]
```

## Dependencies

| 工具 | 安装 | 用途 |
|------|------|------|
| chromadb | `pip install chromadb` | 向量数据库 |
| sentence-transformers | `pip install sentence-transformers` | 嵌入模型 |
| jieba | `pip install jieba` | 中文分词 |
| PyMuPDF | `pip install PyMuPDF` | PDF 文本提取 |

## 嵌入模型选择

| 模型 | 维度 | 语言 | 大小 | 推荐场景 |
|------|------|------|------|----------|
| `BAAI/bge-small-zh-v1.5` | 384 | 中文为主 | ~33MB | **默认推荐**，轻量够用 |
| `BAAI/bge-base-zh-v1.5` | 768 | 中文为主 | ~110MB | 精度更高，资源够时用 |
| `shibing624/text2vec-base-chinese` | 768 | 中文 | ~110MB | 中文语义匹配 |
| `paraphrase-multilingual-MiniLM-L12-v2` | 384 | 多语言 | ~120MB | 中英混合论文 |

**推荐**：`BAAI/bge-small-zh-v1.5` — 384维，33MB，本地 CPU 跑得动，对中文论文足够。

## 数据库设计

### 集合结构（Chroma Collection）

```python
collection = client.create_collection(
    name="papers",
    embedding_function=bge_embedding
)

# 每条记录的 metadata:
{
    "bibtex_key": "lin2025",       # BibTeX 引用键
    "title": "文章标题",
    "authors": "作者A, 作者B",
    "year": "2025",
    "journal": "期刊名",
    "pdf_path": "papers/lin2025.pdf",  # 源文件路径
    "section": "引言",              # 来源章节（如有）
    "page_num": 1,                  # 页码
    "sentence_index": 5,            # 段落内句子索引
}
```

### 索引规模

| 论文数量 | 向量数（每篇约500句） | 存储空间 |
|----------|----------------------|----------|
| 100篇 | ~50,000条 | ~150MB |
| 500篇 | ~250,000条 | ~750MB |
| 1000篇 | ~500,000条 | ~1.5GB |

本地 SQLite 级别，无需部署服务。

## API 设计

### 入库

```python
def add_paper(pdf_path: str, bibtex_key: str, metadata: dict):
    """提取 PDF 文本、分句、嵌入、写入向量库"""
    text = parse_pdf(pdf_path)          # doc-parser 输出
    sentences = split_sentences(text)    # jieba 分句
    embeddings = embed(sentences)        # BGE 嵌入
    collection.add(
        ids=[f"{bibtex_key}-{i}" for i in range(len(sentences))],
        embeddings=embeddings,
        metadatas=[{**metadata, "sentence_index": i} for i in range(len(sentences))],
        documents=sentences
    )
```

### 搜索

```python
def search(query: str, k: int = 5) -> list[dict]:
    """搜索相似文段，返回 Top-K 匹配"""
    query_emb = embed([query])
    results = collection.query(
        query_embeddings=query_emb,
        n_results=k
    )
    return [
        {
            "text": doc,                    # 原文片段
            "bibtex_key": meta["bibtex_key"],
            "title": meta["title"],
            "confidence": distance,
        }
        for doc, meta, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        )
    ]
```

### 推荐引用

```python
def suggest_citation(text: str) -> list[dict]:
    """
    给定一段文字，推荐应该引用的论文。
    返回按置信度排序的引用建议。
    """
    matches = search(text, k=5)
    return [
        {
            "cite_key": m["bibtex_key"],
            "matched_text": m["text"][:100] + "...",
            "confidence": m["confidence"],
        }
        for m in matches
        if m["confidence"] > 0.7  # 置信度阈值
    ]
```

## 文本预处理

### 中文分句

```python
import re

def split_sentences(text: str) -> list[str]:
    """中文分句：句号、问号、感叹号、引号闭合"""
    # 保留 .（英文句号）、。？！等结束符
    sentences = re.split(
        r'(?<=[。！？?!])\s*',
        text.replace('\n', ' ')
    )
    return [s.strip() for s in sentences if len(s.strip()) > 10]
```

### 清洗规则

- 移除页眉页脚（页码、标题头）
- 合并断行（英文单词 hyphenation）
- 过滤过短片段（<10字符）
- 过滤表格/公式（纯符号行）

## 与其他模块集成

```
           doc-parser/                     citation-database/
PDF ──► parse_pdf.py ──► 结构化文本 ──► 分句→嵌入→入库
              │                                │
              │                           search() ──► 引用建议
              │                                │
              ▼                                ▼
         Markdown 写作 ←─────────── [@citekey] 自动插入
```

## 工具检查

```bash
# 检查 chromadb
python -c "import chromadb; print(chromadb.__version__)"

# 检查 sentence-transformers
python -c "import sentence_transformers; print(sentence_transformers.__version__)"

# 检查 jieba
python -c "import jieba; print(jieba.__version__)"

# 检查 PyMuPDF
python -c "import fitz; print(fitz.__doc__)"
```

## 已知限制

1. **首次嵌入慢**：BGE 模型首次加载需要下载（~33MB），后续缓存
2. **扫描件 PDF 不支持**：需先通过 OCR（如 ocrmypdf）转为文本 PDF
3. **图表内容不提取**：PyMuPDF 只提取文本层
4. **匹配精度依赖语种**：中英混合论文需选择合适的嵌入模型
