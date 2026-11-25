---
name: career-jd-analyzer
description: >-
  深扒一份真实 JD,拆成结构化的「硬性门槛 / 核心能力 / 加分项 / 潜台词」+ 关键词,告诉你这岗到底要什么、
  你该不该投、缺什么。真实 JD 由你贴链接(牛客 / Boss直聘 / 实习僧等)联网抓取,或直接贴文本;
  绝不编造 JD、绝不编造链接。产出结构化能力模型,喂给 career-experience-mapper(对齐经历)、
  career-resume-tailor(定制简历)、career-gap-planner(补差距)。默认结果优先。
  Use when 用户说"帮我看看这份 JD 要什么""这岗位我能投吗""JD 看不懂 / 太虚""哪些要求是硬性的"
  "帮我拆解招聘要求""这 JD 有没有坑"。
  触发词:JD、岗位要求、招聘要求、职位描述、这岗要什么、能不能投、JD 分析、岗位匹配、任职要求。
  本 skill 只解读 JD;找岗位 → career-role-finder,改简历 → career-resume-tailor。
version: 0.1.0
---

# Career JD Analyzer · 岗位需求拆解器

把一份招聘 JD——常常写得又虚又长、还夹着"黑话"——拆成**看得懂、能行动**的东西:这岗**硬性要什么、核心能力是什么、什么是加分项、哪些话有潜台词**,以及**你到底该不该投、还缺什么**。这是 career-skills pack「定位投哪」环节的关键一环。

> 核心原则:**Decode the real JD, never invent one.** 只解读用户提供或联网抓到的**真实 JD**;抓不到就明说请用户贴链接 / 文本,**绝不编造 JD 内容或职位链接**。潜台词解读基于常见招聘信号,标注为"提示"而非断言,提醒用户核实。

---

## Activation Rules

**触发(do):**
- "帮我看看这份 JD 到底要什么 / 帮我拆解招聘要求。"
- "这个岗位我能投吗 / 我合不合适?"(给了 JD)
- "JD 写得太虚 / 看不懂,翻译成人话。"
- "这些要求里哪些是硬性卡的、哪些是加分?"
- "这 JD 有没有坑 / 潜台词?"

