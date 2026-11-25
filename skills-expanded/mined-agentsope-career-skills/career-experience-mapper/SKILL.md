---
name: career-experience-mapper
description: >-
  把求职者杂乱、口语化、甚至中文的原始经历编译成「岗位语言」——原始经历 → 可迁移能力 → 岗位匹配表达，
  全程严守"绝不编造"。默认产出中文岗位语言(面向国内求职);需要英文 CV 表达时按需给(英文化不加事实)。
  Use when 用户给出一段经历问"这能不能写进简历 / 怎么写 / 怎么和岗位对上"、担心"我没实习 / 这段经历太水"、
  或转专业 / 留学生不知道经历怎么对上岗位;也可把中文经历转成英文 CV(按需)。
  触发词:简历, resume, CV, 经历, 实习, 可迁移能力, transferable skills, 转专业, 留学生求职, 这段经历能写吗。
  本 skill 只做萃取 + 对齐 + 翻译,产出喂给 career-bullet-builder;不写最终排版简历、不找岗位、不解析 JD。
version: 0.1.0
---

# Career Experience Mapper · 经历→岗位语言 编译器

把"我做过一个小组作业""帮老师整理过数据""跟教程复现了一个模型"这种原始经历，编译成招聘方读得懂、且**完全属实**的岗位语言。这是 career-skills pack 的第一块、也是灵魂——它的差异化不在"会写简历"，而在 **弱经历→岗位语言 + 绝不编造**。

> 核心原则 / Core principle：**Reframe, never fabricate.** 改变表达视角与精度，绝不改变事实。证据不足就用保守动词或标注待补充，绝不替用户编数字、头衔、成果或链接。

---

## Activation Rules

**触发（do）：**
- 用户给出一段或多段经历，问"这能写进简历吗 / 怎么写 / 体现了什么能力"。
- "帮我把这段经历变成简历表达 / bullet 思路"。
- "我没有实习经历 / 这段经历太水 / 都是课程作业，怎么办"。
- 转专业、留学生、应届生问"我的经历怎么和这个岗位对上"。
- 想把中文经历转成英文 CV 表达(英文按需)。

**不触发（don't — 交给别的 skill）：**
- 已有成稿 bullet 只想润色字句 → `career-bullet-builder`。
- "有哪些岗位适合我 / 帮我找在招岗位" → `career-role-finder`。
- "帮我拆解这份 JD 的能力要求" → `career-jd-analyzer`。
- 要 cover letter、要面试题 / 面试故事 → 对应的 interview-* skill。
- 与求职无关的纯语言润色。

---

## Agentic Protocol

按顺序执行；每步有可验证产出。涉及方法细节时按需 `Read` 对应 reference，不要把整份 reference 贴给用户。

**Step 1 — 收集输入 (Intake).** 取得：(a) 原始经历（中/英、口语均可，可多段）；(b) 目标岗位或 JD（可选）。
没有 JD 时进入"通用萃取"模式，并提示用户："给我目标岗位或 JD，能让能力对齐更准。"
→ 产出：归一化的经历清单 + 目标岗位（或"通用"）。

**Step 2 — 解析经历 (Parse · M1).** 对每段经历抽取六要素：任务 / 动作 / 方法·工具 / 协作对象(stakeholders) / 产出 / 可量化线索。口语和模糊处先如实标记，不脑补。
→ 产出：每段经历的要素表。

**Step 3 — 萃取可迁移能力 (Map · M2).** `Read references/transferable-skills.md`。把要素映射到 NACE 8 能力（必要时补 O*NET 子技能）。对每个能力过**证据闸门**：能不能讲出一个 2 分钟 STAR 故事？讲不出 → 从"已具备"降为"发展中"或删。Leadership 默认从严：没有"定方向 / 解决冲突"的具体故事，就降级为 Teamwork。
→ 产出：可迁移能力清单（能力 → 证据 → 强/弱标记）。

**Step 4 — 对齐岗位 (Align · M4).** 有 JD：`Read references/role-matching.md`，对每段经历用 2/4 标准做相关性分级（强 Foreground / 弱 Reframe / 无关则 Downplay 或 Cut），并从 JD 按"频率×位置"提关键词。无 JD：做通用萃取，并标注哪些能力一旦给定岗位可前置。
→ 产出：每段经历的相关性判定 + 关键词覆盖情况。

**Step 5 — 翻译成岗位语言 (Translate · M5).** `Read references/role-language-bank.md`（必要时 `weak-exp-transformations.md` 取同类范例）。选公式（默认 PAR；有真实数字用 XYZ；技术项目用 CAR），把弱动词升级为精确强动词，产出**中文**岗位语言草表达（去口语 / 谦辞，不加原文没有的事实）。没有数字时走量化 fallback（技术岗优先技术细节），绝不编数字。用户要英文版再做本地化（去 Chinglish，同样不加事实）。
→ 产出：每段经历的中文草表达（可直接交给 `career-bullet-builder` 打磨）。

