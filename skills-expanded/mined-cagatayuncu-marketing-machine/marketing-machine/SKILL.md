---
name: marketing-machine
description: Own the whole marketing content pipeline for this codebase — set itself up, scan the product for what actually works, write the copy, enforce the rules mechanically, and render cards (PNG) and video (MP4) from one HTML contract. Use for "set up marketing", "write a post", "review this copy", "make a card for this", "render a video", "scan the product", or "do the whole thing".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# marketing-machine

Argument: `$ARGUMENTS` — what to do. Examples:
`setup` · `write post about inventory turnover` · `review marketing/posts/12-report.md` ·
`card 12` · `video intro` · `scan` · `everything`

This skill owns the pipeline end to end. Nobody should need to read a README or run a script by
hand: if something is missing, set it up; if a command fails, read its error and act on it.

Toolchain path: `<TOOLCHAIN>`. If that still reads as a placeholder (angle brackets intact), this
skill arrived without `init` having run — resolve the path yourself, first match wins:

1. `$CLAUDE_PLUGIN_ROOT` is set in your environment → that directory IS the toolchain (plugin
   install; scripts, rules and templates travel with it).
2. A `TOOLCHAIN` file sits next to this SKILL.md → its single line is the path.
3. Neither → the toolchain is not on this machine yet. Clone it, then continue:
   `git clone https://github.com/cagatayuncu/marketing-machine ../marketing-machine` and use `../marketing-machine`.

Every command below runs from the host repo root.

## The chain

```
setup ──▶ scan ──▶ (human confirms facts) ──▶ write ──▶ visual / video ──▶ lint ──▶ report
  │                                                                          ▲
  └── config, fonts, brand roles, CI gate                    every output goes through here
```

Asked to do "everything", walk the whole chain and stop at the two points that genuinely need a
human: confirming which product facts are true, and deciding which claims are defensible. Never
invent an answer to either.

## 0 · Orient

**First, check whether the machine is installed:** is there a `marketing.config.json` at the repo
root?

- **No** → go to §1 SETUP. Do not try anything else first; every other command needs the config.
- **Yes** → run doctor, then load context:

```bash
node <TOOLCHAIN>/scripts/doctor.mjs
```

If doctor reports a failure, **fix it** (§1.3 covers the two common ones). Do not proceed with a red
doctor: a missing font or an unmapped brand role produces output that looks fine and is wrong.

Doctor also reports whether this machinery is current — `skill copy` (does the installed skill
still match the toolchain that drives it) and `toolchain version` (is the toolchain behind its
upstream repository). Neither blocks work, but do not swallow them: tell the user in one line and
name the fix — `init --refresh` for a stale copy; `git pull` in the toolchain (or the plugin
marketplace update) for an old version, then `init --refresh`. If the user says update, update
first: producing content with yesterday's rules and then re-doing it is the expensive order.
Offline is fine — an unreachable upstream reads as unknown, not as a problem to fix.

Then read `marketing.config.json` and these three files **in full** (do not skim):

1. `<paths.context>/product-facts.md` — what actually works. **The single arbiter.**
2. `<paths.context>/claims.md` — which claims are usable
3. `<paths.context>/brand-voice.md` — tone, bans, word preferences

Read at least two already-published pieces from `<paths.posts>` to calibrate the voice. If there are
none yet, say so — the first piece has no reference and needs closer review.

---

## 1 · SETUP — `setup`

### 1.1 Install

Pick the agent target from what the repo already uses: `.claude/` present → `claude`,
`.cursor/` → `cursor`, `AGENTS.md` → `agents`. If several or none, ask.

```bash
node <TOOLCHAIN>/scripts/init.mjs --agent <target>
```

Read the output carefully and **relay it**: it lists what was derived from the codebase and what
could not be. That report is the only place naming the fields still needing a human.

### 1.2 Interview

`init` reports what it derived. Now ask about what a codebase cannot know. Ask these as one short
conversation, not one question at a time, and write the answers where they belong.

**Content language.** `init` infers one from the locale files, but **the product's interface
languages and the marketing language are different decisions.** A product whose UI ships in three
languages may market in one; a product with no localisation at all still markets in something. Ask
which language the copy will be written in, and if the product ships several, ask whether marketing
follows all of them or starts with one.

If the answer differs from what was inferred:

```bash
node <TOOLCHAIN>/scripts/init.mjs --refresh --lang <code>
```

That re-derives the language-dependent pieces — the rule pack, the verification-table heading, the
verify marker — while keeping paths, channels and anything already tuned. Do not hand-edit
`language.primary` on its own; the rule pack and the in-content headings move with it.

