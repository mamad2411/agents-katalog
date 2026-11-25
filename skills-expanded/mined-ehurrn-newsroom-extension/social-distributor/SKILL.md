---
name: social-distributor
description: "Convert approved articles into platform-optimized social posts. Multi-platform (Facebook, X/Twitter, LinkedIn, Bluesky, Threads). Legally defensible marketing copy—libel exposure is identical to article text. A/B test hooks. Metadata verified."
---

# Social Distributor Skill

## Overview

Social Distributor transforms a published, fact-checked article into **platform-optimized social media posts** that drive traffic while maintaining legal defensibility.

**Critical principle:** Marketing copy is legally liable to the same libel/defamation standards as the article itself. A misleading social hook can expose the newsroom to legal risk even if the article is accurate.

This skill covers:

- **Platform-specific post optimization** (Facebook, X/Twitter, LinkedIn, Bluesky, Threads)
- **Hook generation** (surprising fact, question, local paradox)
- **Character limit optimization** and platform formatting
- **Legal defensibility** (avoid editorializing, motive attribution, unverified claims in the hook)
- **OpenGraph/metadata verification** (social cards display correctly)
- **A/B testing framework** (test 2–3 hooks; measure CTR)
- **Implementation workflow**
- **Common mistakes and red flags**

---

## Platform-Specific Posting Standards

### Facebook

**Audience Profile:**
- General population (all ages, demographics)
- Prefer emotional hooks and storytelling
- Longer engagement (likely to read 3–5 paragraph posts)
- Heavy use of images/video

**Post Format:**

