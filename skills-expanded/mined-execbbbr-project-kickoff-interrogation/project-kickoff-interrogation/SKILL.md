---
name: project-kickoff-interrogation
description: Use when a user is starting a new project (0→1) or saying things like "我想做一个 X" / "I want to build" / "let's make a tool that". Conducts a 9-step interrogation grounded in the 钉钉 ONE post-mortem (《置身钉内》, 75k 字, 滕雅辛 2026) to lock down 发心/用户/场景/价值/竞争/双边博弈/MVP/倒排陷阱/止损线 BEFORE writing code or plans. Each question comes with intro + multiple-choice options (not blank-slate prompts), so the user picks rather than free-writes. Produces a frozen baseline.md the user can use to slap themselves later when the project drifts.
version: 1.0.0
author: Hermes Agent (inspired by 滕雅辛《置身钉内》, 2026)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [product, kickoff, interrogation, post-mortem, planning, dingding-one, anti-vibe]
    related_skills: [writing-plans, plan, spike, ideation]
---

# Project Kickoff Interrogation (立项拷问)

## Overview

大部分项目不是死在执行，是死在「让我们开始做吧」那一刻——没有人逼着回答本来会杀死这个项目的问题。

这个 skill 是 *ideation*（发散）和 *writing-plans*（执行）之间缺失的中间层。它在项目最脆弱的瞬间（用户兴奋、答案还很软）逼一遍 9 个问题，把答案冻结成一份 baseline 文档，让以后的漂移可见、可问责。

9 个拷问 **不是凭空设计的**——每一条都对应滕雅辛《置身钉内》（钉钉 ONE 项目 75k 字复盘，2026 年 6 月）里的一个具体失败。完整映射见 `references/one-case-study.md`。

## When to Use

**Use when:**
- 用户说"我想做一个 X" / "我有个 idea" / "I want to build" / "let's make"
- 项目位于 brainstorm 已完成 → 实施计划未开始 之间
- 用户很兴奋，回答听起来"都行"、"看情况"、"应该是"
- 团队即将投入人力/预算到一条新产品线
- 重新评估一个已经在漂移的项目

**Don't use for:**
- 纯技术 spike（→ `spike`）
- 完全没方向的发散（→ `ideation`）
- 方向已经锁定，要写实施计划（→ `writing-plans` / `plan`）
- 用户明说"side project 别 overthink"

**强触发短语：** "我有个想法" / "我想做" / "I want to build" / "let's build" / "we should make a tool that" / "如果有一个 X 就好了".

## The Anti-Pattern This Skill Targets

> 「ONE 一开始就不是一个发心单纯的产品。它既想替用户减负，也想替钉钉换代；既想证明 AI 能进入工作流，也想证明钉钉还能站在下一代办公入口上。这里面有理想，也有指标；有用户价值，也有组织意志。」
> —— 《置身钉内》第一卷

跳过这个 skill，你会复刻 ONE：300 人团队、首发 DAU 300 万、半年内被全网抵制、产品收缩。**根因不是技术，是没人在 day 0 强迫创始人回答"这个产品不是给谁用的"。**

## How to Run This Interrogation

**核心规则：**

1. **一次只问一个问题** — 不要 dump 所有 9 个。等用户答完一个再下一个。
2. **每个问题先给 intro，再给 choices，再问** — 不要让用户从零开始写。
3. **不接受 "and / both / 都要 / 看情况"** — 选项是互斥的。如果用户含糊，追问"那个**最**重要？"。
4. **第 2 题选 A（单边）时，跳过第 6 题** — 单边产品没有双边博弈。
5. **第 7 / 8 题如果用户选 C 或 D**，必须显式说："这是 ONE 同款 red flag，你确认知道这个风险后继续吗？" 得到 Y 才继续。
6. **第 9 题必须落地具体数字、日期、人名** — "我们都会注意" = "没人会拉闸"。
7. **9 题做完一定写 baseline.md** — 不落档就白做。

---

## 拷问 1 — 发心 (Origin Intent)

