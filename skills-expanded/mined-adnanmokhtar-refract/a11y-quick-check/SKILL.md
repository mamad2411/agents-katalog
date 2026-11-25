---
name: a11y-quick-check
description: "60-second a11y pass on one screen or diff for @ux-reviewer: a machine lane (static greps, one axe route with wcag22aa, computed contrast) and a human runbook, each with its real coverage."
kind: skill
pack: ui-ux
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: a11y-quick-check

The **fast path**, not an audit. `@ux-reviewer` runs it as its Lane A when time is the constraint and the change is one screen; `/design-review`, `/enhance-ui` and `/redesign` run it for their a11y lane. It **owns no class list.** The classes, their regexes and their oracles belong to `a11y-code-scan` (static, §1–§14) and `a11y-scan` (rendered, §1–§7), both frontend pack. This skill runs a small, fixed slice of them on one surface, computes the contrast pairs, and hands a person the runbook for the lane no machine can close. For the full WCAG 2.2 AA pass, `@ux-reviewer` dispatches those detectors directly; `/frontend-audit` and `/a11y-audit` run them on a whole repo.

## Premise

**Two lanes, reported separately — because an agent can run one of them and cannot run the other.**

An unattended run executes **Lane A** and nothing else. Printing a single blended "coverage" number over both lanes is how this skill used to claim credit for work no run performed. So:

- **Lane A — machine-resolvable.** A1 one axe route, A2 the static slice and computed contrast, A3 target size stated at the right threshold. An agent closes this lane completely, or names what blocked it.
- **Lane B — human-only.** Screen-reader announcement quality, keyboard *feel*, focus-order sanity on a real device, the OS reduced-motion toggle, zoom. An agent **cannot** run these. It emits the runbook and marks the lane `NOT RUN (human lane)` — never `✓`, never silently absent.

Every finding cites `<path:line>` (or an axe rule id + DOM selector) and names the WCAG 2.2 criterion **with its conformance level**. "Looks inaccessible" is not a finding; "icon-only `<button>` at `Cart.vue:42` has no accessible name — `a11y-code-scan` §2, axe `button-name`, WCAG 4.1.2 (Level A)" is.

**How much do the auto-tools cover? Do not print a number.** Automation finds part of the problem by any measure, and the published figures measure different things — issue volume, barrier coverage — none of them the share of success criteria (`precedents/ui.md` § 58). What decides the split on *your* screen is which criteria the surface trips: a table of text and links is mostly machine-checkable; a custom combobox, a drag-reorder or a live region is mostly not.

## Scope and routing

- **Web DOM only.** React, Vue, Svelte, Angular and plain HTML screens. A native tree (React Native, Flutter, Compose, SwiftUI, Android XML) goes to `mobile-a11y-scan` (mobile pack, when installed). Without it, print `Lane A: N/A (native UI — not a DOM)` and keep Lane B; never run DOM tooling on a native tree.
- **One surface.** A screen, a component, or the files of one diff. Anything wider is `@ux-reviewer`'s full dispatch or `/frontend-audit`.
- **When the frontend pack is installed,** A1 and A2 run its detectors' own recipe and greps on the scope. **Without it,** they run the fallback below, which copies the same three static greps and the same axe tag set; the rows say `owner: a11y-code-scan | a11y-scan (frontend pack not installed — quick lane only)`.

## Procedure

### Lane A1 — one axe route (needs a browser)

Run `a11y-scan` §1 on the one route that renders the surface, in the state that shows it (the dialog open, the menu expanded), light and dark, at the desktop and 360 px widths. That recipe (`axeAt` with `TAGS`) is the **one** axe recipe in the repo; cite it, do not carry another. Report rule ids, never prose, and list `incomplete` nodes as review rows, never dropped.

Without the frontend pack, the fallback is the same tag set in **one** `.options()` object (`@axe-core/playwright` 4.13.0: chaining `.withTags()`, `.options()` and `.disableRules()` drops the earlier call, `precedents/ui.md` § 50):

```ts
const r = await new AxeBuilder({ page }).options({ runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'] } }).analyze();
```

Reach the surface first and prove it rendered (its own content marker, never `networkidle`); a route that lands on the sign-in page is `RENDER BLOCKED`, not clean. No browser, no harness → `SKIPPED (no harness)`; Lane A2 still runs. A Lighthouse score is not axe and not a conformance claim (`precedents/ui.md` § 51): report its failing audits if it ran, never the score as a pass.

### Lane A2 — the static slice and computed contrast (no browser)

