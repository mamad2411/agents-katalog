---
name: apple-design-principles
description: >
  Apply Apple's 8 foundational design principles (from WWDC26) to review, critique, score, or generate UI/UX decisions.
  Use this skill whenever the user wants to evaluate a design, review a screen or flow, audit a feature for design quality,
  decide what to build or cut, check if a UI feels right, or think through how to design something for iPhone/Mac/Apple platforms.
  Also trigger when the user asks "is this good design?", "what's wrong with this UI?", "how should I design X?", or
  "review this from a design perspective." Don't wait for the user to explicitly say "Apple design principles" — invoke
  whenever the conversation is clearly about design quality, UX decisions, or product design critique.
---

# Apple Design Principles — Evaluation & Critique Framework

From Apple's WWDC26 session "Principles of great design" (Linda & Doug, Design Evangelists at Apple).

> "Design is making something with intention. It's focusing on what's most important to people, so you can build something they will truly value."

---

## How to use this skill

When asked to review, critique, score, or guide a design decision:

1. **Identify** what is being designed or reviewed (screen, feature, flow, product, component)
2. **Evaluate** through each of the 8 principles below — only spend depth on the ones that are relevant; don't force all 8 if the question is narrow
3. **Surface tensions** — note where principles pull against each other and explain the tradeoff
4. **Recommend** — end with concrete, actionable next steps, not just observations

For a full design critique, produce a **scorecard** (see format at the bottom). For a targeted question ("is this too complex?"), just address the relevant principle(s) directly and concisely.

---

## The 8 Principles

### 1. Purpose
Design with intention. Every feature asks something of the person using it — their time, attention, and trust.

**Key questions to ask:**
- Does this serve a real need people actually have?
- Would removing this feature make the product better?
- Are you building this because it's genuinely useful, or because it's technically possible?

**Red flags:** Feature bloat, unclear value proposition, solutions looking for problems, screens that exist "just in case."

**Rule of thumb:** Choosing what NOT to build is as important as what you build. If you can't articulate the human benefit in one sentence, reconsider it.

---

### 2. Agency
People need to feel in control. They should be able to explore at their own pace, do things their way, and recover from mistakes without anxiety.

**Key questions to ask:**
- Can people undo any action they might accidentally take?
- Are you interrupting people for things that don't warrant an interruption?
- Are you forcing a single path, or allowing exploration?

**Forgiveness mechanism:** Make undo trivially easy. Use confirmation dialogs only before truly destructive, irreversible actions — not as a habit. When people know they can recover, they explore more confidently.

**Red flags:** Irreversible actions with no warning, confirmation dialogs on every tap, forced linear flows with no escape, no undo.

---

### 3. Responsibility
Act in people's best interest, not just your product's interest. Privacy is a human right.

**Key questions to ask:**
- Are you only collecting data you genuinely need?
- Are permission prompts contextually explained? (Would you trust a stranger who asked for your phone number with no context?)
- If using AI: have you anticipated how the model could fail or cause harm?
- Have you added appropriate safeguards — preview, confirmation, disclaimer — before AI-generated actions are taken?

**AI design checklist:**
- What happens when the model is wrong?
- Could the output cause physical, emotional, or financial harm?
- If the risk outweighs the value: remove the feature entirely, don't just add a disclaimer.

**Red flags:** Permission requests without context, unexplained data collection, AI acting without confirmation, no recovery path from model errors.

---

### 4. Familiarity
Build on what people already know — from the real world and from established platform conventions.

**Key questions to ask:**
- Does this metaphor help people predict behavior? (Not too literal, not too abstract)
- Are things that look the same behaving the same?
- Are you following platform conventions where they exist? (Close = top-left on Mac, swipe back on iPhone, etc.)
- Are you reinventing something that doesn't need reinventing?

**Metaphor calibration:** A trash can for delete = correct (established, not too literal). A trash can for archive = broken (violates expectation). An abstract icon with no connection to prior knowledge = confusing.

**Red flags:** Inventing new patterns for standard actions, inconsistent placement of controls, visual similarity between things that behave differently, gestures that conflict with system defaults.

---

### 5. Flexibility
People use things in unpredictable contexts and have vastly different needs.

**Key questions to ask:**
- Does this work for someone with different accessibility needs (visual, motor, cognitive)?
- Have you designed for the specific strengths of each platform?
  - iPhone: quick, glanceable, touch-first, single-hand use
  - Mac: deep focus workflows, precise pointer, keyboard shortcuts, multiple windows
