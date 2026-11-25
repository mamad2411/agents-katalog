---
name: 20vc-playbook
description: >
  Apply frameworks and mental models from 200+ episodes of 20VC (The Twenty Minute VC) to any
  startup, investment, or operator challenge. Use this skill whenever the user wants to:
  evaluate a business decision, design a sales comp plan, analyze competitive moats, think through
  a fundraise, assess founder quality, build a GTM strategy, price a product, evaluate AI disruption
  risk, think about hiring, or apply any startup/VC mental model to their situation.
  Also trigger when the user mentions: quota design, accelerators, pipeline construction, 8 moats,
  omission vs commission errors, portfolio construction thinking, PLG vs SLG, SaaS terminal value,
  burn multiple, DPI, NRR, outbound strategy, agent deployment, or any topic Harry Stebbings covers.
---

# 20VC Playbook

A comprehensive skill synthesized from 200+ episodes of 20VC (2024–2026), covering interviews
with Marc Andreessen, Demis Hassabis, Sam Altman, Klarna CEO, Monday.com CEO, ElevenLabs CRO,
Sequoia/a16z/Coatue/Benchmark partners, and 100+ top founders and operators.

## How to Use This Skill

When the user presents a challenge, **identify which framework(s) below apply**, then reason
through their situation using the relevant mental models. Always ground advice in specific
quotes and frameworks from the corpus — not generic startup advice.

---

## FRAMEWORK 1: Sales Compensation Architecture

**When to apply:** User is designing quotas, commissions, comp plans, or incentive structures.

### The ElevenLabs Model (most discussed in 20VC corpus)
- **Base commission rate:** 5% on everything including quota attainment
- **Quota = 20x base salary** (industry standard is 6-10x — 20x drives elite culture)
- **Accelerator tiers:** 1.1x → 1.2x → 1.5x → 2x above quota
- **Never pay on pilots** — only on signed annual/multi-year contracts
- **Pay on expansion:** anything that grows in next 12 months earns commission
- **AI-closed deals get full human commission** — aligns everyone with AI adoption
- **Product spiffs:** rotate quarterly to direct attention to strategic priorities

### Key Principles
- *"For every $1M in revenues any single person signs, that's $3M in extra valuation. Pay accordingly."*
- A $1M commission check is a win — that person just added $33M in company value
- Dual AE+CSM incentive on NRR: *"I'm paying double but they're both busting their ass to expand"*
- Public pipeline reviews (monthly) beat private 1:1s for building accountability culture
- Figma counter-model: quotas "kind of made up" — set to reflect the nature of the work, not as a safety blanket. Their NRR: 131% → 136%.

### What Doesn't Work
- Commissions on pilots → incentivizes wrong behavior (closing bad-fit customers)
- Too many spiffs/accelerators simultaneously → reps optimize for unlocks, not customers
- AI SDR outbound → response rates below 0.01%. *"Outbound is dead unless done humanly."*

---

## FRAMEWORK 2: Competitive Moat Analysis (Gokul's 8 Moats)

**When to apply:** User is evaluating defensibility of their business, a competitor, or an investment target.

Score each company **0–1** on each dimension:

| Moat | Description | Strong Example |
|------|-------------|----------------|
| **Data** | Live, proprietary, non-replicable | Palantir's operational data |
| **Workflow** | Embedded in daily operations (an OS, not a feature) | Rippling, Datadog |
| **Regulatory** | Compliance complexity as barrier | Stripe (financial licensing) |
| **Distribution** | You own the channel; others come through you | Salesforce AppExchange |
| **Ecosystem** | Partners/integrations create switching costs | Atlassian marketplace |
| **Network** | Value compounds with each user | LinkedIn, Slack |
| **Physical** | Hardware, data centers, real-world assets | Anduril, AWS |
| **Scale** | Cost advantages that compound with size | AWS, NVIDIA |

**Scoring:** 4+ = secure. 2–3 = vulnerable. 0–1 = at risk.

### Key Insights
- *"If you have a score of four or more, you're pretty damn secure. If you have two or three, you're in trouble."*
- Brand alone is **not** a B2B moat in the AI era (Gokul) — but brand + trust IS the only remaining moat when functionality is commoditized (Elena Verna counter-argument)
- **"Commoditize a complement"**: give away the non-profit-pool layer for free; charge for the defensible layer
- AI is attacking moats 1 (data), 2 (workflow), and 5 (ecosystem) fastest — audit these first

---

## FRAMEWORK 3: Decision-Making Under Uncertainty

**When to apply:** User is making a high-stakes decision with incomplete information.

### Omission vs. Commission Errors (Andreessen, Mitchell Green, Benchmark)
- **Commission error:** You make a bad investment/hire/bet and lose $10M → visible, embarrassing
- **Omission error:** You don't invest in Google → invisible, catastrophic
- *"The sins of omission are much more significant than the sins of commission."*
- Default your anxiety to: *"What am I not doing?"* not *"What went wrong?"*

