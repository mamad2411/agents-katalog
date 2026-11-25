---
name: codebase-analyzer-docs
description: Consult this skill BEFORE starting any task where a user asks for written documentation, architecture explanation, design docs, onboarding material, ramp-up guides, or contributor guides covering an entire codebase, repository, service, module tree, crate, package, or project. Do NOT begin exploring the repo or drafting docs directly — read this skill first; it defines the multi-document structure, grounding rules, and diagram conventions that the user expects and that a direct chat summary will miss. Trigger phrasings include "document this repo", "write an architecture doc for X", "help me onboard to this codebase", "produce a design doc for the backend", "deep-dive this repo and write it up", "write a contributor guide", "ramp-up guide", "write docs for the whole project", "explain how this thing is put together", "give me a structured writeup of X", and any non-English equivalents. ALSO trigger on narrative/situational asks that imply a whole-codebase writeup, even when the word "document" is not used — e.g. "I just inherited this monorepo, help the new hires ramp up", "we hired 3 engineers and want them reading something useful", "nobody remembers why half these packages exist, can you deep-dive this", "the readme is 4 lines, give me something proper", "help me understand this codebase". If the target is a whole repo/module tree (not a single file or function), invoke. Without this skill, the model produces a short chat summary; with it, the model produces a multi-file documentation suite (OVERVIEW.md, ARCHITECTURE.md, QUICKSTART.md, per-module deep-dives, Mermaid diagrams, GLOSSARY.md) under docs/codebase/ in the target repo, grounded with file:line citations throughout. Do NOT trigger for single-file or single-function explanations, README polishing, API reference generation from docstrings (use Sphinx/TypeDoc/rustdoc), design docs for features that don't exist yet, blog posts, or fixing bugs in an existing docs site.
license: MIT
---

# codebase-analyzer-docs

Produce the documentation a new engineer actually needs: an honest, specific, grounded walkthrough of how a codebase is put together, why it's shaped that way, and where to look when you want to change something.

The output is a **suite of documents** — not one megapage — placed under `docs/codebase/` in the target repo (override on request). Every non-obvious claim cites real code (`path/to/file.ext:line`), so the reader can verify and so you can't drift into plausible-but-wrong generalities.

## When to use this

- User points at a repo ("document this", "write an architecture doc for the auth service", "help me onboard to this codebase") and wants something deeper than a README.
- User says "design doc", "architecture writeup", "onboarding guide", "contributor guide", or "explain how X is put together" and the target is a whole repo/project/module tree.
- Codebase is unfamiliar to both the reader *and* the person asking — the goal is genuine understanding, not a sales summary.

Skip this skill when:
- The ask is "explain this function" / "what does this file do" — answer inline, no doc suite needed.
- The ask is API reference generation from docstrings (use a doc generator like Sphinx/TypeDoc/rustdoc).
- The user only wants a top-level `README.md` polish.

## The quality bar

Before touching the keyboard, keep these in mind — they're what separates a useful doc suite from a glossy-but-empty one.

1. **Grounded, not plausible.** Every architectural claim, call path, data shape, or invariant must be traceable to actual code. Cite file and line (`src/api/router.ts:42`). If you can't find evidence, mark it *Uncertain* and say what you looked at — never fill gaps with generic framework knowledge.
2. **Specific beats comprehensive.** Prefer "the `Scheduler` coalesces updates via a 50ms debounce in `core/scheduler.ts:88`" over "the system uses various optimization techniques". Readers can always skim detail; they cannot un-skim vagueness.
3. **Explain why, not just what.** Names and signatures already say *what*. The value you add is *why* — the constraint that forced this shape, the tradeoff that was taken, the non-obvious invariant that would break if you edited carelessly. Look for these signals: comments, commit messages, `git blame` on gnarly sections, tests that exist for unexpected reasons.
4. **Readable to two audiences.** A working contributor should find the deep-dive detail they need to make a change. A newcomer should be able to enter via `OVERVIEW.md` → `QUICKSTART.md` and not drown. Every deep doc should start with a 3-5 line "in plain words" summary before going technical.
5. **No hallucinated diagrams.** A diagram that reflects code is worth ten paragraphs; a diagram invented to look professional is worse than no diagram. Only draw structures you've verified against source.

## The workflow

