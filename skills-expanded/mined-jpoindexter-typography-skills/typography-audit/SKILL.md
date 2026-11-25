---
name: typography-audit
description: Use when systematically reviewing existing typography against criteria — "check this page", "audit our type", pre-launch review, design-system compliance, or inherited work of unknown quality. Produces a pass/fail finding list with evidence. Use typography-critique instead when the question is about taste rather than compliance.
---

# Typography audit

A repeatable, evidence-producing pass. An audit finds **defects against criteria**.
It does not express preferences — that's `typography-critique`.

## 1. When to invoke

- "Audit our typography" / "check this page."
- Pre-launch or pre-handoff review.
- Design-system compliance checking.
- Inherited code or design of unknown quality.
- Verifying a fix actually landed.

## 2. Required context

- **Scope** — which pages, components, breakpoints, locales, themes.
- **Criteria** — the design system, brand guidelines, and conformance target.
  Without stated criteria you're doing critique, not audit.
- **Access to the rendered artifact.** An audit from source alone is not an audit.
- Which findings are **blocking** vs. advisory.

## 3. Invariant principles

- **Audit the rendered result.** CSS review finds a subset of defects and invents
  others.
- **Every finding needs evidence** — the location, the observed value, the expected
  value, the criterion. "Line-height feels tight" is critique; "body line-height is
  1.2, system token is 1.5, at `/pricing`" is a finding.
- **Criteria before findings.** Define what pass means before looking, or you'll
  grade against a standard set after seeing the output.
- **Report what you did not check.** An audit that hides its coverage gaps is worse
  than no audit, because it licenses false confidence.
- **Accessibility findings are blocking by default.** They sit at the top of the
  source hierarchy.
- **Passing one criterion establishes nothing about another.** Contrast, resize,
  and spacing-override fail independently.

## 4. The audit checklist

Work through in order. Record pass/fail/not-checked for each.

**A. Accessibility (blocking)**
- [ ] 1.4.3 Contrast — every text/background pair, every state, incl. over imagery
- [ ] 1.4.4 Resize to 200% — no loss of content or function
- [ ] 1.4.12 Text spacing override — no loss of content or function
- [ ] 1.4.5 Images of text — inventoried and justified
- [ ] Zoom not suppressed (`user-scalable`, `maximum-scale`)
- [ ] Heading levels sequential and semantic
- [ ] Text sizes in relative units

**B. Reading**
- [ ] Measure within a defensible range at every breakpoint
- [ ] Line-height appropriate to measure and size
- [ ] Body size appropriate to face, device, and distance
- [ ] Paragraph separation single and unambiguous

**C. System compliance**
- [ ] All font sizes on-scale / on-token
- [ ] All line-heights unitless and on-token
- [ ] Weights limited to the shipped set
- [ ] No unauthorised typefaces
- [ ] Component tokens route through semantics

**D. Micro**
- [ ] Correct quotes, dashes, ellipses
- [ ] No rivers; word spacing even
- [ ] Justified text only where measure supports it
- [ ] All-caps runs tracked
- [ ] No orphans/widows in prominent text
- [ ] No faux bold/italic synthesis

**E. Data and UI**
- [ ] Tabular figures wherever numbers align vertically
- [ ] `1 l I` and `0 O` distinguishable
- [ ] Longest realistic string tested per label, per locale
- [ ] Truncation recoverable

**F. Performance**
- [ ] Only rendered weights/styles shipped
- [ ] `font-display` set explicitly
- [ ] Font-attributed CLS measured
- [ ] Preloads have `crossorigin` and are limited to critical files

**G. Internationalisation** (if in scope)
- [ ] Every script covered by a real font
- [ ] Logical properties used; RTL verified
- [ ] `lang` and `dir` set correctly
- [ ] Per-script line-height verified with real text

## 5. Failure patterns in auditing itself

