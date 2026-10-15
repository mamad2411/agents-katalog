---
name: headline-virality-scorer
description: "Score and rank headlines, news titles, article titles, blog titles, or website titles — in ANY niche (tech, business, fitness, food, finance, lifestyle, education, entertainment, and more) — for content-creation potential: how viral they could go, how strongly they attach to people's existing sentiment, and how relevant they are to the creator's niche. Produces per-platform scores (X, LinkedIn, YouTube, Instagram), visible sub-scores, a ranked ordering, and hook suggestions for the top picks. USE THIS SKILL whenever the user pastes one or many headlines/titles and wants them scored, rated, ranked, triaged, or prioritized for what to post/make content about — even if they just say 'which of these is worth posting?', 'rate this headline', 'score these for virality', or 'what should I make a video/thread about?'. Also use when the user wants to decide what news or topics to cover on Twitter/X, LinkedIn, YouTube, or Instagram."
---

# Headline Virality Scorer

Score headlines for **content-creation potential**: given a title, judge how much traction a creator could get by making content about it, and on which platform. Works for **any niche** — tech, business, fitness, food, finance, lifestyle, education, entertainment, and beyond. This is a decision tool — the output should make it obvious what's worth posting and where.

## When this triggers

The user hands over one headline or a batch (news, blog, article, or website titles) and wants them scored/ranked for virality, sentiment pull, or relevance — usually to decide what to post or make a video/thread about. The headlines usually already sit inside the creator's niche, so the job is discriminating *between* them for content potential, not confirming the topic fits. If the user states a niche, score against it; otherwise score broad resonance for a general audience.

## Input handling

