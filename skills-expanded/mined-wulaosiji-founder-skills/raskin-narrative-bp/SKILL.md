---
name: raskin-narrative-bp
description: |
  Andy Raskin风格的叙事pitch框架。故事驱动的5节拍格式，专为现场演示和Demo Day设计。通过世界层面的设定而非产品层面的描述创造紧迫感和必然性。
  Use when: "Raskin pitch", "叙事BP", "故事驱动pitch", "Demo Day演示", "路演比赛", "现场投资人会议", "narrative pitch framework", "B2B销售deck", "Andy Raskin框架".
  最好的pitch不从你开始，从世界开始。投资人不投公司，他们投必然性。Cross-references: sequoia-structured-bp, yc-insight-driven-bp, pitch-deck-creator.
  Built by UniqueClub 🌐 https://uniqueclub.ai
license: MIT
---

# Raskin Narrative BP

> Andy Raskin风格的叙事pitch框架。故事驱动、紧迫感先导、戏剧化。最好的pitch不从你开始，从世界开始。

## When to Use

Use this skill when:
- 用户需要故事驱动的现场演示框架（Demo Day、路演比赛）
- 用户需要在投资人会议中现场present
- 用户需要B2B销售deck
- 用户需要通过世界层面的设定创造紧迫感和必然性
- 用户需要5个叙事节拍的pitch结构（而非幻灯片信息容器）

Do NOT use this skill if:
- 用户需要冷邮件发送的deck（非现场演示）→ use `sequoia-structured-bp` 或 `yc-insight-driven-bp` instead
- 用户需要严谨的数据驱动框架（A轮及以后、机构投资人）→ use `sequoia-structured-bp` instead
- 用户需要极简的洞察先导框架（pre-seed到seed）→ use `yc-insight-driven-bp` instead
- 用户需要可编辑的PPTX文件 → use `pitch-deck-creator` instead

Typical triggers:
- 「叙事pitch」「故事驱动BP」「Demo Day演示」「路演比赛框架」「现场路演」
- "Andy Raskin pitch", "narrative deck", "story-driven pitch", "Demo Day presentation"

## Workflow

本框架描述"如何使用Raskin叙事BP框架"的步骤：

本工作流遵循六步推进法，共6个步骤：
1. **探查 (Probe)**：动手前先完整读取全部输入，确认目标和约束。
2. **约束 (Constrain)**：验证输入完整性，设定边界和不可降级的交付标准，受阻时换通道。
3. **证据 (Evidence)**：每个数字必须来自输入、具体信源或可复现计算，收集支撑数据。
4. **执行 (Execute)**：调用脚本/API/生成内容，先给影响与结论，再给行动和必要证据。
5. **验证 (Verify)**：用"可能失败"的动作验证——不同于生成路径的方式回读输出。
6. **交付 (Deliver)**：返回结果，清理临时文件。

### Step 1: 探查 (Probe)
完整读取用户的项目信息，确认演示场景（现场Demo Day/Zoom会议/B2B销售）、行业、目标受众和核心叙事。理解项目的世界层面转变。

### Step 2: 约束 (Constrain)
设定框架使用边界：
- 输出为5个叙事节拍，不是幻灯片信息容器
- 语气：戏剧化、预言式、紧迫
- 前30秒不提及公司——从世界的转变开始
- 描述能力（capabilities）而非功能（features）
- 不取代现有巨头——让他们更高效（消除恐惧）
- 受阻时换通道，不降级交付物

### Step 3: 证据 (Evidence)
收集支撑叙事的证据：
- Beat 1需要令人震惊的统计数据、令人心痛的客户轶事或令人恐惧的行业趋势
- Beat 2需要相邻领域的可比成功案例（证明模式），或监管/技术顺风
- Beat 3需要before/after对比，感觉像魔法
- Beat 4需要展示能力的traction指标和确认转变的客户引言
- Beat 5需要3个逻辑相邻市场，建立在同一核心能力之上
- 所有数据必须有来源或可辩护

### Step 4: 执行 (Execute)
按照下方「Framework Content」中的5个叙事节拍，逐节拍撰写pitch叙事。先给影响与结论，再给行动和必要证据。每个节拍遵循：Goal → Rule/Technique → Good/Bad Example → Check 的结构。同时准备交付技巧（Pacing、Body Language、Voice）。

