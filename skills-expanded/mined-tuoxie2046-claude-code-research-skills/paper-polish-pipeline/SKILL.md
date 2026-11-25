---
name: paper-polish-pipeline
description: >-
  Staged, diagnosis-driven academic paper polishing pipeline (bilingual 中文/English).
  Use to revise a paper from rough draft to final submission across ordered stages:
  diagnose first, then optimize section by section, derive abstract/contributions from the
  revised body, polish the language to reduce AI-sounding phrasing, and run a
  pre-submission/defense risk check. Enforces research-integrity guardrails: no fabricated references/data, no
  overclaiming, correlation is not causation, limited samples are not universal laws, and
  missing information is flagged not invented. Works for thesis, journal, course paper, and
  grant proposal. Also trigger on Chinese phrasings like 论文润色、论文修改、论文诊断、
  降AI味、降低AI味、引言重构、文献综述优化、研究方法规范、结果讨论深化、摘要提炼、
  创新点提炼、答辩问题预测、投稿前检查、终稿风险检查、毕业论文修改、期刊论文润色.
---

# Paper Polish Pipeline / 论文润色全流程

## Overview / 概述

A multi-stage workflow for revising an academic paper from rough draft to final copy. Rather
than polishing sentences, it works through the paper in order: first diagnose the real
problems, then fix structure and logic, and write the abstract and contributions only once the
body is settled, before a final language pass and a pre-submission check.

本 skill 按顺序修改论文,把它从初稿带到终稿。它不是逐句润色,而是先诊断定位真正的问题,
再改结构与逻辑,正文定稿后才提炼摘要与创新点,最后做语言精修和投稿/答辩前的风险检查。
它服务于真实研究者的定稿流程,不替作者编造内容。

Applicable to / 适用: 毕业论文 thesis · 期刊论文 journal article · 课程论文 course paper ·
项目申请书 grant proposal.

---

## IRON RULES — Research Integrity (HIGHEST PRIORITY) / 学术诚信铁律(最高优先级)

These rules apply to **every** stage and override any stylistic goal. Later stage templates
may specialize them but must never weaken them. 以下规则适用于所有阶段,优先级最高。

1. **No fabrication / 不虚构.** Never invent references, authors, years, datasets, data
   values, equipment, parameters, sample sizes, software versions, experimental steps, or
   figure/table contents. 绝不新增原文没有的文献、作者、年份、数据、设备、参数、样本量、
   软件版本、实验步骤或图表信息。
2. **Flag gaps, don't fill them / 缺信息要标注,不要编造.** When the source lacks needed
   information, mark it as `【此处需补充……】` / `[TO BE ADDED: …]` and move on.
3. **No overclaiming / 不夸大.** Avoid "填补空白 / fills a gap", "具有重大意义 / of great
   significance", "首次提出 / first to propose", "颠覆性 / disruptive" unless the source
   already proves it. Never turn an incremental improvement into a breakthrough.
4. **Preserve the facts / 保真.** Keep the research object, scope/boundaries, core claims,
   data, methods, and conclusions unchanged. 不改变研究对象、研究边界、核心观点、数据、
   方法与结论。
5. **Logic integrity / 逻辑不越界.** Do not turn correlation into causation (相关≠因果);
   do not turn "可能 / may suggest" into "证明 / proves" or "确定机制 / established
   mechanism"; do not turn a limited-sample finding into a universal law.
6. **Reduce AI-sounding phrasing / 降 AI 味.** Remove template connectors (首先/其次/最后/
   综上所述/总而言之 · firstly/secondly/in conclusion), avoid over-symmetry, avoid empty
   elevation, and do not pile up fancy vocabulary for the sake of sounding advanced.
7. **Output discipline / 输出纪律.** 每个阶段都按其规定的编号结构输出(见对应 reference)。
   凡产出改写文本的阶段(②–⑥),结尾给出"待核查项 / 风险提醒",列出作者需确认或补充的内容;
   诊断(①)与风险检查(⑦)本身即以问题清单为主,不另设该项。Stages that rewrite text end
   with a "to-verify / risk" note; the diagnostic and risk-check stages are problem lists in
   themselves.

---

## Pipeline & Ordering / 流程与顺序

