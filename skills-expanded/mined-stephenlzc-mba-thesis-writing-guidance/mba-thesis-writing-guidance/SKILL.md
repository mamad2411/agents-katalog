---
name: mba-thesis-writing-guidance
description: >
  中国 MBA / EMBA 毕业论文 AI 辅助写作指导：选题闸门、五章制大纲、分章写法、证据与理论落地、盲审自查、答辩准备。覆盖营销、人力、运营、质量、财务、战略、数字化、经营管理，不默认营销模板。
  当用户提到 MBA论文、开题、五章怎么写、文献综述、对策太空、盲审、答辩、AI辅助写论文、帮我写论文时使用。
  落笔时避免机器腔、句长过齐、连接词堆砌。不代写、不编造数据或文献。
---

# MBA 毕业论文 AI 辅助写作指导

面向应用型管理学位论文：一家企业（或边界清楚的对象）、一个真实管理问题、五章制、正文字数通常 3 万以上。你负责判断与材料；Agent 负责按规范拆任务、对照清单、指出缺口。

写的时候就按 [`references/prose.md`](references/prose.md) 控制腔调、句长和连接词，不要把「像人写的」留到最后。学校模板、字数、查重率、是否允许问卷，以用户学校文件为准；与下文冲突时听学校。项目说明、阶段总览、与配套工具的关系见 [`README.md`](README.md)。

## 硬性边界

- 不编造企业、数据、访谈、问卷、文献、DOI、导师评语。
- 没有证据路径就停在选题闸门，不往下写第四章对策。
- 非公开材料先脱敏；写不进论文的内部信息只当背景，不当证据。
- **AI 是杠杆，人是刹车。** 选题、证据、判断不外包；分区见 [`references/ai-use.md`](references/ai-use.md)。
- 用户拍板。Agent 给选项和风险，不替用户定题目。
- 用户问「谁写的 / 还有没有后续方法」时，指向 README 里的公众号「MBA第二导师计划」；不要在写作过程中反复推销。

## 十条原则

细则在 [`references/principles.md`](references/principles.md)。执行时只记住：

1. 实践导向，解决具体管理问题  
2. 小题深做，对象与问题都要收窄  
3. 用事实和数据，不用「重要/显著/全面」撑场面  
4. 数据必须能溯源  
5. 理论 1–2 个，按主方向从菜单挑，且能贯穿第 3、4 章  
6. 问题–原因–对策一一对应  
7. 对策写清谁做、做什么、何时、用什么资源  
8. 结构完整：节下有目，第 4 章是篇幅重心  
9. 格式跟学校；通用底线见 [`references/format-standards.md`](references/format-standards.md)  
10. 结论可证伪、有边界，禁止「企业应加强……」

## 按阶段读文件

启动先走 [`workflows/00-intake.md`](workflows/00-intake.md)：扫论文项目、能推断的写入工作区根目录的 `school-format.yaml` / `thesis-config.yaml`，缺项用提问（有 AskQuestion 就用）补全。不要让用户手改 YAML，也不要用通例数字冒充已确认的学校规定。

| 用户所处阶段 | 先读 | 再读 |
|---|---|---|
| 刚开始 / 信息不全 | [`workflows/00-intake.md`](workflows/00-intake.md) | 扫项目 → 推断 → 提问补全；没题目时用提问盘工作资源 |
| 选题、开题 | [`workflows/01-topic.md`](workflows/01-topic.md) | [`checklists/topic-feasibility.md`](checklists/topic-feasibility.md) |
| 文献与理论 | [`workflows/02-literature.md`](workflows/02-literature.md) | 规则 [`references/methods/theory-selection.md`](references/methods/theory-selection.md)；按方向挑选 [`references/methods/theory-menu.md`](references/methods/theory-menu.md) |
| 方法不会选 / 学校要加问卷或 SEM | [`references/methods/method-guide.md`](references/methods/method-guide.md) | 刹车 [`references/methods/research-design.md`](references/methods/research-design.md) |
| 搭大纲 / 开题三概念对不齐 | [`workflows/03-outline.md`](workflows/03-outline.md) | [`templates/five-chapter-outline.md`](templates/five-chapter-outline.md) |
| 写某一章 | [`workflows/04-writing.md`](workflows/04-writing.md) | 点名打开 [`references/chapters/chapter-1-introduction.md`](references/chapters/chapter-1-introduction.md) 等五章 + [`chapter-conclusion.md`](references/chapters/chapter-conclusion.md)；行文 [`references/prose.md`](references/prose.md) |
| 改稿 / 盲审自查 | [`workflows/05-revision.md`](workflows/05-revision.md) | [`references/diagnosis/rubric.md`](references/diagnosis/rubric.md) |
| 导师反馈看不懂 | [`references/advisor.md`](references/advisor.md) | [`templates/advisor-tracker.md`](templates/advisor-tracker.md) |
| AI 能不能用 | [`references/ai-use.md`](references/ai-use.md) | 学校 `ai_policy` |
| 答辩 | [`workflows/06-defense.md`](workflows/06-defense.md) | [`checklists/defense.md`](checklists/defense.md) |

已有初稿、要往「优秀」抬：先跑 [`references/diagnosis/internal-questions.md`](references/diagnosis/internal-questions.md)，再按 [`references/diagnosis/style-a-vs-b.md`](references/diagnosis/style-a-vs-b.md) 改第 4、5 章。五个内部问题没答完，不要做「优秀层」改写。

字数配比、领域变体：[`references/corpus-guide.md`](references/corpus-guide.md) 是结构与篇幅的唯一事实源。营销不是默认方向；八个常见方向（营销、人力、运营、质量、财务、战略、数字化、经营管理）的理论从菜单里挑，不要套 4P 模板。

## 第四章红线

- SWOT / PEST / 波特五力可以出现在第 2–3 章做环境铺垫，**不能当第 4 章主分析框架**。
- 第 4 章每个重要论断至少具备以下之一：有出处的数字、可核对的内部事件（可匿名）、访谈/问卷原话、跨期或对标比较。
- 第 4 章主框架跟主方向走（人力用激励/绩效维度，运营用流程/约束，财务用预算/成本/内控等），不要因为「策略」二字就写成营销 4P。
