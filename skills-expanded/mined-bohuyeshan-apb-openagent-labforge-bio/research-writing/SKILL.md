---
name: research-writing-skill
description: Chinese-first research paper writing, revision, polishing, section drafting, rebuttal, peer-review response, thesis prose improvement, and manuscript argument planning. Use when the user asks to write or revise论文正文, abstracts, introductions, methods, results, discussion, conclusions, related work, responses to reviewers, LaTeX/Overleaf text, or academic prose. Preserve formulas, English paper titles, terms, citations, and measured results.
category: academic
exposure: tool
---

# Research Writing Skill

## Scope

Use this skill for research writing and revision when the output is prose, LaTeX, Markdown, or manuscript text. Use `office-academic-skill` instead when the main deliverable is Word/PPT. Use `scientific-toolkit-skill` when the task is primarily MATLAB, Python, plotting, statistics, simulation, or literature search.

## Writing Principles

- Default to Chinese academic expression unless the user requests English.
- Preserve English titles, formulas, variables, methods, software names, citations, and reference entries.
- Do not invent data, DOI, journal details, experiment settings, results, or author claims.
- Separate `原文/已有数据`, `用户确认内容`, `根据上下文推断`, and `建议性扩展`.
- Prefer verifiable technical statements over generic claims.
- When revising, preserve the user's intended meaning and terminology unless a change is clearly needed.

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

## Formatting Standards（字体格式规范）

当输出为DOCX时，必须遵守以下字体规范：

| 元素 | 中文字体 | 英文/数字字体 | 默认字号 |
|------|----------|---------------|----------|
| 正文 | 宋体 SimSun | Times New Roman | 14pt（小四号） |
| 一级标题 | 黑体 SimHei | Times New Roman | 15pt |
| 二级标题 | 黑体 SimHei | Times New Roman | 14pt |
| 图表标题 | 宋体 SimSun | Times New Roman | 12pt |
| 参考文献 | 宋体 SimSun | Times New Roman | 12pt |

**其他格式要求：**
- 行距：1.5倍
- 首行缩进：0.74cm（2字符）
- 如用户指定其他字号（如小五号12pt），按用户要求调整

## Manuscript Workflow

For a new section or paper draft:

1. Clarify target: journal/conference/thesis/course report, language, length, audience, and required format.
2. Identify source material: paper notes, experiment results, figures, tables, MATLAB/Python outputs, references, advisor comments.
3. Build an argument outline before full prose: problem, gap, method, evidence, contribution, limitation.
4. Draft in coherent paragraphs, not empty slogan bullets.
5. Add source or evidence labels for quantitative claims and literature claims.
6. Revise for logic, specificity, terminology consistency, and citation accuracy.

For revision or polishing:

- Keep claims tied to evidence.
- Replace vague words such as "显著", "先进", "有效", "鲁棒" with measured conditions, comparison baselines, or remove them.
- Check whether each paragraph advances the section's purpose.
- Keep formulas with variable definitions, units, assumptions, and applicable conditions.
- For experimental sections, state dataset/sample, hardware/software, parameters, metrics, baselines, and uncertainty when available.

## Section Guides

Use these default moves unless the user's school or journal template overrides them:

- Abstract: problem, method, experiment/data, key result, contribution.
- Introduction: background, unresolved gap, why it matters, proposed approach, contributions.
- Related work: organize by technical theme, compare assumptions and limitations, avoid simple paper-by-paper summaries.
- Methods: model assumptions, variables, workflow, algorithm, implementation details needed for reproduction.
- Experiments: data/source, platform/software, parameters, metrics, baseline, repeated trials, visualization plan.
- Results and discussion: claim first, evidence second, mechanism/explanation third, limitation last.
- Conclusion: answer the research question, summarize evidence, state limitations and next steps.

## Bundled References

The folder `references/paper-writing/` contains external writing checklists and section patterns adapted as references. Load only the relevant file when needed:

- `brainstorming_guide.md` for turning an unclear idea into a paper plan.
- `section_rhetorical_moves/` for section structure.
- `writing_checklists/` for self-diagnosis.
- `figure_templates/` for figure planning.
- `author_profile/` for editorial heuristics.

These references come from an external systems/networking-oriented repository. Treat them as optional craft guidance, not binding rules, and adapt them to光电信息科学与工程, optics, optoelectronics, sensing, communication, signal processing, and MATLAB simulation work.

## Final Checks

Before delivery, state:

- What was drafted or revised.
- Which source material was used.
- Which claims still need user-provided data or citation support.
- Any uncertainty about terminology, parameters, or references.
