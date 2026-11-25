---
name: academic-writing
description: Academic writing workflow with literature management, citation validation, LaTeX/MD pipelines, local citation vector database, multi-format citations (APA/IEEE/Chicago/MLA/Vancouver/GB-T-7714), and complete research-to-publication pipeline
category: academic
exposure: standard
---

# Academic Writing Skill

Comprehensive academic writing support for ExtendAI Lab. Covers the full pipeline: literature management → PDF parsing → citation database → writing → output generation.

## Mode Selection

**Academic Mode** (default for paper writing):
- Full academic rigor with citation validation, integrity checks, multi-stage review
- Use when: writing papers, literature reviews, research proposals

**Engineering Mode** (for software docs, READMEs, technical reports):
- Streamlined writing without excessive academic overhead
- Use when: writing documentation, technical specs, blog posts, README files
- Activate with: "engineering mode" or "technical writing"

## Architecture Overview

```
                    ┌─────────────────────────────────────┐
                    │        文献入库 Pipeline             │
 CNKI ──► cnki-parser ──┐                                │
 DOI ───► papis ────────┤                                │
 手动 ──► 直接导入 ────┼──► 统一 BibTeX 库 (.bib)        │
 Zotero ► Better BibTeX ┤                                │
                    └─────────────────────────────────────┘
                                       │
                                       ▼
                    ┌─────────────────────────────────────┐
                    │     PDF 解析 + 向量入库 Pipeline    │
 论文 PDF ──► doc-parser ──► 结构化文本                    │
               (PyMuPDF)     ├── 分句 → BGE 嵌入           │
                             └── 写入 Chroma 向量库        │
                    └─────────────────────────────────────┘
                                       │
                                       ▼
                    ┌─────────────────────────────────────┐
                    │        写作 + 输出 Pipeline          │
 管线A: MD ──► Python Direct ──► DOCX  ✅（v4 主力）      │
 管线B: MD ──► Pandoc ────────► DOCX  （快速草稿）        │
 管线C: MD ──► Pandoc ────────► HTML  （仅预览）          │
 管线D: TeX ──► xelatex+biber ─► PDF  （LaTeX 用户）      │
                    └─────────────────────────────────────┘
```

## Core Principles

1. **On-Demand Tool Checking** — Only check tools when the user needs to write a paper, not on every startup
2. **Main Pipeline: Python Direct (v4)** — MD → python-docx low-level XML with REF field codes (verified production)
3. **Pandoc Only for Drafts** — Pandoc 用于快速草稿，不用于最终输出
4. **HTML Only for Preview** — HTML 仅用于预览，**禁止** HTML→DOCX 管线
5. **PDF 解析标准化** — 统一走 doc-parser 脚本，不依赖模型自身解析能力
6. **本地引用数据库** — Chroma + BGE 向量库，实现文段→论文溯源
7. **Mode-Aware** — 自动检测学术/工程模式，避免过度学术化

## 学术诚信规则（强制执行）

本插件面向学术用户，学术诚信是不可妥协的底线。

### 核心原则
- **回答不一定是对的** — 你的判断和生成内容都可能有误。对所有结论保持怀疑，优先保证准确性。
- **审慎对待文献来源** — 无论是英文期刊还是中文期刊，都必须十分慎重。不轻信任何单一来源。
- **不保证 AI 生成内容的准确性** — AI 生成的内容无法被人类快速辨别真伪。你只能在力所能及的范围内减少问题。
- **必要时主动索要补充信息或证据** — 如果信息不足或无法验证，明确告知用户需要什么证据。

### 学术写作规则
- **不编造数据**：不虚构 DOI、作者、期刊信息、实验结果、图表编号、页码或任何可验证的学术信息。
- **标注来源**：对声明、参数、定量结果、数据集、图表等附加来源标签。区分「原文/已有数据」「用户确认内容」「根据上下文推断」「建议性扩展」四类信息。
- **审慎引用**：引用文献时，如果无法确认文献的真实性，明确标注「待验证」或「来源未确认」。
- **避免模糊用词**：避免「显著」「先进」「有效」「鲁棒」等模糊用词，代之以可测量的条件和对比基准。

### 生物学领域特别注意事项
近期国内生物学领域学术造假事件频发。在处理生物学相关任务时：
- 对实验数据和结论保持更高警惕
- 不轻信预印本或低影响力期刊的结果
- 对统计分析结果进行合理性检查
- 明确标注任何无法验证的数据或结论

### 回答风格
- 避免过分夸赞用户的输入或想法
- 你的回答不一定是对的，用户的判断也不一定是对的
- 对待所有问题都要反复推敲，优先保证准确性
- 保持结构化输出，条理清晰

## Available Skills (Load on Demand)

