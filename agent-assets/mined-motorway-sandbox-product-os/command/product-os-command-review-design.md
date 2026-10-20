<!-- owner: shared | audience: all-pms | last-updated: 2026-02 -->
<!-- purpose: Structured design review using psych audit, persona evaluation, activation fit, and assumption mapping -->

# Design Review

Review design screenshots against your product frameworks and save a structured, evidence-based review.

**Arguments:** $ARGUMENTS (optional — the hypothesis being tested)

## Instructions

### Phase 1: Gather Context

1. **Check for images.** If no design screenshots are visible in the conversation, ask the user to paste them before continuing. Do not proceed without images.

2. **Parse the hypothesis.** If `$ARGUMENTS` contains text, use it as the hypothesis. If it is empty or missing, ask: "What hypothesis is this design testing? (If/then/because format is ideal, but a plain description works too.)"

3. **Determine context.** Ask the user (if not obvious from the designs):
   - Is this **customer-facing or internal/B2B-facing**?
   - What **journey stage** does this sit in? (e.g. onboarding, checkout, post-purchase, admin dashboard)
   - Is there an **existing project file** this relates to? (e.g. a file in `projects/`)

4. **Read reference files silently** (do not output their contents). Always read:
   - `context/product.md`
   - `data/funnel-context.md`
   - `context/brand/messaging/how-we-sound.md`
   - `context/brand/messaging/our-language.md`
   - `pm-playbook/process/4-design.md`

   If relevant, also read:
   - `strategy/activation/activation-strategy.md` (**Note:** this is a DRAFT document — use its frameworks as reference but do not treat its specific recommendations as validated or current strategy)
   - `context/personas/customer-personas.md`

   For B2B/partner-facing features, also read:
   - `strategy/activation/partner-activation-strategy.md` (**Note:** this is a DRAFT document — same caveat as above)
   - `context/personas/partner-personas.md`

   If a **project file** was identified, also read it.

### Phase 2: Analyse (6 Lenses)

Work through all six lenses below. Do not skip any.

#### Lens 1: Hypothesis Alignment

For each screen/state in the design:
- Does this screen directly serve the stated hypothesis?
- Are there elements that are unrelated to or contradicting the hypothesis?
- Is the hypothesis testable from what's shown?

Flag any disconnects between the design and the hypothesis.

#### Lens 2: Psych Audit

Using the Psych Framework from the activation strategy, score each significant element on a scale of **-3** (strong negative psych) to **+3** (strong positive psych). Consider:
- What does the user see at each point?
- How does it make them feel?
- Does it motivate or drain?

Then identify:
- **Psych valleys** — where is motivation at its lowest?
- **Missing positive psych** — where could the design add value, motivation, or reward that it currently doesn't?
- **Negative hotspots** — elements that introduce friction, confusion, effort, or anxiety

Score from the user's perspective, not the PM's.

#### Lens 3: Persona Evaluation

Evaluate the design from the perspective of the **2 priority personas** for the relevant side of the marketplace:

- **Customer-facing:** your two priority customer personas (from context/personas/customer-personas.md)
- **Partner/B2B-facing:** your two priority partner personas (from context/personas/partner-personas.md)

For each persona, consider:
- Does the design address their primary concerns?
- Where might they get stuck or drop off?
- What would make them feel confident proceeding?

#### Lens 4: Activation Fit Check

Rate the following as **Strong**, **Adequate**, or **Weak** with a one-line rationale:

| Fit | Question |
|-----|----------|
| **Audience** | Does the design speak to the right users with the right context? |
| **Promise** | Is the value proposition clear and compelling? |
| **Intent** | Does it meet the user where they are in their journey (high intent vs low intent)? |
| **Knowledge** | Does it assume the right level of user knowledge? |

#### Lens 5: Design Best Practice

Evaluate the design against the frameworks below. Only flag issues where there is a genuine concern — do not pad with generic advice. When flagging an issue, cite the specific principle by name so the designer can look it up.