### Step 5: 验证 (Verify)
用Self-Review Checklist逐项验证——不同于生成路径的方式回读输出：
- 前30秒是否零提及公司？
- 问题是否创造情感反应（震惊、恐惧、紧迫）？
- 是否命名了可比成功来证明模式？
- 是否描述能力而非功能？
- traction指标是否关于转变而非增长？
- 愿景是否展示3个逻辑相邻市场？
- ask是否感觉像邀请？
- 如果现场演示：是否准备了60秒demo？

### Step 6: 交付 (Deliver)
返回完整的5节拍pitch叙事（Markdown格式），包含每个节拍的目标、技巧、示例和检查清单，以及交付技巧（Pacing、Body Language、Voice）。如非现场演示，提供适配为deck的版本（每个节拍1页，极简文字）。清理临时文件。如需生成可编辑PPTX，使用 `pitch-deck-creator`。

## Output

输出为Markdown格式的完整5节拍pitch叙事，包含：
- 5个叙事节拍，每个包含：Goal、Rule/Technique、Good/Bad Example、Check清单
- The Ask（独立于叙事，在故事之后）
- Delivery Tips（Pacing、Body Language、Voice）
- Adapting to a Deck（如非现场演示，每个节拍1页极简文字）
- Self-Review Checklist
- Anti-Patterns to Avoid（5种常见反模式）
- When to Use This Framework（场景推荐表）
- Raskin's Greatest Hits（3个学习案例）
- 所有示例基于ChainLedger作为统一案例

## Framework Content

### Meta