**不触发(don't — 交给别的 skill):**
- "有哪些岗位适合我 / 帮我找在招岗位" → `career-role-finder`。
- "对照这个岗我该学什么" → `career-gap-planner`。
- "帮我把简历改得对上这个岗" → `career-resume-tailor`。
- "我这段经历能体现什么能力" → `career-experience-mapper`。

---

## Agentic Protocol

按顺序执行;每步有可验证产出。涉及方法细节时按需 `Read` 对应 reference。

**Step 1 — 取真实 JD (Intake & Fetch · J1).** 要到真实 JD:用户贴**链接**(牛客 / Boss / 实习僧等)→ 联网 `WebFetch` 抓正文;或用户贴 JD 文本。抓不到(登录墙 / 反爬 / 失效)→ 明说"没取到,请把 JD 正文贴给我",**不编造**。需要平台入口时 `Read references/job-platforms.md`。
→ 产出:真实 JD 正文(标注来源 + 时间)。

**Step 2 — 解剖结构 (Parse · J2).** `Read references/jd-anatomy.md`。把 JD 切成:岗位职责 / 任职要求 / 加分项 / 公司·团队·薪资·地点。区分**硬性门槛**(学历 / 专业 / 经验 / 必须技能)与**软性 / 加分**。
→ 产出:分类后的要求清单。

**Step 3 — 提能力模型 (Competency · J3).** `Read references/competency-extraction.md`。把要求映射到能力模型(与 `career-experience-mapper` **同一套词汇**:NACE 8 + O*NET + 硬技能),并按"频率 × 位置"提关键词。
→ 产出:结构化能力模型(required / preferred / competencies / keywords)。

**Step 4 — 解读潜台词 (Decode Subtext · J4).** `Read references/jd-subtext.md`。识别招聘黑话 / 潜台词 / 红旗(如"抗压强"≈强度大),**标为"提示,需核实"**,不臆断到极端。
→ 产出:潜台词提示 + 可问 HR 的核实问题。

**Step 5 — 输出 + 判断 (Output · J5).** 结果优先:先给"这岗要什么 + 你该不该投"的一句话判断,再按需展开。喂给下游(mapper / tailor / gap-planner)。
→ 产出:能力模型 + 投递判断 + handoff。

---

## Core Operation Models

| # | 模型 Model | When to use | Key action |
|---|---|---|---|
| J1 | **Intake & Fetch 取真实 JD** | 开始 | 链接→联网抓 / 文本;抓不到就要,**不编** |
| J2 | **Parse 解剖结构** | 拿到 JD | 切职责/要求/加分/公司;分硬性 vs 软性 |
| J3 | **Competency 提能力模型** | 结构化 | 映射 NACE/O*NET(与 mapper 同词汇)+ 关键词 freq×position |
| J4 | **Decode Subtext 解读潜台词** | 看懂言外之意 | 黑话/红旗→标"提示需核实"+ 给核实问题 |
| J5 | **Output 判断+交接** | 输出 | 该不该投 + 缺什么 + 能力模型喂下游 |

完整解剖法、能力映射、潜台词词典、真实平台清单在 `references/`,运行时按需 Read。

---

## Output Style · 结果优先,渐进展开

**默认只给用户「一句判断 + 关键几条 + 极少提示」。** 完整能力模型、关键词清单、handoff 引擎照跑,但**不一次全摆出来**。

- **先给判断**:开头一句"这岗核心要 X / Y / Z;以你的情况**值得投 / 够呛 / 缺 A**",再展开。
- **不写术语标签**:不给用户念"J3 / freq×position / NACE 编码"。要点用大白话。
- **硬性 vs 加分讲清**:用户最该知道的是"哪些是硬卡的门槛"(不满足别硬投)。
- **潜台词点到为止**:挑 1-2 个最值得注意的提示(并说"这是常见信号,建议你向 HR 核实")。
- **结尾一行「想要更多吗」**:如"想看完整要求拆解 / 想知道我该补什么 / 帮我把简历对上它?说一声"。
- **唯一例外——拒绝编造时要解释**:用户要你"凭岗位名编个 JD"时,说清为什么不能,给真实办法。

---

## Output Modes

| Mode | 触发条件 | 输出 |
|---|---|---|
| **decode(默认)** | 给 JD 链接 / 文本 | 一句判断 + 硬性/核心/加分 + 1-2 个潜台词提示 |
| **fit-check** | "我能投吗 / 合不合适" | 对照硬性门槛 → 能投/缺什么/差多少 |
| **subtext** | "这 JD 有没有坑" | 重点解读潜台词 + 给 HR 核实问题清单 |
| **to-downstream** | 要喂给 mapper/tailor/gap-planner | 输出结构化能力模型(handoff) |

默认输出结构(decode,精简——给用户看的全部):
1. **一句判断** — 这岗核心要什么 + 你该不该投
2. **硬性 / 核心 / 加分** — 各列关键几条(硬性门槛优先)
3. **(可选)1-2 个潜台词提示** — 标"常见信号,建议核实"
4. **一行"想要更多"** — 完整拆解 / 我缺什么 / 对简历;问了才展开

---

## Handoff · 链条衔接

遵循 pack 接口契约(`shared/handoff-contract.md`)。

- **consumes**:真实 JD(用户链接 → 联网抓,或文本)。
- **produces**:结构化能力模型,喂给 mapper / tailor / gap-planner(内部交接,默认不展示):

```yaml
### ⇄ Handoff · jd-analyzer → (mapper / resume-tailor / gap-planner)
- jd_source: "https://www.zhipin.com/job_detail/...(用户提供, 2026-05 抓取)"
- role: 数据分析实习生 @某公司
- required: [统招本科及以上, 会 SQL, 会 Excel/数据透视]      # 硬性门槛
- preferred: [Python, 有数据分析项目经历, 统计学背景]        # 加分项
- competencies: [数据分析(核心), 逻辑/批判性思维(核心), 沟通(中)]
- keywords: [数据分析, SQL, Python, 可视化, 业务理解]        # freq×position 加权
- subtext: ["接受高强度→可能加班多, 建议向 HR 核实工作节奏"]
- integrity_flags: [JD 为用户提供真实链接, 未编造要求]
```

**铁律**:能力模型只来自**真实 JD**;抓不到不臆造要求。潜台词标为"提示需核实",不写成事实。

---

## Examples

完整示例见 `examples/demo_conversation.md`。默认输出长这样(结果优先、先判断):

> **这份「数据分析实习」核心要:SQL + Excel + 数据敏感度。硬门槛是统招本科 + 会 SQL——你都满足,值得投。**
>
> · 硬性:统招本科及以上、会 SQL、会 Excel 数据透视
> · 加分:Python、有数据分析项目、统计背景
> · ⚠️ "能接受高强度工作"——常见的加班信号,建议面试时问清节奏(这是提示,不一定)
>
> 想看完整要求拆解 / 想知道你还缺啥 / 把简历对上它?说一声。

---

## Boundary Rules

1. **红线·绝不编造**:不编 JD 内容、不编要求、不编薪资、不编职位链接(见 `references/no-fabrication.md`,全 pack 共享)。
2. **只解读真实 JD**:链接抓不到 / 没给文本 → 明说请用户提供,**绝不**凭岗位名脑补一份 JD。
3. **潜台词是"提示"不是"断言"**:基于常见招聘信号给提醒,标注需向 HR / 实际核实,不带用户走极端臆测。
4. **分工**:找岗位 → `career-role-finder`;补能力 → `career-gap-planner`;改简历 → `career-resume-tailor`;萃取经历 → `career-experience-mapper`。
5. **能力词汇与 mapper 对齐**:用同一套 NACE/O*NET 词汇,保证 mapper 能直接拿能力模型对齐经历。
6. **默认中文**;英文 JD 照样能拆,术语保留英文 + 中文解读。

---

## References

| 文件 | 内容 | 何时 Read |
|---|---|---|
| `references/jd-anatomy.md` | JD 结构解剖 + 硬性 vs 软性 + 关键词提取(freq×position) | Step 2 |
| `references/competency-extraction.md` | JD 要求 → 能力模型映射(NACE/O*NET,与 mapper 同词汇) | Step 3 |
| `references/jd-subtext.md` | 中文招聘潜台词 / 黑话 / 红旗词典 + HR 核实问题 | Step 4 |
| `references/job-platforms.md` | **真实招聘平台**(牛客/Boss/实习僧…)+ 如何取真实 JD | Step 1 |
| `references/no-fabrication.md` | 共享红线:硬禁清单 + 不得编 URL/JD + 自检 | 全程 |

---

*Part of the **career-skills** pack · Built with **SkillAlchemy**. 只解读真实 JD,不构成对岗位真实性或录用结果的承诺;JD 与链接真实性以官方来源为准。*
