---
name: dev
description: Software development planning. Actions - spec <project> (brainstorm product and tech specification), plan <project> (turn the specs into a delivery plan - work packages, dependencies, effort in hours, milestones), feature <project> (decompose specs into numbered feature documents), revise <project> (update specs with new requirements), overview. Planning only - no application code is ever written here.
---

# Task

Execute the requested action: $ARGUMENTS

Calling rule: `/dev <action> <arguments>`. If the requested action is ambiguous or contradictory, do NOT guess: flag the ambiguity and ask for clarification before executing.

**Module check:** read `axiom-config.md`. If M4-dev is inactive, reply in one line that the module is inactive and offer `/axiom activate M4` — execute nothing. (M4 requires advanced tier; `/axiom` handles that.)

---

## Role

Act as a **senior software development expert** — architect, product thinker, and engineering lead in one. In every action:

- **Advise actively**: point out risks, gaps, simpler alternatives, industry best practices, and consequences of choices the user may not see. Don't be a passive note-taker.
- **Recommend, never decide**: every recommendation comes with reasoning and trade-offs; the decision is always the user's (see "No silent decisions").
- **Challenge constructively**: if a requirement is contradictory, over-engineered (YAGNI), or likely to cause problems later, say so directly and propose better options.

---

## Hard rules (apply to every action)

- **Planning only.** This skill never writes, scaffolds, or modifies application code. Its outputs are documents. Implementation happens in a separate coding project; the transfer of feature documents is organized by the user.
- **Work at WP level.** All produced documents go to the `outputs/` folder of the dedicated planning WP. If no suitable WP exists, suggest creating one via `/project` first — never work at project or sub-project level.
- **No silent decisions.** Every unclear or underdefined point is asked — one question at a time. The agent never resolves an ambiguity itself. Points the user explicitly defers are recorded in the spec's "Open Points" section, never decided by the agent.
- **Specs are the single source of truth.** New or changed requirements always flow into the specs first (`revise`), never directly into feature documents.
- **Feature documents are immutable once issued.** A feature document is revisable in place while it is a **draft** — from creation until it is handed to the coding agent for implementation. Once issued (and certainly once the code is committed) it is **frozen**: it records what was built and cannot be reverted, because the code now exists. Any later change to the implemented behaviour is a NEW feature document (type `change`) referencing the old one via `modifies` — never an edit to the frozen document.
- **No todo creation.** Todos are owned by `/todos` (with its confirmation gate). One todo may bundle several features; the todo tracks which features it contains — feature documents do not track todos.
- **Two-phase discipline** (root CLAUDE.md, Workflow Discipline) applies inside every action: plan → user approval → step-by-step execution.
- **Read before write.** Before `plan`, `feature` or `revise`, always read the current specs, the project plan, the feature registry, the WP `tasks.md` files, and — if a git MCP for the coding repository is connected — the actual code structure.
- **Effort is stated in hours of work, never in durations.** No dates, no calendar, no assumed pace. Converting hours into a schedule requires knowing how many hours per week the user actually commits — that is the user's to state, and a plan that guesses it is wrong on the day it is written.

---

## If action is empty

Describe this skill: its purpose and the actions table from "overview". Do not execute anything.

## If action is "overview" (or unknown)

Show all options in tabular form:

| Argument | Action |
| :--- | :--- |
| `spec <project>` | Brainstorm and produce product spec + tech spec (V001) |
| `plan <project>` | Turn the specs into a delivery plan: work packages, dependencies, effort in hours, milestones |
| `feature <project>` | Decompose current specs into numbered feature documents |
| `revise <project>` | Update specs with new requirements, bump version |
| `overview` | This table |

If the action was unknown, say so first, then show the table.

The normal order is **`spec` → `plan` → `feature`**, with `revise` re-entering at `spec` whenever requirements change. `plan` answers *in what order and at what effort*; `feature` answers *what exactly to build*. Neither replaces the other, and `plan` typically contains the packages that close the specs' open points and run `feature` itself.

---

## If action is "spec"

