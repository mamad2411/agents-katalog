---
name: slopbuster-docs
license: Apache-2.0
description: Document an entire codebase for two audiences — humans taking it over (handoff/onboarding) and an AI replaying it (a reverse-engineered, replayable rebuild blueprint). Use when asked to document a project or codebase, write technical/architecture docs, produce onboarding or handoff documentation, bring an undocumented project up to speed, OR to reverse-engineer the specs and prompts that would let an AI agent regenerate the project ("reverse vibe coding" — extract the design system, architecture, and feature specs as replayable prompts). Reads the code file-by-file (never from memory) and produces a durable docs set — overview, architecture, per-subsystem, data model, setup, operations, a handoff briefing, and an optional rebuild blueprint (design-system + per-area spec/prompt pairs + a rebuild order) — with diagrams, plus a small docs.json manifest.
---

# SlopBuster — Docs

You are writing the documentation a new senior engineer needs to **take this codebase over
cold** — no prior context, no original author to ask. Documentation and handoff are where
projects live or die: undocumented systems rot into slop because nobody dares change what
nobody understands. Your output is a **map and the reasoning behind it**, not a tour and not a
restatement of the code.

The bar is the **handoff test**: could a competent engineer who has never seen this repo become
productive — find the entry points, change a subsystem safely, ship, and operate it — from these
docs alone? If not, the docs aren't done.

## Ground every word in the actual code — never document from memory

Documentation that lies is worse than none: it sends the reader confidently wrong. So the same
discipline as the audit applies here.

1. **Reconstruct intent and detect the stack** from manifests and layout (`pyproject.toml` /
   `Cargo.toml` / `package.json` + framework configs), the README, and any existing
   `.slopbuster/plan/` docs. What is this system, who is it for, what's the runtime shape
   (sync / streaming / async, service / library / CLI / app)?
2. **Enumerate the source set and read it.** Glob the real source files (exclude build/vendor),
   write the list down, and **open the files that matter end to end with the Read tool** — entry
   points, the largest and most-imported modules, the data layer, the public surface, config and
   wiring. You do not need every trivial file verbatim, but every claim you write must trace to
   code you actually read, not to a guess or a memory. When you state how something works, you
   should be able to point at the file and symbol.
3. **Trace the real paths.** Follow a request / command / event from entry point to its effect.
   The valuable documentation is the *flow* and the *why*, and those only come from tracing.
4. **Reconcile with existing artifacts.** If `.slopbuster/plan/` or `.slopbuster/audit/` exist,
   read them: the plan records intended design and decisions; the audit records known problems.
   Fold their truth in (and note where the code has since diverged from the plan).

## What good technical docs contain (and what they don't)

Document the things that are **true, stable, and not already obvious from reading one file**:

- **The mental model** — the one-paragraph "what is this", then the shape of the system: the
  major parts and how they fit. A reader should be able to hold the whole thing in their head.
- **Architecture & boundaries** — components/modules/services, who owns what, the dependency
  direction, and the data/control flow between them. Name the seams where responsibility changes.
- **The critical paths** — for each important flow (a request, a job, a user journey), how it
  travels through the system and where the real work happens.
- **The data model** — entities, schema, relationships, lifecycle, and the **invariants** that
  must hold (these are the things a newcomer breaks without knowing).
- **Setup & development** — how to get it running, build, test, and the everyday dev tasks.
- **Operations** — how it deploys and runs, configuration and secrets, runtime topology,
  observability, and the known failure modes (for anything that actually runs in production).
- **The why** — the decisions that shaped the system and the rationale behind them, especially
  the non-obvious ones. A reader who knows *why* can change safely; one who only knows *what*
  cannot.
- **Tribal knowledge & landmines** — the things the original author knows that aren't written
  anywhere: the fragile spots, the "don't touch X because Y", the workarounds, the gotchas, the
  half-finished threads. This is the highest-value, most-often-missing content. Capture it.

Do **not** write: a line-by-line narration of code (it rots and duplicates the source), generic
filler that restates the obvious ("this function returns a value"), aspirational docs for things
that don't exist, or a wall of auto-generated API signatures with no explanation. If a sentence
would be equally true of any project, cut it.

### Durability — write docs that survive edits

