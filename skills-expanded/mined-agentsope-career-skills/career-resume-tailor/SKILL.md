---
name: career-resume-tailor
description: >-
  把一堆成品简历 bullet + 目标岗位,组装成一份针对该岗位、可直接投递的中文简历:挑哪些经历、怎么排序取舍、
  整份结构(教育/实习/项目/技能)、控制长度(应届一页)、整体对齐 JD 关键词,并能为不同岗位出不同投递版本。
  默认结果优先(先给成品简历,深的藏在"想要更多"后面),严守绝不编造、绝不编造职位链接
  (真实 JD 由你贴链接或联网抓)。承接 career-bullet-builder 的产出。
  Use when 用户说"帮我把简历针对这个岗位调一下""投这个岗要改啥""把这些经历组装成一份简历"
  "简历太长怎么砍""这份简历投 X 岗合适吗"。
  触发词:简历投递、简历排版、针对岗位改简历、简历太长、简历结构、投递版本、校招简历、一页简历、resume。
  本 skill 做整份简历的取舍/排序/结构/投递;不打磨单条 bullet(→ career-bullet-builder)、不挖能力(→ career-experience-mapper)、不找岗位(→ career-role-finder)。
version: 0.1.0
---

# Career Resume Tailor · 简历投递定制器

把一堆打磨好的 bullet 和"我要投这个岗",变成一份**结构清楚、详略得当、对得上岗位、可直接投递的中文简历**。这是 career-skills pack「做简历」环节的收口——上游 `career-bullet-builder` 把每条经历磨成成品行,本 skill 决定**这份简历放哪些、怎么排、砍到多长、怎么对上这个岗**。

> 核心原则:**Tailor to the job, never fake the job.** 针对岗位做取舍和侧重,但不编造经历、不编造数字、不编造职位链接。真实 JD 由用户提供或联网抓取;抓不到就明说,绝不造 URL。

---

## Activation Rules

**触发(do):**
- "帮我把简历针对这个岗位调一下 / 投这个岗要改啥?"
- "把这些经历组装成一份简历。"
- "我简历太长 / 太乱,帮我砍到一页、排好。"
- "同一份简历投运营和投数据,怎么各出一版?"
- "这份简历投 X 岗合适吗?投递前帮我体检。"

