---
name: shadcn-quality-gate
description: Use when a shadcn/ui implementation needs an expert, evidence-first quality decision covering accessibility, design token conformance, bundle impact, form validation correctness, and Radix primitive integrity before merge or promotion.
---

# shadcn/ui Quality Gate

## Specialization

Produce one deterministic, evidence-first go or no-go decision for a shadcn/ui implementation — covering accessibility compliance, design token conformance, bundle health, form validation integrity, Radix primitive correctness, and RSC boundary safety.

This skill reviews completed implementations. It does not implement or fix components. It produces severity-tagged findings and a signed disposition. Remediation is owned by the implementing team.

## Trigger Conditions

- A shadcn/ui implementation is ready for merge or promotion to staging or production.
- A component library update introduces new variants, theming changes, or new Radix primitives.
- A form implementation needs a correctness check before shipping.
- A dark mode implementation is complete and needs contrast and token verification.
- A multi-theme update requires token conformance and cross-theme accessibility checks.
- A cross-project shared component package needs a gate check before consuming projects update.

## When Not to Use

- Initial project setup or `components.json` wiring (use `shadcn-setup`).
- Component design and CVA variant work in progress (use `shadcn-component-design`).
- Token and theme design in progress (use `shadcn-theming`).
- Form pattern implementation in progress (use `shadcn-forms`).
- Source freshness checks before starting new work (use `shadcn-source-curation`).

## Inputs

- Implementation scope: component files, `globals.css`, `tailwind.config`, form schemas, and server action handlers.
- Target framework and RSC usage (Next.js App Router, Vite, etc.).
- Accessibility requirement level (default: WCAG 2.2 AA).
- Bundle performance targets if established.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| Accessibility verdict | Radix a11y inheritance confirmed; ARIA roles, keyboard navigation, focus management, and contrast checked |
| Token conformance verdict | All color, spacing, and radius utilities traced to CSS variables; no raw arbitrary color values without justification |
| Bundle health verdict | CSS and JS bundle impact from shadcn components assessed; tree-shaking confirmed |
| Form integrity verdict | Zod schema completeness, `FormField` composition correctness, error surface coverage, and server-side validation presence confirmed |
| RSC boundary verdict | All components with browser APIs, event handlers, or React state have `"use client"` directives; no server component rules violated |
| Radix primitive verdict | Primitive APIs used correctly; `asChild` usage justified; no deprecated primitive patterns |
| Findings table | All findings severity-tagged (critical, major, minor, advisory); owner assigned per finding |
| Gate recommendation | `GO`, `GO-WITH-CONDITIONS`, or `NO-GO` with explicit reason and evidence reference |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Spot Check | Fast sanity check on a single component | Component renders, a11y snapshot passes, no console errors |
| L2 Release Gate | Full pre-merge or pre-promotion review | All verdict dimensions complete; gate recommendation issued |
| L3 Design System Audit | Token conformance across a component library | All tokens traced; no drift between light and dark; all themes checked |
| L4 Governance Baseline | Recurring quality policy for a project or team | Repeatable checklist and threshold policy documented for CI use |

## Gate Dimensions and Checks

### 1. Accessibility

| Check | Pass Criterion | Failure Risk |
|---|---|---|
| ARIA roles | Radix primitives provide correct roles automatically; custom components must declare roles manually | Screen reader misidentification |
| Keyboard navigation | All interactive components operable by keyboard per WAI-ARIA APG pattern | WCAG 2.1.1 failure |
| Focus visible | `focus-visible:ring-2 focus-visible:ring-ring` present on all focusable elements | WCAG 2.4.7 failure |
| Color contrast | Text contrast ≥ 4.5:1 (normal text) and ≥ 3:1 (large text) in both light and dark | WCAG 1.4.3 failure |
| Touch target size | Interactive elements ≥ 44×44px on touch surfaces | WCAG 2.5.5 failure |
| Reduced motion | Animations guarded with `motion-safe:` or `@media (prefers-reduced-motion)` | WCAG 2.3.3 advisory |
| Icon-only buttons | All icon-only buttons have `aria-label` | Screen reader failure |

### 2. Design Token Conformance

