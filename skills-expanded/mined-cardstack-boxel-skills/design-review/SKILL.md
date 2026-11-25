---
name: design-review
description: 'Score the taste and coherence of a built Boxel screen, card or whole app against its brief and an aesthetic bar, from captures. Runs only when asked (`/design-review`, optionally as a mode, `set`, `card <CardDef>` or `refine`, scoped with `--layout`, `--typo`, `--colour` or `--coherence`, anchored with `--benchmark`, cut to the numbers with `--score`, or `--redesign` for a bigger rebuild from existing parts). Use it when someone points at a card or app they already have and wants it reviewed or scored, or asks for a critique ("how does this look", "is this good enough", "why does this feel off"), when all screens exist and need checking as a set, and for linked CardDefs whose embedded, fitted and atom views were written in passing. It reports first and edits nothing until they choose a fix. The basics (hit areas, contrast, phone overflow, wired actions) are not scored here: the build check owns them and runs automatically after every design build.'
boxel:
  kind: skill
  tools:
    - codeRef:
        module: '@cardstack/boxel-host/tools/run-realm-code'
        name: default
---

# Design Review

_Score what was built, from what it looks like._

| Contract | |
|---|---|
| **Reads** | Captures of the built thing, and the unit's brief card when it has one: its `spec`, the acceptance lines and anti-patterns in a `designDirection` field when an earlier brief carries them, and what its `motion` field asks for, where that is filled |
| **Writes** | Never the brief card: it records decisions, not scores. The build itself only after the user picks a fix or a redesign, or asks for `refine` (which authorises its one fix round) |
| **Stops when** | The report is given and the next step (a fix round, `--redesign`, review another surface, revisit a decision, or stop) is offered in the choice UI |

Everywhere below, `## Design direction` means the brief card's `designDirection` field and
`## Motion` its `motion` field. `boxel-design`'s Look check writes only a `Look:`, a `Surface:` and a `Real details:` line into
`designDirection`: score the colour against `Look:`, the shell against `Surface:`, and
check that no proof was invented beyond `Real details:`. With no `Surface:` line, infer the surface the way
[`surface-types.md`](../boxel-design/references/surface-types.md) does and name it in the report. A brief from earlier work, or one written by hand, may carry a full direction. Every rule below
that reads `## Design direction` acceptance lines, its Views table or its Width line applies only when that
field holds them. Without them, score each format against the design-playbook's Stage 0f content matrix where one
was written (otherwise against what the isolated view shows), and `prefersWideFormat` against what
the isolated capture needs. With no brief at all, what was decided is
the build's own hand-off line, or, for existing work, what the screens show.

You review a built thing against two standards: what was decided for it, and an
aesthetic bar that a competent-but-generic result does not clear. Where they conflict, `## Design direction`
wins on *what was decided* and you judge only *how well it was executed*.

**Visual scores come only from captures.** The rendered DOM and running the controls may confirm
controls, focus, hover and behaviour. Source code is never evidence that something looks right.

**Modes.** `set` reviews every screen of an app together; reach for it whenever more than one screen
exists, because coherence across screens is the thing no single-screen review can see.
`card <CardDef>` reviews one card's formats as a family, and is the mode nobody remembers to run: in an
app, the cards behind the links are the surfaces that get built in passing and scored by nothing.
Asked for by hand on one screen, it reviews that screen. `refine` is review, then one fix round, then the user decides: asking for
`refine` is what authorises that one round (see
[`references/benchmark-and-refine.md`](references/benchmark-and-refine.md)).

## After every design build: the build check, not a review

`boxel-design` and the design-playbook decide and build; the last step is the **build check**
([`references/build-check.md`](references/build-check.md)), which is pass/fail and shows no score. It
owns the basics: hit areas, text size and contrast, phone overflow, container-query breakpoints, a
wired main action, pseudo-controls, blank regions, and fitted/embedded carrying the key fact. When a
build of an app, a card family or a page finishes, the builder captures its own work, fixes
every failing line, re-checks the views the fix touched, and reports "what I fixed / what is still
open". No scorecard, no 8.5 verdict, no invitation to a review.

This skill does **not** run after a build. It runs when the user asks for it: `/design-review`, a
critique request, or a scoped flag (*Flags*). A fix after a review is a build like any other, so a
review never chains into a second round on its own.

A review may note a missed basic once, as a note. It is a defect for the build check, not a score.

When an independent reviewer is available (a subagent with a fresh context), it scores the captures
and names the gaps from them; the main agent routes each gap (*Gap routes*) and applies the fixes.
Otherwise mark the scores provisional. Never print an internal score that a rule needed but the user
did not ask for.

