---
name: onboarding-email-sequence-writer
description: |
  Writes complete onboarding email sequences mapped to the activation
  milestone — welcome, quick-win catalyst, setup shepherd, social proof,
  activation nudge — with behavioral triggers, segmentation logic, and
  copy ready to drop into Customer.io, Klaviyo, HubSpot, or ActiveCampaign.
  Use when the user says "write me an onboarding email sequence", "build
  a welcome series", "create a new-customer nurture for [product]",
  "reduce trial drop-off", or "improve activation". Email-channel
  onboarding specifically — for full multi-channel post-purchase
  experience design use post-sale-delight-engineer.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="onboarding-email-sequence-writer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — specifically ICA profiles, brand voice guidelines, product/service details, known activation milestones, and any prior onboarding sequence performance data.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Product/service overview** — What is the user being onboarded into? (SaaS platform, membership, course, service engagement, etc.)
- **ICA definition** — Who is the new user? Role, sophistication level, primary pain point at moment of purchase, and expected outcome.
- **Activation milestone** — What is the single action that, once completed, correlates most strongly with long-term retention? (e.g., "completes first project," "invites a team member," "uploads first dataset")
- **Current sequence** — Share any existing onboarding emails, or confirm this is net-new.
- **Sequence parameters** — Desired number of emails, cadence constraints, sending platform (for any technical formatting considerations).
- **Known friction points** — Where do new users currently drop off, get confused, or submit support tickets?
- **Brand voice and tone** — Formal, conversational, bold, understated? Share examples or reference materials if available.

If FutureProof context already supplies answers to any of the above, confirm them with the user rather than re-asking.

## Step 3: Map the Onboarding Journey Architecture

Before writing a single email, construct the **Onboarding Journey Map** — a structured framework that ensures every email earns its place in the sequence:

### 3a. Define the Value Realisation Timeline

Plot the critical path from sign-up to activation milestone:

1. **Moment Zero** — Purchase/sign-up (emotional peak: excitement + uncertainty)
2. **First Value Touch** — The smallest possible win the user can achieve in < 5 minutes
3. **Core Setup Actions** — 2–4 configuration or orientation steps required before the product delivers ongoing value
4. **Activation Milestone** — The defined "aha moment" that predicts retention
5. **Social Proof Gate** — The point where the user has enough experience to appreciate testimonials and case studies from similar ICAs

### 3b. Identify Behavioural Triggers and Segmentation Logic

For each email in the sequence, define:
- **Send condition** — Time-based, behaviour-based, or hybrid trigger
- **Assumed user state** — What has the user likely done (or not done) by this point?
- **Emotional state** — Excitement, confusion, impatience, buyer's remorse, momentum
- **Primary barrier** — The single biggest reason a user at this stage would disengage

### 3c. Assign Email Archetypes

Map each position in the sequence to one of the following proven onboarding archetypes:

| Archetype | Purpose | Typical Position |
|---|---|---|
| **Welcome & Orient** | Reduce overwhelm, set expectations, deliver first micro-win | Email 1 |
| **Quick Win Catalyst** | Guide user to first tangible value in one focused action | Email 2 |
| **Setup Shepherd** | Walk through a specific setup step with friction-reducing clarity | Emails 3–4 |
| **Social Proof Bridge** | Show ICA-matched success story at the moment doubt peaks | Email 4–5 |
| **Activation Nudge** | Direct, specific push toward the activation milestone with urgency framing | Email 5–6 |
| **Expansion Teaser** | Introduce an advanced feature or use case to deepen engagement | Email 6–7 |
| **Feedback & Relationship** | Ask for input, open dialogue, humanise the brand | Final email |

## Step 4: Write the Email Sequence

Draft each email with the following structure and standards:

### Per-Email Deliverable Format

For each email, provide:

- **Email #[N]: [Internal Name]** (e.g., "Email #2: Quick Win — Create Your First Dashboard")
- **Archetype**: [from table above]
- **Send trigger**: [time-based and/or behavioural condition]
- **Subject line**: Primary + one A/B variant
- **Preview text**: 40–90 characters, complements (not repeats) the subject line
- **Body copy**: Full draft, formatted for email (short paragraphs, single-column logic)
- **Primary CTA**: One clear, specific call to action — button text + destination
- **Secondary CTA** (if applicable): Lower-commitment alternative for hesitant users
- **Design notes**: Layout guidance, image/GIF suggestions, mobile considerations