- **Required:** the title(s). Accept a single title or a list.
- **Optional (use if given, don't ask for it):** source/publication, a one-line snippet, publish date, and the user's **niche/audience**.
- **Niche:** if the user states a niche (e.g. "I make content for backend engineers," "my audience is home cooks," "I coach amateur runners"), score **relevancy** against that niche. If no niche is given, score relevancy as **broad general-audience resonance**.
- **Batch mode is the default workflow.** When given multiple titles, score each, then present them **ranked best-to-worst** so the winners surface at the top.
- **No web lookups by default.** Score from the headline's intrinsic properties. Searching every item in a large batch is slow and usually unnecessary. If a score genuinely hinges on recency or context you don't have (e.g. "is this still fresh?"), say so in one line rather than guessing — don't silently assume.

## The scoring model

Every headline gets three **sub-scores (0–100)**, which then combine into **four platform scores (0–100)**.

### Sub-score 1 — Virality

How much the *headline itself* makes someone stop, react, and share. Score by counting how many of these levers it pulls, and how hard:

- **Curiosity gap** — opens a loop the reader needs closed ("Nobody is talking about what GPT-6 actually broke").
- **Contrarian / counterintuitive** — challenges a held belief ("Microservices were a mistake").
- **Identity & tribe signal** — flags an in-group ("If you've ever fought a flaky test, you know").
- **Practical utility** — promises a concrete, usable win ("7 git commands that saved my job").
- **Emotional charge** — awe, outrage, fear, delight, FOMO, schadenfreude.
- **Timeliness** — newsjacks a live moment (a fresh launch, outage, drama).
- **Specificity** — real numbers, named products/people, concrete stakes. Vague = weak.
- **Magnitude / stakes** — "this changes everything" energy, backed by something real.
- **Aspiration / status** — success, money, freedom, elite skill.

A headline pulling 1–2 levers weakly is ~20–40. Several levers, hard = 80+.

### Sub-score 2 — Sentiment pull

How strongly the headline **plugs into feelings people already carry** before they read it. Viral content rarely creates emotion from scratch — it taps a pre-loaded current. Every niche has its own raw nerves: job/automation anxiety, status and FOMO, tribal loyalties, distrust of incumbents, hype-cycle excitement, nostalgia, outrage, aspiration, or genuine wonder. (For a tech audience that's AI-job anxiety, framework fatigue, big-tech distrust; for fitness it's body-image and "am I doing this wrong"; for finance it's greed and recession dread — identify the currents that run under *this* niche.) High sentiment pull = the headline lands on a nerve that's already raw. Neutral, purely informational titles score low here even if factually interesting.

### Sub-score 3 — Relevancy

Fit for the audience. If a niche was given, score against it (a marathon-taper headline is a 90 for a running niche, ~20 for a home-baking niche; a Kubernetes headline is a 90 for DevOps, ~25 for no-code founders). With no niche, score broad general-audience resonance — how many viewers would care at all.

### Platform scores

The same headline performs differently per platform because each rewards different levers. Blend the sub-scores using these as a **steer, not rigid math** — apply judgment and the platform notes:

| Platform | Virality | Sentiment | Relevancy | Rewards | Penalizes |
|---|---|---|---|---|---|
| **X** | 0.50 | 0.30 | 0.20 | Speed, hot takes, contrarianism, insider drama, breaking news | Slow evergreen explainers, corporate tone |
| **LinkedIn** | 0.35 | 0.30 | 0.35 | Career/business implications, "what this means for you", lessons, aspiration | Memes, pure drama, edgelord takes |
| **YouTube** | 0.40 | 0.25 | 0.35 | Curiosity gap, tutorials, "X explained", big claims that sustain a watch, evergreen value | Ephemeral micro-news with no depth |
| **Instagram** | 0.35 | 0.45 | 0.20 | Broad "wow", relatable, emotional, visually promising, low-jargon | Deep-technical/insider headlines with no broad hook |

Notes that override the weights:

- **Timeliness** boosts X most, Instagram least; **evergreen value** boosts YouTube most.
- **Deep-technical / insider** headlines: boost X and LinkedIn relevance for technical niches, but cap Instagram unless there's a broad emotional or "wow" angle.
- **LinkedIn**: reframe-ability toward career/business lifts the score even when raw virality is modest.

## Calibration anchors

Keep scores consistent across runs by anchoring to these (assume no niche → broad resonance). The examples span niches on purpose — the *pattern* transfers; recalibrate the wording to the creator's own niche:

- **~90** — "Why I quit my $500K FAANG job to go farm" (contrarian + identity + emotional + aspirational; huge sentiment pull).
- **~88** — "The best-selling protein powder is quietly making you worse" (timely + named + drama + health-anxiety current).
- **~72** — "10 pantry swaps that cut my grocery bill in half" (strong utility + list specificity; broad; low emotional depth).
- **~55** — "The new tax rule that changes how freelancers file" (timely + relevant, but dry; sentiment only if framed around dread).
- **~45** — "Understanding the difference between a Roth and a traditional IRA" (evergreen utility for a personal-finance niche; no hook, no emotion).
- **~28** — "Our team migrated a billing service to Kubernetes" (no curiosity gap, no stakes, no emotion; niche-internal).

Resist score inflation. Most real-world headlines are mediocre — a batch should have real spread, not everything in the 70s. If everything looks high, you're grading too generously.

## Output format

### Batch (default)

1. **Ranked table**, best overall first. Columns: Rank | Headline (truncated) | Best platform | X | LinkedIn | YouTube | Instagram.
2. **Top 3 detail** — for each of the top 3 only, add: the three sub-scores, a one-line "why", and a **hook suggestion** (a concrete opening line / title angle the creator could actually use, tuned to the best platform).
3. **JSON block** at the end (see schema) so an agent/pipeline can consume it.

### Single headline

Skip the table. Give: the three sub-scores, the four platform scores, best-platform verdict, a one-line "why", a hook suggestion, then the JSON object for that one headline.

### JSON schema

Always end with a fenced ```json block. One object per headline:

```json
{
  "results": [
    {
      "headline": "string",
      "sub_scores": { "virality": 0, "sentiment_pull": 0, "relevancy": 0 },
      "platform_scores": { "x": 0, "linkedin": 0, "youtube": 0, "instagram": 0 },
      "best_platform": "x | linkedin | youtube | instagram",
      "why": "one-line rationale",
      "hook": "suggested hook — present for top 3 (batch) or always (single), else null"
    }
  ]
}
```

## Consistency rules

- Score the headline in front of you, not the topic in the abstract — wording is most of virality. "Kubernetes migration" phrased as a war story scores far above the dry version.
- Never inflate relevancy to "it's in the niche so it's relevant" — discriminate.
- Sentiment pull measures *pre-existing* feeling the headline taps, not how you feel about it.
- Keep rationales to one line. The scores and hooks are the product; don't pad.
- If input context is thin and a score depends on missing info (recency, niche), note it in one line rather than silently assuming.