## Flags

`/design-review [set | card <CardDef> | refine] [unit] [--layout] [--typo] [--colour] [--coherence] [--benchmark] [--score] [--redesign]`

The modes (`set`, `card`, `refine`) are words, not flags; see *Modes* above.

- **No flag:** the full review: the direction gate (when the brief has acceptance lines), every
  aesthetic dimension, and coherence. Prints the scorecard. The 8.5 gate applies to this run only.
- **`--layout`:** composition only. Name the surface first (the `Surface:` line, or inferred from
  [`surface-types.md`](../boxel-design/references/surface-types.md) and said in one line). On an admin,
  dashboard or back-office surface with no fixed sidebar, "no app shell" is the first layout gap,
  ahead of tile weights. Then: does something dominate, is the reading order legible from the
  capture, can the main action be found, does `prefersWideFormat` fit, does the shell match the
  brief's `Surface:` line, does the signature treatment survive into embedded and fitted. One score,
  evidence, gaps. When nothing dominates, name the move from
  [`layout-vocabulary.md`](../boxel-design/references/layout-vocabulary.md) that would (*Gap routes*).
- **`--typo`:** typography only: size and ladder in real use (including phone), role clarity, tracking on
  micro-labels, weights against the named look in
  [`style-families.md`](../boxel-design/references/style-families.md), and **suitability for this
  specific app**: what it is for and who reads it. If the pairing looks unsuitable, explain why in plain words for this app and let the
  user decide in the choice UI: keep as is / adjust sizes or weights through theme tokens / switch to a
  named pairing, with the reason. Never auto-fix. A font change edits the Theme card, so it routes
  through [`boxel-theme-development`](../boxel-theme-development/SKILL.md), never card CSS. If the
  review disagrees with a decided direction, say so once as a note, not a score.
- **`--colour`:** colour roles and restraint against the look's colour strategy, and library defaults
  beside themed controls.
- **`--coherence`:** the same gesture, accent role, type family and voice across screens (set) or across a
  card's formats (card).
- Media, detail and motion are scored only in the no-flag run; motion only if the build animates.
- Combined flags give one score per dimension and **no overall number**. A scoped run says the 8.5 gate
  was not assessed.
- Scoped runs are read-only and end with a choice scoped to the flag (*Fix loop* → *After a scoped run*):
  fixes for that dimension only, each option naming the component, catalog card or token it swaps in.
- **`--benchmark`:** anchor the scoped dimension with
  [`references/benchmark-and-refine.md`](references/benchmark-and-refine.md); otherwise say the scores
  are unanchored.
- **`--score`:** show the scores and nothing else. The review still captures and scores as usual (never
  from source), then prints only the score lines: the per-dimension scores, and for a no-flag run the
  scorecard row and the verdict. No gap list, changelog, evidence prose or fix choice. Read-only; it
  edits nothing and offers no fix round. Combines with any dimension flag and with `--benchmark`. Ask
  for the same review without `--score` to see why a score is what it is.
- **`--redesign`:** see below. User-triggered only; never part of a scoped run.

## Scoring existing work

When the user points at a card or app that already exists, nothing was just built and nothing is fixed.

1. **Pick the unit.** One card: `card <CardDef>`. An app or several screens: `set`, plus each CardDef the
   screens link to. If it is unclear which they mean, ask in the choice UI.