If there is no rule pack for that language yet, say so plainly: only the structural rules will be
enforced, the vocabulary bans will not, and someone has to write `rules/lang.<code>.json` for that
half to exist.

**Channel.** Which surface is this for — a social feed, a blog, email, a landing page? It sets the
card and video geometry, and it decides the post anatomy. Do not set up channels nobody asked for;
`config.channels` ships three geometries and one of them is usually enough to start.

**Audience.** Fill `<paths.context>/audience.md` from the answers: who they are, the words *they* use
for the problem, what they already tried, the first objection, and who this is explicitly not for.
That last one matters — without it the copy drifts vague.

**Product.** `product.oneLiner` in the user's own words, and `product.stage`. Do not write the
one-liner for them off the README; positioning is a judgment. `brand.footerUrl` if no domain was
detected.

Leave any `[VERIFY]` marker you cannot resolve in place and report it. A marker is better than a
guess.

### 1.3 Get doctor to green

**Fonts.** If doctor cannot resolve a font package, its error names the exact command. Run it **in
the toolchain directory, not the host repo** — the fonts belong to the renderer:

```bash
cd <TOOLCHAIN> && npm i <package>
```

Save it rather than using `--no-save`: npm prunes unsaved packages on the next install, so a
second font would silently delete the first.

If the family is not on a font CDN (a licensed or custom typeface), ask the user for the `.woff2`
files and set `config.fonts.<role>.files` to those paths instead of `package`.

**Brand roles.** If any of the six roles is unmapped, open the stylesheet named in
`config.brand.colorsSource`, read the palette, and **propose a mapping** with your reasoning
(`bg` ← the darkest surface, `accent` ← the interactive/primary color, and so on). Get agreement,
then write it into `config.brand.roles`. Cards refuse to render until all six resolve, which is
deliberate: wrong-brand artwork is worse than no artwork.

Even when all six auto-resolve, **show the mapping and ask for a sanity check.** It is guessed from
names and can be confidently wrong.

**ffmpeg** is only needed for video. Leave it until someone actually wants an MP4.

Re-run doctor until it prints `Ready.`

### 1.4 Offer the CI gate

The rules are advisory until something runs them. Once doctor is green, offer to wire the gate:

```bash
node <TOOLCHAIN>/scripts/lint.mjs --warnings-as-errors
```

If the repo uses GitHub Actions, offer to add a workflow that runs it on changes under the
`config.paths` directories. Ask before writing to `.github/` — that is their build.

---

## 2 · SCAN — `scan`

```bash
node <TOOLCHAIN>/scripts/scan.mjs
```

Output lands in `<paths.factsDraft>` as a **draft**. Every line sits under the verify marker with a
`file:line` reference.

**You do not move the draft into `product-facts.md` yourself.** A scanner sees that a symbol exists;
it cannot see that the feature works end to end. What you do:

1. Read the draft.
2. Present it section by section, in the draft's order.
3. For each candidate ask: "does this work end to end, and what is the evidence?"
4. Move only what the user confirms into `product-facts.md` under **WORKS**. Everything else goes to
   **PARTIAL** or **ABSENT**, with the reason.

Spend the most time on section 1, the outbound-call inventory. If any claim about where data goes is
planned, **every row there** has to be reviewed. One unreviewed call falsifies an absolute claim.

Then help fill `claims.md`. For each candidate claim: is it provable, and by what? The UNPROVABLE
rows are the valuable ones — write them as rules in `config.lint.projectRules` so the build enforces
them. A claim recorded only in `claims.md` is advice, and advice gets missed.

---

### Drift — approved copy does not stay approved by itself

The linter re-resolves every `file:line` in the facts file and in post verification tables on
every run: a cited file that is gone is a **violation**, a backticked evidence excerpt that no
longer appears in the file is a **warning**, an excerpt that merely moved lines is a **note**
carrying the new line number. What that means for you:

- When promoting rows from the draft, keep the backticked evidence excerpt next to the ref — a
  row with only `file:line` gets existence checking and nothing deeper. Refs are recognised when
  the path carries a directory (`src/app.js:7`); a bare root filename (`package.json:5`) is the
  linter's accepted blind spot, so re-check those rows yourself when the scan walk revisits them.
- A moved-line note is mechanical: apply the suggested line number, say what you did, move on.
- A gone/missing finding is NOT mechanical: re-walk that row with the human exactly like the
  original scan walk. Renamed feature → update ref and excerpt. Removed feature → retire the
  fact AND every post sentence that leans on it. Nothing gets re-approved silently.

---

## 3 · WRITE — `write <channel> <topic>`

