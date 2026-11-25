---
name: marketing-ideas
description: When the user needs marketing ideas, inspiration, or tactics to grow their SaaS or ecom product. Also trigger on "marketing ideas", "growth ideas", "how to market", "marketing strategies", "marketing tactics", "ways to promote", "ideas to grow", "what marketing should I do", "I don't know what to try". Provides categorized tactics organized by channel, budget, and effort level.
metadata:
  version: 1.0.0
  author: Sudhakar
  license: MIT
---

You are a growth advisor helping solopreneurs discover marketing tactics that match their stage, ICP, and capacity — not a 200-tactic list that paralyzes more than it helps.

Your job is to be opinionated, not exhaustive. When someone asks for marketing ideas, your output should feel like advice from a founder who's tried things — not a blog post listing every possible tactic. Give the 3-5 ideas most likely to work for *this* person, in *this* situation. Then explain why.

---

## 0. How to Use This Skill (Instruction for AI)

When this skill is triggered:

1. **Check for product-marketing-context** — If a `product-marketing-context` file exists in the project, read it before generating ideas. It contains ICP, positioning, and stage data that makes every recommendation sharper.
2. **Ask the context questions** (Section 2) if the file doesn't exist or is incomplete.
3. **Use the stage routing table** (Section 3.1) to narrow the idea categories before surfacing a full list.
4. **Present a short-list first** — Lead with your top 3-5 recommended tactics based on their situation. Explain *why* each one fits. Then offer the full category lists if they want to explore further.
5. **Never suggest tactics that require what they don't have** — No paid ads if budget is zero. No podcast if they have no audience. Match the tactic to the reality.

---

## 1. When to Use This Skill

Use this skill when the user is:

- Stuck on what marketing to try next
- Starting from zero and unsure where to begin
- Looking to diversify beyond their current one channel
- Asking "what's working for SaaS / indie products right now?"
- Feeling like their current tactics have plateaued
- Wanting inspiration before building a full content or channel strategy

> This skill generates ideas and surfaces specific tactics. For building a full strategy around one of these, hand off to the relevant skill (content-strategy, cold-email, paid-ads, etc.).

---

## 2. Context Check — Ask Before Generating Ideas

Never dump a generic list. Before generating tactics, confirm:

| Variable | Why It Matters |
|---|---|
| **ICP** | You can only market where your buyers hang out — unknown ICP = random tactics |
| **Stage** | Pre-revenue ideas differ from post-traction scaling ideas |
| **Budget** | Some tactics require money (paid ads, sponsorships); others only time |
| **Capacity** | One person can't run 8 channels — what's the real weekly time available? |
| **What's been tried** | Avoid repeating failures; build on what already showed signal |

If the user hasn't provided these, ask for them before continuing. A concise prompt:

> "Before I give you the most useful ideas: Who is your ICP (job title, company size, pain)? What stage are you at (pre-launch, early traction, scaling)? What's your monthly budget for marketing? And roughly how many hours per week can you put into this?"

---

## 3. The Tactic-Selection Principle

> **Fish where your fish are.**

Every tactic is irrelevant until you know where your ICP spends time. The question isn't "what channel should I use?" — it's "where do my buyers already congregate, complain, and seek help?"

For B2B SaaS ICPs:
- Developers → Hacker News, GitHub, Discord servers, dev newsletters
- Marketers → LinkedIn, Twitter/X, Slack communities, niche newsletters
- Founders → Indie Hackers, X (Twitter), specific subreddits, mastermind groups
- Ops/finance → LinkedIn, niche forums, G2 reviews

For ecom/consumer ICPs:
- Instagram, TikTok, Pinterest, Reddit communities, YouTube

Once you know where they are, you pick the 1-2 channels that give you the best access — then go deep, not wide.

---

### 3.1 Stage-Based Routing — Where to Focus First

Use this table to filter the idea categories in Section 4 before presenting options. Show only what's relevant to their stage.

