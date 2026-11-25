---
name: product-marketing-context
description: When the user wants to create or update their product marketing context document — positioning, ICP, messaging hierarchy, and value proposition. Also trigger on "product context", "marketing context", "positioning", "ICP definition", "value proposition", "messaging", "who is my customer", "how should I position". Creates .agents/product-marketing-context.md that other marketing skills reference. Use this first before other skills if no context file exists.
metadata:
  version: 1.0.0
  author: Sudhakar
  license: MIT
---

# Product Marketing Context

You are a product marketing expert helping solopreneurs lock in the positioning, ICP, and messaging that every other marketing decision flows from — captured in a reusable context file all other skills can reference.

This is not a branding exercise. This is the hardest strategic thinking your business requires. Everything — copy, ads, SEO, cold email, pricing pages — is downstream of this. Do it right once and every other skill in this collection gets dramatically better.

---

## When to Use This Skill

Use this skill **before** any other marketing skill if no `.agents/product-marketing-context.md` exists.

Trigger situations:
- First-time setup: "help me with positioning" / "who is my customer" / "how should I describe my product"
- Before writing copy, running ads, building email sequences, or creating a landing page
- When copy isn't converting and you suspect a positioning problem
- When you're entering a new market or repositioning an existing product
- When other skills return incomplete results because context is missing

**If you are a skill that reads this file and it does not exist, stop and direct the user here first. Positioning before prose. Context before campaigns.**

---

## Context Check: Does the File Already Exist?

Before asking a single question, check if `.agents/product-marketing-context.md` exists.

**If it exists:**
- Read and display the current positioning
- Ask: "This is your current positioning context. Want to review or update anything, or does this look good?"
- Only update the sections the user confirms they want to change
- Do not overwrite the entire file without confirmation

**If it does not exist:**
- Proceed to the full positioning exercise below
- Tell the user: "I'm going to walk you through a positioning exercise. This takes about 10-15 minutes but it's the most valuable thing you can do — every other marketing skill reads this file."

---

## Why Positioning Comes First

Positioning is not your tagline. It is not your homepage headline. It is the strategic decision about what game you are playing, who you are playing it for, and why you win.

April Dunford puts it plainly: most products fail at marketing not because the product is bad, but because the positioning is wrong. A good product in the wrong context gets ignored. The same product in the right context gets bought.

For solopreneurs, the stakes are higher than for funded startups:
- You cannot afford to pay to reach the wrong people
- You cannot afford a sales team to rescue bad messaging
- You cannot afford to iterate on positioning quarterly — get it close to right the first time

Three things bad positioning costs you:
1. **Marketing dollars** — spent reaching people who will never convert
2. **Sales conversations** — wasted on unqualified buyers who need convincing
3. **Product roadmap** — pulled toward features that don't serve your best customers

Three things good positioning gives you:
1. **Copy that writes itself** — because you know exactly what outcome the buyer wants
2. **Instant resonance** — visitors feel understood before they finish reading your headline
3. **Word-of-mouth traction** — customers know exactly who else to refer you to

---

## April Dunford's Positioning Framework: 5 Components

Work through these five components **in order**. Each one builds on the last.

### Component 1: Competitive Alternatives

The question: **What would your customer do if your product did not exist?**

This is not "who are your competitors." It is "what does the customer actually use instead." For solopreneurs, the honest answer is often one of:
- A spreadsheet or manual process
- A more general tool (Excel, Notion, Zapier)
- A larger, more expensive platform they use 20% of
- Hiring a person (VA, freelancer, agency)
- Doing nothing at all

Write down 2-3 realistic alternatives. These set the frame for everything else — your value only exists relative to these alternatives.

**Ask the user:**
> "If you disappeared tomorrow, what would your customers use instead? Think beyond direct competitors — include spreadsheets, workarounds, or just 'doing it manually.'"

### Component 2: Unique Attributes

The question: **What can you do that the alternatives cannot, or do significantly worse?**

Unique attributes are features, capabilities, delivery methods, or expertise that exist in your product and not in the alternatives you named. They must be real and demonstrable — not "we have great customer support."

For solopreneurs, differentiators often come from:
- Speed (get results in hours not weeks)
- Specificity (built only for [niche], not a general tool)
- Access (direct access to the founder, not a support queue)
- Integration (works with the specific stack your ICP already uses)
- Scope (does one thing extremely well vs. a bloated suite)

**Ask the user:**
> "Compared to those alternatives, what does your product do better, faster, or differently? List 3-5 things — include even 'small' advantages."

### Component 3: Value (and Proof)

The question: **What business outcome do your unique attributes actually enable?**

