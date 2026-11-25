---
name: plan-deck
description: >
  Turn a plan into a short, very visual PDF slide deck before it runs, rendered locally with `aval deck`
  (no vendor, any project, any agent). Use before executing any odd/tasks plan, and whenever someone asks
  for slides, a deck, a presentation or "diapositivas" of a plan, feature or architecture.
---

# plan-deck

aval's rule: **nobody runs a plan they have not seen.** Before executing a plan,
turn it into a deck the person can read in five minutes and understand without
being technical. The deck is a PDF, built on this machine by `aval deck`, with
the look fixed by aval. You write only content.

The plan gate enforces it: while the active `odd/tasks/*.md` plan has no deck,
edits outside `odd/` are denied. `aval deck build ... --plan <plan>` unlocks them.

## Workflow

1. **Read the plan** and what it touches. Write in the language the person is using.
2. **Ask where to save it**, once per session, with the runtime's question tool
   (Claude Code: AskUserQuestion; elsewhere a plain question). Offer:
   `<project>/docs/decks/` (recommended in a repo), `~/Documents/aval/decks/<project>/`,
   or a path they type. Then STOP and wait.
3. **Get the shape**: run `aval deck example` once. It prints a valid spec using
   every layout; copy its structure, never its words.
4. **Write the spec** straight to `<dir>/<slug>.deck.json` (slug = plan name).
5. **Build**: `aval deck build <dir>/<slug>.deck.json -o <dir>/<slug>.pdf --plan odd/tasks/<plan>.md --open`.
   Validation and overflow errors name the slide: shorten the text or split the
   slide, rebuild. Never loosen a limit or hand-edit HTML.
6. **Reply** with the PDF path and three lines: what the deck says, what was left
   out, what is still unverified.

## The story (default order; drop what the plan does not need)

| # | Layout | Purpose |
|---|---|---|
| 1 | `cover` | The promise in one sentence: what changes for the person |
| 2 | `statement` | Define the one word everything depends on (e.g. "context") |
| 3 | `cards` (warn) | The problem: 3 symptoms the person already feels |
| 4 | `compare` or `flow` | The idea, as a picture or before/after |
| 5 | `steps` | How it works, in 3-5 steps that happen in order |
| 6 | `timeline` | A concrete example with times and names |
| 7 | `checklist` | What is guaranteed or kept |
| 8 | `groups` | Who or what it covers, grouped by what the person notices |
| 9 | `section` | "Inside: how it is built" |
| 10 | `flow` | The pieces, named by what they do, and how they connect |
| 11 | `steps` or `table` | What happens inside, step by step |
| 12 | `tree` | How it decides (question → answer) |
| 13 | `table` | Decisions: *we decided · because · instead of* |
| 14 | `table` | Map: where each part lives (folders, commands) |
| 15 | `checklist` | Safety: brakes, limits, what happens when it fails |
| 16 | `steps` | The road: phases, the first one marked as the gate |
| 17 | `closing` | The next concrete step |

A small plan needs 6-8 slides (1, 3, 5, 6, 13, 17). A feature needs 12-20. Never over 40.

## Tone (learned the hard way)

- **Plain first.** The first half must make sense to someone who does not code.
  The second half ("Inside") can be technical, but every term is explained by
  what it does.
- **Keep the real word.** Use the domain's own term (context, cache, migration)
  and define it with a picture early; never hide it behind a metaphor only.
- **Declarative names.** Name pieces by their job: *Meter, Decider, Note writer,
  Work register, Brakes*, not internal jargon (tiers, ports, T0, adapters). Jargon
  goes in `note`, or in the Inside part with its meaning beside it.
- **Titles are claims.** "The context stays in the comfortable zone", not
  "Comparison". The `eyebrow` names the section.
- **One idea per slide.** Short sentences. Concrete: times, names, numbers the
  plan really has.
- **Show the decisions.** Every important choice says what was rejected and why.
- **Honest.** Mark targets as targets and unverified facts as unverified. Never
  invent a statistic, a quote or a capability.
- **Speaker notes** (`note`): what to say on that slide, one or two sentences.

## Tones (meaning, not decoration)

- `good` (green): the new way, what works, what is kept.
- `warn` (orange): a threshold, a problem, something to watch.
- `muted` (dashed grey): the old way, an alternative, what is out.
- No tone: neutral.

## Checklist before building

- [ ] Asked where to save, and used that path
- [ ] The first slides work for a non-technical reader
- [ ] The key word is defined early, with a picture
- [ ] An example with real-looking times or names
- [ ] Pieces named by their job; jargon only explained
- [ ] Decisions show what was rejected
- [ ] Unverified things are marked
- [ ] Ends with the next concrete step

## Never

- Claude Artifacts, Google Slides or any other vendor: the deck is local and the output is always PDF.
- Hand-written HTML or CSS: the look belongs to aval (dark brand, fixed type scale).
- A deck tied to a tool the plan is replacing.
- Walls of text, light themes, everything in tables, or a deck with no "Inside" part when the plan builds something.
- Bypassing the gate (`AVAL_PLAN_DECK_OFF=1`) unless the person asks for it.
