---
name: ux-principles-skill
description: >-
  Apply established UX, interaction-design, and visual-design principles when
  designing, building, or reviewing any user-facing interface or flow. Use when
  creating or editing UI components, screens, forms, navigation, or layouts;
  when making product/interaction decisions (goals, personas, postures, states);
  when setting type, hierarchy, and visual structure; and when reviewing or
  auditing usability, accessibility, or polish. Grounded verbatim in seven
  foundational books — Norman (Design of Everyday Things), Cooper (About Face),
  Lidwell (Universal Principles of Design), Lupton (Thinking with Type),
  Buxton (Sketching User Experiences), Rogers/Sharp/Preece (Interaction Design),
  and Moggridge (Designing Interactions).
---

# UX Principles

A practical toolkit that distills seven foundational UX / interaction-design /
visual-design books into working reference files. Each file teaches the source
author's **exact vocabulary, rules, numbers, and examples** — not generic advice —
so you can design interfaces from scratch, make better decisions while writing UI
code, and review interfaces against proven principles.

Every reference is grounded in a specific book and cites it. The point is to apply
the *named* concept correctly (a "sovereign posture," a "Gulf of Evaluation," a
"river" in justified text), with the reasoning behind it, rather than assert taste.

## When to use this skill

Activate whenever the work touches a human-facing interface:

- **Designing from scratch** — a new screen, feature, flow, or product.
- Creating or modifying UI components, screens, forms, modals, navigation, layouts.
- Making **product/interaction decisions** — user goals, personas, scenarios, postures, states.
- Setting **type, hierarchy, spacing, and visual structure**.
- Structuring **information architecture**, navigation, or user flows.
- Exploring **alternatives** before committing to a design.
- Reviewing a PR, screen, or flow for **usability, accessibility, or polish**.

If the task is purely backend/infrastructure with no user-facing surface, this skill
usually does not apply.

## How to use it

1. **Decide the mode** — are you *framing* a problem, *creating* part of an interface,
   or *reviewing* one?
2. **Load only the reference(s) the task needs** (progressive disclosure). Pick by topic
   from the table below; don't dump all of them.
3. **Apply the named principles concretely** in the code/design you produce — use the
   book's vocabulary and the **Apply:** lines in each file.
4. **Self-check** against the relevant file's checklist and `usability-heuristics.md`
   before finishing.

## Reference files

Each file is a self-contained distillation of one (or two) of the source books.

