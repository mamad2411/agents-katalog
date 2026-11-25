---
name: market-intelligence
description: Run live web market, competitor, and Voice-of-Customer (VoC) analysis with the Organic Fit Gate so market trends are never forced. Sub-skill: load only when routed from the hook-everything entry skill, not for general writing or editing.
---
# Live Market Intelligence & The Organic Fit Gate

Hooks fail in two opposite ways:
1. **Vacuum Writing** happens when the writer ignores what is actually happening in the market today, repeating outdated advice or promises that 10 competitors already commoditized two years ago.
2. **Forced Trend-Jacking ("Cringe News-Pegging")** happens when the writer shoehorns a trending news story or macro buzzword into a piece where it has zero causal relevance (`"Just like [Trending Event], your database needs..."`), immediately triggering **Persuasion Knowledge** (Friestad & Wright 1994) and making the piece feel cheap.

Use this skill to mine high-signal market reality via web search and apply the **Organic Fit Gate** so market context is only included when it strengthens the hook naturally.

---

## Phase 1 - The 4-Layer Live Market Scan (When Search Tools Are Available)

Before drafting a campaign, landing page, or industry article, run targeted web searches across these 4 layers:

### Layer 1: 2-to-4 Star Verbatim Voice-of-Customer (VoC) Mining
- **Why 2-to-4 Star Reviews Matter** 5-star reviews are generic praise (`"Great app"`) and 1-star reviews are often billing or support rage. **2-to-4 star reviews**, GitHub issues, Reddit threads, and Hacker News comments contain the exact **functional trade-offs** (`"I love feature X, but every time I export more than 500 rows, the CSV encoding breaks"`).
- **Action Step** Harvest 3 to 5 verbatim phrases and exact workflow complaints used by real practitioners in the last 6-12 months. Use their exact nouns and verbs in your hook instead of marketing terminology.

### Layer 2: Competitor Promise Cluster & Blind-Spot Matrix
- **Action Step** Scan the top 3-5 alternatives in the space and write down their hero headlines.
- **Identify the Promise Cluster** Usually, 80% of competitors cluster on the exact same adjective (`"The fastest AI-powered X"`).
- **Find the Orthogonal Wedge** Position your hook on the concrete operational pain that the cluster ignores or causes (e.g., if every competitor promises `"1-click AI generation"`, position on `"Zero-hallucination deterministic diffs you don't have to spend 40 minutes debugging"`).

### Layer 3: Pricing, Packaging & Lock-In Friction
- **Action Step** Check how incumbents currently gate features (e.g., SSO tax, per-seat minimums, hidden overage fees, export lock-in).
- **Application** Turn the industry's most resented pricing or packaging friction into your **Costly Signal / Trust Damper** (`"No seat minimums, and SAML SSO is included on the base tier"`).

### Layer 4: Structural Tailwinds & Newly Broken Workarounds
- **Action Step** Identify what changed recently (an OS update, a browser policy change, an API deprecation, a cloud pricing change, or a new compliance rule) that broke the old manual workaround.
- **Application** Use this concrete change as the **Why Now** anchor of your hook.

---

## Phase 2 - The Organic Fit Gate (Strict Anti-Shoehorning Filter)

**NEVER force a market trend, news event, or statistic into a piece just to show you searched the web.** Before including any external market signal in your draft, it must pass all **4 gates** below. If it fails even one gate, **discard the trend completely** and use a timeless operational or narrative hook instead.

| Gate | Question to Ask | Pass Condition | Fail Condition (DROP IT) |
|---|---|---|---|
| **1. Causal Relevance Gate** | Does this market shift *directly cause, worsen, or solve* the specific problem the user is here for? | E.g., Citing Chrome's third-party cookie deprecation in a post about server-side attribution. | E.g., Mentioning a trending sports event, celebrity, or unrelated AI model release as a metaphor for accounting software. |
| **2. Zero-Explanation Gate** | Can the reader grasp the connection in `< 1 sentence` without you having to explain why the trend relates to the topic? | Connection is self-evident to anyone in the target audience. | Needs 2 sentences of transitional gymnastics (`"You might be wondering what X has to do with Y..."`) to bridge the gap. |
| **3. Register & Dignity Gate** | Does referencing this signal match the calm, high-competence voice of a domain peer? | Sounds like a sharp engineer or researcher noting a real constraint. | Sounds like a desperate social media manager chasing algorithm keywords. |
| **4. The "So What?" Deletion Test** | If you delete the trend reference and keep only the core mechanism, does the hook get weaker or stronger? | Deleting it removes a key reason why the old workaround stopped working today. | Deleting it makes the opener tighter and cleaner. (If so, **delete it**.) |

---

## Phase 3 - How to Weave Market Signals Invisibly (When They Pass the Gate)

When a market signal passes all 4 gates, integrate it using **Subordinate Forensic Placement** - never as a loud headline announcement:

- **BAD (Forced News-Peg / AI Slop)**
  > "With the recent explosion of LLM agents in 2026, API rate-limiting has become more crucial than ever for modern enterprises!"
- **GOOD (Invisible Subordinate Placement)**
  > "Once our customers started pointing automated coding agents at our public API in March, our traffic pattern shifted from steady human clicks to 400-request bursts inside a 200ms window. Our token-bucket rate limiter dropped 18% of legitimate paid webhooks before we switched to a sliding-window counter."

### Rules for Natural Market Integration
1. **Skip news-peg openers** such as `"With the recent..."`, `"In light of recent..."`, or `"As the market shifts toward..."`.
2. **Translate macro trends into micro symptoms** by naming the exact metric on the user's screen ("AWS charging $0.045 per GB for cross-AZ NAT traffic") instead of abstract macro labels ("cloud cost inflation").
3. **Validate private frustration with public data** so the market finding proves that a bottleneck the reader thought was their own fault is actually a structural shift affecting everyone in their role.
