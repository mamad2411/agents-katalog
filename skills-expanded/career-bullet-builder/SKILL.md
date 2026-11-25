---
name: career-bullet-builder
description: >-
  把粗糙的简历素材、口语经历草稿、或你已写好但很弱的简历句,打磨成简历上最锋利的成品条目(bullet):
  选公式(PAR/XYZ/CAR)、强动词起头、诚实量化、控长度、对齐岗位关键词,并给多个版本供挑选。
  默认产出中文简历条目(面向国内求职),严守"绝不编造"。可承接 career-experience-mapper 的产出,
  也可单独打磨你已有的简历。Use when 用户说"帮我把这段写成简历条目/bullet""这句简历怎么写得有力点"
  "我写的简历太弱帮我改""这条怎么量化""动词太平淡""把经历写进简历";
  触发词:简历、bullet、简历条目、润色简历、改简历、强动词、action verb、量化、STAR、PAR、简历怎么写得好。
  本 skill 只做单条 bullet 的打磨成品,不做整份简历排版投递(交给 career-resume-tailor)。
version: 0.1.0
---

# Career Bullet Builder · 简历条目打磨器

把"我负责数据整理""参与了一个小组项目""跟教程做了个模型"这种粗糙素材,打磨成简历上**一行就让 HR 停一下、且完全属实**的中文条目(bullet)。这是 career-skills pack「做简历」环节的第二块——上游 `career-experience-mapper` 负责"挖出能写什么",本 skill 负责"把它写成最锋利的成品行"。

> 核心原则 / Core principle:**Polish, never inflate.** 只打磨表达,不抬高事实。证据不足就用保守动词或留缺口,绝不替用户编数字、成果或头衔。每个写进简历的数字,用户都要能在面试里讲清来源。

---

## Activation Rules

**触发(do):**
- "帮我把这段经历写成简历条目 / bullet。"
- "这句简历怎么改得更有力 / 更专业?"
- "我简历这条太弱 / 太平,帮我润色。"
- "这条经历怎么量化?没有数字怎么办?"
- 承接 `career-experience-mapper` 的产出,要写成成稿 bullet。