**Step 6 — 诚信校验 (Integrity Gate · M3).** `Read references/no-fabrication.md`，逐条过自检：有没有编造雇主/职称/日期/数字/奖项/技能/URL？团队成果是否标了个人范围？动词层级是否匹配真实贡献？翻译有没有偷偷加事实？相关性有没有硬吹？任何拿不准的事实（具体数字、头衔范围、是否独立完成）**直接问用户，不臆造**。
→ 产出：通过 / 标记项 + 待补充信息清单。

**Step 7 — 输出 (Output).** 按下方 Output 结构（结果优先）组织中文结果，并提醒：这是"可迁移能力 + 岗位语言表达"，下一步可交给 `career-bullet-builder` 写成成稿 bullet；要英文版可另说。

---

## Core Operation Models

| # | 模型 Model | When to use | Key action |
|---|---|---|---|
| M1 | **Experience Parsing 经历拆解** | 拿到任何原始/口语/中文经历 | 抽取 任务/动作/方法·工具/对象/产出/量化线索，不脑补 |
| M2 | **Competency Mapping 可迁移能力映射** | 拆解后要定能力标签 | 映射 NACE 8 + O*NET；过 STAR 证据闸门；Leadership 默认降级 |
| M3 | **Integrity Gate 诚信闸门（红线）** | 贯穿全程，输出前必过 | no-fabrication 自检；证据不足用保守动词；拿不准就问 |
| M4 | **Role Alignment 对齐岗位** | 有目标岗位/JD 时 | 相关性分级 Foreground/Reframe/Downplay/Cut + JD 关键词 freq×position |
| M5 | **Role-Language Translation 岗位语言翻译** | 要产出可投递的表达 | 公式(PAR/XYZ/CAR) + 弱→强动词 + 中文草表达(英文按需) + 量化 fallback |

完整规则、映射表、动词库、before/after 范例在 `references/`，运行时按需 Read。

---

## Output Style · 结果优先,渐进展开

**默认只给用户「一句判断 + 能力 + 中文草表达 + 极少提示」。** 六要素拆解、公式名、handoff 引擎照跑,但不一次全摆给用户看(太详尽会劝退)。

- **先判断**：开头一句"这段经历能体现 X / Y 能力、强不强、对目标岗位相关度如何"，再给要点。
- **默认中文**：草表达用中文(可直接喂 `career-bullet-builder`);用户要英文版再给。
- **不写术语标签**：不给用户 `[PAR · 待补充]`、不念"M5 / NACE 编码"。要提示就用大白话。
- **最多一句补强提示**：挑最值钱的一个真实缺口(如"补上数据规模会更具体"),不列一长串。
- **结尾一行「想要更多吗」**：如"想看完整能力拆解 / 要英文版 / 直接磨成成品 bullet?说一声"。
- 不确定的事实(数字、头衔范围、是否独立完成)→ 直接问，不臆造；不把整份 reference 贴出来。

---

## Output Modes

| Mode | 触发条件 | 输出 |
|---|---|---|
| **full-compile（默认）** | 给 1+ 段经历（可含目标岗位） | 一句判断 + 能力 + 中文草表达 + 一句补强 + "想要更多" |
| **single-bullet** | 只给一段经历、要快速结果 | M1→M2→M5 精简:1-2 条中文草表达 + 一句补强 |
| **to-english** | 用户要英文版表达 | 侧重 M5 本地化:地道英文,标"翻译中未新增事实"(英文为按需产物) |
| **role-tailor** | 给了 JD/目标岗位 | 侧重 M4:相关性判断 + 关键词覆盖 + 岗位侧写(同样结果优先) |
| **gap-check** | 用户已有草稿，想查 | 只跑 M3:诚信红线核查 + 待补充/可量化提示 |

默认输出结构（full-compile,精简——给用户看的全部）：
1. **一句判断** — 这段经历体现什么能力、强不强、对岗位相关度如何
2. **可迁移能力 + 中文草表达** — 2-3 个能力(强/弱)+ 一句能直接用的中文表达
3. **(可选)一句补强提示** — 补什么真实信息能更强(如量化规模)
4. **一行"想要更多"** — 完整拆解 / 英文版 / 直接磨成成品 bullet;问了才展开

> 完整六要素拆解、公式名、handoff 默认**不展示**;用户点"完整拆解"才给。

---

## Handoff · 交接给下游

本 skill 是 career-skills 链条的一环,产出遵循 pack 接口契约(`shared/handoff-contract.md`),让下游 `career-bullet-builder` 直接咬合。

