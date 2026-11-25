---
name: durable-product-playbook
description: >-
  Use when establishing practices that keep a real software product coherent, honest, and
  maintainable across many sessions with an AI coding partner — especially solo/small-team
  builders whose project is starting to drift, contradict itself, or overpromise. Reach for it
  when the user wants a project manual / CLAUDE.md / contributor guide, sets working conventions,
  needs docs and code kept in sync, worries an AI assistant keeps losing context between sessions,
  is defining what the product must refuse to do (or how to handle requests that cross that line
  without caving), is tempted to overpromise (claim an "edge", inflate unproven results), wants
  a Definition of Done, deploy runbook, or design-system rules that survive context loss, or asks
  how to make months-long AI-assisted development sustainable. Don't wait for the word
  "playbook". It's about durable practice, not one-off tasks — skip it for a single deploy
  script, summarizing a file, API docs for a few endpoints, fixing one test, or a throwaway
  prototype.
---

# Durable Product Playbook

How one person (or a small team) plus an AI coding partner can grow an idea into a product that
stays **coherent, honest, and maintainable** across hundreds of sessions — instead of decaying
into a heap of contradictory one-off changes that no one, human or AI, can hold in their head.

This is a **flexible** skill: principles to adapt, not a rigid checklist to obey. The audience is
the AI partner doing the building — but everything here is meant to be set up *with* the human and
owned by both.

## Why this exists

An AI partner is brilliant per-session and amnesiac across sessions. Each new session starts blind:
it can't see last week's reasoning, the dead ends you already ruled out, or the line you swore never
to cross. Left alone, this produces **drift** — the product slowly contradicts itself, re-litigates
settled decisions, repeats failed experiments, and quietly overpromises because no single session
remembers the promise you made to your users.

The fix is not a smarter model. It is **infrastructure that survives context loss**: a living manual
the AI reads first, a memory of hard-won truths, a definition of "done" with automated guards, and a
product spine of boundaries that no session is allowed to bend. Build that scaffolding once and every
future session inherits your standards instead of guessing at them.

The playbook has six parts. A-B-D are *how you work*. C is *what you refuse to compromise*. E-F keep
the surface and the collaboration itself from rotting.

- **A. Collaboration infrastructure** — the artifacts that make an amnesiac partner effective.
- **B. Definition of Done + drift guards** — how "finished" stays finished.
- **C. Product discipline** — honesty over hype; the soul of a tool people trust.
- **D. Execution patterns** — how features actually get built and shipped.
- **E. Design-system consistency** — one surface, not fifty hand-rolled ones.
- **F. Working with the AI partner** — meta-habits that compound.

Read the part you need. The reference files hold copy-paste templates — pull them in only when
you're actually setting that piece up.

---

## A. Collaboration infrastructure

The single highest-leverage move in AI-assisted development is writing down what the AI must know
*before it touches anything* — and keeping that writing true.

### A1. Make the project manual the AI's first read

Most projects have a README aimed at users. You also need a manual aimed at **the AI doing the work**.
Not "what this product is" — but "the rules, the conventions, the map, and the traps." Put the
non-negotiable boundaries (Part C) at the very top so no session can miss them.

A good manual answers, in order:
- **Red lines** — what this product must never do, stated as absolutes (see Part C).
- **Conventions** — the decisions already made (naming, colors, layout idioms, commit style) so the
  AI matches the house style instead of inventing a new one each session.
- **Code map** — "want to change X? touch these files." This is the difference between a session that
  edits the right three files and one that flails through the repo re-deriving the architecture.
- **Known traps** — the non-obvious gotchas that have already bitten you (a stale proxy env var, a
  data source that publishes late, a deploy window you must avoid). Each trap written down is a future
  session saved from rediscovering it the hard way.

Keep it **current**. A manual that lies is worse than none — the AI will confidently follow a stale
rule. Updating the manual is part of finishing work, not a separate chore (see Part B).

> Template: `references/claude-md-template.md`

### A2. Add a navigation table so onboarding takes minutes

At the top of the manual, a tiny "looking for X? go here" table. New session, new contributor, future
you at 2am — all oriented in under a minute. It costs five lines and saves the same fifteen-minute
re-exploration every single session.