### The Scalded Stove Anti-Pattern (Andreessen)
- Don't let a failed investment/initiative in a category close your mind to the next opportunity there
- AI was "a great way to lose money from 1945 to 2017" — then became the most important theme ever
- In venture AND in GTM: learning the wrong lesson from a failure is worse than the failure itself

### Self-Validation Machine (Oren Zeev, quoting Annie Duke)
- *"We are self-validation machines, not truth seekers"* — brains filter new data to confirm priors
- Test: *"Would I still do this if I hadn't already started?"* Run this before every follow-on decision
- Celebrate team members who change their minds with new data; penalize those who double down on ego

### Intuition vs. Wishful Thinking (Jerry Murdock, Insight Partners)
- *"Intuition was almost never wrong. But what I was wrong about was thinking it was intuition — it was wishful thinking."*
- Pattern: people you **struggle with** personally often succeed. People you **like** often disappoint.
- Distinguish: pattern-recognition from experience (intuition) vs. wanting something to be true (wishful thinking)

### Process vs. Outcome
- A good bet can lose. A bad bet can win.
- Judge decisions by the quality of your *process*, not the result
- Keep a decision journal: write reasoning *before* outcomes; review quarterly

**Recommended reading:** *Thinking in Bets* by Annie Duke (referenced in 15+ episodes)

---

## FRAMEWORK 4: Portfolio Construction Thinking

**When to apply:** GTM strategy, market entry, investment strategy, resource allocation.

### Applied to Go-to-Market (Carles Raina, ElevenLabs)
- *"GTM is exactly like investing in venture — test 100 things to find 3–5 that perform."*
- Forecasting is "impossible" in this model — and that's **correct** behavior, not a bug
- Every market entry needs a written thesis *before* you start — so you can kill it cleanly if wrong
- Kill experiments that don't produce signal in 90 days; double down on the ones that do

### Applied to VC Fund Strategy
- *"Fund size IS the strategy"* — size determines what you can and cannot do
- Mega funds ($3B+): must swing for $10B+ outcomes; can't do true seed
- Seed specialists ($50-150M): win ownership at entry, but can't protect at growth
- The middle ($300-800M) is being squeezed from both sides

### The Lily Pad Model (Anduril)
- Never commit large capital until small learning-contracts prove viability
- Run an internal investment committee review at each jump to new commitment level
- *"Don't enter the J-curve if you don't have faith it will come through the other end"*

### Go Wide, Not Sequential
- Old VC advice: "go deep in one market, then expand" — **explicitly called outdated**
- In an AI world where competitors emerge in weeks, parallelizing market bets is the only defense
- Counter: *"You need a thesis for each market — not as many markets as possible, but parallel bets with reasoning"*

---

## FRAMEWORK 5: Revenue Architecture for the AI Era

**When to apply:** User is building or rebuilding their revenue motion, CS team, or sales process.

### Customer Success = Revenue Function (Not Satisfaction)
- CS must be incentivized on expansion, upsells, cross-sells — not NPS or happiness scores
- *"Customer success needs to be a money generation function for the business"*
- The farmer vs. hunter problem: cushy CS loses every renewal to a competitor's hungry hunter
- Figma model: **no CS team** — AEs own post-sale relationships proactively

### Pipeline Construction (vs. Pipeline Management)
- Balance **whales** (large enterprise = confidence) with **liquidity** (smaller deals = momentum)
- Without liquidity in the pipeline, reps lose confidence and stop closing anything
- *"Be as negative as possible on forecast. If you think $500K, put $24K."* — radical conservatism = board trust

### Outbound Culture
- AI SDR mass outbound is dead: response rates below 0.01%
- Only outbound that works: hyper-personalized, human-sounding, genuinely relevant
- ElevenLabs went from 10% → 40% outbound by building culture, not buying AI tools
- *"A good leader needs to be a good outbounder. A VC is just a glorified SDR."*

### AI in Revenue Operations (What Actually Works)
1. **AI proposals manager**: scans web for RFPs/RFIs, scores and drafts proposals
2. **AI CS drafts**: reads all customer data + contract + pricing tiers → drafts personalized emails each morning. Human reviews and sends. Store sent+response for fine-tuning.
3. **AI-closed deals**: pay full commissions as if a human closed it

---

## FRAMEWORK 6: AI Agent Deployment

**When to apply:** User is evaluating, building, or deploying AI agents in their business.

### The Deployment Sequence
1. **Coding agents** (best starting point — LLMs natively good here)
2. **Computer-using agents** (browser, apps, workflows)
3. **General agents** (open-ended tasks)
*"All agents are actually coding agents — coding is just the best way for an agent to use a computer."* — OpenAI Codex Lead

