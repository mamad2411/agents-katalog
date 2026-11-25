---
name: manuscript-writing-studio
description: Use when the user asks to draft, rewrite, polish, translate, or final-check academic manuscript text, including title, abstract, introduction, literature review, methods, results, discussion, conclusion, Chinese/English polishing, or journal-style manuscript revision. This skill distinguishes Chinese vs English journal writing and social-science vs technical manuscript conventions before editing.
---

# Manuscript Writing Studio

本 skill 负责论文写作、改写、润色和中英转换。它不是参考文献下载、引文核验或审稿回复总控；涉及引用、证据、审稿意见或投稿包时，必须回到对应工作流。

## Required References

- `<VELA_RUNTIME_ROOT>/skills/catalog/manuscript_writing_workflow.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/writing_quality_rules.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/publication_style_rules.json`

## Global Writing Floor

所有写作、重写、润色、中英转换、目标期刊适配和定稿检查都必须先服从这组底层规则：

- 论文要有一条能讲清楚的主线。正式稿应能用四句话概括：基于什么背景，关注什么问题，使用什么方法或材料，得到什么结论。
- 写作要直接推进论点。减少迂回立论、防御式铺垫、否定式开场和二元反转套式；`not X but Y`、`rather than`、`since`、`however`、`therefore`、`not only but also` 及其中文同义结构只有在真正承担逻辑关系时才使用。
- 不为了规避某些句式而加入无必要解释。改写后的文本必须让第一次阅读的读者更容易理解。
- 方法选择要自然衔接。先说明研究问题、材料结构、识别需求或解释目标，再进入模型、算法、编码、比较或细读程序；技术细节不能过早压住问题意识。
- 每段有明确任务，避免重复。段落和句子要长短错落，不能把正文切成一串四五行小碎段，也不能让所有句子使用同一长度和同一节奏。
- 限制 AI 味、翻译腔、过度技术化词语、自创概念和内部工程用词。正文面向读者和审稿人，不展示本地工作流、route、quality gate、agent、harness 等内部用语，除非论文主题本身研究这些对象。
- 使用对应学科公认常用概念。中文概念优先查中文文献、中文期刊和中文学术通行用法，不能先查英文再自行翻译成中文术语。
- 审稿和写作不能过度自我削弱。先告诉读者本文能说明什么、如何说明、推进了哪一部分，再说明证据边界和局限。

## Route Boundaries

- 写作、重写、润色、标题、摘要、引言、文献综述、方法、结果、讨论、结论、中译英、英译中 -> 使用本 skill。
- 正式引用、参考文献表、正文引用支撑关系、证据句 -> 交给 `writing-reference-capture`、`evidence-based-literature-workflow`、`citation-verifier`。
- 回复审稿、response letter、rebuttal、返修矩阵 -> 交给 `reviewer-response-pack`；本 skill 只负责被明确要求的措辞润色。
- 图、表、图注、表注、科研插图 -> 交给 `research-figure-studio` 或 `figure-table-studio`。

## Target Declaration

动笔前先声明两个目标：

1. 语言目标：
   - `cn_humanities_social_science`：中文人文社科、CSSCI、中文学位论文或中文报告。以本地中文社科写作规则为主。
   - `en_high_impact_journal`：英文期刊、高影响期刊、英文摘要、英文 cover letter 或英文 response。可以更积极借鉴 Nature-style 结构和英文句法控制。
   - `bilingual_transition`：中英转换。先重建论证图，再按目标语言写作，不逐句硬译。
2. 学科目标：
   - `humanities_social_science`：人文社科默认标准。
   - `computational_social_science_or_method`：计算社科或方法技术型论文，可更多借鉴技术论文的模块化方法、pipeline、benchmark 和复现表达。
   - `traditional_quantitative_social_science`：传统量化研究，以理论、变量、模型、识别、稳健性和边界为主。
   - `qualitative_or_interpretive_social_science`：质性或解释性研究，以材料、案例、编码、解释链和反身性边界为主。

如果用户没有说明目标，按当前材料推断，并在输出开头写明“本次默认按哪个目标处理”。不要把英文期刊写法或理工科写法自动套到中文社科论文上。

## Humanities Thesis Adapter

当用户说“写论文”“选题”“没有新意”“理论和文本脱节”“章节逻辑”“脚注格式”“论文修改”或明显在做人文社科长文时，先进入人文论文澄清流程，不要直接起草。

先确认：

- 论文类型：课程论文、本科论文、硕士论文、博士论文、期刊论文或投稿修改稿。
- 研究对象：具体文本、作品、事件、案例、田野材料、历史材料或社会现象。
- 核心问题：用户真正困惑的地方，以及它为什么值得论证。
- 论点方向：暂定要证明什么，是否可争辩、可材料支撑、有方向。
- 理论工具：读过哪些理论或文献，它们解释了什么，哪些地方解释不了。
- 材料边界：已有材料、缺失材料、不可编造材料。
- 输出目标：字数、章节、格式、目标期刊或学校要求。

诊断常见状态：

