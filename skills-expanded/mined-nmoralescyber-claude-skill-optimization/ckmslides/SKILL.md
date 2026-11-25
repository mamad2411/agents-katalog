---
name: ckmslides
description: Creates strategic HTML/web presentations with Chart.js, design tokens, responsive layouts, copywriting frameworks, and contextual slide strategies. Make sure to use this skill whenever the user says build a slide deck, create a presentation, design slides for [meeting], make a web-based deck, build a presentation with charts, design board slides, build investor slides, design customer presentation, or describes any multi-slide presentation work where the output is HTML (not PowerPoint .pptx — use anthropic-skills:pptx for that). Specializes in cybersecurity-context decks (board updates with risk metrics, customer presentations with trust signals, investor decks for security companies, technical architecture presentations). Includes copywriting frameworks (problem-solution-proof, before-after-bridge, AIDA), slide structures by meeting type, chart selection guidance, and design token integration. Do NOT use for: PowerPoint .pptx file creation (use anthropic-skills:pptx), single-page collateral (use create-one-pager), interactive product demos (use create-workflow-demo), or full multi-slide sales decks tied to a specific deal context (use create-deck — though this skill produces the slides, create-deck wraps it in deal-specific framing).
---

# Strategic Web Presentations

HTML-based presentation decks with Chart.js, design tokens, responsive layouts, and contextual slide strategies.

## When to use vs. adjacent skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Output is HTML (browser-rendered presentation) | Output must be .pptx file → `anthropic-skills:pptx` |
| Multi-slide deck with embedded charts | Single-page collateral → `create-one-pager` |
| Generic deck or technical-architecture deck | Sales deck wrapped in specific deal context → `create-deck` (which then often invokes this skill for the slides themselves) |
| Web-deployable deck (shareable URL) | Interactive product walkthrough → `create-workflow-demo` |

## Output format: web HTML, not PowerPoint

This skill produces HTML decks. Why HTML over .pptx for many use cases:

- **Shareable as URL** — no file download
- **Live data integration** — slides can pull current metrics
- **Interactive elements** — charts respond to hover, click-throughs work
- **Version control** — Markdown source diffs cleanly
- **Embeds anywhere** — iframe in product, blog, email
- **Responsive** — works on laptop, tablet, phone

When .pptx is the right answer:
- Recipient must edit the file in PowerPoint/Keynote
- Compliance requires .pptx (some enterprises do)
- Offline presentation in venues with no internet
- Investor docs that need to embed in board books

For .pptx, route to `anthropic-skills:pptx`. This skill is for HTML.

## Deck types this skill handles

### Board update deck
Audience: board members, quarterly cadence usually.

Standard structure (10-15 slides):
1. Cover — quarter, company, date
2. Executive summary — 5 bullets max
3. KPI dashboard — 6-9 numbers with trends
4. Wins this quarter — 3-5 specific, customer-grade examples
5. Losses / challenges — 2-3, with root cause and learning
6. Financials snapshot — revenue, burn, runway, growth metrics
7. Customer pipeline / customer health — depending on stage
8. Team — hires, departures, key changes
9. Risks — current top 3, with mitigation
10. Asks of the board — specific, actionable
11. Next quarter focus — 3-5 priorities

For cybersecurity / security-product companies, add:
- Security incident summary (none / count by severity / RCA links)
- Compliance program status (SOC 2 / ISO progress)
- Customer trust events (security questionnaires, pen tests, audits)

### Investor deck (web-shareable version)
Audience: prospective investors, sent as URL after meeting or for screening.

Same structure as the .pptx version but optimized for async consumption:
- Sticky nav for skipping around
- Embedded video (founder intro, product demo)
- Live data (if metrics will be current at time of viewing)
- Click-through to deeper resources (financial model, customer call recording, technical brief)

### Customer presentation deck
Audience: existing customer in a QBR, expansion conversation, or executive briefing.

Standard structure (8-12 slides):
1. Cover — both logos, meeting date, attendees
2. Outcomes delivered — what we did for them last period
3. Their KPIs / our contribution to them
4. Roadmap from us — what's coming that benefits them
5. Their roadmap — what they shared, our alignment
6. Expansion / value adds — modules, seats, use cases
7. Health check — utilization, satisfaction, risks
8. Asks — referrals, case study, intros, expansions
9. Next steps + commitments

