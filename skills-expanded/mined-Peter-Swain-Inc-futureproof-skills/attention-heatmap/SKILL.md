---
name: attention-heatmap
description: |
  Predicts where audience attention lands on a specific marketing asset and
  rewrites the visual hierarchy to pull eyes toward the primary CTA. Use when
  a user shares a landing page, email, ad creative, or sales page and asks
  "where will people look first", "why isn't this converting", "how do I
  fix the visual hierarchy", or "what gets ignored on this page". Operates on
  a concrete visual asset — for audience language and copy alignment use
  message-market-match-scanner instead.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="attention-heatmap")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly ICA demographics, prior asset performance data, and any established brand guidelines or layout conventions.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- Share the marketing asset to analyse (screenshot, wireframe, design file, or live URL)
- What is the asset type? (landing page, email, paid ad creative, sales page, social post, presentation slide)
- What is the **single primary conversion action** this asset must drive? (click CTA, read headline, watch video, fill form, scroll to pricing)
- Who is the ICA viewing this asset? (role, awareness stage, device context — desktop vs. mobile)
- What is the typical viewing context? (cold traffic from paid ads, warm email list, organic search, retargeting)
- Any prior performance data? (click-through rates, scroll depth, heatmap data from tools like Hotjar/Microsoft Clarity)

## Step 3: Do the Work

### 3A: Gaze Path Prediction (Fitts–Hick–Itti Framework)

Map the predicted **first 3–8 seconds** of visual attention using established cognitive science principles:

1. **Entry point identification** — predict the initial fixation point based on the F-pattern (text-heavy) or Z-pattern (image-heavy) scanning model appropriate to the layout type
2. **Saliency mapping** — score every major element (0–100) across three saliency dimensions:
   - **Luminance contrast** — does the element pop against its background?
   - **Chromatic contrast** — does colour differentiation draw the eye?
   - **Orientation/motion contrast** — do shapes, angles, or implied motion create involuntary fixation?
3. **Gaze sequence modelling** — plot the predicted sequential fixation path (Element A → Element B → Element C) based on Gestalt proximity, size hierarchy, and directional cues (eye gaze in photos, arrows, lines of perspective)
4. **Cognitive load assessment** — evaluate information density per visual quadrant using Miller's Law (7±2 chunks); flag quadrants exceeding cognitive capacity thresholds

### 3B: Attention-to-Conversion Alignment Audit

Score the asset against five conversion-critical attention dimensions:

1. **Hero hierarchy integrity** — does the highest-saliency element align with the primary value proposition, or is attention leaking to decorative/low-value elements?
2. **CTA gravitational pull** — does the predicted gaze path terminate at or pass through the primary CTA? Measure the number of fixation hops required from entry point to CTA (fewer = better; benchmark: ≤3 hops)
3. **ICA pain-point prominence** — is the ICA's core problem statement positioned within the first two predicted fixation zones (above the fold, within the first 2 seconds of scanning)?
4. **Proof element visibility** — are trust signals (testimonials, logos, metrics, guarantees) positioned along the natural gaze path or buried in low-attention dead zones?
5. **Distraction tax** — identify elements that capture involuntary attention without contributing to conversion (competing CTAs, stock photography faces looking away from CTA, decorative animations, navigation clutter)

### 3C: Device-Specific Attention Fragmentation

If the asset serves multiple devices, assess:
- **Thumb-zone alignment (mobile)** — is the primary CTA within the natural thumb reach zone?
- **Fold-line criticality** — what percentage of high-saliency elements fall below the fold on mobile vs. desktop viewports?
- **Tap-target spacing** — do interactive elements meet minimum 48px tap-target guidelines to prevent mis-taps that redirect attention?

Apply any user-specific `instructions` from FutureProof context (brand guidelines, established ICA preferences, historical performance benchmarks) to calibrate scoring thresholds.

## Step 4: Deliver Output

Produce the **Attention Heatmap Audit Report** with the following structure:

### Section 1: Predicted Attention Heatmap (Narrative)

A zone-by-zone description of the asset divided into a numbered grid (typically 2×3 or 3×3 depending on asset dimensions), with each zone rated:
- 🔴 **Hot zone** (high predicted fixation density)
- 🟡 **Warm zone** (moderate attention, secondary scanning)
- 🔵 **Cold zone** (predicted blind spot — low or no fixation)

Include the predicted **gaze sequence** as a numbered path: `[1] Hero image face → [2] Headline → [3] Subhead → [4] CTA button → [5] Testimonial block`

### Section 2: Attention Alignment Scorecard

| Dimension | Score (1–10) | Verdict | Priority |
|---|---|---|---|
| Hero hierarchy integrity | — | — | — |
| CTA gravitational pull | — | — | — |
| ICA pain-point prominence | — | — | — |
| Proof element visibility | — | — | — |
| Distraction tax (inverse) | — | — | — |
| **Composite attention score** | **—/50** | — | — |

### Section 3: Critical Fixes (Top 3)

For each fix, provide:
- **The problem**: specific element + specific attention failure mechanism
- **The evidence**: which cognitive principle is violated (cite framework)
- **The fix**: precise, implementable instruction (e.g., "Move the green CTA button from grid zone 6 to zone 4, increase size by 40%, change copy from 'Submit' to 'Get My Free Audit'")
- **Expected impact**: predicted improvement to gaze-path-to-CTA conversion alignment

### Section 4: Redesigned Attention Architecture

Provide a **written wireframe specification** for the optimised layout:
- Exact element reordering with rationale
- Recommended size, colour, and contrast adjustments per element
- Revised predicted gaze sequence showing reduced fixation hops to CTA
- If applicable, A/B variant specifications (control vs. optimised)

### Section 5: Quick-Win Checklist

A scannable 8–12 item checklist of micro-optimisations the user can implement in under 30 minutes (e.g., "Add directional cue arrow pointing toward CTA," "Crop hero image so model's eye gaze faces the headline," "Reduce navigation links from 7 to 3 above the fold").

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
FutureProof:save_experiment(skill="attention-heatmap", experiment={
  hypothesis: "Repositioning the primary CTA from below-fold zone 6 to above-fold zone 3 with a 40% size increase reduces fixation hops from 5 to 2 and increases click-through rate",
  variants: ["control: current CTA placement and size in zone 6", "variant: CTA moved to zone 3 with increased size and directional cue"],
  measurement: "CTA click-through rate, scroll depth to CTA, and Hotjar/Clarity heatmap fixation density on CTA zone — measured over 2,000 sessions",
  expected_impact: "20–35% increase in CTA click-through rate based on Fitts' Law distance reduction"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="attention-heatmap",
  query="Latest eye-tracking studies on landing page conversion optimisation 2024, mobile-first visual hierarchy benchmarks, and emerging attention patterns for AI-era browsing behaviour",
  reason="Calibrate gaze path prediction models against current empirical data and account for evolving scanning behaviours driven by short-form content consumption habits"
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
FutureProof:save_session(skill="attention-heatmap", session={
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