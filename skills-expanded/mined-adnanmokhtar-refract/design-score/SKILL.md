---
name: design-score
kind: skill
pack: ui-ux
description: Scores ONE rendered surface's hygiene against the shared rubric, from the screenshot; rejects metric-only scores. Impression is /art-direct --studio.
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Skill: design-score

Turn one rendered surface into one scorecard: per-lens verdicts, per-component verdicts, and a single **at-bar / below-bar** answer the caller can route on.

## Why this is a skill and not a paragraph

The rubric lived in `redesign.md` prose with three consumers reading it — `/redesign`, `/ui-audit` Phase 1.5, and `design-canvas`. A load-bearing step with no artifact behind it gets re-interpreted by each caller, and the cheapest interpretation wins: **derive the score from the metrics already computed and never open the image.** That produces a run that measures ten things, finds each within tolerance, and reports a mediocre page as clean — observed on a real app, where the run finished fast, claimed every page scanned, and wrote no screenshot at all.

This skill exists to make that specific outcome impossible to reach by accident.

## What the score measures — hygiene, not impression

**`at-bar` means the surface clears the craft-and-usability bar. It never means beautiful, impressive or award-level.** Every lens in the rubric asks whether something is done right: hierarchy, rhythm, states, contrast, motion present, modern register. None asks whether a demanding client would be impressed, and a still frame graded by a rubric cannot answer that.

**MEASURED, 2026-10.** Three homepage directions for a bilingual premium B2B site summed 25, 25 and 24 of 26 on this rubric (✓ = 2, Δ = 1, ✗ = 0 over 13 lenses). The owner rejected all three as "different, not the best a heavyweight creative would do". The page that later impressed went through a separate process: an independent critic, a jury-style score on four axes, and a yes / no on "impress the target executive" and "top studio".

So:

- A summed lens total is reported as **`hygiene NN/26`**, never as a quality, beauty or "best" score. It is never used to rank directions on appeal.
- Every scorecard carries `impression: not-measured`. When the caller's question is "is it impressive / premium / beautiful?", route it to the critic loop in [`studio-process.md § Step 5`](../../references/studio-process.md), run by `/art-direct --studio`. Do not raise lens verdicts to answer it.

## Inputs (precise contract)

| Input | Source | Required |
|---|---|---|
| `$RENDER` — screenshot of the surface, at one declared viewport | `visual-check` / Playwright MCP | **YES — no render, no score. Halt.** |
| `$VIEW` — the view identifier: the route **plus** the tab panel, wizard step, or open modal / drawer this render shows | caller | YES — a route with six tabs is six views and six scorecards; grading the default panel and reporting the route is the defect this field exists to prevent |
| `$RUBRIC` — the lens set | [`redesign.md § Design principles`](../../commands/redesign.md) | YES (never a second, private rubric) |
| Design tokens | `_extracted-idioms.md § Tokens` | YES — a proposal must name an existing token |
| `PRODUCT_CONTEXT` | `_extracted-idioms.md § Context` | YES for the density, hierarchy and whitespace lenses — a dense table is correct in an ERP and wrong in a storefront, and grading one by the other's norm is the most common false finding a sweep produces. Absent → grade those three lenses `NOT RUN` with the reason rather than against an implicit norm |
| Shared wrappers | `_extracted-idioms.md § Wrappers` | NO (component grading is coarser without it; say so) |
| `$DIRECTION` — the project's stated design intent | `ai/design/direction.md` | NO — but a lens whose verdict turns on INTENT rather than measurement is `NOT RUN` without it, never graded against the grader's own taste |
| `$REFERENCE` — approved surfaces and before/after pairs | `ai/design/reference/` | NO — enables the resemblance lens below |
| `$METRICS` — contrast ratios, token coverage, state coverage, axe results | the caller's detectors | NO — **inputs to lenses, never the score** |
| `$BASELINE` — a prior scorecard for this view | `ai/ui-audit/scores/<route>/<view>.md` | NO (present on a re-score; enables the before→after delta) |

## Procedure

1. **Open the render.** If there is none, halt — do not proceed on source, and do not emit a provisional score. If the image is a login wall, a blank shell or an unresolved skeleton, halt as `BLOCKED`: that is not the surface.
2. **Read the TEXT before the layout.** Before any lens, scan the rendered copy for strings that
   are not language: raw i18n keys (`stats.avg_across_orders`), untranslated fallbacks, `undefined`
   / `NaN` / `[object Object]`, a date in the wrong locale, a placeholder that shipped.

   **MEASURED, and it is the finding that justifies this whole skill.** An analytics screen with no
   data — the first screen a new account sees — rendered `stats.avg_across_orders` and
   `composition.of_orders` as user-facing text. Arabic has a `_zero` plural form that is *not* a
   synonym for `_other`, three keys defined every form except that one, and i18next fell through to
   the key itself. **Every existing check passed**: the keys are present so the i18n audit is clean,
   nothing is hardcoded so the lint is clean, and contrast, tokens and axe are all indifferent to
   what a string says. It needed someone to open the page while it was empty and read it.

   Grade the EMPTY state deliberately, because it is where this class lives: zero counts, absent
   lists, unset dates. A screen that is correct with data and broken without it is broken for every
   new account.