**Everything in the copy comes from this repository.** Not from what products in this category
usually claim, not from the README's own marketing language, not from what would sound good. The
chain is: the scan found it in the code → a human confirmed it → it is WORKS in `product-facts.md` →
it may appear in a sentence → the sentence carries its `file:line` in the verification table.

If you want to write something and cannot trace it back through that chain, you have two honest
options: leave a verify marker and ask, or leave it out. Reaching for generic category copy is how a
tool like this becomes worthless.

### Settle the topic
Which audience, which angle, which call-to-action level? Decide, and record it in the post's header
block. If the user keeps a "will not write" list, respect it: say why and stop.

### Write
Anatomy: hook → enlarge the problem → turn → evidence → **limitation sentence** → one question.

- The product name does not appear in the first two lines.
- No em dash inside a sentence. Split the sentence.
- **The limitation sentence is not optional.** Copy that only says good things is not believed.
- Use unicode bold only on digits and on words with no language-specific letters.
- Where you are unsure of a fact, leave the verify marker with a reason. Do not invent.

### Terminology — the product's words, not the dictionary's

When the copy language is not English, technical terms are a decision, not a translation. A
literal dictionary rendering of a domain term ("tenant" → the residential word for a renter)
reads as machine output and burns trust in one line.

1. **The product's own locale strings are the authority.** Before writing, look the term up in
   the product's i18n files (`config.scan.i18nLocales`). Whatever the product shows its users is
   what the post says — even when that is the untranslated English term.
2. **No product translation → industry form wins.** If the product has not translated the term,
   keep the form practitioners actually use in that language (often the English term as-is).
   Never coin a literal translation for marketing that the product itself does not use.
3. **Record the decision.** Keep a `## Glossary` table in `<paths.context>/brand-voice.md`
   (term → what we write → why). Check it before writing; extend it when a new term is settled.
4. **Make repeat offenses mechanical.** A form that must never appear again goes into
   `marketing/rules/project.json` as a rule, so the linter fails the build instead of you
   remembering.

### Save
`<paths.posts>/NN-slug.md`. Template:

```markdown
# Post NN — <title>

**Pattern:** <one sentence describing the structure>
**Audience:** <who>
**CTA:** <level>
**Lang:** <code — the language THIS post is written in>
**Visual:** <file, or "none" + reason>
**Alt text:** <what the card conveys>

---

<the copy>

---

## Verification notes

| Claim | Source |
|---|---|
| ... | file:line |
```

**The verification table is mandatory.** Every number in the body must appear in it; the linter
checks this and fails the build when it does not.

### Lint (not optional)
```bash
node <TOOLCHAIN>/scripts/lint.mjs <file>
```

A `VIOLATION` blocks publication. **Fix it and run again.** Tell the user briefly what you changed.
Weigh `WARNING` and `NOTE` items with judgment: some are deliberate choices, and when they are,
record the reason in the post's header block.

Vocabulary rules are chosen per FILE, from the post's `**Lang:**` header (or a `name.<code>.md`
suffix). In a repo publishing in more than one language, write that header on every post — without
it each file is checked against every loaded language pack at once, and you get one guaranteed
false warning per post per foreign pack.

What the linter **cannot** see, and you must: whether the limitation sentence is any good, whether
each claim maps to a WORKS fact, audience coherence, hook strength.

---

## 4 · VISUAL — `card <post>`

### Decision table — first match wins

| What the post contains | Format | Why |
|---|---|---|
| Something visible in the product UI **and full enough to carry the frame** | **Screenshot** | A real screen beats a drawing. Do not build a card; ask for the screen. |
| A step-by-step flow or process | **Flow card** | Order reads at a glance |
| Two states compared (before/after, right/wrong) | **Comparison card** | Contrast is what a visual does best |
| A measurement, ratio or headline number | **Number card** | A number disappears in prose and holds in a card |
| A numbered teaching list | **List card** | Raises saves |
| The product's **motion** is the point | **Video** | Motion cannot be described, only shown |
| Several sequential ideas that each deserve a frame | **Carousel** (PDF) | LinkedIn document posts hold attention per-swipe |
| A confession, an opinion, an engineering diary, a conceptual argument | **NO VISUAL** | Text posts work better in this column |

**The default is no visual.** Do not make decorative cards; an empty card weakens the post.

**The trap in the screenshot row:** copy happening inside the product UI does not by itself earn a
screenshot. The test is whether that one screen element can carry the whole frame alone. A full
panel can; a single-line warning strip cannot. If it cannot, fall back to the structure in the
post's spine (flow, comparison, number).

State the decision in one sentence with its reason, then proceed.