Follow these phases in order. Don't try to write the per-module docs before you've mapped the terrain — you'll repeat yourself and miss cross-cutting themes.

### Phase 1 — Scope & inventory

Goal: know what you're looking at before you write anything.

- Confirm the target repo path and the desired depth: **lite** (one `OVERVIEW.md`, skim top layers), **standard** (overview + 3–8 module deep-dives + diagrams, default), or **deep** (add per-submodule docs, data-model doc, ADR-style rationale sections). Ask once if unstated.
- Confirm the output path. Default: `<repo>/docs/codebase/`. If that would overwrite existing docs, propose a subdir or ask.
- Build an inventory without opening every file:
  - Root-level files (`README`, package/manifest files, build configs, CI configs, license).
  - Top-level source directories and their size (file count, line count).
  - Language mix, framework fingerprints (`requirements.txt`, `package.json`, `go.mod`, `Cargo.toml`, `pom.xml`, etc.).
  - Entry points (`main.*`, `cli.*`, `server.*`, `index.*`, HTTP route registrations, `if __name__ == "__main__"`).
  - Test layout (where tests live, what framework, coverage if configured).
- Produce a short **inventory note** (internal — no need to render) listing: language/framework stack, entry points, top-level modules, build & test commands, and anything unusual (generated code, vendored deps, submodules).

If the repo is huge (>5k files or >500k LOC), propose a focused scope rather than documenting everything. Documentation that never gets finished is worse than documentation that's explicit about its boundaries.

### Phase 2 — Architecture synthesis

Goal: form a single coherent mental model before describing pieces.

Read in this order, not alphabetically:

1. **Entry points** — where does execution actually start? Trace the first 50–200 lines from each entry to understand what gets wired up.
2. **Composition roots** — DI containers, service registries, route tables, plugin registries. These reveal the component graph.
3. **Core domain types** — the 5–15 types that appear most often in the rest of the code. These are the vocabulary of the system.
4. **Boundary code** — HTTP handlers, CLI commands, database adapters, message consumers. These show the system's shape to the outside world.
5. **Hot spots** — files with the most `git log` churn, largest files, files touched by many contributors. These are usually where the real complexity lives.

From these, answer: What are the layers? What are the components in each layer? How do requests (or events, or jobs) flow through? What are the main data shapes that cross component boundaries?

### Phase 3 — Module deep-dives

Goal: for each significant module, produce a document a new contributor could read and then confidently make a change.

A good module deep-dive is structured like this:

```
# <Module name>

## In plain words
<3–5 line summary a non-specialist can follow.>

## Responsibility
<What this module owns. What it explicitly does NOT own.>

## Public surface
<Exported types/functions/endpoints, with file:line refs.>

## Internal structure
<Key files, their roles, and how they relate. One Mermaid diagram if the
shape isn't obvious from prose.>

## Key code paths
<2–4 concrete flows through the module, each traced with quoted snippets.
Snippets should be short — 5–20 lines — with a file:line ref above each.>

## Invariants & gotchas
<Things that will burn a new contributor: subtle ordering, thread-safety,
caching assumptions, "don't call X without Y". Source these from comments,
tests, or commit messages — don't guess.>

## How to extend it
<A worked example: "To add a new <thing>, touch these files, following the
pattern already used by <existing example>.">

## Related
<Links to other module docs, ADRs, or external references.>
```

Quote code with a fenced block and a reference line:

```ts
// src/scheduler/coalesce.ts:88
if (pending && now - pending.ts < DEBOUNCE_MS) {
  pending.merge(update);
  return;
}
```

Keep each snippet focused on one idea. Large dumps defeat the purpose — readers start skimming.

### Phase 4 — Diagrams

Use Mermaid by default: it renders on GitHub, in most IDEs, and needs no toolchain. PlantUML is supported only if the user asks or if the repo already uses it.

Draw these when they clarify something prose cannot:

- **Component diagram** (`flowchart`) — top-level blocks and the edges between them. One at repo level, optionally one per large module.
- **Sequence diagram** (`sequenceDiagram`) — for request/event flows that span ≥3 components. Pick 1–3 canonical flows, not every endpoint.
- **Data model / ER** (`erDiagram`) — for any persistent schema, derived from actual migrations / schema files, not inferred.
- **State diagram** (`stateDiagram-v2`) — when the code has an explicit state machine (look for `status` / `state` enums with transition logic).

