---
name: context-vigilance
description: Lossless Group's framework for managing context-v/ directories in any project. Use whenever creating, updating, or organizing files in any context-v/ folder (specs, plans, prompts, blueprints, reminders, agent-skills, explorations, issues — plus the universal extra/ and sitemap/, and the experimental loops/, handoffs/, decisions/, habits/, and contracts/), or when the user asks about context engineering, AI co-development workflow, or the "context-v" convention. Enforces directory roles, the four-part epoch.major.minor.patch versioning, YAML frontmatter standard, wikilink cross-references, and the prep/reflective/journey cognitive modes.
---

# Context Vigilance

A framework for Human + AI collaboration: **manage the context available to AI and collaborators with the same rigor you manage code.** Every Lossless project has a `context-v/` directory with (commonly) eight subdirectories, organized into three cognitive modes: **Prep, Reflective, and Journey** — plus two universal utility folders and a small experimental tier still finding its shape.

**Norms, not rules.** Patterns here are loosely enforced. The team is generative-first; consistency emerges when attention focuses on a project, file, or pattern. Be generous reading existing files (they may pre-date current norms or be experiments) and careful writing new ones. See `references/philosophy.md` for the deeper rationale.

**Drift policy:** When you encounter inconsistencies (mismatched frontmatter, deviating filenames, partial-convention adoption), **observe, note, surface, but do not auto-fix as a side effect of unrelated work.** Cleanup happens only with explicit user permission. The user runs parallel agent sessions; silent normalization creates conflicts. (This rule lives globally in `~/.pi/agent/AGENTS.md`; restated here for redundancy.)

Reference: <https://www.lossless.group/projects/gallery/context-vigilance>

## When to use this skill

- The user asks you to create or edit any file under a `context-v/` directory
- The user mentions specs, prompts, blueprints, reminders, explorations, or issues in the Lossless sense
- Starting a new project and setting up `context-v/`
- The user asks about context engineering, AI co-development, or "the context-v thing"

## The Eight Directories

### Prep Mode (spec → plan → prompt)

The work of deciding what to build *is* the work — "prep" here is not "minor pre-work", it's the deliberate forward construction phase. Specs, plans, and prompts are the artifacts, in descending altitude.

- **`context-v/specs/`** — Living specifications. What you're building and why. Constantly updated. Single source of truth. Every prompt references a spec.
- **`context-v/plans/`** — Actionable work plans: sequenced, scoped, closer to execution than a spec but not yet the step-by-step of a prompt. The natural home for agent-produced plans (plan-mode output, migration sequences, refactor roadmaps). Promoted to canon 2026-07-21 after appearing organically in 14 repos — the most-adopted folder the original six didn't name.
- **`context-v/prompts/`** — Step-by-step, prompt-by-prompt implementation documents (NOT single chat messages). Each prompt references specs/plans/blueprints/reminders. Success at each step is verifiable before moving on.

> A prompt without a spec is a vibe. A prompt within a spec is engineering.

### Reflective Mode (blueprint ↔ reminder, plus agent-skills)

