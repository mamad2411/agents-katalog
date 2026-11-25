---
name: ideal-client-generator
description: Generates a research-grounded Ideal Client Handbook with real verbatim Voice of Customer (VOC) quotes from web research, competitive landscape analysis, and deep analysis. Produces a human-readable handbook, a structured ontology with behavioral segments and trigger events, a messaging framework, and an evidence audit with gap report. Use when the user asks to generate an ideal client profile, ideal client analysis, ideal client handbook, or VOC research.
---

Generate a comprehensive, **research-grounded** Ideal Client Handbook. Unlike generic persona generators, this skill mines real Voice of Customer (VOC) data from the web, competitor ecosystems, and user-provided sources, then builds analysis grounded in actual human language.

**Outputs (4 files):**
1. **Handbook** (`.md`) — Human-readable 29-section analysis with VOC citations
2. **Ontology** (`.json`) — Structured entity graph for AI engine schema
3. **Messaging Framework** (`.md`) — Deployable messaging assets derived from VOC
4. **Evidence Audit** (`.md`) — Confidence heat map + gap report with recommended searches

---

## PHASE 0: GATHER INPUTS

Collect all of the following. Ask for everything at once:

### Required
1. **Your Name** — How the analysis should refer to you
2. **Your Purpose** — What is the purpose of your business/service? (2-5 sentences)
3. **Desired Transformation** — What outcome do you wish for your clients?
4. **Business Type** — How would you describe your business/service type?
5. **Preferred Language** — Output language (default: English)

### Research Parameters
6. **Niche Keywords** — 3-5 specific terms your ideal clients would use to describe their problem (e.g., "burnout recovery", "executive coaching", "ADHD entrepreneur")
7. **Competitor Names** — 2-3 competitors or similar businesses whose clients match your ideal client. Include their website URLs if known. (Even if no direct competitors, name businesses serving an adjacent audience.)
8. **Known Communities** (optional) — Specific subreddits, forums, Facebook groups, Slack communities where your ideal clients congregate
9. **User-Provided VOC Data** (optional) — Paste or attach any existing material: interview transcripts, survey responses, testimonials, reviews, support tickets, sales call notes, DMs, comments. The more raw material, the better.

Confirm all inputs back to the user before proceeding.

---

## PHASE 1: DEEP VOC RESEARCH

**This phase is critical.** Before generating any analysis, conduct extensive web research to build a VOC Evidence Bank of real, verbatim quotes from real people. Do NOT skip or abbreviate this phase.

### 1A: Audience VOC Mining

Execute the following searches using `WebSearch` and `firecrawl_search`/`firecrawl_scrape` tools. Run as many in parallel as possible. Aim for **15-25 distinct searches minimum**.

#### 1. Reddit Mining
For each niche keyword, search:
- `site:reddit.com "[niche keyword]" struggling OR frustrated OR afraid OR wish`
- `site:reddit.com "[niche keyword]" "I feel like" OR "I'm so tired of" OR "what worked for me"`
- `site:reddit.com "[niche keyword]" advice OR help OR recommendation`

Scrape the top 3-5 threads per search. Extract verbatim quotes (full sentences/paragraphs, not fragments).

#### 2. Quora Mining
- `site:quora.com "[niche keyword]" why OR how OR struggle`
- `site:quora.com "[business type]" "best advice" OR "biggest mistake"`

#### 3. Review Mining
For each competitor name (if provided):
- `"[competitor name]" review OR testimonial site:trustpilot.com OR site:g2.com`
- `"[competitor name]" review "changed my life" OR "waste of money" OR "game changer"`

For the niche generally:
- `"[business type]" review OR testimonial "I finally" OR "I wish I had"`

#### 4. Forum & Community Mining
- `"[niche keyword]" forum OR community "my experience" OR "my story"`
- Search any user-specified communities directly

#### 5. YouTube Comment Mining
- `site:youtube.com "[niche keyword]"` and scrape comment sections of top results

#### 6. Amazon Book Review Mining
- Search for top books in the niche, scrape 1-star and 5-star reviews (these contain the most VOC-rich language)
- `site:amazon.com "[niche keyword]" book reviews`

#### 7. Social Media Mining
- `site:twitter.com OR site:x.com "[niche keyword]" "I need" OR "I hate" OR "I love"`
- `site:linkedin.com "[niche keyword]" "lessons learned" OR "what I wish"`

#### 8. Podcast & Substack Mining
- `"[niche keyword]" podcast transcript OR episode "I realized" OR "what I learned"`
- `site:substack.com "[niche keyword]" comments OR discussion`
- `"[niche keyword]" podcast interview "the hardest part" OR "what nobody tells you"`
- Search for niche-relevant podcasts on Apple Podcasts / Spotify, then look for transcripts or show-notes pages to scrape

Podcasts are where knowledge entrepreneurs speak at length in their own voice — less filtered than forum posts. Substack comment sections often contain high-quality, reflective VOC from engaged audiences.

#### 9. Industry Report Mining
- `"[niche keyword]" survey OR report OR study 2024 OR 2025 OR 2026 site:mckinsey.com OR site:gartner.com OR site:hubspot.com OR site:statista.com`
- `"[business type]" "state of" report OR survey`
- `"[niche keyword]" market research findings OR trends`

Industry reports provide third-party validation for patterns found in community VOC. Quote specific statistics and findings. Attribute precisely (report title, publisher, date, page/section).

### 1B: Competitive Landscape VOC Mining

**Purpose:** Mine what competitors say TO the audience and what their clients say ABOUT them. This reveals validated pain points, positioning gaps, and transformation language that converts.

For each competitor:

#### Sales Page Analysis
- Scrape their main sales/landing pages using `firecrawl_scrape`
- Extract: headline promises, pain point language, transformation claims, pricing framing, CTAs
- Record the exact language they use — this is what the market has validated with dollars

#### Testimonial Mining
- Scrape competitor testimonial pages, case study pages, and success story sections
- These contain real client language about before/after states
- Record as VOC quotes with source attribution: `"Competitor testimonial: [competitor name]"`

#### Positioning Analysis
For each competitor, capture:
- **Primary promise:** What transformation do they lead with?
- **Pain points they target:** Which fears/frustrations do they address?
- **Pain points they ignore:** What do they NOT address?
- **Tone/voice:** How do they communicate? (Hype-heavy? Academic? Casual?)
- **Pricing model:** How do they frame the investment?

#### Gap Identification
After analyzing all competitors, identify:
- **Shared positioning:** What everyone says (table stakes)
- **Unoccupied territory:** Pain points, desires, or segments nobody is speaking to
- **Language gaps:** Emotional language the audience uses that NO competitor mirrors
- **Trust gaps:** Objections the audience has that no competitor addresses

Record competitive VOC quotes as `[VOC-C###]` (C for competitive source).

### VOC Evidence Bank Construction

After research, compile a **VOC Evidence Bank** — a structured collection of all verbatim quotes found. Present it to the user before proceeding to analysis.

For every quote captured, record:

```
[VOC-###]
Quote: "exact verbatim text"
Source: Platform (Reddit/Quora/Amazon/etc.)
URL: full URL
Date: approximate date if available
Context: 1-sentence description of the thread/post/review context
Author Context: Role/profession, experience level, industry if discernible from the post (e.g., "Executive coach, 10+ years" or "New freelancer, first year"). Write "Unknown" if not determinable.
Theme Tags: [pain_point, fear, desire, objection, transformation, belief, behavior, trigger_event, etc.]
```