**The static slice is `a11y-code-scan` §1–§3** on the files in scope: §1 non-semantic interactive control (2.1.1, A), §2 missing accessible name or label (4.1.2 / 1.3.1 / 3.3.2, A), §3 focus indicator removed (2.4.7, AA). With the frontend pack, run those three greps from its pre-flight with `ROOTS` set to the scope. Without it, run the fallback, copied from that pre-flight:

```bash
PATHS=( "$@" ); [ ${#PATHS[@]} -eq 0 ] && PATHS=( $(git diff --name-only --diff-filter=AMR HEAD -- '*.jsx' '*.tsx' '*.vue' '*.svelte' '*.astro' '*.html' '*.css' '*.scss') )
[ ${#PATHS[@]} -eq 0 ] && { echo 'scope empty — name the screen files'; exit 0; }
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|\{/\*|<!--|#(?!\{))')
TB='(?:[^>{]|\{(?:[^{}]|\{[^{}]*\})*\})*'
ICON='(?:<(?:[A-Z][\w.]*|svg|i)\b(?!'"$TB"'\baria-label)'"$TB"'/>|<(?:svg|i|mat-icon)\b(?!'"$TB"'\baria-label)'"$TB"'>(?:[^<]|<(?!/?(?:button|svg|i|mat-icon|title)\b)[^>]*>)*</(?:svg|i|mat-icon)>)'
# §1 non-interactive element with a click handler and no role (a stopPropagation-only wrapper is excluded)
rg -n -U --pcre2 '<(?:div|span|li|td|tr|p|img|section|article|label)\b(?='"$TB"'\s(?:onClick|@click|v-on:click|on:click|onclick|\(click\))\s*=)(?!'"$TB"'\srole\s*=)(?!'"$TB"'\s(?:onClick|\(click\))\s*=\s*["{]\s*(?:\(\s*\$?\w*\s*\)\s*=>\s*)?\$?\w+\.stopPropagation\(\)\s*["}])'"$TB"'>' "${PATHS[@]}" | "${NC[@]}"
# §2 icon-only and glyph-only buttons; images with no alt; placeholder-only inputs
rg -n -U --pcre2 '<(button|Button|IconButton)\b(?!'"$TB"'\b(?:aria-label|aria-labelledby|title|label)\]?\s*=)(?!'"$TB"'\{\s*\.\.\.)'"$TB"'>\s*(?:'"$ICON"'\s*)+</\1>' "${PATHS[@]}" | "${NC[@]}"
rg -n -U --pcre2 '<button\b(?!'"$TB"'\b(?:aria-label|aria-labelledby|title)\]?\s*=)'"$TB"'>\s*(?:[^\w\s<{}]{1,2}|&\w+;)\s*</button>' "${PATHS[@]}" | "${NC[@]}"
rg -n -U --pcre2 '<(?:img|Image|NuxtImg|NuxtPicture)\b(?!'"$TB"'(?:\balt|\{\s*\.\.\.)\]?\s*=?)'"$TB"'/?>' "${PATHS[@]}" | "${NC[@]}"
rg -n -U --pcre2 '<(?:input|textarea)\b(?='"$TB"'\bplaceholder\]?\s*=)(?!'"$TB"'\b(?:id|aria-label|aria-labelledby)\]?\s*=)(?!'"$TB"'\{\s*\.\.\.)(?!'"$TB"'\btype=["\x27](?:hidden|submit|button|reset|checkbox|radio|file)["\x27])'"$TB"'/?>' "${PATHS[@]}" | "${NC[@]}"
# §3 outline removed outside :focus:not(:focus-visible); Tailwind outline-none with no focus replacement on the line
rg -n -U --pcre2 '(?m)^(?![^{\n]*:not\(:focus-visible\))[^{}\n]*\{[^{}]*\boutline\s*:\s*(?:none|0)\s*(?:!important\s*)?[;}]' "${PATHS[@]}"
rg -n --pcre2 '^(?!.*\b(?:focus-visible|focus|focus-within):(?:ring|outline-(?!none\b)|shadow|border|underline|bg-)).*(?<![.\w-])(?:focus:)?outline-none\b(?!-)' "${PATHS[@]}" | "${NC[@]}"
```

**Measured** (2026-10-05): on `benchmarks/fixtures/review-decoys` (`change/web`) the fallback returns exactly the three seeded rows (RD-A11Y-01 clickable `div` close, RD-A11Y-02 `<img>` with no alt, RD-A11Y-03 placeholder-only input); on `web-dashboard` it returns the seeded glyph-only refund button (WEB-A11Y-01) plus three candidates — a backdrop `div` with `onClick` (`ui § 16` decides), an avatar `<img>` with no alt and a search input labelled only by its placeholder.