**对应 ONE 失败：** 第一卷 — 同时挂 4 个发心 = "贪心是七罪之一"，后期所有决策被多目标撕扯。

**Intro to give the user:**
> 一个产品的「发心」是它最原始的出发点。原文给出 5 种典型。**好产品通常只有一个主发心**——其他可以是 side benefit，但不能并列。混发心的产品后期会被各种目标拉扯到崩。

**Choices (pick exactly ONE primary):**
- **A. 解决某个尚未被解决的具体问题** — 最纯，最容易诞生有历史价值的产品
- **B. 提升解决某个已解决问题的效率** — 常见且可行（要 10× 改善才有迁移动力）
- **C. 服务好某个具体人群** — 社区/身份驱动（vertical SaaS、某行业工具）
- **D. 推广某种理念** — 意识形态驱动（Linux、开源、去中心化）
- **E. 销售某种资源** — 分发驱动（手里有 token / 算力 / 库存要消化）

**Follow-up (mandatory):**
- 列出次发心（每个标 ✓ side-benefit 或 ⚠️ distraction）
- 如果主发心选 E 且没有 A/B/C 作为次发心 → 显式提醒："销售资源 + 没有用户问题 = 分发游戏，不是产品。确认继续？"

---

## 拷问 2 — 用户定位

**对应 ONE 失败：** 第二卷 — "带着一盒薛定谔的用户出发了"，老板 vs 员工诉求拒绝下场判断。

**Intro to give the user:**
> 目标用户是谁是一半的问题。另一半是**「不是」谁**——而这一半更重要。ONE 拒绝回答"不是谁"，于是想服务所有人，结果谁也没服务好。

**Choices (pick the SHAPE):**
- **A. 单边 (single-side):** 付费 = 使用 = 受益，同一个人（消费应用、indie dev tools、开发者自己付钱给自己用的工具）
- **B. 软双边 (aligned two-side):** 不同人但利益一致（Slack: IT 买，员工用，都想协作顺）
- **C. 硬双边 (opposing two-side):** 不同人、利益对立（ONE: 老板买想管控，员工用想喘息）—— **死结警告**
- **D. 多边平台 (3+ sides):** 双边市场、广告支撑（淘宝、抖音、Uber）

**Follow-up (mandatory, 全部必须答)：**
- 目标用户关键特征（一句话）：规模 / 行业 / 角色 / 习惯
- **明确不是谁**：写下 3 类不要的用户。如 "不是个人开发者" / "不是非技术人员" / "不是 enterprise 合规客户"
- 如果选了 C：**谁的诉求必须牺牲？** 写下原则（不是"具体看情况"）

---

## 拷问 3 — 场景定位

**对应 ONE 失败：** 第二卷三场景定位本来是 ONE 早期最优秀的部分（早晨排兵 / 开会后补课 / 下班前查漏，分钟级具体）。第三卷崩在卡片承载边界失控——审批/会议/文档/钉任务全部接入，从单场景智能助手变成"全模块消息聚合出口"，**等于在原有钉钉消息之外新增一层信息流**。

**Intro to give the user:**
> "高频日常工具"是模糊词。要回答的是**具体哪一秒钟，用户的什么动作或情绪，让他想到你**。

**Choices (frequency shape):**
- **A. 高频日常 (high-freq daily):** 每天 N 次，竞争秒级注意力（IM、邮箱、浏览器）
- **B. 事件触发 (event-triggered):** 特定信号出现时才用（alert tool、incident response、客服 ticket）
- **C. 周期任务 (periodic):** 每周/月/季度一次（review、planning、billing）
- **D. 项目周期 (project-based):** 一段时间集中用，结束就放下（IDE、design tool）

**Follow-up (mandatory):**
- 用模板写出具体场景："**用户在 ___ 之后/之前/期间，因为 ___ 痛苦/需要，想到我。**"
- ✓ 好答案示例（ONE 早期）："用户在开完 2 小时长会、再次打开钉钉发现几十个未读群时，需要快速赶上进度，想到我。"
- ✗ 坏答案示例："AI 办公助手，提升日常效率。"

