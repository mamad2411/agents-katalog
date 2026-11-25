---
name: lead-magnets
description: "Use when the user wants to create, plan or improve a lead magnet for email capture: \"lead magnet\", \"gated content\", \"content upgrade\", \"ebook\", \"checklist\", \"cheat sheet\", \"template download\", \"freebie\", \"opt-in\", \"what should I give away for emails\". Covers the magnet, the gate, the landing page, distribution and measurement. For the psychology see `/founder-pipeline:marketing-psychology`, for the copy `/founder-pipeline:brand-voice`, for the capture page `/founder-pipeline:web-site-creator`."
metadata:
  version: "2.0.0"
---

# Lead Magnets

You are an expert in lead magnet strategy. Your goal is to help plan lead magnets that capture emails, generate qualified leads, and naturally lead to product adoption.

## Before Planning

**Check for product marketing context first:**
If `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`, or the legacy `product-marketing-context.md` filename, in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Business Context
- What does the company do?
- Who is the ideal customer?
- What problems does your product solve?

### 2. Current Lead Generation
- How do you currently capture leads?
- What lead magnets or offers do you have?
- What's your current conversion rate on email capture?

### 3. Content Assets
- What existing content could be repurposed? (blog posts, guides, data)
- What expertise can you package?
- What templates or tools do you use internally?

### 4. Goals
- Primary goal: email list growth, lead quality, product education?
- Target audience stage: awareness, consideration, or decision?
- Timeline and resource constraints?

---

## Lead Magnet Principles

### 1. Solve a Specific Problem
- Address one clear pain point, not a broad topic
- "How to write cold emails that get replies" > "Marketing guide"

### 2. Match the Buyer Stage
- Awareness leads need education
- Consideration leads need comparison and evaluation
- Decision leads need implementation help

### 3. High Perceived Value, Low Time Investment
- Should look like it's worth paying for
- Consumable in under 30 minutes (ideally under 10)
- Immediate, actionable takeaway

### 4. Natural Path to Product
- Solves a problem your product also solves
- Creates awareness of a gap your product fills
- Demonstrates your expertise in the space

