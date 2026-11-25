---
name: sequoia-structured-bp
description: |
  红杉资本风格的结构化商业计划书/pitch deck框架。10-12页数据驱动格式，包含逐页写作指南、示例和检查清单。最适合A轮及以后、机构投资人、尽调密集的融资轮次。
  Use when: "红杉BP", "Sequoia pitch deck", "结构化BP", "数据驱动BP", "A轮融资 deck", "institutional investor deck", "投资人级BP结构", "sequoia framework", "严谨BP框架".
  投资人只有3分钟，每页必须要么降低风险要么提升上行空间，没有装饰。Cross-references: yc-insight-driven-bp, raskin-narrative-bp, pitch-deck-creator.
  Built by UniqueClub 🌐 https://uniqueclub.ai
license: MIT
---

# Sequoia Structured BP

> 红杉资本风格的结构化BP框架。数据驱动、投资人级、模块化。投资人只有3分钟，每页必须要么降低风险要么提升上行空间。

## When to Use

Use this skill when:
- 用户需要严谨的、投资人级的BP结构
- 用户正在融A轮及以后，面对机构投资人
- 用户需要数据驱动的pitch deck框架（10-12页）
- 用户需要逐页写作指南、示例和检查清单
- 用户的融资轮次尽调密集，需要证据充分的deck

Do NOT use this skill if:
- 用户需要极简的、以洞察为先导的框架（pre-seed到seed）→ use `yc-insight-driven-bp` instead
- 用户需要故事驱动的现场演示框架（Demo Day/路演比赛）→ use `raskin-narrative-bp` instead
- 用户需要可编辑的PPTX文件 → use `pitch-deck-creator` instead
- 用户需要中文融资BP大纲 → use `fundraising-bp-planner` instead

Typical triggers:
- 「红杉风格BP」「结构化商业计划书」「A轮融资deck」「数据驱动pitch deck」
- "Sequoia pitch deck", "institutional investor deck", "data-driven BP framework"

## Workflow

本框架描述"如何使用红杉结构化BP框架"的步骤：

本工作流遵循六步推进法，共6个步骤：
1. **探查 (Probe)**：动手前先完整读取全部输入，确认目标和约束。
2. **约束 (Constrain)**：验证输入完整性，设定边界和不可降级的交付标准，受阻时换通道。
3. **证据 (Evidence)**：每个数字必须来自输入、具体信源或可复现计算，收集支撑数据。
4. **执行 (Execute)**：调用脚本/API/生成内容，先给影响与结论，再给行动和必要证据。
5. **验证 (Verify)**：用"可能失败"的动作验证——不同于生成路径的方式回读输出。
6. **交付 (Deliver)**：返回结果，清理临时文件。

### Step 1: 探查 (Probe)
完整读取用户的项目信息，确认融资阶段（A轮及以后为佳）、行业、关键数据和目标投资人。理解项目的核心价值主张和证据基础。

### Step 2: 约束 (Constrain)
设定框架使用边界：
- 输出长度10-12页，不超过15页
- 语气：自信、基于证据、不炒作
- 每页必须要么降低风险要么提升上行空间，没有装饰
- 所有数字必须有来源或可辩护
- 不使用流行词（disrupt, synergy, AI-powered等）
- 受阻时换通道，不降级交付物

### Step 3: 证据 (Evidence)
收集支撑每页内容的证据：
- 市场规模数据需来自可信来源（非自行计算的TAM）
- traction数据需有趋势（增长，而非静态数字）
- 团队经验需与业务直接相关
- 财务预测需自下而上（"10个销售×5笔/季度×$50k ACV"）而非自上而下（"1%市场份额"）
- 竞争分析需承认真实竞品，不声称"没有竞争"

### Step 4: 执行 (Execute)
按照下方「Framework Content」中的逐页指南，逐页撰写BP内容。先给影响与结论，再给行动和必要证据。每页遵循：Goal → Structure/Formula → Good/Bad Example → Check 的结构。

