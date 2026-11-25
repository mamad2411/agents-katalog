---
name: academic-humanization-studio
description: Use when the user asks to reduce AI-like academic prose, lower AIGC-like surface signals, humanize, deslop, remove translationese, or make Chinese or English manuscript text sound more authorial while preserving facts, citations, data, results, and uncertainty.
---

# Academic Humanization Studio

This helper skill is part of the local manuscript workflow. Its purpose is rigorous academic surface cleanup, not detector evasion. It can improve wording, rhythm, density, attribution, and paragraph control, but it must not change claims, evidence, references, variables, estimates, limitations, or author intent.

Use it conditionally. If the current text is already rigorous, natural, and evidence-faithful, keep the text and report a pass instead of rewriting for the sake of rewriting.

## Use It When

- The user says `降 AI 率`, `降 AIGC`, `去 AI 味`, `不像 AI 写的`, `humanize`, `deslop`, `stop slop`, `avoid AI writing`, `去翻译腔`, or `学术去模板化`.
- A draft is already written and the problem is surface quality, not missing evidence or broken logic.
- Manuscript-writing-studio or quant-analysis has locked the claim, evidence, result, citation, and uncertainty boundary.

Do not use it to generate fake human imperfection, bypass a detector, hide fabricated work, or rewrite unsupported claims into more persuasive language.

## Intake Lock

Before rewriting, declare:

- target language: Chinese academic, English academic, or bilingual transition;
- section type: title, abstract, introduction, literature review, methods, results, discussion, conclusion, or response letter;
- locked items: facts, data, citations, variables, estimates, p values, confidence intervals, quotations, limitations, and author-defined terms;
- edit strength: detect-only, light polish, paragraph rewrite, or section-level rebuild;
- output container: plain text, Word/DOCX, LaTeX, or response-letter text.

Record these as the `locked-items ledger`; every later revision must be checked against it.

If any locked item is missing or unstable, stop and route back to `manuscript-writing-studio`, `writing-reference-capture`, `evidence-based-literature-workflow`, or `quant-analysis`.

## Modes

| Mode | Use when | Output |
| --- | --- | --- |
| `detect` | The user wants diagnosis only. | issue ledger with severity and examples |
| `rewrite` | The user wants revised prose. | issue ledger, revised text, change log |
| `chinese_academic` | Chinese CSSCI, thesis, or social-science prose sounds templated. | five-step Chinese surface audit and revision |
| `english_academic` | English journal prose sounds generic, over-polished, or machine-like. | severity audit and revised academic prose |
| `bilingual_transition` | Translationese or term drift is the main issue. | term lock, argument rebuild note, revised text |

## Stop Slop Adapter

The local workflow adapts `hardikpandya/stop-slop` as a pattern source, not as a separate skill route. Use it as a surface scan inside this helper.

Check for:

- throat-clearing openers and meta-announcements before the real claim;
- performative emphasis, pull-quote endings, slogan-like paragraphs, and vague declarations of importance;
- binary reversal formulas such as "not X but Y" when the sentence can state the real claim directly;
- negative lists that delay the actual argument;
- mechanical `rather than`, `since`, `however`, `therefore`, and `not only but also` patterns when they create detours instead of logic;
- limitation-first or apology-like passages that weaken a supported contribution before stating it;
- inanimate subjects hiding the actor when an actor matters;
- repeated three-part cadence, identical sentence lengths, uniform four-to-five-line paragraph blocks, and paragraph endings that sound manufactured.

Academic adaptation:

- Do not ban all adverbs, passive voice, hedging, or field terms. Keep them when they mark evidence strength, statistical uncertainty, methods, institutional processes, or standard scholarly caution.
- In formal academic prose, do not replace neutral scholarly voice with conversational "you" unless the target output is a talk, memo, or user-facing guide.
- Treat the scan as a density and precision check. It cannot override locked facts, citations, variables, estimates, quotations, or limitations.
- Do not add extra explanation just to avoid a watched phrase. The revised sentence must be clearer for a first-time reader.
- Chinese concepts must be checked against Chinese-language scholarship and common Chinese academic usage. Do not search English first and invent a Chinese term.
- Keep contribution posture. If the evidence supports a contribution, state it directly before boundaries and limitations.