2. **Find the brief.** If the unit has a brief card, score against it. If not, skip Phase 1 and open
   with one line: "Reviewed without a brief: judged against what the screens show, <primary user> doing
   <main action>." Read both from the UI; if you cannot name them, that is a finding. Do not create a brief.
   Name the surface type and the shell you see in the same line ("Surface: Admin / dashboard. Shell:
   none"), the surface inferred the way [`surface-types.md`](../boxel-design/references/surface-types.md)
   does (read that file now). `Shell:` is `fixed sidebar` only when the capture shows a left sidebar of
   the app's destinations; a header over stacked sections is `none`. Never scope the shell out as "a card-only
   review": in Boxel the app is made of cards, so a card whose isolated view is the screen its user works
   in (`prefersWideFormat`, or a Home or dashboard card) owns its shell. Only a card that is one record shown
   inside another screen (a deal, a contact) has none of its own: write `Shell: n/a (record card)`. Every
   layout judgment below is made against that surface and shell.
3. **Capture** (`realm.capture` in a `run-realm-code` script in the app, `npx boxel screenshot` from a
   terminal; [`references/capture.md`](references/capture.md)).
4. **Run the build check silently, without editing**, and report it as ONE pass/fail *Basics* block
   ("9 of 14 basics fail"). If most basics fail, give no taste scores: they would be provisional until
   the basics are fixed. Offer to fix the basics first, then review, and stop there.
5. **Otherwise score** with the flags asked for (*Flags*). *Reviewing work in progress* does not apply.
6. **Report causes, not instances.** A gap is a cause: six failures from one missing theme block are one
   gap. Expect two or three root causes. Check the shell against the surface named in step 2: when the surface is `Admin / dashboard`
   or `Back-office / data tool` and `Shell:` is `none`, G1 is "no app shell → Pret UI app shell". It
   comes first, ahead of tile weights and phone fixes, and is never folded into another gap. Order
   fixes by leverage: theme tokens first (one change restyles colour, type and radius), then the shell
   and lead element, then component swaps. Say in one line what
   already works, so a round does not rewrite what nobody objected to.
7. **Patch or redesign** (starting thresholds, tunable): once the basics pass, if the taste score is below
   about 5, or most dimensions are below 6, recommend `--redesign`; otherwise a fix round.
8. **Ask**, in the choice UI. Edit nothing before the user picks:
   - "Switch to a fixed sidebar with the content scrolling beside it → Pret UI app shell (destinations:
     <the app's real ones>)" — **required, first in the list and recommended** whenever step 6 found
     "no app shell"
   - "Feature <the flagship, the newest or the key figure> as the lead tile (two columns wide, or above
     the grid)" and, right after it, "Keep them equal" — **required** whenever nothing dominates
   - "Fix the top gaps: <G1> → <its reuse>, <G2> → <its reuse>, <G3> → <its reuse>" (recommended unless
     a layout option above or step 7 says otherwise), for example "G1 → Pret UI MoneyInput, G2 → Pret UI
     Button, G3 → theme chart tokens". It lists only the gaps that have no line of their own: the shell gap
     and the lead tile are left out of it, never bundled in
   - "Fix the basics first" (when step 4 stopped the review)
   - "Redesign from existing parts (`--redesign`)", only in addition to the two layout options above,
     never in place of them
   - "Fix only <G1> → <its reuse>"
   - "Also review the linked cards" (when only one surface was reviewed)
   - "Revisit the brief or the surface type" (when the direction itself looks wrong)
   - "Stop here, change nothing" (recommended when it clears the gate)
   - and room for the user to name something else.

   **A layout option, when the layout calls for one.** The two required layout options above are
   separate lines of the list, never a clause inside "Fix the top gaps", and a bare "Redesign" never
   stands in for them (*Gap routes* → *Standout in a row of equals*).

   The list is a list: the choice UI, or lettered options in chat ending with "Something else". A
   prose line such as "fix this, review another dimension, or stop" is not a choice.

   Each fix option names what it swaps in. When the user cannot write to the realm the unit lives in (a
   catalog card, someone else's workspace), offer only "Also review the linked cards" and "Stop here,
   change nothing", and say why.

**A fix round** fixes at most three gaps, on the failing screens or cards alone, each by its route. A fix is
a build: before the first write, take the `index.md` pre-flight reads, and load
[`boxel-ui-component-discovery`](../boxel-ui-component-discovery/SKILL.md) for a `component` gap and
[`catalog-reuse`](../catalog-reuse/SKILL.md) for a `catalog` gap, however small the fix looks. A gap fixed
by hand-rolling what the catalog or a component covers is not fixed. Only a named blocker (a read-only
realm, a Spec that does not load, a component that cannot carry the card's data) skips a gap, and it stays
open. Then run the build check on every view the fix touched, at desktop and phone width, re-capture, and
re-score what changed. Report what changed and what was left alone. It never chains into a second round.

## Redesign (`--redesign`)

A bigger change than a fix round, built from parts that already exist. The user triggers it; it is never
automatic and never part of a scoped review.

1. Propose one or two options. Each names: the Pret UI components or catalog Specs it reuses (searched first,
   per `boxel-ui-component-discovery` and `catalog-reuse`), the layout move from
   [`layout-vocabulary.md`](../boxel-design/references/layout-vocabulary.md) (all eight are on the table), the
   signature treatment from [`signature-treatments.md`](../boxel-design/references/signature-treatments.md),
   and the theme tokens it changes.
2. Ask before applying. Applying is a build: take the `index.md` pre-flight reads first.
3. `boxel-design` still owns look decisions. A redesign borrows from it and invents nothing of its own, and
   it does not write the brief card.

## Gap routes

**Search before you route.** For each gap, run one quick Spec search for what the gap needs ("money
input", "formatted number", "chart", "legend"): one search over the catalog realm covers both, and the Pret
UI hits are the ones whose `ref.module` starts `@cardstack/pretui/components/` (prefer them), as
[`boxel-ui-component-discovery`](../boxel-ui-component-discovery/SKILL.md) → *Procedure* searches,
with `realm.entries.search` in a `run-realm-code` run (this skill declares the tool). One or two terms per gap is enough. The
query is an object, never a string; the realm call takes a second argument, and all the gaps go in one script:

```js
const { entries, total, incomplete } = await realm.entries.search(
  {
    filter: {
      on: { module: '@cardstack/base/spec', name: 'Spec' },
      every: [{ eq: { specType: 'component' } }, { matches: 'sidebar' }],
    },
  },
  { scope: 'cards', limit: 10 },
);
```

Leave `realms` out: the search then covers every realm the user can read, the catalog (where the Pret UI
Specs live) included, and a hit whose `ref.module` starts `@cardstack/pretui/components/` is a Pret UI
component. This differs from `boxel-ui-component-discovery`, which scopes `realms` to the catalog: here
that `ref.module` test is what keeps a Spec someone wrote in a workspace from passing as Pret UI. Use the app's own words for `matches` ("sidebar", "app shell", "data table"). On an admin,
dashboard or back-office surface, also search the structure terms from
[`boxel-ui-component-discovery`](../boxel-ui-component-discovery/SKILL.md) (app shell, sidebar, dashboard
grid, stat, chart, data table), whatever the gap's own words were. With no hit, retry once with
`matches: 'sidebar OR app shell'` and no `specType`, as
[`catalog-reuse`](../catalog-reuse/SKILL.md) says. A call that errors is retried once with the shape
above before anything else. Only if it still fails, write `reuse: not searched: <reason>` and say so in
the report; never fill `reuse:` from memory, and never route a gap `local` because the search errored.
Then route by what it found:

- **`component`**: a component does the job, even when adopting it means replacing an input, a chart
  or a display the card renders now. Fix it with that component, restyled through
  [`restyle-component.md`](../boxel-ui-component-discovery/references/restyle-component.md).
- **`catalog`**: a catalog card or Spec does it, or a reused catalog card looks like another app.
  Restyle an adopted card through
  [`restyle-reused-card.md`](../catalog-reuse/references/restyle-reused-card.md), never by editing or
  rewriting it, and record `adopted, route: …`; with no match, record the refusal before building.
- **`local`**: only when the search found nothing that fits: spacing, copy, layout or a plain bug in
  markup the card already owns. A local fix takes its values from the theme's tokens, never
  hand-picked colours or sizes. A hand-rolled app frame (header, sidebar, grid) beside an existing
  shell Spec is not `local`: it is `component`.
- **Standout in a row of equals:** a row or grid of same-size cards usually wants one card that
  leads. Offer "Feature <the flagship, the newest or the biggest> as the lead tile (two columns wide, or
  above the grid)" as a choice, with "Keep them equal" beside it. Parallel items qualify. It is an
  option, never a rule, and nothing changes until the user picks it. The fix is routed `local` with
  `reuse: lead tile`: a class on the lead card and `grid-column: span 2` in the parent's own grid (a class
  on the field, never `:deep()`;
  [`delegated-render-control.md`](../boxel-ui-guidelines/references/delegated-render-control.md)), DOM order
  equal to reading order, the lead carrying the card's key fact, and the lead first on a phone.
- **A Bento** is a different fix, for items that really differ in kind, routed `local` with
  `reuse: layout-vocabulary -> Bento`. Quote its limits from `layout-vocabulary.md` → *2 · Bento*: 4 to 7
  items of genuinely different weight; a 4-column grid with the lead at `span 2` and row `span 2`;
  collapse by container query 4 → 2 → 1; drop `dense` if it reorders visible tiles; at most 3 distinct
  tile sizes; each tile its own `embedded` or `fitted` format.

**The fix ladder: no CSS hacks.** Go down a step only when the one above cannot reach: (1) theme tokens in
the app's Theme card, including the tokens of other tones (`success`, `destructive`, `info`, `warning`); (2) the
component's documented args and variables (`@tone`, `@appearance`, `@size`, `@shape`, `--pretui-button-h`,
`--fc-*` on `FittedCard`); (3) a class on the component root through `...attributes`, scoped to what the
args cannot reach; (4) `:deep()` last, with the gap named. Never `!important`, hard-coded colours or
sizes, `:global`, or a removed focus ring. Steps in full:
[`restyle-component.md`](../boxel-ui-component-discovery/references/restyle-component.md).

