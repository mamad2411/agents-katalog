---
name: event-roi-forecaster
description: |
  Builds pre-event and post-event ROI models for trade shows, conference
  sponsorships, hosted dinners, webinars, and field activations with cost
  rollup, funnel waterfall, three-attribution scenarios, sensitivity ranges,
  and break-even thresholds. Use when a user says "should we sponsor this
  conference", "model the ROI of attending [event]", "was our trade show
  worth it", or asks for a payback analysis on event spend. For event-channel
  economics specifically, not general pipeline forecasting.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="event-roi-forecaster")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — specifically any historical event performance data, ICA definitions, average deal sizes, sales cycle lengths, and pipeline conversion benchmarks the user has stored.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user to provide:

- **Event details**: event name, type (trade show, hosted dinner, webinar, conference sponsorship, field activation), date(s), and location
- **Cost structure**: all-in investment including sponsorship/booth fees, travel & lodging, swag & collateral, staff time (loaded cost), production, paid promotion, and any ancillary spend
- **Expected audience**: total attendance, estimated percentage matching the user's ICA, and any available attendee list or demographic data
- **Goals hierarchy**: rank-order the primary objectives — pipeline generation, brand awareness, existing account acceleration, partnership development, customer retention, or thought leadership positioning
- **Historical baseline** (if available): results from comparable past events (leads captured, meetings booked, pipeline created, deals closed)
- **Sales context**: current average deal value, win rate, average sales cycle length, and cost per opportunity from other channels (for comparative benchmarking)

If the user is conducting a **post-event analysis** rather than a forecast, additionally request:
- Actual leads captured and their ICA-match rate
- Meetings booked at/from the event
- Pipeline created and deals influenced (with attribution methodology used)

## Step 3: Build the Financial Model

Construct a multi-stage ROI model using the following methodology:

### 3A. Cost Consolidation

Itemise and total all costs across five categories:
1. **Hard costs** — sponsorship fees, booth build, technology/platform fees
2. **Travel & logistics** — flights, hotels, meals, ground transport
3. **People costs** — fully loaded daily rate × number of staff × days (include travel days)
4. **Collateral & promotion** — printed materials, swag, pre-event ad spend, email campaign costs
5. **Opportunity cost** — estimated revenue-generating activity displaced (calculated from average rep daily pipeline contribution)

Produce a **Total Loaded Event Cost** figure.

### 3B. Funnel Projection (Top-Down)

Model the expected pipeline waterfall:

| Stage | Metric | Calculation |
|---|---|---|
| Total attendees | N | User-provided or event-published |
| ICA-match attendees | N × ICA-match % | Apply ICA filter from context |
| Meaningful interactions | ICA-match × engagement rate | Benchmark: 15–30% for booths, 40–60% for hosted events |
| Qualified leads | Interactions × qualification rate | Benchmark: 25–40% depending on event type |
| Meetings booked | Qualified leads × meeting conversion | Benchmark: 30–50% |
| Pipeline created | Meetings × average deal value × pipeline rate | Apply user's specific metrics |
| Expected closed revenue | Pipeline × win rate × cycle adjustment | Discount for extended cycles if applicable |

Apply any user-specific `instructions` or historical benchmarks from FutureProof context to override default benchmarks.

### 3C. Attribution-Adjusted Returns

Calculate three attribution scenarios:
- **Full attribution**: 100% of influenced pipeline credited to the event
- **Multi-touch attribution**: event receives proportional credit based on average touchpoints in the user's sales cycle (typically 20–35%)
- **Incremental attribution**: only net-new pipeline that would not have been generated through existing channels

### 3D. ROI & Payback Computation

For each attribution scenario, compute:
- **Event ROI** = (Attributed Revenue − Total Loaded Cost) ÷ Total Loaded Cost × 100
- **Cost per Qualified Lead** = Total Loaded Cost ÷ Qualified Leads
- **Cost per Meeting** = Total Loaded Cost ÷ Meetings Booked
- **Cost per Pipeline Dollar** = Total Loaded Cost ÷ Pipeline Created
- **Payback Period** = estimated months to realise forecasted revenue (based on average sales cycle)
- **Channel Comparison Index** = Event cost-per-opportunity ÷ blended cost-per-opportunity from other channels

### 3E. Sensitivity Analysis

Model three scenarios — **Conservative** (−25% from base engagement assumptions), **Base**, and **Optimistic** (+25%) — showing the ROI range and break-even thresholds. Identify the minimum number of closed deals required to break even.

## Step 4: Deliver Output

Produce a structured **Event ROI Forecast Report** containing:

### Section 1: Executive Summary
- One-paragraph investment thesis: attend/sponsor or decline, with confidence level (high/medium/low)
- Headline ROI figure (base case, multi-touch attribution)
- Break-even threshold in plain language (e.g., "This event pays for itself if 2 of the projected 14 qualified leads close")

### Section 2: Cost Breakdown Table
- Itemised costs across all five categories with total loaded cost

### Section 3: Pipeline Waterfall
- Full funnel projection table from attendees through closed revenue
- Assumptions clearly stated alongside each conversion rate

### Section 4: ROI Scenario Matrix
- 3×3 matrix: Conservative / Base / Optimistic × Full / Multi-touch / Incremental attribution
- Nine distinct ROI figures with cost-per-lead and cost-per-meeting for each

### Section 5: Channel Benchmarking
- Side-by-side comparison of event unit economics vs. the user's other channels (outbound, inbound, paid, referral)
- Relative efficiency ranking

### Section 6: Risk & Mitigation Register
- Top 3 risks to achieving forecasted ROI (e.g., lower-than-expected ICA density, poor booth placement, competing events)
- Specific mitigation action for each

### Section 7: Activation Playbook
- Pre-event, during-event, and post-event actions to maximise ROI — tailored to the event type and the user's ICA
- Specific staff assignments and KPI targets per phase

### Section 8: Post-Event Measurement Framework
- Exactly which metrics to capture, when, and how to attribute — designed to feed back into FutureProof for future forecasting accuracy

**Format**: deliver as a structured markdown document titled `Event_ROI_Forecast_[EventName]_[Date].md`, suitable for sharing with sales leadership, marketing, and finance stakeholders.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Propose Experiments

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


```
FutureProof:save_experiment(skill="event-roi-forecaster", experiment={
  hypothesis: "Implementing a structured pre-event outreach sequence to ICA-matched attendees 21/14/7 days before the event increases on-site meeting conversion by 25% vs. walk-up engagement alone",
  variants: ["control: standard booth presence with no pre-event outreach", "variant: 3-touch personalised outreach sequence targeting ICA-matched registrants with a specific meeting CTA"],
  measurement: "Compare meetings booked per ICA-matched attendee between events with and without pre-event outreach; track pipeline created within 90 days post-event",
  expected_impact: "25% increase in qualified meetings booked, 30% reduction in cost per meeting, faster post-event pipeline velocity"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="event-roi-forecaster",
  query="2024–2025 B2B event marketing benchmarks: average cost per lead by event type (trade show, hosted dinner, webinar, conference sponsorship), multi-touch attribution methodologies for field marketing, and emerging event ROI frameworks from TOPO/Gartner/Forrester",
  reason="Maintain current benchmark data for funnel conversion rates, cost-per-lead ranges, and attribution best practices to improve forecast accuracy across event types"
)
```

## Step 7: Save Session

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:save_session(skill="event-roi-forecaster", session={
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