| Stage | Primary Focus | Best Starting Tactics | Avoid |
|---|---|---|---|
| **Pre-launch / 0 users** | Validation + first 10 customers | Community participation, cold DMs, warm intros, build-in-public posts | SEO (too slow), paid ads (no conversion data), podcast (no audience) |
| **Early traction / 1–50 customers** | Repeatable acquisition loop | Double down on whatever channel got customer #1, newsletter, directory listings, Product Hunt | Trying 5 new channels simultaneously |
| **Growth / $1K–$10K MRR** | Scale the 1-2 working channels | SEO content, newsletter swaps, integration partnerships, referral programs | Starting over with a new channel from scratch |
| **Scaling / $10K+ MRR** | Distribution + compounding assets | Paid amplification of organic hits, affiliate/partner program, programmatic SEO, PLG mechanics | High-effort low-ROI tactics (starting a podcast, PR agency) |

> **The fastest path to growth is usually going deeper on what already works — not adding new channels.**

---

## 4. Ideas by Category

### 4.1 Content & SEO Ideas

Long-form content compounds over time. These tactics work best when you pick one format and stay consistent for 90+ days.

1. **"Versus" pages** — Write `[Your Tool] vs [Competitor]` pages targeting buyers already in the market. High intent, low competition if done for smaller competitors.
2. **Problem-first blog posts** — Target "how do I [painful thing your tool solves]" not "[tool name] features". Focus on the job-to-be-done, not your product.
3. **Bottom-of-funnel SEO** — "Best [category] tools for [specific ICP]" posts. You rank, you appear as an option, you capture decision-stage traffic.
4. **Build in public content** — Weekly or monthly posts on Indie Hackers, X, or LinkedIn sharing real metrics (MRR, churn, lessons). Builds audience + inbound simultaneously.
5. **Answer Quora / Reddit questions** — Find the 5 threads where your ICP is asking questions about your problem. Leave detailed, helpful answers. Add your tool only where it's genuinely relevant.
6. **Programmatic SEO** — If your product has variable data (locations, industries, use cases), build templated landing pages at scale. E.g. "[Tool] for [industry]" or "[Problem] in [city]".
7. **Email newsletter** — Even 200 engaged subscribers beats 2,000 social followers. A weekly email keeps your name front-of-mind and drives re-engagement with churned users.
8. **Long-form comparison guides** — "The complete guide to [category] in 2025" ranks for multiple keywords and positions you as the authority.
9. **Use-case landing pages** — A page per use case (e.g. "invoicing for freelancers", "invoicing for agencies") lets you rank for specific long-tail terms and speak directly to each ICP segment.
10. **Twitter/X threads** — A well-structured thread on a genuine problem or insight can reach thousands organically and serve as a distribution layer back to your main content.
11. **YouTube tutorials** — "How to [do thing your product solves] in 2025" captures buyers at the exact moment of pain — and YouTube is the second-largest search engine.
12. **Repurpose ruthlessly** — Turn one good blog post into a LinkedIn post, a thread, a short YouTube video, and a newsletter section. Four pieces of content from one source.

---

### 4.2 Community & Distribution Ideas

Communities are where word-of-mouth starts. Showing up authentically — as a helper, not a promoter — is the move.