Route and reuse are separate. Every gap carries a `reuse:` field naming what the fix reuses: **one**
component with its Spec (an alternative may follow as a footnote), token names, the restyle-component
step, or `searched "<terms>": none fits`. If the search found something that fits, the route is not
`local`. A candidate whose fit is unknown is written `candidate: <name>, fit unchecked: <reason>`, and
does not change the route. Replacing a hand-built part with a catalog card is a proposal to the user
(or a `--redesign` option), not something a fix round does inside its three gaps.

```
G1 · Home price shows 1104000 unformatted · route: component · reuse: Pret UI MoneyInput (pretui-money-input)
G2 · Chart series are two similar greens · route: local · reuse: --chart-1, --chart-2, --chart-3
     candidate: Pret UI Chart, fit unchecked: this card draws a custom cumulative line chart
```

## Capture first: there is no review without it

You cannot judge a design from CSS. Capture before scoring, and stop if you cannot: a code-only
review reads as a real review and is not one. If some views cannot be captured, review the ones that
were and list the rest by name rather than blocking.

**Re-capture before reporting a fault that loading could cause**: a blank or stale image, an old
version of a screen, a control that looks disabled, a missing font. Report it only if the second
capture shows it too; one that does not is a capture fault, not the design's.

**A blank region in a capture is a finding.** A build's entrances never start from `opacity: 0` in
base CSS ([`template-patterns.md`](../boxel-ui-guidelines/references/template-patterns.md) →
*Entrance animations — never put `opacity: 0` in base CSS*), so a section left empty after loading is
a fault. A card still loading can paint one, so re-capture a blank region once, then report it.