| Skill | Location | Load command | Purpose |
|-------|----------|-------------|---------|
| `academic-cnki-parser` | `resources/academicSkills/citation/cnki-parser/` | `skill("academic-cnki-parser")` | CNKI 导出→BibTeX |
| `academic-cite-match` | `resources/academicSkills/citation/cite-match/` | `skill("academic-cite-match")` | `[[cite:keywords]]`→`[N]` 标记匹配 |
| `academic-md2docx` | `resources/academicSkills/formatting/md2docx/` | `skill("academic-md2docx")` | MD→DOCX 三管线指南 |
| `academic-latex-pipeline` | `resources/academicSkills/writing/latex-pipeline/` | `skill("academic-latex-pipeline")` | LaTeX 模板+编译 |
| `academic-citation-database` | `resources/academicSkills/writing/citation-database/` | `skill("academic-citation-database")` | 本地向量数据库 |
| `document-formatting` | `src/skills/document-formatting/` | `skill("document-formatting")` | DOCX 排版规范 v4 |
| `research-writing-skill` | `resources/academicSkills/writing/research-writing-skill/` | `skill("research-writing-skill")` | 论文写作、修改、润色、审稿回复 |
| `office-academic-skill` | `resources/academicSkills/office/office-academic-skill/` | `skill("office-academic-skill")` | 学术 Word/PPT 生成与编辑 |
| `scientific-toolkit-skill` | `resources/academicSkills/computing/scientific-toolkit-skill/` | `skill("scientific-toolkit-skill")` | 科研计算、MATLAB/Python、数据分析 |

## Citation Formats

| Format | Use Case | Example (Journal Article) |
|--------|----------|---------------------------|
| **GB/T 7714-2015** | 国内学位论文、中文期刊 | 张三, 李四. 人工智能研究综述[J]. 计算机学报, 2024, 47(1): 1-20. |
| **APA 7th** | 社会科学、心理学、教育学 | Smith, J., & Johnson, A. (2024). AI research review. *Journal of Computing*, 47(1), 1-20. |
| **IEEE** | 工程、计算机科学 | J. Smith and A. Johnson, "AI research review," *J. Comput.*, vol. 47, no. 1, pp. 1-20, 2024. |
| **Chicago** | 人文科学、历史学 | Smith, John, and Alice Johnson. "AI Research Review." *Journal of Computing* 47, no. 1 (2024): 1-20. |
| **MLA** | 文学、语言学 | Smith, John, and Alice Johnson. "AI Research Review." *Journal of Computing*, vol. 47, no. 1, 2024, pp. 1-20. |
| **Vancouver** | 医学、生物医学 | Smith J, Johnson A. AI research review. J Comput. 2024;47(1):1-20. |

### Format Selection Guide

| Target | Recommended Format |
|--------|-------------------|
| 国内学位论文 | GB/T 7714-2015 |
| 中文核心期刊 | GB/T 7714-2015 |
| SCI 期刊（理工科） | IEEE 或 APA 7th |
| SCI 期刊（社会科学） | APA 7th |
| SSCI/A&HCI | APA 7th 或 Chicago |
| 会议论文（IEEE） | IEEE |
| 会议论文（ACM） | APA 7th |
| 医学期刊 | Vancouver |

## Paper Structures

| Structure | Use Case | Sections |
|-----------|----------|----------|
| **IMRaD** | 实验研究、实证研究 | Introduction, Methods, Results, and Discussion |
| **Literature Review** | 综述论文 | Introduction, Search Strategy, Thematic Analysis, Discussion, Conclusion |
| **Theoretical Analysis** | 理论研究 | Introduction, Framework, Analysis, Discussion, Conclusion |
| **Case Study** | 案例研究 | Introduction, Case Description, Analysis, Discussion, Conclusion |
| **Policy Brief** | 政策研究 | Executive Summary, Background, Analysis, Recommendations |
| **Conference Paper** | 会议论文 | Introduction, Related Work, Method, Evaluation, Conclusion |

### Structure Selection Guide

| Research Type | Recommended Structure |
|---------------|----------------------|
| 实验研究 | IMRaD |
| 综述论文 | Literature Review |
| 理论研究 | Theoretical Analysis |
| 案例研究 | Case Study |
| 政策研究 | Policy Brief |
| 会议投稿 | Conference Paper |

## Tool Checking

Use `academic_check_tools()` to check available tools:

```typescript
// Check all
academic_check_tools()

// Check specific
academic_check_tools({ tools: ["pandoc", "papis", "python-docx", "xelatex", "officecli"] })
```