**5a. Usability heuristics** (Nielsen's 10 heuristics — flag any violations)

| Heuristic | What to check |
|-----------|---------------|
| **Visibility of system status** | Does the user know where they are, what's happening, and what just happened? Look for progress indicators, loading states, confirmation feedback, and clear system responses. The Goal-Gradient Effect (lawsofux.com) shows users are more motivated as they see progress — especially relevant to multi-step flows like onboarding. |
| **Match between system and real world** | Does the design use language and concepts familiar to the user, not internal jargon? Does it follow real-world conventions? Check against your brand voice (`how-we-sound.md`, `our-language.md`). |
| **User control and freedom** | Can users undo, go back, or exit without penalty? Are there clear escape routes? Users make mistakes — the design should support recovery without starting over. |
| **Consistency and standards** | Does the design follow platform conventions (Jakob's Law: users expect your site to work like others they already know) and your own patterns? Inconsistency forces users to relearn, increasing cognitive load. |
| **Error prevention** | Does the design prevent errors before they happen through constraints, smart defaults, or confirmations? This is better than good error messages after the fact. For forms: inline validation, sensible defaults, and clear input formatting. |
| **Recognition over recall** | Are options, actions, and information visible or easily retrievable? Users shouldn't need to remember information from a previous screen. Labels, contextual help, and visible navigation reduce memory burden. |
| **Flexibility and efficiency** | Does it serve both first-time and repeat users? Are there shortcuts for experienced users without cluttering the novice experience? |
| **Aesthetic and minimalist design** | Does every element serve a purpose? Extra content competes with relevant information and reduces signal. This is not about "looking nice" — it's about signal-to-noise ratio. |
| **Help users recover from errors** | Are error messages in plain language, do they explain what went wrong, and do they suggest a fix? No error codes, no dead ends. |
| **Help and documentation** | If the flow requires explanation, is it available in context (tooltips, inline help) rather than requiring the user to leave the flow? |

**5b. Cognitive load and decision-making** (Laws of UX)

- **Hick's Law** — Does the design present too many choices at once? The time to decide increases with the number and complexity of options. Simplify choices, use progressive disclosure, and set smart defaults.
- **Miller's Law** — Is information chunked into digestible groups? Working memory holds roughly 7 items (plus or minus 2). Long lists, too many form fields, or dense content should be broken into sections.
- **Fitts's Law** — Are interactive elements (buttons, links, inputs) large enough and close enough to reach easily? Primary CTAs should be the largest, most prominent tap target on the screen. This is critical on mobile.
- **Peak-End Rule** — Users judge an experience by its most intense moment and its ending. Is the peak moment designed well? Does the flow end on a high note (confirmation, reward, clear next step)?
- **Von Restorff Effect** — The element that's visually different from its surroundings is the one users remember. Is the most important element (CTA, key message) visually distinct?
- **Zeigarnik Effect** — People feel compelled to complete tasks they've started. Progress indicators and partial-completion cues can leverage this to reduce drop-off in multi-step flows.

**5c. Mobile experience** (critical — most users are on mobile)

- **Touch targets** — Minimum 44x44px (WCAG 2.2) for all interactive elements. Primary CTAs should be larger, ideally 48px+. Baymard Institute research shows undersized targets are a leading cause of mobile usability failures.
- **Thumb-zone layout** — Primary actions should sit in the natural thumb-reach zone (bottom half / centre of screen). Avoid placing critical actions in hard-to-reach corners.
- **Form optimisation** — Baymard research shows the average ecommerce form can reduce fields by 20-60% without losing necessary information. Only ask for what's needed at this step. Use the right input types (numeric keyboard for numbers, email keyboard for email).
- **Single-column layout** — Multi-column forms and side-by-side elements cause mis-taps and confusion on small screens.
- **Performance perception** — Mobile users abandon if the page feels slow. Are there loading indicators? Is content prioritised so the most important information appears first?
- **Scroll depth** — Is critical information or the primary CTA visible without scrolling? On mobile, anything below the fold has significantly lower engagement.

**5d. Visual hierarchy and layout**

- **Information hierarchy** — Is the most important content the most visually prominent (size, weight, position, contrast)? Scan the design: where does the eye land first, second, third?
- **CTA clarity** — Is there one clear primary action per screen? Is it visually distinct from secondary actions? Competing CTAs split attention and reduce conversion.
- **Whitespace and grouping** — Law of Proximity: elements near each other are perceived as related. Is related content grouped and separated from unrelated content with adequate spacing?
- **Copy quality** — Is the language clear, concise, and aligned with your brand voice? Does it tell the user what to do and why? Avoid ambiguous labels ("Submit", "Continue") — be specific ("Get started", "See your results").

**5e. Accessibility fundamentals**

- **Colour contrast** — Text must meet WCAG AA contrast ratio (4.5:1 for normal text, 3:1 for large text). Don't rely on colour alone to convey meaning (e.g. red for errors should also have an icon or text label).
- **Text size** — Minimum 16px body text on mobile to prevent browser auto-zoom on input focus and ensure readability.
- **Interactive element labels** — All inputs, buttons, and links should have clear labels (visible or aria-labelled). Placeholder text alone is not a label.
- **Focus and keyboard** — Can the flow be completed without a mouse? Is focus order logical?

**5f. Error and edge states**

- Are error states designed, not just the happy path? Consider: empty states, validation errors, network failures, timeouts, and partial data.
- Do error messages explain the problem and suggest a fix in plain language?
- Is error prevention prioritised over error recovery? (Inline validation as the user types, not after submission.)

#### Lens 6: Assumption Mapping

Identify **3-5 key assumptions** baked into this design. For each:

| Assumption | Type | Risk | De-risk suggestion |
|------------|------|------|--------------------|
| [State it clearly] | Usability / Viability / Feasibility | High / Medium / Low | [Specific, actionable suggestion] |

Types:
- **Usability** — will users understand and use this correctly?
- **Viability** — will this deliver the intended business or user value?
- **Feasibility** — can this be built as designed?

### Phase 3: Output and Save

Compile the analysis into a single structured review document in this format:

```markdown
# Design Review: [Brief title]

**Date:** [YYYY-MM-DD]
**Hypothesis:** [The hypothesis being tested]
**Designs reviewed:** [Brief description of what was reviewed — number of screens, flow, etc.]
**Side:** [Customer / Partner]
**Journey stage:** [e.g. Onboarding, Checkout, Dashboard]

---

## What's Working Well

[3-5 specific, evidence-based items. Reference the framework or data point that supports each.]

## What Could Be Improved

[3-5 specific, actionable items. Use collaborative language — "I wonder if...", "The research suggests...", "{priority persona 1} might feel...". Ground each in a framework, persona, or data point.]

## Psych Audit Summary

| Element | Score (-3 to +3) | Rationale |
|---------|:-----------------:|-----------|
| [Element 1] | [Score] | [Brief rationale] |
| ... | ... | ... |

**Psych valley:** [Where and why]
**Missing positive psych:** [Opportunities]
**Negative hotspots:** [Key concerns]

## Persona Check

**[Persona 1 name]:** [How they'd experience this design — concerns, confidence level, likely behaviour]

**[Persona 2 name]:** [How they'd experience this design — concerns, confidence level, likely behaviour]

## Activation Fit Assessment

| Fit | Rating | Rationale |
|-----|--------|-----------|
| Audience | [Strong/Adequate/Weak] | [One-line rationale] |
| Promise | [Strong/Adequate/Weak] | [One-line rationale] |
| Intent | [Strong/Adequate/Weak] | [One-line rationale] |
| Knowledge | [Strong/Adequate/Weak] | [One-line rationale] |

## Design Best Practice

**Usability heuristic flags:**
[Only list heuristics where there's a genuine issue. Format: "**Heuristic name** — description of the concern and suggested improvement."]

**Cognitive load & decision-making:**
[Any issues related to Hick's Law, Miller's Law, Fitts's Law, Peak-End Rule, etc. Only flag real concerns.]

**Mobile experience:**
[Touch targets, thumb-zone, form optimisation, scroll depth, performance. Only flag real concerns.]

**Visual hierarchy & layout:**
[Information hierarchy, CTA clarity, whitespace/grouping, copy quality. Only flag real concerns.]

**Accessibility:**
[Contrast, text size, labels, focus order. Only flag real concerns.]

**Error & edge states:**
[Missing error states, validation approach, empty states. Only flag real concerns.]

## Key Assumptions

| Assumption | Type | Risk | De-risk suggestion |
|------------|------|------|--------------------|
| [Assumption 1] | [Type] | [Risk] | [Suggestion] |
| ... | ... | ... | ... |

## Alternative Ideas / Opportunities

[2-3 ideas, each labelled as either **Refinement** (improve current direction) or **Alternative** (different approach). Brief description with rationale.]

## Overall Assessment

[One of: **Ready for engineering** / **Needs minor iteration** / **Needs significant iteration**]

[1-2 sentence summary of the key finding and recommended next step.]
```

**Save the review:**
- If a project was identified: `projects/{project-slug}/design-reviews/review-YYYY-MM-DD.md`
- If no project context: `projects/design-reviews/review-YYYY-MM-DD.md`

Create directories as needed.

After saving, tell the user where the file was saved and offer:
- "Want me to iterate on any section?"
- "Want me to reformat this for a different audience (e.g. Slack summary for the designer, or a brief for stakeholders)?"

## Key Principles

- **Evidence over opinion** — every suggestion must reference a framework, persona, or data point. No "I think it would look better if..."
- **Collaborative tone** — "I wonder if...", "The research suggests...", "From {priority persona 1}'s perspective..." not "Change this"
- **Persona-first** — score from the user's perspective, not the PM's or designer's
- **Consider both sides** — customer-facing designs should note potential internal/operational impact and vice versa
- **Mobile-first lens** — most users are on mobile; flag anything that doesn't work on small screens
- **UK English** throughout, no emojis, no fabricated data or statistics
- **Don't pad** — if something is genuinely fine, don't invent criticism. Equally, don't hold back on real concerns
