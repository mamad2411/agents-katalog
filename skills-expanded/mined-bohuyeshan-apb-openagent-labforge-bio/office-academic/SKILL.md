---
name: office-academic-skill
description: Chinese-first academic Word and PowerPoint workflow for paper reading reports, thesis or group-meeting PPTs, editable DOCX/PPTX generation, Office file inspection, template matching, speaker notes, and layout quality checks. Use when the user asks to read papers into Word reports, create or polish PPT/PPTX, convert paper/thesis materials into slides, edit DOCX/PPTX, inspect Office files, or produce Chinese academic presentation/report deliverables. Preserve English paper titles, formulas, variable names, software commands, and references.
category: academic
exposure: tool
---

# Office Academic Skill

## Scope

Use this skill for:

- Word reports from PDFs, DOCX files, arXiv papers, journal articles, theses, and manuscripts.
- Chinese-first academic PPTs for literature reports, group meetings, courses, opening/midterm/defense presentations, and project presentations.
- Editable `.docx` and `.pptx` generation, inspection, repair, and style preservation.
- PPT template matching, native slide editing, speaker notes, and visual quality checks.

Do not use this skill for pure manuscript prose drafting without a Word/PPT deliverable; use `research-writing-skill` instead. Do not use it for MATLAB, Python analysis, statistics, or plotting unless those outputs are being inserted into Word/PPT.

## Recommended Tool: OfficeCLI

**OfficeCLI** is the preferred tool for Word/Excel/PowerPoint operations. It is a single-binary CLI that creates, reads, and modifies `.docx`/`.xlsx`/`.pptx` files without requiring Microsoft Office.

### Installation

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/iOfficeAI/OfficeCLI/main/install.sh | bash

# Windows (PowerShell)
irm https://raw.githubusercontent.com/iOfficeAI/OfficeCLI/main/install.ps1 | iex
```

### Key Commands

```bash
# Create
officecli create report.docx
officecli create deck.pptx
officecli create budget.xlsx

# Add content
officecli add report.docx / --type paragraph --prop text="Title" --prop style=Heading1
officecli add deck.pptx / --type slide --prop title="Q4 Results"
officecli add budget.xlsx / --type sheet --prop name="Data"

# Read/inspect
officecli view report.docx outline
officecli view deck.pptx html -o /tmp/deck.html
officecli get report.docx /body/p[1] --json

# Modify
officecli set report.docx /body/p[1]/r[1] --prop text="New Title"
officecli set deck.pptx '/slide[1]/shape[1]' --prop color=FF0000

# Validate
officecli validate report.docx
officecli view report.docx issues --json
```

### When to Use OfficeCLI vs python-docx

| Scenario | Tool | Reason |
|----------|------|--------|
| Create new Word/PPT/Excel | OfficeCLI | Single command, no Python setup |
| Edit existing Office files | OfficeCLI | Path-based element access |
| Complex data processing + Office | python-docx + pandas | Better for data pipelines |
| CI/CD document generation | OfficeCLI | Zero dependencies, single binary |
| Template-based batch reports | OfficeCLI `merge` | `{{key}}` placeholder replacement |

### Detection & Auto-Install

When this skill is loaded, check if OfficeCLI is available:

```bash
officecli --version
```

**If not installed**, suggest installation to the user:

> OfficeCLI is a recommended tool for high-quality Word/Excel/PowerPoint operations. It's a single binary with zero dependencies. Would you like me to install it globally?

**If user agrees**, install globally:

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/iOfficeAI/OfficeCLI/main/install.sh | bash

# Windows (PowerShell)
irm https://raw.githubusercontent.com/iOfficeAI/OfficeCLI/main/install.ps1 | iex
```

**When to suggest OfficeCLI:**
- User wants high-quality document output
- User has iterated multiple times with existing skills but quality is not satisfactory
- User asks for Word/PPT/Excel creation or editing
- User wants template-based batch document generation

## Language And Evidence

- Default to Chinese for explanations, Word report prose, slide text, outlines, and speaker notes.
- Preserve English titles, formulas, variables, model names, software commands, reference entries, and direct source labels.
- Distinguish `论文原文`, `图表/公式证据`, `代码或仿真结果`, `根据上下文推断`, and `建议`.
- Do not invent DOI, authors, journal details, experiment values, figure numbers, section names, page numbers, or conclusions.
- Attach source labels to claims, parameters, quantitative results, formula explanations, datasets, figures, limitations, and novelty statements.

## 学术诚信规则（强制执行）

本插件面向学术用户，学术诚信是不可妥协的底线。

### 核心原则
- **回答不一定是对的** — 你的判断和生成内容都可能有误。对所有结论保持怀疑，优先保证准确性。
- **审慎对待文献来源** — 无论是英文期刊还是中文期刊，都必须十分慎重。不轻信任何单一来源。
- **不保证 AI 生成内容的准确性** — AI 生成的内容无法被人类快速辨别真伪。你只能在力所能及的范围内减少问题。
- **必要时主动索要补充信息或证据** — 如果信息不足或无法验证，明确告知用户需要什么证据。