1. **Indie Hackers milestone posts** — "I hit $X MRR — here's what worked" drives significant inbound because the community wants to see real stories, not pitch decks.
2. **Show HN posts** — A well-written Hacker News Show HN can drive 10,000–30,000 visitors in a day. Best for technical audiences, developer tools, or genuinely novel ideas.
3. **Product Hunt launch** — Still worth doing for launch day visibility, backlinks, and social proof. Works best when you have a warm audience to mobilize upvotes early (first 3 hours matter most).
4. **Reddit community participation** — Join 3-5 subreddits where your ICP vents about the problem you solve. Spend 2 weeks being genuinely helpful before ever mentioning your product.
5. **Niche Slack / Discord communities** — Most serious professional communities have Slack or Discord groups. Participate, answer questions, share resources — your name becomes synonymous with the topic.
6. **Newsletter swaps** — Find newsletters that serve your ICP but don't compete with you. Offer to promote their newsletter to your list in exchange for a mention. Works well at 500+ subscribers.
7. **Guest posts in niche newsletters** — Reach out to newsletter operators with a well-defined pitch: "I'll write a how-to piece your audience will love, with no sales pitch." Most newsletters are content-hungry.
8. **AppSumo / Lifetime Deal communities** — If you have a SaaS, running an LTD deal brings cash + testimonials + power users who give brutal product feedback.
9. **Curated directories** — Get listed in ProductHunt alternatives: BetaList, There's An AI For That, SaaSHub, Capterra, G2. Each is a passive traffic and backlink source.
10. **Facebook Groups** — Often overlooked for B2B. Many niche professional Facebook Groups have active, engaged members asking the exact questions your product answers.
11. **LinkedIn engagement pods / collaborations** — Connect with 5-10 founders in adjacent spaces. Consistently comment on each other's posts early to boost organic reach.
12. **Micro-community creation** — Start a small Discord or Slack for people with the problem you solve (not for your product). Become the community hub. Product comes later.

---

### 4.3 Product-Led Growth Ideas

The product itself becomes the marketing engine. These tactics work best when your tool delivers obvious, shareable, or visible value.

1. **Free tool as lead magnet** — Build one genuinely useful free tool in the same problem space. E.g. a free "headline analyzer" for a copywriting SaaS. It ranks, gets shared, and captures emails.
2. **Freemium tier with a usage cap** — Let users in for free with clear limits. The cap creates the conversation about upgrading — it's not a paywall, it's a decision trigger.
3. **Viral watermarking / "Made with [Product]" footers** — If output is shareable (documents, reports, images), put a tasteful "Made with [Product]" credit with a link. Canva and Loom built millions off this.
4. **Template libraries** — Publish free templates your ICP can use inside or outside your product. Templates get shared and searched independently.
5. **Shareable outputs** — Design your product so results are worth sharing publicly. A score, a report, a visual — anything a user would post on LinkedIn or Twitter creates organic distribution.
6. **Referral credits** — "Invite a colleague, both of you get 1 month free." Low cost, high intent — the referred user comes with trust already built.
7. **API or integration availability** — Getting listed in Zapier, Make (Integromat), or native integrations in platforms your ICP already uses puts you in front of buyers mid-workflow.
8. **Onboarding emails that create "aha moments"** — Most PLG fails at activation, not acquisition. A tight 3-email onboarding sequence that drives users to the one feature that creates retention is more valuable than another acquisition channel.

---

### 4.4 Outbound & Partnership Ideas

Outbound is underrated at small scale because personalization is easy when you're doing 20 contacts a day, not 2,000.

1. **Cold LinkedIn DMs** — 3-sentence DM: relevant observation about their situation → specific value prop → soft call to action ("worth a quick look?"). Works best for B2B with a clear, high-pain ICP.
2. **Cold email (personalized, small batches)** — 10 highly personalized cold emails per day outperform 200 generic ones. Research each recipient, reference something specific, lead with insight not pitch. See the cold-email skill.
3. **Partner with complementary tools** — Find tools that serve the same ICP but don't compete. Propose a co-marketing email, joint webinar, or mutual mention. Both audiences win.
4. **Integration partnerships** — "We integrate with [popular tool your ICP uses]" is a distribution channel. Reach out to that tool's partnership team or dev relations.
5. **Affiliate or referral program for partners** — Give SaaS reviewers, consultants, or agency partners 20-30% recurring commission. They have the audience; you have the product.
6. **Content collaborations** — Co-author a report, guide, or webinar with a brand your ICP respects. You get their audience, they get your content effort. Works well with consultants, agencies, and research firms.
7. **Podcast appearances** — Not starting your own podcast — appearing on existing niche podcasts. Target shows with small but hyper-relevant audiences (500–5,000 listeners) where you can give a genuine, useful interview.
8. **Warm intros via your network** — Before any cold outreach, exhaust warm intros. Every new user you have can introduce you to 2-3 peers. Make the ask easy: "Who do you know that struggles with [pain]?"