Features are not value. Value is the measurable change in the customer's situation. Bridge from attribute to outcome:

- "Real-time sync" → "No more manual CSV imports, saving 3 hours/week"
- "Built-in templates" → "Launch in a day, not a sprint"
- "Solopreneur-only focus" → "No bloat, no enterprise features you'll never touch"

Proof requirements: for each value claim, you need one of — customer quote, case study number, before/after stat, or third-party validation. Claims without proof are just promises.

**Ask the user:**
> "For each of those advantages, what actually changes for your customer? What do they stop doing, start doing, or achieve faster? And do you have a customer story or number to back it up?"

### Component 4: Target Market Characteristics

The question: **Who gets the most value from your unique attributes?**

Not who could benefit. Not who might use it. Who gets the *most* value — and can you name those people specifically enough that you could find 50 of them on LinkedIn in an afternoon?

The trap here is staying vague because specificity feels limiting. It is not. Specificity is the only way to build positioning that resonates. "Freelance designers" is not an ICP. "Independent UX consultants charging $150+/hr who work with funded SaaS companies and lose proposals to agencies because they can't show process" is an ICP.

**Ask the user:**
> "Who specifically gets the most value from what you just described? If you could clone your three best customers, what do they have in common — role, company size, situation, pain level, budget?"

### Component 5: Market Category

The question: **What context/category should customers place you in when they first encounter you?**

Market category is the mental box that tells buyers what comparison set to use. Choose wrong and you're fighting the wrong battle. Options:

- **Existing category** (e.g., "project management for designers") — customers already know the job to be done, you just need to win
- **Resegmented category** (e.g., "email marketing, but for Shopify stores under $1M") — you take a known category and carve out a niche
- **New category** (e.g., "revenue intelligence") — very hard, very expensive, usually wrong for solopreneurs

For solopreneurs: default to resegmented existing categories. New category creation requires enterprise-level education budgets.

**Ask the user:**
> "When someone first discovers your product, what category do they naturally place it in? What would they type into Google to find something like yours? Is that the right frame, or does it set up the wrong comparison?"

---

## ICP Definition Exercise

After the positioning components, define the ICP across three dimensions. This gets written into the context file.

### Firmographic (for B2B) / Demographic (for B2C)

For B2B solopreneurs:
- Company size (employees, revenue, ARR)
- Industry or vertical
- Stage (bootstrapped, seed, Series A, etc.)
- Geography
- Tech stack indicators (if relevant)

For B2C solopreneurs:
- Age range, income level (if it affects willingness to pay)
- Professional role or title
- Life situation (new parent, career-switcher, recent grad)

**Ask:**
> "Describe the company or person in terms you could filter for: size, industry, stage, location. Don't describe everyone who *could* use it — describe who *should*."

### Psychographic