Each hit is a candidate, judged with `a11y-code-scan`'s "read the code" questions for that § and `precedents/ui.md` § 11–34 (headless primitives own role and keyboard, `ui § 12`; a shared field wrapper owns label wiring, `ui § 14`; a visible ring replaces the outline, `ui § 18`).

**Computed contrast, from the token pair.** Resolve the foreground and background **token pair** for each text and control role on the surface (the token file `design-token-audit` resolves, when it ran) and **compute** the ratio in every theme the project ships, at the default, hover, focus and disabled states — auto-tools test the default state only. Print `#595959 on #fff → 7.0:1 ✓ AA` / `#999 on #fff → 2.85:1 ✗ AA`. An unresolvable pair (a dynamic value, an unresolved var) prints `contrast: SKIPPED (pair unresolved)`, never a guess. Disabled controls and decoration are exempt; placeholder text is not (`ui § 19`). The rendered check of the same pairs is `a11y-scan` §3.

### Lane A3 — target size: two numbers, and which tool decides each

| Threshold | Criterion | Level | Use it as |
|---|---|---|---|
| **24 × 24 CSS px** | WCAG 2.2 SC 2.5.8 Target Size (Minimum) | **AA** | The **conformance floor**, with five exceptions: Spacing (a 24 px circle on each undersized target intersects no other target's), Equivalent, Inline, User-agent control, Essential (`ui § 20`) |
| **44 × 44 CSS px** | WCAG 2.2 SC 2.5.5 Target Size (Enhanced) | **AAA** | A **design target** (Apple HIG's 44 pt; Material's 48 dp is larger) — a sound house rule, stated as the house rule, never as "what AA requires" (`ui § 4`) |

**axe decides 2.5.8 only when it ran with `wcag22aa` in its tags.** axe-core 4.13.0 ships `target-size` disabled; a plain `analyze()` never runs it (`precedents/ui.md` § 49). So "axe clean" from a run without that tag says **nothing** about 24 × 24, and nothing ever says anything about 44 × 44 except a measured border-box. Print the tag set with the result, and both thresholds separately:

`target-size: axe wcag22aa clean (2.5.8 AA, 24 × 24) · house 44 target: 3 below (measured, smallTargets at 360 px)` — or `target-size: NOT RUN (axe ran without wcag22aa)`.

The measured box and the spacing exception are `a11y-scan` §5's `smallTargets` probe when the frontend pack is installed.

### Lane B — the human runbook (emit it; do not claim it)

Hand these to a person. An unattended run prints the runbook and marks the lane `NOT RUN (human lane)`.

1. **Screen reader, 5 minutes** — VoiceOver (macOS `Cmd+F5` / iOS), NVDA (Windows, free), TalkBack (Android). Listen for: buttons announced as "button" (not "graphic" or "div"); fields announcing label and state ("Email, edit text, required"); errors announced when they appear; headings spoken with their level. iOS VoiceOver behaves differently from macOS: test the platform users have.
2. **Keyboard only** — mouse away, touch off. Every action reachable; focus visible at every step; no trap outside a modal; `Esc` closes modals and returns focus to the trigger; `Enter` activates buttons, `Space` toggles checkboxes.
3. **OS reduced motion** — toggle the system setting and re-walk the flow. A CSS branch that exists in source is not proof the rendered motion stops (`motion-audit` owns the inventory).
4. **Zoom and reflow** — 200 % zoom and a 320 px-wide viewport: no content lost, no horizontal scroll outside a 2-D container (WCAG 1.4.10 Reflow, AA).

## Output

```
## A11y quick-check — <screen / component> — <date>
Scope: src/features/cart/CartView.vue + 2 components · lanes: frontend pack installed (a11y-code-scan, a11y-scan recipe)

### Lane A — machine-resolvable
A1 axe (wcag2a…wcag22aa) on /cart, light + dark, 1280 + 360: 2 violations (button-name ×1, color-contrast ×1) · 1 incomplete (bgGradient)
A2 static slice (a11y-code-scan §1–§3): 3 hits → 1 candidate
   contrast (computed from tokens): 6 pairs × 2 themes · 1 fails
   - `Button.vue:31` disabled → exempt (ui § 19) · `CartView.vue:58` muted text, dark: #6b6b6b on #1e1e1e → 3.1:1 ✗ — WCAG 1.4.3 (AA)
A3 target-size: axe wcag22aa clean (2.5.8 AA, 24 × 24) · house 44 target: 3 below (measured) — reported as the house rule

Findings (self-verified — the full judge is @ux-reviewer):
1. `CrudActions.vue:19` icon-only submit has no accessible name — a11y-code-scan §2, axe button-name, WCAG 4.1.2 (A)   [report-with-fix]
2. `CartView.vue:58` dark-theme muted text 3.1:1 — a11y-scan §3, WCAG 1.4.3 (AA)                                         [report-with-fix]
3. `Toolbar.vue:44` close button 32 × 32 — passes 2.5.8 (AA); below the house 44 target                                 Hardening (house rule)
Verification: 5 candidates → 2 findings · 0 unconfirmed · 1 hardening · 0 pre-existing · 2 refuted

### Lane B — human runbook (NOT RUN — requires a person)
screen reader · keyboard only · OS reduced motion · 200 % zoom / 320 px reflow — emitted above; nothing in this lane is claimed.

### Coverage (which lane actually ran)
Lane A: A1 axe ✓ (wcag22aa, 2 themes, 2 widths) · A2 §1 ✓ §2 ✓ §3 ✓ · contrast ✓ (default, hover, disabled; focus SKIPPED — token unresolved) · A3 ✓
Lane B: NOT RUN (human lane) — screen reader, keyboard, OS reduced motion, zoom/reflow
Not covered by this skill: a11y-code-scan §4–§14 and a11y-scan §2, §4, §6, §7 — run @ux-reviewer's full dispatch for those.
Not validated: everything in Lane B. Do not read this run as "the screen is accessible".
```

Any check that did not run prints `SKIPPED (<why>)` or `NOT RUN (human lane)` — never an empty, implicitly passing section. The `Not covered` line names the classes outside the slice, so a quick check is never mistaken for the full pass. Inline PR comments, or `ai/audits/a11y-<scope>-<date>.md`.

## Halt conditions

- This skill does not confirm a finding. Its rows are `self-verified` candidates; under `@ux-reviewer`, `/design-review` or an audit command, they go through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10 (accessibility column) with a verifier that did not produce them. Never drop a candidate; bucket it.
- Halt on any finding without `<path:line>`, an axe rule id with its selector, or a reproducible artifact (a screen-reader transcript, a screenshot).
- Halt on a severity without a named WCAG criterion **and its level**. AAA criteria and house targets are Hardening, never the AA floor (`ui § 4`).
- Halt on any target-size claim from an axe run whose tag list lacks `wcag22aa`, and on any 44 × 44 claim without a measured border-box.
- Halt on a contrast ratio that was estimated rather than computed from two resolved colour values.
- Halt on "auto-tool said clean" used as a stand-in for Lane B, and on Lane B printed as `✓` by an unattended run.
- Halt on DOM tooling run against a native tree.

## Failure modes

- **Auto-tool said clean → declared good.** axe cannot see focus order quality, announcement wording, or whether motion actually stopped. That is Lane B, and Lane B did not run.
- **"Axe clean ⇒ 24 × 24".** Without `wcag22aa` in the tags, `target-size` never ran. The previous version of this skill printed exactly that inference.
- **A AAA criterion quoted as the AA floor.** Claiming AA against 2.5.5 both over-reports the requirement and hides that 2.5.8 — with its Spacing exception — was never evaluated.
- **`aria-label` reported missing on an element with visible text.** Visible text names it; a label that differs from it breaks 2.5.3 Label in Name.
- **Tap target measured in CSS, not as a rendered border-box.** Padding miscounts, and the hit area is what the criterion is about.
- **Treating the quick check as the audit.** It covers three static classes and one route; the `Not covered` line exists so nobody reads it as more.

## Related

- `@ux-reviewer` (this pack) — the WCAG judge; this skill is its Lane A fast path, and its fallback for `a11y-code-scan` (Lane A2) and `a11y-scan` (Lane A1) when the frontend pack is absent.
- `a11y-code-scan` §1–§3 and `a11y-scan` §1, §3, §5 (frontend pack, when installed) — the classes, recipe and probes this skill runs a slice of. `/frontend-audit` and `/a11y-audit` run them in full.
- `mobile-a11y-scan` (mobile pack, when installed) — the native a11y floor; this skill routes native trees there.
- `motion-audit` (this pack) — the reduced-motion inventory; Lane B's OS toggle checks the rendered result.
- `design-token-audit` (this pack) — resolves the token pairs this skill computes; a token swap must not drop contrast below AA.
- `ui-design-sweep` (this pack) — verbs 12 `lift-contrast`, 13 `align-focus-ring`, 16 `expand-tap-target`, 18 `clarify-affordance` close the visual findings.
