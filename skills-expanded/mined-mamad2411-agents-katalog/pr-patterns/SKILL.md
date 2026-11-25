---
name: pr-patterns
description: "When to activate: press release, media relations, PR strategy, earned media, journalist outreach, embargo, wire services, crisis PR, HARO, thought leadership"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: marketing
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# PR Patterns

## Press Release Template

```
FOR IMMEDIATE RELEASE / EMBARGOED UNTIL [DATE TIME TIMEZONE]

[COMPANY] [VERB] [WHAT] — [BENEFIT/HOOK IN ONE LINE]

[CITY, DATE] — [Company] today announced [what], enabling [who] to [benefit].

[Paragraph 1: The news. What, who, why it matters. Lead with the strongest hook.]

[Paragraph 2: Context. Market problem, why now, what makes this different.]

[Paragraph 3: Quote from CEO/Founder — voice, vision, human angle.]

[Paragraph 4: Product/feature details, availability, pricing if relevant.]

[Paragraph 5: Customer/partner quote if available.]

[Boilerplate: 2-3 sentences about the company. Always the same.]

Media Contact:
Name | Title
email@company.com | +1 (555) 000-0000
```

## Newsworthiness Checklist

Before pitching, verify the story has at least one:
- [ ] Significant funding/milestone (revenue, users, growth %)
- [ ] New product/feature with clear market impact
- [ ] Partnership with recognizable name
- [ ] Research or data nobody else has
- [ ] Contrarian take on a trending topic
- [ ] Human interest angle (founder story, customer transformation)
- [ ] Timeliness hook (responds to news cycle)

## Media List Building

### Tier Structure
| Tier | Outlet type | Lead time | Relationship req. |
|------|------------|-----------|-------------------|
| T1 | WSJ, NYT, TechCrunch, Forbes | 3-4 weeks | Warm intro preferred |
| T2 | Vertical trade press, mid-size tech blogs | 2 weeks | Cold pitch ok |
| T3 | Newsletters, podcasts, niche communities | 1 week | Cold pitch ok |

### Building the List
1. Search "[competitor name] featured in" — clone their press coverage
2. Search "[industry keyword] reporter" on Twitter/X/LinkedIn
3. Use Muck Rack or Cision to find beat reporters
4. Check bylines on competitor coverage
5. Track who covers funding rounds in your space (Crunchbase News, The Information)

## Pitch Writing Framework

### Structure (under 200 words)
```
Subject: [Data point or strong hook] — not "press release attached"

Hi [First name],

[1 sentence: Why this is relevant to their specific beat/recent coverage]

[2-3 sentences: The news. Concrete, specific, numbers where possible]

[1 sentence: Why their readers care]

Happy to set up a briefing or send more details. Exclusive window
available until [date] if interested.

[Name]
```

### Subject Line Formulas
- `[Company] raises $Xm to [solve specific problem]`
- `[Number]% of [audience] now [behavior] — new data`
- `[Recognizable brand] picks [your company] for [use case]`
- Avoid: "Exciting news!", "Check this out", generic announcements

### Personalization (non-negotiable)
- Reference a specific article they wrote
- Connect the story to their beat explicitly
- Never use mail-merge-style "I love your work on [topic]"

## Embargo Strategy

### When to Use an Embargo
- Coordinating simultaneous coverage across multiple outlets
- Giving reporters time to prepare in-depth stories
- Aligning with a product launch date

### Embargo Best Practices
- Set specific date + time + timezone: `Embargoed until 9am ET Tuesday June 10`
- Keep embargo list small — more outlets = more risk of leak
- Get verbal confirmation before sharing embargoed materials
- Send a reminder 24h before lift
- If one outlet breaks early, lift for everyone immediately

### Exclusive vs. Embargo
| | Exclusive | Embargo |
|-|-----------|---------|
| Who gets it | One outlet | Multiple outlets |
| Tradeoff | Better story quality | More coverage volume |
| Risk | Outlet passes | Leak |
| Best for | Big narrative stories | Product launches |

## Wire Services

### When to Use
**Use wire (PRNewswire, BusinessWire, GlobeNewswire) for:**
- Public company disclosures (required)
- Announcements requiring broad pickup (funding, partnerships)
- SEO value of syndicated links

**Skip wire for:**
- Most startup announcements (organic pitch converts better)

### Cost Guidance
- PRNewswire national: $800–$2,000 per release
- BusinessWire: Similar range
- Accesswire: Budget option ~$300–$500

## HARO / Connectively Usage

### High-Response Pitch Format
```
Hi [Reporter name],

[Credentials: I'm the [title] at [company], [relevant expertise].]

[Direct answer to their question — 2-4 sentences, specific and quotable]

[Optional: supporting data point or example]

Available for follow-up at [email/phone].

[Name], [Title], [Company]
```

### Workflow
1. Subscribe to daily emails (3x/day) at helpareporter.com
2. Scan within 1 hour of receipt — speed matters
3. Reply within 2-3 hours with focused, quotable answer
4. Track placements and follow up to build relationships

## Crisis PR Basics

### Golden Hour Protocol (first 60 minutes)
1. Confirm facts internally — do not guess
2. Assemble: CEO, legal, comms, relevant exec
3. Draft holding statement: acknowledge + "we're investigating" + ETA for update
4. Identify single spokesperson
5. Post on owned channels before media calls

### Holding Statement Template
```
We are aware of [situation]. The safety/security/wellbeing of
[customers/users/employees] is our top priority. We are actively
investigating and will provide an update by [specific time].
```

### What Not to Do
- Do not say "no comment" — implies guilt
- Do not speculate on cause before investigation
- Do not let multiple people speak to media
- Do not delete social posts — screenshots exist

## Thought Leadership Pipeline

### Owned → Earned Flywheel
1. Publish data/research on your blog
2. Pitch the findings to relevant reporters
3. Reference the coverage in future outreach ("as seen in X")
4. Reporters now know you have data — future pitches convert higher

### Byline Placement
- Target vertical trade publications and mid-tier outlets first
- Pitch the article idea first, not the finished piece
- Length: typically 600-900 words
- Disclosure: mention your company once, not a billboard

## PR Metrics

| Metric | How to measure |
|--------|---------------|
| Share of Voice | Mention % vs competitors (Mention.com, Brandwatch) |
| Coverage quality | DA/authority of placing outlets (Ahrefs) |
| Referral traffic | GA4 → Acquisition → Referral → filter by press outlets |
| Backlinks | Ahrefs site explorer → new backlinks |
| Tier 1 placements | Count of T1 outlet hits per quarter |
| Sentiment | Positive / Neutral / Negative ratio |