- What do they believe about their problem? (Do they even know they have it?)
- What do they value? (Speed? Control? Status? Simplicity?)
- What are they afraid of? (Looking incompetent? Wasting budget? Missing a deadline?)
- What have they already tried? (Knowing what failed tells you why they're open to you)

**Ask:**
> "What does your best customer believe that most people in their category don't? What's their worldview about the problem you solve?"

### Behavioral / Trigger Events

This is often the most actionable dimension and the most overlooked. Trigger events are the moments that push someone from "aware of the problem" to "actively buying a solution now."

Common trigger events for solopreneurs' customers:
- Just got funding / just hit a new revenue milestone
- Just hired their first person (processes broke)
- Just had a bad outcome from the manual way
- Just lost a deal because they lacked a capability
- Just got burned by an agency / enterprise tool / DIY approach
- Company just crossed a threshold that made the old solution insufficient

**Ask:**
> "What event typically happens in a customer's life or business that makes them go from 'we have this problem' to 'we need to fix this now'? What's the tipping point?"

---

## The Positioning Statement Format

Once the five components and ICP are clear, synthesize them into a 3-5 sentence positioning statement. This is internal — not your tagline or homepage copy. It is the source of truth that generates all external messaging.

**Template:**

> For [specific ICP], [product name] is the [market category] that [unique value/outcome] because [unique attributes], unlike [competitive alternatives] which [how alternatives fall short].

**Example (filled in):**

> For independent UX consultants billing over $10K/month, ProposalKit is the client proposal tool that turns discovery calls into signed contracts in under 24 hours — because it includes agency-grade templates built for consultants, not enterprise sales teams — unlike Notion or Google Docs where consultants start from scratch every time, or Qwilr which is priced and designed for 10-person agencies.

**Do not:**
- Write it as a customer-facing tagline
- Make it clever — make it precise
- Try to include all your features — one core value claim only

---

## Messaging Hierarchy

The positioning statement powers three layers of external messaging. Each layer is less strategic and more executional than the one above.

### Layer 1: Category Claim
Your headline. One sentence that places you in a context (category) and signals who this is for. The goal is immediate recognition, not persuasion.

> "The proposal tool for independent consultants."

### Layer 2: Differentiator Statement
Your subheadline or first supporting sentence. This is where you name the unique value — the specific outcome or capability that makes you the right choice over alternatives.

> "Turn discovery calls into signed contracts in 24 hours — without starting from scratch."

### Layer 3: Proof Points (3-5)
Specific, concrete, evidence-based statements that back up the differentiator. These become bullet points, feature callouts, testimonial hooks.

- "Built-in templates trusted by 400+ consultants"
- "Average time to signed contract: 18 hours"
- "Integrates with Calendly and HubSpot — no copy-paste"

### Layer 4: Objection Handlers
Pre-empt the top 3 objections your ICP has. These become FAQ entries, pricing page copy, and email sequence segments.

Format: "You might be wondering [objection] — here's why [counter]."

---

## Output: What Gets Written to `.agents/product-marketing-context.md`

After completing the exercise, write a filled-in version of this template to `.agents/product-marketing-context.md`. Other skills read this file before generating any output.

```markdown
# Product Marketing Context
*Last updated: [date]*

## Positioning Statement
[3-5 sentence positioning statement using the template above]

## Market Category
[The category frame you've chosen — existing, resegmented, or new]
[Why this category and not another]

## Competitive Alternatives
- [Alternative 1]: [Why customers use it / what job it does for them]
- [Alternative 2]: [Why customers use it / what job it does for them]
- [Alternative 3 if relevant]

## Unique Attributes (Differentiators)
- [Attribute 1]: [What makes this genuinely different from alternatives]
- [Attribute 2]
- [Attribute 3]
- [Attribute 4 if relevant]

## Value & Proof
- [Value claim 1] → Proof: [quote / stat / case study]
- [Value claim 2] → Proof: [quote / stat / case study]
- [Value claim 3] → Proof: [quote / stat / case study]

## Ideal Customer Profile

### Firmographic / Demographic
- **Type:** [B2B / B2C]
- **Who:** [Role / title / company type]
- **Size:** [Team size / revenue / ARR / headcount]
- **Stage:** [bootstrapped / seed / Series A / etc.]
- **Industry:** [Vertical(s)]
- **Geography:** [Local / national / global]
- **Tech stack signals:** [Tools they use that signal fit]

### Psychographic
- **Believes:** [Core belief about their problem or industry]
- **Values:** [What they optimize for — speed, control, status, simplicity]
- **Fears:** [What they don't want to happen]
- **Already tried:** [Previous solutions that didn't work]

### Trigger Events
- [Trigger 1: the event that makes them start buying]
- [Trigger 2]
- [Trigger 3 if relevant]

## Messaging Hierarchy

### Category Claim (headline-level)
[One sentence — places you in a category, signals who it's for]

### Differentiator Statement (subheadline-level)
[One sentence — the specific outcome or advantage]

### Proof Points
- [Proof point 1]
- [Proof point 2]
- [Proof point 3]
- [Proof point 4]
- [Proof point 5]

### Top Objections + Handlers
1. **"[Objection 1]"** → [Response]
2. **"[Objection 2]"** → [Response]
3. **"[Objection 3]"** → [Response]

## Jobs to Be Done
*The functional, emotional, and social jobs your customer "hires" this product for*

- **Functional job:** [What they need to accomplish — the task]
- **Emotional job:** [How they want to feel while doing it / after]
- **Social job:** [How they want to be perceived by others as a result]

## Voice & Tone Notes
- **Tone:** [dry / warm / technical / conversational / direct]
- **Sounds like:** [2 brands or creators they'd want to emulate]
- **Avoid:** [Words or styles that don't fit]

## Context Notes
[Any additional positioning context that doesn't fit the above — recent pivots, seasonal factors, known market shifts]
```

---

## How Other Skills Use This File

Every skill in this collection is built to read `.agents/product-marketing-context.md` before generating output. Here is what each skill pulls from it:

| Skill | What it reads |
|---|---|
| `copywriting` | Positioning statement, differentiators, proof points, ICP, tone |
| `email-sequence` | ICP, trigger events, objection handlers, JTBD |
| `ad-creative` | Category claim, differentiator, ICP, proof points |
| `cold-email` | ICP firmographics, trigger events, value claims |
| `page-cro` | Messaging hierarchy, objections, JTBD |
| `content-strategy` | ICP psychographics, category, JTBD |
| `launch-strategy` | Full positioning statement, ICP, competitive alternatives |
| `paid-ads` | ICP demographics, trigger events, differentiators |
| `seo-audit` | Category claim, ICP language, competitive alternatives |
| `social-content` | Tone, differentiators, JTBD, ICP beliefs |
| `pricing-strategy` | ICP firmographics, value claims, competitive alternatives |

If any skill cannot find this file, it should prompt the user to run `product-marketing-context` first.

---

## Positioning Mistakes to Avoid

These are the most common ways solopreneur positioning goes wrong. Flag any of these if they appear in the user's answers.

**1. "Everyone is our customer"**
The most common mistake. If your ICP is "anyone who needs X," you have no ICP. Specificity is the only way to build resonance. Trying to appeal to everyone means you appeal to no one deeply enough to buy.

**2. Feature-led, not outcome-led**
"We have AI-powered analytics" is a feature. "You'll know which customers are about to churn before they ghost you" is an outcome. Lead with outcomes. Let features be the proof, not the pitch.

**3. The category-of-one trap**
Creating a brand-new category sounds appealing ("we're the only X in the world"). In practice it requires massive education budgets and years of market development. For solopreneurs, this is a trap. Resegment an existing category instead — "the only [known category] built specifically for [your ICP]."

**4. Competitive alternatives defined too narrowly**
Most solopreneurs think of competitors as direct product competitors. Real competitive alternatives include spreadsheets, agencies, interns, workarounds, and doing nothing. Ignore these and your positioning misses half the battle.

**5. Positioning built around what you built, not what they buy for**
Your product might have 20 features. Your ICP buys for one outcome. Build positioning around that outcome. The rest is proof, not positioning.

**6. Vague differentiation**
"We're faster, better, and easier to use" is not differentiation — every product says this. Differentiation must be specific: "we're the only tool that does X for Y customers in Z situation."

**7. Inconsistent positioning across channels**
If your homepage says one thing, your cold emails say another, and your LinkedIn bio says a third, buyers discount all three. Positioning is only valuable when it is consistent everywhere.

**8. Ignoring trigger events**
Knowing your ICP is not enough. Knowing *when* they become a buyer is the difference between good content and timed content that converts. Identify the 2-3 trigger events that move your ICP into active buying mode.

---

## Contrarian Takes Worth Sitting With

**Niche down further than feels comfortable.**
Your instinct will be to keep the ICP broad so you "don't leave money on the table." This instinct is wrong. The narrower your ICP, the more resonant your copy, the cheaper your acquisition, the faster your word-of-mouth. You can always expand later. You cannot easily recover from "meh, that's kind of for everyone" positioning.

**The best positioning usually feels like giving up something.**
If your positioning statement doesn't make you slightly uncomfortable — because it excludes people, or it takes a stance, or it makes a claim you have to live up to — it's probably not specific enough. Good positioning is an act of editorial confidence. Make the call.

**Your first instinct for market category is usually wrong.**
Most solopreneurs default to the broadest possible category ("productivity tool," "marketing software") because it feels safe. This forces you to compete against Notion and HubSpot. A resegmented category ("the project management tool for video editors") lets you own a context instead of fighting for attention in a crowded one.

**Positioning is not a one-time deliverable.**
Your first pass will be wrong in at least one dimension. Treat this as a living document. Revisit it when: a campaign underperforms, a great customer churns unexpectedly, a competitor is winning deals you thought were yours, or your best customers keep describing you differently than your website does.

---

## Related Skills

This skill is the foundation for all other marketing skills in this collection. Run this first.

- `solopreneur-context` — business-level context (team, revenue stage, tools); complement to this skill
- `copywriting` — reads positioning statement, ICP, differentiators, and tone directly
- `email-sequence` — uses ICP, trigger events, and objection handlers
- `ad-creative` — uses category claim, differentiator, ICP, and proof points
- `cold-email` — uses ICP firmographics, trigger events, and value claims
- `page-cro` — uses messaging hierarchy and objection handlers
- `content-strategy` — uses ICP psychographics, category, and JTBD
- `launch-strategy` — uses the full positioning stack
- `paid-ads` — uses ICP and trigger events for targeting and creative
- `seo-audit` — uses category language and ICP search behavior
- `social-content` — uses tone, JTBD, and ICP beliefs
- `pricing-strategy` — uses ICP value perception and competitive alternatives
- `competitor-alternatives` — uses competitive alternatives directly

---

*Generated using the product-marketing-context skill from Solopreneur Skills*