### Writing Standards Applied Across All Emails

1. **One email = one job** — Each email has exactly one primary objective. No multi-purpose emails.
2. **ICA mirroring** — Use the vocabulary, mental models, and aspiration language of the ICA, not internal product jargon.
3. **Specificity over motivation** — Every CTA tells the user exactly what to do, how long it takes, and what they gain. ("Click here to set up your first automation — takes 90 seconds" not "Get started!")
4. **Progressive disclosure** — Never expose complexity before the user needs it. Sequence information in the order the user encounters it.
5. **Friction acknowledgement** — Name the barrier before offering the solution. ("If you're staring at an empty dashboard wondering where to start — here's the exact first step.")
6. **Proof placement** — Position testimonials and results from ICAs in the same segment, at the moment where doubt is highest (typically emails 4–5).
7. **Unsubscribe empathy** — Footer copy that respects the reader and maintains brand integrity.

Apply any user-specific `instructions` from FutureProof context (brand voice, compliance requirements, formatting rules, tone preferences) as overrides to default standards.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Deliver Output

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Produce the following structured deliverables:

### Deliverable 1: Onboarding Sequence Strategy Brief
A one-page summary containing:
- **ICA snapshot** — Who this sequence is written for
- **Activation milestone** — The target behaviour
- **Sequence overview** — Number of emails, total cadence duration, trigger logic summary
- **Key strategic decisions** — Rationale for archetype ordering, cadence choices, and segmentation recommendations

### Deliverable 2: Full Email Sequence Document
All emails in the per-email format defined in Step 4, presented in send order. Each email is production-ready copy requiring only brand asset insertion and platform configuration.

### Deliverable 3: Sequence Performance Scorecard
Rate the completed sequence against the following dimensions (1–10):

| Dimension | Score | Rationale |
|---|---|---|
| **Time-to-first-value** | | How quickly the sequence delivers a tangible win |
| **Activation path clarity** | | How unmistakably the sequence drives toward the activation milestone |
| **ICA language fidelity** | | How precisely copy mirrors the ICA's vocabulary and mental models |
| **Friction pre-emption** | | How effectively known drop-off points are addressed before they occur |
| **Emotional arc coherence** | | How well the sequence manages the emotional journey from excitement through doubt to momentum |
| **CTA specificity** | | How concrete and low-friction every call to action is |
| **Proof density and placement** | | How strategically social proof is deployed at high-doubt moments |

### Deliverable 4: Implementation Checklist
- Platform setup steps (list, segment, automation triggers)
- Required assets (images, GIFs, links, tracking parameters)
- Recommended send-time windows based on ICA behaviour patterns
- QA checklist (link testing, mobile rendering, personalisation token fallbacks)

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="onboarding-email-sequence-writer", experiment={
  hypothesis: "Sending the Quick Win Catalyst email within 30 minutes of sign-up (behaviour-triggered) instead of at 24 hours (time-triggered) reduces drop-off before first value event",
  variants: ["control: Email #2 sent at T+24 hours", "variant: Email #2 sent 30 minutes after sign-up if activation milestone not yet reached"],
  measurement: "Activation milestone completion rate within 7 days of sign-up, email open rate and CTA click-through rate for Email #2",
  expected_impact: "20% increase in activation milestone completion within first week"
})
```

```
FutureProof:save_experiment(skill="onboarding-email-sequence-writer", experiment={
  hypothesis: "Subject lines that name the specific next action outperform curiosity-gap subject lines in onboarding emails (where user intent is already established)",
  variants: ["control: curiosity-driven subject lines across sequence", "variant: action-specific subject lines (e.g., 'Your first [deliverable] in 90 seconds')"],
  measurement: "Open rate, click-through rate, and activation milestone completion rate across full sequence",
  expected_impact: "12% improvement in average sequence click-through rate"
})
```

## Step 7: Request Research

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:request_research(skill="onboarding-email-sequence-writer",
  query="Latest benchmarks on SaaS and digital product onboarding email sequence performance: optimal cadence, open rates by email position, activation correlation data, and behavioural trigger vs. time-based send performance comparisons 2024–2025",
  reason="Ensure sequence cadence, send-trigger strategy, and performance expectations are calibrated against current industry data and evolving inbox behaviour patterns"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="onboarding-email-sequence-writer", session={
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