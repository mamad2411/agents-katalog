---
name: predicting-accessibility-risks
description: Use this skill to identify accessibility risks in a proposed feature, design, or technical plan before implementation begins. Triggers when planning a new feature, reviewing a design, assessing a technical approach for accessibility impact, or asking what could go wrong for disabled users.
---

# Predicting Accessibility Risks

Identify accessibility risks in a proposed change before implementation begins. The goal is to surface problems that would be expensive to fix later — structural choices, interaction patterns, and data model decisions that affect whether disabled users can use the feature.

This is a planning skill. It does not review implemented code (use `reviewing-accessibility` for that) and it does not write code. It produces a risk assessment that a developer or coder agent can act on.

## Gather context

Before assessing risks, understand what is being proposed:

1. **Read the plan** — feature description, user story, design document, technical spec, or conversation describing the intended change.
2. **Read affected code** — if the change modifies existing UI, read the current implementation to understand what is already in place. Risks are relative to the starting point.
3. **Identify the user interactions** — what will people do with this feature? List the verbs: navigate, filter, select, submit, drag, expand, dismiss, etc. Each interaction is a potential risk surface.
4. **Identify the content** — what information does the feature present? Text, images, status indicators, data visualisations, real-time updates. Each content type has accessibility constraints.

## Assess risks

For each risk identified, produce:

| Field | Description |
|-------|-------------|
| **Risk** | One-sentence description of what could go wrong |
| **Affected users** | Which disability groups are affected and how (screen reader users, keyboard-only users, low vision, cognitive, motor) |
| **WCAG criteria** | The success criteria at stake (e.g., 2.1.1 Keyboard, 1.3.1 Info and Relationships) |
| **Likelihood** | How likely is this to occur without explicit attention? High (almost certain without mitigation), Medium (depends on implementation choices), Low (only if a specific mistake is made) |
| **Cost to fix later** | How expensive is this to retrofit if caught after implementation? High (requires architectural changes), Medium (requires rework of multiple components), Low (localised fix) |
| **Mitigation** | Specific, actionable recommendation to avoid the risk. Identify the pattern or approach ("use the APG dialog pattern", "ensure focus returns to the trigger on close"), not specific markup or API calls — implementation details belong in the coding phase where they can respond to the actual architecture |

Focus on risks that meet at least one of these criteria:
- High cost to fix later (structural or architectural)
- High likelihood (the default implementation path would miss it)
- Affects a fundamental interaction (navigation, form submission, content access)

Do not list every conceivable WCAG criterion. A risk assessment that lists 30 items is not actionable. Aim for the 5-10 risks that matter most for this specific change.

## Involve disabled people

Technical risk prediction covers part of the picture. Automated tools and AI-based analysis can assess at most 30% of WCAG success criteria, and none of them fully. The risks identified by this skill are indicators that narrow the scope for human evaluation — they are not definitive accessibility assessments.

### Why

"Nothing about us without us" applies directly to software development. Interfaces can pass every automated check yet fail the people who use them. The gap between technical conformance and actual usability can only be closed by involving disabled people.

### When

Involve disabled people at each phase — the earlier it happens, the cheaper it is to act on findings:

- **Discovery and planning** (where this skill operates) — contextual inquiry and interviews with disabled users to understand existing barriers and priorities.
- **Prototyping** — co-design sessions and proxy testing with assistive technology users before committing to an implementation approach.
- **Implementation** — AT-specific usability testing against builds, not just automated checks against code.
- **Post-launch** — ongoing monitoring and feedback channels that disabled users can actually reach.

### How

Scale the approach to the project. Not every project has a research budget, but every project can get closer to real feedback than technical analysis alone provides.

**Solo and small projects** — test with a screen reader yourself (VoiceOver, NVDA, or TalkBack are free), ask a disabled friend or colleague to try key flows, post in accessibility communities for informal feedback, or use free single-session options from panel services. Even one person using assistive technology will reveal things automated checks cannot.

