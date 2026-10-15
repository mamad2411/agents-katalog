---
name: intent-architecture
description: >-
  Establish, bootstrap, or refactor any repository into the intent-governed four-leg structure —
  a durable `intent/` tree (vision, principles, glossary, concepts, subsystem contracts) that
  governs `design/` (the how + the chronological record of building it — design entries and ADRs),
  `src/` (code), and `test/` (tests). Use when asked to set up this layout, start a brand-new
  repository with it (scaffolds from the companion getting-started template, including its pinned
  Markdown check gate), migrate an existing repo into it, extract intent (the durable what & why)
  from existing docs and code, or explain the rules, directory/file structure, file sections,
  AGENTS.md, and per-level READMEs that govern it — including the optional build-record disciplines:
  the spec-feedback adjudication lifecycle and the delivery shape for agent-built entries.
  General-purpose: contains no project-specific content.
---

# Intent-governed architecture (the four legs)

This skill sets up — or refactors an existing repository into — a structure where a **durable
statement of intent governs everything else**. The repo stands on four parallel trees:

| Leg       | What it holds                                                                                                                                                                                                                             | Rate of change                                       |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| `intent/` | The durable **what & why** — purpose, concepts, and constraints.                                                                                                                                                                          | Only when understanding of the system changes.       |
| `design/` | The **how**, and the **chronological record of building it** — numbered **design entries** (each: scope, design, build log, spec-feedback) plus stack ADRs in `design/decisions/`, in the order made and **superseded, not overwritten**. | Appends as the build proceeds; old entries are kept. |
| `src/`    | The code that implements the design.                                                                                                                                                                                                      | Moves with `design`.                                 |
| `test/`   | Tests holding the code to the design **and** the intent.                                                                                                                                                                                  | Moves with `design`.                                 |

`design` + `src` + `test` form a triangle that moves together. **`intent` sits above them and
governs all three.** A change that must touch `intent` means you _learned something about the system
itself_, not that a tool moved.

Plus, at the root, an **`AGENTS.md`** (harness-neutral guidance for any agent/human working in the
repo) and a **`README.md`** (the orientation door). Each leg has its own `README.md` too.