Author context is often available from Reddit flair, LinkedIn profiles, Amazon reviewer bios, forum signatures, or self-identification within the post itself ("As a coach of 15 years..."). Capture whatever is available — even partial context (e.g., "Consultant, experience unknown") is more useful than none.

Number each quote sequentially (VOC-001, VOC-002, etc.) so they can be cross-referenced throughout the handbook.

### Integrate User-Provided Data

If the user provided VOC data (transcripts, surveys, etc.), process it identically:
- Extract verbatim quotes
- Tag with `[VOC-U###]` (U for user-provided)
- Apply the same theme tags
- Source attribution: "User-provided: [type of source]"

### Research Summary

After completing research, present to the user:
- Total quotes collected (web-sourced vs. user-provided vs. competitive)
- Top 10 recurring themes/patterns with frequency counts
- Competitive landscape summary (shared positioning + gaps)
- Any surprising findings or contradictions
- Confidence assessment: which areas have strong evidence vs. thin coverage
- Gaps where more user-provided data would strengthen the analysis

**Ask the user to confirm before proceeding to Phase 2.** They may want to add more source material based on gaps identified.

---

## PHASE 2: GROUNDED HANDBOOK GENERATION

Work through each section in order. **Every section must reference specific VOC evidence.** Use the notation `[VOC-###]` inline to cite quotes that support claims.

### Evidence Integration Rules

For every section:
1. **Lead with evidence.** Start with the strongest VOC quotes that illuminate the topic, then build analysis around them.
2. **Tag all claims:**
   - `[EVIDENCED]` — Directly supported by one or more VOC quotes
   - `[PATTERN]` — Inferred from a recurring pattern across multiple quotes
   - `[INFERRED]` — Logical inference from available evidence (state the reasoning)
3. **Never fabricate quotes.** If a section lacks direct VOC evidence, state that explicitly and mark inferences clearly.
4. **Verbatim blocks:** Display key quotes in blockquote format with attribution:
   > "I've been trying to figure this out for years and I just feel stuck."
   > — Reddit r/coaching, 2024-03 [VOC-017]

Begin the document with:
```
================================================================
[NAME]'s IDEAL CLIENT HANDBOOK
Research-Grounded Voice of Customer Analysis
Generated: [date]
VOC Evidence Bank: [X] web-sourced quotes, [Y] user-provided quotes, [Z] competitive quotes
================================================================
```

---

### SECTION 1: OVERVIEW

Generate PURPOSE, DESIRABLE TRANSFORMATION, and MISSION STATEMENT as before — written in first person from [NAME]'s perspective. The mission statement begins with "What I believe."

**Addition:** After the mission statement, add a subsection:

**VOC ALIGNMENT CHECK:** Using the evidence bank, identify 3-5 verbatim quotes from real people that validate the purpose and transformation — real people expressing the need that [NAME]'s business serves. This grounds the mission in market reality.

---

### SECTION 2: DEMOGRAPHICS

Create detailed demographic profile with categories: Approximate Age, Gender, Location, Education Level, Profession, Income Level, Preferred Communication Channels, Buying Habits, Usage Patterns, Worldview, Motivations, Learning Style, Communication Style, Decision Making, Change Orientation, Problem Solving.

**Evidence requirement:** For each category, cite at least one VOC quote that informs or validates the inference. Where demographic data appears in quotes (mentions of age, profession, location, etc.), highlight it.

---

### SECTION 3: PSYCHOGRAPHICS

Categories: Values, Interests, Opinions, Lifestyle, Personality, Motivations, Attitudes, Beliefs, Behavior, Identity.

**Evidence requirement:** This section should be HEAVILY grounded in VOC data. Psychographic claims are exactly what verbatim quotes reveal. Lead each category with 2-3 real quotes, then synthesize.

---

### SECTION 4: HAPPINESS DRIVERS & ROLE MODELS

Happiness Drivers, Role Models, Aspirational Identity.

**Evidence requirement:** Search the VOC bank for quotes about what makes them happy, who they admire, who they want to become. Cite directly.

---

### SECTION 5: COMMUNICATION PREFERENCES

Optimal tone, framing, evidence types that resonate. Include a demonstration of optimal messaging.

**Evidence requirement:** Analyze the LANGUAGE PATTERNS in the VOC bank. What words do they actually use? What tone do the highest-engagement posts use? What framing gets the most upvotes/responses? This section should be a linguistic analysis of actual communication patterns.

---

### SECTION 6: PAIN POINTS

TOP 10 FEARS, TOP 10 FRUSTRATIONS, TOP 10 LIMITING BELIEFS.

**Evidence requirement:** EVERY pain point must cite at least one VOC quote. This is the highest-value section for verbatim data. Rank by frequency of appearance in the evidence bank.

---

### SECTION 7: PAIN POINT STATEMENTS — VERBATIM

**CRITICAL CHANGE FROM ORIGINAL:** Do NOT fabricate statements. Instead, curate the best ACTUAL verbatim quotes from the VOC bank organized into:
- Real statements about fears
- Real statements about frustrations
- Real statements about limiting beliefs

For each, provide the full quote in blockquote format with full attribution. If gaps exist, note them and provide [INFERRED] statements clearly marked.

---

### SECTION 8: RECOMMENDED SOLUTIONS & DESIRABLE OUTCOMES

Solutions the program could offer + specific desirable outcomes.

**Evidence requirement:** Mine the VOC bank for quotes about what people WISHED existed, what finally worked, what they'd pay for. Lead with those quotes.

---

### SECTION 9: TESTIMONIAL & WHAT I REALLY WANT TO SAY

**TESTIMONIAL:** If real testimonials exist in the evidence bank, present those first (attributed). Then synthesize a composite testimonial clearly marked as [COMPOSITE].

**WHAT I REALLY WANT TO SAY:** Mine the VOC bank for the most vulnerable, raw, unfiltered quotes — the ones that got the most emotional engagement. Present real quotes first, then synthesize.

---

### SECTION 10: CLIENT STATEMENTS

WHAT KEEPS ME UP AT NIGHT / WHAT I WANT / I AM COMMITTED.

**Evidence requirement:** For each, present 3-5 real VOC quotes that express this sentiment, then synthesize a composite statement marked as [COMPOSITE].

---

### SECTION 11: OBJECTIONS

Common reasons clients don't purchase, categorized objections, strategies to overcome.

**Evidence requirement:** Search for VOC quotes about price hesitation, skepticism, bad past experiences, comparison shopping. Objections are one of the richest VOC categories — every claim should cite real quotes.

---

### SECTION 12: CLIENT JOURNEY

Touchpoints, moments of influence/uncertainty/friction, experience improvements.

**Evidence requirement:** Map the journey using VOC quotes that describe how people discovered solutions, what made them hesitate, what pushed them to act.

---

### SECTION 13: PERSONALITY ANALYSIS (MYERS-BRIGGS)

Top 3 most likely MBTI types with reasoning.

**Evidence requirement:** Infer types from behavioral and communication patterns visible in the VOC data. Cite specific quotes that demonstrate personality traits. Mark as [PATTERN-BASED INFERENCE].