**Teams with some research capacity** — include disabled participants in existing user research. The NHS benchmark of 1 person with access needs in every 5 research participants is a reasonable starting point. Recruit from disability organisations, charities, or internal staff disability networks.

**Dedicated accessibility research** — panel services like [Fable](https://makeitfable.com/), [Access Works](https://knowbility.org/programs/accessworks) (Knowbility), and [AbilityNet](https://abilitynet.org.uk/) provide pre-qualified participants with documented assistive technology configurations. This is the most reliable option for structured usability testing across multiple AT setups.

Regardless of scale, recruit based on assistive technology configuration, not diagnosis. What matters is how someone interacts with software (screen reader, switch access, voice control, magnification) rather than their medical history.

### What this skill cannot assess

The following require human judgment and cannot be evaluated by technical analysis alone:

- Whether alt text is meaningful in context (not just present)
- Whether screen reader announcements make functional sense in sequence
- Whether keyboard navigation flow supports real task completion
- Whether cognitive load is manageable for the target audience
- How users recover from errors in practice
- Whether multi-step workflows are actually usable versus merely conformant

## Risk patterns by feature type

These are common risk areas, not exhaustive checklists. Use them as prompts to identify risks specific to the proposed change.

### New pages and routes

- Missing landmark structure makes the page unnavigable for screen reader users
- No focus management on route change leaves focus at the top of the DOM, forcing keyboard users to tab through the entire page
- Missing or generic page title (`<title>`) makes it impossible to distinguish tabs
- Heading hierarchy that skips levels or uses multiple `h1` elements breaks document structure

### Interactive widgets (custom controls, menus, trees, grids)

- No established ARIA pattern selected — custom widgets without an APG pattern tend to accumulate ad-hoc ARIA that confuses assistive technology
- Keyboard model not defined upfront — retrofitting keyboard navigation onto a mouse-first widget often produces inconsistent or incomplete key bindings
- Missing focus management for state changes — opening, closing, creating, and deleting items all require deliberate focus decisions
- Live region strategy absent — dynamic updates (filtering results, loading states, toast notifications) that are not announced leave screen reader users unaware of changes

### Forms

- Placeholder-only labels disappear on input, leaving users with no label reference
- Error handling designed visually but not programmatically — errors that are shown in red text but not associated with fields via `aria-describedby` are invisible to screen readers
- Missing autocomplete attributes force users to manually type data that browsers and password managers could fill
- Multi-step forms without clear progress indication and the ability to go back

### Modals and overlays

- No focus trapping allows keyboard users to interact with background content while a modal is open
- No focus return on close leaves focus in a destroyed DOM node or at the document root
- No escape key dismissal traps keyboard users in the overlay
- Background content not marked inert allows assistive technology to interact with hidden content

### Drag and drop

- No keyboard alternative — drag and drop is inherently inaccessible to keyboard-only and many assistive technology users without an alternative interaction
- No screen reader indication of draggable items, drop targets, or current position
- Move operations that rely solely on pointer position with no confirmation step

### Data visualisation (charts, graphs, maps)

- No text alternative or data table for the information conveyed visually
- Colour-only encoding (red/green for good/bad) excludes colour-blind users
- Interactive chart elements not keyboard accessible
- Tooltip-only data not available to screen readers

### Real-time and time-dependent content

- Auto-updating content (live feeds, countdowns, stock tickers) that cannot be paused
- Time limits on actions (session timeouts, form expiry) without extension mechanisms
- Content that changes while a screen reader is reading it, producing incoherent output

### Colour and theming

- New colour pairings not verified for contrast in all supported themes
- Status information conveyed by colour alone (green badge = active, red = error)
- Custom animations without `prefers-reduced-motion` consideration

### Content and media

- Images without alt text strategy (which images are informative, which are decorative?)
- Video or audio without captions/transcripts planned
- Complex content (tables, diagrams) without a simplification or alternative strategy
- PDFs or documents generated without accessibility structure

## Report format

```markdown
## Accessibility Risk Assessment - [feature/change name]

### High Risk

| Risk | Affected users | WCAG | Likelihood | Fix cost | Mitigation |
|------|---------------|------|------------|----------|------------|
| ... | ... | ... | ... | ... | ... |

### Medium Risk

| Risk | Affected users | WCAG | Likelihood | Fix cost | Mitigation |
|------|---------------|------|------------|----------|------------|
| ... | ... | ... | ... | ... | ... |

### Low Risk

| Risk | Affected users | WCAG | Likelihood | Fix cost | Mitigation |
|------|---------------|------|------------|----------|------------|
| ... | ... | ... | ... | ... | ... |

### User research recommendations

- Which risks would benefit most from validation with disabled users
- What disability groups and AT configurations to prioritise in testing based on the risks identified
- At what development phase testing would be most valuable for each risk

### Recommendations

[Ordered list of the most important mitigations to implement, distilled from the table above. These should be concrete enough that a developer can act on them without further research.]
```

Omit empty risk levels. If there are no high risks, do not include an empty High Risk section.

## Gotchas

- **Risk prediction is not a compliance audit.** The goal is to identify problems before they are built, not to produce a WCAG scorecard. A risk assessment that just lists WCAG criteria without connecting them to specific design decisions is not useful.
- **Not every feature needs a full risk assessment.** A text content change, a colour tweak with verified contrast, or a change to backend logic with no UI impact may have zero accessibility risks. Say so rather than inventing risks.
- **Component libraries reduce but do not eliminate risk.** Headless UI libraries (Base UI, Headless UI, Ark UI) handle many ARIA patterns correctly, but the risk shifts to composition — how components are assembled, what labels are provided, and how focus is managed between them.
- **The most dangerous risks are structural, not superficial.** A missing alt text is easy to add later. A widget built without a keyboard interaction model requires a redesign. Prioritise structural risks over cosmetic ones.
- **"We'll add accessibility later" is itself the highest risk.** If the plan defers accessibility to a future sprint, flag this explicitly. Retrofitting accessibility onto a finished feature is consistently and often significantly more expensive than building it in from the start.
- **Consider the full range of disabilities.** Accessibility reviews disproportionately focus on screen reader users. Keyboard-only users, users with low vision (who may not use screen readers), users with cognitive disabilities, and users with motor impairments all have distinct needs. Name the affected group explicitly.
- **Custom components carry more risk than standard HTML.** A `<button>` has built-in keyboard handling, focus management, and role. A `<div onClick>` has none of these. The more custom the implementation, the higher the risk.
- **Mitigations should identify patterns, not prescribe code.** "Use the APG combobox pattern" is appropriate for a planning skill. "Add `role="combobox" aria-expanded="false" aria-haspopup="listbox"` to the input wrapper" is implementation detail that belongs in a code review, not a risk assessment. Premature specificity narrows the solution space and carries unearned authority if a developer treats it as reviewed implementation guidance.
- **This risk assessment is not a substitute for involving disabled people.** It identifies technical patterns likely to cause barriers, but it cannot evaluate whether an interface is actually usable by people with disabilities. Plan user research with disabled participants — the risks flagged here can help scope that research.

## Authoritative references

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [Understanding WCAG 2.2](https://www.w3.org/WAI/WCAG22/Understanding/)
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [W3C WAI — Involving Users in Web Projects](https://www.w3.org/WAI/planning/involving-users/)
- [W3C WAI — Involving Users in Evaluating Web Accessibility](https://www.w3.org/WAI/test-evaluate/involving-users/)
- [GOV.UK — Running research sessions with disabled people](https://www.gov.uk/service-manual/user-research/running-research-sessions-with-people-with-disabilities)
- [NHS Service Manual — Accessibility user research](https://service-manual.nhs.uk/accessibility/user-research)
- [Fable — Accessibility research FAQs](https://makeitfable.com/article/accessibility-research-faqs/)
