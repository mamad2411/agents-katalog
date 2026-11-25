---
name: competitor-content-spotter
description: |
  Audits competitor content output to reveal positioning gaps, messaging
  vulnerabilities, and audience-capture openings the user can exploit. Use
  when a user asks "what are my competitors publishing", "where are their
  content gaps", "how do I differentiate my content", or "give me a
  competitive content audit". Analyzes published competitor material — for
  category-wide unmet needs use invisible-demand-detector.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="competitor-content-spotter")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly any previously identified competitors, ICA definitions, content pillars, and prior competitive analyses.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Competitors to analyse**: Which 2–5 competitors should we examine? (Provide URLs, brand names, or social handles)
- **Content channels in scope**: Which channels matter most? (e.g., blog/SEO, LinkedIn, YouTube, email newsletter, podcast, X/Twitter, paid ads)
- **ICA definition**: Who is the audience you're competing for? (Role, industry, stage of awareness, primary pain point)
- **Your current content positioning**: What themes, angles, or points of view do you already own? (Share content pillars, a positioning doc, or recent top-performing pieces)
- **Strategic objective**: What decision will this analysis inform? (e.g., new content calendar, repositioning, launch campaign, gap exploitation)

If the user's ICA or competitor set exists in FutureProof context, confirm it rather than re-collecting.

## Step 3: Do the Work — Competitor Content Inventory

For each competitor, build a **Content Inventory Matrix** across the channels in scope:

| Dimension | What to Capture |
|---|---|
| **Publishing cadence** | Frequency per channel, consistency patterns, seasonal spikes |
| **Content formats** | Long-form, short-form, video, carousel, thread, newsletter, gated assets, webinars |
| **Primary themes** | Top 3–5 recurring topics or content pillars |
| **Narrative positioning** | Brand story archetype (challenger, trusted authority, contrarian, educator, community leader) |
| **ICA targeting signals** | Language register, role-specific jargon, pain points addressed, aspiration language used |
| **Engagement signals** | Relative engagement patterns (high-performing vs. average posts, comment sentiment themes) |

Produce one inventory row set per competitor. Flag where data is inferred vs. directly observed.

## Step 4: Do the Work — Messaging & Positioning Deconstruction

For each competitor, deconstruct their content through five lenses:

1. **Value proposition framing** — What transformation do they promise? Is it explicit or buried? How do they articulate before-state → after-state for the ICA?
2. **Authority construction** — What proof assets do they deploy? (Case studies, data, credentials, social proof, borrowed authority, proprietary frameworks)
3. **Objection handling in content** — Which ICA objections does their content pre-emptively address? Which do they ignore or handle poorly?
4. **Point-of-view differentiation** — Do they hold a distinctive, defensible perspective? Or are they echoing category consensus?
5. **Call-to-action architecture** — How do they convert attention to action? (Funnel structure, lead magnets, nurture pathways visible in content)

Score each competitor 1–10 per lens with a one-line justification. Apply any user-specific `instructions` from FutureProof context to weight dimensions by strategic priority.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Do the Work — Gap & Opportunity Mapping

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Cross-reference the competitor inventory against the user's own positioning to produce three artefacts:

### 5a. Content Gap Matrix

A grid mapping **ICA pain points / questions** (rows) against **competitors + user** (columns), marking coverage as:
- ✅ Well-covered (depth + frequency)
- 🟡 Surface-level (mentioned but not authoritative)
- ❌ Absent

Highlight cells where **all competitors show ❌ or 🟡** — these are exploitable white-space opportunities.

### 5b. Messaging Vulnerability Register

Identify 3–5 specific weaknesses in competitor content positioning:
- **Vulnerability**: precise description of the gap or flaw
- **Evidence**: specific content examples demonstrating it
- **Exploitation angle**: how the user can create content that directly capitalises on this weakness
- **ICA resonance potential**: why the ICA would care (tied to their pain points or aspirations)

### 5c. Competitive Attention Map

Categorise the competitive content landscape into four quadrants:

| | Low Competitor Saturation | High Competitor Saturation |
|---|---|---|
| **High ICA Demand** | 🏆 Priority capture zones | ⚔️ Battleground — win on depth, POV, or format |
| **Low ICA Demand** | 🔍 Monitor / emerging | 🚫 Avoid — low ROI |

Place each major topic/theme into the appropriate quadrant with rationale.

## Step 6: Deliver Output

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


Produce a **Competitor Content Intelligence Brief** containing:

1. **Executive Summary** (200 words max): Key competitive dynamics, the single most important finding, and recommended strategic posture (attack, differentiate, or dominate)
2. **Competitor Scorecards**: One per competitor — the five-lens scores from Step 4 with narrative summary
3. **Content Gap Matrix**: From Step 5a
4. **Messaging Vulnerability Register**: From Step 5b — the 3–5 vulnerabilities with exploitation playbooks
5. **Competitive Attention Map**: From Step 5c — quadrant placement with priority ranking
6. **Recommended Content Moves**: A prioritised list of 5–7 specific content pieces or series the user should create, each specifying:
   - Topic and angle (not generic — a specific headline-ready framing)
   - Target channel and format
   - Which gap or vulnerability it exploits
   - Expected ICA response (what shift in perception or behaviour it drives)
7. **Watch List**: Competitor signals to monitor going forward (emerging themes, format experiments, positioning shifts detected)

Format as a structured document suitable for sharing with a content strategy team or marketing leadership.

## Step 7: Propose Experiments

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:save_experiment(skill="competitor-content-spotter", experiment={
  hypothesis: "Publishing authoritative content in the top-priority white-space gap will capture ICA attention with lower competition and higher engagement than battleground topics",
  variants: [
    "control: next 4 content pieces follow current editorial calendar",
    "variant: next 4 content pieces target the #1 and #2 white-space gaps identified in the Content Gap Matrix"
  ],
  measurement: "Engagement rate (comments, saves, shares), inbound lead attribution, and search ranking movement over 30 days",
  expected_impact: "25–40% higher engagement rate on white-space content vs. battleground content, with measurable organic search gains within 60 days"
})
```

## Step 8: Request Research

```
FutureProof:request_research(skill="competitor-content-spotter",
  query="Emerging content formats and distribution channel shifts in [user's industry/niche] 2024–2025, with competitive benchmarking data on content engagement by format and platform",
  reason="Ensure competitive analysis accounts for channel migration trends and format innovation that could invalidate current competitor advantages or create new positioning opportunities"
)
```

## Step 9: Save Session

```
FutureProof:save_session(skill="competitor-content-spotter", session={
  summary: "...[fact-dense: ICA, format, tone, constraints, what was delivered, amends made. End with: Next session defaults: ...]",
  outcomes: [
    "Format: [format chosen]",
    "Tone: [tone and constraints]",
    "ICA: [ICA description]",
    "Deliverable: [what was produced]"
  ],
  metadata: {}
})
```