| Element | Specification | Example |
|---|---|---|
| **Hook (first 2 lines)** | 2–3 sentences; emotional appeal; no link in text | "We spent 6 months investigating a hidden problem affecting families in your area. Here's what we found." |
| **Body (context)** | 3–5 sentences; summarize article, tease reveal; no spoilers | "Our team obtained internal documents showing..." |
| **Image** | 1200×628px (16:9 ratio); avoid text overlay; attractive/surprising | High-quality photo from article or custom graphic |
| **Link** | Shortened URL at end (bit.ly, news.co/...) | "Read full investigation: [link]" |
| **CTA (call-to-action)** | "Read more," "Learn what we found," "See the full investigation" (not "Click here") | "Read the full investigation" |
| **Hashtags** | 2–3 relevant (not #fb or platform meta-tags) | #Investigation #LocalNews #YourCity |

**Character Limit:** None (Facebook de-prioritizes longer posts but doesn't truncate)

**Example Post:**
```
We spent 6 months investigating a hidden problem in your community.
We found: [one-sentence revelation].

Our reporters obtained internal documents showing [tease]. Here's what you need to know:
• [Key finding 1]
• [Key finding 2]
• [Call to action: Read full investigation]

Read the full investigation: [link]

#Investigation #LocalNews
```

---

### X (formerly Twitter)

**Audience Profile:**
- News junkies, journalists, engaged readers
- Fast-moving feed; brevity rewarded
- Retweets/shares crucial for reach
- Prefer breaking-news or contrarian angles

**Post Format:**

| Element | Specification | Example |
|---|---|---|
| **Tweet 1 (hook)** | 280 chars max; one headline-like fact; no link | "Breaking: Municipal contracts worth $5M went to single vendor with no competitive bidding." |
| **Tweet 2–3 (thread)** | Build narrative; each tweet <280 chars; link at end | "We obtained city council records showing [detail]. [Link to article]" |
| **Image** | Optional (reduces text character count but increases engagement) | Social card/screenshot |
| **Link format** | Shortened (t.co auto-shortens; use bit.ly for tracking) | Standard news site link |

**Character Limit:** 280 characters per tweet (including spaces, punctuation, links)

**Threading Strategy:**

Tweet 1 (hook):
```
Breaking: Municipal contracts worth $5M went to single vendor with no competitive bidding.
```
(137 chars)

Tweet 2 (data):
```
We obtained city council records revealing the vendor was awarded 47 of 50 contracts since 2020.
No other bidders were solicited.
```
(136 chars)

Tweet 3 (CTA):
```
Full investigation: [link]
```

**Retweet Bait Tips:**
- Lead with surprising number or contradiction
- Use "thread" format (encourages conversation)
- Avoid qualifiers ("may," "might," "allegedly") until evidence presented
- Tag relevant reporters/organizations (not spam)

---

### LinkedIn

**Audience Profile:**
- Professional/business audience
- Longer form acceptable (up to 3,000 chars)
- Prefer data, trends, industry analysis
- Executive decision-makers, policy influencers

**Post Format:**

| Element | Specification | Example |
|---|---|---|
| **Opening hook** | Professional tone; establish credibility/authority | "Our 6-month investigation into municipal procurement reveals systemic bias in contract awards." |
| **Context/problem statement** | 2–3 sentences; why this matters to professionals | "In government, competitive bidding ensures fair resource allocation. When skipped, taxpayers lose." |
| **Data/insight** | 3–5 bullet points; concrete findings | "• 94% of $5M in contracts awarded to one vendor • Zero competitive solicitations • Pattern consistent 2020–2024" |
| **Takeaway** | What should change; policy angle | "Governments must require competitive bidding documentation for all contracts >$50K." |
| **Link** | Full article link | "Read full analysis: [link]" |
| **Image** | Chart, graph, or data visualization (1200×628px) | Bar chart showing vendor concentration |

**Character Limit:** 3,000 characters (includes spaces, line breaks)

**Example Post:**
```
Our 6-month investigation into municipal procurement reveals systemic bias in contract awards.

In government, competitive bidding ensures fair resource allocation. When skipped, taxpayers lose.

Key findings:
• 94% of $5M in contracts awarded to single vendor
• Zero competitive solicitations since 2020
• Pattern identified across 4 fiscal years
• Internal documents show decision-makers did not follow procurement policy

Governments must require competitive bidding documentation for all contracts >$50K. Transparency protects taxpayers.

Read the full analysis: [link]
```

---

### Bluesky

**Audience Profile:**
- Early-adopter tech/media professionals
- Less algorithm-driven (chronological feed)
- Prefer thoughtful, nuanced discussion
- Smaller but engaged audience

**Post Format:**

Similar to X/Twitter but:
- Slightly longer than Tweet (300 chars approx.)
- More room for nuance and qualifiers
- Less "breaking news" expected; more analysis
- Threads encouraged (similar to Twitter)

**Example Post:**
```
We investigated municipal procurement over 6 months. Found: one vendor awarded 47 of 50 contracts worth $5M.

City council records show zero competitive bidding solicited. Either procurement policy wasn't enforced, or it was deliberately circumvented.

Full investigation: [link]
```

---

### Threads (Meta's Twitter Alternative)

**Audience Profile:**
- Overlaps with Facebook (Meta ecosystem)
- Shorter attention span than Bluesky
- Prefer visual posts; threads format encouraged
- Growing but still niche

**Post Format:**

Treat like X/Twitter with Threads-specific features:
- Longer character limit (500 chars per thread post)
- Can build narrative across 10+ connected posts
- Hashtags less important than X
- Video performs well

**Example Thread:**
```
Post 1: "We spent 6 months investigating municipal contracts. What we found should alarm every taxpayer."

Post 2: "One vendor was awarded $5M across 47 contracts since 2020. Competitive bids? Zero."

Post 3: "City council records obtained by our reporters show procurement policy was either unenforced or deliberately bypassed."

Post 4: "The real question: was this negligence or corruption? Read our investigation: [link]"
```

---

## Hook Generation Framework

### Hook Types (with Legal Safeguards)

| Hook Type | Pattern | Example | ⚠️ Legal Risk | ✅ Safe Version |
|---|---|---|---|---|
| **Surprising Stat** | "[Number]% of [X] shows [unexpected pattern]" | "94% of city contracts awarded to one vendor—zero competitive bids." | Low (if stat verified) | Same; fact from article |
| **Question** | "Did [decision-maker] know about [consequence]?" | "Did city council know competitive bidding was being skipped?" | MEDIUM (implies knowledge; avoids "deliberately" but hints at motive) | "City council records show competitive bidding was skipped. Why?" (observable fact, not motive) |
| **Local Paradox** | "[City/org] claims [principle]. Reality: [contradiction]." | "City claims fair procurement. Reality: one vendor got 94% of contracts." | Low (compares claimed vs. actual) | Same |
| **Consequence Angle** | "[X] means [Y impact] for [audience]." | "No competitive bidding means less oversight. Taxpayers lose." | Low (causal reasoning) | Same; state as analysis, not certainty |
| **Human Impact** | "[Group] affected by [finding]" | "5,000 families impacted by hidden water contamination—here's why." | Low (if specific, verifiable) | Confirm number before posting |
| **Investigative Process** | "We obtained [source]; here's what it shows:" | "We obtained 3 years of council records. Procurement is broken." | Low (if source real) | Same; link to source |

### Red-Flag Hook Language (AVOID)

| Phrase | Why It's Risky | Safe Alternative |
|---|---|---|
| "City officials deliberately hid [fact]" | Attributes motive without stating evidence of intent | "City officials did not disclose [fact]" (observable action) |
| "Corruption uncovered" | Legal term; implies criminal intent (defamatory) | "Irregularities found in [specific process]" |
| "Mayor took bribes" | Explicit accusation; defamatory if unproven | "Mayor accepted $X from vendor; no disclosure filed" (observable fact) |
| "Taxpayers defrauded" | Assumes illegal intent; implies crime | "Taxpayers paid more due to [specific failure]" |
| "Cover-up" | Implies intent to hide; requires proof of motive | "Documents were not publicly disclosed" (observable) |
| "Mayor's cronies" | Character attack; not fact-based | "Contracts awarded to former mayor's business partner" (relationship is fact) |

### A/B Testing Framework

Test 2–3 hooks for the same article; measure **click-through rate (CTR)**:

```yaml
article: "Municipal Procurement Investigation"
publish_date: "2025-04-01"
platform: "Facebook"

hook_a:
  text: "We spent 6 months investigating city contracts. What we found is shocking."
  post_date: "2025-04-01 09:00 AM"
  reach: 5420
  clicks: 127
  ctr: "2.3%"

hook_b:
  text: "94% of city contracts went to one vendor. Zero competitive bids. Here's how it happened."
  post_date: "2025-04-01 11:00 AM"
  reach: 6100
  clicks: 289
  ctr: "4.7%"

hook_c:
  text: "Your tax dollars: $5M to one vendor, no questions asked. Our investigation explains why."
  post_date: "2025-04-01 02:00 PM"
  reach: 5900
  clicks: 201
  ctr: "3.4%"

winner: "hook_b"
insights: "Specific data (94%, one vendor) outperforms vague language (shocking, questions asked)"
```

**Repeat:** Repost winning hook to other platforms with format adjustments.

---

## OpenGraph & Metadata Verification

### Social Card Requirements

When article is shared on Facebook, X, LinkedIn, the platform reads **OpenGraph (OG) metadata**:

| OG Tag | Purpose | Specification |
|---|---|---|
| `og:title` | Headline for social card | 50–65 chars; same or variant of article headline |
| `og:description` | Summary for social card | 155–160 chars; compelling hook, not just first paragraph |
| `og:image` | Thumbnail image | 1200×628px (16:9); JPG/PNG; <200KB; unique per article |
| `og:type` | Content type | "article" for news |
| `og:url` | Canonical URL | Full article URL; no tracking parameters in OG tag |

### Verification Checklist

```html
<!-- Example OG tags in article HTML -->
<meta property="og:title" content="Municipal Contracts: One Vendor Received 94% of $5M Awards">
<meta property="og:description" content="Our investigation reveals systemic procurement bias. City council records show zero competitive bidding over 4 years.">
<meta property="og:image" content="https://newsroom.org/images/article-2025-04-01-contracts.jpg">
<meta property="og:url" content="https://newsroom.org/articles/2025-04-01-procurement-investigation.html">
<meta property="og:type" content="article">
```

**Test:** Use Facebook Sharing Debugger (facebook.com/developers/tools/debug) to preview card.

- [ ] og:image renders correctly (not distorted, not placeholder)
- [ ] og:title displays (not truncated)
- [ ] og:description visible (all 155–160 chars shown)
- [ ] og:url links to correct article (no 404)

---

## Character Limit Optimization

### Conversion Chart by Platform

| Platform | Limit | Strategy | Example |
|---|---|---|---|
| **X/Twitter** | 280 chars | Brutal concision; use numbers; thread for context | "94% of $5M contracts to one vendor. Zero competitive bids." (67 chars) |
| **Facebook** | None | 2–3 sentences + link + image (length doesn't matter, but ~200 chars for preview) | "We spent 6 months investigating municipal contracts. One vendor got 94%. We obtained the proof." |
| **LinkedIn** | 3,000 chars | Use full allowance for context, data, analysis | Full paragraph + bullets + insight |
| **Bluesky** | ~300 chars | Slightly more than X; allow nuance | "Our investigation: municipal contracts worth $5M awarded to single vendor. City claims fair procurement. Records show zero competitive bidding." |
| **Threads** | 500 chars per post | Use threads for narrative; each post ~500 chars | 5–10 connected posts, each building story |

**Optimization Rules:**

1. **X/Twitter:** Count every character. Use numerals (94% not "ninety-four percent"). Cut articles ("the," "a"). Abbreviate ("muni" not "municipal").
2. **Facebook:** Assume first 200 chars visible in preview; hook hard, link at end.
3. **LinkedIn:** Use full space; data + insight beats brevity.
4. **Bluesky/Threads:** Treat like X but add 20–40 more characters for nuance.

---

## Libel Safety in Marketing Copy

### Legal Standard: Defamation

A social post is defamatory if it:

1. **Makes a factual claim** (not opinion)
2. **About an identifiable person/entity**
3. **Is false**
4. **Is published** (posted to social media = published)
5. **Causes reputational harm**
6. **Is not protected speech** (opinion, satire, true statement)

**Marketing copy can be defamatory. Your headline can be accurate, but the social hook can be inaccurate or misleading.**

### Safe Phrasing Patterns

| Risky Phrase | Safe Phrase | Why It's Safer |
|---|---|---|
| "Mayor took bribes" | "Mayor received $X from vendor; undisclosed in filings" | States observable facts; avoids criminal accusation |
| "Corruption at city hall" | "City procurement shows irregular spending patterns" | Describes finding; avoids legal-adjacent language |
| "Official lied to public" | "Official's statement contradicts released documents" | Compares claim to evidence; doesn't attribute intent |
| "Embezzlement investigation" | "City treasurer misappropriated $X; investigation ongoing" | Describes action; avoids legal conclusion |
| "Conspiracy uncovered" | "Three officials coordinated decisions affecting vendor selection" | Describes observable behavior; avoids conspiracy accusation |

### Pre-Publication Checklist (before social post)

- [ ] **Claim in hook is in the published article** (no new claims in marketing)
- [ ] **Claim is not opinion** (e.g., "was wrong" is opinion; "contradicts X" is fact)
- [ ] **Claim names identifiable person/entity** (or leaves vague if unverified)
- [ ] **Claim is verified in the article** (cite specific source/quote if challenged)
- [ ] **No hedging language** ("allegedly," "may have," "possibly") that undermines certainty (unless source itself uncertain)
- [ ] **No motive attribution** ("deliberately," "intentionally") without explicit evidence of intent
- [ ] **No inflammatory language** ("liar," "crook," "corrupt") if not legally precise

---

## Implementation Workflow

### Pre-Publication (Before Article Publishes)

1. **Coordinate with copy-review & final-editor-review** (social marketing is part of publication package)
2. **Draft 3 hook options** (send to editor for approval before article goes live)
3. **Prepare OG tags** (og:image, og:description) and verify
4. **Prepare image assets** (1200×628px social card)
5. **Test OpenGraph** (use Facebook Sharing Debugger, Twitter Card Validator)

### Day 1: Publication

1. **Post hook A** (9:00 AM) to flagship platform (likely Facebook or X)
2. **Measure engagement** for 1–2 hours (see CTR, reach)
3. **Post hook B** (11:00 AM) to test alternative angle
4. **Measure performance** (compare CTR)
5. **Decide winning hook** for replication on other platforms

### Day 2–3: Cross-Platform

6. **Repost winning hook** to all platforms (adjusted for character limits):
   - X/Twitter version (280 chars)
   - LinkedIn version (3,000 chars; more context)
   - Bluesky version (300 chars; nuanced)
   - Threads version (build as 5–10 post thread)

7. **Tag relevant accounts** (journalists, organizations, decision-makers mentioned in article—sparingly, not spam)
8. **Engage with replies** (respond to comments; answer reader questions; cite article for fact-checks)

### Ongoing: Repromote

9. **Week 1:** Repost hook to different audiences (e.g., if originally morning, post evening)
10. **Month 1:** Every 1–2 weeks, repost to new followers (they didn't see original)
11. **On anniversary:** Repost article annually; update hook if new related story breaks

---

## Common Mistakes & Red Flags

### Hook Writing Mistakes

| Mistake | Why It's Bad | Fix |
|---|---|---|
| **New claim in hook not in article** | Defamatory if false; readers click expecting to see evidence they won't find | Every social claim must appear verbatim (or close paraphrase) in published article |
| **Clickbait headline** ("This One Trick Will Shock You") | Low-quality audiences click; high bounce rate; undermines credibility | Use specific fact from article as hook; avoid hype |
| **Motive attribution** ("Mayor deliberately bypassed procurement to help friend") | Defamatory if motive unproven; states criminal intent | Rephrase: "Mayor bypassed procurement; vendor is campaign donor [cite]" (facts, not motive) |
| **Hedge language** ("Possibly the largest contract award...") | Weakens authority; readers unsure if true; poor CTR | If verified: "Is the largest contract..."; if uncertain, don't post yet |
| **No specific detail** ("City hall in crisis") | Too vague; no reason to click; looks like sensationalism | Add fact: "97% of contracts to one vendor; no competitive bids" |
| **Call-out/tag every person mentioned** | Spam; looks aggressive; may trigger harassment reports | Tag only directly quoted/interviewed sources; max 2–3 tags per post |

### Metadata Mistakes

| Mistake | Why It's Bad | Fix |
|---|---|---|
| **og:image is generic placeholder** | Social card looks low-quality; low CTR; appears lazy | Create unique social card per article; use article photo or custom graphic |
| **og:image is >200KB** | Slow to load; may not display; wasted bandwidth | Compress to <200KB (use TinyPNG); maintain 1200×628px ratio |
| **og:title is click-bait** | Misleads readers; high bounce rate; damages publication credibility | og:title should match or closely reflect article headline |
| **og:description is first paragraph copy-pasted** | Boring; no hook; poor preview | Write compelling og:description (155–160 chars) that entices click |
| **og:url includes tracking parameters** | OG tag should be canonical; may break social caching | Use clean article URL without utm_source, etc. (add tracking to actual posted link separately) |

### A/B Testing Mistakes

| Mistake | Why It's Bad | Fix |
|---|---|---|
| **Only post one hook; declare "winner" based on gut feeling** | No data; subjective; can't replicate success | Always test 2–3 hooks; measure CTR; declare winner after 2 hours |
| **Post all hooks at same time** | Can't isolate which hook performs; confounding variables (time of day) | Stagger hooks by 1–2 hours; control for timing |
| **Test on different platforms** ("Facebook wins, so Twitter loses") | Audiences different; can't compare X hook to Facebook hook | Test different HOOKS on SAME platform; compare apples to apples |
| **Stop after first test; never repeat** | One win ≠ pattern; may have been timing luck | Run 2–3 A/B tests over different weeks; identify pattern |

### Engagement Mistakes

| Mistake | Why It's Bad | Fix |
|---|---|---|
| **Ignore comments/replies** | Readers feel unheard; damages relationship; looks dismissive | Reply to first 10–20 substantive comments; thank shares |
| **Argue with critics in replies** | Escalates conflict; looks unprofessional; algorithm downranks | Reply once (factually); don't continue debate |
| **Promote without fact-checking replies** | Comments may contain misinformation; newsroom doesn't correct | Pin your comment with fact-check if significant inaccuracy in top reply |
| **Repost at same time every day** | Algorithm learns pattern; deprioritizes | Vary posting time; post when audience is most active (use platform analytics) |

---

## Legal Defensibility Checklist

Before posting **any** social hook:

- [ ] **Claim appears in published article** (exact quote or close paraphrase)
- [ ] **Source is cited in article** (primary document, named source, or both)
- [ ] **Claim is factual** (not opinion; "was" not "was wrong")
- [ ] **No motive attribution** ("deliberately," "intentionally," "conspired") without explicit evidence
- [ ] **No character attack language** ("liar," "crook," "corrupt") unless legally precise (convicted felon, etc.)
- [ ] **Hedging language removed** (if claim is confident in article, be confident in post)
- [ ] **Identifiable person/entity** (if claiming wrongdoing, name them; if unverified, attribute or leave vague)
- [ ] **OpenGraph metadata verified** (og:image displays, og:description compelling, og:url works)
- [ ] **No affiliate links or paywall tricks** (link goes to free version of article if applicable)

---

## Escalation

If a social post receives **cease-and-desist** or legal threat:

1. **Take post down immediately** (while review happens)
2. **Screenshot** the post and threat (preserve evidence)
3. **Alert legal/editor** with link to threat and full post text
4. **Do NOT** engage with threatening account or reply to threat
5. **Do NOT** re-post or defend on social
6. Let newsroom's legal team handle response

---

## Platform-Specific Best Practices Summary

| Platform | Best for | Max Hooks | Posting Frequency | Image Requirement |
|---|---|---|---|---|
| **Facebook** | Emotional, narrative | 3–5 | 1–2x daily | Required (1200×628px) |
| **X/Twitter** | Breaking, timely, threads | 5+ (thread) | 2–4x daily | Optional (helps) |
| **LinkedIn** | Professional, analysis, B2B | 2–3 | 3–5x weekly | Recommended (charts) |
| **Bluesky** | Engaged, early-adopter | 2–3 | 1x daily | Optional |
| **Threads** | Narrative, long-form | 1 (as thread) | 2–3x weekly | Optional (builds engagement) |

