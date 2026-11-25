---
name: regression-interpreter
description: Use this skill when reading, interpreting, or writing up regression results. Given a regression table and variable definitions, it explains each coefficient in plain language with correct direction, magnitude and units; reads log-level, log-log and standardized coefficients correctly (semi-elasticity / elasticity / standard-deviation); checks whether a results write-up overstates correlation as causation and rewrites causal wording ("causes/raises/improves") into comparison/conditional wording ("is associated with / higher / after controlling for"); distinguishes statistical from economic significance; and adds outline (**#) comments to bare regression do-files. Emphasizes comparison-not-effect framing and human review; never fabricates coefficients, data, or results.
---

# regression-interpreter（回归结果解读员）

会跑回归之后，最琐碎、也最容易出错的一步是**把系数写成人话、且不写过头**。这个技能帮你把一张回归表解读成准确的自然语言，核对对数/标准化系数的读法，并守住「相关不等于因果」这道护栏。判断权始终在你手里——AI 起草，你回到变量定义和数据核对。对应第 4 讲「AI 协作」的四项训练。

## 何时用

- 拿到一张回归表，想快速、准确地把核心系数解释成人话；
- 因变量或自变量取过对数、做过标准化，拿不准系数该按百分比、弹性还是标准差来读；
- 写完结果说明，想检查有没有把「相关」写成「导致 / 提升 / 影响」；
- 分不清「统计显著」与「经济显著」，想说清一个系数在现实里到底多大；
- 有一段光秃秃的回归 do 代码，想加上分层大纲注释、方便课堂导航与复看。

## 使用方式（提示词）

**逐个解释核心系数**：

> 你是一位计量经济学助教。下面是一张回归表和变量定义。请逐个解释【核心系数】：(1) 方向、大小和单位；(2) 若因变量/自变量取了对数，按半弹性/弹性正确解读；(3) 用「比较」而非「因果」的措辞；(4) 每个系数一句话，通俗但准确。
> 【变量定义】…　【回归表】<粘贴 esttab 输出>

**检查相关 vs 因果**：

> 请审查下面这段实证结果表述，找出把【相关关系】写成【因果关系】的地方。对每一处：(1) 指出是哪个词（如"导致""提升""使得"）；(2) 说明为何超出回归能支持的范围；(3) 给出「比较/条件」措辞的改写版本。不要改动数字与结论强度以外的内容。
> 【待审段落】<粘贴>

**核对对数、标准化的系数读法**：

> 下面是变量字典和我对系数的解读草稿。请核对解读与变量【变换方式】是否一致：因变量为 ln(·)→按百分比/半弹性读；两端都是 ln(·)→按弹性读；变量标准化→按标准差读。指出不一致处并改正。
> 【变量字典】…　【我的解读草稿】<粘贴>

**回归代码加注释版**：

> 请为下面这段 Stata 回归代码加注释：(1) 用 `**#` / `**##` 多级大纲注释标出每个分析步骤；(2) 关键命令后加一句行内注释，说明在做什么、为什么；(3) 不改动代码逻辑。
> 【原始代码】<粘贴 do 代码>

## 输出约定

- 系数解读必须说清**方向、大小、单位**，并按变换方式（水平/对数/标准化）给正确读法；
- 一律用「比较/条件」措辞（相关、更高、在控制…之后），**不下因果结论**，除非用户另给识别策略；
- 区分**统计显著**（星号、$p$ 值）与**经济显著**（用实际单位说清效应多大）；
- 加注释时不得顺手改动设定（控制变量、标准误选项等）；
- 一切以用户提供的回归表、变量定义、代码为准，**不编造系数、不虚构数据与结论**；拿不准处显式标出。

## 最小使用示例

> 用 regression-interpreter 帮我解释这张表：因变量 lwage=ln(时薪)，自变量 educ=受教育年限，educ 系数 0.109、括号 0.014、三颗星。这个系数怎么读？能说"多读一年书让工资涨 11%"吗？

## 人工检查清单

- AI 给的每一句解读，回到**变量定义与数据处理代码**核对——尤其对数系数是否被当成绝对值、百分比有没有搞反；
- 因果措辞审查可能矫枉过正，把本就恰当的表述也标成问题，由你判断；
- 变换方式以你的代码为准，别让 AI 凭变量名猜；
- **AI 辅助、不替代判断**：能否下因果结论，取决于识别策略而非回归系数本身，最终由你把关。

## 来源与许可

- 原创：本课程为「连享会 2026 暑期班·初级班」编写，Agent 无关的开放 Skill，MIT（随仓库 `LICENSE-CODE`）。
- 最后验证日期：<!-- TODO: T7 彩排 Claude Code 与 Codex 双端实测后填写 -->