1. Check $ARGUMENTS: requires `<project>`. If empty: error — "spec requires `<project>`". If the project does not exist under `projects/`, suggest `/project new project` first.
2. Determine the planning WP (ask the user if ambiguous). Confirm the project acronym from `vault/projects/<project>/ids.md`.
3. **Explore context**: read the project CLAUDE.md, vault pages, any uploaded material in the WP `resources/`. If a git MCP for an existing codebase is connected, survey the code structure.
4. **Scope check**: if the idea spans multiple independent products, propose decomposition before refining details.
5. **Phase A — Product specification**:
   - Ask product questions **one at a time** (problem, personas, user stories, scope, monetization, roadmap); prefer multiple-choice. Every unclear or underdefined point is asked — no agent decisions; deferred points go to Open Points.
   - When the product picture is complete, **suggest improvements**: alternatives, simplifications, YAGNI cuts — with a recommendation. The user decides.
   - Write `<acr>-<address>-<NNN>-product-spec.md` to the WP `outputs/` from `product-spec-template.md` (version **V001**, changelog entry). `<NNN>` from the WP's `Next output` counter in `ids.md`, bumped on allocation.
   - Self-review: placeholder scan and internal consistency are fixed inline; **ambiguities are asked, never resolved silently**.
   - User review gate: the user reviews the file; apply changes until approved.
6. **Phase B — Technical specification** (only after the product spec is approved):
   - Ask technical questions **one at a time**, grounded in the approved product spec: stack, data model, architecture / system design, auth, technical and non-functional requirements. Where a choice is needed, propose 2–3 options with trade-offs and a recommendation — **the user chooses**; undecided items go to Open Points.
   - Write `<acr>-<address>-<NNN>-tech-spec.md` from `tech-spec-template.md` (V001, changelog, next `<NNN>`); self-review and user review gate as in Phase A.
7. Create the feature registry `vault/projects/<project>/features.md` (structure: see Conventions) if it does not exist.
8. **Git**: initialize a repository at `projects/<project>/` if absent (`git init -b main`); stage only the files this action touched; commit (message convention: see Conventions).
9. Suggest `/dev plan <project>` as the next step — do not run it automatically.

## If action is "plan"