Read `references/capture.md` for which tool captures which view, the capture budget, where
captures go, and the flakiness rules.

## Phase 1 — The direction gate (only when the brief has one)

When the brief card's `designDirection` field holds acceptance lines, it is the primary rubric.

1. Read its acceptance lines, its set acceptance lines, and its anti-patterns block. Each
   anti-pattern counts as an acceptance line.
2. Check each against the captures and the DOM. Tick or fail, with no partial credit and no commentary.
3. Report first, in this shape:

```
Design direction: <passed>/<total> acceptance lines
FAILED
- <screen> · <line verbatim> · <one-line evidence> · <capture file>
```

Every failed line carries the screenshot it failed on, not just words. **Any failure is an
ITERATE** regardless of the score below, and in set mode it iterates that screen alone, not the set.

**Do not re-judge what `## Design direction` already decided.** The layout direction, the interaction way and
the named style were chosen deliberately, with reasons recorded. Score how well they were executed.
If you think a decision itself was wrong, say so once, separately, as a note to the user, not as a
score.

With no acceptance lines, skip this phase and say the review ran without them.

## Phase 2 — The aesthetic gate

The bar is work that would be singled out, not work that is inoffensive. A result that is
professional, polished and forgettable sits around 6–7; the gate is **8.5**.

**Anchor the number to the field.** For a unit with an award-style category (portfolio, landing page,
product page, editorial), the benchmark in
[`references/benchmark-and-refine.md`](references/benchmark-and-refine.md) compares it with three recent
award winners, dimension by dimension. Compare composition and type, not WebGL or page-wide motion a
card cannot do. Without a benchmark (no `--benchmark` and not `refine`), say the scores are unanchored
and name no references.

Score and name the specific thing behind each number:

- **Typography** — does the pairing look chosen? When the build names a look from [`boxel-design/references/style-families.md`](../boxel-design/references/style-families.md), score against *its* check: editorial wants large-light against small-bold, playful and vibrant want a heavy display against a plain body, brutalist wants hard and heavy. Each look's row says which weights it wants; a Restrained editorial build set entirely between 500 and 600 with a small step fails. Is there tracking on uppercase micro-labels where the look uses them? With no named look, judge on role clarity.
- **Honest gaps are not unfinished.** A section left out, a role in place of a name, or a marked slot where the business's real review, price or rating will go is correct ([`boxel-design/references/critical-rules.md`](../boxel-design/references/critical-rules.md) → *Never invent proof*). Never score it down as incomplete. An invented rating, name, year or testimonial is a finding, unless the brief's `Real details:` line is `concept (demo mode)` and each one carries a visible "Sample" label.
  A **labelled placeholder image** is the same kind of gap: the build puts one where no photo may be
  used (a real person, the user's own product, a real film poster) or none could be found
  ([`sample-images.md`](../boxel-file-def/references/sample-images.md) → *Pick the source* and
  *Labelled placeholders*). Score that slot as if a fitting photo stood in it: its space, crop, shape
  and place in the composition. Never score the placeholder itself: not its colours, not its label,
  not that it is a box instead of a photo, and not how many of them there are.
- **Colour** — against the colour strategy the look uses. Restrained looks: one accent in at most two places. Playful, vibrant, vintage: several colours are right when each has a named role and none competes for the same job. Colours with no assigned role fail in any look.
- **Composition** — does something dominate, or is it a row of equals? When nothing does, name the move that
  would (Bento, unequal split, layered surface, a lead tile in a row of equals; *Gap routes*). Is the reading order legible
  in the screenshot alone? Can the main action be found without hunting for it? Name the signature
  treatment on the dominant object and say whether it belongs to this style;
  [`boxel-design/references/signature-treatments.md`](../boxel-design/references/signature-treatments.md)
  is the authority on which treatments a style earns and why the default gradient-and-glass look
  scores *lower* than a plain surface. Judge against it rather than restating it. Check the treatment
  survives into `embedded` and `fitted` as a compressed idea rather than a shrunken copy.
- **Media** — if the card has imagery, does it get real space, or hide under metadata? Check it
  **across formats, not just this screen**: `embedded` and `fitted` show a focused crop rather than a
  shrunken copy of the hero, and a card with an image never renders a text-only tile. A media slot (a
  poster, a listing photo, a dish, a profile photo) that ships as a gradient, a lone glyph or initials
  is a finding: the first build fills it, at least with a labelled placeholder, which passes this row
  (*Honest gaps*, above).
- **Detail** — the small touches that signal care, judged against the build's own look and brief:
  does each one read as chosen for this unit, and do two or three carry the whole page rather than
  every element being decorated? Name no treatment to add; a look that is plain by intent is not
  short of detail, and a treatment borrowed from another look is a finding, not a gap to fill.
- **Motion** — score it only when the build animates; a still page is not marked down for being
  still. Motion follows [`card-motion`](../card-motion/SKILL.md): the smallest pattern for the job,
  names scoped by card id, nothing missing with motion off. Spatial motion with character reads as
  designed; a fade on everything reads as unfinished. When the brief's `## Motion` records what the
  user asked for, check the build does it. When it moves with scroll, capture the start, middle and
  end as [`references/capture.md`](references/capture.md) → *Scroll motion* says: a single screenshot
  cannot show a sequence.
- **Emptiness and error** — do they invite and instruct, or apologise?

Below 8.5, name the two or three things standing between here and the bar. Those are the round's
gaps. Do not soften the number to be encouraging; the number is the useful part.

## Phase 3 — Look-level constraints

The basics (main action and controls, accessibility, affordance legibility and honesty, clarity, domain
fit, robustness) are not scored here: they are lines of
[`references/build-check.md`](references/build-check.md). Report a missed one once, as a note.

One constraint stays in review because it is taste:

- **Components take the app's look.** A Pret UI or boxel-ui component left at its library default
  (colour, radius, type) beside controls that carry the app's theme is a finding, scored under colour or
  coherence ([`restyle-component.md`](../boxel-ui-component-discovery/references/restyle-component.md)).
  So is a reused catalog card whose stock look still reads as another app; a stock layout kept under the
  theme because it fits is correct ([`restyle-reused-card.md`](../catalog-reuse/references/restyle-reused-card.md)).
  A component the build named as a gap that no restyle step reaches is reported as that gap, not scored
  down again.

Do not resolve a finding by making the design plainer. A contrast failure is solved by finding a colour
that reads *and* belongs, not by reverting to grey.

## Set mode

`design-review set <unit>` reviews the whole app.

1. Capture every screen in one pass, **plus every CardDef the screens link to, in each format the
   screens show it in** (`embedded` in lists, `fitted` in Home tiles): those render inside the
   screens, so they are set surfaces. This is the formats shown, not the full family (*Card mode*).
2. Tick the **set acceptance lines** from `## Design direction` across all captures, where it has
   them, then each screen's own.
3. Score coherence as its own dimension, looking across screens **and the linked cards' embedded
   and fitted views, which are part of the set**: one display face; the accent in the same role and nowhere
   else; one treatment for section labels, whatever it is; the same way for the same kind of action; one empty-state voice;
   consistent spacing rhythm between groups. A linked card that does not look like it belongs to
   the app it appears in is a set failure, not a card failure.
4. Report one table for the set, then per-screen failures. Iterate the failing screens only.

Run it early: once more screens stand on these, coherence problems get lived with instead of fixed.

## Card mode

`design-review card <CardDef>` scores one CardDef's `isolated`, `embedded` and `fitted` (every size
that will actually be used) as one family, plus `atom` and `edit` where the build wrote them. Atom is
optional and `edit` usually stays the host's default (design-playbook, Stage 4); a missing custom
one is not a gap. Run it for **every CardDef the app links to**, not only the ones that have
their own screen: a card reached through `linksToMany` is a surface the user sees, and it is the
surface that gets written in passing.