### Step 5: 验证 (Verify)
用Self-Review Checklist逐项验证——不同于生成路径的方式回读输出：
- 能否在3分钟内读完整个deck？
- 每个数字是否有来源或可辩护？
- 是否用市场顺风解释了"why now"？
- 团队页是否关于相关经验而非学历？
- traction页是否展示趋势而非快照？
- ask是否具体且有可衡量的里程碑？
- 是否零流行词（disrupt, synergy, AI-powered）？
- 妈妈能否理解问题和方案？

### Step 6: 交付 (Deliver)
返回完整的10-12页BP内容（Markdown格式，逐页指南），包含每页的目标、结构、示例和检查清单。清理临时文件。如需生成可编辑PPTX，使用 `pitch-deck-creator`。

## Output

输出为Markdown格式的完整BP逐页指南，包含：
- 10-12页幻灯片，每页包含：Goal、Structure/Formula、Good/Bad Example、Check清单
- Self-Review Checklist（发送前逐项检查）
- Anti-Patterns to Avoid（5种常见反模式）
- 所有示例基于ChainLedger（跨境B2B支付合规结算网络）作为统一案例

## Framework Content

### Meta

- **Style**: Data-driven, investor-grade, modular
- **Best For**: Series A and beyond; institutional investors; due-diligence-heavy rounds
- **Source**: Sequoia Capital pitch framework
- **Output Length**: 10–12 slides
- **Tone**: Confident, evidence-based, no hype

### Core Philosophy

The investor has 3 minutes. Every slide must either (a) reduce risk or (b) increase upside. No decoration.

> "If you can't explain it with data, you don't understand it well enough." — adapted from Einstein

---

### Slide 1: Company Purpose (1 sentence)

**Goal**: Make the investor "get it" in 5 seconds.

**Formula**:
```
[Company] is a [category] that helps [target customer] [solve problem] by [unique mechanism].
```

**Good Example**:
> "ChainLedger is a compliance settlement network that helps cross-border B2B traders reduce settlement time from 7 days to 4 hours through real-time sanction screening."

**Bad Example**:
> "ChainLedger is a blockchain-based fintech platform leveraging AI and machine learning to disrupt the payments industry."

**Check**:
- [ ] Can a non-expert understand it?
- [ ] No buzzwords (AI, blockchain, disruptive, synergy)
- [ ] Contains: who, what problem, how

---

### Slide 2: Problem

**Goal**: Prove the problem is real, urgent, and valuable.

**Structure**:
1. **Scene-setting** (1 sentence): What world do your customers live in?
2. **Pain quantification**: Use a number. $18B/yr in fines. 3–5 intermediaries. 4–7 day delay.
3. **Who feels it most**: Define your ICP (Ideal Customer Profile) narrowly.

**Good Example**:
> "Cross-border B2B payments involve 3–5 intermediaries, 4–7 day settlement, and compliance gaps that cost enterprises $18B/yr in fines globally. The pain is most acute for mid-market manufacturers importing from Asia — they have 2-person finance teams and zero compliance expertise."

**Bad Example**:
> "Cross-border payments are broken. They're slow, expensive, and non-compliant."

**Check**:
- [ ] The problem is quantified with a specific number
- [ ] The ICP is defined narrowly (not "all businesses")
- [ ] The investor can feel the pain (emotional hook)

---

### Slide 3: Solution

**Goal**: Show your solution is inevitable once the problem is understood.

**Structure**:
1. **The insight** (1 sentence): What did you see that others missed?
2. **How it works** (2–3 sentences): Mechanism, not architecture.
3. **Before/After**: One sentence contrasting old way vs. your way.

**Good Example**:
> "We built an end-to-end compliance settlement network using real-time sanction screening, automated KYC/KYB, and instant settlement rails. Instead of routing through 3 correspondent banks over 7 days, we settle directly in 4 hours with full audit trails."

**Bad Example**:
> "Our platform uses a microservices architecture with PostgreSQL, Redis, and Kubernetes on AWS."

**Check**:
- [ ] Describes outcome, not technology stack
- [ ] Contains a before/after contrast
- [ ] Can be explained to a 10-year-old

---

### Slide 4: Why Now?

**Goal**: Convince the investor the timing is non-negotiable.

**Structure**:
List 2–3 market tailwinds that make this business possible *now* but not 5 years ago.

