---
name: audit-app-design
description: Audit an app's UI/UX and branding (spacing, type, color, motion, touch targets, dark mode, taste). Use when screens feel off, generic or inconsistent, or before a release. For whether it works, use verify-app.
---

# Audit App Design — evidence-driven UI/UX audit with a fix loop

You are running a **design audit campaign**, not giving opinions. The sibling of verify-app: same honest-inventory discipline, applied to look-and-feel. The output is threefold: a **findings ledger** (every issue with severity and screenshot evidence), **system-level fixes** (fix the token, not the instance) each with before/after proof, and a **debt ledger + lint greps** so drift is visible after you're gone. The core rule: **audit rendered pixels, never source code alone** — code tells you what was intended; only the screenshot tells you what ships.

Companion taste sources when present: `emil-design-eng` (animation decision framework, easing, the invisible-details philosophy) and `impeccable`/`design-taste-frontend` for web surfaces. This skill is the *process* that applies that taste to a real app build.

**Load `design-taste-frontend` before Phase 2 and keep it open for the Taste dimension.** Most of that skill is web-specific (Tailwind classes, CTA copy, scroll choreography) and does not apply to a native app — ignore that. What transfers is its *anti-default discipline*: the observation that a model left to itself reaches for the same handful of looks every time, and that catching this requires naming the default and checking against it mechanically, not squinting and saying "looks fine."

## Phase 0 — Recon

0. **State the design read before you look at anything.** One line, in the ledger:
   *"Reading this as: \<app kind> for \<audience>, with a \<vibe> language, leaning toward \<aesthetic family>."*
   Everything downstream is judged against this read, and the read itself is a
   finding if it doesn't match what the app is trying to be. Without it, "taste"
   collapses into personal preference and the audit becomes unfalsifiable.
1. Find the design system: token/color/font/spacing definition files, brand docs (BRAND.md, UI_UX_SPEC.md), the platform's conventions (HIG for iOS, Material for Android). The audit measures against **the app's own system first**, platform norms second, personal taste last.
2. **Grep for drift before looking at screens** — mechanical, high-yield:
   - raw hex colors outside the token file
   - hardcoded paddings/sizes that are off-grid (not multiples of 4/8) or one-off (`13`, `17`, `22`)
   - font sizes/weights applied inline instead of via the type scale
   - animation durations and easings scattered ad hoc; repeat-forever animations with no Reduce Motion guard
   Every hit is a candidate finding; the fix is almost always "route it through the system."
3. Reuse the repo's QA affordances (verify-app's launch flags: reset-state, skip-first-run, force-capability-off, screenshot mode). If none exist, add them first — deterministic screens are the prerequisite for comparable evidence.
4. Dedicated device/simulator, same rules as verify-app: create your own, serialize runs, never the user's booted device.

## Phase 1 — Capture the evidence grid FIRST

Opinions come after pixels. Build the grid before judging anything:

- **Configs**: light × dark × default-type × accessibility-large type × smallest supported device. iOS: `xcrun simctl ui <udid> appearance dark`, `content_size accessibility-large` (underscore, not hyphen), `status_bar <udid> override --time 9:41` for clean chrome.
- **Screens**: every screen and every distinct state (empty/loading/error/populated) — take the screen inventory from the verify-app matrix if the repo has one.
- **Motion**: stills cannot judge animation. Record video (`xcrun simctl io <udid> recordVideo`), then step through frames (`ffmpeg -ss`). Capture each transition twice: normal and with Reduce Motion on (`xcrun simctl spawn <udid> defaults write com.apple.Accessibility ReduceMotionEnabled -bool true`, relaunch; confirm it took effect before trusting the recording).
- **Verify the fixture seeded** before shooting — a prior run's wiped store silently turns a "populated" sweep into an empty-state sweep.
- **Actually look at every capture.** An unreviewed screenshot is not evidence. Reviewing is where the findings come from — content pinned under floating chrome, clipped labels, and mis-fired overlays are all caught by eyes on frames, never by code reading.

Track it as a matrix in `docs/design-audit.md`: screens × dimensions, statuses ✅ audited-clean / ⚠️ finding logged (link it) / ❌ not yet audited / 🚫 needs a human (haptics, gesture feel, real-device color). Rules as in verify-app: never ✅ without naming the evidence; findings never deleted, only resolved.

## Phase 2 — The audit dimensions

Work screen by screen against this checklist. Cite the app's own system when it exists; the platform bar below is the floor, not the target.

**Typography** — limited scale (5–7 steps, not 15 ad-hoc sizes); clear hierarchy per screen (one primary, everything else earns its size); body ≥ 16px equivalent; line-height ≥ 1.3 body text; Dynamic-Type sweep renders without truncation or overlap.