- **Style**: Story-driven, urgency-led, theatrical
- **Best For**: Pitch competitions; Demo Day; investor meetings where you present live; B2B sales decks
- **Source**: Andy Raskin (Silicon Valley's top pitch coach)
- **Output Length**: 5 narrative beats, not slides
- **Tone**: Dramatic, prophetic, urgent

### Core Philosophy

The best pitch doesn't start with you. It starts with the world.

> "The greatest sales deck I've ever seen didn't mention the company's product until slide 14." — Andy Raskin

Investors don't invest in companies. They invest in **inevitability** — the feeling that this future is already happening and they'd be foolish to miss it.

---

### The 5 Narrative Beats

Unlike Sequoia's 12 slides or YC's insight-first memo, Raskin's framework is **5 narrative beats**. Each beat is a story moment, not an information container.

#### Beat 1: Name a Big, Changeable Problem (The Setup)

**Goal**: Create tension. The investor must feel that *something is wrong with the world*.

**Rule**: Never start with your company. Start with a shift in the world that creates pain.

**Techniques**:
- **The statistic that stuns**: A number so large it demands attention.
- **The anecdote that hurts**: A real customer story that makes the investor wince.
- **The trend that terrifies**: A shift that threatens an entire industry.

**Good Example** (Statistic):
> "$18 billion. That's how much global enterprises lost last year to compliance fines alone. Not fraud. Not cyber attacks. Just paperwork that was filed incorrectly. And that number has doubled in the last 3 years."

**Good Example** (Anecdote):
> "Last month, a mid-size manufacturer in Shenzhen lost a $2 million order. Not because their product was bad. Not because their price was high. Because their compliance paperwork took 11 days, and the buyer went with a competitor who could do it in 3. Eleven days. For paperwork."

**Good Example** (Trend):
> "In 2019, 73% of CFOs said relationship banking was their top priority. Today, 89% say cash flow visibility is. That's not a preference shift. That's a survival shift. And most banks haven't noticed."

**Check**:
- [ ] The first 30 seconds contain no mention of your company
- [ ] The investor feels an emotion (shock, fear, urgency)
- [ ] The problem is big enough to justify a billion-dollar company

---

#### Beat 2: Show That the Problem Will Inevitably Be Solved (The Promise)

**Goal**: Create hope. Show that *someone* is going to solve this, and soon.

**Technique**: Point to a company in an adjacent space that has already won by solving a similar problem. This proves the pattern.

**Good Example**:
> "Stripe didn't just build better payment infrastructure. They made developers the heroes of payments. The result? $95 billion company. Compliance is the next infrastructure layer that desperately needs a Stripe. The only question is: who builds it?"

**Alternative Technique**: Show regulatory or technological tailwinds that make the solution inevitable.

**Good Example**:
> "PSD2 in Europe. Open banking APIs in the UK. Regulatory sandboxes in Singapore. Governments worldwide are *mandating* data sharing between financial institutions. The compliance walls are coming down. Someone is going to build the router that connects them."

**Check**:
- [ ] You've named a comparable success (proves the pattern)
- [ ] The investor thinks "of course someone will solve this"
- [ ] The inevitable solution is a platform, not a feature

---

#### Beat 3: Introduce Your Product as the Inevitable Solution (The Reveal)

**Goal**: Make your product feel like the *only* logical answer.

**Technique**: Don't describe features. Describe **capabilities** — what your product makes possible that was impossible before.

**Good Example**:
> "ChainLedger is the compliance settlement network. Instead of 3 banks independently verifying the same KYC data, we verify once and share the attestation across the network. What used to take 7 days now takes 4 hours. What used to cost $2,500 now costs $200. And here's the key: we're not replacing banks. We're making them 10x more efficient."

**Bad Example**:
> "ChainLedger is a SaaS platform with AI-powered compliance automation, real-time sanction screening, and automated KYC/KYB workflows."

**The Difference**:
- Capabilities: "What becomes possible"
- Features: "What we built"

**Check**:
- [ ] You describe capabilities, not features
- [ ] There's a before/after that feels magical
- [ ] You're not displacing incumbents — you're making them better (removes fear)

---

#### Beat 4: Provide Proof (The Evidence)

**Goal**: Make the inevitable feel real.

**Structure**:
1. **Traction that demonstrates the capability**
2. **Customer story that validates the transformation**
3. **Demo** (if presenting live)

**Good Example** (Traction + Story):
> "In 6 months, 120 enterprise customers. $50k MRR. 12% MoM growth. But here's the number that matters: our customers' compliance costs dropped 90%, and their settlement times went from 7 days to 4 hours. One customer told us: 'We didn't even know this was possible. We thought 7 days was just the cost of doing business internationally.'"

**The Demo Rule**:
If you're presenting live, show the product. Not a screenshot — the actual product. Walk through one workflow. Make the investor see the magic.

**Check**:
- [ ] The traction metric demonstrates the capability (not just growth)
- [ ] The customer quote confirms transformation (not satisfaction)
- [ ] If live: you demo, not describe

---

#### Beat 5: Reveal the Vision (The Close)

**Goal**: Expand from product to platform. Show this is bigger than it looks.

**Technique**: Take the core capability and show how it unlocks 3 adjacent markets.

**Good Example**:
> "Today, we're the compliance layer for cross-border trade. But compliance data is also credit data. Once we know a company's trade history, compliance record, and settlement behavior, we can offer trade credit at 1/10th the cost of traditional letters of credit. Then trade insurance. Then supply chain finance. The compliance network becomes the trade network."

**The Formula**:
```
Today: [what you do now]
Next: [adjacent market 1, unlocked by your data/capability]
Then: [adjacent market 2]
Eventually: [the platform vision]
```

**Check**:
- [ ] The vision is a logical extension, not a pivot
- [ ] Each adjacent market builds on the same core capability
- [ ] The final vision is a platform, not a product

---

### The Ask (Separate from the Narrative)

Raskin's framework doesn't include the ask in the narrative. The ask comes *after* the story, when the investor is already emotional.

**Good Example**:
> "We're raising $1.1M to build the compliance layer for global trade. The walls are coming down. We have the team, the traction, and the timing. The only question is whether you're in."

**Check**:
- [ ] The ask feels like an invitation, not a request
- [ ] The investor has already decided "yes" before you ask

---

### Delivery Tips (Critical)

This framework fails if read silently. It's designed for **live presentation**.

#### Pacing
- Beat 1 (Problem): Slow. Let the pain sink in.
- Beat 2 (Promise): Building. Create anticipation.
- Beat 3 (Reveal): Pause. Let the product land.
- Beat 4 (Evidence): Confident. Show the proof.
- Beat 5 (Vision): Expansive. Paint the future.

#### Body Language
- Beat 1: Still. Let the statistic/anecdote do the work.
- Beat 2: Moving. Walk to show inevitability.
- Beat 3: Center stage. This is the moment.
- Beat 4: Open. Show the evidence with open palms.
- Beat 5: Expansive. Arms wide for the vision.

#### Voice
- Beat 1: Lower, slower. Create gravity.
- Beat 2: Rising. Build tension.
- Beat 3: Clear, strong. The reveal.
- Beat 4: Conversational. "Let me show you..."
- Beat 5: Dreamy, then sharp. Vision, then ask.

---

### Adapting to a Deck (If Not Presenting Live)

If you must send a deck (not present live), adapt each beat to 1 slide with minimal text:

| Beat | Slide Title | Max Words |
|------|-------------|-----------|
| 1 | "$18B Lost to Paperwork" | 15 |
| 2 | "This Is the Next Stripe" | 15 |
| 3 | "4 Hours Instead of 7 Days" | 20 |
| 4 | "120 Customers, 90% Cost Reduction" | 20 |
| 5 | "From Compliance to Trade Network" | 15 |

**Rule**: If the investor can understand the deck without you, you've written too much. The deck is a prop, not the pitch.

---

### Self-Review Checklist

- [ ] Does the first 30 seconds contain zero mention of my company?
- [ ] Does the problem create an emotional reaction (shock, fear, urgency)?
- [ ] Have I named a comparable success to prove the pattern?
- [ ] Do I describe capabilities, not features?
- [ ] Is the traction metric about transformation, not growth?
- [ ] Does the vision show 3 logical adjacent markets?
- [ ] Does the ask feel like an invitation?
- [ ] If presenting live: do I have a 60-second demo ready?

### Anti-Patterns to Avoid

1. **Starting with "Hi, I'm X and this is Y"**: The investor doesn't care who you are yet.
2. **The Feature Dump**: "We have AI, blockchain, and machine learning." Capabilities, not features.
3. **The Modest Vision**: "We want to be the best compliance tool." Be the platform, not the tool.
4. **The Generic Traction**: "We're growing fast." Transformation metrics only.
5. **The Apologetic Ask**: "We were wondering if maybe you might consider..." Invitation, not apology.

### When to Use This Framework

| Scenario | Recommended? | Notes |
|----------|-------------|-------|
| Live pitch / Demo Day | **Strong yes** | This framework was built for live performance |
| Zoom call with partner | **Yes** | Adapt pacing for video |
| Cold email deck | **No** | Use Sequoia or YC format instead |
| B2B sales deck | **Yes** | Replace "investor" with "prospect" |
| Accelerator application | **Partial** | Combine with YC insight format |

### Raskin's Greatest Hits — Examples to Study

1. **Zuora's subscription economy pitch**: Started with "The world is shifting from products to subscriptions" — not "Zuora is a billing platform."
2. **Gainsight's customer success pitch**: Started with "Your customers are leaving and you don't know why" — not "Gainsight is a customer success platform."
3. **ChainLedger (example above)**: Started with "$18B lost to paperwork" — not "We automate compliance."

The pattern: always start with the shift in the world, never with the company.

## Guardrails

**Anti-patterns**
- NEVER 以"你好，我是X，这是Y"开始——投资人还不在乎你是谁
- Do NOT 功能堆砌——"我们有AI、区块链和机器学习"。说能力，不说功能
- NEVER 愿景 modest——"我们想成为最好的合规工具"。要成为平台，不是工具
- Do NOT 通用traction——"我们增长很快"。只用转变指标
- NEVER 道歉式ask——"我们在想您是否可能考虑..."。邀请，不是道歉
- Do NOT 在前30秒提及公司——从世界的转变开始
- NEVER 编造数据——每个统计、轶事和趋势必须有来源或可辩护

**Constraints**
- 输出为5个叙事节拍，不是幻灯片信息容器
- 语气：戏剧化、预言式、紧迫
- 前30秒不提及公司
- 描述能力（capabilities）而非功能（features）
- 不取代现有巨头——让他们更高效（消除恐惧）
- traction指标关于转变而非增长
- 愿景展示3个逻辑相邻市场
- ask感觉像邀请而非请求
- 本框架为现场演示设计，静默阅读会失败

## Related Skills

- **sequoia-structured-bp** — 红杉风格的严谨数据驱动框架，适合A轮及以后、机构投资人、冷邮件deck
- **yc-insight-driven-bp** — YC风格的极简洞察先导框架，适合pre-seed到seed、加速器申请
- **pitch-deck-creator** — 叙事内容完成后，从结构化JSON生成可编辑的10页PPTX文件

## About UniqueClub

Part of the UniqueClub toolkit.
🌐 https://uniqueclub.ai