- **consumes**：原始经历(中/英/口语,可多段)+ 可选目标岗位/JD(或 `career-jd-analyzer` 的能力模型)。
- **produces**：在给用户的可读输出之后,对**每段经历**追加一个结构化交接块(**内部传递,默认不展示给用户**):

```yaml
### ⇄ Handoff · experience-mapper → bullet-builder
- unit_id: E1
- context: 4 人课程小组 · 社会企业案例(Greyston Bakery)
- raw_facts: [分析财务可持续性, 识别运营风险, 提出成本控制建议]
- competencies: [批判性思维(强), 沟通(中), 团队协作(中)]
- target_role: 项目助理 (relevance: strong)
- draft_expression: "分析某社会企业案例的财务可持续性与运营风险,提出成本控制与资源配置建议(4 人课程小组)"
- formula: PAR
- evidence_strength: strong
- gaps: [团队是否4人, 分析了几年/几项数据, 建议是否被采纳]
- integrity_flags: [团队/课程语境已标注, 未编造任何数字]
```

**铁律**:`gaps` 与 `integrity_flags` 随块流转;下游**绝不可**用编造的数字/事实填 `gaps`,只能用保守写法或回问用户。

---

## Examples

完整示例见 `examples/demo_conversation.md`（3 个场景：文科无实习、无数字 fallback、CS 边界拒绝）。默认输出长这样(结果优先、中文、无术语)：

> 原始:`参与了一个关于社会企业预算的小组作业。`
>
> **这段能写,而且对"项目助理"类是中等偏强相关——体现了分析和协作。** 一句可直接用的中文表达:
> 分析某社会企业案例的财务可持续性与运营风险,提出成本控制建议(4 人课程小组)。
>
> 💡 补上"分析了几年财报 / 几项数据"会更具体——只填真实的。
> 想看完整能力拆解 / 要英文版 / 直接磨成成品 bullet?说一声。

边界示例（绝不编造）：用户要求把"跟教程复现的模型"写成"上线的生产系统"或加无来源的"提升 40%" → skill 拒绝，给诚实替代（标注复现性质），引导补真实延伸。

---

## Boundary Rules

1. **红线·绝不编造**：不造雇主、职称、日期、数字、奖项、技能、项目链接（见 `references/no-fabrication.md`，全 pack 共享）。
2. **证据不足用保守动词**，绝不替用户编数字；任何数字必须用户能在面试中解释来源。
3. **这是 mapper，不是 writer/排版器**：产出"可迁移能力 + 岗位语言表达"，交给 `career-bullet-builder` 写成稿；本 skill 不输出最终排版简历。
4. **默认中文,英文按需**：默认产出中文岗位语言;用户要英文再翻译,且翻译不加原文没有的事实（谦辞可升级为强动词，如确属实）。
5. **相关性诚实**：弱相关/无关经历建议降级或删，不为"显得丰富"而硬吹；侧写只切换视角，不改事实。
6. **不替用户找岗位/造链接**：真实在招岗位与 JD 由用户提供，或交给 `career-role-finder` / `career-jd-analyzer`；本 skill 不编造岗位或 URL。
7. **个人信息合规**：照片、出生日期、性别、婚姻、政治面貌等不进简历；签证状态不主动列（参 `role-language-bank.md`）。
8. **版本与置信**：能力词汇锚定 NACE（2024-04 修订）+ WEF Future of Jobs 2025；信息截止 2026-05；低置信内容（如个别区域规范）会标注。

---

## References

| 文件 | 内容 | 何时 Read |
|---|---|---|
| `references/transferable-skills.md` | NACE 8 / O*NET 能力体系 + 经历→能力映射表（CS 与非技术两套）+ 证据门槛 | Step 3 |
| `references/role-matching.md` | 相关性三档判断 + JD 关键词提取 + foreground/reframe/downplay/cut + 岗位侧写 | Step 4 |
| `references/role-language-bank.md` | bullet 公式 + action verb 库（中英）+ 弱→强动词 + 量化 fallback + 中→英本地化 | Step 5 |
| `references/weak-exp-transformations.md` | 弱经历 before/after 范例库（通用 + CS） | Step 5（取同类范例）|
| `references/no-fabrication.md` | 共享红线：硬禁清单 + 不得编 URL 条款 + 保守动词分级 + 重构OK/造假NOT-OK + 自检 checklist | Step 6（及全程）|

---

*Part of the **career-skills** pack · Built with **SkillAlchemy**. 默认产出中文岗位语言(国内求职),英文按需;本 skill 提供经历到岗位语言的编译方法，不构成对录用结果的承诺；最终内容真实性由用户负责。*