**Spacing & alignment** — 4/8pt grid; one consistent screen inset (not 16 here, 20 there); optical alignment over mathematical (icons and text baselines); related items closer than unrelated (proximity = grouping); scrollable content must clear floating chrome at rest AND at max scroll — content pinned under a floating bar is a finding, not a style.

**Color & contrast** — **measure, don't eyeball**: `contrast.py` in this skill's directory computes WCAG ratios from screenshot pixels (sample the glyph's *peak* pixel — antialiasing makes most text pixels blends). AA floor: 4.5:1 normal, 3.0:1 large text — in BOTH modes. Dark mode is a designed palette, not inversion: elevated surfaces lighter than the background, desaturated accents, no pure black/white. Semantic tokens only; one accent doing one job; color never the sole signal.

**Motion** — apply the frequency framework (see `emil-design-eng`): seen 100+ times/day → no animation; keyboard/shortcut-initiated → never; occasional (sheets, toasts) → 200–350ms; rare/celebratory → may delight. Entrances ease-out; nothing appears from `scale(0)` or from nothing; pressed states respond the instant the finger lands. **Reduce Motion disables, it doesn't slow** — verify from the RM recording, and grep for repeat-forever animations missing the guard. No infinite motion in idle screens.

**Touch targets & ergonomics** — ≥ 44pt (132px on a 3x screenshot) with ≥ 8pt gaps; hit area may exceed the visual (contentShape), never the reverse; primary actions in the thumb zone (bottom half), destructive actions out of it; an element can be visible yet occluded by an overlay — a tap that lands on the wrong layer is a blocker-severity finding.

**States & feedback** — every screen's empty/loading/error states designed, not defaulted; loading style consistent (don't mix skeletons and spinners for sibling surfaces); errors in plain language, no leaked `localizedDescription`; disabled ≠ invisible; every async action acknowledges within 100ms.

**Copy** — one capitalization convention throughout (pick sentence case or title case, per surface type); consistent voice; labels say what happens, not what the widget is; icon-only buttons still need accessibility labels (an unlabeled SF Symbol button is both an a11y and an automation finding).

**Copy humanizer** — sweep every user-facing string (grep string literals in views + Localizable files, then read them as a set) for text that reads machine-generated rather than written by a person who cares:
- *Hype verbs & filler*: "unlock", "elevate", "empower", "supercharge", "seamlessly", "effortlessly", "delve", "harness", "journey". An empty state that says "Unlock your productivity journey!" gets rewritten to what the screen actually does.
- *Template cadence*: three parallel marketing clauses in a row, "X. Y. Z." staccato taglines everywhere, every sentence the same length, headline-and-subhead pairs that restate each other.
- *Robotic mechanics*: em-dash chains, "Note that…", "Simply…", "Please note", exclamation marks on non-celebratory surfaces, Title Case Mid Sentence, hedging ("may", "might", "could" stacked).
- *Wrong register*: error messages that apologize theatrically ("Oops! Something went wrong 😢") or lecture; confirmations that over-celebrate a trivial action. Errors say what failed and what to do next, in the app's own voice.
- The bar: read each string aloud — if it sounds like a press release, a chatbot, or nobody, it's a finding (paper-cut). Fixes must match the app's established voice (take 3–5 good existing strings as the reference corpus before rewriting anything), and copy rewrites on brand-carrying surfaces (onboarding, paywall) are product decisions — log with a recommendation.

**Platform conventions** — standard gestures do standard things; sheets/navigation follow the platform idiom; system spacing around system components; deviate only deliberately and consistently.

**Taste** — every other dimension asks *is this correct?*; this one asks *does this look like anyone decided anything?* An app can pass contrast, grid, target-size and Dynamic Type and still look like it came out of a generator. Run this pass with `design-taste-frontend` loaded, against the Phase-0 design read, and keep it **mechanical** — each check below is countable from the captures or greppable from the tokens, so a taste finding is evidence, not vibes.

