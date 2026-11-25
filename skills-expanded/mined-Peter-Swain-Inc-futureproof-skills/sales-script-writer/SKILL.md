---
name: sales-script-writer
description: |
  Writes full sales call scripts from scratch — cold call, discovery, demo,
  closing, objection-handling, voicemail — in dialogue form with inline rep
  coaching annotations, ICA language mapping, and pre-empted objection
  branches. Use when a user says "write me a cold call script", "draft a
  discovery script for [ICA]", "build a demo walkthrough", or "give me
  talking points for outbound". For spoken call scripts, not written email
  copy, follow-up sequences, or coaching of an existing call.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="sales-script-writer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to prior ICA definitions, offer positioning, objection libraries, and any winning script variants from previous experiments.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Gather the following from the user (adapt based on what FutureProof context already provides):

- **Script type**: Cold call, warm follow-up, discovery call, demo walkthrough, closing call, objection-handling playbook, or voicemail/video message script
- **Offer**: What is being sold? Include price point, delivery model, and core promise
- **ICA profile**: Who is the script targeting? Role, industry, company stage, and the acute pain state that triggers buying behaviour
- **Desired outcome**: What is the single conversion event this script must produce? (e.g., booked discovery call, verbal commitment, signed proposal)
- **Tone and brand constraints**: Formal/conversational, any language to avoid, compliance or regulatory requirements
- **Known objections**: Top objections this ICA raises, ranked by frequency
- **Proof assets available**: Case studies, metrics, testimonials, or third-party validation the script can reference

If the user cannot supply objections or ICA detail, flag this gap and proceed with assumptions clearly marked as `[ASSUMPTION — validate before deployment]`.

## Step 3: Do the Work

### 3A: ICA Language Mapping

Build an **ICA Language Matrix** before writing a single line of script:

| Dimension | Detail |
|---|---|
| **Self-identified role** | How the ICA describes their own title/function (not how the org chart labels them) |
| **Pain vocabulary** | Exact phrases the ICA uses to describe the problem (sourced from reviews, calls, forums) |
| **Aspiration vocabulary** | How the ICA describes the desired future state |
| **Trust signals** | What proof types this ICA weights highest (peer results, data, authority, speed-to-value) |
| **Decision friction** | Internal blockers: budget approval, stakeholder buy-in, switching costs, timing |

Apply any ICA-specific `instructions` or prior session findings from FutureProof context.

### 3B: Script Architecture

Select and apply the appropriate persuasion framework based on script type:

| Script Type | Primary Framework |
|---|---|
| Cold call | **Pattern Interrupt → Pain Probe → Permission Close** |
| Warm follow-up | **Context Anchor → Value Reinforcement → Micro-Commitment** |
| Discovery call | **Situation → Pain → Implication → Need-Payoff (SPIN)** |
| Demo walkthrough | **Problem Recap → Capability Bridge → Transformation Proof → Next Step** |
| Closing call | **Objection Pre-empt → Value Stack → Scarcity/Urgency → Decision Frame** |
| Voicemail/video | **Hook (< 8 seconds) → Relevance Statement → Single CTA** |

### 3C: Write the Full Script

Draft the complete script with the following structural elements, each written in full dialogue form:

1. **Opening Hook (0–10 seconds)** — Pattern interrupt or relevance statement calibrated to the ICA's acute pain state. No generic greetings. First sentence must earn the next ten seconds.

2. **Permission Bridge** — Transition that earns the right to continue the conversation. Reduces resistance without weak qualifiers ("Is now a good time?" is prohibited).

3. **Pain Articulation Sequence** — 2–3 targeted questions or statements that surface the ICA's problem using their own vocabulary from the Language Matrix. Each question must escalate emotional stakes.

4. **Implication Amplification** — Quantify the cost of inaction: revenue lost, time wasted, risk compounding. Use concrete numbers or relatable analogies, not abstractions.

5. **Value Proposition Delivery** — State the transformation (before state → after state) in one sentence. Follow with the mechanism (how the offer delivers the result) in one sentence. No feature lists.