1. **Capture each format**, per `references/capture.md`: fitted inside the parent that renders it,
   at the sizes the app actually renders, not all sixteen. `atom` and `edit` need a browser from a
   terminal; in the app, list them as uncaptured.
2. **Tick the content matrix**, the design-playbook's Stage 0f block written at planning. It says
   which fields appear at each format, in what wording register, and what is omitted. Check the
   capture against it field by field. A format carrying fields the matrix omits is as much a failure
   as one missing them.
3. **Score the family, not each format.** The question is whether the formats read as the same card
   at different fidelities: same signature gesture, same accent role, same type family, wording compressing
   rather than truncating.
   - **Check the breakpoints fire.** Capture each format at a narrow width as well as a wide one.
     A `@container` rule that targets the element carrying `container-type` is dead and silent: the
     layout simply never changes. Two tells without reading CSS: the narrow capture is identical to
     the wide one, or a two-column layout overflows instead of stacking.
   - **Check `isolated` hardest.** It is often the one format that appears in no screen, so nothing
     in the build teaches it and nothing else reviews it. Two tells: `isolated` should be the
     *largest* of the formats (a full page thinner than its own thumbnail is nobody's decision), and no
     field should appear in `fitted` or `embedded` but be missing from `isolated`.
4. **Check the two failures this mode exists to catch:**
   - **The pedestrian fitted**: title in big type, description truncated, date in muted small
     text. It means the format is showing whatever fields existed rather than the ones that
     identify the card. Name the signature field it should be leading with.
   - **The data-empty embedded**: styled, bounded, and telling the reader nothing they could act
     on. An embedded card that omits the thing the user came for (the price, the name, the status)
     fails even if it looks composed.
5. **Check `prefersWideFormat` against what you captured**, and against the Width line in
   `## Design direction` when it has one. An isolated view that crops, collapses a grid to one
   column, or renders a wide layout in a narrow column is missing the static property. Report it as
   a finding with the capture.

Report as one block per card, then iterate the failing formats alone.

## Reviewing work in progress

A review run on a Stage 1 or 2 mockup, before the build is themed, sees deliberately hardcoded work:
real hex, named fonts, no `var(--*)`, one or two instances per CardDef. **Both are the correct state
at that point and neither is a finding.** Judge the layout on the content that is there; "needs more
rows to evaluate" is not a review. Do not report literal colours, a missing theme link or
untokenized values: tokenizing early pushes the build to fix values before the design is settled.
This applies only before theming. A review of finished work (*Scoring existing work*) never uses it.

What *is* fair game at every stage: everything visual, plus `border-radius`, `border`, `box-shadow`
or `overflow: hidden` on a format's outermost element, which the host owns
([`delegated-render-control.md`](../boxel-ui-guidelines/references/delegated-render-control.md)
→ *Per format — what's safe and what isn't on the outermost element*).

Structure is also fair game: the screens should already stand on real CardDefs with the domain's
real `linksTo`/`linksToMany`. A screen rendering from `containsMany` stand-ins will be rewritten
later, taking the layout with it; report that as a note, separately from the score.

**Pseudo-controls.** Anything the capture reads as a control (a button, a stepper, a picker, a
selectable cell, a tab) that is a `<div>` or an `<li>` with nothing wired under it. These pass every
reuse rule by accident: a build with no raw `<button>` and no component trips nothing. In a mockup,
name each one as a note. In a finished build they fail build-check line 8.

## Fix loop

A fix round runs only when the user picks it in the choice UI, and never chains into another. Each round
reports what it changed and what it left alone: a round that silently rewrites things nobody objected to
makes the next review meaningless.

**After reporting, ask what happens next in the choice UI**; do not just leave the report and wait.
Options: "Fix the top gaps" (recommended when it did not clear the gate), "Redesign from existing parts"
(when step 7 of *Scoring existing work* says so), "Review the next screen / run `set` or `card`"
(recommended once this unit passes and others remain), "Revisit a decision in the brief" (when a failure
traces to the decision itself, not its execution; see Phase 1), and "Stop here" (recommended once
everything in scope has passed), plus room for the user to name something else. Stopping is always one of
the options, never a line asking the user to type "skip".

**After a scoped run** (`--layout`, `--typo`, `--colour`, `--coherence`), the choice is about the
dimension asked for and nothing else:

- **A gap was found:** offer "Fix <gap> → <its reuse>" for each gap in that dimension only, never a
  gap from another one. The reuse comes from the *Search before you route* search, judged against the
  brief's `Surface:` line and the app's direction, not from a generic default. For example, `--layout`
  on a back-office app with no sidebar finds the gap "no app shell"; the search runs for "app shell" and
  "sidebar", and the option reads "Fix: add a fixed sidebar → Pret UI app shell" (or the catalog Spec
  that fits), with the app's real destinations as its items. A fix that is only a token or a class says
  so. For a row of equals, the option reads "Fix: feature <the flagship or newest> as the lead tile
  (two columns wide, or above the grid)", and "Keep them equal" is listed as its own option right after it. Add "Review another dimension" and "Stop here". Give them as a list (the choice UI, or lettered
  options in chat), never as one prose line.