### 学术写作规则
- **不编造数据**：不虚构 DOI、作者、期刊信息、实验结果、图表编号、页码或任何可验证的学术信息。
- **标注来源**：对声明、参数、定量结果、数据集、图表等附加来源标签。
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

## Paper Reading To Word

Default output, unless the user asks otherwise:

1. A bilingual English-Chinese report for fast browsing.
2. A Chinese-only report for submission, teaching, or presentation preparation.
3. Optional Markdown working notes if useful.

Before writing, build a source map:

- Title, authors, venue, year, DOI/arXiv if present.
- Section headings and page spans when available.
- Figures, tables, equations, datasets, hardware/software, and evaluation settings that support key claims.
- Uncertain or missing metadata marked as `未在原文中明确给出`.

Use `references/report-structure.md` for the default report structure and evidence-label format.

For `.docx` creation or editing:

- Prefer structured headings, summary tables, figure/table placeholders, and source labels.
- **字体规范（必须遵守）**：
  - 中文字体：宋体（SimSun）用于正文，黑体（SimHei）用于标题
  - 英文/数字字体：Times New Roman
  - 默认字号：正文14pt（小四号），标题可适当增大
  - 行距：1.5倍
  - 首行缩进：0.74cm（2字符）
  - 如用户指定其他字号（如小五号12pt），按用户要求调整
- For existing academic/legal/business Word documents, make a new version or use tracked-change style edits rather than overwriting the original.
- For advanced DOCX operations, use `references/office-docx/ooxml.md`, `references/office-docx/docx-js.md`, and the scripts under `references/office-docx/`.

## Academic PPT Workflow

First clarify only the high-impact missing details:

- Purpose: literature report, group meeting, course report, opening/midterm/defense, project display, science communication, or other.
- Duration and slide count.
- Audience and evaluation criteria.
- Required template, school/company constraints, fonts, ratio, logo, sections, notes, or output format.
- Source files: paper, thesis, Word draft, data, MATLAB/Python/Origin figures, screenshots, old PPT, template.

If the user asks to proceed immediately, make reasonable defaults and state them briefly.

For research PPTs, use a concise structure:

1. Cover.
2. Research background and problem.
3. Related work or theoretical basis.
4. Method, model, system, or algorithm.
5. Experiment/simulation setup.
6. Results and analysis.
7. Comparison and discussion.
8. Contributions, limitations, and outlook.
9. Q&A.

For paper-reading PPTs, use:

1. Paper metadata.
2. Background.
3. Core problem.
4. Method framework.
5. Experiment setup.
6. Main results.
7. Contributions.
8. Limitations.
9. Possible improvements.
10. Relationship to the user's topic.

## Slide Quality Rules

- One core point per slide.
- Prefer action titles that state the conclusion, not vague topic labels.
- Figures, diagrams, tables, and formulas should carry the technical argument; avoid long paragraphs.
- Keep axes, units, legends, formulas, assumptions, data sources, and figure captions scientifically accurate.
- Use white or restrained academic backgrounds unless a supplied template requires otherwise.
- Limit colors and decoration; use color to direct attention to evidence.
- Avoid text overflow, image stretching, Chinese garbling, missing fonts, stale template text, bad navigation labels, and overlapping elements.

The `academic-pptx` repository was reviewed as an external reference. Because it marks its license as proprietary, do not copy its text into outputs or this skill. Use only general academic presentation principles: argument-first structure, action titles, evidence-led slides, and the ghost-deck test.

## PPTX Technical Work

For template-matched defense PPTs:

- Prefer copying native template slides and replacing content rather than rebuilding from blank slides.
- On Windows with Microsoft PowerPoint installed, PowerPoint COM can be used for cloning, export, and overflow inspection.
- Never modify the user's original PPTX directly. Work on a timestamped or versioned copy.
- Do not disable PowerPoint add-ins or change application settings unless the user explicitly approves in that task.

Useful bundled resources:

- `references/thesis-defense-pptx/scripts/` for thesis context extraction, template cloning, slide export, contact sheets, text scans, and overflow inspection.
- `references/office-pptx/` for OOXML-level PPTX inspection and editing.
- `references/office-docx/` for OOXML-level DOCX inspection and editing.

## Quality Gate

Before final delivery, verify what is feasible:

- For Word: inspect extracted text or package XML for missing text, garbled Chinese, broken images, table overflow, and source labels.
- For PPT: export or inspect slides, check page order, stale placeholders, text overflow, image aspect ratio, overlap, and readability.
- Report output file paths, source paths, extraction method, checks performed, and unresolved uncertainties.
