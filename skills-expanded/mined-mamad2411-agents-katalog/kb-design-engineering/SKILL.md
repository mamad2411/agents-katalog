---
name: kb-design-engineering
description: Portable execution process for visual polish — translating an approved visual direction into production UI without breaking product logic. 5-step flow (scope → classify → map to system → implement with restraint → validate) plus high-leverage targets (headers, filters, tables, KPI cards, empty/loading states) and anti-patterns. Route here when a screen feels generic, a skin must be applied, or tables/cards/nav need refinement.
last-verified: 2026-04-23
---

# Design Engineering — Visual Polish Execution

> Bridge between approved visual direction and production UI code. This skill is about **applying** direction, not choosing it.
> If the direction doesn't exist yet → load `doc-visual-direction` first.

---

## 1. When to use this skill

**Use for:**

- A screen needs visual polish in code
- A selected skin must be implemented
- The UI feels correct but generic
- Tables, cards, filters, forms, or dashboards need refinement
- Design tokens need to be applied consistently
- Hover / focus / selected / pressed states need improvement
- UI refactors that must preserve product logic

**Don't use for:**

- Backend or database work
- API design
- Choosing the product's visual strategy from scratch → use `doc-visual-direction`
- Pure critique without implementation intent
- Performance tuning unrelated to UI

---

## 2. Inputs to gather before touching code

Before writing a single class, confirm (or consciously infer) the 6 inputs:

1. **Visual direction** — selected skin, trust vs novelty posture
2. **Layout direction** — shell type, density, page composition expectations
3. **Theme direction** — primitives, semantic tokens, component tokens
4. **Iconography direction** — base icon family, accent rules
5. **Motion direction** — motion tone, state transitions, reduced-motion expectations
6. **Domain constraints** — finance/admin/operator/consumer, trust requirements, a11y needs

If something is missing → state the assumption and proceed conservatively. Don't guess silently.

---

## 3. The 5-step process

### Step 1 — Identify UI scope

- Which screen(s) or components are affected
- Whether the task is shell-level, component-level, or page-level
- What must remain untouched (don't refactor adjacent code)

### Step 2 — Classify visual problems

Name the current issues explicitly. Common patterns:

- Weak hierarchy
- Same-depth surfaces (base / panel / overlay indistinguishable)
- Generic layout (no rhythm, no composition)
- Poor spacing rhythm
- Dry tables
- Weak nav identity
- Inconsistent icon treatment
- Poor interaction feedback
- Weak dark-mode contrast
- Excessive card repetition

### Step 3 — Map to system decisions

Translate each visual intent into a **system-level** change:

| Visual intent           | System decision                                                                |
| ----------------------- | ------------------------------------------------------------------------------ |
| Stronger hierarchy      | Semantic foreground tokens (e.g. `muted-foreground`) + ratio                   |
| Surface differentiation | Shadow / bg / ring tokens at 3 depths                                          |
| More rhythm in a page   | Extract a layout wrapper (if repeated 3+ times) instead of ad-hoc flex classes |
| Consistent hover/focus  | Motion primitive + token                                                       |
| Coherent icons          | Icon wrapper component + rule for base vs accent                               |

The change should live in the system (tokens, variants, wrappers) whenever possible — not scattered utility classes.

### Step 4 — Implement with restraint

**Prefer:**

- Reusable abstractions over one-off styling
- Semantic tokens over raw values
- Stable component APIs — don't reshape props for cosmetic changes
- Low-risk visual refactors
- Strong consistency across related surfaces

**Avoid:**

- Random one-off styling
- Visual overcorrection (turning a "weak" UI into a "loud" UI)
- Adding effects without hierarchy
- Touching unrelated logic
- Patterns that conflict with the design system

### Step 5 — Validate

Before declaring polish done:

- [ ] Hierarchy is clearer than it was
- [ ] Components still align with the active skin
- [ ] Dark / light (and any custom theme) still work
- [ ] Contrast remains WCAG AA
- [ ] Spacing follows the project scale
- [ ] Responsive behavior is intact
- [ ] Interaction states feel intentional (hover/focus/pressed/selected)
- [ ] UI feels more premium without losing trust

---

## 4. Common high-leverage targets

These surfaces punch above their weight — small visual investments give big perceived-quality returns:

| Target                  | Why it matters                       |
| ----------------------- | ------------------------------------ |
| Page headers            | First thing users see, sets tone     |
| Search / filter bars    | Repeated across modules, high impact |
| Data tables             | Usually the weakest visual element   |
| KPI cards               | Opportunity for accent / emphasis    |
| Dashboards              | Composition defines the premium feel |
| Sidebar / topbar        | Shell identity                       |
| Form layouts            | Consistent input treatment           |
| Modal / drawer surfaces | Elevated surface hierarchy           |
| Empty / loading states  | Often forgotten, hurts polish        |

> When time is limited, invest polish budget here first.

---

## 5. System rules (non-negotiable)

- **Favor semantic tokens over raw values.** No hex inline, no pixel literals for radius/spacing.
- **Favor component variants over repeated class strings.** If the same visual recipe appears 3+ times, extract a variant.
- **Favor wrapper components over repeated visual patterns.** Icon containers, badges, KPI tiles → wrappers.
- **Respect the domain.** Finance / admin tools should feel precise, not playful. Premium ≠ flashy.
- **Strong hierarchy beats decorative effects.** If adding blur/gradient/glow is your fix, the hierarchy is the real problem.
- **Accent treatments must have a role.** Accent on the primary action, not on every card.
- **Every visual change should improve clarity, consistency, or feel.** If it does none of the three, skip it.

---

## 6. Anti-patterns

| ❌                                                    | ✅                                                      |
| ----------------------------------------------------- | ------------------------------------------------------- |
| "Premium" = more blur + more gradient + more glow     | Hierarchy, restraint, typography, token discipline      |
| Hardcoded visual values scattered across files        | Tokens + variants                                       |
| Every card styled the same way                        | Card hierarchy (base, featured, accent)                 |
| Nav and content surfaces indistinguishable            | Differentiated surfaces (shell vs page vs overlay)      |
| No depth system (everything at the same elevation)    | Three elevation tokens used consistently                |
| Styling that makes data harder to scan                | Polish serves legibility first                          |
| Mixing multiple style families in one pass            | One coherent direction per pass                         |
| Renaming props or reshaping APIs for cosmetic changes | Change styling only; leave component surface area alone |

---

## 7. Output contract

When finishing a polish pass, produce:

- **Scope** — screens/components touched, anything explicitly untouched
- **Visual problems classified** — the issues the pass addressed
- **System changes** — tokens/variants/wrappers added or modified
- **Validation** — checklist from §3 Step 5 marked
- **Known limitations** — anything deferred (explicit, not hidden)

---

_Cross-reference: `doc-visual-direction` for choosing the direction upstream. `kb-design-system` for the token discipline rules this skill must respect. `kb-tailwind-v4` for v4-specific class syntax. `kb-ui` for component patterns in this stack._