```
| Looking for...            | Go to                         |
| Capabilities overview     | README.md                     |
| 30-min onboarding         | docs/ONBOARDING.md            |
| Domain jargon             | docs/GLOSSARY.md              |
| Architecture / data flow  | docs/architecture.md          |
| Progress & TODO           | docs/ROADMAP.md               |
```

### A3. Use memory for truths the code can't show

Some of the most valuable facts are **invisible in the code**: that you tried approach X and it failed
(and why), that a rule exists because of a specific past incident, that a metric looks promising but
doesn't survive validation. Code shows *what is*; memory preserves *what you learned and decided*.

Write these down as durable notes — one fact per note, with the **why**. The payoff is enormous:

- **No repeated dead ends.** "We already tried the aggressive variant; it backtested worse" stops the
  AI from cheerfully rebuilding it next month.
- **No re-litigating settled calls.** A decision with its rationale recorded is a decision that stays
  made.
- **Negative results become assets.** "This doesn't work, here's the evidence" is often more valuable
  than another feature — record it with the same care.

Treat memory and the manual as a pair: the manual holds *standing rules*, memory holds *the evidence
and history behind them*. Cross-link them.

### A4. Turn repeated workflows into commands

Anything you explain more than twice — onboarding, the test routine, the deploy sequence, a
"summarize where we are" recap — should become a named command (a slash command, a script, a make
target). Encoding the workflow once means every future run is consistent and you stop paying the
re-explanation tax. Good candidates: `onboard`, `test`, `deploy` (with preflight checks), `recap`,
`summary`, and project-specific scaffolds ("add a new <thing>").

---

## B. Definition of Done + drift guards

A change isn't done when the code works. It's done when the project is **still coherent** after the
change. Make that explicit, and automate the parts a machine can check.

### B1. Write an explicit Definition of Done

State what "finished" means and make every session self-check against it before wrapping up. A
typical bar:

1. **Code + tests** — new behavior has tests; the suite is green; if the UI changed, it builds.
2. **Docs follow the code** — added a scheduled job / data table / API / command? The docs that list
   those are updated in the same change.
3. **Roadmap updated** — finished a unit of work? Tick it off, bump the milestone, adjust the TODO.
4. **Commit cleanly** — message in the house style, with whatever attribution convention you use.

The point isn't ceremony. It's that **half-done work is invisible later** — a feature with no test, a
table with no doc entry, a finished task still marked open. Each of those is a small lie the next
session will trip over.

> Full template: `references/definition-of-done.md`

### B2. Separate machine-checkable facts from judgment, and automate the first kind

Some "done" criteria are mechanical: does every scheduled job appear in the schedule doc? Does every
API route appear in the API doc? Does every data table have a doc entry? **These you can verify with a
script** — a "docs doctor" that diffs reality against the docs and flags drift. Run it at the end of
every change; wire it into a pre-commit hook that *reminds* (don't make it block — a guard that blocks
on a false positive teaches people to bypass it).

Other criteria need judgment: is the roadmap honestly updated? Is this feature actually good? Those
stay human/AI discipline — but at least you've shrunk the surface that relies on vigilance.

> Drift-guard setup (docs-doctor concept + pre-commit hook): `references/definition-of-done.md`

### B3. Periodic self-audit

Drift accumulates slowly. A recurring "summarize what changed, what's the current state, where did
docs drift, what's next" pass catches the slow leaks before they compound. Make it a command (A4) so
it actually happens.

---

## C. Product discipline — honesty over hype

This is the soul of the playbook. Tools people *trust* are built by teams that decided, up front, what
they would never do — and held the line even when a feature request, or the AI's own helpfulness,
pushed against it.

### C1. Define the boundary first, and make it immutable

Before features, write down **what the product refuses to do**. State it as an absolute and put it at
the top of the manual where no session can miss it.

> Example (a market-observation tool): *"Only observe and notify. Never emit buy/sell signals, never
> place orders, never claim an edge. The decision belongs to the user."*

