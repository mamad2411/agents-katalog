---
name: paper-reviewer-en
description: Review academic papers or manuscripts from local LaTeX source files, LaTeX project directories, or Markdown documents, and write a Chinese evidence-grounded peer-review `review.md` beside the input. Optionally incorporate OpenReview forum, review, rebuttal, or discussion materials after first resolving an OpenReview-capable Python interpreter that can `import openreview`. Use when the user asks to 审稿, review, or act as a reviewer for a paper/manuscript. Do not use for code review, thesis review, or NSFC proposal review.
---

# Paper Reviewer EN

## Overview

Use this skill to review one academic paper or manuscript from AI-readable local `.tex` or `.md` materials and write a Chinese peer-review `review.md` beside the input by default.

Keep English method names, dataset names, benchmark names, metric names, and other technical terms unchanged. If the user explicitly asks to incorporate OpenReview materials, first resolve an OpenReview-capable Python interpreter instead of looking for a shell CLI. Read [references/review-template.md](references/review-template.md) for the output scaffold and [references/style-rules.md](references/style-rules.md) when you need the tone and evidence rules.

## Input Contract

Accept only the following input types:

1. A single LaTeX source file, such as `main.tex`
2. A LaTeX project directory containing files such as `main.tex`, chapter `.tex` files, appendix `.tex` files, or supplementary `.tex` files
3. One or more Markdown documents from the same directory containing manuscript text, structured notes, parsed sections, or author summaries

Optional runtime input for OpenReview-backed tasks:

- `python_path`: an absolute path to a Python interpreter that can `import openreview`

Optional OpenReview-backed materials, only when the user explicitly asks for them:

- OpenReview forum URL
- official reviews
- author rebuttal or response
- discussion thread or reviewer comments

All accepted inputs must be:

- local and text-readable
- quoteable and locatable by section, figure, table, equation, appendix, or Markdown heading
- sufficient to trace major claims back to explicit textual evidence

## Unsupported Inputs

Do not treat the following as valid default inputs:

- PDF only
- images, screenshots, scans, or photos
- slide screenshots or webpage screenshots
- other non-text files that are not directly machine-readable

If the user provides only unsupported inputs, do not produce a review conclusion. Ask for a readable local `.tex` file, LaTeX directory, or `.md` document instead.

## Source Priority And Auxiliary Material Rules

1. If LaTeX source is available, use LaTeX as the primary source.
2. If only Markdown is available, analyze directly from Markdown.
3. If both `.tex` and `.md` are available, use the more complete source as primary input and use the other only for cross-checking.
4. Extra review notes, summaries, reading notes, or side Markdown files are auxiliary checks only. If used, label them as `辅助校验：...` and never present them as manuscript fact.
5. If only partial chapters or partial Markdown notes are available, continue only as a partial review and explicitly state that the result is `基于不完整材料`.
6. If key evidence such as experiment tables, appendix details, or method context is missing, mark related judgments as `待核实` or `证据不足`.
7. OpenReview forum, review, rebuttal, or discussion materials are optional review context only. Use them only when the user explicitly asks for them, and never present them as manuscript fact.

## OpenReview Preflight

Run this section only when the task explicitly needs OpenReview materials such as a forum URL, official reviews, rebuttal, discussion thread, or reviewer comments. Skip it for pure local `.tex` or `.md` review.

Treat OpenReview availability as Python importability, not as a shell CLI binary. The required check is whether a Python interpreter can run `import openreview`.

Deterministic preflight sequence:

1. Try the current interpreter first:

```bash
python3 -c "import openreview"
```

2. If that succeeds, treat the current `python3` as the OpenReview runtime for the rest of the turn.
3. If that fails, ask the user for an absolute `python_path`, for example `/Users/yuzy/.venv/bin/python3`.
4. Validate the user-provided interpreter:

```bash
<python_path> -c "import openreview"
```

5. If validation succeeds, reuse that exact interpreter for every OpenReview-related command in the turn. Do not mix interpreters.
6. If validation still fails, do not attempt any OpenReview fetch. Report that the OpenReview environment is unresolved and wait for a valid Python path.

Expected failure prompt:

`当前 python3 无法导入 openreview。请提供一个可用的绝对 Python 路径，例如 /Users/yuzy/.venv/bin/python3。`

## Output Path Rules

Resolve the output path before writing the final review:

1. If the input is a directory, write to `<input_dir>/review.md`.
2. If the input is a single `.tex` or `.md` file, write to `<parent_dir_of_input>/review.md`.
3. If the user provides multiple explicit files, write automatically only when all files are in the same directory. Otherwise, stop and ask for a single paper directory.
4. If `review.md` already exists at the target path, overwrite it directly.

Examples:

- input `/path/paper_dir` -> output `/path/paper_dir/review.md`
- input `/path/main.tex` -> output `/path/review.md`
- input `/path/paper.md` -> output `/path/review.md`

## Core Workflow