This skill is **general-purpose** — it carries no domain content. You supply the domain by mining
the target repository. Ready-to-copy skeletons live in `references/templates/`; the full layout spec
and file-section schemas live in `references/structure.md`; and a complete, ready-to-run repository
template (the four legs plus a pinned Markdown check gate) lives in the skill's home repository
under [`template/`](https://github.com/crumley/intent-architecture/tree/main/template).

---

## The two layers: what/why vs. how

The whole structure rests on one distinction:

> **Intent is the _what_ and the _why_. Design is the _how_.** Intent states what must be true and
> why it matters. Design states how we build it — the plans, structures, tools, and algorithms that
> make the _what_ real.

A useful heuristic when sorting a statement: _if we changed how we build it, would this sentence
still hold?_ If yes, it is probably intent (the what/why); if it only makes sense given a particular
build, it is design (the how).

This is a **guide, not a vocabulary police.** Intent may name a concrete tool when it genuinely
clarifies — an analogy, a fixed external constraint, a worked example — and design names tools
throughout. The line is _what/why vs. how_, not whether a tool's name appears. Don't contort an
intent sentence to avoid a noun; do move a sentence to `design/` when its substance is a build
choice.

---

## The governing rules (the discipline)

1. **What/why vs. how.** Intent holds the durable purpose and constraints; design holds the
   implementation. (See the heuristic above.)
2. **One home per idea.** Every concept has exactly one canonical slice; every other place **links**
   to it rather than restating it. Each file declares what it owns in a _Canonical home for_
   section. This is what keeps an idea in one place instead of smeared across files.
3. **Why, always.** Every concept and every choice carries its reasoning. A statement without its
   _why_ is not done — the _why_ is what lets a reader apply it to a case it does not literally
   name.
4. **The triangle reconciles.** `intent`, `design`+`src`, and `test` move together but not always in
   the same commit. When one diverges, reconcile it in a following step — don't leave them silently
   inconsistent.
5. **Two audiences, always.** Everything serves a human (readable prose) and an agent (parseable
   structure: stable headings, front matter, live relative links).

Two conventions support the rules:

- **Numbered for reading order.** `00-`, `01-`, `02-` prefixes on directories and files sort into
  the order to read them. Unnumbered files (`README.md`, glossary, open-questions) are _references_
  read out of sequence — they sort to the end of their directory. Renumber neighbors when you insert
  a step and update references.
- **Cross-reference by relative path; keep links live.**

---

## The structure at a glance

```
repo/
├── AGENTS.md                      # harness-neutral guide; "read first"
├── README.md                      # the four legs + how to use the repo
│
├── intent/                        # GOVERNS the other three — the what & why
│   ├── README.md                  # the what/why-vs-how line; the rules; reading order
│   ├── 00-foundation/             # GLOBAL intent
│   │   ├── 00-vision.md           #   why the system exists, the problem, non-goals
│   │   ├── 01-principles.md       #   cross-cutting invariants every slice honors (+why)
│   │   ├── glossary.md            #   term → one-line meaning → defining slice (indexes, never owns)
│   │   └── open-questions.md      #   genuinely cross-cutting unresolved tensions
│   ├── 01-concepts/               # the DOMAIN: the nouns & processes, with their why
│   │   ├── 00-<concept>.md
│   │   └── 01-<concept>.md
│   └── 02-subsystems/             # the SWAPPABLE SEAMS: each a contract any design must satisfy
│       └── 00-<subsystem>.md
│
├── design/                        # the HOW + the record of building it — organized FOR BUILDING
│   ├── README.md                  # what design is; the entry format; the Serves-intent rule
│   ├── 0000-template/             # the design-entry template (copy to start a new entry)
│   ├── decisions/                 # ADRs — one per stack/tooling choice (start: 0000-template.md)
│   └── NNNN-<slug>/               # design entries: each README.md = scope + design + build log + spec-feedback
│
├── src/
│   └── README.md                  # implements design; layout mirrors design (itself a design choice)
└── test/
    └── README.md                  # design tests (move with code) vs. intent tests (survive swaps)
```

**`design/` does not mirror `intent/`.** Intent is organized for _understanding_ (concepts, seams);
design is organized for _building_ — which happens over time, in units of related work that may look
nothing like the concept/subsystem breakdown. Each unit is a numbered **design entry**
(`NNNN-<slug>/`); a recommended first entry is the **foundation** (global architecture + dev flow).
See `references/structure.md` for the full spec and the file-section schemas.

**A design entry is self-contained.** Its `README.md` follows one **common format** — _Serves intent
· Scope · Design · Build log · Spec-feedback · Status_ — so a single entry holds both the _how_ and
the record of producing it (what used to be split into a separate "plan"). **Stack/tooling ADRs**
live once, in **`design/decisions/`**, and entries link them.

**`design/` is a record, not a mirror.** Entries are filed in the order made and **superseded by
appending, not overwriting** — when work is re-done later, the new entry marks what it replaces and
points back; the old one stays (its Status points forward), so _why it changed_ is never lost. This
is what makes `design/` read differently from `intent/`: intent is a fresh statement of the current
tip; design is the lineage that got there — and the diff in `intent/` between entries is the visible
payoff.

---

## Optional: the build record, the delivery shape, and contribution guidelines

Three things earn their keep in repos that are **where a system is built**, not only specified. All
are **optional** — add them when they fit; omit them for a pure spec repo.

- **The build record lives in `design/` itself** (there is **no separate `plan/` leg** — it folds
  into design). When the repo is also where the system is _made to run_ as an experiment that feeds
  back into `intent/`, a design entry carries not just the _how_ but the **act of building** it: its
  **Scope** (boundary + acceptance test), an append-only **Build log** (goal / what was done /
  what-works-now-with-the-exact-command / next), and **Spec-feedback** (intent frictions found while
  building). Stack/tooling choices are **ADRs in `design/decisions/`**. The load-bearing discipline:
  **the build does not silently rewrite `intent/`** — a friction is recorded in the entry's
  Spec-feedback with a **stable identifier** (`SF-001`, …, so a human can cite it precisely) and a
  concrete proposed revision, and the build proceeds on a stated assumption, leaving the spec change
  for human review. Adjudication has a shape of its own: each accepted change is its **own small
  intent-edit PR**, never bundled into a build PR (kept separate it stays reviewable and atomic, and
  a build PR cannot smuggle intent edits past review); the human's **merge is the adjudication act**
  — auditable in history, not in chat — while the build proceeds meanwhile on the SF's stated
  assumption. Once settled, the SF gets a **disposition** appended (never rewriting its text):
  `adjudicated — <link to the intent change>` or `declined — <one-line why>`; until then it is
  `pending`, and the design README indexes the pending queue so it lives in the repo, not in
  someone's head or one session's memory. Because entries are numbered and kept, the _progression_
  shows: the diff in `intent/` across entries is the visible payoff. (A pure spec repo's entries are
  just the _how_; a built repo's also carry Scope/Build-log/Spec-feedback.) Templates:
  `design-entry`, `design-decision`.
- **The delivery shape for agent-built entries.** When entries are built by agents and gated by a
  human: **entry ↔ branch ↔ PR, one to one**, the PR body distilling the entry (scope, evidence, SFs
  raised) with links back to it; the **owner's commissioning directive quoted verbatim** at the top
  of the entry — the exact words are what later adjudication rules against, and a paraphrase loses
  the ground truth; the orchestrating agent **verifies the build independently** (its own gate run,
  its own smoke test, a read of the entry) before the PR opens; gated acts (merge, close) stay with
  the human. Concurrent entries add a protocol, because two PRs each green alone can make the main
  line red when both merge — **file-disjoint is not meaning-disjoint**: each entry's build log names
  its shared surfaces; the second of any concurrently built pair merges only after a rebase and a
  combined gate; the main line's gate is verified after any merge of concurrent work; and entry
  numbers are **reserved at commission time** so parallel builds don't collide on "next in
  sequence". Finally, **delivered means reachable**: a forge reporting "merged" is not proof the
  work reached the main line (a stacked PR can merge into a stale base and strand the work) — before
  an entry's Status moves to accepted, verify the merge commit is an ancestor of the main line
  (`git merge-base --is-ancestor <merge-commit> <main>`), and retarget stacked PRs to the main line
  before merging. Full detail: `references/structure.md`.
- **`CONTRIBUTING.md` — how we build here.** The engineering qualities every contribution honors —
  **opinionated, automated formatting/linting on every artifact** (push checks into tooling so a
  contributor, human or agent, gets fast automated feedback), **a fast write→fail→fix test loop**,
  and **high-assertion-density, table-driven tests** (cases first, setup at the bottom, pinned
  counts kept as deliberate composition tripwires). Distinct from `AGENTS.md` (the four-leg
  discipline) and `intent/` (what the system is). Template: `CONTRIBUTING`.

---

## When asked to start a NEW repository

When the user wants a **fresh repository** with this structure (there is nothing yet to mine),
scaffold from the companion **getting-started template** instead of hand-assembling the skeleton.
The template ships the four legs, per-leg READMEs, `AGENTS.md` (with a `CLAUDE.md` symlink), an
`intent/` placeholder skeleton, a `design/` tree whose `0001-docs-foundation` entry and ADRs record
the template's own tooling choices, and a pinned Markdown check gate (mise running dprint + lychee,
with CI running the same `mise run check`).

1. **Scaffold** into the target directory and initialize git:

   ```sh
   npx degit crumley/intent-architecture/template <dir> && cd <dir> && git init
   ```

   (No `npx`? `git clone --depth 1 https://github.com/crumley/intent-architecture` and copy its
   `template/` directory instead. No network at all? Build the docs skeleton from
   `references/templates/` and tell the user the check gate can be added later from the template
   repository.)

2. **Prove the gate green before touching content**: `mise install && mise run check` (Markdown
   format + links). If mise is not installed, say so and continue — the structure works without it;
   the gate can be enabled later.
3. **Work the checklist** at the top of the template's `README.md`: name the system, choose and
   commit a license (the template deliberately ships none — until one lands, the new repo is
   all-rights-reserved by default), then delete the getting-started block.
4. **Fill the intent from the user, not from thin air.** Continue with phases 3–9 below, treating
   the conversation and anything the user provides as the material to mine — phase 1's survey is the
   conversation itself, and the do-not-invent rule applies with full force to an empty repo.
5. **Leave the template's design record in place.** `design/0001-docs-foundation/` and its ADRs
   document tooling the new repo actually ships; if the project later chooses differently, supersede
   them (never delete). The project's first real design entry is `0002-`.

---

## When asked to apply this to a repository

Work through these phases. **Do not invent domain content** — extract it from what exists. If the
repo is brand-new, scaffold from the template first (previous section), then join at phase 3; if it
has docs and code, you are mining and refactoring. Read `references/structure.md` and the relevant
`references/templates/` before writing files.

### 1. Survey what exists

Inventory the repo before changing anything. Look for, and read:

- READMEs, `docs/`, `ARCHITECTURE.md`, ADRs, design notes, wikis, RFCs, comments at the top of
  modules, commit messages, issue/PR descriptions.
- The code itself: module boundaries, public interfaces, config, what is pluggable vs. hardwired.

Produce a short inventory: where purpose lives, where constraints live, where build/how detail
lives, and what is missing. **Present this and your migration plan before mass-moving files.**

### 2. Separate the what/why from the how

This is the heart of the work. For each statement you found, ask whether it is the _what & why_
(destined for `intent/`) or the _how_ (destined for `design/`). Watch for the common case: a "we use
X to do Y" sentence usually hides an intent constraint (_why Y must happen_) wrapped around a design
choice (_X_) — split it, sending each half to its leg. Recover missing _why_ (rule 3) from the code,
history, and issues; if it can't be recovered, record it as an open question rather than fabricating
it.

### 3. Lay the foundation (`intent/00-foundation/`)

- **`00-vision.md`** — what the system is, the problem it solves, the boundaries, non-goals. The
  _why_ every other slice serves. If there's a single organizing lens (a "prime directive"), name it
  here.
- **`01-principles.md`** — the numbered cross-cutting invariants, each with its _why_. Mine these
  from recurring rules in the code and docs ("we always…", "never…", validation patterns).
- **`glossary.md`** — term → one-line meaning → _defining slice_. It indexes, it never owns a second
  definition.
- **`open-questions.md`** — only genuinely cross-cutting tensions; per-slice questions live inline
  in their slice and are indexed here.

### 4. Identify concepts and subsystems

- **Concepts (`01-concepts/`)** — the nouns and processes of the domain, with their _why_. One file
  per concept, numbered in reading order.
- **Subsystems (`02-subsystems/`)** — the _swappable seams_: the places where a concrete tool plugs
  in (storage, transport, rendering, an external provider, the CLI surface…). Each intent file
  states the **contract any design must satisfy** and points to wherever its design is planned.
  Number them from the most foundational outward.
- Where a concept or subsystem deliberately **leaves a decision or constraint to implementation**,
  say so _inline_ in that slice (a short "Left to implementation" note) — that is the right home for
  deferred decisions, not a separate top-level register. Deferral is deliberate room: the build may
  realize an open mechanism with **more than one technique behind the same contract** and let real
  use pick the winner (the design rule _plural techniques converge through use_).

Write each slice from `references/templates/intent-concept.md` and
`references/templates/intent-subsystem.md`.

**Recommended: a walkthrough** (e.g. `intent/03-walkthrough.md`) — one concrete scenario threaded
through the concepts. Not required structure, but it earns its keep twice over: a scenario is intent
text a builder can **rule against**, not just read — in practice, when a design question arises
mid-build, walkthrough sections get cited as adjudication authority — and it stress-tests the
concepts, because a gap shows up as a step the walkthrough cannot narrate.

### 5. Plan the build in `design/`

`design/` holds numbered **design entries**, filed in the order the work happens — not as a mirror
of `intent/`. Each entry is a directory whose `README.md` follows the common format (_Serves intent
· Scope · Design · Build log · Spec-feedback · Status_), so it holds both the _how_ and the record
of building it. Typically:

- Start with a **foundation entry** (recommended first step): the global architecture and dev flow —
  language/runtime, repo and module layout, the toolchain and its single check gate.
- Then add an entry per unit of work as it clusters (milestone, component, feature area, phase).
  Each opens by pointing back to the intent it serves (the _what/why_ it realizes), then states the
  _how_.
- Record stack/tooling choices as **ADRs in `design/decisions/`**; entries link the ADRs they rest
  on.

Use `references/templates/design-foundation.md`, `design-entry.md`, and `design-decision.md`.

### 6. Place `src/` and `test/`

- `src/README.md` — code implements `design/` under `intent/`; the module layout mirrors the design
  (and the layout is itself a recorded design decision).
- `test/README.md` — distinguishes **design tests** (the code does what _this_ design says; move
  with code) from **intent tests** (durable constraints that should survive a design change). If a
  test must change because a tool changed, it was really a design test.
- If code already exists, leave it in place and document how it maps; don't relocate working code
  just to match the diagram unless the user asks.

### 7. Write the doors: `AGENTS.md` and the READMEs

Use the templates: root `README.md`, root `AGENTS.md`, and a `README.md` for each of `intent/`,
`design/`, `src/`, `test/`. `AGENTS.md` is harness-neutral (not tied to any one agent tool) and
restates the rules and the reading order. The repo "reads first" from `AGENTS.md`.

### 8. Apply the numbering and check the links

Apply the numbering convention to intent (and to design where an ordering exists), and confirm every
relative cross-reference resolves.

### 9. Hand off the living discipline

The structure is now the **living contract** for the repo going forward, not a one-time artifact.
Tell the user the maintenance loop: changes flow `intent → design → src/test`; touching `intent`
means understanding changed; every idea keeps one home; every choice keeps its _why_. Point them at
`AGENTS.md` as the entry point.

---

## Adapt, don't impose

The four-leg skeleton and the rules are invariant. The _contents_ are not: the number of foundation
files, whether a repo needs `01-concepts/` vs. only `02-subsystems/`, and how `design/` is organized
all depend on the target. A tiny library may need only `intent/00-foundation/` and a single design
entry; a large system may need many concepts, seams, and entries. The build-record depth of
`design/` (the Scope / Build-log / Spec-feedback in entries, and ADRs in `decisions/`), the delivery
shape, and `CONTRIBUTING.md` are likewise scaled to fit — add them only when the repo is _built_,
not merely specified. Scale the structure to the repo, but never collapse the **what/why ↔ how
boundary** or the **one-home** rule — those are what make it work.