**Examples**:
- Regulatory: "PSD2 + open banking APIs made real-time settlement legally possible in EU"
- Technology: "Cloud compliance tools dropped KYC cost from $50 to $5 per check"
- Behavior: "Post-COVID, 73% of CFOs now prioritize cash flow visibility over relationship banking"

**Check**:
- [ ] At least one tailwind is verifiable (cite source if possible)
- [ ] The tailwinds are accelerating, not static
- [ ] Without these tailwinds, the business doesn't work

---

### Slide 5: Market Size

**Goal**: Show the prize is worth the investor's time.

**Structure**:
```
TAM: $X billion (top-down, industry report)
SAM: $Y billion (bottom-up, reachable in 5–7 years)
SOM: $Z million (what you can capture in 2–3 years)
```

**Good Example**:
> "TAM: $180B cross-border B2B payments
> SAM: $12B mid-market Asia-Europe trade corridor
> SOM: $840M Chinese manufacturers with <500 employees"

**Bad Example**:
> "The fintech market is $300T. If we capture 0.01%..."

**Check**:
- [ ] TAM is from a credible source (not self-calculated)
- [ ] SAM is defensible (geography + segment + use case)
- [ ] SOM is achievable (implies realistic market share)

---

### Slide 6: Competition

**Goal**: Show you understand the landscape and have a differentiated position.

**Structure**:
1. **2x2 matrix**: X-axis = speed, Y-axis = compliance depth (pick axes relevant to your market)
2. **Where you sit**: Explain *why* you're in the top-right.
3. **Moat preview**: Hint at what's hard to replicate (don't fully reveal yet).

**Good Example**:
> "Legacy banks (bottom-left): 7 days, high compliance but manual. Fintechs (top-left): 1 day, low compliance. We're the only player in top-right: 4 hours + full automated compliance."

**Check**:
- [ ] You acknowledge real competitors (not "we have no competition")
- [ ] The axes are meaningful to customers, not just to you
- [ ] You explain why others can't easily move to your position

---

### Slide 7: Product

**Goal**: Show the product is real and differentiated.

**Structure**:
1. **Screenshot/demo**: One image or 30-sec Loom.
2. **Key differentiator**: One feature no one else has.
3. **Integration**: How customers adopt (API, dashboard, Slack bot, etc.).

**Check**:
- [ ] There's visual evidence (screenshot, not wireframe)
- [ ] The differentiator is defensible (not "better UI")
- [ ] Adoption path is low-friction

---

### Slide 8: Business Model

**Goal**: Show how you make money and that the economics work.

**Structure**:
1. **Pricing**: Simple, transparent. One primary model.
2. **Unit economics**: CAC, LTV, gross margin if available.
3. **Expansion revenue**: How customers grow over time.

**Good Example**:
> "SaaS: 0.15% per transaction + $2k/mo platform fee. Enterprise: custom pricing.
> Unit economics: CAC $4,200 (inside sales), LTV $48,000, gross margin 82%."