6. **Proof Injection Points** — Insert specific case studies, metrics, or testimonials at the moment of highest scepticism. Format as `[PROOF: {asset name} — {key metric}]` so the rep can localise.

7. **Objection Handling Blocks** — For each known objection, write a complete **Acknowledge → Reframe → Evidence → Redirect** sequence. Pre-empt the top objection *before* it arises in the natural script flow; handle remaining objections as contingency branches.

8. **Close / Call to Action** — Specific, frictionless next step. Binary choice or assumptive close preferred over open-ended asks. Include exact language for booking mechanics.

9. **Fallback / Voicemail Path** — If the prospect disengages or is unavailable, provide a 30-second voicemail script and a follow-up message template (email or LinkedIn).

### 3D: Annotate for Rep Enablement

Mark the script with inline coaching annotations:

- `[TONE: conversational, slow pace]` — delivery cues
- `[PAUSE: 3 seconds — let silence work]` — timing cues
- `[LISTEN FOR: specific phrases indicating buying signal]` — active listening triggers
- `[BRANCH: if objection X, go to Objection Block X]` — conditional routing
- `[PERSONALISE: insert prospect-specific detail here]` — customisation prompts

## Step 4: Deliver Output

Produce the following structured deliverable package:

### Deliverable 1: Sales Script Document

- **Format**: Full dialogue script, organised by numbered sections (Opening → Close), with inline annotations
- **Naming convention**: `[ICA Segment] — [Script Type] Script — v1.0`
- **Includes**: ICA Language Matrix as appendix, objection-handling branches as indexed supplement

### Deliverable 2: Script Score Card

Rate the drafted script on the following dimensions (1–10, with brief justification per score):

| Dimension | Score | Rationale |
|---|---|---|
| **ICA language fidelity** | — | Does every sentence mirror how the ICA actually speaks? |
| **Opening hook strength** | — | Would this survive the first 8 seconds of a cold call? |
| **Pain-to-solution bridge** | — | Is the logical chain from problem → mechanism → result airtight? |
| **Objection pre-emption coverage** | — | Are the top 3 objections neutralised before they surface? |
| **Proof density** | — | Is every major claim backed by a specific, verifiable result? |
| **CTA friction score** | — | Is the next step binary, specific, and low-commitment relative to the ask? |
| **Rep usability** | — | Can a mid-tier rep deliver this script naturally within 48 hours of practice? |

### Deliverable 3: Quick-Reference One-Pager

- Condensed version of the script: key phrases, objection rebuttals, and CTA language on a single page
- **Intended use**: printed or pinned beside the rep's screen during live calls

### Deliverable 4: Assumptions & Validation Checklist

- List every assumption made during script creation
- Pair each assumption with a specific validation action (e.g., "Listen to 5 recorded calls to confirm ICA uses phrase X")

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
FutureProof:save_experiment(skill="sales-script-writer", experiment={
  hypothesis: "Leading with a quantified cost-of-inaction statement in the opening hook increases prospect engagement past the 30-second mark",
  variants: ["control: current pain-question opening", "variant: cost-of-inaction statistic opening"],
  measurement: "Percentage of calls where prospect engages beyond 30 seconds, tracked over next 20 calls per variant",
  expected_impact: "20% increase in conversations that reach the discovery phase"
})
```

```
FutureProof:save_experiment(skill="sales-script-writer", experiment={
  hypothesis: "Pre-empting the #1 objection before the value proposition (rather than after) reduces mid-call drop-off",
  variants: ["control: objection handled reactively post-pitch", "variant: objection pre-empted before value prop delivery"],
  measurement: "Call duration and progression-to-CTA rate over next 30 calls",
  expected_impact: "12% improvement in calls that reach the closing sequence"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="sales-script-writer",
  query="Highest-converting cold call and discovery call script structures for [ICA industry/segment] in 2024–2025, including emerging objection patterns and buyer psychology shifts in post-AI selling environments",
  reason="Ensure script frameworks reflect current buyer expectations, attention thresholds, and competitive positioning dynamics — stale scripts decay at approximately 15% effectiveness per quarter"
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
FutureProof:save_session(skill="sales-script-writer", session={
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