1. Check input legality and stop early for unsupported inputs.
2. If the user explicitly requests OpenReview materials, run the OpenReview preflight above before doing any OpenReview-related work.
3. Read the primary manuscript source first. Use [references/review-template.md](references/review-template.md) as the scaffold and [references/style-rules.md](references/style-rules.md) as the tone guide when drafting.
4. Build the paper skeleton: title, problem setting, claimed contributions, method sections, experiment sections, appendix materials, and conclusion.
5. Extract explicit evidence from sections, figures, tables, equations, appendix materials, and explicitly requested OpenReview materials. Ignore pure formatting commands and other LaTeX noise.
6. Judge contribution boundary and evidence sufficiency. Separate manuscript fact from reviewer inference at every major judgment.
7. Resolve the output path using the rules above.
8. Write the final `review.md`.
9. Reply only with the output path and a brief summary. Do not repeat the full review in chat unless the user explicitly asks for it.

## Peer Review Checklist

For most papers, explicitly check:

- problem setting, assumptions, and target bottleneck
- claimed contributions versus actual contribution boundary
- method logic and whether the core design is motivated
- experiment coverage, baseline strength, ablations, robustness, efficiency, and failure cases
- clarity, reproducibility, and whether important setup details are missing
- significance and where the paper's claims stop being well supported

When relevant, also check:

- 3D papers: geometry consistency, representation capacity, rendering or inference cost, memory or storage cost
- graphics papers: visual fidelity, controllability, physical plausibility, complexity, and deployability
- foundation-model papers: pretraining assumptions, scaling evidence, transfer scope, and compute tradeoffs

## Deterministic Output Structure

Write `review.md` using the following sections in order:

### 1. 标题与一句话概述

- `标题`：论文标题
- `一句话概述`：必须用一句话讲清方法的输入、核心变换和输出/主要收益，优先写成“以 A 和 B 为输入，通过 C，输出 D，从而 E”的形式
- `来源依据：...`

### 2. 论文摘要与核心主张

- 论文试图解决什么问题
- 作者最核心的 2-4 个主张
- 哪些主张在现有材料中证据较强，哪些仍需保守理解
- `来源依据：...`

### 3. 主要优点

- 列出 3-5 条最重要优点
- 每条都要说明为什么这是优点，而不是只给结论
- 每条都附 `来源依据：...`

### 4. 主要问题

- 列出 3-8 条最重要问题
- 每条都按“问题 -> 为什么影响判断 -> 建议怎么改”来写
- 对证据不足、边界不清、实验不充分等问题，明确影响范围
- 每条都附 `来源依据：...`

### 5. 分维度评审

固定写以下五个维度，顺序不可变：

- `Novelty`
- `Technical Soundness`
- `Experimental Evidence`
- `Clarity / Reproducibility`
- `Significance / Scope Boundary`

每个维度都要包含：

- 当前判断
- 最关键的支持证据或反证
- 主要风险或边界
- 一句最有价值的修改提示
- `来源依据：...`

### 6. 需要作者回应的问题

- 给出 3-5 个需要作者正面回应的问题
- 优先问会改变审稿判断的问题，而不是次要润色问题
- `来源依据：...`

### 7. 修改建议

- 给出一组按优先级排序的修改动作
- 每条建议都要可执行，并与上面的关键问题对应
- `来源依据：...`

### 8. 总体判断

- 概括论文真正贡献了什么
- 明确哪些主张是当前材料最能支持的
- 明确论文的 claim boundary 和尚不能推出的结论
- `来源依据：...`

Do not output accept or reject recommendations, overall score, numeric rating, confidence, or OpenReview-style verdict labels.

## Evidence Rules

1. Every major judgment must be traceable to explicit evidence.
2. Use anchors such as:
   - `来源依据：第 3 节, Fig. 2, Table 1`
   - `来源依据：公式 (4), Appendix B`
   - `来源依据：Markdown 小节 "Method"`
3. Separate paper fact from reviewer inference. If you infer something, phrase it as analysis, not manuscript fact.
4. Do not invent datasets, baselines, equations, experiments, or conclusions that are not in the input materials.
5. When materials are incomplete, say `基于不完整材料` and mark uncertain points as `待核实` or `证据不足`.
6. If auxiliary notes are used, cite them as `辅助校验` rather than primary evidence.
7. If OpenReview materials are used, cite them separately, for example `来源依据：OpenReview official review #1` or `来源依据：OpenReview author rebuttal`.
8. OpenReview reviews or rebuttals may sharpen reviewer context, but they do not become manuscript fact.

## Writing Rules

1. Write in Chinese by default, but keep English technical terms unchanged.
2. Follow [references/style-rules.md](references/style-rules.md) to avoid generic AI-review voice.
3. Use a natural expert tone. Avoid empty praise, filler transitions, and template-like symmetry.
4. For every substantial weakness, explain why it matters and attach a concrete revision action.
5. Prefer short paragraphs and compact bullets over long blocks of prose.
6. Quote only the minimum needed to support a judgment.
7. Focus on the paper's decisive technical logic, evidence strength, and contribution boundary.

## Output Contract

When provided with valid inputs, do all of the following:

1. Write one real local `review.md` file following the deterministic structure above.
2. Use the resolved output path rules defined in this skill.
3. Overwrite an existing target `review.md` by default.
4. Return only a short confirmation with the output path and a brief summary.

When the user requests OpenReview-backed materials and the current `python3` cannot `import openreview`, ask for an absolute `python_path` and do not attempt any OpenReview fetch until that path is validated.

When provided only unsupported inputs, ask for AI-readable `.tex` or `.md` sources and do not invent a review.