## Core Workflow

1. Lock claims and evidence before any sentence edit.
2. Diagnose the surface issue by category and severity.
3. Rewrite only the surface layer.
4. Compare revised text against locked items.
5. Run a second pass and report remaining risks.

The second pass is mandatory. A polished paragraph that quietly changes the claim is a failed output.

## English Academic Checks

Flag and fix only when the phrase is actually empty, generic, or misleading in context:

- vague attribution: `research shows`, `studies indicate`, `the literature suggests` without named support;
- inflated novelty or importance: `groundbreaking`, `critical`, `transformative`, `important` without evidence;
- causal overclaiming: `drives`, `leads to`, `shapes`, `impacts` when the design supports only association;
- mechanical transitions: `moreover`, `furthermore`, `in addition`, `it is worth noting` when they add no logic;
- AI-heavy verbs and nouns: `leverage`, `delve`, `underscore`, `robust framework`, `multifaceted`, `nuanced` when they replace precise terms;
- excessive hedging or certainty: `may possibly suggest` versus unsupported `demonstrates`;
- generic conclusions that restate the topic without naming the finding or boundary;
- uniform sentence rhythm, rule-of-three lists, synonym cycling, false ranges, decorative contrast, vague importance claims, and hidden-actor passive constructions.

Preserve legitimate field terms, cautious causal language, and standard statistical wording when they are evidence-faithful.

## Chinese Academic Checks

Use a five-step loop:

1. 定位扫描：找出套话、空转连接、机械排比、公文腔、翻译腔和低信息密度句。
2. 诊断分类：区分论证问题、证据问题、术语问题、句法问题和节奏问题。
3. 差异化改写：保留概念密度和问题意识，删空话，补逻辑词，不补假证据。
4. 五维自评：检查信息密度、论证推进、术语稳定、证据边界和句群节奏。
5. 二次复查：确认没有改动事实、引用、变量、结果、局限或作者意图。

重点清理：

- `总而言之`、`值得注意的是`、`不可忽视的是`、`多维度视角`、`双刃剑` 这类空转表达；
- 没有逻辑功能的四字套话和排比；
- 过度主语回避、隐藏被动和泛化判断；
- 句长和结构过于整齐导致的模板感；
- 结论绝对化或把相关写成因果；
- 先否定两个空靶子再揭示论点、用反转句制造戏剧性、用“深层原因”“重要意义”替代具体机制。
- 连续小碎段、整齐句式和过度一致的段尾节奏。
- 把中文概念从英文材料中自行直译，或把本地内部工程用语带进论文正文。
- 过度防御式表述，例如在贡献尚未说明前反复写“本文不能”“本文无法”“不是……而是……”。

不要为了“像人写的”加入口语、错别字、奇怪同义词、古风表达或无依据的情绪化判断。

## Output Contract

Default output:

```markdown
目标判断：语言 = ...；模式 = ...；修改幅度 = ...

锁定项：
- ...

问题清单：
- [P1/P2/P3] 类型：原句/位置 -> 问题 -> 处理方式

修改后文本：
...

二次复查：
- 主张是否改变：否/需用户确认
- 证据和引用是否改变：否/需用户确认
- 结果和不确定性是否改变：否/需用户确认
- 剩余表层风险：...
```

For detect-only requests, omit the revised text and return the issue ledger plus recommended edit strength.

## Red Lines

- Do not promise to bypass Turnitin, CNKI AMLC, GPTZero, or any detector.
- Do not alter evidence, DOI, references, quotations, data, variables, estimates, uncertainty, limitations, or author decisions.
- Do not polish unsupported causal, novelty, or policy claims into stronger language.
- Do not use external humanizer skills as separate competing routes; this helper stays under local manuscript and empirical workflows.