- 有对象但没有问题：先帮助把材料中的张力变成研究问题。
- 有问题但没有论点：先形成可争辩、可证明、有方向的临时论点。
- 理论和材料脱节：回到具体文本、史料、案例或田野材料，再判断理论是否适用。
- 笔记很多但结构散：先做材料清单和可用性判断，再重建递进结构。
- 已有草稿但逻辑不顺：先查章节职责、引文后分析、章末过渡和术语一致性。

写作原则：

- 理论是工具，材料是落点。不能先铺理论再硬套材料。
- 背景是语境，不是解释。不能用历史背景替代论证。
- 引文、文本细节、史料和访谈摘录之后必须有分析，不能引用后直接跳到新话题。
- 文献综述按论证功能分组：奠基文献、对话文献、缺口文献，而不是按年份平铺。
- 术语和译名必须稳定；不确定术语标记待核验，不能自行发明通行译名。
- 脚注承担出处、补充说明或防御性说明；空脚注、格式混用、缺页码或缺文献类型标识不能进定稿。

这些规则吸收自 `ganzhi-black/humanities-thesis-skill` 的人文论文方法，但不安装它的检索脚本。正式文献发现、全文获取、引用核验、Zotero 入库和 PDF 证据仍走本地 `evidence-based-literature-workflow`、`reference-fulltext-acquisition`、`citation-verifier` 和 `writing-reference-capture`。

## Workflow

1. 判断任务模式：起草、结构重写、语言润色、中英转换、定稿检查。
2. 声明语言目标和学科目标。
3. 收集或提取核心主张、证据、材料、方法、边界和不可改动术语。
4. 按 `manuscript_writing_workflow.json` 选择对应章节合同。
5. 先诊断问题属于论证、证据、段落、术语还是句子风格。
6. 结构不成立时先修结构；证据不足时列为阻断项；只有结构和证据边界清楚后才润色句子。
7. 输出正文改写结果，同时给出必要的修改说明、风险标记和需要回到引用/证据链的项目。

## Writing Rules

- 不编造数据、样本量、结果、参考文献、DOI、期刊状态、页码或原文引句。
- 不把“写得顺”当作“论证成立”。
- 不把相关写成因果，不把局部样本写成总体规律，不把探索性发现写成已证实机制。
- 不把文章写成防御性说明或局限清单；证据能支撑的贡献要写清楚。
- 不把中文学术概念从英文材料中自行翻译出来；中文稿优先核对中文文献和通行译法。
- 不让段落、句子和连接词呈现机械均匀的模板节奏。
- 英文高影响期刊稿件可以使用更紧的摘要、引言 funnel、短句和 section moves。
- 中文社科稿件保持概念密度、问题意识、理论脉络和 PEEL 闭环，不机械套用英文短句节奏。
- 计算社科和方法技术型论文可以更强调 pipeline、方法模块、数据处理和复现。
- 传统量化和质性研究仍以本地社科写作逻辑为主，不强行套用理工科方法段和图组结构。

## Long-Form Word And Thesis Adapter

The local workflow absorbs useful writing-organization patterns from `Jinze-Lee/codex-skills-workbench/master-thesis-studio-skill`, but this is not a default route.

Use these patterns only when the user explicitly asks for a thesis-style or long-form Word project workflow:

- Start with project facts, asset inventory, current stage, writing mode, missing materials, and authenticity boundaries.
- Create a chapter plan before drafting chapter prose.
- Keep a decisions log for user confirmations, assumptions, and changes.
- Track figures, tables, formulas, code, data, and references through manifests instead of loose conversation memory.
- Use stable placeholders such as figure/table/equation/reference tokens when a later DOCX or template-writeback step needs deterministic placement.
- Do not invent example data, example figures, sample sizes, metrics, references, or results unless the user explicitly permits illustrative placeholders.

For ordinary article drafting, journal polishing, or simple Word export, stay with the normal manuscript workflow and `research-docx-export`; do not silently switch into a thesis-studio or Word XML pipeline.

## Prompt Pattern Adapters

The local workflow absorbs useful prompt constraints from `Leey21/awesome-ai-research-writing` as adapters, not as copy-paste prompts.

Use these adapters when the task asks for translation, polishing, shortening, expanding, humanizing, logic checks, result analysis, or venue migration:

- Format-sensitive translation: first decide whether the output is LaTeX, Word, DOCX, or plain text. LaTeX output preserves commands and escapes `%`, `_`, and `&`; Word/plain-text output must not contain Markdown, code fences, or LaTeX escaping.
- Bilingual reconstruction: for serious manuscript text, extract the claim, evidence, boundary, and terminology before translation; use a back-translation or logic-flow note when meaning drift is risky.
- Micro revision: distinguish small shorten/expand requests from structural rewriting. Micro edits must preserve all facts, variables, results, citations, uncertainty, and boundaries, and return a concise delta log.
- Humanized surface check: remove empty rhetoric, mechanical transitions, overused AI phrases, and translationese without changing claims. If the original is already rigorous and natural, keep it and report a pass.
- Data-bound result analysis: write trends, comparisons, gains, robustness, and tradeoffs only from supplied or verifiable data. If the data do not show a clear pattern, say so.
- Venue migration: if the user asks to change conference, change journal, resubmit, or migrate a template, hand the package-level work to `social-science-submission-packager` after drafting the target-requirement checklist.