### Technical architecture deck
Audience: engineering, security, IT decision-makers; sometimes auditors.

Standard structure (10-20 slides):
1. Cover + scope
2. System overview — high-level architecture diagram
3. Data flow — request lifecycle, encryption boundaries
4. Authentication & authorization architecture
5. Network architecture
6. Data residency and storage
7. Encryption (at rest, in transit, key management)
8. Logging & audit
9. Incident response architecture
10. Disaster recovery / business continuity
11. Compliance mapping (SOC 2 / ISO / GDPR / etc.)
12. Sub-processors and third-party dependencies
13. Common questions / FAQ

### Webinar deck
Audience: registered attendees, often educational mid-funnel.

Standard structure (15-25 slides for a 30-min webinar):
1. Title + speaker
2. Agenda (set expectations)
3. Speaker credentials (brief, earn trust)
4. The problem (5-7 slides, depth matters)
5. The solution framework (vendor-neutral if possible — earn credibility)
6. Case study or example (3-5 slides, specific)
7. Practical takeaways (3-5 slides)
8. Q&A teaser
9. CTA / next step

## Slide design principles

### 1. One idea per slide
If a slide has two ideas, it's two slides.

### 2. Slide title = the takeaway
Not "Q4 Revenue" but "Q4 revenue beat plan by 23% on enterprise expansion."

### 3. Visuals over text
A chart, diagram, or image with one sentence beats a paragraph.

### 4. Speaker notes carry the depth
The slide is the prompt. The speaker notes are the script. Don't put the script on the slide.

### 5. Reveal progressively when needed
For complex slides, build content step-by-step (click-through) rather than dumping everything at once.

### 6. Consistency across the deck
Same fonts, same color palette, same chart style, same image treatment. Inconsistent decks signal cobbled-together.

### 7. Print-friendly fallback
For decks that may be printed (board, customer leave-behind), test print preview. Avoid backgrounds that bleed off-page.

## Copywriting frameworks for slides

### Problem-Solution-Proof
For demo slides, capability slides:
- The problem (specific, stated in customer language)
- The solution (your capability)
- The proof (data, customer outcome, demo)

### Before-After-Bridge
For transformation pitches:
- Before (their current world, painful)
- After (their world with you, better)
- Bridge (how you get them there)

### AIDA (Attention-Interest-Desire-Action)
For persuasive sales/marketing:
- Attention (hook)
- Interest (relevance to them)
- Desire (specific outcome)
- Action (next step)

### STAR (Situation-Task-Action-Result)
For customer story slides:
- Situation (the customer's context)
- Task (what they needed)
- Action (what you did)
- Result (quantified outcome)

## Chart selection for slide context

Chart picks differ from product UI because slides are read in 5-10 seconds:

| Trying to show | Best slide chart |
|---|---|
| Trend over time | Line (1-3 series max) |
| Big-number with trend | Hero KPI with arrow indicator |
| Comparison (5-10 items) | Horizontal bar |
| Composition | Stacked horizontal bar (avoid pie for 4+ slices) |
| Process / flow | Flow diagram or waterfall |
| Geographic | Map with annotations on key locations |
| Funnel | Funnel chart or stacked bar |
| Distribution (rare in slides) | Histogram |

Slide chart anti-patterns:
- 3D pie charts (banned)
- Charts with 8+ data series
- Default Excel chart styling (looks lazy)
- Tiny axis labels
- Logarithmic scale without explanation
- Charts requiring legend lookup (label inline)

## Design token integration

For decks that match an existing brand:
- Read the brand's design tokens (often shared with `ckmui-styling` or `ckmdesign`)
- Apply: brand color primary, brand typography, brand iconography
- Charts use the brand color palette

For brand-less decks (early-stage, internal):
- Default: clean sans-serif (Inter), neutral palette (slate + white + brand accent), Chart.js defaults

## Output

Produces:
1. **HTML deck file** — single self-contained HTML or multi-file structure
2. **Speaker notes** — separate from slide content, scriptable
3. **Asset list** — images, logos, charts the deck depends on
4. **Embed instructions** — how to share (direct URL, iframe, PDF export)
5. **Optional .pptx export** — chains to anthropic-skills:pptx if the user needs PowerPoint after
