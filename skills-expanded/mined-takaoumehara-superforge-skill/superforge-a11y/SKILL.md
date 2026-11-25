---
name: superforge-a11y
description: >
  Audit and fix accessibility against WCAG 2.2, ARIA, Apple, and Material
  guidance — a seven-pass run (automated, keyboard, screen reader, zoom and
  reflow, colour, motion and time, forms and errors) that produces a
  criterion-by-criterion verdict instead of a scanner dump. Covers Web, iOS,
  and Android, and the legal standard that actually applies (EN 301 549 /
  EAA, ADA Title II, Section 508, JIS X 8341-3). Use when the user says
  "accessibility", "a11y", "WCAG", "screen reader", "VoiceOver", "TalkBack",
  "keyboard navigation", "contrast", "colour blind", "compliance", "ADA",
  "アクセシビリティ", "スクリーンリーダー", "キーボード操作", "コントラスト",
  "色覚", "読み上げ", "障害", "高齢者", "WCAG準拠", "アクセシビリティ対応",
  or runs /superforge-a11y.
license: MIT
metadata:
  author: Takao Umehara
  version: "2.0"
compatibility: >
  Standalone.
  Reads docs/design.md, docs/design.html, and docs/brief.md when present.
  Writes docs/accessibility.md.
  scripts/contrast.py needs python3 (stdlib only); without it, contrast is reasoned and marked as such.
  Automated passes need the project's own runner; every manual pass degrades
  to a documented reasoning check when no runtime is available.
---

# Superforge A11y — Accessibility Audit & Remediation Engine

Accessibility is not a scanner score. A page can pass every automated rule and
still be unusable with a screen reader, unreachable by keyboard, and illegal in
the EU. This skill runs the parts a machine cannot run, and says which specific
person is blocked by each finding.

---

## 0. The rule this skill exists to enforce

**Never report a conformance result that came only from an automated tool.**

axe-core — the engine inside almost every scanner — ships 63 rules for WCAG
2.0/2.1/2.2 Level A and AA. Level AA has **55 success criteria**. The rules are
not one-per-criterion: whole criteria (focus order, meaningful sequence, link
purpose in context, error suggestion, consistent help, dragging movements,
accessible authentication) have **no automated rule at all**, because passing
them is a judgment about meaning.

So: a clean `axe` run is the *start* of the audit, and the report must say so.
Anything else is a false clearance the user will act on.

---

## 1. Scope before auditing

Fix four things and write them at the top of the report. Guess the defaults and
confirm rather than interrogating.

| | Default if unstated |
|---|---|
| **Target level** | WCAG 2.2 **AA** — 31 Level A + 24 Level AA criteria |
| **Surface** | every distinct template/screen, plus each step of the primary flow end to end |
| **Platform** | infer from the repo (Web / iOS / Android) |
| **Legal standard** | ask only if the user mentions a market; otherwise audit to 2.2 AA, which meets or exceeds every current regime → `references/conformance-and-law.md` |

Conformance is claimed for **whole pages and complete processes**, never for a
component. If a checkout is 4 steps and step 3 fails, the process fails.
Auditing one component in isolation is fine — calling it conformant is not.

---

## 2. The seven passes

Run them in this order. Each one finds what the previous one structurally
cannot. Record the evidence per pass; a pass with no evidence did not happen.

| # | Pass | Finds what nothing else finds |
|---|---|---|
| 1 | **Automated** | mechanical failures at volume — missing names, bad ARIA, contrast, lang |
| 2 | **Keyboard** | traps, unreachable controls, invisible focus, order that contradicts the layout |
| 3 | **Screen reader** | things that are announced wrong, announced twice, or not at all |
| 4 | **Zoom & reflow** | what breaks at 200% text and 320 CSS px |
| 5 | **Colour & contrast** | measured ratios, and meaning that dies in greyscale |
| 6 | **Motion & time** | vestibular triggers, timeouts, autoplay, things that move and cannot be stopped |
| 7 | **Forms & errors** | label association, error text, and whether recovery is actually possible |

Full procedure, per-pass commands, and the exact acceptance bar for each →
**`references/audit-protocol.md`**.

---

## 3. Severity is named by who is blocked

Rule IDs do not motivate a fix; a blocked person does. Every finding states the
user it stops, in one clause.