Each diagram must have a one-paragraph caption explaining *what the reader should notice*. Diagrams without captions are decoration.

Anti-pattern: drawing a generic "client → API → service → DB" flowchart that would fit any web app. If your diagram would be true of someone else's codebase, it isn't telling the reader anything about this one.

### Phase 5 — Glue documents

These tie the suite together and are the actual entry points for readers.

- **`OVERVIEW.md`** — one page. What the project is, the problem it solves, the 3–7 major components, and a repo-level component diagram. Ends with "Where to go next" pointing at the other docs.
- **`QUICKSTART.md`** — how to clone, install, build, run, and test, *derived from actual scripts* (`Makefile`, `package.json` scripts, CI configs). Mark steps the docs imply but you haven't verified.
- **`ARCHITECTURE.md`** — the synthesis from Phase 2, written long-form. Layers, components, data flows, major design decisions. This is the doc senior contributors will actually cite.
- **`GLOSSARY.md`** — domain/project-specific terms that appear in the code but aren't obvious. Pull from naming, comments, docstrings.
- **`modules/<name>.md`** — one per deep-dive from Phase 3.
- **`decisions/`** *(deep mode only)* — short ADR-style notes for major design decisions you can reconstruct from commits, comments, or the code's shape.

## Output layout

Default target (inside the repo being documented):

```
docs/codebase/
├── OVERVIEW.md
├── QUICKSTART.md
├── ARCHITECTURE.md
├── GLOSSARY.md
├── diagrams/
│   ├── system-overview.md      # Mermaid source + caption
│   └── <flow>.md
├── modules/
│   ├── <module-a>.md
│   └── <module-b>.md
└── decisions/                   # deep mode only
    └── 0001-<slug>.md
```

If the target repo already has a `docs/` tree, nest under `docs/codebase/` rather than merging — avoid collisions with whatever convention they already have.

## Handling uncertainty

You will hit things you can't fully explain from source alone. Handle them like this, in order of preference:

1. **Resolve via evidence** — `git log`, `git blame`, test names, commit messages, linked issue IDs.
2. **Mark explicitly** — `> **Uncertain:** this looks like a cache-warming path but no test exercises it; verify with the original author.`
3. **Ask the user** — if a handful of uncertainties could be resolved by two questions, ask before finalizing.

Never paper over gaps with generic framework knowledge ("this is probably a standard Express middleware pattern"). The reader already knows what Express is; they're reading your doc to learn *this* codebase.

## Depth tiers

- **lite** — `OVERVIEW.md` + `QUICKSTART.md` + one repo-level diagram. Use when the user asks for a "quick writeup" or the repo is tiny.
- **standard** *(default)* — all glue docs + 3–8 module deep-dives + 2–4 diagrams. Suitable for most repos.
- **deep** — standard + submodule docs + `decisions/` ADRs + a data-model doc if there's persistence. Use for production systems a team needs to onboard into.

Pick once, announce the plan to the user before writing, and stop to confirm if scope creeps.

## Anti-patterns to avoid

- **The glossy tour.** Marketing prose with no file refs. Readers can't act on it.
- **The autogenerated wall.** Dumping every class/function with its docstring. This is what `sphinx-apidoc` / `typedoc` / `rustdoc` are for, and they do it better. Don't duplicate them.
- **Aspirational docs.** Documenting how the code *should* work instead of how it does. If you spot a bug or a weird shape, note it as an observation; don't rewrite reality.
- **Diagram-shaped decoration.** A flowchart that could describe any web app. See Phase 4.
- **Unbounded scope.** Trying to document a 1M-LOC monorepo end-to-end. Pick a surface and say so in `OVERVIEW.md`.

## Finishing checklist

Before handing off, confirm:

- [ ] Every doc opens with a "plain words" summary readable by a newcomer.
- [ ] Every non-trivial claim has a file:line reference.
- [ ] Diagrams reflect code you actually opened, with captions pointing at what to notice.
- [ ] `QUICKSTART.md` commands are pulled from real build/CI scripts, not invented.
- [ ] Uncertainties are flagged, not hidden.
- [ ] `OVERVIEW.md` reads well as the first thing a newcomer opens.