- Does this work on the go, at home, and in between?
- Can people make this their own — rearrange, hide, customize?

**Inclusive design mindset:** Age, language fluency, technical skill level, and physical ability all vary in your audience. The best flexibility often comes from letting people personalize rather than picking a single "correct" configuration.

**Red flags:** iPhone UIs that require two hands, Mac interfaces with no keyboard support, no accessibility labels, one-size-fits-all layouts that ignore context.

---

### 6. Simplicity
Strip away everything that doesn't serve the core purpose. This is **not** the same as minimalism.

**Two levers:**

**Conciseness** — reduce friction:
- Use plain language, not jargon
- Fewer steps to complete a task
- No redundant elements or repeated information
- Get to the point

**Clarity** — reduce confusion:
- Visual hierarchy answers: *What do I look at? What can I tap? How do I do it?*
- Use order, spacing, and contrast to rank importance
- Most important = most visually prominent
- Every element must earn its place

**Counter-intuitive insight:** Sometimes *adding* information makes something simpler. A progress bar showing "3 min remaining" is simpler than one with no context — it resolves the user's anxiety without requiring action.

**Red flags:** Interfaces that look minimal but leave users confused about what to do, walls of controls with no hierarchy, jargon in labels, tasks that require 5 steps when 2 would do.

---

### 7. Craft
Uncompromising attention to detail. Craft is the difference between something that feels polished and something that feels rushed.

**What craft looks like:**
- Typography that responds beautifully across sizes and devices
- Colors that adapt thoughtfully to light and dark mode
- Animations that feel fluid and physically grounded, not decorative
- Icons and graphics that are sharp at every resolution
- A foundation that's reliable, fast, and doesn't break

**Craft is ongoing, not a ship milestone.** A design needs to be maintained over time — updated when new hardware ships, audited when new features are added, kept coherent as the product grows.

**Red flags:** Animations that lag or feel arbitrary, colors that don't adapt to dark mode, pixelated assets, type that overflows or clips, interactions that feel inconsistent across different parts of the product.

---

### 8. Delight
Hard to define, instantly recognizable. Delight is not confetti — it's not a layer you add at the end.

**How to design for delight:**
1. Identify the emotion you want the person to feel (relaxed? confident? excited? powerful?)
2. Reinforce that emotion at every touchpoint throughout the experience — not just one moment
3. Make the experience feel human

**The key insight:** Delight is the natural result of getting all the other principles right. When someone has purpose-driven, agency-respecting, responsible, familiar, flexible, simple, and crafted experiences — the natural outcome is joy.

**Red flags:** Adding animations or flourishes that don't serve the user's emotion, calling something "delightful" because it has confetti, designing for wow-moments while the core experience is painful.

---

## Principle Tensions

No formula. Leaning into one principle sometimes feels like compromising another. Use judgment.

| Tension | How to navigate |
|---|---|
| Agency vs. Simplicity | More control = more complexity. Offer smart defaults + progressive disclosure for power users. |
| Familiarity vs. Innovation | Follow convention for standard actions; innovate where you have genuine reason to. |
| Flexibility vs. Simplicity | More options = more cognitive load. Personalization > defaults; let users opt into complexity. |
| Responsibility vs. Agency | Safety guardrails can feel restrictive. Make safeguards feel like help, not surveillance. |
| Craft vs. Shipping | Perfect is the enemy of shipped. Craft what's visible; don't polish what no one will see. |

---

## Design Scorecard Format

When producing a full critique, use this structure:

```
## Design Review: [Name of screen/feature/flow]

### Summary
[1-2 sentences: overall verdict]

### Principle-by-principle assessment

| Principle | Rating | Key observation |
|---|---|---|
| Purpose | ✅ / ⚠ / ❌ | ... |
| Agency | ✅ / ⚠ / ❌ | ... |
| Responsibility | ✅ / ⚠ / ❌ | ... |
| Familiarity | ✅ / ⚠ / ❌ | ... |
| Flexibility | ✅ / ⚠ / ❌ | ... |
| Simplicity | ✅ / ⚠ / ❌ | ... |
| Craft | ✅ / ⚠ / ❌ | ... |
| Delight | ✅ / ⚠ / ❌ | ... |

✅ Strong  ⚠ Needs attention  ❌ Missing/broken

### Top 3 issues (prioritized)
1. [Most critical issue + why it matters + how to fix it]
2. ...
3. ...

### What's working well
- ...

### Recommended next steps
- ...
```

Skip the scorecard for narrow questions — just answer directly using the relevant principle(s).