- **`context-v/blueprints/`** — Codified patterns, architecture decisions, proprietary thinking. Institutional knowledge AI needs to respect the system (e.g., "how our extended markdown flavor works", component organization, naming rationale).
- **`context-v/reminders/`** — Short, sharp corrections born from repeated AI mistakes (e.g., "We don't use React. Astro + Svelte for interactivity. Do not hard-validate frontmatter."). Battle scars turned into guardrails.
- **`context-v/agent-skills/`** — Per-repo agent skills following the Anthropic agent-skills shape (`<name>/SKILL.md` + optional `references/`, `templates/`, `scripts/`). This is the incubator: skills are born here next to the code they serve, and graduate to the shared public `lossless-agent-skills` repo (mounted at the anchor monorepo's `context-v/skills/`) once they prove out or apply beyond one repo. Reflective mode's executable tier — a blueprint an agent can *load and follow*, not just read.

### Journey Mode (unpaired)

- **`context-v/explorations/`** — Documents where the destination is unclear. Research, prototype tradeoffs, option-space mapping, thinking out loud with AI as partner. Ends when you've learned enough to write a spec — or decided you don't need one.
- **`context-v/issues/`** — Issue-resolution journey logs. The painful, winding path through debugging. Capture so no human or AI has to retrace it.

### Universal utility folders (any project, any mode)

Two folders that aren't doc-types so much as infrastructure, applicable to every project:

- **`context-v/extra/`** — Scratch and out-of-band material: half-thoughts, pasted transcripts, working files that aren't ready to be (or shouldn't become) real docs. **Gitignored by default** — add `context-v/extra/` to the repo's `.gitignore` when scaffolding. Corpus rollups and ingesters already exclude it by convention; the gitignore makes the privacy boundary structural rather than tooling-dependent.
- **`context-v/sitemap/`** — Maps of the project's own surfaces: pages, routes, slides, endpoints, screens — described as context docs so agents can reason about "what exists where" without crawling the source. First proven across the deck client-sites; applicable to any project with a navigable surface.

### Experimental tier (proposed, not yet consistent)

Folders the team is actively trialing. Their shape is **not settled** — expect variation between repos, and don't enforce consistency across them yet:

- **`context-v/loops/`** — Definitions of recurring operational loops: a loop's scope, cadence, per-iteration procedure, and exit conditions (e.g., a dependency-upgrade loop that fans out across sites until every build is green). Pairs naturally with agent loop-runners like Claude Code's `/loop` — the doc is the durable definition; the runner is the execution.
- **`context-v/handoffs/`** — Session-to-session handoff notes: the state of work captured at the end of a working session (what landed, what's mid-flight, what the next session must know) so a future session — human or agent, same person or a collaborator — resumes without re-derivation. The agentic-tooling world is converging on handoff documents as a primitive; this folder is where ours live.
- **`context-v/decisions/`** — Artifacts of clear decisions made: what was decided, when, by whom, and what alternatives were passed over. Supplements specs and plans by isolating the *decision itself* — a spec tells you the current state of intent, a decision doc tells you the moment intent changed and why. Kin to the industry's ADR (Architecture Decision Record) convention, but not limited to architecture.
- **`context-v/habits/`** — Recurring maintenance practices the team commits to performing, each named `Maintain <the thing> [across <the scope>]`. A habit answers *"what do we keep doing, and what fires it"* — the trigger, the procedure, and how far it applies (`applies_to` is the load-bearing frontmatter field). Two trigger shapes are in use: **event-driven** (update the README when a change makes it untrue) and **periodic sweep** (walk every `context-v/` promoting stale `status:` values). **Distinct from `reminders/`:** a reminder is a correction — *when you do X, do it this way* — and fires only when you happen to be doing X. A habit is an obligation — *do X, on this trigger, across this scope* — and fires whether or not anything reminded you. Most habits are addressed to the **agent** rather than the developer, and should say so explicitly.
- **`context-v/contracts/`** — Binding agreements, in two flavors that share one property: they are *not suggestions*. (1) **Constitution contracts** — standing rules agents must always follow, regardless of session, task, or model (invariants stronger than reminders: a reminder corrects drift, a contract defines the boundary of acceptable behavior). (2) **Interface contracts** — ironclad API-level documentation of how data must flow through the app or across a microservices architecture: schemas, payload shapes, ownership boundaries, who may write what. Where a blueprint explains *how the system is designed*, a contract states *what must never be violated*.

When creating either, follow the standard frontmatter baseline and note in the doc that the folder is experimental. When you see one shaped differently from this description, that's expected — surface the divergence, don't normalize it.

### When you find a folder outside the set

The set above is convention, not closed. Experimentation is normal — you'll encounter folders that don't match (observed in the wild: `narratives/`, `profiles/`, `inquiry/`, `models/`, `strategy/`, `notes/`, `research/`). Some are domain-specific and correct where they are: `narratives/` and `slides-content/` in deck workspaces, `profiles/` and `inquiry/` across the studies shelf. When you find one:

1. **Don't fight it.** Read what's there.
2. **Identify the cognitive mode** (planning / reflection / journey / something new).
3. **Discuss with the user** whether the folder should be assimilated (promoted to a new convention — the path `plans/` and `agent-skills/` took), folded (contents moved into an existing folder), or kept as project-specific.
4. **Default to keeping it** if unsure. Re-organizing someone's mental model mid-session is rude.

## Conventional Frontmatter

Frontmatter in `context-v/` is **scattered in practice** — some files have lots of properties, some have very few. When creating new files, lead with this baseline:

```yaml
---
title: "Human-readable title"
lede: "Subtitle-length hook — 140 chars max, two rendered lines."
publish: true
date_created: YYYY-MM-DD
date_modified: YYYY-MM-DD
date_authored_initial_draft: YYYY-MM-DD
date_authored_current_draft: YYYY-MM-DD
authors:
  - Author Name
augmented_with:
  - Claude Code on Claude Opus 5
at_semantic_version: 0.0.0.1
status: Draft
tags:
  - Relevant-Tag
  - Another-Tag
---
```

When editing existing files, **respect what's there**. Don't add fields the file didn't have unless they're genuinely useful. Don't remove fields you don't recognize.

### The three date families — and why `context-v/` needs all of them

This is the part agents get wrong, and it matters more here than anywhere else in the tree: **`context-v/` documents constantly evolve.** A spec is revised across months; a plan accumulates phases and post-ship notes; a blueprint gets superseded. Telling a doc that moved last week from one stable since spring is the whole job. That is why the vocabulary is broad.

| Family | Keys | Source of truth | Answers |
|---|---|---|---|
| **Filesystem** | `date_created`, `date_modified` | `stat` | "When did these bytes appear and last change?" |
| **Editorial** | `date_authored_initial_draft`, `date_authored_current_draft`, `date_authored_final_draft` | A human's judgment about the content | "When was this really written, last meaningfully revised, and finished?" |
| **Lifecycle** | `date_first_published`, `date_last_updated` | The work, not the file | "When did it ship? When was it last touched at all?" |

Filesystem dates lie in both directions, which is exactly why the editorial pair exists:

- `date_modified` **overstates** recency. Obsidian bumps mtime just for *opening* a file. A doc untouched in substance for months shows yesterday.
- `date_created` **can overstate** age-of-origin. A machine recovery in this tree reset birthtime on a batch of files to the recovery date. **Where frontmatter records an earlier `date_created` than the filesystem, the frontmatter is the more accurate record — never overwrite it with `stat`.**

Corollary when deriving a missing `date_created`: if the file has a `date_authored_initial_draft`, prefer it over filesystem birthtime. A document cannot be created *after* its own first draft.

`date_authored_final_draft` is often **present but deliberately empty** — that means "not final yet." Do not delete the empty key.

### Key migrations

Legacy spellings being renamed as files are touched. Preserve the value verbatim; change only the key:

| Legacy | Current | Note |
|---|---|---|
| `created:` | `date_created:` | |
| `date:` | `date_authored_initial_draft:` | Mostly on changelog entries |

### `at_semantic_version` — standard spelling, with a permanent alias

**Write `at_semantic_version`.** It is the standard and what every new doc and template uses (~4,140 files).

**`semantic_version` is an accepted alias for the same property and the same value** (~330 files). It is *not* a legacy spelling awaiting migration — **there is no sweep planned and none is wanted.** Anything that reads the field reads both names and treats them identically; that costs a renderer one extra key lookup and saves rewriting hundreds of files for zero gain.

So: write `at_`, read either, and **never rewrite an existing file just to change the spelling.** If you're touching a file for other reasons and it says `semantic_version`, leave it.

Key conventions (full details in `references/frontmatter-spec.md`):

- **All property names are `snake_case`** — enforced by Obsidian's frontmatter rendering. Never camelCase or kebab-case keys.
- **`publish`** is a boolean and it is a *decision*. `false` means a stub, a title with nothing under it, something deliberately held back, **or anything a stranger shouldn't see**. **If the key already exists, never flip it** — especially never `false` → `true` because a doc "looks long enough." Judging it on an existing file means **reading the file**: a stale "Stub" banner over a developed body is `true`; a polished title and lede over placeholder sections is `false`.
- **Avoid disclosing what could be considered sensitive** — and prefer **genericizing over hiding.** Most `context-v/` work should be published; that's how the practice spreads. But write generically about specifics that aren't yours to share: name a client only when it adds something (it usually doesn't), keep PII and a client's proprietary frameworks and confidential deal terms out, and never paste a live credential *value*. Variable and env-var names, architecture, schemas, and our own candid post-mortems are all fine — over-screening makes the corpus useless. **The document's job comes first:** if it is materially better with the specific names in it, keep them and set `publish: false` — it stays in the repo for us, which is what `context-v/` is for. Never water a document down for a publication that was never going to happen. See *Avoid disclosing what could be considered sensitive* in `references/frontmatter-spec.md`.
- Update `date_modified` whenever you edit the file — but bump `date_authored_current_draft` only on a **substantive** revision, and move `at_semantic_version` with it
- `at_semantic_version` is **four-part `epoch.major.minor.patch`** — see `references/versioning.md`. `semantic_version` is a permanently-accepted alias for the same property and value: **write `at_`, read either, never rewrite a file to change which one it uses.**
- **Never delete a frontmatter key you don't recognize.** The vocabulary is broad on purpose — different surfaces read different keys, and the cost of carrying an unused one is zero. Not knowing what a key does is a reason to leave it, not to remove it.
- `authors` is **humans only**, always a list. AI agents are tracked separately under `augmented_with` (format: `Pi on Claude Sonnet 4.5`). See `references/frontmatter-spec.md`.
- `tags` use **Train-Case** values (e.g., `Markdown-Rendering`, `Issue-Resolution`) — Obsidian convention
- `status` uses **Train-Case** values too — it's a display string, not a machine enum
- `lede` (or `description`) is optional on any doc-type — a newsroom hook for preview cards / OG snippets / list views. **Keep it subtitle-length** (see *Lede length discipline* below).
- `date_work_started` / `date_work_completed` are optional and record **when the work happened**, not when the document was written. For a spec or plan these come apart hard — a plan is written before the work, revised during it, and the work finishes long after the last edit, so none of the four dates is derivable from another. `date_work_completed` normally gets set in the same edit that moves `status` to `Shipped`. **Omit rather than guess, and do not backfill.** See *Work dates vs. document dates* in `references/frontmatter-spec.md`.
- `site_uuid` and `hex_code` are **write-once identity fields — mint them on every new file.** `site_uuid` is a lowercase v4 UUID; `hex_code` is 6 chars of `[a-z0-9]` and serves as the doc's own citation ID (`[^a4f2c1]` inline → `[^a4f2c1]: [[Filename-to-Reference]]` in `## References`). They exist because `[[Filename]]` is already ambiguous — one blueprint in this tree resolves to eight files across originals and roll-ups — and because Chroma/Graphiti/SurrealDB need a key that survives re-ingest and renames. **Always generate with a command, never type one:** `uuidgen | tr 'A-Z' 'a-z'` and `LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c6`. Seven model-typed UUIDs in this tree contain non-hex characters. Full rationale, the collision math, and the never-sweep-roll-ups rule: `references/frontmatter-spec.md`.
- `summary` is optional and **agent-facing** — the counterpart to `lede`, not a longer version of it. `lede` earns a human's click and flows into OpenGraph automatically; `summary` tells an agent what the doc is *for*, where it sits in the workflow, and what downstream logic consumes it. Worth writing on anything an agent has to *triage* — specs, blueprints, handoffs, issues. See *`lede` vs. `summary`* in `references/frontmatter-spec.md`, which also covers the legacy-alias trap (some repos used `summary` to mean `lede`).

## The `lede` property — what it's for

**`lede` exists because `title` and `description` each fail at a different half of the job.**

- **`title` says what the thing *is*.** That's its job and it does it well — but knowing what something is rarely makes you want to open it.
- **`description` is always too long and too boring.** It's a summary, written for completeness. On a card it wraps to five lines and nobody reads past the second.
- **`lede` says why you'd care, in a glance.** Short enough to render, interesting enough to earn the click.

This is why the field is called `lede` and not `description` — the word is a newsroom instruction. *Write something that grabs attention.*

**It's a rendering field, first and foremost.** Content cards, list views, index pages, search results, and OpenGraph/social previews all need one line of prose under the title, and they need it to be *good*. A doc with a great body and no lede renders as a bare title in every one of those surfaces. A doc whose lede is a truncated description renders as noise. Both are worse than they need to be, and the fix costs one sentence.

Practical consequence: **if a doc will ever appear in a list, it wants a lede** — which in this tree is most of them, since `context-v/` renders publicly through Astro Knots sites and the corpus splash.

## Lede length discipline

**The lede is a subtitle, not an abstract.** It's the single line a reader sees in a list view, a preview card, or an OpenGraph snippet before deciding to click. Its whole job is to make them want to keep reading — and a hook that runs long has stopped being a hook.

The rule: **140 characters maximum, target 90–130 — two rendered lines, never three.** A hard budget, not a guideline. Write ONE clause that lands, not a sentence with a subordinate clause trailing off it. If you can't say it in a subtitle, the lede isn't the place — the material belongs in the body.

**Why a number and not "a few sentences."** Prose guidance does not constrain a writer, human or agent. A 2026-08-17 sweep briefed against the old "~3 rendered lines" wording produced 55 ledes averaging 370 characters — every one of them good prose, every one of them clipping mid-sentence in an OpenGraph unfurl, and all of them rewritten. Give the budget as a count.

**The one thing worse than a long lede is a vague short one.** Never trade specificity for brevity. "A profile of Qdrant, a vector database" is under budget and worthless. If a document genuinely resists a 140-character hook, surface that rather than papering over it.

When you feel the lede wanting to grow — to carry the full context, the journey, the stakes, the file inventory — that's the signal to **start a `## Why Care?` section directly under the title** (or an equivalent context/intro section) and put the long version there. The body is unbounded; the lede is not.

```
✅  lede: "The single org slot becomes an open-ended stack of affiliation
          cards — pick an org once instead of retyping it on every person."

❌  lede: "Yesterday the surface held one org per person, which was a lie about
          how careers work because people sit on boards and advise and change
          jobs and keep past titles, so tonight we … [200 more words]"
          ← this is a Why Care? section wearing a lede's clothes
```

This mirrors the audience cascade the `changelog-conventions` skill codifies: **lede = the two-second hook; `Why Care?` = the paragraph that earns the scroll.** Same discipline, every doc-type — specs, explorations, blueprints, issues.

### A lede is written, never extracted

**No script can generate a lede.** It is the one frontmatter field that requires having read the document and judged what is interesting about it. Every other field can be derived from the filesystem, the filename, git, or another key. This one cannot.

A generated-then-abandoned lede is worse than no lede, because it renders as garbage on exactly the surfaces the field exists for — list views, preview cards, OG unfurls. Real failure signatures found in this tree, all from one extraction pass:

| Symptom | What went wrong |
|---|---|
| `lede: "---"` | Captured a horizontal rule instead of prose |
| `lede: "…allows each firm (e.g."` | Sentence-splitter broke on the period inside `e.g.` |
| `lede: "…12Ps-scorecard."` | Split on a period inside a filename |
| `lede: "Added a set of CLI tools to tighten the workflow:"` | Lifted a sentence that introduces a bullet list, trailing colon and all |
| `title: "Summary"` / `title: "Overview"` | Took the first `##` rather than the document's subject — four docs ended up sharing one title |

**Repairing one is a content edit, not a normalization** — it changes an existing value, so it falls outside an additive-only sweep and needs its own directed pass. To do it: read the document, find the most interesting or surprising thing in it, and write one to three sentences that make someone want the rest. The raw material is nearly always already in the body — a `## Summary` opener, a problem statement, a concrete number. Prefer the specific over the categorical.

**If the document is a genuine stub, leave the lede empty.** An empty lede on an empty document is accurate; inventing a hook for content that doesn't exist is fabrication, and it reads as a promise the page can't keep.

## Status discipline

The `status:` field is the load-bearing signal of where a document sits in its lifecycle. A directory full of `status: Draft` plans, half of which actually shipped, is a directory you can't trust. **Status reflects reality** — promote it as work lands.

Canonical values (Train-Case display strings, not machine enums):

`Draft` → `In-Review` → `Signed-Off` → `Implementing` → `Shipped` · `Partially-Shipped` · `Deferred` · `Stale` · `Superseded` · `Archived`

Companion fields that must move with status:

- **`Shipped`** — set `date_first_published: YYYY-MM-DD`; optionally `post_ship_note:` for things learned after ship.
- **`Partially-Shipped`** — set `date_first_published:` for the first shipped slice; append a `## Remaining work (as of YYYY-MM-DD)` section enumerating what's done and what's left.
- **`Deferred`** — set `deferral_note:` explaining the named reason.
- **`Superseded`** — set `superseded_by: [[Successor-Doc]]`.

In every case, bump `date_last_updated` (or `date_modified`) on the same edit. Status changes are meaningful edits.

**When to update:** when you ship a substantial portion, defer explicitly, supersede, or notice the field doesn't match reality during a sweep.

**When NOT to update:** mid-session as a side effect of unrelated work (drift policy — surface, don't silently normalize); for docs authored by someone else whose ship state you're not sure about (ask first); as a way to "tidy up" without a real ship event to point at.

Full reference: `references/status-discipline.md`. The periodic sweep procedure: `lossless-monorepo/context-v/habits/Maintain-Status-Discipline-Across-Context-V-Files.md`.

## Cross-references

Cross-referencing is how humans and agents focus on a limited scope at any moment — **humans have context windows too.** Three styles, all valid:

1. **Obsidian-style backlinks (preferred):** `[[path/to/Filename.md]]` or `[[Filename]]`
2. **Standard Markdown links:** `[link text](../specs/Some-Spec.md)`
3. **Backtick paths:** `` `context-v/specs/Some-Spec.md` `` for references the reader isn't expected to click

Use whichever serves the reader. Backlinks are preferred because most `context-v/` directories are symlinked into Obsidian vaults, where `[[wikilinks]]` unlock graph view, autocomplete, and backlink panes.

Common linking patterns:

- prompts → link the spec they implement
- reminders → link the blueprint that explains the pattern
- explorations & issues → link whatever they relate to

## Audience: User + Agent + Reader

Almost everything in `context-v/` is destined for public web publishing through one of the Lossless [Astro Knots](https://www.lossless.group/projects/gallery/astro-knots) sites. So every document balances three audiences:

1. **The User** writing or editing it
2. **The Agent** that will load it as context in some future session
3. **The Reader** who lands on it on the web with no prior context

Practical implications:

- **Lead with marketing. Lead with why. Lead with something anyone can understand.** Get into technical detail deeper in the doc.
- **The first paragraph should be readable by an outsider.** The rest can be specialized.
- **Fork early; don't wait for "too long."** Long-context-window models (Opus 4.7 with 1M tokens, etc.) can technically ingest huge documents — but **creativity, cross-referencing, and human-agent cooperation all degrade as a single doc grows**, regardless of what the model can accept. The trigger to split is *anxiety about length*, not a word count: when you (or the user) notice you're scrolling past sections to reach the one that matters, that's the cue. The practice is **fork-and-cross-reference**, not "split when forced." Pre-emptively factor self-contained sub-systems into sibling specs, reusable patterns into blueprints, and specific debugging journeys into issues — each linked from the parent. The parent doc keeps the *map*; the children carry the *detail*. See `references/philosophy.md` for the longer rationale.
- **Common split shapes when forking:** marketing/why stays at the top (or its own short doc), pattern/architecture → blueprint, thing-being-built → spec, how-to-build-it → prompt. Whatever fits.

## Filename conventions

Use **Train-Case** for filenames: `Train-Case.md`. Same convention as tags. Matches existing examples like `When-Claud-Code-and-When-Pi.md`, `Migrating-Study-to-its-own-Pseudomonrepo.md`.

## Decision tree: which folder?

- Defining what to build, with criteria & scope? → **specs/**
- Sequenced, scoped work plan (plan-mode output, roadmap, migration sequence)? → **plans/**
- Step-by-step implementation prompts referencing a spec or plan? → **prompts/**
- Capturing how/why a system is designed (pattern, architecture)? → **blueprints/**
- Short correction the AI keeps needing? → **reminders/**
- Executable know-how an agent should load and follow (SKILL.md shape)? → **agent-skills/**
- Don't know the answer yet, need to research/weigh options? → **explorations/**
- Debugging a specific painful problem and capturing the path? → **issues/**
- Scratch, pasted transcripts, not-a-doc-yet material? → **extra/** (gitignored)
- Mapping the project's own pages/routes/slides/surfaces? → **sitemap/**
- Recurring operational loop definition? → **loops/** (experimental)
- End-of-session state capture for the next session or a collaborator? → **handoffs/** (experimental)
- Isolated record of a decision made — what, when, why, alternatives passed over? → **decisions/** (experimental)
- Recurring practice with a trigger and a scope — *"we keep doing X"*? → **habits/** (experimental)
- Inviolable rule — agent constitution or ironclad data-flow/API contract? → **contracts/** (experimental)

When in doubt, see `references/doc-type-guide.md`.

## Templates

When creating a new file, start from the matching template in `templates/`:

- `templates/spec.md`
- `templates/prompt.md`
- `templates/blueprint.md`
- `templates/reminder.md`
- `templates/exploration.md`
- `templates/issue.md`

## Typical flow for a `context-v/` task

Not a checklist — a default rhythm. Adjust to the situation.

1. **Locate the project's `context-v/`.** Walk up from cwd if needed. Some repos have multiple (e.g., one per sub-project).
2. **Survey what's there.** Look at sibling files for tone, depth, and frontmatter conventions. Match them.
3. **Pick the folder** using the decision tree. If nothing fits, see *When you find a folder outside the set* above.
4. **Copy the matching template** from `templates/` if helpful, or write from scratch matching nearby files.
5. **Frontmatter:** today's date for both `date_created` and `date_modified`. Start at `0.0.0.1`. Add the user as author. If you (an AI) contributed materially, add yourself under `augmented_with` (e.g., `Pi on Claude Sonnet 4.5`) — not under `authors`.
6. **Lead with the why.** First paragraph readable by an outsider.
7. **Cross-link** to related docs using `[[wikilinks]]`.
8. **Filename & tags:** Train-Case (`My-New-Doc.md`, tags like `- New-Pattern`).
9. **When editing an existing doc:** bump `semantic_version` per `references/versioning.md` and update `date_modified`. Respect existing frontmatter shape.
10. **If the doc is ballooning, propose a split** before continuing. Better two clean docs than one bloated one.

## Developing a spec (the rich case)

Specs have more rhythm than the other doc-types: stub-first, discuss-then-write, handle stale prior art without hijacking the primary dialog, sign-off gate before implementation, narrative pass *after* sign-off, and pair with prompts for chunked execution. The full rhythm lives in `references/developing-a-spec.md` — load it whenever you're initiating or developing a spec with the user.

## The philosophy (tl;dr)

- AI doesn't learn between sessions → externalize memory as loadable docs
- Context windows have limits (humans too) → modular docs designed for selective loading and cross-linking
- Specs align everyone again, better → AI makes specs cheap to write and cheaper to keep current
- We publish in public → docs serve users, agents, and outside readers simultaneously
- Norms over rules → generative first, consistency emerges with attention

For the deeper version, see `references/philosophy.md`.