### Build the card
Copy `<paths.cards>/_template-card.html`, keep the `<section>` matching the archetype, delete the
rest, fill the slots.

Invariants:
- **Leave `<!--FONTS-->` and `<!--TOKENS-->` in place.** Colors and fonts come from config; never
  write a hex value or a font name into the card.
- Identity text uses placeholders: `{{brand.wordmark.text}}`, `{{brand.footerUrl}}`. A placeholder
  with no value behind it fails the render.
- **Logo:** when `config.brand.logo` is set, the header shows the logo image, not the text
  wordmark: `<img src="{{brand.logoData}}" style="height:40px" alt="" />` — the renderer inlines
  the file. Set the height only and let width follow; never stretch or recolor it. No
  `brand.logo` in config → text wordmark, and do not use `{{brand.logoData}}` at all.
- At most `config.lint.cardMaxWords` words. A card is one idea, not a summary of the post.
- The card does not repeat the copy; it completes it.

Layout discipline — a card that renders is not yet a card that reads:
- **Normal flow only.** No absolute positioning for text, no negative margins, no fixed pixel
  heights on text containers — that is exactly how list numbers end up printed over the headline.
  Space with flex/grid and `gap`; let every box grow with its content.
- **Reserve wrap room.** Any headline may take one line more than you expect, in any language.
  Nothing below it may depend on where it happens to end.
- A list marker and its text share one flex row (`align-items: center`); rows never share
  coordinates with anything else.
- Between distinct blocks (headline / list / footer) leave at least one line-height of air. A
  crowded card reads as broken even when nothing technically overlaps.

Not the same card twice:
- Before building, open the last two or three files in `<paths.cards>` (and `<paths.scenes>` for
  video). If this one would repeat the same skeleton — same archetype, same alignment, same scale
  rhythm — change the composition deliberately: flip the alignment, trade the list for a grid,
  let the number dominate the frame, move the emphasis elsewhere. Brand stays fixed (roles,
  fonts, wordmark); composition must not fossilise into one layout wearing different words.

```bash
node <TOOLCHAIN>/scripts/render-card.mjs <name>
node <TOOLCHAIN>/scripts/lint.mjs --only card
```

If the render fails, read the error and act on it — it names the cause and the fix. Pass anything you
cannot resolve through **verbatim**; do not paper over it.

### Carousel, languages, themes

- **Carousel:** author `<name>.slide1.html` ... `<name>.slideN.html` (each an ordinary card,
  same invariants, ONE shared geometry), then `carousel <name>` binds them into
  `<paths.out>/<name>.pdf`. Slide 1 must stand alone — the feed shows it before any swipe. One
  idea per slide; the last slide carries the wordmark and the URL.
  Slides live in `paths.cards` like any other card; `carousel <name> --png` also writes each slide
  as a PNG, which is how you do the look-at-it pass below on a document.
- **Languages:** put translatable copy into `<name>.copy.json` (`{ "langs": { "en": {...},
  "tr": {...} } }`) and reference it as `{{copy.<key>}}` in the card. `card <name>` renders every
  language; terminology follows the Glossary exactly as in posts. Layout QA applies PER LANGUAGE
  — text lengths differ.
  A carousel reads the same decks: `<name>.copy.json` covers every slide of `<name>`, a
  `<name>.slideN.copy.json` overrides it for one slide, and the output becomes `<name>.<lang>.pdf`.
  Every slide that declares languages must declare the SAME ones, or the run refuses by name.
- **Themes:** when `config.brand.themes` exists, `card <name> --theme all` renders every role
  set. A theme is a full set of six roles; never hand-build a "light version" by editing colors
  into the HTML.
- **Live capture (`record`):** a `<name>.drive.json` drives the REAL product and records it —
  provenance is `driven-app` by definition and the file refuses anything else. Prefer it over a
  simulation whenever the product can actually be driven; never present either as a screen
  recording.
- **Claims registry:** when `config.paths.claims` exists, cite `claim:<id>` in verification
  tables instead of repeating file:line. Retiring a claim in the registry flags every post that
  cites it (and `paths.published` adds the live URL to the finding). Keep the registry the
  single place a claim's status changes.
- **Metrics journal:** after a post has real numbers, add `**Metrics:** impressions=N
  reactions=N comments=N` to its header. `report` aggregates by pattern — read it before
  choosing the next post's angle; it describes, you judge.

### Look at what you rendered (not optional)