| Pattern | Why it's wrong |
|---|---|
| Auditing from CSS only | Misses rendered defects; invents non-defects |
| Testing only the happy path | Defects live in longest strings, empty states, other locales |
| Testing only breakpoint endpoints | Fluid typography breaks mid-band |
| Reporting "passes accessibility" after a contrast check | Three other criteria unchecked |
| Findings without locations | Unactionable |
| No stated criteria | Critique wearing an audit's clothes |
| Omitting what wasn't checked | Manufactures false confidence |
| Grading against standards set after seeing the work | Guarantees a pass |

## 6. Evaluation procedure

1. **Write the criteria down first.** System tokens, conformance target, scope.
2. Enumerate surfaces: pages × breakpoints × locales × themes. State the sample.
3. Render each. Screenshot for evidence.
4. Work §4 A→G. Record pass / fail / **not-checked** — never leave a row blank.
5. For each fail: location, observed, expected, criterion, severity.
6. Re-run any automated checks (contrast tooling, token lint) and reconcile with
   what you observed.
7. Rank by severity: accessibility → reading → compliance → micro.
8. **Explicitly list coverage gaps.**

## 7. Output format

```
AUDIT — <scope>
Criteria: <system version> · conformance <AA|AAA> · locales <list>
Surfaces sampled: <n> of <n> (<list>)

FINDINGS (ranked)
[BLOCKING] <criterion> — <location>
    observed: <value>   expected: <value>
    evidence: <screenshot/measurement>
[MAJOR] …
[MINOR] …

PASSED: <list of checks that passed>
NOT CHECKED: <list, with reason>
```

## 8. Examples

**Pre-launch audit of a marketing site, AA target.**

> Criteria fixed first: the v2 token set, WCAG AA, EN + DE, light and dark.
> Sampled 6 pages × 3 breakpoints × 2 locales × 2 themes = 72 surfaces; rendered
> all, screenshotted each.
>
> Three blocking findings. Captions are `#8A8A8A` on white = 3.1:1 across all
> pages — fails 1.4.3 (needs 4.5:1 at that size). The pricing table clips its
> footnote row at 200% zoom — fails 1.4.4, caused by fixed `height`. And under the
> 1.4.12 spacing override the nav overlaps the logo — fails, caused by a fixed-width
> header.
>
> Two major: the German hero heading overflows at 375px, and `font-display` is unset
> on two of five faces so they default to block-like behaviour.
>
> Not checked: dark-mode contrast over hero imagery (the images are CMS-driven and I
> only had two samples), and no screen-reader pass was run. Both should be closed
> before launch — I'm not claiming they pass.

## 9. Counterexamples

- ❌ "Typography audit: looks good, maybe increase line-height a bit." — No
  criteria, no evidence, no locations. That's an opinion.
- ❌ "Accessibility: pass (contrast checked)." — Three other criteria unexamined.
- ❌ "Audited the CSS, found no issues." — Not an audit.
- ❌ Findings with no severity ranking. — Everything reads as equally urgent.
- ❌ Omitting the "not checked" section. — The most dishonest part of a bad audit.
- ❌ "Tested at 375 and 1440." — For fluid type, the middle is where it breaks.
- ❌ Auditing with lorem ipsum. — Real content is where labels overflow.

## 10. Source citations

- **WCAG 2.2** §1.4.3, §1.4.4, §1.4.5, §1.4.12 — the blocking criteria.
- Hochuli, *Detail in Typography* — the micro checklist: rivers, word spacing,
  justification limits, paragraph indication.
- Lupton, *Thinking with Type* 3e — hierarchy, paragraph composition, typographic
  conventions; when breaking a rule is appropriate (an audit must distinguish a
  deliberate break from a defect).
- Rutter, *Web Typography* — measure, font loading, figure styles, OpenType.
- Brown, *Flexible Typesetting* — responsive behaviour across the whole band.
- Stocks, *Universal Principles of Typography* — a retrieval-friendly index of
  principles to audit against.
- This pack's `../type/references/source-hierarchy.md` for resolving conflicts between
  findings.