The boundary is what makes the product honest. It's also what makes it *designable* — a clear "no"
turns a thousand fuzzy feature debates into a single test: does this cross the line?

### C2. Reframe requests into the boundary — don't bend the boundary

Users (and the AI eager to please) will ask for things just past the line. The skill is to find the
**honest version** that delivers the underlying value without crossing it — not to quietly relax the
rule.

> Example: a user asks for *"predict tomorrow's winners."* Prediction crosses the line (it implies a
> signal/edge). The honest reframe: *show the observable structure* — what's actually happening now,
> ranked and explained — and let the user draw conclusions. Same value (insight), boundary intact.

When you reframe, say so plainly: "X would cross our line because…; here's Y, which gives you the same
thing honestly." That transparency is itself trust-building.

### C3. Quality gate over output volume — "an honest blank beats a padded page"

Set the bar for what's worth showing, and hold it even when that means showing *nothing*. Zero honest
results is a feature, not a failure — it means the filter works. The failure mode is loosening the
rule to fill space, which trains users to distrust everything you show.

When you return little or nothing, frame it as **discipline**, not breakage: "nothing cleared the bar
today" reads as integrity; "the system found nothing" reads as malfunction. Same fact, opposite trust
outcome.

### C4. Earn claims with evidence

Don't claim a capability, an "edge", or a result until it's actually validated — and be loud about
what *doesn't* work. An unproven claim is a debt that comes due the moment a user relies on it. Record
negative results (Part A3) so the whole team, including future AI sessions, stops chasing what's
already been disproven. "We looked; here's what we found, including the parts that failed" is more
credible than any polished promise.

### C5. Value-forward, honesty-as-footnote tone

Honest products often over-correct into apology — so hedged and disclaimered that users feel the tool
doesn't believe in itself. The fix is **ordering, not dishonesty**:

- **Lead with what the system did for the user** — the work it did on their behalf, concretely.
- **Demote caveats to a footnote** — present, findable, but not the headline.
- **Never use a fear posture.** A blank result is "held to the standard," not "the system gave up."
- **And never soften the actual boundary.** Value-forward tone changes *emphasis and order*, never the
  red line itself. If a thing is unproven, it still says so — just not as the first and loudest word.

The test: a user should finish reading feeling *served and respected*, not *warned and scolded* — and
should still come away with an accurate picture of the limits.

---

## D. Execution patterns

### D1. Spec → Plan → Execute, sized to the task

For anything non-trivial, separate the thinking from the typing:

1. **Brainstorm to a spec** — agree on *what* and *why* before *how*. Cheap to change here.
2. **Write a plan** — bite-sized, ordered tasks with exact files and test-first steps.
3. **Execute** — one task at a time, tests first, review between tasks.

This keeps the AI from sprinting confidently in the wrong direction, and it gives you natural
checkpoints. But **size the process to the work** (see D3).

### D2. Fresh context per feature unit

Long-running sessions accumulate noise that degrades quality. For a substantial feature, prefer
giving the work a clean, well-briefed context (a fresh session or a delegated sub-task) with exactly
the information it needs — rather than piling it onto a context already crowded with unrelated
history. You reason best about what you can hold in view at once.

### D3. Calibrate process weight to the change

The full spec→plan→execute→review machinery is right for features. It is *overkill* for a one-line
copy fix or a color tweak, and forcing it there just makes the human wait. Read the situation: heavy
process for heavy changes, a lean fast path for small ones. Let the human steer the dial — some
explicitly prefer the lean path and resent ceremony.

### D4. Document the deploy runbook — including what *not* to do

Shipping is where tacit knowledge hides and bites. Write the exact steps down: build, transfer,
restart, verify. Crucially, capture the **timing constraints and footguns**:

- **Windows to avoid** — if a scheduled job fires at a set time and won't back-fill, don't redeploy
  across that window or you silently drop that run.
- **Secrets handling** — *never paste passwords, keys, or root credentials into the conversation.*
  Read them on the server, don't print them. State this rule in the manual so every session inherits
  it.
- **Verification** — the one command that proves the deploy actually worked.

> Template: `references/deploy-runbook-template.md`

---

## E. Design-system consistency