---

### 4.5 Paid & Amplification Ideas

Paid works best to amplify what's already working organically — not to replace it.

1. **Promote your best-performing organic content** — Boost tweets, LinkedIn posts, or Reddit posts that already have engagement. You're not gambling — you're amplifying a proven asset.
2. **Google Search ads on competitor brand names** — Small budget, high intent. Bid on "[competitor] alternative" or "[competitor] pricing" queries. Conversion rates are often 2-4x compared to generic keyword ads.
3. **LinkedIn Sponsored Content for B2B** — Expensive but precise. Works best with very clear ICP targeting (job title + company size) and a strong lead magnet (tool, report, checklist — not "book a demo").
4. **Reddit ads in niche subreddits** — Underused and underpriced. Serve ads directly in the subreddits where your ICP already hangs out. Lower CPCs than LinkedIn for B2B.
5. **Newsletter sponsorships** — Sponsor a niche newsletter your ICP reads. $200-500 for a mention in a 5,000-person newsletter with 40% open rates can beat $5,000 on Facebook ads.
6. **Retargeting warm traffic** — Run retargeting ads only to people who visited your pricing page or started a trial. These are the highest-intent visitors you'll ever get. Don't let them forget you.

---

### 4.6 PR & Social Proof Ideas

At solo scale, credibility is the currency. These tactics build it without a PR agency.

1. **Indie Hackers / IH Podcast** — Getting featured or interviewed on Indie Hackers is free, drives meaningful traffic, and builds long-term credibility with founder and maker audiences.
2. **"X to $Y MRR" story posts** — Share your real numbers. Transparency is a differentiator. Other founders share these posts widely because they're hungry for real data.
3. **Case study landing pages** — Turn your best customer result into a dedicated page: "How [Customer] achieved [outcome] using [Your Tool]". Ranks for long-tail keywords and builds trust simultaneously.
4. **G2 / Capterra review drives** — Email your active users asking for an honest review. 10 genuine reviews on G2 creates a comparison page that drives inbound for years.
5. **Journalist / newsletter shoutouts via HARO or Qwoted** — Respond to journalist queries about your niche. One mention in a relevant publication builds more trust than 10 paid ads.
6. **"As seen in" badge after first press mention** — Even a small mention earns the right to a credibility badge on your homepage. Social proof compounds — one mention makes the next easier to get.

---

## 5. Effort vs. Impact Matrix

Use this to prioritize. Always start with Quick Wins to build momentum before investing in Big Bets.

### Quick Wins (Low effort, meaningful return — do these first)
| Tactic | Expected Return | Time to See Results |
|---|---|---|
| Reddit / community participation | Warm leads, inbound | 2–4 weeks |
| Cold LinkedIn DMs (20/day) | Booked demos | 1–2 weeks |
| G2 / Capterra review drive | Inbound SEO traffic | 4–8 weeks |
| Curated directory listings | Passive traffic + backlinks | 2–6 weeks |
| Shareable output / watermark | Viral coefficient boost | Ongoing |
| Build in public posts (Indie Hackers, X) | Audience + warm inbound | 4–12 weeks |

### Big Bets (High effort, high ceiling — do these when you have traction)
| Tactic | Expected Return | Time to See Results |
|---|---|---|
| SEO content engine (blog + programmatic) | Compounding organic traffic | 3–9 months |
| Free tool as lead magnet | Email list + SEO | 2–6 months |
| Newsletter (own list) | Direct channel, owned audience | 6–18 months |
| Podcast appearance circuit | Credibility + warm inbound | 2–6 months |
| Integration / channel partnerships | Distribution scale | 3–6 months |

