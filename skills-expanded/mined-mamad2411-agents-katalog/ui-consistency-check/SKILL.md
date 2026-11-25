---
name: ui-consistency-check
description: Runs a structured visual/UI design-system consistency check across a project's web and/or mobile frontend — design token usage (colors, spacing, typography scale, border-radius, shadows) sourced from a single system rather than hardcoded per component, component reuse vs. visually inconsistent duplicate implementations (buttons, modals, form fields, cards, badges), typography and font-family consistency, spacing/layout-grid and responsive-breakpoint consistency, semantic color and dark-mode/theme-token consistency, interaction-state (hover/focus/active/disabled) and iconography consistency, design-system-to-code drift (Storybook/Figma/style-guide vs. shipped implementation), cross-platform (web/iOS/Android) token consistency, motion/animation timing consistency, and empty/loading/error-state pattern consistency — then reports the results as one table (check, area, status, evidence, recommendation). Explicitly does not cover color-contrast ratios, focus-indicator visibility, or other accessibility-specific visual requirements (that's the accessibility-check skill) or code-level duplication/maintainability of components (that's the code-review/architecture-review skills) — this skill's angle on duplicated components is the visual/UX inconsistency a user would notice, not code cleanliness. Use this whenever the user asks for a "UI consistency check", "UI consistency audit", "design system audit", "design system consistency check", "visual consistency check", "visual consistency audit", "design token audit", "component consistency check", "style consistency check", "UI/UX consistency review", "brand consistency check", "cross-platform consistency check", "ui design konsistenz prüfen", "design-system-konsistenz", "design-system prüfen", "designsystem audit", "visuelle konsistenz prüfen", "konsistenzprüfung ui", "styleguide prüfen", "corporate design prüfen", or "markenkonsistenz prüfen" — even if they only name one or two specific items this covers (e.g. "are our buttons consistent" or "check if we're using design tokens everywhere") rather than asking for a full audit.
---

# UI Consistency Check

A structured, evidence-based check of a project's visual design against its own design system —
does the shipped UI actually look and behave like one coherent product, or has it drifted into a
patchwork of near-duplicate components, one-off magic values, and per-screen reinventions of the
same pattern. This is a **visual/UX consistency** review — the question throughout is "would a
user browsing multiple screens notice this looks/feels inconsistent," not "is this code clean." It
is a peer to two other skills and deliberately does not re-cover their ground:

- **accessibility-check** owns color-contrast ratios, focus-indicator visibility, and every other
  accessibility-specific visual requirement. If a color/contrast issue surfaces while you're
  looking at semantic color usage here, note that it exists in one line and point the user at
  `accessibility-check` rather than computing a contrast ratio here.
- **code-review** / **architecture-review** own code-level duplication and maintainability — is
  the *implementation* of two similar components copy-pasted, hard to change safely, badly
  factored. This skill's lane is the parallel but distinct problem: two independently-built
  versions of "the same" UI element that render *differently* (different padding, corner radius,
  color, font) so a user perceives the product as inconsistent, even if the underlying code were
  perfectly clean. When a finding could be filed either way (e.g. a duplicated Button
  implementation that is both hard to maintain *and* visually drifted), report the visual angle
  here and note in one line that the code-quality angle belongs to those skills.

## Ground rules

- **Evidence or it didn't happen.** Every row needs a concrete pointer — a `file:line`, an actual
  hex/pixel/rem value found via grep, a named pair of components/screens whose rendered properties
  you actually compared, or an explicit note that this needs a human/designer's judgment call.
  Never write "the UI looks consistent" or "this follows the design system" without having opened
  the actual token file and the actual component files and compared them.
- **Sample breadth, not one instance.** A single hardcoded hex value is a rounding error; the same
  hardcoded hex value (or the same drifted pattern) recurring across many components/screens is a
  systemic problem. Grep across the whole component tree and report *how widespread* the drift is
  (e.g. "14 of 22 button usages bypass the `Button` component" not just "found one inline button"),
  not just the first hit.
- **This is static investigation of code/styles/markup, not a live pixel-diff or a designer's
  aesthetic opinion.** You can check what's checkable from source: token definitions, hardcoded
  literals, component implementations, and doc/spec files. You cannot render every screen in a real
  browser/simulator and eyeball it, and "is this palette pleasant" is not this skill's question —
  "does this palette get applied consistently" is. Say this once, up front.
- **Boundary vs. accessibility-check:** don't compute or restate color-contrast ratios, focus-ring
  visibility, or touch-target sizing here — flag that the surface exists and point to
  `accessibility-check`. **Boundary vs. code-review/architecture-review:** don't build out a full
  code-duplication/maintainability finding here — a one-line pointer suffices when a finding could
  be filed either way; this skill's version of "duplication" is about what the user sees, not the
  underlying code.
- **Don't invent scope you can't check, and don't silently drop scope either.** No design-token
  system exists at all yet → say so and mark the token-usage checks `➖ N/A` with that one-line
  reason (a real, reportable finding in itself — see UI1). No mobile app → mark mobile/cross-platform
  checks `➖ N/A`. Backend-only project with no UI → mark the entire skill `➖ N/A` with that one-line
  reason rather than forcing rows. Every check in this file gets a row; none are quietly skipped.
- **Be genuinely thorough.** Don't stop after checking the two or three most obvious components
  (buttons, one modal) — the checks that take real digging (icon-set mixing, animation timing
  drift, empty-state reinvention per feature) are usually exactly the ones nobody has looked at
  before and where the biggest findings live.

## Workflow

1. **Identify the stack and whether a design-token/component system exists.** Determine the UI
   framework(s) (React/Vue/Angular/plain CSS on web; SwiftUI/UIKit on iOS; Jetpack Compose/XML on
   Android; React Native/Flutter cross-platform), and whether the project is single-platform or
   spans web + iOS + Android. Look for a token/theme source: CSS custom properties (`:root { --* }`),
   a Tailwind/theme config (`tailwind.config.*`), a Style Dictionary or other JSON/YAML token file,
   a shared component package (`packages/ui`, `@org/design-system`), a Storybook instance
   (`.storybook/`), or a linked Figma library referenced in docs. If none of this exists, say so
   explicitly — "no shared design-token system found" is itself the first, most important finding,
   not a reason to skip the rest of the check (fall back to comparing raw values directly across
   components instead of against a token source).
2. **Work through the checklists below**, grouped by theme — every check gets a row, marked
   ✅/❌/⚠️/➖. Investigate with actual Grep/Read: search for raw hex codes, arbitrary pixel/rem
   values, and duplicate component names/patterns rather than assuming a design system is followed
   just because it exists.
3. **Sample multiple screens/components and compare them against each other and against the
   documented system**, not just one. For each "same" UI pattern (button, modal, card, form field,
   badge, empty state, loading state), find at least 2-4 independent usages/implementations across
   different features/screens and diff their actual rendered properties (padding, color, radius,
   font, transition timing) — that comparison, not a single file's contents, is the evidence a
   consistency finding needs.
4. **Report as one table**, most widespread/most user-visible drift first within each area, followed
   by the prioritized punch list and needs-review list.

## Design tokens & theming architecture

**UI1 — A single design-token/theme source exists and is the one source of truth.** Confirm there
is exactly one place colors, spacing, typography, radius, and shadow values are defined (a theme
file, CSS variables, a Tailwind config, a Style Dictionary JSON). If there are *multiple*
competing token sources (e.g. a legacy SCSS variables file *and* a newer CSS-custom-properties file
*and* inline Tailwind config values that don't reference either), that's a `❌` in itself — report
each source found and which components pull from which. No token system at all → `➖ N/A`, but state
that this is a foundational gap everything else in this file will surface symptoms of.

**UI2 — Colors sourced from tokens, not hardcoded hex/rgb values.** Grep component files for raw
color literals (`#[0-9a-fA-F]{3,8}\b`, `rgb(`, `rgba(`, `hsl(`) outside the token/theme file itself.
Report the count and a representative sample of files/lines — a handful of one-off values in
prototype/test code is a minor note, but hardcoded colors recurring across dozens of components
(especially the *same* color repeated as a literal instead of referencing its token) is a systemic
`❌`. Cross-check whether any of those hardcoded colors duplicate an existing token's value under a
different literal — a strong signal the token exists but isn't being used.

**UI3 — Spacing, radius, and shadow values sourced from tokens, not arbitrary literals.** Grep for
raw pixel/rem/em margin, padding, `border-radius`, and `box-shadow`/`elevation` values outside the
token system (e.g. `padding: 13px`, `border-radius: 6px` when the token scale defines 4/8/16/24,
arbitrary Tailwind bracket values like `p-[13px]` bypassing the configured spacing scale). Report
how many distinct one-off values were found and whether they cluster near an existing token (a sign
of "close enough" drift) or are wildly arbitrary.

**UI4 — Typography scale defined as tokens and actually referenced.** Confirm font sizes,
line-heights, and font-weights are defined as a named scale (e.g. `text-xs`/`text-sm`/`text-lg`, a
`typography.ts`/`type-scale.json`) rather than each component declaring its own `font-size: 15px;
line-height: 1.4;`. This check is about the *token layer*; UI7/UI8 below check whether it's actually
*applied* consistently on top of existing tokens.

## Component reuse vs. visual duplication

**UI5 — Buttons: sampled instances render consistently.** Find every place a button-like element is
implemented (a shared `<Button>`/`Button.tsx` component, but also raw `<button>`/`<a>` elements
styled ad hoc, and platform-native button views). Sample at least 3-4 instances of the "same"
button variant (e.g. primary CTA) across different screens/features and compare actual padding,
corner radius, font-weight/size, and color. Report each independently-implemented version found and
where its rendered properties diverge from the shared component or from each other — this is the
visual/UX angle (a user notices two differently-shaped primary buttons); if the underlying
implementation is also copy-pasted/hard to maintain, note that in one line and point to
`code-review`/`architecture-review` rather than building it out here.

**UI6 — Modals/dialogs: consistent chrome and behavior across instances.** Sample every modal/dialog
implementation in the codebase (a shared `<Modal>` component vs. one-off overlays built per
feature). Compare header styling, close-button placement/icon, backdrop treatment (color/opacity/
blur), corner radius, and entry/exit animation across instances. Report each independent
implementation and how its visuals diverge from the others.

**UI7 — Form fields: consistent label, border, error, and focus-state styling across the app.**
Sample text inputs/selects/checkboxes from at least 3-4 different forms/screens. Compare label
position and typography, border color/radius/thickness, spacing between label-input-helper text,
and error-state presentation. (Reminder: the *contrast/focus-indicator visibility* half of this is
`accessibility-check`'s job — only the visual-consistency-across-instances half belongs here.)

**UI8 — Cards and badges: consistent shape language across usages.** Sample card and
badge/chip/tag components used for different content types (a product card, a user card, a
notification card; a status badge, a category tag). Compare corner radius, padding, shadow/border
treatment, and typography — flag cases where visually-equivalent containers use noticeably different
shape language for no apparent content-driven reason.

## Typography consistency

**UI9 — Heading levels and body text follow the defined type scale.** Grep component/screen files
for one-off `font-size`/`line-height`/`font-weight` declarations on heading and body text that don't
reference the type-scale tokens from UI4. Sample headings of the "same" semantic level (e.g. every
page's H1, every card's title) across multiple screens and confirm they render at the same size/
weight — report specific screens where a heading of the same conceptual level renders differently.

**UI10 — Font-family consistency, no silent fallback-font rendering.** Confirm the custom/brand
font is loaded and applied consistently (check the `@font-face`/font-loading config and that
components reference the font token/variable rather than a hardcoded family name that could
mismatch it). Look for screens/components that reference a different or misspelled font-family
string, or that fail to reference the font variable at all — these render in the browser/OS default
fallback without an obvious visual error, so they're easy to miss; grep for `font-family:` outside
the token file and check each one actually matches the intended brand font's name.

## Spacing & layout grid consistency

**UI11 — Spacing scale (e.g. 4pt/8pt grid) used via tokens/utility classes, not arbitrary values.**
Beyond UI3's raw-literal grep, check whether the values that *are* present cluster on a defined
increment (multiples of 4 or 8) or are genuinely arbitrary (`padding: 13px`, `margin-top: 7px`).
Report the increment the project appears to intend (inferred from the token scale or the majority of
values found) and every value that breaks it.

**UI12 — Responsive breakpoints defined once and reused, not redefined per component.** Grep for
raw `@media (min-width:` / `(max-width:` breakpoint values across CSS/component files and compare
them against any central breakpoint definition (a theme config, a `breakpoints.ts`, Tailwind's
`screens` config). Report every breakpoint value that doesn't match the central definition (e.g. the
system defines 768px for tablet but three components use 760px/769px/800px instead) — mismatched
breakpoints cause visibly inconsistent responsive behavior between components on the same page.

## Color & theming consistency

**UI13 — Semantic colors (error/success/warning/info) used consistently for the same meaning.**
Grep for how error/success/warning states are colored across different features/screens — form
validation errors, toast/notification colors, status badges, alert banners. Confirm they all
reference the same semantic token (e.g. `--color-error`) rather than each screen picking its own ad
hoc shade of red. Report every distinct "error red" (or success green, etc.) found and where each is
used — note explicitly that this check is about *semantic consistency*, not contrast ratio
(`accessibility-check`'s job).

**UI14 — Dark mode / alternate theme sourced from theme-aware tokens throughout.** If the project
supports a dark mode or alternate brand theme, grep for hardcoded colors (especially white/black/
light-gray literals used for backgrounds or text) that bypass the theme-aware token and would
render wrong (invisible text, wrong-colored surface) when the theme switches. If no dark
mode/alternate theme exists, mark `➖ N/A` with that reason.

## Interaction states & iconography

**UI15 — Hover/focus/active/disabled treatment consistent across equivalent interactive elements.**
Sample the same category of interactive element (e.g. all primary buttons, all list-row actions)
across multiple screens and confirm each interactive state gets a treatment, and that the treatment
looks the same everywhere it's used — flag cases where one instance implements a disabled/hover
style and a near-identical instance elsewhere has none. (Focus-indicator *visibility*/contrast
specifically is `accessibility-check`'s territory — this check is about whether the *visual
treatment* is applied consistently, not whether it's contrast-compliant.)

**UI16 — Single icon set/style used consistently, with consistent sizing relative to text.** Grep
icon imports/usages across the codebase for more than one icon library/set in concurrent use
(e.g. both `react-icons` and a custom SVG set, or mixed outline/filled styles or mismatched stroke
widths from the same conceptual set). Sample icons placed next to text labels across several
components and compare their rendered size relative to the adjacent font-size — flag icons that are
noticeably oversized/undersized relative to their text in some places but not others.

## Design-system-to-code drift

**UI17 — Documented design-system specs match shipped implementation.** If a Storybook instance, a
linked Figma library, or a written style guide exists, spot-check several components' actual
implementation (colors, spacing, radius, typography) against what the documentation specifies.
Report concrete mismatches (e.g. "style guide specifies 8px corner radius for cards;
`ProductCard.tsx:42` ships `border-radius: 4px`"). A design system that exists on paper but that the
current implementation has drifted away from is a real, reportable `❌` — do not mark this `✅`
just because the documentation technically exists; the check is whether the code still matches it.
No documented system found at all → this duplicates UI1's finding; mark `➖ N/A` here with a pointer
back to UI1 rather than repeating the same evidence twice.

## Cross-platform consistency

**UI18 — Shared brand/design tokens applied consistently across web, iOS, and Android.** Only
applicable if the product spans more than one platform — otherwise mark `➖ N/A` with that reason.
Where it does apply, compare each platform's token source (web CSS/theme file, iOS
`Colors.xcassets`/Swift constants, Android `colors.xml`/`dimens.xml`/Compose theme) for the same
brand color, spacing unit, and type scale. Report any value that has drifted independently per
platform (e.g. the brand primary blue is a slightly different hex on Android than on web/iOS) —
this is a common symptom of each platform team maintaining its own copy of the tokens instead of a
shared source.

## Motion & animation consistency

**UI19 — Transition durations and easing consistent for equivalent interactions.** Grep for
`transition:`/`animation:`/`duration:` values (CSS, or platform animation APIs) across modal
open/close, hover transitions, and loading-state transitions. Compare the duration/easing-curve
values used for the *same category* of interaction across different components (e.g. every modal's
open animation) and report where they diverge (one modal fades in 150ms ease-out, another 400ms
linear) — inconsistent timing is a common source of a product "feeling" inconsistent even when
colors and spacing check out.

## Empty/loading/error state consistency

**UI20 — Empty, loading, and error states implemented consistently across features.** Sample how
different screens/features handle having no data (empty state), waiting for data (spinner/skeleton),
and failing to load data (error state). Compare the actual components/markup used — is there a
shared `<EmptyState>`/`<Skeleton>`/`<ErrorState>` component reused across features, or has each
feature built its own one-off version with different copy tone, iconography, and layout? Report
every independently-invented version found, since these are exactly the states teams tend to
deprioritize and reinvent ad hoc per feature.

## Output format

Start with 3-4 sentences: which platform(s) were identified (web/iOS/Android/cross-platform), what
design-token/component-system source(s) were found (or the explicit absence of one, per UI1), what
couldn't be reached (no Storybook/Figma access, no live rendering to visually diff, no design
team/spec to consult), and the ground-rule caveat — this is static source investigation and sampled
comparison, not a live pixel-diff or a designer's aesthetic judgment.

Then ALWAYS use this exact table — one row per check, none omitted:

| # | Check | Bereich/Area | Status | Befund/Evidence | Empfehlung/Recommendation |
|---|---|---|---|---|---|
| 1 | ... | Tokens/Components/Typography/Spacing/Color/Interaction/Drift/Cross-Platform/Motion/States | ✅/❌/⚠️/➖ | file:line, grep results with counts, or named components compared | only if not ✅ |

(Match the table's actual language to the conversation's language — the column names above are
illustrative, not a fixed vocabulary. Keep evidence concrete: a path+line, an actual hex/pixel value
found, or the specific screens/components you compared and what diverged. Group rows by area with a
subheading or an "Area" column, whichever reads more clearly for the number of rows involved.)

Status legend:
- ✅ Pass — sampled components/screens were actually compared and render consistently, or values
  trace back to the single token source
- ❌ Fail — checked, and drift/duplication/hardcoding was actually found (cite the specific
  instances)
- ⚠️ Needs manual/design review — a genuine judgment call code can't fully resolve (e.g. is a
  visual difference intentional per a documented exception, does a near-but-not-exact value count as
  "on-scale") — give your reasoning, don't force a confident ✅/❌
- ➖ N/A — this check's surface doesn't exist in this project (no design-token system at all, no
  mobile app, no dark mode, no documented design system) — state the one-line reason; for UI1 in
  particular, the *absence itself* is the deliverable, not a reason to skip the row

End with a **prioritized punch list**: every ❌, ordered by how widespread/user-visible the
inconsistency is (systemic token-bypassing and duplicated core components like buttons/modals
first, cosmetic one-offs last), each with a one-line fix. Follow it with a **needs-review list**:
every ⚠️, since those need a designer's or product owner's call, not a mechanical fix.