| File | Grounded in | Use it for |
|------|-------------|-----------|
| [design-of-everyday-things.md](references/design-of-everyday-things.md) | Norman | Cognitive foundations — affordances vs signifiers, mapping, feedback, conceptual models, the two Gulfs, Seven Stages of Action, constraints, forcing functions, slips vs mistakes, designing for error, human-centered design. |
| [goal-directed-design.md](references/goal-directed-design.md) | Cooper, *About Face* | Users & product behavior — goals vs tasks, the three goal types, personas & persona types, scenarios, requirements-as-needs, the four **postures**, orchestration/flow, and **excise**. |
| [design-principles.md](references/design-principles.md) | Lidwell, *Universal Principles* | A catalog of ~50 UI-relevant principles/laws — Gestalt grouping, signal-to-noise, Hick's & Fitts's laws (with formulas), 7±2/chunking, progressive disclosure, 80/20, aesthetic-usability effect, and more. |
| [typography.md](references/typography.md) | Lupton, *Thinking with Type* | Readable, structured type — anatomy & classification, kerning/tracking, leading, **measure**, alignment rules, rivers/widows/orphans, hierarchy, grids, and punctuation — with CSS. |
| [interaction-design-process.md](references/interaction-design-process.md) | Rogers/Sharp/Preece + Moggridge | The process — usability & UX goals, the Double Diamond, the four activities, conceptual models, the five interaction types, data gathering, prototyping fidelity, and evaluation (heuristic eval, cognitive walkthrough, Fitts' Law), plus Moggridge's durable lessons. |
| [sketching-and-ideation.md](references/sketching-and-ideation.md) | Buxton, *Sketching UX* | Exploring alternatives — "getting the **right** design vs the design right," sketch-vs-prototype, the design funnel, and concrete ideation methods (10+10, storyboards, Wizard of Oz, paper prototyping) adapted for an AI agent. |
| [usability-heuristics.md](references/usability-heuristics.md) | Nielsen / Shneiderman / Norman / WCAG | Reviewing & auditing — Nielsen's 10 heuristics, Shneiderman's 8 golden rules, WCAG POUR accessibility checks, severity ratings, and the finding-report format. |

**Routing shortcuts:**
- *"Design X from scratch"* → goal-directed-design (frame goals/personas/postures) → sketching-and-ideation (explore) → design-of-everyday-things + design-principles (apply) → typography (type) → usability-heuristics (self-review).
- *"Why is this hard to use?"* → design-of-everyday-things (gulfs, mapping, conceptual model).
- *"Who is this for / what should it do?"* → goal-directed-design.
- *"Lay this out / establish hierarchy"* → design-principles (+ typography).
- *"Set the type / make this readable"* → typography.
- *"Structure the process / evaluate / prototype"* → interaction-design-process.
- *"Explore options before building"* → sketching-and-ideation.
- *"Review / audit / accessibility check"* → usability-heuristics.

## Core defaults (apply even without opening a reference)

Highest-leverage rules, each drawn from the references. Default to them.

1. **Design for goals, not features or tasks.** Ask what end-state the user wants, then
   make the shortest sound path to it. Remove steps that serve only the tool — **excise** (Cooper).
2. **Match the user's mental model, not the implementation model** (Cooper/Norman). The
   represented model should reflect how users think, not how the code works.
3. **Close the Gulfs** (Norman). Make possible actions **discoverable** (Gulf of Execution)
   and make system state **perceivable and interpretable** (Gulf of Evaluation).
4. **Always show system status** with **feedback** within ~100ms; nothing silently succeeds
   or fails; prefer **modeless feedback** over interrupting dialogs.
5. **Design every state, not just the happy path.** Empty, loading, partial, error, success,
   zero-results, offline, first-run. Missing states are the #1 source of bad UX in real apps.
6. **Design for error** (Norman). Constrain inputs, prevent errors, make actions reversible
   (prefer **undo** over confirmation), and write messages that say what happened and how to
   fix it — never blame the user (root-cause, not blame).
7. **Recognition over recall.** Show options and context; put knowledge **in the world**, not
   in the user's head (STM holds only ~3–5 items).
8. **Respect hierarchy and grouping** (Gestalt + Lidwell). Use proximity, alignment, size,
   weight, and whitespace so the eye lands on the most important thing first. One clear
   primary action per screen.
9. **Readable type by default** (Lupton). Body ≥16px, line-height ~1.4–1.6, **measure**
   45–75 characters, contrast ≥4.5:1. See typography for the full rules.
10. **Choose the right posture** (Cooper). Sovereign apps optimize for perpetual intermediates
    and fill the screen with a quiet visual style; transient apps are bold, obvious, single-window.
11. **Be consistent** and follow standards unless you have a good reason not to — deviating
    forces users to relearn every idiom.
12. **Accessibility is not optional** (WCAG POUR). Keyboard-operable, visible focus, semantic
    HTML, labels on inputs, ≥4.5:1 contrast, ≥44px targets, don't rely on color alone, respect
    reduced motion.
13. **Get the *right* design before you get the design right** (Buxton). For non-trivial UI,
    propose 2–3 cheap, disposable alternatives before committing to one.

## Quick workflows

**Designing from scratch (screen / feature / product)**
Frame the user & goal (goal-directed-design) → explore 2–3 directions cheaply
(sketching-and-ideation) → apply cognitive & layout principles (design-of-everyday-things,
design-principles) → set the type (typography) → design every state with real copy →
self-review (usability-heuristics). Scale the phases to the task; never skip framing or review.

**Creating a single screen/component**
1. State the user goal and primary action in one sentence.
2. Sketch 2–3 layout options (words or ASCII wireframe); pick one and say why.
3. Enumerate every state (empty/loading/error/success/edge) and design each.
4. Build it applying hierarchy, feedback, type, and accessibility defaults.
5. Self-review against `usability-heuristics.md`.

**Reviewing an interface / PR**
1. Identify the primary user goal of the screen.
2. Walk the heuristics in `usability-heuristics.md`; note violations with location + severity.
3. Check the accessibility (POUR) and forms checklists.
4. Report findings as: *issue → where → principle violated → severity → suggested fix.*

## Guardrails

- **Scope.** These references teach *principles and process* grounded in the seven books.
  They deliberately do **not** prescribe a specific color system, spacing scale, design-token
  architecture, or component library — for those, **follow the existing project's conventions
  and design system first**, and apply these principles on top. When a token, component, or
  pattern already exists, reuse it before inventing one.
- Principles are defaults, not dogma. State the tradeoff when you deviate, and deviate
  toward the user's benefit — not the implementation's convenience.
- Never design **dark patterns** (forced continuity, confirm-shaming, hidden costs,
  sneak-into-basket, hard-to-cancel). If asked, flag the ethical issue and offer an honest
  alternative. (See the ethics note in `usability-heuristics.md`.)
- The source books live in `references/` locally but are **copyrighted and never committed**;
  only these distilled `.md` files ship.
