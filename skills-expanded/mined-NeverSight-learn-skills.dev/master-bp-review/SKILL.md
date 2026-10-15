---
name: master-bp-review
description: Use when the user wants feedback on a business plan, pitch deck, or other business document for investor-style or strategic review. Trigger for requests like "review my BP", "点评商业计划书", "review this pitch deck", "投资人视角分析这份 deck", "帮我看看这个商业计划书", or when the user shares a BP, deck, memo, or business document and asks for business or investor-style feedback. Do not use for raw startup ideas without a document or deck to review — if the user only has a concept/idea with nothing written down, use `startup-idea-evaluator` instead.
---

<!-- Ver 2026-07-19 05:30, by Claude Sonnet 5 (updated; originally by GPT-5) -->

# Master BP Review

This skill evaluates business plans (BPs), pitch decks, and other business documents by selecting the 5 most suitable master reviewers from a broader candidate pool. The goal is not to force every business through the same famous-person checklist, but to match the review lenses to the actual business: VC-scale startup, bootstrapped SaaS, small business, creative brand, creator tool, marketplace, local service, or China-specific product.

## Core Principles

### Context-Fit Before Authority

The first job is to understand the business, then select reviewers whose lenses expose the most important truths. A small creative business should not be judged only by monopoly and venture-scale growth. A B2B SaaS should not be judged only by brand storytelling.

### Independent Voices

Each selected master reviews independently. This is what makes the output valuable. The tension between perspectives is desirable: Jobs may love the product vision while Thiel finds no monopoly; Hormozi may like the offer while 张小龙 rejects the engagement mechanics.

### Selection Transparency

Before writing reviews, explain why the 5 masters were selected. The user should see the fit between the BP and the review panel.

## Master Selection Rules

After reading the input document, select exactly 5 masters from the candidate pool.

Selection should optimize for:

- **Business archetype**: B2B SaaS, consumer app, creative business, creator economy, marketplace, local service, enterprise, community, hardware/software, content brand, etc.
- **Stage**: idea, prototype, early users, revenue, growth, fundraising.
- **Main uncertainty**: demand, positioning, distribution, unit economics, product quality, offer strength, operational complexity, founder-market fit, defensibility.
- **Strategic tension**: choose reviewers who will disagree in useful ways instead of five people who all ask the same question.
- **Team context**: small team, bootstrap-first, China familiarity, global reach, low paid-ad reliance.

Required selection output:

| Master | Why selected | Primary lens | Key question this master will ask |
| --- | --- | --- | --- |

Do not select a master only because they are famous. If a master is not a good fit for this BP, leave them out.

## Master Candidate Pool

### 1. Steve Jobs

**Focus Areas:**
- Product perfection ("insanely great" standards)
- User experience (简洁、优雅、直觉)
- Design excellence
- Brand storytelling and positioning
- "Think Different" - challenging conventions
- Emotional connection with users

**Best For:**
- Consumer products, creative tools, hardware/software experiences, premium brands, products where taste and UX are central.

**Characteristic Voice:**
- Demanding, uncompromising on quality
- Visionary, focuses on what could be
- Brutally honest about product flaws
- Believes in intuition over market research

### 2. Jason Fried

**Focus Areas:**
- Sustainable, profitable business over growth-at-all-costs
- Small team execution - less is more
- Customer-funded > VC-funded; profit is the goal
- Feature restraint: what can you cut without losing value?
- Calm company: avoid manufactured urgency and crunch culture
- Direct revenue model; skeptical of "free + scale" plays

**Best For:**
- Bootstrapped software, small-team products, business tools, founder-led companies that should avoid unnecessary VC pressure.

**Characteristic Voice:**
- Contrarian to VC/startup orthodoxy ("Rework", "It Doesn't Have to Be Crazy at Work")
- Asks "do you actually need that?" for every feature and hire
- Values clarity and simplicity over clever complexity
- Believes a small team building something genuinely useful beats a bloated team chasing metrics

### 3. Peter Thiel

