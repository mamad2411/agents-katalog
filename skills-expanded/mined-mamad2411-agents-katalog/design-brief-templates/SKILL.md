---
name: design-brief-templates
description: Design brief structure, interaction specification patterns, and design-engineering handoff formats. Use when translating feature specs into briefs for design teams or documenting design requirements for handoff.
---

# Design Brief Templates

A design brief translates a technical feature spec into the context a design team needs: who the user is, what they're trying to accomplish, what constraints apply, and what the design must enable. Good briefs produce focused design work. Vague briefs produce designs that are aesthetically polished but functionally wrong.

## When to Use This Skill

- Writing a design brief from a feature spec and journey map
- Documenting design requirements for a new screen or flow
- Communicating technical constraints (API limits, performance, data availability) in designer-friendly language
- Reviewing a design brief for completeness before sending to design
- Creating a component inventory for design system decisions

## What a Design Brief Is (and Isn't)

**Is:** Context, goals, constraints, and requirements the designer needs to make good decisions

**Is not:** A wireframe. A solution. An instruction to "make it look like this." The brief defines the *problem space* — the designer defines the *solution*.

## Standard Design Brief Template

```markdown
# Design Brief: [Feature Name]

**Feature Spec reference:** [Link or section]
**Design owner:** [Name]
**Brief status:** Draft / In Review / Approved
**Date:** [Date]

---

## User Context

**Who is this for?**
[1-2 sentences describing the user. Use the ICP / segment, not a vague persona.]

**What are they trying to accomplish?**
[The job-to-be-done — what success looks like for the user at the end of this flow]

**What's their context when they reach this screen/flow?**
[Are they in a hurry? On mobile? Coming from a notification? First time or returning?]

**What's their emotional state?**
[Are they anxious (financial transaction)? Excited (new feature)? Frustrated (error recovery)?]

---

## What the Design Must Enable

### Must-Have Interactions
- [The user must be able to do X]
- [The user must see Y when Z happens]
- [The user must be able to recover from [error] without losing progress]

### Must-Have States
All designs must address these states:
- [ ] Default / First-time state
- [ ] Loading state
- [ ] Empty state (with guidance for what to do)
- [ ] Populated state
- [ ] Error state (with recovery path)
- [ ] Success state (with clear confirmation)

### Must-Have Content
- [Specific data that must be visible — e.g., "order total must always be visible during checkout"]
- [Specific actions that must be accessible — e.g., "cancel order must be one tap away"]

---

## Technical and Data Constraints

**Data that is available:**
- [Field name]: [Data type, max length, always present / sometimes present]
- [Field name]: [Data type, notes]

**Data that is NOT available:**
- [Field name]: [Why it's not available and implications for design]

**Performance constraints:**
- [e.g., "Product images load asynchronously — design must handle delayed image appearance"]
- [e.g., "API response is < 200ms — no skeleton screen needed for this data"]

**API limitations:**
- [e.g., "Cannot search within results — filtering must happen client-side on loaded data"]
- [e.g., "Pagination is cursor-based — no jump-to-page functionality possible"]

---

## Platform Requirements

**Primary platform:** [iOS / Android / Web / All]

**Device breakpoints to design for:**
- Mobile: [320px – 430px]
- Tablet: [768px – 1024px] — [Required / Optional]
- Desktop: [1280px+] — [Required / Optional]

**Orientation:** Portrait only / Both / Landscape-friendly

---

## Accessibility Requirements

- Minimum contrast ratio: 4.5:1 for normal text, 3:1 for large text (WCAG 2.1 AA)
- Touch targets: minimum 44×44pt
- Focus states: all interactive elements must have visible focus indicator
- Screen reader: all images need alt text; form fields need associated labels
- [Any feature-specific accessibility requirements from the feature spec]

---

## Design System Guidance

**Existing components that apply:**
- [Component name] — use for [element]
- [Component name] — use for [element]

**Potential new patterns needed:**
- [Description of element that doesn't fit existing components]
- [Reason existing components don't apply]

**What NOT to use:**
- [Component or pattern that seems applicable but shouldn't be used here, and why]

---

## Out of Scope for Design

The following are explicitly not part of this design brief:
- [Item 1]
- [Item 2]

---

## Success Criteria for Design Review

Design is ready for engineering handoff when:
- [ ] All required states are designed
- [ ] Designs exist for all required breakpoints
- [ ] Accessibility requirements are met
- [ ] Component inventory is documented (existing vs. new)
- [ ] Interaction specs are written for non-obvious behaviors
- [ ] Edge cases are handled visually, not deferred
```

## Interaction Specification Patterns

For interactions that aren't self-evident from the visual design, write an interaction spec:

```markdown
## Interaction: [Name]

**Trigger:** [What the user does — tap, swipe, type, etc.]

**Animation:** [Type, duration, easing — or "none" if static]
  Example: "Fade in, 200ms, ease-out"

**Behavior:** [What happens as a result]

**Edge cases:**
  - If [condition]: [modified behavior]
  - If [condition]: [modified behavior]

**Platform notes:**
  - iOS: [any platform-specific behavior]
  - Android: [any platform-specific behavior]
```

### Common Interactions to Spec

- Form submission (success, error, loading states)
- Pull-to-refresh (trigger threshold, animation, failure state)
- Infinite scroll (loading threshold, end-of-list state, error state)
- Toast / snackbar messages (duration, dismissibility, positioning)
- Modal / sheet (entry animation, dismiss behavior, back navigation)
- Swipe-to-action (threshold, snap-back vs. commit behavior)

## Component Inventory Format

Document design system decisions per feature:

```markdown
## Component Inventory: [Feature Name]

| Element | Component Decision | Notes |
|---------|-------------------|-------|
| Primary CTA | Existing: PrimaryButton | Standard usage |
| Item list | Existing: ListCard | Use compact variant |
| Error banner | Existing: AlertBanner | Critical variant |
| [Element] | NEW: QuantitySelector | Needs design; qty +/- not in DS |
| [Element] | MODIFIED: SearchBar | Needs location filter added |
```

## Constraint Communication Guide

Technical constraints often need translation for designers:

| Technical Constraint | Designer-Friendly Framing |
|---------------------|--------------------------|
| "API is paginated at 20 items" | "The user sees 20 results at a time. Design must include a clear way to load more, and handle the end of results." |
| "Images are user-uploaded, variable dimensions" | "Images may be portrait, landscape, or square. Design must handle any aspect ratio gracefully (don't assume square thumbnails)." |
| "Real-time data is delayed by 30s" | "Data refreshes every 30 seconds, not in real-time. Design should not imply live updates." |
| "Search results return in < 500ms" | "Search response is fast — no loading state needed. But design for the empty results case." |
| "Username is max 32 characters" | "Max username length is 32 characters. Design must accommodate the longest realistic names without breaking layouts." |

## Best Practices

1. **Briefs are for the designer, not for the record** — write in plain language; avoid jargon
2. **User context is the most important section** — designers make better decisions when they understand who they're designing for
3. **Constraints are gifts** — don't apologize for constraints; they focus the design
4. **Out-of-scope is mandatory** — designers will design to the edges of ambiguity; the brief must define the edges
5. **Review with engineering before sending** — engineering often spots technical constraints that Product missed
