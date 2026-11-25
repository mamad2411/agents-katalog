---
name: technical-research-report
description: "Write structured technical research reports for internship/assignment tasks — market research, algorithm documentation, exchange analysis. Covers formatting conventions, PDF extraction, and the paired Mermaid+Code block pattern."
version: 1.0.0
---

# Technical Research Report — Authoring Skill

For internship/assignment research reports on quantitative finance topics (exchanges, trading algorithms, market structure).

## When to Use

- User requests a research report on exchanges, trading venues, algorithms
- Task involves documenting algorithms with code examples
- Reference document is provided as image-based PDF

## Workflow

### 1. Gather Reference Material

- Read all provided PDFs and email instructions
- For image-based PDFs (Canva/PPTX exports with no extractable text):
  1. `python3 -c "import fitz; doc=fitz.open('path.pdf'); [doc[i].get_pixmap(dpi=300).save(f'page_{i+1}.png') for i in range(len(doc))]"`  
  2. Use `vision_analyze` on each PNG to extract text
  3. Clean up temp images afterward
- For text-based PDFs: use `fitz`'s `page.get_text()` directly

### 2. Plan First

- Write a `plan.md` covering all sections from the task requirements
- Confirm with user before writing the full report

### 3. Report Structure

Each section should follow this hierarchy when applicable:

```
## Section Number — Title

**Definition / Description:** 一句话概括
**Use case:** 何时使用

**Parameters table:** (if applicable)
| 参数 | 说明 |
|------|------|

```mermaid
flowchart TD
    ...decision flow...
```

```python
class AlgorithmName:
    def run(self, order):
        ...implementation...
```

### 4. Formatting Conventions

| Situation | Preferred Format |
|-----------|-----------------|
| Comparisons (A vs B) | Markdown table with aspect rows |
| Lists of issues/features | Dot list (`- **Title** — description`) |
| Algorithm documentation | Mermaid flowchart + Python code block pair |
| Numbered process steps | Numbered list (1. 2. 3.), NOT code block |
| Time ranges | `9:30 AM – 4:00 PM ET` (AM/PM with ET suffix) |
| Similar entities (Nasdaq/NYSE) | **Consolidate** into one row/entry, say "both are the same" |
| Language | Chinese正文, English terms in parentheses |
| Broker comparison | 5-column table: `维度 | Side A | 后果 | Side B | 后果`. Each row shows one dimension, both implementations, and consequences |

### 5. "我说你做" Interaction Pattern

When the user gives formatting corrections:
- Execute immediately — do NOT explain, ask, or justify
- Make the change, confirm briefly, wait for next instruction
- Common corrections received: "改中文", "用dot list", "合并两个", "写mermaid+python"

## Pitfalls

- **Image-based PDFs** are silent failures for `read_file` — always check with `fitz` if the extracted text is empty or garbled, then fall back to vision_analyze
- **eFX Algo Strategy Guide** style documents have precise parameter definitions — must cite exactly, not paraphrase
- **Algorithm definitions** in reference docs override your general knowledge — always read first, write second
- **Python code blocks** in the report must pass `ast.parse` before calling done — silently broken code is worse than no code
- **Remove temp PNG files** after extraction to keep the working directory clean
- **Don't separate similar entities** (Nasdaq vs NYSE) unless the task explicitly asks for differences

## Related

- `references/infra-benchmark-report.md` — slide format for infrastructure/tool benchmarking reports (DB comparison, performance analysis) with icon conventions, data representation, and code reference patterns