**不触发(don't — 交给别的 skill):**
- "帮我把这一条写得更有力" → `career-bullet-builder`(单条打磨)。
- "我这段经历能体现什么能力" → `career-experience-mapper`。
- "有哪些岗位适合我 / 帮我找在招" → `career-role-finder`。
- "帮我深扒这份 JD 的能力要求" → `career-jd-analyzer`。

---

## Agentic Protocol

按顺序执行;每步有可验证产出。涉及方法细节时按需 `Read` 对应 reference。

**Step 1 — 接素材 (Intake · T1).** 取得:(a) `career-bullet-builder` 的成品 bullets(或用户已有简历);(b) 目标岗位 / JD——**优先要真实链接**(牛客 / Boss / 实习僧等),用户给链接我联网抓,或贴 JD 文本。没有目标岗位时提示:"给我目标岗位或 JD 链接,我才能对着调;否则只能出通用版。"
→ 产出:bullet 池 + 目标 JD(真实)或"通用"。

**Step 2 — 取舍与排序 (Select & Order · T2).** 按与 JD 的相关性给经历/bullet 分级:强相关前置、弱相关精简、无关删。最相关的经历放最前、每段最有力的 bullet 放第一条。
→ 产出:留用清单 + 排序。

**Step 3 — 结构编排 (Structure · T3).** `Read references/resume-structure.md`。定模块顺序(应届默认:教育 → 实习/项目 → 技能 → 校园经历;有强相关实习则前移)、倒序排列、砍到合适长度(应届一页)。
→ 产出:整份简历骨架。

**Step 4 — 针对岗位定制 (Tailor · T4).** `Read references/tailoring-by-jd.md`。整体对齐 JD 关键词(用原词)、按岗位调整详略侧重;要投多个岗位时出多个投递版本。需要真实岗位/JD 时 `Read references/job-platforms.md` 取真实来源。
→ 产出:针对该岗位的简历(可多版本)。

**Step 5 — 诚信 + 格式 + 合规闸门 (Gate · T5).** `Read references/no-fabrication.md`。核查:没有为对岗位而编造经历/数字/链接;继承的 `gaps` 未确认数字不写死;ATS 格式无雷(见 `resume-structure.md`);个人信息合规(照片/出生日期/性别等不进简历)。
→ 产出:通过 / 待补充 + 投递建议。

**Step 6 — 输出 (Output).** 按结果优先给整份简历 + 一句最关键的补强/取舍提示 + 一行"想要更多"。

---

## Core Operation Models

| # | 模型 Model | When to use | Key action |
|---|---|---|---|
| T1 | **Intake 接素材** | 拿到 bullets + 目标岗位 | 收成品 bullet + 真实 JD(链接优先,联网抓) |
| T2 | **Select & Order 取舍排序** | 决定放哪些、怎么排 | 按 JD 相关性 前置/精简/删 + 影响力排序 |
| T3 | **Structure 结构编排** | 组装整份 | 模块顺序 + 倒序 + 砍到一页 |
| T4 | **Tailor 针对岗位** | 对上特定岗位 | 关键词对齐 + 详略侧重 + 多投递版本 |
| T5 | **Integrity+Format Gate(红线)** | 输出前必过 | 不编经历/数字/链接;ATS 格式;信息合规 |

完整结构规范、JD 对齐法、真实平台清单在 `references/`,运行时按需 Read。

---

## Output Style · 结果优先,渐进展开

**默认只给用户「整份成品简历 + 极少提示」。** 取舍理由、关键词清单、handoff 这些引擎照跑,但**不摆给用户看**。

- **先甩成品**:直接给排好的整份简历(或修改后的版本),前面不长篇讲过程。
- **不写术语标签**:不给用户念"T2/ATS 权重/relevance 分级"。要提示就用大白话。
- **最多一句关键提示**:挑最值钱的一个(如"你这份对该岗最弱的是 XX 经历,我往后挪了/建议删")。
- **结尾一行「想要更多吗」**:如"想出第二个岗位的版本 / 要英文版 / 想知道我砍了啥、为什么?说一声"。
- **唯一例外——拒绝编造时要解释**:用户要为对岗位而加假经历/假数字/假链接时,简短说清为什么不能,给诚实替代。
- 不确定就问(投哪个岗、要不要留某段);不把整份 reference 贴出来。

---

## Output Modes

| Mode | 触发条件 | 输出 |
|---|---|---|
| **full-tailor(默认)** | 一堆 bullet + 目标岗位 | 针对该岗的整份中文简历 + 一句关键提示 |
| **reorder-trim** | 已有简历太长/乱 | 取舍 + 排序 + 砍到一页 |
| **multi-version** | 要投多个岗位 | 一份底稿 → 各岗位侧重不同的投递版 |
| **jd-align** | 给 JD(链接/文本) | 现有简历对齐该 JD 的关键词与侧重 |
| **check** | 投递前体检 | 格式 / 长度 / 信息合规 / 关键词 快检 + 修订 |

默认输出结构(full-tailor,精简——给用户看的全部):
1. **整份简历** — 排好、对上岗位、控制好长度
2. **(可选)一句关键提示** — 最该补/该删/该确认的那一个
3. **一行"想要更多"** — 多版本 / 英文 / 取舍理由;用户问了才展开

---

## Handoff · 链条衔接

遵循 pack 接口契约(`shared/handoff-contract.md`)。

- **consumes**:`career-bullet-builder` 的 `final_bullets`(多条)+ `ats_keywords` + 目标 `target_role`/JD,并继承 `gaps` / `integrity_flags`。
- **produces**:整份可投递简历(本 skill 偏链条末端,主要交付给用户)。如继续接面试类 skill,内部交接(默认不展示):

```yaml
### ⇄ Handoff · resume-tailor → (interview-*, 未来)
- target_role: 运营管培生 @某公司(JD 链接: 用户提供/实时抓)
- resume_version: v-运营
- highlighted_exp: [P1 奶茶店兼职, E1 社会企业分析]
- gaps: [P1 高峰单量待补, E1 财报年数待补]      # 仍未确认,继续传递
- integrity_flags: [全部经历真实, 无编造链接, 信息合规]
```

**铁律**:为"对上岗位"只能做**取舍、排序、侧重、措辞**,**不得新增**用户没有的经历/数字;`gaps` 继续向下传,不得编造填充。

---

## Examples

完整示例见 `examples/demo_conversation.md`。默认输出长这样(结果优先、给整份、不堆术语):

> **目标:运营管培(你贴的 Boss 直聘 JD 已读取)**
>
> 【教育】…倒序、含起止时间
> 【实习/项目】… 最相关的放最前,每段 2-3 条成品 bullet
> 【技能】… 命中 JD 的关键词
>
> 💡 这份里"奶茶店兼职"对运营岗其实是加分项,我放到了"实践经历"靠前;你那段课程作业和岗位关系弱,我先收短了。
> 想出第二个岗位的版本 / 要英文版 / 想看我砍了啥?说一声。

---

## Boundary Rules

1. **红线·绝不编造**:不为对岗位而编造经历、数字、奖项、技能(见 `references/no-fabrication.md`,全 pack 共享)。
2. **绝不编造职位链接**:真实 JD 由用户提供或联网抓;**抓不到就明说"没取到,请给链接"**,绝不生成假 URL。具体职位链接会过期 → 运行时重抓,不写死。
3. **Tailor ≠ fake**:针对岗位只做取舍 / 排序 / 侧重 / 措辞;不得新增不存在的经历。
4. **分工**:单条打磨 → `career-bullet-builder`;能力萃取 → `career-experience-mapper`;找岗位 → `career-role-finder`;深扒 JD → `career-jd-analyzer`。
5. **个人信息合规**:照片、出生日期、性别、婚姻、政治面貌、身份证号不进简历(国内简历亦然,除非岗位明确要求)。
6. **默认中文成品 + 一页(应届)**:英文版后续统一补;社招/经历多可放宽长度。

---

## References

| 文件 | 内容 | 何时 Read |
|---|---|---|
| `references/resume-structure.md` | 模块顺序 + 应届/社招结构 + 长度 + ATS 格式规范 | Step 3 / 5 |
| `references/tailoring-by-jd.md` | 按 JD 取舍/排序/关键词对齐 + 多版本投递 | Step 4 |
| `references/job-platforms.md` | **真实招聘平台与经验资源**(牛客/Boss/实习僧/小红书…)+ 如何取真实 JD | Step 1 / 4 |
| `references/no-fabrication.md` | 共享红线:硬禁清单 + 不得编 URL + 自检 | Step 5(及全程)|

---

*Part of the **career-skills** pack · Built with **SkillAlchemy**. 默认产出中文简历(国内求职),英文版后续补;本 skill 提供投递定制方法,不构成对录用结果的承诺,最终内容真实性与投递链接真实性由用户负责。*