Code moves; docs that pin to it die. Anchor to **stable references**: cite `path` + symbol name
(function / type / module), not bare line numbers. Describe behavior and contracts, not exact
current implementation detail that will change next week. Prefer concepts that outlive a refactor.

### Diagrams where they earn their place

Use **Mermaid** fenced blocks for what prose explains badly: a `flowchart` for architecture and
component relationships, a `sequenceDiagram` for an important request/event flow, an
`erDiagram` for the data model, a `stateDiagram-v2` for a lifecycle/state machine. One clear
diagram per major concept — not decoration. See [references/writing-guide.md](references/writing-guide.md)
for conventions and the documentation-type framing (orientation vs. how-to vs. reference vs.
explanation), grounded in established documentation practice.

### Write rich, scannable markdown — not walls of text

Dense paragraph dumps are hard to read and hide the signal. Make every doc read like a real report
that someone can skim: **headings & subheadings** to chunk it, **bullet and numbered lists** for
steps/sequences/options, **tables** for anything comparative or tallied (entities, config keys,
endpoints, a setup checklist, a per-module breakdown), **inline `code`** for symbols/paths/values and
**fenced code blocks** for commands/snippets, **bold** for the load-bearing phrase, and
**blockquotes** for a key caveat. Lead each document with a short orientation, then break the rest
into sections. The bar: the reader grasps the shape in seconds and finds the exact thing they need
without reading a wall of text.

## Output: a docs set + a small manifest (master-detail, one folder of its own)

Like the audit and the plan, the documentation is **many focused markdown files, one per area —
not one monolithic document** — plus a small `docs.json` manifest as the index. This keeps each
file readable and editable and drives the desktop app's master-detail UI (left = the doc list
with summaries, right = the selected doc).

**Sections are flexible — fit them to the project.** Default to the set below; add, drop, split,
or merge to match what this codebase actually is (a library needs no `operations.md`; a service
may want `api.md`; a monorepo may want one file per package). Each section you keep becomes one
`docs.json` entry **and** one markdown file.

Default sections:

- **`overview.md`** — what it is, who it's for, the mental model, a 5-minute orientation.
- **`architecture.md`** — components, boundaries, dependency direction, data/control flow, the
  architecture diagram(s).
- **`<subsystem>.md`** — one per major module/service/package: its responsibility, public
  surface, internals worth knowing, and its gotchas.
- **`data-model.md`** — entities, schema, relationships, invariants, migrations.
- **`setup.md`** — prerequisites, install, run locally, build, test, common dev tasks.
- **`operations.md`** — deploy, config/env, secrets, runtime topology, observability, failure
  modes (only for things that run in production).
- **`handoff.md`** — the takeover briefing (see below).
- **`glossary.md`** — domain terms a newcomer won't know.

Rebuild-blueprint sections (add when the goal includes regenerating or replaying the project — see
"Rebuild blueprint" below). Skip them for a pure read-to-understand handoff:

- **`design-system.md`** — the project's real visual language extracted from the actual CSS /
  components (concrete tokens: colors, spacing, typography, radii, layout). A spec, not a prompt.
- **`rebuild-<area>.md`** — one per regenerable area (architecture, a feature, the stack): the
  distilled, concrete spec. A spec, not a prompt.
- **`rebuild-order.md`** — the dependency-ordered build sequence (scaffold → design system → data
  layer → features → polish).
- **`rebuild-prompt.md`** — the **single** copy-paste prompt that drives the whole rebuild (see
  below). This is the one file the user hands to an AI agent.

### The handoff briefing (`handoff.md`) — the signature deliverable

This is the document that makes this skill worth running. Write the briefing you would give the
engineer replacing you if you had one hour: **current state** (what's done, solid, in-flight, or
fragile), **known issues and landmines** (what breaks, what not to touch and why), **tribal
knowledge** (the non-obvious mechanics, the workarounds, the historical reasons), **the risky
operations** (deploys, migrations, anything that can lose data), and **the open threads** (what
the next person should pick up). Be specific and honest — this is where you stop being polite and
tell the truth about the codebase.

### Rebuild blueprint — "reverse vibe coding" (optional)

When the goal includes **regenerating or replaying** the project (not just understanding it), also
reverse-engineer what an AI agent needs to **rebuild it from scratch**. The audience is vibe coders:
people who build by prompting AI. The model is deliberately **separated into specs + one driver
prompt** — NOT a prompt embedded in every facet:

1. **Spec files** (`design-system.md`, `rebuild-<area>.md`, `rebuild-order.md`) — each a concrete,
   grounded SPEC of one regenerable facet. Plain documentation of *what to build*, with real values
   (real color hexes, real spacing, the real architecture, the real feature behavior). No prompt
   text inside them. Specificity is the whole point — generic specs produce generic slop.
   - **Extract the design system from the real CSS/components** — read the token definitions and pull
     the actual values (colors, spacing scale, typography, radii, shadows, layout shell).
   - **Cover architecture and each major feature** as its own concrete spec, grounded in the code.
   - **`rebuild-order.md`** — the dependency-ordered build sequence (scaffold → design system → data
     layer → features → polish).

2. **One driver prompt** — `rebuild-prompt.md` is a **single, self-contained, copy-paste prompt**.
   It does NOT restate the specs; it **instructs an AI agent to READ the other md files in this
   folder and rebuild the project from them**, in `rebuild-order.md`'s order, to the stated stack and
   quality bar. The intended workflow is literally: the user copies `rebuild-prompt.md`, drops all
   the blueprint md files into a fresh project folder, pastes the prompt — and the agent reads the
   specs and regenerates the whole project. So the prompt names the files to read, states the build
   order and acceptance bar, and forbids inventing beyond the specs — it is the one thing the user
   hands over, the specs are its inputs.

These rebuild facets live in the **same docs set** (same `docs.json`, same version dir) as the
handoff docs — they are the AI-replay half of documenting the codebase. Ground every spec exactly
like the rest: it traces to code you opened (cite path + symbol), never fabricated.

## Persist the docs (automatic) — manifest + per-section files

Write the docs into a versioned directory **in their own folder** at the repo root, mirroring the
audit and plan layout (each kind in its own folder, one subdir per run):

```
.slopbuster/docs/<version>/
  docs.json          ← small index manifest, the app reads this first
  overview.md        ← one file per section, full content for that section only
  architecture.md
  data-model.md
  handoff.md
  …
```

`<version>` is a date (`date`, e.g. `2026-06-12`) or a version label. Create the directory if it
doesn't exist. If the app passes an explicit versioned target dir (e.g. `.slopbuster/docs/v2-<date>/`),
write `docs.json` and the section md files into that dir instead. If the user named a different
location (e.g. the repo's `docs/`), use that — these are durable team artifacts meant to be
promoted into the repo. Tell the user the directory path when finished.

### `docs.json` — the index manifest

```json
{
  "overall": "<one-paragraph summary of the whole system and what these docs cover>",
  "meta": {
    "generatedBy": "<tool + model, e.g. 'claude-code / claude-opus-4-8' — never blank>",
    "author": "<git log -1 --format=%an>", "email": "<git log -1 --format=%ae>",
    "commit": "<git rev-parse HEAD>", "branch": "<current branch>",
    "generatedAt": "<ISO-8601 — date>"
  },
  "docs": [
    { "key": "overview", "label": "Overview", "doc": "overview.md",
      "summary": "<1–2 line summary of this section>" },
    { "key": "architecture", "label": "Architecture", "doc": "architecture.md",
      "summary": "<1–2 lines>" }
  ]
}
```

- **`overall`** — short prose for the whole docs set, shown above the doc list.
- **`docs[]`** — **one entry per md file you actually wrote** (flexible set, see above). `key` is
  a stable slug, `label` is the human title, `doc` is the md filename relative to the manifest
  dir, `summary` is a 1–2 line description for the list row. Order from orientation to detail
  (overview first, handoff/glossary last). No stubs — only sections you wrote.

The full field-by-field contract is in [references/output-contract.md](references/output-contract.md).

## Working in stages (large codebases)

A big system won't document in one pass. Build the section files up incrementally:

- Go subsystem by subsystem: read it, then write or extend its section file and append anything
  architecture-level to `architecture.md`.
- **Re-read and reconcile** as you go — later subsystems reveal that an earlier description was
  incomplete or wrong; fix it.
- Write `docs.json` last, once the section set and summaries are final, so its entries match the
  files on disk.

The docs are ready only when the handoff test passes: a new engineer could take this over from
them alone. If you can't say yes, they're not done.