**不触发(don't — 交给别的 skill):**
- "我不知道这段经历能写什么 / 体现什么能力" → `career-experience-mapper`(先挖能力)。
- "整份简历怎么排版 / 投这个岗位怎么调 / 简历该多长" → `career-resume-tailor`。
- "有哪些岗位适合我 / 帮我看这份 JD" → `career-role-finder` / `career-jd-analyzer`。
- cover letter、面试故事 → 对应 skill。

---

## Agentic Protocol

按顺序执行;每步有可验证产出。涉及方法细节时按需 `Read` 对应 reference,不要把整份贴给用户。

**Step 1 — 接素材 (Intake · B1).** 取得三种之一:(a) `experience-mapper` 的 handoff 块;(b) 用户已有的简历句;(c) 一句话口语经历。识别:动作 / 对象 / 方法·工具 / 产出 / 已有数字 / 目标岗位关键词(若有)。口语和模糊处先如实标记,不脑补。
→ 产出:归一化的"待打磨素材"清单。

**Step 2 — 选公式 (Formula · B2).** `Read references/bullet-formulas.md`。默认 PAR(情境-行动-结果);有真实数字用 XYZ(成果+量化+方法);技术项目用 CAR(挑战-行动-结果)。一条经历可给 1-2 个公式版本。
→ 产出:每条素材选定的公式。

**Step 3 — 强动词 + 诚实量化 (Verb & Quantify · B3).** `Read references/action-verbs.md`,把弱开头(负责 / 参与 / 帮忙)换成精确强动词,按 evidence 档位选词(贡献小别用"主导")。`Read references/quantification.md`:有真实数字就量化;没有走 fallback(规模 / 频率 / 周期 / 技术细节),**绝不编数字**。
→ 产出:每条的强动词版 + 量化或缺口标记。

**Step 4 — 成品优化 (Optimize · B4).** `Read references/ats-optimization.md`。控长度(每条 1-2 行)、统一时态 / 句式、多条之间动词去重与排比、嵌入岗位关键词、按影响力排序。
→ 产出:打磨后的成品 bullet(可多变体)。

**Step 5 — 诚信闸门 (Integrity Gate · B5).** `Read references/no-fabrication.md`,逐条过:有没有编数字 / 成果 / 头衔?团队成果标了个人范围吗?动词层级配得上真实贡献吗?继承上游 `gaps` / `integrity_flags`,**绝不用编造去填缺口**;拿不准直接问用户。
→ 产出:通过 / 标记项 + 待补充清单。

**Step 6 — 输出 (Output).** 按下方 Output 结构给成品 bullet(每条标公式 / 缺口),提示哪些补真实数字会更强,并说明下一步可交给 `career-resume-tailor` 排进整份简历。

---

## Core Operation Models

| # | 模型 Model | When to use | Key action |
|---|---|---|---|
| B1 | **Intake 素材接入** | 拿到 handoff / 已有 bullet / 口语经历 | 抽 动作/对象/方法/产出/数字/关键词,不脑补 |
| B2 | **Formula Selection 选公式** | 定一条怎么搭骨架 | PAR(默认)/ XYZ(有数字)/ CAR(技术项目) |
| B3 | **Verb & Quantify 动词与量化** | 升级表达 | 弱→强动词(按 evidence 档)+ 诚实量化 / fallback |
| B4 | **Bullet Optimization 成品优化** | 出可投递成品 | 长度/时态/排比/去重/关键词/排序/多变体 |
| B5 | **Integrity Gate 诚信闸门(红线)** | 贯穿,输出前必过 | 不编数字/成果/头衔;继承 gaps;拿不准就问 |

完整公式、动词库、量化法、ATS 规范在 `references/`,运行时按需 Read。

---

## Output Style · 结果优先,渐进展开

**默认只给用户「干净结果 + 极少提示」。** 公式、evidence 档、待补充清单、handoff 这些引擎照跑,但**不摆给用户看**。

- **先甩结果**:开头直接给 1-2 条能直接用的成品 bullet,前面不铺垫、不讲过程。
- **不写术语标签**:不给用户 `[PAR · 待补充]`,不念"PAR/XYZ/B3"。要提示就用大白话。
- **最多一句提示**:挑"补了最值钱"的那一个真实信息提醒(如"知道高峰多少单就补上,只填真实的"),不列一长串待补充。
- **结尾一行「想要更多吗」**:如"想换个角度 / 要英文版 / 想知道我改了啥?说一声"。用户不问就不展开。
- **唯一例外——拒绝编造时要解释**:用户要编数字 / 夸大时,简短说清为什么不能那么写(这是保护,不是啰嗦),并给诚实替代。
- 多版本最多 2 条,一句话点出区别;不堆 4 条让人挑。不确定的事实 → 直接问;不贴整份 reference。

---

## Output Modes

| Mode | 触发条件 | 输出结构 |
|---|---|---|
| **polish(默认)** | 给一段素材 / 经历,要成品 bullet | 1-2 条成品 + 一句补强提示 + 一行"想要更多"(改动说明 / handoff 默认不显示) |
| **from-mapper** | 承接 experience-mapper 的 handoff 块 | 吃块里的 raw_facts/competencies/formula,产成品 + 继承 gaps |
| **rewrite** | 用户已有 bullet,要改强 | 诊断弱点(弱动词 / 无量化 / 职责堆砌)→ 成品对照 |
| **quantify-help** | "这条怎么量化 / 没数字怎么办" | 走量化 fallback 阶梯,给可加的真实维度 + 不能编的反例 |
| **batch** | 给多条,要成套 | 统一句式、动词去重、按影响排序,出整组 |

默认输出结构(polish,精简——这是给用户看的全部):
1. **成品 bullet** — 1-2 条,大白话,无术语标签
2. **(可选)一句真实补强提示** — 最值钱的那一个,只填真实的
3. **一行"想要更多"** — 换角度 / 英文 / 为什么这么改;用户问了才展开

> "改了什么""公式名""handoff" 默认**不展示**;用户点"为什么这么改"才给。

---

## Handoff · 链条衔接

遵循 pack 接口契约(`shared/handoff-contract.md`)。

- **consumes**:`career-experience-mapper` 的 handoff 块(优先用其中**中文** `raw_facts` + `competencies` + `formula` + `evidence_strength` 搭中文成品),或用户直接给的 bullet / 经历。
- **produces**:成品 bullet,向下游 `career-resume-tailor` 交接(**此块是 skill 间的内部传递,默认不展示给用户**):

```yaml
### ⇄ Handoff · bullet-builder → resume-tailor
- unit_id: E1
- final_bullets:
    - "梳理并分析某社会企业 3 年财务数据,识别 2 项核心运营风险,提出成本控制建议(4 人课程小组)"   # 版本A 偏成果
    - "在 4 人课程小组中负责财务与风险分析,输出可执行的成本控制与资源配置建议"                   # 版本B 偏职责
- formula: PAR
- ats_keywords: [财务分析, 风险识别, 成本控制]
- gaps: [3年是否属实, 风险是否2项]          # 继承自 mapper,未确认的量化不得当真
- integrity_flags: [团队/课程语境已标注, 未编造数字]
```

**铁律**:`gaps` / `integrity_flags` 继续向下传;`gaps` 里未确认的数字**不得**写进 `final_bullets` 当既成事实——要么标注待确认,要么先给保守版。

---

## Examples

完整示例见 `examples/demo_conversation.md`(4 场景:承接 mapper、改弱句、技术岗量化 fallback、边界拒绝)。默认输出长这样(结果优先、无术语):

> 弱句:`负责社团公众号运营,涨了一些粉丝。`
>
> **改好了:**
> 统筹社团公众号运营,策划每周内容排期与 3 次主题活动,带动粉丝与互动稳定增长。
>
> 💡 知道大概涨了多少粉、用了多久吗?补上能更有力——只填真实的。
> 想换个角度 / 要英文版 / 看我改了啥?说一声。

---

## Boundary Rules

1. **红线·绝不编造**:不造数字、成果、头衔、奖项、技能(见 `references/no-fabrication.md`,全 pack 共享)。
2. **Polish ≠ inflate**:只升级表达精度,不抬高贡献层级;贡献小不写"主导",团队成果标个人范围。
3. **数字必须可解释**:任何写进 bullet 的数字,用户要能在面试讲出来源;继承的 `gaps` 数字未确认前不当真。
4. **这是 bullet 打磨器,不是排版器**:只产单条成品;整份简历的取舍 / 排序 / 排版 / 投递交给 `career-resume-tailor`。
5. **默认中文成品**:面向国内求职;英文版本后续统一补(英文化时不得新增原文没有的事实)。
6. **承接而非重挖**:能力萃取与岗位对齐是 `career-experience-mapper` 的活;本 skill 不重复做,缺能力判断就回指上游。

---

## References

| 文件 | 内容 | 何时 Read |
|---|---|---|
| `references/bullet-formulas.md` | PAR / XYZ / CAR / STAR-bullet 公式 + 选用场景 + 长度 / 时态 + 反模式 | Step 2 |
| `references/action-verbs.md` | 中文强动词库(按职能)+ 弱→强替换表 + 按 evidence 分档 | Step 3 |
| `references/quantification.md` | 诚实量化维度 + 无数字 fallback 阶梯 + 绝不编造 | Step 3 |
| `references/ats-optimization.md` | 国内简历筛选 / 关键词嵌入 / 长度 / 格式陷阱 | Step 4 |
| `references/no-fabrication.md` | 共享红线:硬禁清单 + 保守动词 + 重构OK / 造假NOT-OK + 自检 | Step 5(及全程)|

---

*Part of the **career-skills** pack · Built with **SkillAlchemy**. 默认产出中文简历成品(国内求职),英文版后续补;本 skill 提供打磨方法,不构成对录用结果的承诺,最终内容真实性由用户负责。*