### What Works
- Scoped, well-defined workflows with clear success criteria
- Agents that have access to the actual source data (not docs or summaries)
- Human-in-the-loop review for ambiguous cases + exceptions
- Every deployed agent requires: custom data cleansing, forward-deployed engineers, 3–6 months of tuning

### What Doesn't Work
- AI SDR mass outbound (see Framework 5)
- General agents on ambiguous, long-horizon tasks (not yet reliable)
- Plug-and-play agent tools without customization — enterprises that try self-deploy spend 3 months failing

### Key Metrics
- **Token spend as % of revenue**: coding apps 40-70% (existential), most B2B 5-8% (ignore it)
- This is the new AWS cost conversation — bring it to every board meeting

---

## FRAMEWORK 7: Talent Architecture

**When to apply:** Hiring decisions, team design, performance management, culture-building.

### The Non-Negotiable Bar
- **Never hire a B player.** Headcount gaps are better than quality dilution.
- *"I haven't hired a B player. I don't have all the headcount I need, but I haven't hired a B player."* — Figma CRO
- *"Whenever you make a change, there's a one-in-three chance the person you hire is an empty suit."*

### Mercenary vs. Missionary Detection
- Mercenaries: lead with comp/title/benefits optimization in interviews
- Missionaries: first questions are about mission, product, customer, impact
- Watch the *sequence* — what they ask about first reveals what drives them

### Hire for Grit, Not Credentials
- *"Determination, resilience, and belief in the vision — we should have hired those people from the start."*
- People who've survived real crises (failure, financial collapse, adversity) are dramatically more reliable under pressure
- Andreessen's formula: **IQ + courage + primal drive** (not IQ + pedigree + references)

### Founder Quality Signal (for investors)
- *"I only need 20 minutes to know if I want to hire someone"* — Carles Raina
- The people you struggle with personally often succeed. The people you like often disappoint.
- Best predictor: *"Does this person continuously hit target?"* — Inertia is the best mental model.

---

## FRAMEWORK 8: Pricing & AI Monetization

**When to apply:** Pricing strategy, AI feature monetization, packaging decisions.

### The AI Monetization Litmus Test (Jason Lemkin)
A company is genuinely AI if and only if:
1. It **charges meaningfully** for AI features (not giving them away to protect NRR optics)
2. It shows **50%+ ARPO growth** attributable to AI

Everything else is *"AI dust sprinkled on analytics software"* — the market will eventually reprice it.

### Pricing Model Evolution
- Seat-based: still alive in B2B (Figma NRR 131% → 136%) but under pressure where AI replaces labor
- Consumption/outcome-based: winning for products that replace headcount
- Rule: *"If you're building from scratch, you have pricing power. If you're competing, you'll get squeezed."*

### Token Economics
Track **token spend as % of revenue**:
- Coding apps: 40-70% → existential, must be managed obsessively
- Most B2B SaaS: 5-8% → irrelevant, stop worrying

---

## FRAMEWORK 9: Fundraising & Valuation Discipline

**When to apply:** Raising a round, evaluating a term sheet, setting valuation expectations.

### The 2-Year Rule (Ali Ghodsi / Databricks)
*"Never raise more than two years ahead of the valuation I was confident I could hit."*
- Beyond 24 months of extrapolation = creating future emotional debt
- The Brex lesson: raised at $12B in 2021, sold for $5.15B in 2026 — technically great, emotionally brutal
- *"The bad feelings last a day. The $5 billion lasts forever."*

### DPI is the Only Metric That Matters (LP perspective)
- TVPI (paper gains) has lost credibility post-2022
- IRR is gameable with NAV timing
- *"DPI or die"* — distributed, realized capital is the only honest number
- Practical: understand your cap table's DPI pressure — it shapes board behavior

### Revenue Multiples Are Category-Permanent
- Financial services companies trade at 7x forever, regardless of growth-era narrative
- AI-native infrastructure: 40-100x
- *"Things prove up in the end for what they really are"*

---

## FRAMEWORK 10: Brand & Trust as Growth Infrastructure

**When to apply:** Growth strategy, marketing, demand generation, events.

### Trust Hierarchy (Elena Verna — highest to lowest ROI)
1. **Product** — reliability and delight create trust
2. **Community** — users trusting each other amplifies product trust
3. **Word of mouth** — peer recommendations; highest-converting channel
4. **Content/creators** — your ideas earning attention before your product does
5. **Paid media** — lowest trust, highest cost, last resort

*"Investing in paid in your first year is a death trap. You haven't earned trust yet."*

### Enterprise Brand = Shortened Sales Cycles
- *"Brand reduces enterprise sales cycles by 1 million percent"* — Carles Raina
- The goal: *"No one gets fired for buying IBM"* — make your brand the safe choice
- Cursor, Anthropic, OpenAI: the only three AI brands where this is true in 2025-2026