| | Meaning | Example phrasing |
|---|---|---|
| **Blocker** | Someone cannot complete the task at all | "A screen reader user cannot submit this form — the button has no name" |
| **Major** | Completable, but with real cost or guesswork | "A keyboard user reaches it, but focus is invisible on the dark panel" |
| **Minor** | Degraded, worked around | "Heading level jumps h2 → h4, so the outline is wrong" |
| **Polish** | Below the conformance line, worth doing | "Hint text would remove a re-read" |

Never pad the count. Twelve unlabelled icon buttons from one missing component
prop is **one** Blocker with twelve instances, not twelve findings.

---

## 3b. Measure contrast, do not estimate it

Relative luminance is a piecewise sRGB gamma transform, and getting it slightly
wrong moves a ratio across a pass/fail boundary without looking wrong. A design
system also has far more colour pairs than anyone checks by hand, and the
unchecked ones are where the failures are.

```bash
scripts/contrast.py "#767676" "#ffffff"                 # one pair
scripts/contrast.py --tokens tokens.json --level body   # every plausible pair
scripts/contrast.py --tokens tokens.json --level ui --over "#ffffff"
scripts/contrast.py --tokens tokens.json --json         # exit 1 on failure, for CI
```

It reads `docs/design.md`'s token file at any nesting, handles `#rgb` /
`#rrggbb` / `rgb()` / `rgba()`, and **refuses to guess on a colour with alpha
below 1** — pass `--over` to composite it first, or the pair is reported as
UNKNOWN rather than silently wrong.

**Paste its output into the report.** A computed ratio with its command is
grade A evidence (`superforge-verify/references/evidence.md`); a ratio you
reasoned to is not. And a clean run here covers 1.4.3 / 1.4.6 / 1.4.11 only —
one part of one pass out of seven, never a conformance claim.

---

## 4. Artifact

Write `docs/accessibility.md`.

```markdown
# Accessibility — <target>

> Written by: superforge-a11y · Last updated: <YYYY-MM-DD>
> Target: WCAG 2.2 <level> · Platform: <web/iOS/Android> · Standard: <EAA / ADA II / JIS / none stated>
> Passes run: <1-7, and which were reasoned rather than executed>

## Verdict
<conformant / not conformant / not assessable> — and the one sentence why

## Blockers
| # | Finding | Criterion | Who is blocked | Where | Fix |

## Major / Minor / Polish
<same shape, collapsed>

## Criterion ledger
| SC | Level | Result | Evidence |
<pass / fail / not present / not assessed — every A and AA criterion has a row>

## Not assessable without a runtime
<the passes that could not be executed here, and what is needed to close them>

## What is already right
<so it does not get broken during the fixes>
```

**`Not assessed` is an honest result. `Pass` without evidence is not.** If the
environment has no browser, no simulator, and no device, say so per pass rather
than inferring green from source code.

---

## 5. Fix mode

When asked to fix rather than audit:

1. Fix by **cause**, at the component, not at each call site.
2. Prefer the native element. `<button>` over `<div role="button">`; the ARIA
   pattern only when no element exists. **No ARIA beats bad ARIA** — a wrong
   role hides content that was working.
3. Re-run the pass that caught it, and paste the new output.
4. Add the regression check so it cannot come back →
   `references/tooling.md` (CI wiring, `jest-axe`, Playwright, Espresso,
   `XCUIApplication.performAccessibilityAudit`).
5. Update `docs/design.md` if a token changed, so the design system and the
   fix do not diverge.

---

## 6. Deeper references

- **`references/wcag22-ledger.md`** — all 86 active WCAG 2.2 criteria with
  level, version introduced, and what to actually look at for each. The AA
  set is the audit checklist.
- **`references/audit-protocol.md`** — the seven passes step by step, with the
  acceptance bar and the evidence each must produce.
- **`references/tooling.md`** — what each tool catches and what it provably
  misses, per platform, plus CI wiring.
- **`references/native-platforms.md`** — iOS (VoiceOver, Dynamic Type, traits)
  and Android (TalkBack, Switch Access, Compose semantics), including the
  criteria that mean something different off the web.
- **`references/conformance-and-law.md`** — WCAG versions, EN 301 549 / EAA,
  ADA Title II, Section 508, JIS X 8341-3, and how to write a claim that is
  not a lie.

## 7. Delegate when a sharper skill is installed

`accessibility-generator`, `audit` (a11y specialists) · `superforge-ui`
(token and component changes) · `superforge-test` (locking a fix with a test) ·
`superforge-verify` (the release gate) · `superforge-roast` (when the finding
is that the whole flow is wrong, not one control).