| Check | Pass Criterion | Failure Risk |
|---|---|---|
| No raw hex in components | No `text-[#3b82f6]` or `bg-[#fff]` patterns without a justification record | Design drift, dark mode breakage |
| Semantic token usage | Components use `bg-primary`, `text-foreground`, `border-border` etc., not raw palette classes | Theme-breaking on token update |
| CSS variable declarations | All tokens in `:root` and `.dark` blocks in `globals.css` | Dark mode rendering failure |
| `--radius` consistency | Border-radius values use `var(--radius)` derived calculations | Visual inconsistency |
| Dark mode coverage | Every light token has a corresponding dark token | Dark mode incomplete |

### 3. Bundle Health

| Check | Pass Criterion | Failure Risk |
|---|---|---|
| Tree-shaking | Only installed components imported; no barrel imports of entire shadcn registry | Bundle bloat |
| Dynamic class construction | No runtime string-concatenated Tailwind class names | Purged classes in production |
| No duplicate Radix installs | Single version of each `@radix-ui/*` package installed | Hydration errors, runtime conflicts |
| Dead component code | No installed-but-unused shadcn components in `components/ui/` | Maintenance overhead |

### 4. Form Integrity

| Check | Pass Criterion | Failure Risk |
|---|---|---|
| Zod schema completeness | Every form field has explicit validation rules; no `z.any()` | Silent invalid data |
| `zodResolver` wired | `useForm` uses `zodResolver(schema)` — not manual `validate` | Schema validation bypassed |
| `FormField` composition | Every field uses `FormField` → `FormItem` → `FormControl` → `FormMessage` chain | Errors not surfaced |
| Server-side validation | Submission target validates independently of client-side zod | Client-bypass vulnerability |
| Double-submit prevention | Submit button is disabled during `isSubmitting` | Duplicate submissions |
| Server error surface | `form.setError("root", ...)` called on server error; message displayed | Silent server failures |

### 5. RSC Boundaries

| Check | Pass Criterion | Failure Risk |
|---|---|---|
| Client directive placement | `"use client"` at the top of every component using hooks, event handlers, or browser APIs | Server render crash |
| No server import in client | Server-only modules not imported in client components | Build or runtime error |
| Children pattern | Server components pass data to client components via props, not via shared mutable state | Data leakage, hydration mismatch |
| `suppressHydrationWarning` | Used only on elements with intentional server/client divergence (e.g., `<html>` with theme class) | Masked hydration bugs |

### 6. Radix Primitive Integrity

| Check | Pass Criterion | Failure Risk |
|---|---|---|
| `asChild` justification | Every `asChild` usage has a documented reason; no reflexive use | Broken accessibility semantics |
| Primitive version pinned | `@radix-ui/*` versions pinned; no `*` or `latest` ranges | Unexpected breaking changes |
| Deprecated APIs absent | No use of deprecated Radix prop names or removed primitives | Runtime errors on package update |
| Portal container | `Dialog`, `Sheet`, `Popover`, `Tooltip` portals render in correct DOM container | Z-index, scroll, and focus trap failures |

## Severity Classification

| Severity | Definition | Gate impact |
|---|---|---|
| Critical | WCAG failure, security risk, data loss, or build failure | Blocks `GO` |
| Major | Functional regression, form data loss, or significant UX degradation | `GO-WITH-CONDITIONS` minimum; prefer `NO-GO` |
| Minor | Visual inconsistency, token drift, or non-blocking UX gap | `GO-WITH-CONDITIONS` acceptable |
| Advisory | Best practice recommendation; no functional impact | Does not block `GO` |

## Gate Recommendation Rules

- `GO`: Zero critical findings, zero major findings, all minor findings have mitigation plans.
- `GO-WITH-CONDITIONS`: Zero critical findings; major findings have signed remediation commitments with owners and dates.
- `NO-GO`: Any critical finding unresolved, or major findings without owner commitment.

## Pragmatic Stop Rule

Stop when all six gate dimensions are assessed, all findings are severity-tagged and owned, and the gate recommendation is issued with explicit evidence references. A dimension may be marked N/A with justification if it genuinely does not apply to the scope.