### Events ROI Ranking
1. **Dinners** ($3-5K, 12-15 right ICPs): best enterprise ROI. FOMO of competitors at same table accelerates every deal.
2. **Own events**: build your own; stop paying to be a booth at someone else's
3. **Conferences**: almost no ROI. *"We should be spending less on those things."*

---

## FRAMEWORK 11: VC / Investor Mental Models

**When to apply:** Investment decisions, fund strategy, LP management, portfolio support.

### The Contrarian + Right Formula (Oren Zeev)
- *"If a deal looks wrong or weird, there's less competition and a 2-3 year window to build a moat."*
- Being contrarian alone loses money. Contrarian AND correct is the formula.
- Suppress social proof signals deliberately — consensus = crowded = no alpha

### Platform Company Filter (Coatue / Lucas Swisher)
- Invest in companies that can "skip TAMs" — reinvent themselves across multiple S-curves
- Databricks: ELT → data warehousing → AI platform
- Canva: yearbooks → SaaS design → AI creative suite
- Single-product companies get stranded when their S-curve matures (now happens in 18-24 months)

### The 18-Months-Out Money Test (Mitchell Green)
- At any entry price, model revenues forward 18 months + apply a reasonable multiple
- If you're not in the money, don't do the deal — regardless of narrative quality

### Step-Function Company Valuation
- SpaceX/Tesla/DeepMind don't grow linearly — they achieve hard milestones, harvest 5-7 years, fund the next step
- Standard DCF/revenue multiples useless — you're assigning probability to the next milestone occurring on schedule

---

## FRAMEWORK 12: SaaS vs. AI — Survival Analysis

**When to apply:** Evaluating incumbent software companies, SaaS investments, competitive threats.

### The Fortnite Circle / Shrinking Island (Jason Lemkin)
- Claude/AI keeps expanding its surface area. Every adjacent software product's defensible turf keeps shrinking.
- *"No matter what they say, they know they are not the dominant agent in their space."*
- The only protection: own something so deep (databases, production infra) that AI won't bother, or move faster than the foundation model does

### AI Monetization Litmus Test for Incumbents
A company is a real AI company if: (1) charges for AI features, and (2) shows 50%+ ARPO growth.
- Palantir: passes (AIP deployed in production, pricing premium)
- Most others: "AI dust on analytics software"

### The Installed Base Trap
- For incumbents at scale: installed base is simultaneously the greatest asset (no CAC) and greatest liability (50 years of technical debt consumes 98% of engineering)
- Intercom is cited as the only company that consciously let its core business partially decline to fund agent-first reinvention

### Headcount as Signal
- *"Is headcount a bug, not a feature now in companies?"* — Insight Partners
- Klarna: 7,000 → below 3,000 people. Revenue growing.
- Monday.com: replaced 100 SDRs with agents
- Revenue-per-employee at AI-native companies (Cursor: ~$2.6M/employee) rivals Apple

---

## FRAMEWORK 13: Mental Health & Sustainable Performance

**When to apply:** User mentions burnout, founder wellbeing, work-life balance, leadership loneliness.

### The Honest Trade-Off
*"I choose to work the amount I work. But there's a consequence — you're sacrificing your partner, your friends, all of that."*

### What Sustains Peak Performers (across 49+ episodes)
- **Extreme ownership**: *"Life gets simpler if you assume everything is your own fault."* — drains resentment, creates intrinsic motivation
- **Physical rituals**: exercise, sleep, disconnected time — non-negotiable maintenance, not indulgence
- **Grounding activities**: Carles Raina: *"I talk to my plants. That's when I'm most stressed — I spend an hour looking after them. It gives me back energy."*
- **Therapy and community**: more openly discussed in 2025-2026 than any prior era of the show

### Replace Yourself Deliberately
- The company you need to run at $1M ARR is different at $10M, $50M, $200M
- *"If the founder hires someone great, you can have amazing outcomes — that's what the facts say"*
- Write your "replace myself" roadmap: what does the version of you the company needs in 24 months look like?

---

## How Claude Should Apply This Skill

1. **Identify the user's challenge** — fundraise, hiring, pricing, GTM, investment decision, etc.
2. **Select the most relevant framework(s)** from above
3. **Apply specifically** — use the actual numbers, principles, and quotes from the corpus
4. **Surface the tensions** — most decisions involve trade-offs between frameworks (e.g., omission vs. commission, quota difficulty vs. attainability)
5. **Push for specificity** — ask for numbers, context, and constraints before giving generic advice
6. **End with the contrarian view** — always ask: *"What would the person who disagrees with this recommendation say?"*

The goal is to bring the depth of 200+ hours of conversations with the world's best founders, investors, and operators to bear on the user's specific situation — not to summarize the podcast.