Run stages **in order**. In `full` mode, pause after every stage and wait for the user before
continuing; the two gates marked in the diagram below (after ① and after ④) are mandatory
confirmation points. Do not skip ahead. In particular, **Stage 5 (abstract/contributions) must
run only after the body stages (2–4) are revised**, because the abstract must be derived from
the finalized body, not written blind.

按顺序执行。`full` 模式在每个阶段结束后都暂停,等用户确认再继续;下图标出的两个 gate
(① 之后、④ 之后)是必须通过的确认点。不要跳步。**第 5 阶段(摘要/创新点)必须在正文
(2–4)改完之后才能跑**,因为摘要只能来自已定稿的正文,不能提前盲写。

```
①  diagnose            → 产出"修改路线",决定后续顺序
        │  (human checkpoint: 确认优先级)
②  intro-litreview     ┐
③  methods             ├ 正文分章优化 (按 diagnose 给的顺序)
④  results-discussion  ┘
        │  (human checkpoint: 正文是否定稿)
⑤  abstract-innovation → 从已改正文提炼摘要/结论/创新点/关键词
⑥  language-polish     → 终稿语言精修 + 降 AI 味
⑦  risk-check          → 投稿/答辩前风险清单 + 模拟审稿 + 答辩问题预测
```

图中只标出 ① 与 ④ 之后的两个关键 gate;`full` 模式实际在每个阶段结束后都会暂停等用户输入。
The diagram marks only the two mandatory gates; `full` mode actually pauses after every stage.

---

## Modes / 模式

Route by the user's request. Each section mode (①–⑦) loads its full prompt contract from
`references/`; `full` is orchestrated from this file.
根据用户需求选择模式;①–⑦ 各自的完整指令契约见 `references/`,`full` 由本文件编排。

| Mode | 指令 | What it does | Reference |
|---|---|---|---|
| `diagnose` | 1 | 整体诊断:总体评价 + 核心问题清单(严重/中等/细节)+ 修改路线 + 下一步建议 | `references/diagnose.md` |
| `intro-litreview` | 2 | 引言与文献综述重构(背景→现状→不足→切入点→目标→贡献) | `references/intro-litreview.md` |
| `methods` | 3 | 研究方法规范化(对象/数据/材料/变量/流程/可复现性) | `references/methods.md` |
| `results-discussion` | 4 | 结果与讨论深化(从"描述结果"提升到"解释结果") | `references/results-discussion.md` |
| `abstract-innovation` | 5 | 摘要/结论/创新点提炼(必须源自已改正文) | `references/abstract-innovation.md` |
| `language-polish` | 6 | 终稿语言精修 + 降 AI 味(审稿人/资深编辑视角) | `references/language-polish.md` |
| `risk-check` | 7 | 终稿风险检查 + 模拟审稿 + 答辩高频问题预测 | `references/risk-check.md` |
| `full` | — | 按 ①→⑦ 顺序编排,带人工检查点 | this file |

If the user just says "帮我改论文 / polish my paper" without specifying a stage, default to
`diagnose` first and recommend the order — never jump straight to language polishing.

---

## Inputs to ask for / 需要向用户索取的信息

Before any stage, make sure you have (ask only for what's missing):
- **论文类型 / paper type** (thesis / journal / course / grant) and **研究领域 / field**
- **题目 + 当前需求 / title + current need**
- The **relevant section(s)** for the chosen stage (or full text for `diagnose` / `full`)
- For Stage 2–7: the **diagnosis result** from Stage 1, if available, so fixes are targeted

If the user pastes text in one language, polish in that language; produce the prescribed
structure bilingually only when the user is working across both.

---

## How to run a stage / 单阶段执行约定

1. Read the matching `references/<mode>.md` for the exact task list, constraints, and output
   format. 读取对应 reference 拿到该阶段的任务清单、约束与输出格式。
2. Apply the **IRON RULES** above plus any stage-specific constraints.
3. Output in the stage's numbered structure. For rewriting stages (②–⑥), end with a
   **待核查项 / 风险提醒 (to-verify / risk)** note, per IRON RULE 7.
4. In `full` mode, stop after each stage and wait for the user before continuing.

This skill produces **revision suggestions and rewritten text grounded in the user's own
source**. It does not author a paper from nothing, invent results, or make the final
decision — the author verifies and decides. 本 skill 只在用户原文基础上给出修改建议与改写,
不凭空写论文、不编造结果、不替作者拍板。