---

## 拷问 4 — 价值定位

**对应 ONE 失败：** 第三/四卷 — 晨间看板/复盘/发现页都没量化基准。"新鲜感一周后快速衰减"——本来就没人在为这个问题付钱/花时间，省下来也没意义。

**Intro to give the user:**
> 原文："用户原本愿意花费多少钱/时间/其他资源，来达成这种价值？" 没有这个 baseline，你的"价值"就是 PPT 词汇。

**Choices for "用户现在怎么解决这个问题"：**
- **A. 手动忍着** — 那痛感真的够吗？
- **B. 用工具 X**（写出工具名 + 痛点）— 那就是和 X 竞争
- **C. 雇人解决**（写出成本）— 那你是替代人力
- **D. 根本不解决** — ⚠️ 红旗：可能根本没痛

**Follow-up (mandatory):**
- **痛感量化：** 用户每周花多少分钟 / 多少美元 / 多少情绪能量在这事上？给个数字。
- **改善倍数：** 你能省下多少？
  - **10× 改善** = painkiller，有迁移动力
  - **1.2-2× 改善** = vitamin，"有也行没也行"，留存会崩

---

## 拷问 5 — 竞争定位

**对应 ONE 失败：** 第二卷竞争定位 + 第八卷长期思考。原文用 Stack Overflow 月度提问量被 ChatGPT 一年腰斩举例：**过去的积累可能反过来成为被绕过的对象**。ONE 自身的护城河（"钉钉掌握组织关系"）没用对——拿去做管控算法而不是做"事找人"，护城河浪费了。

**Intro to give the user:**
> "差异化在哪？这个差异化是否可持续？" 第二问比第一问更重要。

**Choices (你的护城河本质上是哪一种)：**
- **A. 数据 / context** — 只有你有这数据（组织架构、历史日志、私有数据集）
- **B. 渠道 / 分发** — 只有你能在那个入口触达用户（装机量、系统入口）
- **C. 网络效应** — 用户越多产品越好（marketplace、social network）
- **D. 切换成本 / lock-in** — 数据/工作流锁定（CRM、ERP）
- **E. 品味 / 手艺** — 难以复制的执行力（罕见，通常是自欺）
- **F. 无明显护城河** — speed/timing play 🚨 时间窗口关闭就死

**Follow-up (mandatory):**
- **两年后还在吗？** 假设 LLM 进步 10×、竞品抄走 UI、用户习惯变了，你还剩什么？
- 如果两年后没了 → 你能做的是把短期窗口最大化（变现、被收购）还是放弃这个 idea？

---

## 拷问 6 — 双边博弈 (仅 #2 为 B/C/D 时执行)

**对应 ONE 失败：** 第四卷终极悖论 —— "To B 产品，付费的是老板，使用的是员工。老板要管控，员工要自由。两者需求 100% 互斥，没有折中解。"

**Intro to give the user:**
> 这是 #2 的展开。如果你的产品有多边用户，这里必须把"谁让步"写死。事到临头再决定 = ONE 同款。

**Follow-up (mandatory):**
- 列出每一边的核心诉求（每边一句话）
- 当两者直接冲突时（必然会冲突），**写下优先原则**（不是 case-by-case）
- **数据/能力暴露给一方时，另一方知道吗？** （ONE 同款问题：AI 帮员工梳理时也帮老板看到了员工所有漏洞）
- **付费方和决策方是同一人吗？** 否 → 这是 SaaS 双边死结，强烈建议读完 `references/one-case-study.md` 第四卷再继续

---

## 拷问 7 — MVP 边界

**对应 ONE 失败：** 第五卷 — "正常产品先做 10 分可用，验证后迭代到 80 分完美。ONE 直接一步到位：立项即对标终极形态。还没学会走路，直接强制冲刺百米决赛。"