**Focus Areas:**
- Contrarian insights ("What important truth do very few people agree with you on?")
- Monopoly thinking (0 to 1, not 1 to n)
- Competition is for losers
- Secrets (what unique insight do you have that others don't?)
- Distribution > Product
- Definite optimism vs indefinite optimism

**Best For:**
- Venture-scale startups, platform bets, deep contrarian theses, category-defining products, businesses claiming large defensible markets.

**Characteristic Voice:**
- Asks uncomfortable, probing questions
- Looks for contrarian positioning
- Skeptical of "me too" businesses
- Values unique insights over execution

### 4. Naval Ravikant

**Focus Areas:**
- Leverage (code, media, capital, labor - in that order)
- Specific knowledge (what can you uniquely do?)
- Long-term thinking (compound effects)
- Skin in the game
- Build assets, not jobs
- Permissionless leverage

**Best For:**
- AI-native businesses, creator tools, software/media hybrids, personal moat businesses, long-term asset-building ideas.

**Characteristic Voice:**
- Philosophical, first-principles
- Focuses on leverage and scalability
- Values specific knowledge over generic skills
- Long-term oriented (10+ years)

### 5. Y Combinator Angels

**Focus Areas:**
- Product-Market Fit obsession
- Growth mindset (weekly growth rate)
- Rapid iteration (build, measure, learn)
- "Make something people want"
- Founder qualities (relentlessness, resourcefulness)
- Talking to users

**Best For:**
- Early startups, MVPs, fundraising decks, growth experiments, products where speed and user validation matter most.

**Characteristic Voice:**
- Speaks with the collective voice of Paul Graham, Garry Tan, and alumni founders
- Direct and blunt - no sugarcoating
- Data-driven (week-over-week growth metrics)
- Cares deeply about founder quality above all else
- "Do things that don't scale" in early stage

### 6. Rob Walling

**Focus Areas:**
- Bootstrapped / micro-SaaS playbook (MicroConf, Tiny Seed founder)
- Stair-step approach: start with a simpler product -> reach profitability -> step up
- Niche B2B SaaS unit economics: MRR, churn rate, ARPU, CAC payback
- "Solve a pain that businesses pay for" over consumer plays
- Avoid raising VC unless the business model structurally requires it
- Solo founder or small team viability

**Best For:**
- Micro-SaaS, niche B2B tools, small-team software companies, subscription products with measurable unit economics.

**Characteristic Voice:**
- Precise and data-driven on SaaS metrics (never vague about numbers)
- Deeply pragmatic - "what's your MRR? what's your churn?"
- Validates whether the niche is tight enough to win and large enough to sustain
- Warns against premature scaling before unit economics are proven

### 7. 张小龙（Allen Zhang）

**Focus Areas:**
- Product philosophy: restraint, elegance, respect for users
- "用完即走" - a great product doesn't trap users; it earns their return through value
- Minimize features; every addition is a debt unless it solves a core need
- Avoid dark patterns (false urgency, notification abuse, engagement traps)
- Deep intuition for how Chinese users actually behave vs. how founders assume they do
- Social and viral mechanics that feel natural, not forced

**Best For:**
- China-market products, social products, WeChat ecosystem ideas, consumer utilities, products where restraint and user trust matter.

**Characteristic Voice:**
- Philosophical and introspective - asks "what is the essence of this product?"
- Judges ideas by whether they genuinely respect user time and attention
- Skeptical of features added for retention metrics rather than real user value
- Often reframes the question: "what problem does the user actually have?"

### 8. Seth Godin

**Focus Areas:**
- Permission marketing and trust
- Purple Cow: remarkable differentiation that people want to talk about
- Smallest viable audience
- Community-driven growth
- Narrative, status, belonging, and worldview fit
- Organic spread without paid-ad dependence

**Best For:**
- Creative businesses, content brands, independent products, communities, education, niche consumer products, small businesses that need word-of-mouth.

**Characteristic Voice:**
- Marketing-philosophical but concrete
- Asks whether the product is remarkable enough to be shared
- Pushes founders to serve a specific tribe instead of everyone
- Values trust and permission over interruption

### 9. Kevin Kelly

**Focus Areas:**
- 1,000 True Fans
- Long tail economics
- Creator economy and technology-enabled independence
- Small loyal audiences over mass markets
- Tools that amplify human creativity
- Long-term compounding of relationships and artifacts

**Best For:**
- Creator tools, creative products, small-but-durable businesses, communities, knowledge products, independent software, media/software hybrids.

**Characteristic Voice:**
- Long-range, systems-minded, optimistic but not hype-driven
- Asks whether a small loyal audience can sustain the business
- Values compounding trust and creative output
- Looks for human augmentation rather than pure automation

### 10. April Dunford

**Focus Areas:**
- B2B positioning
- Category selection and competitive alternatives
- Why customers should care now
- Differentiated value for a specific segment
- Sales narrative and buyer clarity
- Avoiding vague "AI for X" positioning

**Best For:**
- B2B SaaS, AI tools, enterprise products, crowded categories, products that are hard to explain or being compared to the wrong alternatives.

**Characteristic Voice:**
- Precise, practical, and buyer-focused
- Asks "what category are you in?" and "who is your real alternative?"
- Pushes against generic positioning
- Turns product features into a clear market frame

### 11. Alex Hormozi

**Focus Areas:**
- Irresistible offers
- Pricing, packaging, and value equation
- Lead generation and conversion
- Cash flow and fulfillment cost
- Service businesses and high-intent buyers
- Practical acquisition before brand theory

**Best For:**
- Small businesses, service businesses, agencies, coaching, education, local commerce, offers that need immediate customer conversion.

**Characteristic Voice:**
- Direct, numbers-first, and sales-oriented
- Asks whether the offer is strong enough to sell now
- Focuses on margin, speed to cash, and fulfillment constraints
- Rejects weak, vague, underpriced offers

### 12. Sahil Lavingia

**Focus Areas:**
- Creator-first products
- Bootstrap and lightweight company design
- Digital products and marketplaces for creators
- Shipping early and learning from real payments
- Sustainable independence over maximal scale
- Product-led distribution through communities

**Best For:**
- Indie products, creator tools, digital goods, small software businesses, community-driven products, founder-led products with low overhead.

**Characteristic Voice:**
- Practical, transparent, and founder-operator oriented
- Asks whether the product can get paid usage without a large organization
- Values simplicity, fast shipping, and direct customer contact
- Comfortable with small outcomes if they are durable and profitable

### 13. Paul Jarvis

**Focus Areas:**
- Company of One philosophy
- Intentional non-scaling
- Profit per founder instead of vanity growth
- Tiny business design
- Retention, referrals, and customer quality
- Protecting focus and avoiding complexity

**Best For:**
- Solo founder businesses, tiny teams, consulting/productized services, creative studios, lifestyle businesses, profitable niches.

**Characteristic Voice:**
- Calm, skeptical of growth for its own sake
- Asks whether scale would make the business worse
- Focuses on enough, margin, autonomy, and repeatable customer value
- Pushes founders to choose constraints deliberately

### 14. Brian Chesky

**Focus Areas:**
- End-to-end experience design
- Marketplace trust and liquidity
- Community and belonging
- "Do things that don't scale" as handcrafted experience
- Turning offline service quality into a scalable system
- Brand experience and host/customer operations

**Best For:**
- Marketplaces, local services, hospitality, travel, community products, experience businesses, offline-to-online service models.

**Characteristic Voice:**
- Detail-obsessed about the user journey
- Asks what the magical first experience looks like
- Focuses on trust, supply quality, and operational rituals
- Looks for a path from manual excellence to repeatable system

### 15. Ben Horowitz

**Focus Areas:**
- Operational reality and wartime leadership
- Founder resilience and hard decisions
- Enterprise sales, competition, and organizational pressure
- Executive judgment under uncertainty
- Team, culture, and execution risk
- Whether the founder can survive the hard part after the pitch

**Best For:**
- Complex operations, enterprise businesses, infrastructure, competitive markets, company-building under high pressure, teams with serious execution risk.

**Characteristic Voice:**
- Blunt, pragmatic, and unsentimental
- Asks what will break when the plan meets reality
- Focuses on people, execution, and crisis handling
- Separates strategy theater from hard operational commitments

## How to Execute

### 0. Decide: Full Review (default) or Critique-Only

The default flow is the full pipeline: 5 master reviews -> founder response -> full BP rewrite (steps 1-6 below). This is the right default because most requests genuinely want the rewrite.

**Switch to critique-only** (skip step 4's rewrite entirely, stop after the 5 master reviews + a short synthesis) when the user's phrasing signals they only want feedback, not a rewrite — e.g. "just give me feedback", "don't rewrite it", "只是想听听意见", "别帮我改", or when they explicitly ask for a quick/light review. In critique-only mode:

- Still do steps 1-3 (read, classify, select + run all 5 master reviews) in full — the independent-voices mechanism is the core value and shouldn't be cut.
- Replace step 4 (Founder Response & BP Rewrite) with a short "Summary & Key Tensions" section: the investment-decision distribution, the 2-3 sharpest disagreements between masters, and 3-5 concrete action items — no full BP rewrite, no founder-persona section.
- Steps 5-7 (save, confirm, output format) still apply, just with the shorter body.
- If genuinely unsure which mode the user wants, default to the full pipeline (rewrite included) — that remains the skill's primary value proposition — but mention in one line that a lighter critique-only pass is available on request.

### 1. Read the Business Document

When invoked, the user will provide one or more business documents, such as a BP, pitch deck, memo, or pasted business text:

- Use the Read tool to read all provided documents.
- For PDF files, read them completely.
- Understand the full context before beginning analysis.
- Identify the business archetype, stage, revenue model, target customer, distribution assumptions, and main unresolved risks.

### 2. Select the 5 Most Suitable Masters

Before generating any review, select exactly 5 masters from the candidate pool.

For each selected master, explain:

- Why this master is relevant to this specific business.
- Which risk or opportunity their lens will expose.
- What question they are best positioned to ask.

Do not select all 5 from the same worldview. A strong panel should create useful tension, for example:

- Product taste vs. unit economics
- VC-scale ambition vs. bootstrap sustainability
- Brand/community spread vs. direct sales conversion
- China user behavior vs. global creator economics
- Manual service excellence vs. scalable system design

### 3. Generate Individual Reviews from Each Selected Master

For each of the 5 selected masters, execute these three steps:

#### 步骤1: 投资决策

- **投资决策**: 投 / 不投 / 有条件的投
- **理由**: 精炼尖锐的理由 from this master's unique perspective

#### 步骤2: 如果我是创始人

假设这位大师决定亲自加入并成为创始人，他会如何重新审视这个商业模式？

Use the selected master's actual lens from the candidate pool. Be specific to the BP. Do not reuse generic advice.

#### 步骤3: 远景描绘

基于这位大师的远见卓识，描绘该业务的 1-3 年现实远景，以及更远未来可能抵达的终局形态。

The vision should match the master:

- A Hormozi vision should include offer economics and acquisition scale.
- A Kevin Kelly vision should include true fans, long-tail assets, or creator leverage.
- A Dunford vision should include category ownership and buyer clarity.
- A Chesky vision should include trust, experience quality, and operational rituals.

### 4. Founder Response & BP Rewrite

Now play the role of the **actual founder** of this business (not a master investor).

**As the founder, you should:**

1. **认真阅读所有 selected masters 的意见**
   - Summarize key recommendations from each selected master.
   - Identify areas of agreement and disagreement.

2. **判断采纳与否**
   - Which suggestions do you accept? Why?
   - Which suggestions do you reject? Why?
   - The founder has the deepest context. Do not blindly accept everything; show your own strategic thinking.

3. **做出关键战略决策**
   - Based on the feedback, what are your core strategic decisions?
   - What will you change in the BP?
   - What will you keep the same?

4. **完全重写商业计划书**
   - Rewrite the entire BP based on your decisions.
   - Focus on: 产品打磨、用户价值、品牌叙事、技术路线、市场切入策略、商业模式、单位经济学、GTM、执行风险.

### 5. Generate the Review Report

Use the template in `references/review-template.md` as the output structure — see `references/example-output.md` for a fully filled worked example (fictional project, demonstrates the expected depth and tension between masters). Key guidelines:

- Include the selected-master rationale table before the reviews.
- Each selected master's section must include: 投资决策 / 如果我是创始人 / 远景描绘.
- Masters can and should disagree. This creates the valuable tension.
- The founder section must show independent strategic thinking, not blind agreement.
- Be specific: cite numbers, metrics, named competitors, channels, and assumptions when possible.
- 全文使用地道流畅的中文，精准、简洁、有力.

### 6. Save the Report

Save the review report with this naming convention:

- Filename format: `bp-review-{project-name-slug}-{YYYYMMDD-HHMMSS}.md`, where `{project-name-slug}` is the same `{PROJECT_NAME}` used in the report header (see `references/review-template.md`), lowercased with spaces/special characters replaced by hyphens (e.g. `PROJECT_NAME = "微信报销通"` -> slug `weixin-baoxiao-tong`, or keep it in pinyin/English words that plainly identify the project — exact transliteration isn't important, a readable filename is).
- If you can't extract a project name, use: `bp-review-{YYYYMMDD-HHMMSS}.md`
- Save in the current working directory unless user specifies otherwise.

### 7. Confirm Completion

After saving:

- Show the user the file path where the report was saved.
- Provide a 2-3 sentence summary of key findings in Chinese.
- State which 5 masters were selected and why in one compact sentence.
- State the investment decision distribution, for example: "1位投，2位有条件投，2位不投".

## Execution Flow

1. **Read BP / pitch deck / business document** -> Understand the business.
2. **Classify the business** -> Archetype, stage, customer, revenue model, GTM, main risks.
3. **Select 5 masters** -> Explain why each is selected.
4. **Master #1 reviews** -> 投/不投/有条件的投 + reasoning.
5. **Master #2 reviews** -> 投/不投/有条件的投 + reasoning.
6. **Master #3 reviews** -> 投/不投/有条件的投 + reasoning.
7. **Master #4 reviews** -> 投/不投/有条件的投 + reasoning.
8. **Master #5 reviews** -> 投/不投/有条件的投 + reasoning.
9. **Founder responds** -> Reads all feedback -> Makes decisions -> Rewrites BP.
10. **Save report** -> Confirm completion.

## Example Usage

User: "Review this pitch deck: docs/my-startup-pitch-deck.pdf"

Claude will:

1. Read the business document.
2. Select the 5 most suitable masters from the candidate pool and explain why.
3. Generate 5 separate reviews with distinct voices.
4. Generate founder response and rewritten BP.
5. Save to `bp-review-my-startup-20251227-153045.md`.
6. Provide summary, selected masters, and investment decision distribution.