3. **Read the screen first.** One line each: the surface's **job**, its **primary action**, and the observed **eye path** (first / second / third). A mismatch between the observed path and the one the job implies is the screen's headline finding; record it before any lens.
4. **Grade every lens** in `$RUBRIC`: `✓` / `Δ` / `✗`, each with a one-line note **citing something visible in the image**. A lens a still frame cannot answer — motion, focus order, keyboard behaviour, performance — is `NOT RUN` with the reason. Never a tick.
5. **Grade every component** as rendered: `at-bar` / `below-bar`. Grade the **filter / control bar first and hardest** (library controls routinely keep their default theme while authored elements move on), then **charts** (their colours live in a config object, not your tokens).
6. **Fold the metrics in as evidence, not as verdicts.** A measured 3.9:1 ratio is the *citation* under a `Δ` on the contrast lens; it is not itself the lens verdict, and a lens that has only a number under it has not been graded.
7. **Grade the resemblance lens, when there is something to resemble.** With `$REFERENCE` present, compare this render against the approved surface of the same type and the nearest before/after pair: does it sit on the same side of that pair's delta? A pair is the only artifact that says *what fine looks like here* rather than in general, so cite the pair by name in the verdict. **With no reference, this lens is `NOT RUN`** — an empty library must never be graded as "resembles nothing", which would teach every later run to ignore the lens.
8. **Check the verdict against `$DIRECTION` before writing it.** A surface can be at-bar on every lens and still contradict the stated intent — spacious where the direction says dense, layered where it says flat. That is a finding, recorded against the direction and not against the rubric, because the rubric cannot see intent. The reverse is the more common error and the one to resist: **do not report a surface as below bar for doing exactly what the direction asked for.**
9. **Decide the bar.** `at-bar` when no targeted lens is `✗`, at most two are `Δ`, and no component is `below-bar`. Anything else is `below-bar`.
10. **Write the scorecard** to `ai/ui-audit/scores/<route>/<view>.md`, beside the render it was made from (`index.md` for the route's default view). The file's existence is what the caller's proof-of-work gate checks; a verdict with no file behind it is a verdict about a surface nobody looked at.

## The anti-cheat (this is the part that matters)

**Before returning, re-read your own scorecard and ask of every lens verdict: could this line have been written from `$METRICS` alone, without the image?**

If the answer is yes for every lens, the scorecard is **rejected** — return `RESCORE-REQUIRED` with that reason rather than a score. A valid scorecard contains at least one verdict that only the render could produce: a relationship between two elements, something the eye reaches in the wrong order, a component that looks unlike its neighbours, a density that reads as cramped at a spacing value that is nominally correct.

The reason this check is worth its cost: **every input in `$METRICS` is a number that is easy to be right about, and none of them answers the question the caller is asking.** A page can be 100% on tokens, clean on axe, complete on states, and still be the page its owner opens and sighs at.

## Outputs (precise contract)

```yaml
view: <route> + <tab | step | modal | default>
verdict: at-bar | below-bar | BLOCKED | RESCORE-REQUIRED
job: <one line>
primary_action: <element>
eye_path: { observed: [first, second, third], implied: [...], match: true|false }
lenses:
  - lens: <name>
    verdict: pass | delta | fail | not-run
    note: <one line, cites the image>
components:
  - component: <name>
    verdict: at-bar | below-bar
    note: <as rendered>
delta_vs_baseline: <per-lens movement, when $BASELINE was supplied>
impression: not-measured   # hygiene score only; "is it impressive?" → /art-direct --studio critic loop
render: <path to the screenshot this was graded from>
```

## When to use / NOT to use

- **USE** for every surface in a `/ui-audit` run (Phase 1.5), and for `/redesign`'s before-diagnosis and after-build scorecards, so both sides of "must beat the diagnosis" are measured the same way.
- **NOT** to decide *what to change* — that is `ui-designer`, which this skill hands its `below-bar` surfaces to.
- **NOT** to grade usability or WCAG conformance. `ux-reviewer` owns the floor. This skill records what it observes and never trades the floor for craft.
- **NOT** on an unrendered surface, ever. The halt is the point of the skill.
- **NOT** to answer "is it beautiful / impressive / award-level?". That is the independent critic loop under `/art-direct --studio` ([`studio-process.md`](../../references/studio-process.md)). A 25/26 here is a clean page, not an impressive one.

## Cross-references

- [`redesign.md § Design principles`](../../commands/redesign.md) — the rubric. Single source; never restated here.
- `ui-designer` (agent) — takes a `below-bar` scorecard and proposes the change.
- `visual-check` (frontend pack, when installed; without it, the Playwright MCP under the same authenticated / blocked-render contract, else `SKIPPED (no harness)`) — the render harness and the blocked-render contract.
- [`ui-design-sweep`](../ui-design-sweep/SKILL.md) — the closed verb set a routed finding lands in.