A product's surface rots the same way its code does — one bespoke layout, one off-palette color at a
time. A little structure keeps it coherent.

### E1. Single source of truth for design tokens

Colors, spacing, radii, typography — define them in **one place** and have everything consume them.
Change the token, the whole surface follows. The anti-pattern is design values sprinkled across
dozens of components, where "make the brand color warmer" becomes a scavenger hunt.

### E2. Respect domain semantic conventions — don't let framework defaults override meaning

Many domains carry color/semantic conventions that mean something specific to users, and a UI
framework's defaults may *contradict* them. Pin the domain meaning explicitly and keep it separate
from incidental UI semantics.

> Example: in Chinese markets, **up is red and down is green** — the opposite of many Western
> frameworks. Price direction must follow the domain convention; meanwhile the framework's own
> success-green / danger-red (for buttons, errors, status) is a *different* axis and must not get
> entangled with price color. Two conventions, both consistent, never crossed.

### E3. Name your layout idioms and reuse them

When you find a layout pattern that works (an equal-height board of scrollable cards, a pinned
toolbar, a standard page header), give it a **name and a reusable implementation**, then use it
everywhere. Hand-rolling each page's layout from scratch guarantees they drift apart and that "make
every page consistent" becomes an endless retrofit. A named idiom is a decision you make once.

### E4. Honest hierarchy applies to the visual layer too

Part C's "value-forward, caveats demoted" isn't only about words — it's about visual weight. A
disclaimer rendered in alarming blood-red at the top of the page shouts; the same words as a calm
footnote inform. Match the visual emphasis to the honest priority.

---

## F. Working with the AI partner

Meta-habits that make the human↔AI loop tighter. These are as much for the human to know as the AI.

### F1. Tell the AI where it's blind

The AI can't see what it can't see — rendered output, a screenshot it wasn't given, the state of a
machine it can't reach. When a task depends on something outside the AI's view, say so and set up the
hand-off: *"I can't see the rendered page — after each change, I'll ask you to confirm per-page."*
Naming the blind spot turns silent misfires into a quick verification loop.

### F2. Don't clobber parallel human work

The human often edits files in their own editor while the AI works. Before overwriting, check whether
the working tree changed under you, and treat unexpected edits as the human's in-progress work to
preserve, not noise to flatten. When in doubt, ask before stomping.

### F3. Correct early and specifically

Vague frustration ("this is wrong") costs a round-trip. Specific correction ("the heat card is cut
off at the bottom on this page; the others are fine") lets the AI fix the actual thing. The AI should
*invite* specific correction (F1); the human gets faster results by giving it. Both directions of this
loop are worth stating in the manual.

### F4. State the non-negotiables, then let the partner run

The strongest pattern observed: the human states the boundaries and the goal, hands off the details,
and lets the AI execute end-to-end with sensible defaults — *because* the boundaries (Part C) and
conventions (Part A) are written down well enough to trust. Good infrastructure is what makes
delegation safe. The more of this playbook you've actually set up, the more you can hand off without
fear of drift.

---

## Where to start

You don't need all six parts on day one. A pragmatic order:

1. **Write the boundary (C1)** — one paragraph of what the product refuses to do.
2. **Start the manual (A1) + navigation table (A2)** — even a skeleton.
3. **Write the Definition of Done (B1)** — so "finished" means something.
4. **Add drift guards (B2) and a deploy runbook (D4)** once there's enough to drift or deploy.
5. **Layer in memory (A3), commands (A4), design tokens (E1)** as the project earns them.

Everything else accretes naturally once the spine is in place. The goal throughout: a product where
any fresh session — human or AI — inherits your standards instead of guessing at them.

---

## Reference files

- `references/claude-md-template.md` — a fill-in skeleton for the project manual (A1/A2), with the
  red-lines block, conventions, code map, and traps.
- `references/definition-of-done.md` — the DoD checklist (B1) plus the docs-doctor concept and a
  pre-commit reminder hook (B2).
- `references/deploy-runbook-template.md` — a deploy runbook skeleton (D4) covering steps, secrets
  handling, timing windows to avoid, and verification.