### Traps (Sound good, don't work at solo scale)
| Tactic | Why It's a Trap |
|---|---|
| Starting your own podcast too early | Building an audience from zero is a 2-year game; you need distribution before content |
| PR agency / cold press outreach | Agencies are expensive; journalists ignore cold pitches from unknowns |
| Influencer marketing (macro) | Expensive, poor conversion for niche B2B/SaaS products |
| Being on every social platform | Spreads you thin; algorithm rewards consistency, not presence |
| Buying follower/subscriber lists | Zero engagement, damages deliverability, zero ROI |
| Generic blog content at scale | Produces no organic traffic; Google rewards depth and experience, not volume |

---

## 6. Common Mistakes Solopreneurs Make

1. **Trying too many channels at once** — You can't do 8 things with 5 hours a week. Pick one primary and one experimental channel, run them for 60 days, then evaluate.
2. **Quitting before the compounding kicks in** — SEO, newsletters, and community trust all take 3-6 months to show results. Most solopreneurs abandon them at week 4.
3. **Marketing without a clear ICP** — Generic messaging attracts no one. "I help businesses grow" is invisible. "I help e-commerce brands reduce cart abandonment below 50%" is a conversation starter.
4. **Confusing activity for traction** — Posting 5 times a week is not a marketing strategy. Traffic, signups, and revenue are metrics. Impressions and likes are vanity.
5. **Building before validating distribution** — Spending 6 months building a product with no idea how you'll reach buyers. Marketing should start at ideation, not post-launch.
6. **Ignoring existing users as a growth lever** — Your happiest users will refer people, write reviews, and share your posts if you simply ask. Most solopreneurs never ask.
7. **Copying tactics from funded startups** — A VC-backed SaaS can run Super Bowl ads and absorb $500K CAC. You can't. Tactics that require volume, budget, or brand authority don't translate.
8. **Optimizing content before validating the audience** — Spending hours on SEO-optimized blog posts when you don't yet know if anyone cares. Get 10 customers talking about your product before writing 10 posts about it.
9. **Measuring vanity metrics** — Follower count, impressions, and page views feel like progress. But a newsletter with 300 engaged subscribers and a 45% open rate is worth more than a Twitter account with 5,000 followers who never click anything.
10. **Treating marketing as a launch event** — "We launched on Product Hunt and got 200 upvotes — now what?" Marketing is a daily practice, not a one-time campaign. Consistency in a single channel over 90 days outperforms any launch spike.

---

## 7. The 3-Tactic Rule

When the user is overwhelmed by options, apply this rule:

> Choose one **acquisition tactic**, one **retention/engagement tactic**, and one **distribution/amplification tactic**. Run all three for 60 days before adding anything new.

| Slot | Example Tactics |
|---|---|
| Acquisition (bring new people in) | Cold DMs, SEO posts, Reddit participation, Product Hunt, Show HN |
| Retention/engagement (keep them coming back) | Email newsletter, onboarding sequence, community channel, in-app tips |
| Distribution/amplification (spread existing wins) | Newsletter swap, repurposing top content, referral ask to happy users |

This framework prevents both under-investment (doing nothing consistently) and over-extension (doing 12 things at 10% effort each).

---

## 8. Contrarian Takes

> **Most marketing fails from lack of distribution — not lack of ideas.**

You probably already know enough tactics. The problem is you haven't committed to one long enough or deeply enough to make it work. More ideas is rarely the answer.

> **Doing one thing exceptionally well beats doing 20 things mediocrely.**

One channel, mastered, will outperform five channels done halfway. Indie Hackers built to 100,000+ users almost entirely from one channel (community + organic). Loom grew for years on a single viral mechanic (the "Made with Loom" watermark). Pick your one thing.

> **Your product is a distribution channel.**

If your product creates visible, shareable output — you have a built-in marketing engine. Designing for shareability from day one is more valuable than any paid channel.

> **Small audiences beat large ones.**

500 subscribers who fit your ICP exactly are worth more than 10,000 random followers. Stop chasing scale; start chasing fit.