---

### SECTION 14: ADDITIONAL PERSONALITY ASSESSMENTS

Human Design, Enneagram, DISC, Archetypes.

**Evidence requirement:** Same as above — ground in observable patterns from VOC data. Mark inferences clearly.

---

### SECTION 15: NEEDS

Emotional Needs, Immediate Needs, Unmet Needs.

**Evidence requirement:** Needs are directly expressed in VOC data. Lead with quotes that express needs, then categorize and synthesize.

---

### SECTION 16: FALSE BELIEFS

Identify false beliefs with reasoning about why they believe them.

**Evidence requirement:** Search for quotes that express misconceptions, wrong assumptions, self-limiting logic. These are often the most valuable VOC data points.

---

### SECTION 17: DEAR DIARY

Journal entry from ideal client's perspective.

**ENHANCEMENT:** Construct this as a mosaic of real VOC quotes woven into a narrative. Attribute inline. Where you bridge between quotes, use [NARRATIVE BRIDGE] notation.

---

### SECTION 18: PERSONAL GAPS

Gap analysis across: Motivations, Beliefs, Learning Style, Emotional Intelligence, Stress Response, Communication, Goals.

**Evidence requirement:** Use VOC quotes that reveal gaps between where people are and where they want to be. This is the "current state vs. desired state" data.

---

### SECTION 19: PERFORMANCE GAPS

Gap analysis across: Business/Offerings, Goals, Challenges, Skills, Processes, Decision-Making, Resources, Support Network.

**Evidence requirement:** Cite VOC data showing capability gaps, resource constraints, system failures.

---

### SECTION 20: IDEAL CLIENT INTRODUCTION

Narrative answering: What do they want? Why? What do they struggle with? What do they think about? What's holding them back? What would they say? Best solution? What would success look like? Where would they find you? What inspires action?

**Evidence requirement:** Weave verbatim quotes throughout the narrative. This section should feel like a case study grounded in real data.

---

### SECTION 21: VALIDATION

What validation does this ideal client seek?

**Evidence requirement:** Cite quotes about recognition, approval, social proof, and achievement.

---

### SECTION 22: CURRENT STATE & ASPIRATIONAL STATE

Current state vs. aspirational state with gap analysis.

**Evidence requirement:** Use VOC quotes that describe "where I am now" (frustration posts) and "where I want to be" (aspiration posts). The gap analysis should reference specific evidence.

---

### SECTION 23: PRIORITIES

Advice to [NAME] about what to prioritize. Written in second person.

**Evidence requirement:** Prioritization should reflect what the VOC data says matters most — by frequency, emotional intensity, and expressed urgency.

---

### SECTION 24: THINK ABOUT IT THIS WAY

Candid message from ideal client's POV. Begins with "Think about it this way."

**ENHANCEMENT:** Construct primarily from real VOC quotes, lightly edited for flow. Attribute each quote inline.

---

### SECTION 25: TRIGGER EVENTS

**Purpose:** Identify what causes the ideal client to shift from passive pain ("I should do something about this") to active search ("I need to find a solution NOW"). Trigger events are the highest-value signals for marketing timing.

Analyze the VOC evidence bank for moments of transition — the specific events, experiences, or breaking points that precede action. Organize into categories:

#### External Triggers
Events that happen TO them:
- Competitive threat (lost a client to someone using the solution)
- Financial pressure (revenue drop, missed opportunity with clear dollar amount)
- Public exposure (asked about the topic and couldn't answer credibly)
- Industry shift (regulatory change, platform update, market disruption)

#### Internal Triggers
Realizations or emotions that reach a tipping point:
- Shame threshold (the embarrassment of falling behind becomes unbearable)
- Time pain (a specific task that "breaks the camel's back")
- Cumulative frustration (the 5th failed tool, the 10th abandoned tutorial)
- Identity threat (seeing themselves as the kind of person who CAN'T figure this out)

#### Social Triggers
People or community events that catalyze action:
- Peer success story (someone they know and respect succeeded)
- Direct recommendation (a trusted person said "you need to talk to X")
- Community post that articulates exactly what they feel
- Mentor/authority figure endorsement

For each trigger event identified:
- Cite specific VOC quotes showing the trigger
- Rate the trigger's conversion power (how strongly it drives action)
- Note the emotional state at the moment of triggering
- Identify the gap between trigger and action (what could still prevent them from acting?)

**Evidence requirement:** Every trigger must cite at least one VOC quote. Mark inferred triggers clearly. Pay special attention to quotes containing phrases like "finally," "that's when I realized," "the last straw," "I couldn't keep," "that's what made me."

---

### SECTION 26: BEHAVIORAL RESPONSE SEGMENTS

**Purpose:** Identify distinct behavioral archetypes within the ideal client niche. The niche is defined by shared emotional experience — everyone feels the same fears, frustrations, wants, and desires. The segments are defined by *how they respond to, approach, and attempt to resolve* that shared experience.

**Key principle:** Segments are NOT demographic. They are behavioral. Two people with identical demographics may be in completely different segments based on their coping strategy.

Analyze the VOC evidence bank for distinct patterns of response to the shared pain. Identify 3-5 behavioral segments. For each segment:

#### Segment Profile
- **Name:** A descriptive archetype name (e.g., "The Frozen Perfectionist," "The Frantic Tool-Hopper")
- **Defining behavior:** The dominant coping/response pattern (1-2 sentences)
- **Share of voice in VOC:** Approximate percentage of quotes that exhibit this pattern
- **Exemplar quotes:** 3-5 VOC quotes that most clearly represent this segment

#### Behavioral Pattern
- **First response to the pain:** What do they do when they first feel the problem? (research, buy tools, avoid, seek community, etc.)
- **Sticking point:** Where do they get stuck in their response pattern?
- **Self-narrative:** What story do they tell themselves about why they're stuck?
- **Visible signals:** How would you identify this segment in a conversation or intake form?

#### Pain Hierarchy
The shared pain points ranked differently for THIS segment:
- **Primary pain:** The one that dominates their experience
- **Secondary pains:** Others they feel but with less intensity
- **Pain they minimize:** Which shared pains do they downplay or deny?

#### Conversion Profile
- **What would move THIS segment to act:** The specific trigger or message that breaks their pattern
- **What repels them:** Messaging approaches that backfire for this segment
- **Optimal entry point:** The best first interaction/offer for this segment
- **Objection they always raise:** Their segment-specific objection

**Evidence requirement:** Each segment must be grounded in observable behavioral patterns from the VOC data. Do not create segments from demographic inference. Each segment must cite at least 3 VOC quotes demonstrating the behavioral pattern.

---

### SECTION 27: COMPETITIVE LANDSCAPE & POSITIONING GAPS

**Purpose:** Synthesize the competitive research from Phase 1B into actionable positioning guidance.

#### Competitive Map
For each competitor analyzed:
- Name and URL
- Primary promise / headline transformation
- Pain points they target (cite their language)
- Tone and communication style
- Pricing model (if discoverable)
- Testimonial themes (what their clients praise most)

#### Shared Positioning (Table Stakes)
What all competitors say — the baseline messaging the audience expects. This is necessary but not differentiating.

#### Positioning Gaps
**This is the highest-value output of competitive analysis.**

Identify:
1. **Unaddressed pain points:** Fears/frustrations from the VOC bank that NO competitor speaks to
2. **Underserved segments:** Behavioral segments (from Section 26) that no competitor targets
3. **Language gaps:** Emotional language the audience uses that no competitor mirrors
4. **Trust gaps:** Objections the audience has that no competitor addresses
5. **Depth gaps:** Topics competitors mention superficially that the audience wants depth on

For each gap, cite:
- The VOC evidence showing the audience need
- The competitive evidence showing the gap
- A recommended positioning angle for [NAME]

**Evidence requirement:** Every gap claim must cite both a VOC quote (showing the need exists) and competitive evidence (showing no one addresses it). Mark gaps based on inference as [INFERRED GAP].

---

### SECTION 28: CONTRADICTIONS & TENSIONS

**Purpose:** Identify places where the audience holds opposing beliefs, desires, or behaviors simultaneously. Contradictions reveal internal conflict — the psychological tension that makes people stuck and that marketing, coaching, and content must navigate carefully.

Scan the entire VOC evidence bank for pairs of quotes (or even within single quotes) that express opposing positions. Organize into categories:

#### Belief Tensions
Where they believe two incompatible things at once:
- Example: "AI will replace me" AND "AI can never do what I do" — both held by the same audience
- For each tension, cite both sides with VOC quotes

#### Desire Tensions
Where they want two things that conflict:
- Example: "I want to automate everything" AND "I want to stay hands-on with my clients"
- These reveal the actual tradeoffs they're struggling to make

#### Behavior Tensions
Where their actions contradict their stated beliefs or desires:
- Example: They say "I'm ready to change" but their behavior shows continued avoidance
- VOC-048 ("For 3 years I pretended my AI tools were game-changers") is a behavior tension — the performance contradicts the reality

#### Cross-Segment Tensions
Where different segments hold opposing views on the same topic:
- Example: Frantic Tool-Hoppers say "just pick a tool and go" while Frozen Perfectionists say "I need to research more before I start"
- These tensions define the challenge of serving the whole niche with one message

For each contradiction identified:
- Cite the specific VOC quotes showing both sides
- Explain why the tension exists (what underlying fear or need drives each side?)
- Note the **strategic implication** — how should [NAME] navigate this tension in messaging, offers, and content? (Hint: usually by acknowledging both sides rather than picking one.)

**Evidence requirement:** Every tension must cite at least two VOC quotes showing the opposing positions. Mark tensions based on a single ambivalent quote as [SINGLE-SOURCE TENSION]. Mark tensions inferred from segment analysis as [CROSS-SEGMENT TENSION].

---

### SECTION 29: BLUE OCEAN CONTENT OPPORTUNITIES

**Purpose:** Identify topics where the audience has high demand but existing content is low-quality, generic, or absent. These are the highest-leverage content opportunities — topics where [NAME] can become the go-to authority.

Analyze the intersection of three data sources:
1. **VOC demand signals** — Questions the audience repeatedly asks, frustrations with existing content, "I wish someone would explain X" statements
2. **Competitive coverage** — Topics competitors address well vs. superficially vs. not at all (from Section 27)
3. **Search landscape** — Use `WebSearch` to check the top results for key audience questions. Are results authoritative or generic?

#### Identifying Blue Oceans
For each high-demand topic from the VOC bank:
- **Search the topic** and assess the top 5 results: Are they from authorities? Are they specific to this audience or generic?
- **Check competitor coverage** — Do any competitors address this well?
- **Rate the opportunity:**
  - **OPEN OCEAN** — High audience demand + no quality content exists + no competitor covers it
  - **UNDERSERVED** — High demand + some content exists but it's generic, outdated, or not specific to this audience
  - **CONTESTED** — High demand + quality content exists but [NAME] has a differentiated angle

#### Output Format
For each opportunity:
```
TOPIC: [specific topic or question]
DEMAND EVIDENCE: [VOC-###] quotes showing audience need
CURRENT LANDSCAPE: Brief assessment of existing content quality
COMPETITOR COVERAGE: Which competitors address this, and how well
OPPORTUNITY RATING: OPEN OCEAN | UNDERSERVED | CONTESTED
RECOMMENDED ANGLE: How [NAME] should approach this topic differently
CONTENT FORMAT: Suggested format (long-form guide, video, tool, etc.)
```

Identify 10-15 opportunities, ranked by opportunity rating (OPEN OCEAN first).

**Evidence requirement:** Every opportunity must cite at least one VOC quote showing demand. Search landscape assessment must reference actual search results, not assumptions.

---

## PHASE 3: ONTOLOGY EXTRACTION

After the full handbook, generate a structured **Ontology** for AI engine schema construction. Output as a fenced JSON code block and save as `.json`.

### Ontology Structure

```json
{
  "ontology_metadata": {
    "domain": "[business type / niche]",
    "generated": "[date]",
    "voc_evidence_count": {
      "web_sourced": 0,
      "user_provided": 0,
      "competitive": 0,
      "total": 0
    },
    "confidence_score": "high|medium|low"
  },
  "entities": {
    "ideal_client": {
      "demographics": {
        "age_range": { "value": "", "evidence": ["VOC-###"], "confidence": "" },
        "gender": { "value": "", "evidence": [], "confidence": "" },
        "location_type": { "value": "", "evidence": [], "confidence": "" },
        "education": { "value": "", "evidence": [], "confidence": "" },
        "profession_cluster": { "value": "", "evidence": [], "confidence": "" },
        "income_range": { "value": "", "evidence": [], "confidence": "" }
      },
      "psychographics": {
        "core_values": [
          { "value": "", "evidence": ["VOC-###"], "weight": 0.0 }
        ],
        "identity_labels": [],
        "worldview_orientation": "",
        "personality_indicators": {
          "mbti_likely": [],
          "enneagram_likely": [],
          "disc_likely": [],
          "archetype": []
        }
      }
    },
    "pain_points": [
      {
        "id": "PP-001",
        "category": "fear|frustration|limiting_belief",
        "label": "",
        "description": "",
        "verbatim_quotes": ["VOC-###"],
        "frequency_rank": 1,
        "emotional_intensity": "high|medium|low",
        "trend": "emerging|stable|fading",
        "trend_note": "Brief context, e.g. 'Spiked after GPT-4 launch, now normalizing'",
        "related_false_beliefs": ["FB-###"],
        "related_needs": ["NEED-###"]
      }
    ],
    "desires": [
      {
        "id": "DES-001",
        "label": "",
        "description": "",
        "verbatim_quotes": ["VOC-###"],
        "type": "aspirational|immediate|emotional",
        "trend": "emerging|stable|fading",
        "related_pain_points": ["PP-###"]
      }
    ],
    "false_beliefs": [
      {
        "id": "FB-001",
        "belief": "",
        "why_they_hold_it": "",
        "truth": "",
        "verbatim_quotes": ["VOC-###"],
        "trend": "emerging|stable|fading",
        "related_pain_points": ["PP-###"]
      }
    ],
    "needs": [
      {
        "id": "NEED-001",
        "type": "emotional|immediate|unmet",
        "label": "",
        "description": "",
        "verbatim_quotes": ["VOC-###"],
        "priority": "critical|high|medium|low"
      }
    ],
    "objections": [
      {
        "id": "OBJ-001",
        "objection": "",
        "root_cause": "",
        "verbatim_quotes": ["VOC-###"],
        "counter_strategy": "",
        "frequency_rank": 1
      }
    ],
    "trigger_events": [
      {
        "id": "TRIG-001",
        "category": "external|internal|social",
        "label": "",
        "description": "",
        "verbatim_quotes": ["VOC-###"],
        "conversion_power": "high|medium|low",
        "emotional_state_at_trigger": "",
        "barrier_after_trigger": ""
      }
    ],
    "segments": [
      {
        "id": "SEG-001",
        "name": "",
        "defining_behavior": "",
        "share_of_voice_pct": 0,
        "exemplar_quotes": ["VOC-###"],
        "first_response": "",
        "sticking_point": "",
        "self_narrative": "",
        "visible_signals": [],
        "pain_hierarchy": {
          "primary": "PP-###",
          "secondary": ["PP-###"],
          "minimized": ["PP-###"]
        },
        "conversion_trigger": "",
        "repelling_message": "",
        "optimal_entry_point": "",
        "segment_specific_objection": "OBJ-###"
      }
    ],
    "competitive_landscape": {
      "competitors": [
        {
          "name": "",
          "url": "",
          "primary_promise": "",
          "pain_points_targeted": [],
          "tone": "",
          "testimonial_themes": []
        }
      ],
      "shared_positioning": [],
      "positioning_gaps": [
        {
          "id": "GAP-001",
          "type": "unaddressed_pain|underserved_segment|language_gap|trust_gap|depth_gap",
          "description": "",
          "audience_evidence": ["VOC-###"],
          "competitive_evidence": "",
          "recommended_angle": ""
        }
      ]
    },
    "transformation_arc": {
      "current_state": {
        "description": "",
        "verbatim_quotes": ["VOC-###"]
      },
      "aspirational_state": {
        "description": "",
        "verbatim_quotes": ["VOC-###"]
      },
      "gaps": [
        {
          "type": "personal|performance|knowledge|resource",
          "description": "",
          "priority": ""
        }
      ]
    },
    "language_patterns": {
      "high_frequency_phrases": [
        { "phrase": "", "count": 0, "contexts": ["VOC-###"] }
      ],
      "emotional_triggers": [],
      "aspiration_language": [],
      "resistance_language": [],
      "decision_language": [],
      "semantic_clusters": [
        {
          "cluster_label": "",
          "description": "",
          "member_quotes": ["VOC-###"],
          "shared_linguistic_pattern": "",
          "insight": ""
        }
      ]
    },
    "journey_touchpoints": [
      {
        "stage": "awareness|consideration|decision|retention",
        "touchpoint": "",
        "emotional_state": "",
        "key_questions": [],
        "verbatim_quotes": ["VOC-###"],
        "trigger_events_at_stage": ["TRIG-###"]
      }
    ],
    "contradictions": [
      {
        "id": "TENS-001",
        "type": "belief|desire|behavior|cross_segment",
        "side_a": {
          "position": "",
          "evidence": ["VOC-###"]
        },
        "side_b": {
          "position": "",
          "evidence": ["VOC-###"]
        },
        "why_tension_exists": "",
        "strategic_implication": ""
      }
    ],
    "blue_ocean_opportunities": [
      {
        "id": "OPP-001",
        "topic": "",
        "demand_evidence": ["VOC-###"],
        "current_landscape": "",
        "competitor_coverage": "",
        "opportunity_rating": "open_ocean|underserved|contested",
        "recommended_angle": "",
        "suggested_format": ""
      }
    ]
  },
  "relationships": [
    {
      "from": "PP-001",
      "to": "FB-001",
      "type": "caused_by|reinforces|blocks|triggers|converts",
      "description": ""
    }
  ],
  "causal_chains": [
    {
      "id": "CHAIN-001",
      "label": "Short descriptive name for this chain",
      "sequence": [
        { "entity_id": "TRIG-001", "role": "trigger", "description": "What initiates the chain" },
        { "entity_id": "PP-001", "role": "fear", "description": "The fear/pain activated" },
        { "entity_id": "FB-001", "role": "belief", "description": "The belief that shapes their response" },
        { "entity_id": "SEG-001", "role": "behavior", "description": "The behavioral response pattern" },
        { "entity_id": "OBJ-001", "role": "outcome", "description": "Where the chain leads without intervention" }
      ],
      "intervention_point": "Where in this chain [NAME]'s solution intercepts",
      "evidence": ["VOC-###"],
      "confidence": "EVIDENCED|PATTERN|INFERRED"
    }
  ],
  "voc_evidence_bank": [
    {
      "id": "VOC-001",
      "quote": "",
      "source_platform": "",
      "source_url": "",
      "source_date": "",
      "context": "",
      "author_context": {
        "role": "",
        "experience_level": "",
        "industry": ""
      },
      "theme_tags": [],
      "referenced_by": ["PP-001", "FB-002"]
    }
  ]
}
```

### Ontology Generation Rules:
1. Every entity must reference at least one VOC quote by ID
2. Pain points, desires, and objections are ranked by frequency in the evidence bank
3. Relationships between entities must be explicitly mapped (e.g., pain point X is caused by false belief Y)
4. Language patterns must be extracted from actual VOC text — these become the vocabulary for the AI engine
5. Confidence scores reflect evidence strength: `high` = 3+ supporting quotes, `medium` = 1-2 quotes, `low` = inference only
6. Trigger events must link to journey touchpoints (which stage do they trigger?)
7. Segments must reference pain points, objections, and trigger events by ID
8. Each VOC quote in the evidence bank must include a `referenced_by` array listing all entities that cite it
9. **Causal chains must be built.** After populating all entities, trace 5-10 directional chains that show how the audience's psychology actually flows: Trigger → Fear/Pain → Belief → Behavioral Response → Outcome. Each chain should identify the **intervention point** where [NAME]'s offering intercepts the chain. Chains are what make the ontology actionable — they answer "what causes what" rather than just "what exists."
10. **Author context must be captured** on every VOC quote where discernible. Role, experience level, and industry enable segment-level analysis and make the evidence filterable by audience sub-type.
11. **Temporal signals must be assessed** for pain points, desires, and false beliefs. Use VOC quote dates and contextual clues to determine whether each entity is `emerging` (new or rapidly growing), `stable` (persistent and established), or `fading` (declining in relevance). Add a brief `trend_note` explaining the assessment. This helps prioritize which pains to lead with (emerging pains are underserved; fading pains are over-addressed).

### Semantic Similarity Clustering

After building the ontology, perform a semantic clustering pass:

1. **Group VOC quotes by linguistic similarity** — not just by theme tag, but by actual word choice, sentence structure, and emotional register. Quotes that use similar language may reveal hidden connections that manual tagging missed.

2. **For each cluster:**
   - Assign a descriptive label
   - Describe the shared linguistic pattern (e.g., "water/drowning metaphors for overwhelm")
   - List all member quotes by ID
   - Note any insight the cluster reveals that individual quotes don't (e.g., "5 unrelated people across 3 platforms all used the word 'drowning' — this metaphor has deep resonance")

3. **Cross-check clusters against entities:** Do any clusters suggest pain points, desires, or segments that the manual analysis missed? If so, flag them.

---

## PHASE 3B: MESSAGING FRAMEWORK

**Output:** Save as a separate `.md` file: `[name]-messaging-framework.md`

Generate a deployable messaging framework derived directly from the ontology. Every message must trace back to specific VOC quotes and ontology entities.

### Headlines & Hooks
For each of the top 10 pain points, generate:
- **Pain-to-promise headline:** Mirrors their language, offers the transformation
- **Pattern-interrupt hook:** An unexpected framing that stops the scroll
- **VOC-echo headline:** Built directly from a real quote (with [VOC-###] citation)

Format:
```
PP-001: Tool Overwhelm
  Pain-to-promise: "[headline]"
  Pattern-interrupt: "[headline]"
  VOC-echo: "[headline]" (from [VOC-###])
```

### Email Subject Lines
Generate 15 email subject lines organized by emotional trigger:
- 5 fear-based (mapped to specific fears from Section 6)
- 5 aspiration-based (mapped to specific desires)
- 5 curiosity-based (mapped to false beliefs — "what if the thing you believe is wrong?")

Each with the entity ID it maps to.

### Objection-Handling Scripts
For each of the top 5 objections, generate a 3-part response:
1. **Acknowledge** — Mirror their language (cite VOC quote)
2. **Reframe** — Introduce the truth from the false_beliefs entity
3. **Prove** — Cite a transformation quote or competitive gap

### Segment-Specific Messaging
For each behavioral segment (from Section 26), generate:
- **Opening line** that signals "this is for you" to that segment
- **Key message** that addresses their primary pain in their behavioral frame
- **CTA** that matches their conversion trigger
- **Message to avoid** — what would repel this segment

### Before/After Statements
Generate 5-10 transformation statements:
```
BEFORE: "[current state language from VOC]" [VOC-###]
AFTER: "[aspirational state language from VOC]" [VOC-###]
```

### Positioning Statement
Based on the competitive gaps analysis, generate:
- A 1-sentence positioning statement for [NAME]
- A "what we do differently" paragraph grounded in the gaps
- The #1 unoccupied positioning angle with evidence

---

## PHASE 3C: EVIDENCE AUDIT & GAP REPORT

**Output:** Save as a separate `.md` file: `[name]-evidence-audit.md`

### Confidence Heat Map

Scan every entity in the ontology and score by evidence strength:

```
EVIDENCE STRENGTH BY ENTITY

Entity                     | Quotes | Strength | Rating
---------------------------|--------|----------|--------
PP-001 [label]             |    5   | █████    | STRONG
PP-002 [label]             |    4   | ████░    | STRONG
...
PP-006 [label]             |    1   | █░░░░    | FRAGILE
...
```

Scoring:
- **STRONG** (5+ quotes, 2+ platforms): High confidence. No action needed.
- **SOLID** (3-4 quotes): Good confidence. Optional to strengthen.
- **THIN** (2 quotes): Moderate confidence. Worth strengthening.
- **FRAGILE** (1 quote): Low confidence. Priority gap.
- **INFERRED** (0 quotes): Inference only. Highest priority gap.

Apply to ALL entity types: pain points, desires, false beliefs, needs, objections, trigger events, segments.

### Gap Report

#### Fragile Entities
List every entity rated FRAGILE or INFERRED with:
- The entity ID and label
- Current supporting quotes (if any)
- **3 specific search queries** designed to find supporting evidence
- Expected source types (Reddit threads, Amazon reviews, forum posts, etc.)

Format:
```
GAP: PP-006 Data Security Fear
  Current evidence: 1 quote (VOC-005)
  Recommended searches:
    1. "AI data privacy" small business OR solopreneur worried OR concerned
    2. site:reddit.com "AI tools" "data leak" OR "privacy" small business
    3. "ChatGPT" OR "AI tools" "security risk" entrepreneur review
  Expected sources: Reddit r/smallbusiness, Quora, tech blog comment sections
```

#### Orphaned Quotes
List any VOC quotes that are not referenced by ANY entity in the ontology:
- Quote ID and text
- Analysis: Does this quote suggest an entity we missed? A segment we didn't identify? A trigger event we overlooked?
- Recommendation: Add to existing entity, create new entity, or discard as noise

#### Platform Coverage Gaps
Assess coverage by platform:
```
Platform     | Quotes | Coverage
-------------|--------|----------
Reddit       |    3   | LOW — blocked during scraping
Quora        |   12   | GOOD
Amazon       |    8   | GOOD
Skool        |    4   | MODERATE
LinkedIn     |    3   | LOW — limited scraping
Facebook     |    5   | MODERATE
YouTube      |    0   | NONE — not attempted or blocked
```

For platforms with LOW or NONE coverage, provide specific search strategies to improve coverage in a follow-up research round.

#### Segment Validation Check
For each behavioral segment identified in Section 26:
- How many unique VOC quotes support this segment?
- Is the segment distinguishable from others with clear behavioral boundaries?
- Confidence rating: VALIDATED (5+ quotes with clear pattern) / EMERGING (2-4 quotes) / HYPOTHESIZED (inference only)

#### Overall Confidence Summary
A 1-paragraph assessment of the ontology's overall evidence strength, noting:
- Strongest areas (highest confidence entities)
- Weakest areas (lowest confidence entities)
- Highest-priority gaps to fill
- Estimated additional research needed (number of searches, expected yield)

### Phase 3D Decision Point

After presenting the audit, ask the user:

"The evidence audit identified [X] INFERRED, [Y] FRAGILE, and [Z] THIN entities. Would you like to run
iterative gap filling (Phase 3D) to automatically strengthen the weakest evidence?
This runs up to [MAX_ITERATIONS] targeted research rounds. Or proceed directly to Phase 4?"

If the user chooses Phase 3D, proceed to the iterative loop.
If they decline, skip to Phase 4.

---

## PHASE 3D: ITERATIVE GAP FILLING

**Purpose:** Automatically strengthen the weakest evidence in the ontology using targeted research loops. Phase 3C identifies where evidence is thin — this phase fills those gaps systematically, prioritizing entities that matter most to the positioning strategy.

**Optional but recommended.** Skip if the user wants to proceed directly to Phase 4.

**Requires Phase 3C.** This phase uses the gap report, evidence ratings, and recommended search queries from Phase 3C. If Phase 3C was not run, run it first before entering this loop.

### Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `MAX_ITERATIONS` | 3 | Maximum research loops before forced stop |
| `QUALITY_THRESHOLD` | No CRITICAL or HIGH-SIS gaps at FRAGILE or INFERRED | Stop condition for evidence quality |
| `MIN_QUOTES_PER_GAP` | 1 | Diminishing returns threshold — fewer than 1 new quote per targeted gap = stop |

### 3D-1: Strategic Importance Scoring (SIS)

**Scored once at loop entry.** SIS depends on the ontology structure, which doesn't change during the loop (ontology regeneration happens at loop end). Re-use scores across all iterations.

Every INFERRED, FRAGILE, and THIN entity gets scored on 4 dimensions (0–3 each, weighted):

| Dimension | Weight | What it measures | How to look it up |
|-----------|--------|-----------------|-------------------|
| Differentiation Centrality | 3× | Does this entity support an unoccupied competitive position? | Check `positioning_gaps` array in ontology and Section 27 of handbook |
| Causal Chain Position | 3× | How many causal chains include this entity? Is it an intervention point? | Count occurrences in `causal_chains` array in ontology |
| Segment Reach | 2× | How many behavioral segments does it affect? | Check `segments[].pain_hierarchy` and `segments[].exemplar_quotes` in ontology |
| Messaging Dependency | 2× | How many messaging framework assets reference this entity? | Grep the messaging framework file for the entity ID/label |

**SIS = (Differentiation × 3) + (Causal Chain × 3) + (Segment Reach × 2) + (Messaging Dependency × 2)**

Maximum score: 30. Tiers:
- **CRITICAL (21–30):** Must fill — undermines positioning strategy
- **HIGH (11–20):** Should fill — weakens important sections
- **MODERATE (6–10):** Nice to fill — affects depth not direction
- **LOW (0–5):** Optional — improves completeness only

**Default for entities with no relationship links in the ontology:** Score as MODERATE (6). Absence of links may mean under-analyzed, not unimportant.

#### Worked Example

Suppose the audit flagged these entities:

**Entity: "Identity Crisis" (THIN, 3 quotes)**
- Differentiation Centrality: 3 — appears in 2 positioning gaps ("mid-career identity work" is an unoccupied position)
- Causal Chain Position: 3 — present in 4 causal chains, serves as intervention point for career pivots
- Segment Reach: 2 — affects 3 of 4 behavioral segments
- Messaging Dependency: 1 — referenced in 2 messaging assets
- **SIS = (3×3) + (3×3) + (2×2) + (1×2) = 9 + 9 + 4 + 2 = 24 → CRITICAL**

**Entity: "Age-Related Anxiety" (FRAGILE, 1 quote)**
- Differentiation Centrality: 2 — supports 1 positioning gap
- Causal Chain Position: 2 — present in 2 causal chains
- Segment Reach: 2 — affects 2 segments
- Messaging Dependency: 1 — referenced in 1 messaging asset
- **SIS = (2×3) + (2×3) + (2×2) + (1×2) = 6 + 6 + 4 + 2 = 18 → HIGH**

**Entity: "Credential Anxiety" (THIN, 2 quotes)**
- Differentiation Centrality: 0 — not tied to any positioning gap
- Causal Chain Position: 1 — appears in 1 causal chain
- Segment Reach: 1 — affects 1 segment
- Messaging Dependency: 0 — not referenced in messaging
- **SIS = (0×3) + (1×3) + (1×2) + (0×2) = 0 + 3 + 2 + 0 = 5 → LOW**

### 3D-2: Gap Triage

1. Rank all INFERRED/FRAGILE/THIN entities by SIS tier, then by evidence rating ascending within tier
2. Select targets for this iteration: all CRITICAL gaps + HIGH gaps (aim for 5–8 total gaps per iteration). If more than 8 CRITICAL+HIGH gaps exist, take all CRITICAL first, then fill remaining slots with the highest-SIS HIGH gaps. Deferred HIGH gaps carry over to the next iteration.
3. Pull recommended search queries from Phase 3C gap report for each target. Note: Phase 3C only generates search queries for FRAGILE and INFERRED entities. For THIN entities (which lack pre-built queries), generate 3 queries per entity based on the entity label, related keywords from the ontology, and platform affinity from the coverage analysis.
4. **Separate audience VOC gaps from competitive intelligence gaps** — these use different research strategies (broad searching vs. targeted page scraping)

Present triage as a compact table:
```
ITERATION [N] TRIAGE — [X] gaps targeted

Entity              | Current | SIS   | Tier     | Type  | Searches
--------------------|---------|-------|----------|-------|----------
Identity Crisis     | THIN(3) | 24    | CRITICAL | VOC   | 3 queries
Age-Related Anxiety | FRAG(1) | 18    | HIGH     | VOC   | 3 queries
Revenue Model Gap   | FRAG(1) | 14    | HIGH     | Comp  | 2 queries
...

Proceed? [Y/continue/stop]
```

Wait for user confirmation. If user says stop, skip to the final audit step (3D-8 loop termination).

### 3D-3: Targeted Research (parallel sub-agents)

**Audience VOC gaps:** Group by platform affinity (not by entity). One search often yields quotes for multiple gaps.
- Dispatch one sub-agent per platform batch (Reddit, LinkedIn, Community/Forum, YouTube)
- All audience batches run in parallel

**Competitive intelligence gaps:** Separate batch — requires targeted page scraping, not broad searching.
- Dispatch one sub-agent for competitor pages (testimonials, reviews, case studies)
- Runs in parallel with audience batches

**Each sub-agent receives a compact brief:**
```
TARGET GAPS: [entity ID, label, current quote count] × N
SEARCH QUERIES: [the 3 recommended queries per gap from Phase 3C]
NUMBERING: Start at VOC-[next available number]
EXISTING IDS: [list of all current VOC-### IDs to skip duplicates]
QUOTE FORMAT:
  [VOC-###]
  Quote: "exact verbatim text"
  Source: Platform
  URL: full URL
  Date: approximate
  Context: 1-sentence
  Author Context: role/experience/industry or "Unknown"
  Theme Tags: [tags]
  Supports: [entity IDs this quote strengthens]
QUALITY BAR: Full sentences only. No fragments. Verbatim — do not clean grammar. Reject if <10 words or no clear attribution.
DEDUP RULE: Skip any quote that substantially overlaps with an existing quote (same author, same point, same thread). When in doubt, include it — parent will dedup.
```

**Each sub-agent returns:** Structured quote objects only. Not raw scrape data. Not search result lists. Just quotes that passed the quality bar.

**Tool fallback:** If firecrawl credits are exhausted, sub-agents fall back to `WebSearch` + `WebFetch`. If both fail for a platform, note it and move on — do not block the iteration on one source.

### 3D-4: Evidence Integration

1. Parent agent reviews returned quotes for duplicates (same person/thread/point as existing bank)
2. Merge approved quotes into evidence bank with sequential numbering
3. **Append to a new section** in the evidence bank file: `# GAP FILL ROUND [N]` — preserves the original organization by source type
4. Map each new quote to the entities it supports (using the `Supports` field from sub-agents)
5. Update entity quote counts and platform diversity
6. First iteration only: also integrate high-value orphaned quotes identified in Phase 3C audit (move from "orphaned" to an appropriate entity)
7. Write updated evidence bank to file immediately

### 3D-5: Re-Score & Assess

Re-compute evidence strength ratings for all targeted entities using the same rating scale from Phase 3C.

Generate iteration delta table:
```
ITERATION [N] RESULTS — [X] new quotes from [Y] platforms

Entity              | Before  | After   | Change
--------------------|---------|---------|--------
Identity Crisis     | THIN(3) | SOLID(5)| +2 quotes, +1 platform
Age-Related Anxiety | FRAG(1) | THIN(3) | +2 quotes, +2 platforms
...
```

Evaluate stop conditions (see 3D-8).

### 3D-6: Update Artifacts (conditional, batched at loop end)

**Per-iteration:** Only update the evidence bank file (done in 3D-4). All other artifact updates are deferred to loop termination to avoid compounding errors from incremental edits.

**At loop end (after final iteration):** For entities that improved from the original Phase 3C baseline:

- **Handbook:** Use the entity → section mapping below. Read the target section by heading, add new blockquote citations, write back. Do NOT re-read or modify unrelated sections.
- **Ontology:** Regenerate the full ontology JSON (Phase 3 process) rather than surgically editing. The JSON is too large and interconnected for safe partial updates. This adds time but prevents structural corruption.
- **Messaging framework:** Add new VOC-echo headlines or objection-handling proof points for entities that are now SOLID+. Do not modify existing messaging — append new assets.

**Entity → Handbook Section Mapping:**

| Entity Type | Primary Section(s) | Secondary Sections |
|-------------|-------------------|-------------------|
| Fears | 6 (Pain Points), 7 (Verbatim) | 10 (Client Statements), 25 (Triggers) |
| Frustrations | 6, 7 | 10, 19 (Performance Gaps) |
| Limiting Beliefs | 6, 7 | 16 (False Beliefs) |
| False Beliefs | 16 | 6, 11 (Objections) |
| Objections | 11 | 12 (Client Journey) |
| Needs (emotional) | 15 | 9 (What I Really Want to Say) |
| Needs (immediate) | 15 | 8 (Solutions), 23 (Priorities) |
| Needs (unmet) | 15 | 27 (Positioning Gaps), 29 (Blue Ocean) |
| Desires | 8 (Solutions & Outcomes) | 9 (What I Really Want to Say), 15 (Needs) |
| Trigger Events | 25 | 12 (Client Journey), 26 (Segments) |
| Behavioral Segments | 26 | 27 (Competitive Landscape) |

### 3D-7: Iteration Report

Present to user:
- New quotes found (count, platforms)
- Entity improvements (delta table from 3D-5)
- Remaining gaps with SIS tiers
- Stop condition status

If loop is not terminating, ask: "Continue to iteration [N+1], or stop here?"

If user says stop at any point, proceed directly to the final audit step (same as loop termination).

### 3D-8: Stop Conditions

Evaluated in order after each iteration:

1. **Quality threshold met:** No CRITICAL or HIGH-SIS gaps remain at FRAGILE or INFERRED → **STOP**
2. **Diminishing returns:** New quotes this iteration < (number of targeted gaps × `MIN_QUOTES_PER_GAP`) → **STOP**. Report which gaps appear unfillable via web research and recommend user-provided data instead (interviews, surveys, intake forms, sales call notes).
3. **Iteration limit:** iteration == `MAX_ITERATIONS` → **STOP**. Report remaining gaps.

**On loop termination:**

1. Run the artifact updates described in 3D-6
2. Generate a **final Evidence Audit** as a new file `[name]-evidence-audit-final.md` (do NOT overwrite the original Phase 3C audit — keep both for comparison)
3. The final audit includes:
   - Updated heat map
   - A "Gap Fill Summary" section showing before/after for all targeted entities
   - Remaining gaps with explanation of why they couldn't be filled
   - Updated Overall Confidence Summary

---

## PHASE 4: CLOSE & OFFER NEXT STEPS

Close the handbook with:
```
================================================================
END OF IDEAL CLIENT HANDBOOK
[NAME] · Generated [date]
VOC Evidence: [X] web-sourced, [Y] user-provided, [Z] competitive, [total] total quotes
================================================================
```

### File Summary
Present all saved files:
1. `[name]-ideal-client-handbook.md` — 29-section handbook
2. `[name]-ideal-client-ontology.json` — Structured ontology
3. `[name]-messaging-framework.md` — Deployable messaging assets
4. `[name]-evidence-audit.md` — Confidence heat map + gap report
5. `[name]-voc-evidence-bank.md` — Raw evidence bank
6. `[name]-evidence-audit-final.md` — Final audit after gap filling (only if Phase 3D was run)

### Next Steps
Offer:
1. **Fill remaining gaps** — If Phase 3D was run, most web-researchable gaps have been addressed. Remaining gaps likely require user-provided data (interview transcripts, survey responses, intake forms, sales call notes). Provide this data and re-run targeted analysis.
2. **Deepen a section** — Re-run research on a specific section with more targeted queries
3. **Deepen a segment** — Run segment-specific research to validate or expand a behavioral segment
4. **Generate AI engine schema** — Transform the ontology into a specific schema format (specify target: knowledge graph, vector DB, chatbot training, etc.)
5. **Competitive deep-dive** — Expand competitive analysis with additional competitors
6. **Run Temporal VOC Analysis** — With 150+ dated quotes accumulated across research rounds, temporal trend analysis is now viable. Identify which fears are emerging vs. fading.

---

## EXECUTION NOTES

- **Parallel research:** Run as many web searches simultaneously as possible during Phase 1
- **Respect rate limits:** If a scrape fails, note it and move on — don't block on a single source
- **Quality over quantity:** 30 strong verbatim quotes beat 100 weak fragments
- **Preserve exact language:** Never clean up grammar or spelling in verbatim quotes — the raw language IS the data
- **Language support:** All sections in the user's preferred language; VOC quotes preserved in their original language with translations in brackets if needed
- **Context window management:** Phase 1 research may produce large volumes. Summarize the evidence bank before proceeding to Phase 2. Keep the full bank available for citation but don't hold all raw scrape data in context.
- **Attribution is non-negotiable:** Every quote must have a source. If attribution is lost during processing, mark the quote as [UNATTRIBUTED] and note the likely source.
- **Competitive ethics:** When scraping competitor pages, record only publicly available information. Do not attempt to access gated content, private communities, or paid materials.
- **Segment discipline:** Segments are behavioral, not demographic. If a proposed segment is distinguishable only by demographics (age, gender, location), it is NOT a valid segment. Valid segments are defined by distinct behavioral response patterns to the shared pain.
- **Messaging traceability:** Every message in the messaging framework must cite at least one VOC quote and one ontology entity. No orphaned messages.
- **Audit honesty:** The evidence audit must be ruthlessly honest. Its purpose is to reveal weakness, not reassure. An audit that rates everything as STRONG is probably wrong.
- **Iterative gap filling context management:** Phase 3D sub-agents carry all search/scrape context. The parent holds only: the SIS-ranked gap list, the iteration delta table, and the evidence bank file path. All raw data lives in files, not in context.
- **SIS scoring lookups:** Score Differentiation from the ontology's `positioning_gaps` and the competitive analysis. Score Causal Chain Position by counting entity occurrences in `causal_chains`. Score Segment Reach from `segments[].pain_hierarchy`. Score Messaging Dependency by grepping the messaging framework file. Default to MODERATE (6) for entities with no relationship data.
- **Quote quality in iterations:** Later iterations target narrower topics and may yield lower-quality results. Sub-agents must maintain the same quality bar as Phase 1: full sentences (not fragments), verbatim (no grammar cleanup), with source attribution. Reject quotes under 10 words. Prefer quotes with discernible author context.
- **Ontology regeneration:** At loop end, regenerate the full ontology rather than surgically editing the JSON. The 200KB+ file with 400+ cross-references is too interconnected for safe partial updates.
- **Tool budget awareness:** Each iteration dispatches 3–5 parallel sub-agents, each making 3–8 web searches. Budget ~20–40 web searches per iteration, ~60–120 across 3 iterations. If search tools hit rate limits or credit exhaustion, the sub-agent should fall back gracefully and report what it could not access.
