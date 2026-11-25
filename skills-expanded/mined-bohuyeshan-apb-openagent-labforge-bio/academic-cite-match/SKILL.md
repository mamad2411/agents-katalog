---
name: academic-cite-match
description: Match body text to bibliography entries and insert superscript [N] citation markers. Use when the user has a paper draft with [[cite:keywords]] markers and needs automatic citation insertion.
tool_type: python
primary_tool: jieba
---

# Academic Cite-Match

Match body text segments to bibliography entries and insert formatted
citation markers (`[1]`, `[2]`, etc.) with a GB/T 7714 reference list.

## Workflow

```
Input: draft.md with [[cite:keywords]] markers
                │
                ▼
  1. Parse [[cite:...]] markers from body text
  2. Match keywords to bibliography (.bib) entries
     - Layer 1: Title exact match
     - Layer 2: Keyword overlap (jieba segmentation + TF-IDF)
     - Layer 3: Semantic similarity (optional, requires text2vec)
  3. Assign sequential [N] numbers and deduplicate
  4. Append GB/T 7714 formatted reference list

Output: draft.md with [1][2] markers + reference section
```

## Usage

```bash
# Basic usage (keyword matching)
python scripts/cite_match.py draft.md --bib refs.bib -o output.md

# With semantic matching (requires text2vec)
python scripts/cite_match.py draft.md --bib refs.bib --semantic -o output.md

# Just generate reference list from .bib
python scripts/cite_match.py --bib refs.bib --refs-only
```

## Markdown Marker Syntax

AI writes markers in the body text where citations are needed:

```markdown
烯效唑处理后[[cite:烯效唑 番茄 上胚轴]]番茄上胚轴显著矮化。
赤霉素相关基因[[cite:赤霉素 GA 株高]]表达上调。
从李金哲等的工作中[[cite:李金哲 烯效唑]]可以得知...
```

The matching engine will:
- Parse `[[cite:keywords]]` into a search query
- Search the bibliography for the best match
- Replace with `[N]` superscript
- Add the reference to the end-matter list

## Matching Layers

| Layer | Method | Precision | Requires |
|-------|--------|-----------|----------|
| 1 | Title exact/keyword match | High | Nothing extra |
| 2 | TF-IDF keyword overlap (jieba) | Medium-High | `jieba` |
| 3 | Sentence embedding similarity | High | `text2vec-base-chinese` |

## Output Format

```markdown
## Body Text

烯效唑处理后[1]番茄上胚轴显著矮化。
赤霉素相关基因[2]表达上调。

## 参考文献

[1] 李金哲,刘斯超,王俊琪,等.烯效唑对番茄苗上胚轴的矮化作用及
     机制分析[J].农业生物技术学报,2026.
[2] 胡鑫.S型类受体蛋白激酶OsGRSK1通过赤霉素调控水稻株高和粒型
     的功能研究[D].河南农业大学,2025.
```

## Dependencies

- `jieba` — Chinese text segmentation (keyword matching)
- Optional: `sentence-transformers` — semantic matching layer