Open the PNG and inspect it before showing it to anyone. The renderer checks values — fonts,
roles, placeholders — not composition; overlap is invisible to it. Check, in order: nothing
overlaps anything, nothing clips at a canvas edge, no text is truncated mid-word, every block has
the air the layout rules demand, and the logo (if any) is sharp and unstretched. If any check
fails, fix the HTML and render again. A card ships only after this pass — in every language it
ships in, since text length changes the layout.

For a carousel, render the slides with `carousel <name> --png` and inspect those. The PDF is the
deliverable, not the review surface: it is not something you can open and look at.

### Alt text (not optional)
Do not copy the words on the card; write **what the card conveys**. Someone using a screen reader
should get the same information without seeing it.

- Bad: "Product card. No more queueing for a report."
- Good: "Four-step flow: ask in plain language, see the query, get the result, add it to the
  dashboard. Below: the query runs on your own machine."

### Update the post file
Fill in `**Visual:**` and `**Alt text:**`. If the decision was no visual, write the reason.

---

## 5 · VIDEO — `video <scene>`

Full contract: [references/video-guide.md](references/video-guide.md). In short:

Video comes from HTML too, through the **same** pipeline as a card. The only difference is that a
scene declares a timeline.

```bash
node <TOOLCHAIN>/scripts/record.mjs <name> --shot 6.5   # one frame — check this first
node <TOOLCHAIN>/scripts/record.mjs <name>              # the MP4
```

Always check a frame before rendering 450 of them.

**Three rules when writing a scene, none negotiable:**

1. Every visual is a **pure function of `t`**. No CSS `transition`/`animation`/`@keyframes`, no
   `setTimeout`/`requestAnimationFrame` driving visuals, no state accumulating across `__seek`
   calls.
2. Use a **fixed rate, not a fixed duration** (typing, scrolling). Longer copy in another language
   must not look pasted in.
3. On-screen strings must match the product's **real strings** exactly. Copy them from the product's
   own i18n source; do not retype. A missing key should fail the build rather than leave a hole in
   the video.

**Provenance is mandatory.** With `config.provenance.required` on, every scene must declare:

```js
window.__provenance = 'simulation';   // real-recording | driven-app | simulation
```

A code-reconstructed interface **is not a screen recording** and must never be shared as one. Record
this in the post file too. The linter reads the declaration out of the scene, so omitting a file does
not get you past it.

**When it is not enough:** if the post's argument rests on evidence ("don't believe me, look"), a
real recording is always stronger. Produce the clip so the post is not blocked, but leave the real
recording on the table and say so.

---

## 6 · REVIEW — `review <file>`

For copy that came from somewhere else.

```bash
node <TOOLCHAIN>/scripts/lint.mjs <file>
```

That is the mechanical part. Add these passes yourself; the linter cannot see them:

1. **Claim verification.** Pull out every capability sentence. Is it WORKS in `product-facts.md`? If
   not, that is a violation. If PARTIAL, does it need framing?
2. **Limitation quality.** Present, and does it state a real limit rather than decoration?
3. **Audience and tone.** Written to one audience? If it is reaching for two, which one wins? Any
   blaming tone?
4. **CTA fit.** Right level for this kind of post? Is the product even in a state to support it?

Report in this severity order: **VIOLATION** (cannot publish) → **WARNING** (publishable but weaker)
→ **SUGGESTION** (optional).

Then give the corrected copy in full. **Fix only violations**; do not rewrite the author's voice or
structure. Do not try to make someone else's copy "better".

Do not modify the file unless asked — a report is often enough.

---

## Invariants

1. **Nothing may be claimed unless it is WORKS in `product-facts.md`.**
2. **Nothing from the UNPROVABLE section of `claims.md` enters the copy.** Softened versions
   included.
3. **Keep legal-compliance claims separate from technical facts.** "Compliant with X" is a legal
   claim, and buying software makes nobody compliant. State the verifiable fact instead.
4. **No absolute claims.** "X never happens" cannot be proven. Write conditionally and measurably.
5. **No unmeasured numbers.** Duration, efficiency and savings claims need a source.
6. **Leave a verify marker where you are unsure.** A gap beats an invention.
7. **Run the linter after every output.** Copy, cards and scenes go through the same rules.
8. **Do not write to product source.** Product code is read-only; all output goes under
   `config.paths`. The one exception is the agent-skill and CI files that setup installs, and only
   with the user's agreement.
9. **Never commit without the user's approval.**

## Report back

At the end, state: file paths, the chosen format and why, the linter result (how many violations,
what you fixed), the artwork produced and its dimensions, the alt text, and any verify markers still
open.

When setup ran, add: what was derived from the codebase, the interview answers (content language,
channel, audience) and where you recorded them, the brand-role mapping used, and whether the CI gate
is in place.