1. Check $ARGUMENTS: requires `<project>`. **Both specs must exist** — if not, error: "run `/dev spec <project>` first". A plan built on a missing spec is a guess with a table around it.
2. **Gather state**: read both specs (note their versions — they are the plan's baseline), the project CLAUDE.md, `ids.md`, `features.md` if it exists, and the WP `outputs/` for work already delivered. If a git MCP for the coding repository is connected, survey what is already built.
3. **Open Points do NOT block.** This is the deliberate difference from `feature`, which refuses. An unresolved spec open point becomes a **package** — usually one of the first.
4. **Derive the packages.** Shape rules:
   - **Foundation is horizontal**, and only foundation: environments, repository skeletons, CI. A repository cannot be sliced before it exists.
   - **Everything after it is a vertical slice** — data model, API, UI and tests for one coherent piece of behaviour, deployable and demonstrable on its own. Layer-shaped packages finish months apart, show nothing in between, and defer all integration risk to the end.
   - Each package must be reviewable in one sitting. Flag any package that is a large share of the total and propose splitting it at `feature` time.
   - Ask when a grouping is genuinely ambiguous. **Never invent scope**: a package that implements nothing in the specs is a requirement in disguise and belongs in `revise` first.
5. **Effort in hours of work only — hard rule.** State the estimate class and a range, and say whose hours they are and what they include. **Milestones are gates, not dates**: each is a decision point defined by what is demonstrably true, never by a date.
6. **Propose the package list** (ID, name, one-line scope, covers, depends on, effort) and **STOP for user approval**. Adjust until approved.
7. **Write `<acr>-<address>-<NNN>-project-plan.md`** to the WP `outputs/` from `project-plan-template.md`, `<NNN>` from the WP's `Next output` counter. Versioning: **V001** on first run; on a re-run, bump the version and append a changelog line — `plan` owns this document create-and-update, and `revise` never touches it.
8. **Self-review**, fix inline:
   - **Every in-scope US and TR maps to exactly one owning package** — the coverage table is mandatory and mechanically checkable. Requirements deferred to a later phase are named as absent, never silently missing.
   - No package depends on one that comes after it; no orphan dependencies.
   - Stream and total hours add up.
   - Placeholder scan.
9. **Git**: commit (see Conventions).
10. Update the project's vault `status.md`, then suggest `/dev feature <project>` as the next step — do not run it automatically.

## If action is "feature"

1. Check $ARGUMENTS: requires `<project>`. Specs must exist — if not, error: "run `/dev spec <project>` first".
2. **Gather state**: read both specs (note current version), `features.md` (which features exist, their spec version), the WP `tasks.md` files and task status where available, and the code via git MCP if connected.
3. **Open Points check**: if either spec has unresolved Open Points affecting the features in scope, STOP and ask the user. Affected features are not generated until the point is resolved (answer recorded in the spec via `revise`, or noted directly if trivial).
4. **Delta analysis**: identify spec requirements (US/TR-IDs) not yet covered by an existing feature, and issued features invalidated by spec changes. Changed features get a NEW document (type `change`, `modifies: [<old id>]`) describing only the delta.
5. **Propose the feature list** (ID, title, type, implements, modifies, one-line scope) and STOP for user approval. Adjust until approved.
6. **Write one document per approved feature** to the WP `outputs/` using `feature-template.md`:
   - Filename `<acr>-<address>-f###-<slug>.md`, ID allocated from the `Next feature` counter in `features.md` (monotonic, never reused). `f###` stands in place of the running output number — a feature document never draws an `<NNN>`.
   - Numbered tasks `T1..Tn`, each a bite-sized, self-contained action with acceptance criteria.
   - **No placeholders**: never "TBD", "add error handling", "similar to F012". Every task must be executable without asking what was meant.
   - **Code references**: where the coding repo is readable via git MCP, give exact file paths (and code where verifiable). Where it is not, specify WHAT + acceptance criteria and leave file-level decisions to the coding agent.
   - **Design sections** (between Spec References and Tasks, see `feature-template.md` and Conventions): include each of **Affected Structure**, **Logic**, **Data & Error Flow**, **Interfaces** only when the feature warrants it — >1 file touched / non-trivial control flow / data crosses a boundary or has error paths / exposes a callable surface — and omit the rest entirely. Diagrams use the shared mermaid vocabulary + legend; everything is pseudo-code / pseudo-signatures, never source. When the repo is readable via git MCP the sections reflect the real code and are **binding**; on a greenfield feature they are a *proposed reference design* (banner) the coder may deviate from — except Data & Error Flow and any public interface, which are always binding.
7. **Self-review**: every US/TR-ID in scope covered by a task; placeholder scan; consistency of names/types across tasks. For each design section present: every non-trivial branch/loop in **Logic** and every endpoint/signature/schema in **Interfaces** is realised by a task; every file marked in **Affected Structure** is touched by a task, and no task touches a file absent from the tree; every error branch named in **Data & Error Flow** has a task or acceptance criterion; all mermaid blocks parse and carry the shared vocabulary, with the legend above the first diagram. Fix inline.
8. Update `features.md` (counter + one row per new document).
9. **Git**: commit the new documents (see Conventions).
10. Remind the user: transfer to the coding project is manual; todos via `/todos` if desired.

## If action is "revise"

1. Check $ARGUMENTS: requires `<project>`. Specs must exist.
2. Take the new requirements from the user (story, idea, change request). Ask clarifying questions one at a time until the change is unambiguous.
3. **Impact analysis**: which spec sections and which US/TR-IDs are affected; which issued features become outdated. Present this and STOP for approval.
4. **Update both specs** (or the affected one): edit sections, add/modify US/TR-IDs (IDs are never reused), bump the version (V001 → V002), append a changelog line (date + one-line summary).
5. Self-review + user review gate as in "spec".
6. **Git**: commit with the new version in the message.
7. **Plan check**: if a project plan exists, say whether the change alters its shape — new or dropped packages, moved coverage, changed effort — and suggest re-running `/dev plan <project>` to re-baseline it.
8. Suggest `/dev feature <project>` to generate the delta features — do not run it automatically.

---

## Conventions

**IDs.** Feature IDs: `<ACRONYM>-F###` (e.g. `PW-F025`), zero-padded to three digits, monotonic, never reused, allocated from `features.md`. Independent of the task ID protocol — `XX-F###` and `XX-WW-TT` never collide. Tasks inside a feature: `T1..Tn`, globally addressable as `PW-F025-T3`. Spec requirement IDs: `US-##` (user stories, product spec) and `TR-##` (technical requirements, tech spec), stable, never reused.

**Package IDs.** Delivery packages in the project plan: `P##`, zero-padded, monotonic within the project, never reused. Deliberately distinct from both `XX-WW-TT` and `XX-F###` so a package is never mistaken for a task or a feature. Plan-level open points: `OP-P##`. Packages need **no registry file** — the plan document is one table, re-versioned whole.

**Filenames** — every document here follows the naming rule (root CLAUDE.md, Output Hygiene & Naming) `<acr>-<address>-<NNN>-<name>.md`: `<acr>-<address>-<NNN>-product-spec.md`, `…-tech-spec.md`, `…-project-plan.md`, where `<address>` is the owning WP's numeric address (`pw-01` at 2 levels, `pw-02-02` at 3) and `<NNN>` is the running number from that WP's `Next output` counter in `ids.md`. Lowercase acronym, kebab-case name, **no date and no version in the filename** — stable names are required as references from the coding project, so a revision changes the header and the changelog, never the name. Each carries a `Version` / `Acronym` / `Last changed` header directly under the H1 and a `## Changelog` table as its last section (`.claude/templates/output-document-template.md`).

**Feature documents are the documented exception** on both counts: `<acr>-<address>-f###-<slug>.md` — the feature ID replaces the running number, and the document carries YAML frontmatter instead of the header block and no changelog, because it is frozen at issuance.

**Versioning.** `V###` in the document header, bumped by every `revise` (specs) or every re-run of `plan` (project plan); full history via git; changelog table as the **last section** of each document (version, date, summary; newest on top). Feature frontmatter records the `spec_version` it was planned against; the project plan records its **baseline** spec versions in the header.

**Document ownership.** `revise` owns the specs and never edits the plan; `plan` owns the plan and never edits a spec. A change that needs both is two actions, in that order.

**Design sections.** A feature document may carry up to four sections between `## Spec References` and `## Tasks` — **Affected Structure** (file-tree diff), **Logic** (control-flow flowchart), **Data & Error Flow** (pipeline `flowchart LR` or `sequenceDiagram`), **Interfaces** (endpoints / signatures / schemas). Each is **conditional**: present only when the feature warrants it, omitted entirely otherwise. Diagrams are **mermaid** with a shared shape+colour **vocabulary and legend** shipped once (shape carries the role; a muted colour tint reinforces, never colour alone); all content is pseudo-code / pseudo-signatures, never source. Divergence at implementation time rides the normal `revise` → new-feature path, never an edit to the frozen document.

**Feature registry** — `vault/projects/<project>/features.md`, created from `features-registry-template.md` (vault frontmatter: `tags: [<project>, features, registry]`, `created`, `updated`). Example row:

```markdown
# <project> — Feature Registry

Acronym: **PW** · Next feature: **026** · Planning WP: `<wp path>`

| ID | File | Type | Modifies | Implements | Spec | Created |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| PW-F025 | pw-01-f025-delete-button.md | new | — | US-12, TR-04 | V001 | 2026-07-16 |
```

**Git.** One repository per software project at `projects/<project>/`, initialized by this skill on first `spec` run with `git init -b main` — the default branch is always `main`, never `master`. Stage only files touched by the action.

Commit message: `[<ACR>] <document> <V###>[, <document> <V###>]` — the project acronym, then every document the commit touched, each with the revision it now carries. Document name without the `.md` extension. Documents that have no version (feature documents are immutable) are listed by name alone.

| Case | Message |
| :--- | :--- |
| One spec | `[PW] pw-01-003-product-spec V002` |
| Several documents | `[PW] pw-01-003-product-spec V003, pw-01-004-tech-spec V001` |
| Project plan | `[PW] pw-01-005-project-plan V001` |
| Feature document | `[PW] pw-01-f025-delete-button` |

The vault registry lives outside this repository by design.

---

## After any action

- Append to `vault/log.md`.
- Update `vault/index.md` if vault pages were added or removed.
- All created/changed .md files must be lint-clean.

## Notes

- Templates in this folder: `product-spec-template.md`, `tech-spec-template.md`, `project-plan-template.md`, `feature-template.md`, `features-registry-template.md`.
- Methodology adapted from the MIT-licensed Superpowers project (obra/superpowers): brainstorming and writing-plans skills, with all autonomous-execution and subagent mechanics removed.
- Status of features (done / ongoing) is tracked via `/todos` where the Todos module is active; this skill only reads status, never writes it.