**Intro to give the user:**
> MVP 不是 "最小但完整"，是 "最小且能验证一个具体假设"。砍到只能验证 #4 的价值假设为止。

**Choices (你计划的 MVP 范围)：**
- **A. 一个动作 (one action):** 单一闭环 — "用户能完成 ___ 这一件事" — ✓ 健康
- **B. 一个功能 (one feature):** 一个核心功能 + 必要 plumbing — 可以，但要确认这一个功能能独立产生价值
- **C. 三个核心功能 (3 features):** ⚠️ 警告 — 是否真的每个都必要？砍到 A/B 试试
- **D. 全场景全链路 (everything):** 🚨 ONE 死亡剧本 — STOP，必须显式 ack 风险

**Follow-up (mandatory):**
- 如果 MVP 只能保留**一个动作/界面/接口**，是什么？
- 这个最小版本能不能独立验证 #4 的价值假设？不能 → 再砍。

**🚨 If user picks C or D:** Stop and ask: "这是 ONE 同款 'MVP 直接做终极形态' 的 red flag。原文记载这条死亡剧本。你确认知道这个风险后继续吗？" 必须得到明确 Y 再走下一题。

---

## 拷问 8 — 倒排陷阱 (Deadline Trap)

**对应 ONE 失败：** 第五卷 — "8 月 25 日是固定对外官宣日，日期不可改、规格不可降、战略不能输。所有排期、所有需求、所有设计、所有开发、所有测试，全部为发布会让路。"

**Intro to give the user:**
> 不需要建议，只需要诚实回答：**是不是有一个外部固定 deadline 在催着这个产品？**

**Choices:**
- **A. 没有外部 deadline** ✓ 健康
- **B. 有 deadline 但可滑动** 还行，注意不要让"将就的 deadline"逐步变成"硬 deadline"
- **C. 有 hard deadline（发布会 / 合同 / 季度汇报 / 融资 demo）** 🚨 ONE 同款
- **D. 是 deadline 倒推出来的产品**（先有 deadline 再凑产品 idea）🚨🚨 ONE 同款，几乎必败

**Follow-up (mandatory if C/D):**
- 这个 deadline 是**真硬**还是**组织 perceived 硬**？能不能 push 1-2 个 sprint？
- 如果 deadline 不动，**MVP 范围（#7）能不能再砍？** 倒排时唯一可调整的是范围，不是质量。

**🚨 If user picks C or D:** Stop and ask: "这是 ONE 同款 'deadline 倒排一切' 的 red flag。你确认知道这个风险后继续吗？" 必须得到明确 Y 再走下一题。

---

## 拷问 9 — 止损线 (Stop-Loss Line)

**对应 ONE 失败：** 第五卷 — "内测出现隐患——压下；灰度出现用户抵触——无视；留存开始下跌——加码运营、加码推送、强行拉活；舆情开始爆发——公关压制、删帖控评。全程没有一次因为负面真实数据，修正顶层定位。" 第四卷数据："次日留存从 45% 暴跌至 18%；7 日留存跌破个位数；超 60% 用户打开三次以内永久关闭。"

**Intro to give the user:**
> 提前写下止损线，事后没有开脱空间。**不写下 = 一定不会拉。**

**Follow-up (mandatory — 必须落到数字、日期、人名)：**
- **主指标：** 是什么？(DAU / 留存 / 转化率 / NPS / 用户数 / revenue / ...)
- **阈值（必须写具体数字+日期）：** 上线 N 个月（N=2 / 3 / 6）后，如果 [指标] < [数值]，就 [stop / pivot / 缩编]。
- **次级触发：** 出现 [质性信号 — 例如 "用户主动卸载 > 1000" / "差评率 > 30%" / "团队半数离职"] 时，立即触发复盘。
- **拉闸人：** 写下**具体人名/角色**。

🚨 不接受："我们都会注意" / "团队一起拉" — 那就是没人会拉。必须有一个具体的负责人。

---

## Output: baseline.md

9 题全部答完后，按 `templates/baseline-template.md` 的结构写一份 baseline 文档。

