---
name: ux-product-design
description: Apply UX design principles, mental models, affordances, and design sprint methodology when designing interfaces, user flows, or product experiences. Use when designing UI, reviewing usability, running design workshops, or when the user asks about UX, usability, HCI, or product design.
---

# UX & Product Design

Drawn from: *The Design of Everyday Things* (Don Norman), *The Laws of Simplicity* (John Maeda), *Design Sprint* (Richard Banfield), *Designing the User Interface* (Shneiderman, Plaisant, Cohen), *Design Is a Job* (Mike Monteiro), *Designing User Interfaces* (Malewicz).

## Norman's Core Principles (Design of Everyday Things)

### Affordances
An affordance is a relationship between an object and a user that signals how it should be used.

- A button **affords** pressing
- A text field **affords** typing
- A handle **affords** pulling

**Apply:** Make interactive elements look interactive. Don't hide clickable things behind non-obvious styling.

### Signifiers
Signifiers communicate where action should take place — they are the perceived cues.

```
❌ Bad: Icon-only button with no tooltip, no label, no visual cue
✅ Good: Button with label + icon + hover state that signals "this does something"
```

### Feedback
Every action must have a visible, timely response. Users must know their action was received.

```typescript
// ✅ Always give feedback: loading, success, error
async function submitForm(data: FormData) {
  setLoading(true);
  try {
    await api.submit(data);
    setSuccess('Saved successfully');
  } catch (err) {
    setError('Failed to save. Please try again.');
  } finally {
    setLoading(false);
  }
}
```

### Conceptual Models
Users build mental models of how a system works. Design should match the user's model, not the system's internal model.

- File/folder metaphor matches how people think about storage
- Shopping cart metaphor matches physical shopping
- Don't expose implementation details in the UI

### Constraints & Mappings
Constrain invalid states visually. Map controls to their effects spatially when possible.

```
✅ Disable a button when the action is not available rather than showing an error after click
✅ Place "delete" far from "save" — physical distance reduces accidental actions
✅ Use natural mapping: volume slider goes up to increase, not down
```

## Maeda's Laws of Simplicity

1. **Reduce** — remove non-essential elements; the simplest way to achieve simplicity is through thoughtful reduction
2. **Organize** — organization makes a system of many appear fewer
3. **Time** — savings in time feel like simplicity
4. **Learn** — knowledge makes everything simpler
5. **Differences** — simplicity and complexity need each other
6. **Context** — what lies in the periphery is not peripheral
7. **Emotion** — more emotions are better than less
8. **Trust** — in simplicity we trust
9. **Failure** — some things can never be made simple
10. **The One** — simplicity is about subtracting the obvious and adding the meaningful

**Apply:** Before adding a feature, ask if you can achieve the same goal by removing something else.

## Shneiderman's 8 Golden Rules of Interface Design

1. **Strive for consistency** — same terminology, layout, and actions across the system
2. **Enable frequent users to use shortcuts** — keyboard shortcuts, macros, abbreviations
3. **Offer informative feedback** — every action gets a system response
4. **Design dialogs to yield closure** — group actions with a clear beginning, middle, end
5. **Prevent errors** — design so errors are hard to make; offer simple error recovery
6. **Permit easy reversal** — undo, back, cancel — reduce anxiety about exploring
7. **Support internal locus of control** — users feel in control, not controlled
8. **Reduce short-term memory load** — display information, don't require recall

## Design Sprint Framework (Banfield / Google Ventures)

A 5-day process to answer critical business questions through design and testing:

```
Monday    → Map the problem. Set a long-term goal. Create a user journey map.
Tuesday   → Sketch. Each person sketches detailed solutions independently.
Wednesday → Decide. Critique and vote on the best sketches. Storyboard.
Thursday  → Prototype. Build a realistic-looking facade — no production code.
Friday    → Test. Interview 5 real users with the prototype.
```

**When to run a sprint:**
- Before committing engineering resources to a new feature
- When the team disagrees on direction
- When you need to validate a risky assumption
- When you're stuck and need a forcing function

**Key insight:** 5 users will reveal ~85% of usability problems. Test early, iterate, then build.

## Usability Heuristics (Nielsen)

Apply when reviewing any interface:

1. Visibility of system status
2. Match between system and real world
3. User control and freedom (undo/redo)
4. Consistency and standards
5. Error prevention
6. Recognition rather than recall
7. Flexibility and efficiency of use
8. Aesthetic and minimalist design
9. Help users recognize, diagnose, and recover from errors
10. Help and documentation

## Hierarchy and Visual Structure

From *Designing User Interfaces* (Malewicz):

```
Visual weight hierarchy: Size > Color > Contrast > Position > Shape
Spacing creates breathing room and groups related elements
Alignment creates order — align to a grid
Color should reinforce meaning, not just decorate
Typography: limit to 2 font families max; use weight and size for hierarchy
```

**Practical rules:**
- One primary action per screen
- Group related elements with whitespace, not boxes
- Use color sparingly — high-contrast for primary actions, muted for secondary
- Minimum touch target: 44×44px

## Accessibility by Default

- Semantic HTML: use `<button>`, `<nav>`, `<main>`, not `<div>` for everything
- Every image has `alt` text
- Keyboard navigation works without a mouse
- Color is never the only indicator of meaning
- Contrast ratio ≥ 4.5:1 for normal text (WCAG AA)

## Design Process Checklist

When designing a feature or screen:

- [ ] Who is the user? What is their goal in this moment?
- [ ] What is the one primary action on this screen?
- [ ] What feedback does the user get after each action?
- [ ] What happens when something goes wrong — is recovery easy?
- [ ] Can a new user understand this without reading documentation?
- [ ] Does the design match the user's mental model of the domain?
- [ ] Have we reduced everything non-essential?
- [ ] Does this work on mobile and with keyboard-only navigation?

## Anti-Patterns

- Hiding important actions behind unlabeled icons
- Error messages that say what went wrong but not how to fix it
- Modal dialogs that block users from seeing the context they need
- Forms that clear on error instead of preserving valid input
- Inconsistent terminology across the same product (e.g., "cancel" vs "dismiss" vs "close")
- Infinite scroll with no way to return to a position
- Designing for the happy path and ignoring empty states, loading states, and errors
