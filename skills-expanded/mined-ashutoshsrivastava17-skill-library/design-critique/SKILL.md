---
name: design-critique
description: >
  Get structured feedback on a design — UI, layout, visual hierarchy, interaction patterns, and usability.
  TRIGGER when: user says "critique this design", "review my design", "feedback on this UI",
  "what do you think of this layout", or shares a screenshot/mockup for review.
argument-hint: "[file path or description of design]"
user-invocable: true
---

# Design Critique

Provide structured, actionable design feedback using established design principles. Balances praise with constructive criticism — always explain *why* something works or doesn't.

## Critique Framework

Evaluate designs across these dimensions, in priority order:

### 1. Usability & Clarity

- **Can the user accomplish their goal?** Is the primary action obvious?
- **Information hierarchy**: Is the most important content the most prominent?
- **Cognitive load**: How many decisions does the user need to make? Can any be removed?
- **Learnability**: Would a first-time user understand this without instructions?
- **Error prevention**: Does the design prevent mistakes before they happen?
- **Feedback**: Does the UI communicate state changes (loading, success, error)?

### 2. Visual Hierarchy & Layout

- **F-pattern / Z-pattern**: Does the layout follow natural scanning patterns?
- **Spacing & proximity**: Are related elements grouped? Is there enough whitespace?
- **Alignment**: Are elements aligned to a consistent grid?
- **Contrast & emphasis**: Do size, weight, and color guide the eye correctly?
- **Consistency**: Are similar elements styled the same way?

### 3. Typography

- **Readability**: Is body text 16px+ on web? Line height 1.4-1.6x? Line length 50-75 characters?
- **Hierarchy**: Are there clear distinctions between heading levels?
- **Font pairing**: Do the typefaces complement each other (max 2-3 fonts)?
- **Weight distribution**: Is bold used sparingly and purposefully?

### 4. Color & Contrast

- **Palette coherence**: Is the color palette limited and intentional?
- **Semantic color**: Do colors convey meaning consistently (red=error, green=success)?
- **Contrast ratios**: Does text meet WCAG AA (4.5:1 for normal, 3:1 for large)?
- **Dark mode consideration**: Does the palette translate to dark mode?

### 5. Interaction Design

- **Affordance**: Do interactive elements look clickable/tappable?
- **Feedback loops**: Hover states, active states, focus states — are they all defined?
- **Transitions**: Are state changes smooth and meaningful (not decorative)?
- **Touch targets**: Are targets at least 44x44px with adequate spacing?
- **Progressive disclosure**: Is complexity revealed gradually?

### 6. Responsiveness & Adaptability

- **Breakpoint behavior**: How does the layout adapt at mobile/tablet/desktop?
- **Content reflow**: Does content stack sensibly on narrow viewports?
- **Image scaling**: Do images resize without distortion or overflow?
- **Navigation patterns**: Does navigation adapt appropriately (hamburger, tab bar)?

## Critique Process

### Phase 1 — Understand Context

Before critiquing, establish:

1. **What is this?** (landing page, dashboard, form, modal, flow?)
2. **Who is the user?** (new user, power user, admin?)
3. **What is the goal?** (convert, inform, complete a task?)
4. If `$ARGUMENTS` provides a file, read/view it. Ask for context if insufficient.

### Phase 2 — Evaluate

Walk through each dimension above. Not every dimension applies to every design — focus on what's relevant.

### Phase 3 — Report

Structure feedback using this format:

```
## Design Critique — {design name or description}

### Context
- **Type**: {landing page / dashboard / form / modal / flow}
- **Target user**: {who}
- **Primary goal**: {what the user should accomplish}

### What Works Well
- {Specific praise with reasoning — "The CTA placement is strong because..."}
- {At least 2-3 positives}

### Needs Improvement

#### High Impact
- **{Issue}**: {what's wrong and why it matters}
  - **Suggestion**: {specific, actionable fix}

#### Medium Impact
- **{Issue}**: {description}
  - **Suggestion**: {fix}

#### Low Impact / Polish
- **{Issue}**: {description}
  - **Suggestion**: {fix}

### Design Principles Applied
- {Which principles inform the critique — Fitts's Law, Hick's Law, Gestalt, etc.}

### Overall Assessment
{1-2 sentences: overall quality and single most impactful change to make}
```

## Tone Guidelines

- **Be specific**: "The 12px gray text on white background is hard to read" not "the text is hard to read"
- **Explain why**: Ground every critique in a principle, heuristic, or user impact
- **Be constructive**: Always pair problems with solutions
- **Prioritize**: Don't list 30 issues — focus on the 5-8 that matter most
- **Respect intent**: Understand what the designer was trying to achieve before suggesting changes
- **No subjective preferences**: "I don't like blue" is not valid feedback. "Blue connotes trust — consider whether that aligns with your brand" is.

## Reference: Design Heuristics

Use these when grounding feedback:

| Heuristic | Summary |
|---|---|
| Nielsen's #1 | Visibility of system status |
| Nielsen's #2 | Match between system and real world |
| Nielsen's #4 | Consistency and standards |
| Nielsen's #6 | Recognition rather than recall |
| Nielsen's #8 | Aesthetic and minimalist design |
| Fitts's Law | Important targets should be large and close to the user's cursor |
| Hick's Law | More choices = slower decisions. Reduce options. |
| Gestalt Proximity | Elements close together are perceived as related |
| Gestalt Similarity | Elements that look alike are perceived as related |
| Miller's Law | Working memory holds ~7 items. Chunk information. |

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners

## Edge Cases

- If input data is incomplete, state assumptions explicitly and flag gaps
- For time-sensitive situations, prioritize speed over comprehensiveness
- If multiple stakeholders have conflicting needs, document the tradeoffs
- For first-time use, start with a simplified version and iterate
- Adapt the depth and detail to the audience's expertise level