Do not let a prompt template override citation verification, writing quality gates, figure/table checks, peer-review protocol, or package freeze.

## Academic Humanization And Stop Slop Adapter

The local workflow adapts useful academic de-template checks from `brycewang-stanford/Awesome-Agent-Skills-for-Empirical-Research` and the surface-pattern scan from `hardikpandya/stop-slop`. Treat them as a writing-quality audit, not as a detector-evasion objective. For non-trivial requests, call `academic-humanization-studio` as the helper skill after the manuscript boundaries are locked.

Use this adapter when the user asks for "去 AI 味", "降 AIGC", "不像 AI 写的", "humanize", "deslop", or final academic polishing:

- First lock the claim, evidence, citations, variables, estimates, uncertainty, limitations, quotations, author-defined terms, output container, and target language.
- Declare whether the task is detect-only, light polish, paragraph rewrite, or section-level rebuild.
- Diagnose surface issues before rewriting: empty rhetoric, throat-clearing openers, performative emphasis, mechanical transitions, inflated novelty, vague attribution, excessive hedging, causal overclaiming, generic conclusions, translationese, binary-reversal formulas, negative-listing setups, false agency, hidden actors, and overly uniform sentence rhythm.
- For English academic prose, prefer precise attribution, bounded claims, field-normal verbs, and short but varied sentence control.
- For Chinese social-science prose, use the five-step loop: locate templated language, classify the issue, rewrite only the surface, self-check information density and argument flow, then run a second-pass review.
- After revision, report the issue ledger, change log, locked-items check, and any remaining risks.
- Never promise to bypass Turnitin, CNKI AMLC, GPTZero, or similar systems. Detector or similarity scores can be mentioned only as non-guaranteed external signals; the allowed goal is rigorous, authorial, evidence-faithful academic prose.
- Do not apply stop-slop mechanically to formal academic writing. Keep legitimate passive voice, hedging, adverbs, and field-standard terms when they preserve evidential caution or methods precision.

If a requested style change would alter facts, data, model outputs, citations, or argumentative boundary, stop and ask before changing the manuscript.

## Target Journal Adaptation Adapter

当用户说“投稿前润色”“按目标期刊修改”“期刊风格”“投这个期刊”“target journal”“journal style”或类似意图时，进入目标期刊适配润色模式。这个模式吸收 `WantongC/journal-adapt-writing-skill` 的优点，但不把它安装成新的主 skill。

先确认：

- 目标期刊或写作目的地。
- 当前稿件或需要处理的章节。
- 目标语言和学科类型。
- 是否已有 5 到 8 篇目标期刊近作的可读全文；没有时说明只能做保守润色，不能声称完成目标期刊风格适配。
- 是否有二级语料，例如同主题顶刊论文、导师样稿、课题组样稿或用户认可的范文。
- 输出容器：LaTeX、Word、DOCX、纯文本或后续投稿包。

执行顺序：

1. 把正文事实、研究问题、主张、数据、结果、引用、公式、变量、图表编号和作者定义术语锁定为最高优先级。
2. 只从可读全文语料里提取写法，不从题名、摘要、检索元数据、片段 OCR 或失败转换文件里生成期刊画像。
3. 对每篇目标期刊语料生成“风格卡”：只描述摘要结构、引言推进、贡献位置、文献综述摆放、方法表达、结果叙述、讨论范围、语气、时态和转折方式；不得引用、仿写或搬运语料论文内容。
4. 汇总成“期刊风格画像”：写明稳定模式、冲突项、红旗和证据不足处。目标期刊语料优先于二级语料，二级语料优先于一般写作规则。
5. 修改正文时一节一节处理：先诊断，再改写，再给修订日志。日志至少说明问题类型、严重度、期刊匹配分、采用的规则、保留不动的引用/公式/变量/结果，以及是否发生规则冲突。
6. 如果改动会影响引用性断言、证据句、结果解释、图表措辞或投稿包状态，停止并转回 `writing-reference-capture`、`evidence-based-literature-workflow`、`research-figure-studio` 或 `social-science-submission-packager`。

优先级：

- P0：原稿事实、证据、结果、引用、公式、变量和作者主张。
- P1：用户明确要求。
- P2：目标期刊可读全文语料的稳定写法。
- P3：同领域顶刊、同主题论文、导师或课题组样稿。
- P4：本地中文/英文、社科/计算社科/量化/质性写作规则。

目标期刊适配只解决“像不像这个投稿目的地的写法”。它不是引用核验、DOI 核验、审稿通过保证，也不是改变研究内容的许可。

## Output Format

默认输出：

```markdown
目标判断：语言目标 = ...；学科目标 = ...
处理模式：...

修改后文本：
...

修改说明：
- ...

仍需核验或补充：
- ...
```

如果只做轻度润色，可以省略长说明，但必须保留会影响主张、证据或引用的风险提示。
