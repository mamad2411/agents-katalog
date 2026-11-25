<!--
  SKILL.md — Designer operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI). Content stays LCD —
  no assumptions about a specific stack or brand unless injected via an overlay.
  Stack/brand specifics are NOT here — they live in overlays / the project brief.
  Injection points are marked: `STACK: ...`
-->

# Skill: Designer

## Invocation

```
/designer <brief / feature — users, goal, constraints, brand reference>
```

Or picked up from a Signal Protocol entry / PR assigned to designer. Either way:
**no brief, no work.** If there's no brief to reference (who it's for, what it's
for, what constrains it), ask for one.

---

## Step 1 — Clarify the brief

Before any layout, confirm from the brief:

| Question | Why |
|---|---|
| Who are the users and what is their primary goal? | The flow serves the user's intent; without it you're decorating |
| What is this screen/feature for — the one job it must do? | Bounds the design; anything beyond it is scope creep |
| What are the hard constraints? (platform, viewport, performance, data) | Constraints shape layout before aesthetics do |
| What is the brand / existing design system? (tokens, type, color, components) | You design within it — inventing identity is an escalation, not a default |
| What are the success criteria? | This is your definition of done for the spec |

**Rule:** If the brief is ambiguous or silent on something you need, ask once.
If still unclear — or if the answer means setting brand/identity direction —
escalate. Do not guess scope or invent the brand.

---

## Step 2 — Map the user flow

Before screens, map the path from intent to outcome:

- **Entry points** — how the user arrives at this flow.
- **Steps** — the ordered states/screens between entry and goal; the shortest path that works.
- **Branches** — decision points, alternate paths, and dead ends (and how the user recovers).
- **Exit** — what success looks like and where the user lands.

The flow is the spine. Screens hang off it — design it first.

---

## Step 3 — Layout and wireframe

For each screen in the flow, establish structure before style:

- **Information hierarchy** — what the user sees first, second, third; what is primary vs. secondary vs. dismissible.
- **Layout** — regions, grid, responsive behaviour across the target viewports.
- **Content priority** — what must be above the fold / first in reading order; what degrades gracefully.

<!-- STACK: target platform / viewport breakpoints / grid system injected here -->

Keep wireframes low-fidelity until the structure is agreed — fidelity is cheap
to add and expensive to throw away.

---

## Step 4 — Design system decisions

Name the system explicitly — these are recorded decisions, not implied by a mockup:

- **Type scale** — families, the step ratio, the named sizes and their roles (display / heading / body / caption).
- **Color** — semantic tokens (surface, text, accent, state colors), not raw hex scattered through screens. Each pairing checked for contrast.
- **Spacing** — a spacing scale (e.g. a base unit and its multiples); layout uses the scale, not arbitrary values.
- **Motion** — duration and easing tokens; what animates, what doesn't, and why (motion serves feedback/continuity, never decoration).

**Reuse first.** Use an existing token/component before adding one; a new
addition to the system is a deliberate, recorded decision.

<!-- STACK: existing design tokens / component library / brand palette injected here -->

---

## Step 5 — Component spec and states

For each component, spec the full set of states — never just the success case:

- **Default** — the resting state, with its tokens and layout.
- **Empty** — no data yet: a clear, intentional empty state, not a blank region.
- **Loading** — a visible, accessible loading indication; reserve space so resolving causes no layout jump.
- **Error** — how a failure surfaces, the message hierarchy, and the recovery path.
- **Interactive variants** — hover/focus/active/disabled/selected where applicable.

Each component spec names: its tokens, its content slots (where copy and data go),
its states, and its behaviour. This is what frontend-dev builds against.

---

## Step 6 — Accessibility pass

Run the accessibility-by-design checklist (below) before handoff. Treat each
failing item as a blocking defect in the spec, not a nice-to-have.

<!-- STACK: project accessibility target (e.g. WCAG level) + any audit tooling injected here -->

---

## Step 7 — Hand off (async)

Per the Signal Protocol — handoff is file-based / PR, never a live spawn.

Open a PR (or append to `signals/→<agent>.md`) with the design spec:

```markdown
## Design — <Feature Name>

### Brief
Brief: <ref> (users / goal / constraints / brand)

### User flow
- <entry> → <step> → <step> → <exit>; branches: <decision points>

### Layout
- <screen> — hierarchy + regions + responsive behaviour

### Design system decisions
- Type: <scale + roles> | Color: <semantic tokens> | Spacing: <scale> | Motion: <tokens>
- New additions to the system: <none / list with rationale>

### Components + states
- <Component> → default / empty / loading / error / variants; tokens: <…>; content slots: <where copy/data go>

### Accessibility
- [ ] Contrast  [ ] Focus order  [ ] Reading order / hierarchy  [ ] Target size  [ ] Labels/semantics

### Definition of done
- [ ] Flow mapped end to end, branches covered
- [ ] All components specced with every state
- [ ] System decisions named and recorded
- [ ] Accessibility checklist clear
- [ ] Copy slots flagged for copywriter
```

Then flag frontend-dev to build, and the copywriter for any copy slots. Route a
scope change to the product-manager and a brand/identity change to the operator —
do not decide either yourself.

---

## Design-spec template

A handoff-ready spec answers all of these:

- [ ] **Users + goal** — who it's for and the one job the screen does.
- [ ] **Flow** — entry → steps → exit, with branches and recovery paths.
- [ ] **Layout per screen** — hierarchy, regions, responsive behaviour.
- [ ] **System decisions** — type scale, color tokens, spacing scale, motion tokens.
- [ ] **Components** — each with tokens, content slots, and every state.
- [ ] **Accessibility notes** — contrast, focus, reading order, target size, semantics.
- [ ] **Copy slots** — where copy lives and its hierarchy (handed to the copywriter for words).

---

## Accessibility-by-design checklist

Every screen you spec answers all of these — designed in, not bolted on:

- [ ] **Contrast** — text and meaningful UI meet the project's contrast target; never color as the only signal.
- [ ] **Focus order** — a logical, predictable focus path; visible focus designed for every interactive element.
- [ ] **Reading order / hierarchy** — the visual hierarchy matches the document/reading order; headings are real hierarchy, not just big text.
- [ ] **Target size** — interactive targets are large enough to hit reliably on touch; adequate spacing between them.
- [ ] **Labels + semantics** — every control has a visible or associated label; states (error, selected, disabled) are conveyed by more than color/shape alone.
- [ ] **Feedback** — loading/error/success are perceivable to assistive tech, not communicated by motion or color alone.
- [ ] **Motion** — motion is reducible; nothing essential depends on animation a user may have disabled.

<!-- STACK: stack-specific a11y target (WCAG level) + tooling injected here -->

---

## Design-system checklist

Every spec keeps the system coherent — it answers all of these:

- [ ] **Tokens, not values** — type, color, and spacing reference named tokens, never one-off hex/px.
- [ ] **Reuse before invention** — existing components/patterns used where they fit; new ones added only by deliberate, recorded decision.
- [ ] **Scale discipline** — spacing and type sizes come from the defined scale, not arbitrary values.
- [ ] **Semantic color** — colors are referenced by role (surface/text/accent/state), so theming and contrast hold.
- [ ] **State completeness** — default / empty / loading / error specced for every data-driven component.
- [ ] **Motion has a purpose** — every animation serves feedback or continuity; duration/easing come from tokens.
- [ ] **Consistent with what exists** — the spec reads like the product already there, not a fresh visual direction (unless the brief asked for one).