- *Accent discipline.* **One accent, doing one job, locked across every screen.** Count the distinct hues that appear as fills or tints across the capture grid: more than one accent family (a warm app that sprouts a cold-blue button on screen seven) is a finding. Semantic colors (success / warning / danger) are exempt — they are not accents and must not double as one.
- *Palette defaults.* Name the palette family out loud and check it against the model's known reaches: warm cream + brass/clay/oxblood + espresso text; near-black plus a lone acid-green or vermilion; purple-to-blue gradient on white. These are banned **as defaults** — acceptable only when the brand genuinely calls for them and you can say why *this* palette fits *this* app. "It's a fitness app so it's black and neon" is the failure mode.
- *Type defaults.* Inter and Space Grotesk as the unexamined "safe" choice, and serif reached for because the brief felt "premium" or "editorial," are both findings. Emphasis inside a heading uses italic or weight **of the same family** — a serif word dropped into a sans headline is amateur. Check the type scale is 5–7 steps actually in use, not 15 ad-hoc sizes (which is the same finding as Typography, arriving from the other direction).
- *Shape and material sameness.* One corner radius on everything, one shadow on everything, every surface a rounded card with an accent rail — the generated-UI signature. Radii and elevation should encode hierarchy (a sheet is not a chip), not be applied uniformly because a token exists.
- *Structure earns its keep.* Numbered markers, eyebrows, dividers and section labels must encode something true — a real sequence, a real grouping. Decorative `01 / 02 / 03` over content that isn't ordered is a finding. Uppercase micro-labels are a spice, not a seasoning: count them across the grid and flag if nearly every section has one.
- *Layout sameness.* Every screen a centred column of identical cards is a finding on its own. Native apps have less freedom than a landing page — a list is a list — so judge this at the level of the screens that *could* differ (home, summary, detail, empty states) and ask whether any of them has a composition worth remembering.
- *Iconography and emoji.* Emoji as section markers or as a substitute for real iconography is a finding. Icon set must be one family at one optical weight.
- *The hero test.* Name the single most characteristic thing about this app's visual identity in one sentence. If the honest answer is "it's clean," the app has no identity yet, and that is the headline finding of the audit — not a nitpick.

Taste findings are **almost always product decisions** (see Phase 3): log with a recommendation and a before/after mock where cheap, and let the owner call it. The exception is provable inconsistency — a second accent, mixed icon families, a rogue radius — which is drift, and drift is yours to fix.

## Phase 3 — The fix loop

finding → **fix the system, not the instance** (a wrong padding fixed locally will reappear; a token fixed is fixed everywhere) → re-capture the same shot → before/after pair in the ledger → one conventional commit per logical change (follow the repo's attribution policy). Severity triage: **blocker** (unreadable, unreachable, occluded, violates RM/contrast floors) → **paper-cut** (inconsistency a user feels but can't name) → **nitpick** (only designers notice). Fix in that order; report what you didn't fix.

Cross-skill hook: **a visual fix invalidates verify-app's 🔍 rows** — if the repo has a verification matrix, update those rows in the same commit (its pre-commit gate will remind you).

Taste calls that change behavior (removing an animation, re-ordering a screen, changing brand color usage) are **product decisions — log them with a recommendation, don't apply unilaterally**. Mechanical corrections (off-grid spacing, contrast failures, missing RM guards, occluded content) are yours to fix.

## Phase 4 — Ledger & drift control

`docs/design-audit.md` keeps: the config-grid inventory, the findings table (id, severity, evidence shot, status), a **debt ledger** for accepted deviations (with the why), and a gotcha list. Optional but high-leverage: a `scripts/design-lint.sh` of the Phase-0 greps (raw hex outside tokens, off-grid magic numbers, unguarded repeat-forever) wired as a pre-commit *warning*, and a committed `design-baseline/` of reference screenshots so the next audit diffs instead of re-judging from scratch.

## Gotchas (seed the project's list with these)

- Screenshots are **pixels, not points** — a 3x device shot is 3px/pt; 44pt targets = 132px. Divide before judging sizes.
- `simctl ui` subcommand is `content_size` (underscore); values like `accessibility-large`. Appearance and content-size persist on the sim — reset them when done.
- Contrast of antialiased text: sample the glyph's darkest/lightest pixel in a box scan, not an average — averages blend text with background and understate the ratio.
- Stills lie about motion twice: they can't show easing, and they CAN show a mid-animation frame that looks like a layout bug. Confirm with video before logging.
- The seeded state can silently be an empty state (prior runs wipe stores) — check what's on screen matches what you meant to audit.
- "Hittable" in automation ≠ tappable in reality — overlays swallow taps; verify by geometry or by observed effect.
- Dark-mode auditing on a lit screenshot viewer skews perception — trust the measured ratios over your calibrated-monitor impression.

## Operating rules

- Evidence before judgment; measurements before adjectives. "Feels cramped" becomes "12pt gap where siblings use 16pt (shot 04)".
- Audit against the app's own system first — consistency beats conformance to your taste.
- The user's device is read-only territory; simulators are yours.
- Keep a session summary in the ledger: shots taken, findings by severity, fixes landed (with before/afters), what still needs a human eye or a real device (true color, haptics, gesture feel).