| Tool | Check command | Purpose |
|------|--------------|---------|
| `pandoc` | `pandoc --version` | MD→DOCX/BibTeX 处理 |
| `papis` | `papis --version` | 文献管理（DOI/arXiv 导入） |
| `python-docx` | `python -c "from docx import Document"` | DOCX 生成（v4 管线） |
| `PyMuPDF` | `python -c "import fitz"` | PDF 文本解析 |
| `xelatex` | `xelatex --version` | LaTeX 编译 |
| `biber` | `biber --version` | 参考文献处理 |
| `chromadb` | `python -c "import chromadb"` | 向量数据库 |
| `sentence-transformers` | `python -c "import sentence_transformers"` | 嵌入模型 |
| `jieba` | `python -c "import jieba"` | 中文分词 |
| `officecli` | `officecli --version` | Office 文档操作（Word/Excel/PPT） |

## Writing Workflows

### Workflow A: Markdown → DOCX (v4 Pipeline, 主力)

```markdown
1. 准备 Markdown 源文件（含 [N] 引用标记 + 有序列表参考文献）
2. 运行 pipeline A：python build_docx_ref_codes.py
3. 输出：DOCX 文件（REF field code + 自动编号 [1][2][3] 格式）
```

### Workflow B: LaTeX → PDF

```markdown
1. 准备 .tex 源文件（ctex + biblatex）
2. 运行编译管线：xelatex → biber → xelatex ×2
3. 输出：PDF 文件
```

### Workflow C: 文献入库

```markdown
1. 从 CNKI/Zotero/DOI 获取文献元数据
2. 统一导出为 .bib 文件
3. 下载 PDF 全文
4. 运行 doc-parser 提取文本 → 写入本地向量数据库
```

## Pipeline Comparison

| Feature | Pipeline A (Python Direct) | Pipeline B (Pandoc) | Pipeline D (LaTeX) |
|---------|---------------------------|---------------------|---------------------|
| **输出格式** | DOCX | DOCX | PDF |
| **引用** | REF field code ✅ | 静态超链接 ⚠️ | BibLaTeX ✅ |
| **编号** | Word 自动编号 `[1][2][3]` | 静态文本 | BibLaTeX 控制 |
| **中文排版** | 完全控制 ✅ | 依赖 template.docx | ctex 宏包 ✅ |
| **速度** | 中等 | 快 | 慢（多次编译） |
| **推荐场景** | **最终论文输出** | 快速草稿 | 需要 PDF 的 LaTeX 用户 |

## Reference Implementation

生产验证的 v4 脚本路径（Windows）：
```
F:\swxxx\scripts\build_docx_ref_codes.py
```

核心实现：
- Markdown 直接解析（正则分块）
- `{ REF ref-N \h }` field code 交叉引用
- 自定义 `word/numbering.xml` 实现 `[1]` 编号格式
- python-docx 底层 XML 操作（OxmlElement）
- `word/settings.xml` 注入 `updateFields`

## Future Enhancements (P2 — 暂不实现)

- `academic_detect_missing_citations()` — 基于向量库的文段缺失引用检测
- `academic_build_html_preview()` — 集成到 dashboard 的 HTML 预览
- OCR 兜底管线（ocrmypdf + tesseract）
- 更多 CSL 引文样式

## Research Pipeline (Academic Mode)

When in Academic Mode, follow this 6-stage pipeline:

### Stage 1: RESEARCH
- Literature search and collection
- Source verification (check DOI, author, journal)
- Annotated bibliography creation
- Research question refinement

### Stage 2: WRITE
- Outline creation based on paper structure
- Draft writing with citation placeholders
- Citation compliance check
- Bilingual abstract (if needed)

### Stage 3: REVIEW
- Self-review against checklist
- Citation verification (all DOIs exist?)
- Logical consistency check
- Methodology review

### Stage 4: REVISE
- Address review comments
- Update citations
- Improve clarity and flow
- Format compliance

### Stage 5: FINALIZE
- Select output format (MD/DOCX/LaTeX/PDF)
- Apply citation format
- Generate bibliography
- Final quality check

### Stage 6: SUMMARY
- Document the writing process
- Track collaboration quality
- Archive materials

## Integrity Verification

### Pre-Writing Checklist
- [ ] Research question is clear and specific
- [ ] Literature search is comprehensive
- [ ] Sources are verified (DOI exists, journal is legitimate)
- [ ] No fabricated data or citations

### Post-Writing Checklist
- [ ] All citations have valid DOIs or are marked "待验证"
- [ ] No plagiarized content
- [ ] Claims are supported by evidence
- [ ] Limitations are acknowledged
- [ ] AI assistance is disclosed (if required)

### Red Flags to Watch
- Suspiciously perfect results
- Citations that don't exist
- Claims without evidence
- Vague or unsubstantiated claims
- Copy-pasted content without attribution

## Mode-Specific Behavior

### Academic Mode (default for papers)
- Full integrity verification
- Citation validation required
- Multi-stage review process
- Detailed bibliography

### Engineering Mode (for technical docs)
- Streamlined process
- Focus on clarity and accuracy
- Minimal academic overhead
- Practical examples preferred

To activate Engineering Mode: "Use engineering mode for this document" or "This is a technical document, not a paper"