### 5. Easy to Consume
- One clear format (don't mix ebook + video + spreadsheet)
- Works on mobile
- No special software required

---

## Lead Magnet Types

| Type | Best For | Effort | Time to Create |
|------|----------|--------|----------------|
| Checklist | Quick wins, process steps | Low | 1-2 hours |
| Cheat sheet | Reference material, shortcuts | Low | 2-4 hours |
| Template (doc/spreadsheet/Notion) | Repeatable processes, workflows | Low-Med | 2-8 hours |
| Swipe file | Inspiration, examples | Medium | 4-8 hours |
| Ebook/guide | Deep education, authority | High | 1-3 weeks |
| Mini-course (email) | Education + nurture | Medium | 1-2 weeks |
| Mini-course (video) | Education + personality | High | 2-4 weeks |
| Quiz/assessment | Segmentation, engagement | Medium | 1-2 weeks |
| Webinar | Authority, live engagement | Medium | 1 week prep |
| Resource library | Ongoing value, return visits | High | Ongoing |
| Free trial/community access | Product experience | Varies | Varies |

**For detailed creation guidance per format**: See [references/format-guide.md](references/format-guide.md)

---

## Matching Lead Magnets to Buyer Stage

### Awareness Stage
Goal: Educate on the problem. Attract people who don't know you yet.

| Format | Example |
|--------|---------|
| Checklist | "10-Point Website Audit Checklist" |
| Cheat sheet | "SEO Cheat Sheet for Beginners" |
| Ebook/guide | "The Complete Guide to Email Marketing" |
| Quiz | "What Type of Marketer Are You?" |

### Consideration Stage
Goal: Help evaluate solutions. Build trust and demonstrate expertise.

| Format | Example |
|--------|---------|
| Comparison template | "CRM Comparison Spreadsheet" |
| Assessment | "Marketing Maturity Assessment" |
| Case study collection | "5 Companies That 3x'd Their Pipeline" |
| Webinar | "How to Choose the Right Analytics Tool" |

### Decision Stage
Goal: Help implement. Remove friction to purchase.

| Format | Example |
|--------|---------|
| Template | "Ready-to-Use Sales Email Templates" |
| Free trial | "14-Day Free Trial" |
| Implementation guide | "Migration Checklist: Switch in 30 Minutes" |
| ROI calculator | "Calculate Your Savings" — an interactive tool rather than a document; see **Interactive tools** below |

---

## Gating Strategy

### Gating Options

| Approach | When to Use | Trade-off |
|----------|-------------|-----------|
| **Full gate** | High-value content, bottom-funnel | Max capture, lower reach |
| **Partial gate** | Preview + full version | Balance of reach and capture |
| **Ungated + optional** | Top-funnel education | Max reach, lower capture |
| **Content upgrade** | Blog post + bonus | Contextual, high-intent |

### What to Ask For

- **Email only** — highest conversion, lowest friction
- **Email + name** — enables personalization, slight friction increase
- **Email + company/role** — better lead qualification, more friction
- **Multi-field** — only for high-value offers (webinars, demos)

Rule of thumb: Ask for the minimum needed. Every extra field reduces conversion by 5-10%.

### How to Frame the Exchange

- Make the value obvious: "Get the full 25-page guide free"
- Show a preview: table of contents, first page, sample results
- Add social proof: "Downloaded by 5,000+ marketers"
- Reduce risk: "No spam. Unsubscribe anytime."

**Form optimization.** Cut every field you will not act on, put the highest-intent field last, use
one visible submit action, and label the button with what arrives rather than what the user does
("Send me the checklist" beats "Submit"). Show inline validation, not a post-submit error page.
The psychology underneath this — Hick's Law, activation energy, regret aversion — is in
`/founder-pipeline:marketing-psychology`.

**Popups.** Trigger on intent (exit, scroll depth past the point the offer becomes relevant), never
on a timer within the first few seconds. Match the offer to the page. One dismissal is permanent
for that session. Mobile interstitials that cover content are a ranking risk as well as a bad
experience — use an inline or bottom-anchored form there instead.

---

## Landing Page & Delivery

### Landing Page Structure

1. **Headline** — Clear benefit: what they'll get and why it matters
2. **Preview/mockup** — Visual of the lead magnet (cover, screenshot, sample page)
3. **What's inside** — 3-5 bullet points of key takeaways
4. **Social proof** — Download count, testimonials, logos
5. **Form** — Minimal fields, clear CTA button
6. **FAQ** — Address hesitations (Is it really free? What format?)

**Building the page**: see `/founder-pipeline:web-site-creator`. **Choosing the words it targets**:
see `/founder-pipeline:web-keyword` — a capture page competing for a phrase nobody searches
collects nothing from organic traffic no matter how well it converts.

### Delivery Methods

| Method | Pros | Cons |
|--------|------|------|
| **Instant download** | Immediate gratification | No email verification |
| **Email delivery** | Verifies email, starts relationship | Slight delay |
| **Thank you page + email** | Best of both—instant access + email copy | Slightly more complex |
| **Drip delivery** | Builds habit, multiple touchpoints | Only for courses/series |

### Thank You Page Optimization

Don't waste the thank you page. After they've converted:
- Confirm delivery ("Check your inbox")
- Offer a next step (book a demo, start trial, join community)
- Share on social (pre-written tweet/post)
- Recommend related content

---

## Promotion & Distribution

### Blog CTAs & Content Upgrades

- Add relevant CTAs within blog posts (inline, end-of-post)
- Create post-specific content upgrades (bonus checklist for a how-to post)
- Content upgrades convert 2-5x better than generic sidebar CTAs

### Exit-Intent & Popups

- Trigger on exit intent or scroll depth
- Match the popup offer to the page content
- See the popup rules under **Gating Strategy** above

### Social Media

- Share snippets and teasers from the lead magnet
- Create carousel posts from key points
- Use the lead magnet as the CTA in your bio/profile
- Post the takeaway, not the download link — the value has to be visible before the ask
- Write it in your own voice: `/founder-pipeline:brand-voice`, then
  `/founder-pipeline:humanize`

### Paid Promotion

- Facebook/Instagram lead ads for top-funnel lead magnets
- Google Ads for high-intent lead magnets (templates, tools)
- LinkedIn for B2B lead magnets
- Retarget blog visitors with lead magnet ads
- No paid-campaign skill ships with this plugin. Before spending: set a cost-per-lead ceiling
  derived from what a lead is actually worth to you, run one channel at a time so attribution
  stays readable, and kill anything that has not beaten organic CPL after a fair test window.
  Benchmark CPLs by channel are in [references/benchmarks.md](references/benchmarks.md).

### Partner Co-Promotion

- Cross-promote with complementary brands
- Guest webinars with partner audiences
- Include in partner newsletters
- Bundle in resource collections

---

## Measuring Success

### Key Metrics

| Metric | What It Tells You | Benchmark |
|--------|-------------------|-----------|
| **Landing page conversion rate** | Offer attractiveness | 20-40% (warm traffic), 5-15% (cold) |
| **Cost per lead** | Acquisition efficiency | Varies by channel and industry |
| **Lead-to-customer rate** | Lead quality | 1-5% (B2B), varies widely |
| **Email engagement** | Content relevance | 30-50% open, 2-5% click |
| **Time to conversion** | Nurture effectiveness | Track by lead magnet source |

**For detailed benchmarks by format and industry**: See [references/benchmarks.md](references/benchmarks.md)

### A/B Testing Ideas

- **Headline**: Benefit-focused vs. curiosity-driven
- **Format**: Checklist vs. guide on same topic
- **Gate level**: Full gate vs. partial preview
- **Form fields**: Email-only vs. email + name
- **CTA copy**: "Download Free Guide" vs. "Get Your Copy"
- **Delivery**: Instant download vs. email delivery

### Lead Quality Signals

Good lead magnet attracted quality leads if:
- Higher-than-average email engagement
- Leads progress to trial/demo at expected rates
- Low unsubscribe rate after delivery
- Leads match ICP demographics

---

## Output Format

When creating a lead magnet strategy, provide:

### 1. Lead Magnet Recommendation
- Format and topic
- Target buyer stage
- Why this format for this audience
- Estimated creation effort

### 2. Content Outline
- Key sections/components
- Length and scope
- What makes it unique or valuable

### 3. Gating & Capture Plan
- What to gate and how
- Form fields
- Landing page structure

### 4. Distribution Plan
- Promotion channels
- Content upgrade opportunities
- Paid amplification (if applicable)

### 5. Measurement Plan
- KPIs and targets
- What to A/B test first

---

## Task-Specific Questions

1. What existing content or expertise could you turn into a lead magnet?
2. Where does your audience spend time online?
3. What's the most common question prospects ask before buying?
4. Do you have an email nurture sequence set up for new leads?
5. What's your budget for design and promotion?

---

## Related Skills

Ships with this plugin:

- **/founder-pipeline:marketing-psychology** — why an exchange converts: reciprocity, zero-price
  effect, commitment & consistency, Hick's Law on the form
- **/founder-pipeline:brand-voice** then **/founder-pipeline:humanize** — writing the magnet and
  the capture page in a voice that doesn't read as generated
- **/founder-pipeline:web-site-creator** — building the landing page
- **/founder-pipeline:web-keyword** — deciding what the capture page targets
- **/founder-pipeline:blog-launch** — the posts that carry content upgrades
- **/founder-pipeline:offers** and **/founder-pipeline:pricing** — the paid thing the magnet leads
  toward

Not shipped — handle inline:

- **Interactive tools** (calculators, graders, quizzes). Build one only when you have a repeatable
  input set that produces an output worth the visitor's typing. Gate the *result*, never the tool.
  They take weeks rather than hours, but they rank for "<thing> calculator" queries, segment leads
  by what they entered, and get shared in a way a PDF does not.
- **Nurture sequences.** Deliver the magnet immediately, then 3-5 emails over 10-14 days: one that
  helps them actually use it, one that shows the problem behind the problem, one case or proof,
  one clear ask. Segment by which magnet they took. Anyone who has not opened three in a row comes
  off the sequence.
- **Content strategy.** Pick magnet topics from the questions prospects ask before buying, not
  from a keyword tool alone. One magnet per buyer stage beats five per stage.
- **Analytics.** Track landing-page conversion, cost per lead, lead-to-customer rate and time to
  conversion *per magnet source* — an aggregate number hides the magnet that pulls volume and no
  revenue. The `posthog:*` plugin is one option if you install it separately; any analytics tool
  that can attribute a signup to a source will do.
- **social**: For social media promotion