- **Nothing was found:** say it passed in one line, suggest no fix and run no search, and ask only
  "Review another dimension (<the ones not run>)" / "Stop here". A scoped pass says nothing about the
  dimensions it did not look at, so name them.
- A fix round from this choice touches only that dimension, then re-scores it, and never chains.

## Output

`--score` prints only the score lines of what follows (the *Scorecard* table, the *Aesthetic* and *Design
direction* tallies, the verdict) and drops the rest.

A full review opens with the scorecard and the changelog, one row and one line per round. Round 0 is the
first review. A scoped run prints one score per requested dimension and no total, and says the gate was
not assessed.

```
Basics: 14/14 build-check lines pass

Scorecard
| Round | Direction | Aesthetic | Reviewer |
|---|---|---|---|
| 0 | 9/11 | 7.5 | independent |
| 1 | 11/11 | 8.0 | independent |

Changelog
- R1 · G1 Names cut off in fitted tiles (one template) · route: local · reuse: searched "tile title": none fits · title wraps to two lines · landed
- R1 · G2 Accent on prices · route: local · reuse: --foreground · prices in ink colour · landed
- R1 · G3 Hero and grid at equal weight · route: local · reuse: lead tile · ambassador tile double width · partial: the phone view stacks it back
Left alone: everything else.

Design direction: 11/11 acceptance lines

Aesthetic: 8.0/10 — gate is 8.5
- Composition: the double-width tile leads at desktop only

Verdict: ITERATE
The one thing between here and the bar: one tile that dominates at phone width too.
```

*Basics* is the build check's tally when the review ran (for existing work, the first look). *Reviewer* says
`independent` or `provisional`. Gap ids (G1, G2, …) stay the same across rounds, so a gap that comes back is
visible, and each names its route (*Gap routes*). A changelog line is round · gap · what changed · landed,
partial or made worse.

## Pair with

Read these live on each run. Links are relative to this skill's folder.

| What | Where |
|---|---|
| The decision being scored | the brief card's `spec`, and its `## Design direction` when it carries acceptance lines |
| Which treatments a style earns | `boxel-design/references/signature-treatments.md` |
| Anti-cliché checklist, proof and clickable controls | `boxel-design/references/critical-rules.md` |
| What each format's root may and may not style | `boxel-ui-guidelines/references/delegated-render-control.md` → *Per format — what's safe and what isn't on the outermost element* |
| Fitted sizes and the verification checklist | `boxel/references/fitted-formats.md` |
| The per-format content matrix a card is scored against | `boxel/references/design-playbook.md`, the Stage 0f `## <CardName> · content matrix` block |
| How a build animates, when it does | `card-motion` |
| Whether an isolated view needed the full viewport | `boxel/references/prefers-wide-format.md` |
| Restyling a reused card or a component | `catalog-reuse/references/restyle-reused-card.md`, `boxel-ui-component-discovery/references/restyle-component.md` |
| Required before fixing a `catalog` gap | `catalog-reuse` |
| Required before fixing a `component` gap | `boxel-ui-component-discovery` |

## Don't use for

- Deciding the look before anything is built: that is `boxel-design` (the index's "Just build it" path).
- Checking code on its own: lint and the correctness check are `boxel` (`boxel/references/lint-workflow.md`); this skill scores captures.
- Auditing or patching a Theme card: that is `boxel-theme-development`.

## Sections (load on demand)

- `references/build-check.md` — the pass/fail check that finishes every design build (the basics, unscored), and the *Basics* block for existing work
- `references/capture.md` — which tool captures which view, budgets, where captures go, and the blank-region, scroll-motion and motion-off rules
- `references/benchmark-and-refine.md` — the award-site benchmark, `refine` mode and the roles in the loop (the gate stays 8.5)