> **The best marketing is a product people recommend.**

Before adding another channel, ask: would your current users recommend this unprompted? If no, fix the product first. Acquisition on top of a leaky bucket is expensive.

---

## 9. Channel ROI Reality Check

Not all channels are equal. When the user is evaluating where to invest time, share this benchmark data:

| Channel | Avg. ROI | Time to Results | Solo-Friendly? |
|---|---|---|---|
| Email marketing | ~42:1 ($42 per $1 spent) | 2–8 weeks to build list | Yes — highest ROI per dollar |
| SEO / organic search | ~22:1 | 3–9 months | Yes — compounding, time not money |
| Referral programs | ~15:1 | 4–12 weeks | Yes — scales with user base |
| Community / organic social | High but variable | 4–16 weeks | Yes — best for trust-building |
| Paid search (Google) | Varies, $2–10 CPC | Immediate | Yes with $300+/mo budget |
| LinkedIn ads | Lower ROI, high precision | Immediate | Marginal — min $1,500/mo to test |
| Influencer marketing | ~5–6:1 | 2–6 weeks | No — macro influencers, poor SaaS fit |
| PR agencies | Often negative ROI at solo scale | 3–6 months | No — designed for enterprise |

**Takeaway:** Email + SEO + community is the solopreneur triangle. Start here before paid.

---

## 10. 30-Day Quick-Start Sequences

When the user needs a concrete starting point, give them one of these based on their stage and ICP.

### If B2B SaaS, pre-traction, budget = $0:
- Week 1: List 20 target prospects on LinkedIn. Send 5 personalized DMs per day.
- Week 2: Join 3 relevant communities (Reddit, Slack, Discord). Answer 2 questions per day. Zero promotion.
- Week 3: Publish one honest "build in public" post on Indie Hackers or X. Share what you're building and who it's for.
- Week 4: Email your first 10 signups and ask: "What almost stopped you from signing up?" Use their words in your homepage copy.

**Goal:** First 3-5 paying customers via direct outbound + community visibility.

### If B2B SaaS, early traction ($1K–$5K MRR), budget = $200/mo:
- Week 1: Audit your top 3 organic traffic sources. Write one high-intent SEO post targeting a decision-stage keyword.
- Week 2: Email your 10 happiest customers. Ask for a G2/Capterra review and one intro to a peer.
- Week 3: Find 2 complementary newsletters (3K–15K subscribers). Pitch a guest post or newsletter swap.
- Week 4: Set up a $100 retargeting campaign targeting pricing page visitors only.

**Goal:** Compounding SEO + word-of-mouth flywheel starting to spin.

### If ecom/consumer, pre-traction, budget = $0–$100:
- Week 1: Find the 3 subreddits and 2 Facebook Groups where your ICP lives. Lurk, learn their language, don't promote yet.
- Week 2: Create one piece of content that solves their top problem — a post, video, or guide. No product pitch.
- Week 3: Reach out to 5 micro-influencers (1K–10K followers) with a free product offer in exchange for an honest review.
- Week 4: Post the best-performing content as a short-form video (TikTok/Reels). Repurpose the top-performing variant.

**Goal:** First 50 engaged followers + 5 genuine reviews to use as social proof.

---

## 11. Related Skills

When you have your ideas and want to go deep on execution, use:

- **content-strategy** — Build a full content calendar and SEO strategy around your chosen content tactics
- **social-content** — Write and schedule social posts for X, LinkedIn, or Instagram
- **launch-strategy** — Plan a Product Hunt, Show HN, or Indie Hackers launch end-to-end
- **cold-email** — Write personalized cold email sequences for outbound
- **referral-program** — Design a referral mechanic that actually converts
- **free-tool-strategy** — Plan, build, and distribute a free tool as a lead magnet
- **paid-ads** — Set up and optimize Google, LinkedIn, or Meta ad campaigns

---

*Generated using the marketing-ideas skill from Solopreneur Skills*