**Check**:
- [ ] Pricing is simple enough to explain in one breath
- [ ] Unit economics are directionally correct (don't need perfection)
- [ ] There's a path to expansion revenue

---

### Slide 9: Traction

**Goal**: Prove momentum. This is the most important slide for early-stage.

**Structure**:
1. **The one metric that matters**: Pick the metric that best shows product-market fit.
2. **Trend line**: Show growth over time (6–12 months).
3. **Logo wall**: 3–5 customer logos (with permission).

**Metric Selection Guide**:
| Stage | Best Metric |
|-------|------------|
| Pre-launch | Waitlist size + engagement rate |
| Post-launch | MAU/DAU + retention curve |
| Revenue | MRR + MoM growth rate |
| Scale | Net revenue retention + expansion rate |

**Good Example**:
> "120+ enterprise customers, $50k MRR, 12% MoM growth last 6 months. Core vertical renewal 90%+."

**Check**:
- [ ] The metric is a leading indicator (not vanity)
- [ ] There's a trend (growth, not a static number)
- [ ] The metric is specific ("120 customers" not "rapidly growing")

---

### Slide 10: Team

**Goal**: Answer "Why you?" — why this team will win.

**Structure**:
1. **Founders**: Relevant experience, not credentials.
2. **Key hires**: Who you've recruited that validates the vision.
3. **Advisors**: 1–2 credible names if available.

**Good Example**:
> "CEO — ex-Ant Group payments lead (8 yrs, built $2B settlement product). CTO — ex-infrastructure architect at Stripe. COO — ex-HSBC compliance director."

**Bad Example**:
> "Team has degrees from MIT, Stanford, and Harvard."

**Check**:
- [ ] Each team member's experience directly maps to the business
- [ ] Credentials are secondary to relevant achievements
- [ ] There's no "MBA from HBS" without context

---

### Slide 11: Financials

**Goal**: Show you understand the financial trajectory.

**Structure**:
1. **Historical** (if any): Revenue, burn, runway.
2. **Projections**: 3-year forecast. Conservative, base, optimistic.
3. **Use of funds**: Where the new money goes.

**Rule**: Never show a hockey stick without explaining *what changes* to make it happen.

**Check**:
- [ ] Projections are bottom-up ("10 sales reps x 5 deals/quarter x $50k ACV") not top-down ("1% market share")
- [ ] Burn rate and runway are disclosed
- [ ] Use of funds is specific ("hire 3 engineers" not "growth")

---

### Slide 12: The Ask

**Goal**: Make it easy to say yes.

**Structure**:
```
We're raising $X on a $Y pre-money valuation.
Use of funds: [specific allocation]
Milestones with this round: [3 measurable goals]
```

**Good Example**:
> "Raising $1.1M on $8.3M pre-money.
> Use: 40% engineering (compliance automation), 30% sales (2 senior AEs), 30% operations.
> Milestones: $200k MRR, 3 enterprise pilots, EU regulatory approval."

**Check**:
- [ ] The amount is specific (not "$1–2M")
- [ ] Valuation is stated (or "open to discussion")
- [ ] Milestones are measurable and time-bound

---

### Self-Review Checklist

Before sending, run through this:

- [ ] Can I read the entire deck in 3 minutes?
- [ ] Is every number sourced or defensible?
- [ ] Do I explain "why now" with market tailwinds?
- [ ] Is the team slide about relevant experience, not credentials?
- [ ] Does the traction slide show a trend, not a snapshot?
- [ ] Is the ask specific with measurable milestones?
- [ ] Are there zero buzzwords (disrupt, synergy, AI-powered)?
- [ ] Would my mom understand the problem and solution?

### Anti-Patterns to Avoid

1. **The "Everything Deck"**: >15 slides. Cut to 10.
2. **The "TAM Fantasy"**: Top-down market size without SAM/SOM.
3. **The "No Competition" Claim**: Every market has competition. Acknowledge it.
4. **The "Team of Geniuses"**: Credentials without relevant experience.
5. **The "Hockey Stick"**: Exponential growth projections without mechanism.

## Guardrails

**Anti-patterns**
- NEVER 超过15页——精简到10-12页
- Do NOT 使用自上而下的市场规模而没有SAM/SOM拆解
- NEVER 声称"没有竞争"——每个市场都有竞争，承认它
- Do NOT 用学历代替相关经验——团队页关于经验而非证书
- NEVER 展示没有机制解释的曲棍球棒式增长预测
- Do NOT 使用流行词（disrupt, synergy, AI-powered, blockchain等）
- NEVER 编造数据——每个数字必须有来源或可辩护

**Constraints**
- 输出长度10-12页，不超过15页
- 语气：自信、基于证据、不炒作
- 每页必须要么降低风险要么提升上行空间
- TAM必须来自可信来源（非自行计算）
- 财务预测必须自下而上而非自上而下
- traction必须展示趋势而非静态快照
- ask必须具体且有可衡量的里程碑

## Related Skills

- **yc-insight-driven-bp** — YC风格的极简洞察先导框架，适合pre-seed到seed、加速器和天使投资人
- **raskin-narrative-bp** — Andy Raskin风格的故事驱动叙事框架，适合现场演示、Demo Day和路演比赛
- **pitch-deck-creator** — 框架内容完成后，从结构化JSON生成可编辑的10页PPTX文件

## About UniqueClub

Part of the UniqueClub toolkit.
🌐 https://uniqueclub.ai