**Save location (agent 自行判断当前环境)：**
- Hermes 环境：`~/.hermes/projects/<project-slug>/baseline.md`（目录不存在就创建）
- Claude Code 在 repo 内：`docs/baseline.md` 或项目根目录
- 通用：在当前 workdir 下创建 `<project-slug>-baseline.md`

**Format 强制要求：**
- 文件顶部必须有「**⚠️ 这是一份冻结基线 (Frozen Baseline)**」声明
- 包含日期
- 包含本 skill 的版本（`project-kickoff-interrogation v1.0.0`）便于追溯

写完之后向用户口头总结：
1. baseline.md 已存到 [path]
2. 高亮其中的 🚨 red flag 项（#7 C/D, #8 C/D 等）
3. 提醒下一步：用 `writing-plans` 写第一阶段实施计划，**只覆盖 #7 写下的 MVP 范围**，不要把 9 题答案当 backlog

## Common Pitfalls

1. **让用户"and / both" 蒙混过关。** Choices 是互斥的。用户说 "A 和 B 都重要" → 必须追问"那个**最**重要？" 直到给一个。

2. **跳过 #2 的"不是谁"。** "Everyone" / "所有人" 不是答案。**强制要求** 3 个明确的 "not for" 类别。

3. **#6 在 #2 = A 时也乱问。** 单边产品没有双边博弈，跳过 #6，不要硬问。

4. **#7 / #8 用户选 C/D 时不停下确认风险。** 这是 ONE 同款致命剧本。必须显式说 "这是 ONE red flag" 并得到明确 Y 再继续。

5. **#9 没人名 / 没数字 / 没日期。** "我们都会注意" 是 ONE 同款"全程没有一次纠偏"的起点。

6. **不存 baseline.md。** 整套拷问做完不落档 = 白做。一定要写文件并报告路径。

7. **照本宣科 ONE 案例。** ONE 是 to-B SaaS。如果用户做 to-C 消费产品 / 开发者工具 / 硬件，举例时要类比到对应领域，不要硬套钉钉场景。用户问"为什么"时再引用 `references/one-case-study.md` 对应卷。

8. **一次 dump 全部 9 题。** 用户会失去耐心或乱答。一次一题，等答完再下一题。

9. **第 2 题 follow-up "不是谁" 接受 2 个就放过。** 必须 3 个。ONE 失败的核心就是没有这一层。

## Verification Checklist (for the agent running this skill)

- [ ] 9 个拷问全部走完（#6 仅在 #2 = A 时跳过）
- [ ] 不接受"and / both / 都要"答案 — 用户互斥选择了一个
- [ ] #2 有明确的"不是谁"列表 (≥3 项)
- [ ] #4 有量化的痛感 baseline + 改善倍数
- [ ] #5 回答了"两年后还在吗"
- [ ] #7 picked A 或 B（如果 C/D 必须显式得到 🚨 ack）
- [ ] #8 picked A 或 B（如果 C/D 必须显式得到 🚨 ack）
- [ ] #9 有具体数字 + 日期 + 人名
- [ ] baseline.md 已落盘
- [ ] baseline.md 顶部有 "冻结基线" 声明
- [ ] 完成后给用户报告：路径 + red flag 高亮 + 下一步建议

## Cross-Agent Note (Hermes + Claude Code)

This skill is designed to run on **both Hermes and Claude Code**. It deliberately avoids tool-specific calls in the question protocol. Both agents should:

1. Read this SKILL.md
2. Conduct the interrogation **conversationally**（一次一题，不要 dump）
3. 引用 `references/one-case-study.md` when 用户问 "为什么要问这个？"
4. Use `templates/baseline-template.md` for output structure
5. Write the output file using whatever file API the agent has

**Placement for Claude Code:** put this skill at `.claude/skills/project-kickoff-interrogation/` for per-repo use, or `~/.claude/skills/` for user-global.

**Placement for Hermes:** already in `~/.hermes/skills/product-thinking/project-kickoff-interrogation/`.
