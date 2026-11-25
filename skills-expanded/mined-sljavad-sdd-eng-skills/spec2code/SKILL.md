---
name: spec2code
description: Runs a project spec-first as small, linked, agent-readable files - discovery of every product and technical gray area, a product spec, numbered, testable FR/NFR requirements with a traceability matrix, a technical spec with ADRs and a researched stack playbook, a stepwise plan, then review with findings recorded in files, with a one-page small track for scripts and small tools. Keeps the specs living (later features are change folders merged when accepted), makes AGENTS.md - imported by CLAUDE.md - the entry point, and runs either one agent or a lead/coder loop that communicates through files, with the user approving every decision beyond the approved spec. Use when starting a new project or major feature, writing product or technical specs, requirements or ADRs, planning an implementation, setting up multi-agent or cross-tool work, handing work to another agent, or reviewing an implementation against its spec.
---

# Spec-driven development

Build the understanding before the code. The spec phases produce a **cook book**: a set of documents
complete enough that a different agent — on a different model, in a different tool, with none of the
conversation that produced them — can implement the project correctly, and split finely enough that it
loads only the pages its task needs.

That constraint is what makes this method worth the effort, and it is the bar every document is held
to. This skill builds on `software-engineer`, which applies throughout; load both. Use the project's
own refactoring or cleanup skill when one exists.

## The pipeline

```
0. Setup and discovery  mode, size, architecture; understanding, gray areas       → AGENTS.md, docs/adr/, docs/discovery/
1. Product              what and why                                              → docs/specs/01-product/
2. Requirements         what exactly, how well                                    → docs/specs/02-requirements/
3. Tech spec            how — with ADRs and the stack playbook                    → docs/specs/03-tech/, docs/adr/, docs/engineering/
4. Plan                 in what order                                             → docs/changes/CH-NNN-<slug>/plan/
   ─────────────── handoff gate ───────────────
5. Implementation       one agent, or the lead/coder loop                         → code, docs/changes/CH-NNN-<slug>/tasks/
6. Review               against the spec and the code-quality lenses              → docs/changes/CH-NNN-<slug>/reviews/  ⇄ 5
7. Close                user accepts; merge into the living specs; archive        → docs/specs/, docs/changes/archive/
```

**Phases 1-4 run to completion before any implementation code is written.** When the plan is done, stop
and hand it back. The user decides whether to implement here, later, or elsewhere.

**The specs are living.** `docs/specs/` always describes the system as it is — or, before the first
release, as it is being built. A later major feature is a *change*: its product, requirement and design
deltas, its plan, tasks and reviews live in its change folder, and are merged into the living specs when
the user accepts it (`references/changes.md`).

**Scale the ceremony to the change.** The full pipeline is for a new project or a major feature. A small
change needs no change folder and no separate plan: run software-engineer's product pass, add or
amend the affected requirements and design items in the living specs — ids, statements, the traceability
row, its Plan step cell naming the change as `YYYY-MM-DD-<slug>` — in the same edit as the code, and
report it as one step; that report is its record. In multi-agent mode the lead writes those items
into the living specs when it marks the step `done` (`references/multi-agent.md`). Heavy process on
small work is how spec-driven development gets abandoned. The project's own weight — its size,
architecture and the practices it uses — is decided once, at setup, with the user. A script, a
utility or a one-job tool takes the **small track** (`references/small-track.md`): one page and one
approval, in place of the pipeline.

## Ask the operating mode first

Before phase 1, ask whether the project runs with **one agent** or a **lead and a coder**, and in which
tools — a small-track project is single agent and is not asked; then, from discovery's answers,
propose its **size, architecture and practices**. Both are in
`references/setup.md`, and the user decides at gate 0. In multi-agent mode `references/multi-agent.md`
governs the loop: each agent is a separate session the user starts. **Never launch a subagent to write
code**, and never offer to.

## Every document is small, focused and linked

A single long specification is expensive for an agent to load and mostly irrelevant to any one task.
Every phase writes **a folder of small topic files**, authored that way from the start — each opening
with its header, cited by stable id, and reachable from `AGENTS.md` in two hops. The rules and the
`AGENTS.md` and `CLAUDE.md` templates are in
`../software-engineer/references/project/project-knowledge.md`.

- **Every plan step names the exact files it needs**, so nobody reads the whole bundle.
- **Each fact is written once; everything else links to it.** A result, a status, a rule or a decision
  copied into a second file drifts, and costs an edit every time it changes.

## Load the phase you are in

Read the files for the current phase, not all of them.

| Phase | Read |
|---|---|
| Small track | `references/small-track.md`, with `references/setup.md` for the mode, the size and `AGENTS.md` — not the phase files |
| 0 — Setup | `references/setup.md`, `../software-engineer/references/project/project-knowledge.md`, `../software-engineer/references/project/decision-records.md` for the architecture ADR; when choosing the architecture, the style files under `../software-engineer/references/architecture/` that `setup.md` names |
| 0 — Discovery, and at every gate | `references/discovery.md` |
| 1 — Product spec | `references/product-spec.md` |
| 2 — Requirements | `references/requirements.md` |
| 3 — Tech spec | `references/tech-spec-structure.md`, then `references/tech-spec-behaviour.md`; `../software-engineer/references/project/decision-records.md` for ADRs; `../software-engineer/references/principles/modern-practices.md` for the stack playbook; the other software-engineer references each step names |
| 4 — Plan | `references/plan.md` |
| A later change, any phase | `references/changes.md`, with that phase's file |
| Multi-agent work | `references/multi-agent.md` |
| 5 — Implementation | the plan step and the files it lists, plus `software-engineer` |
| 6 — Review | `references/review.md`, `../software-engineer/references/quality/review.md`, `../software-engineer/references/quality/security.md`, `../software-engineer/references/quality/testing.md` |
| 7 — Close | `references/changes.md` |

## The handoff contract

Every document satisfies all of these. A document that fails any of them is not finished, however long
it is.

- **Self-contained for its topic.** No "as we discussed", "the approach above", "the usual pattern", or
  reference to anything outside the repository. Other files are cited by id and path from the
  repository root.
- **No pronouns pointing at the conversation.** The reader was not there.
- **Every decision carries its reason** — in the document for a small one, in an ADR for a significant
  one. A decision without a rationale gets silently reversed by the next reader who prefers something
  else.
- **No `TBD`, no `etc.`, no "to be determined during implementation".** Either decide it, or record it
  in the gray-area register and cite its `Q-` id where the doubt sits — escalate, do not guess. An
  implementer must never have to invent a requirement.
- **Concrete over descriptive.** Not "store the amount" but the field, its type, its precision, its
  nullability, and its unit. Not "handle errors" but which error, what the caller sees, what is logged,
  what is stored.
- **Terms are defined once, in the glossary, and used consistently.** Two words for one concept is how
  two implementations of it get built.
- **Everything downstream of phase 2 cites requirement ids.** Components, flows, plan steps and
  review findings name the `FR-`/`NFR-` they serve, and the traceability matrix is the one place
  coverage is recorded.
- **Small and findable.** Within the size budget, opening with its header, in its phase's folder.

Before declaring a phase done, run this test: *if I handed only these files to a competent stranger, in
another tool, what would they have to ask me?* Every answer is a gap. Fix it, or record it in the
register.

## Working method for the spec phases

**Understand, then ask — as software-engineer's "Resolving ambiguity" describes, run as discovery**
(`references/discovery.md`): draft first and mark every inference, never invent a requirement to fill
silence, keep every gray area in the register until it is resolved, and list every `assumed` entry at
the next gate.

**Research, think, propose** — software-engineer's "Thinking beyond the ask". Ideas go to the
proposal register. **Hard rule: a proposal is never built until the user accepts it.**

**Write no implementation code during phases 1-4.** Sketching a type signature or a schema fragment
inside the tech spec is the spec; creating project files is not. Research is the exception: to check a
library's behaviour, or to put a real number on an NFR, build a throwaway probe in a scratch directory,
keep the number, and say that is what you did.

## Order matters, and so does separation

- **The product spec contains no technology.** No framework, no database, no library. If a sentence
  names one, it belongs in the tech spec. This keeps product decisions from being quietly driven by an
  implementation preference.
- **The requirements contain no solution language either**, and no requirement without a source in the
  product spec. They are the product spec made countable and checkable, not a second draft of it.
- **The tech spec contains no product decisions and no new requirements.** If writing it surfaces a
  product question — what should happen when two customers order the last item — that goes back to
  phase 1 and forward through phase 2. If it surfaces a missing requirement, add it in phase 2 rather
  than burying it in a design paragraph.
- **The plan contains no new decisions at all.** It is an ordering of work already specified. If a step
  needs a decision, the tech spec is incomplete; fix it there.

Each phase may send you back to an earlier one. That is the method working, not a failure — the cost of
going back one document is trivial compared with discovering it during implementation.

## Gates

The small track has one stop, the approval of its page (`references/small-track.md`); the gates below
are the standard track's.

**Gate 0 — after setup and the first discovery pass:** present the operating mode, the size,
architecture and practices proposed, the files created, the playback of your understanding, the
`assumed` entries, and the first batch of questions. Wait for the user's corrections
before writing the product spec.

**After each of phases 1 to 4: stop and present.** Summarize what the documents decide; list the
`assumed` entries for confirmation, the open questions, the ADRs awaiting a decision, and the new
proposals; ask for approval or corrections. Do not roll straight into the next phase.

**At the tech-spec and plan gates, run a pre-mortem first** (`references/discovery.md`) and present its
list with the summary.

**After phase 4: hand off.** State that the specs and plan are complete, where they are — `docs/specs/`
and the change folder — and what an implementing agent should read first. Do not begin implementing
unless the user asks you to; in multi-agent mode, the lead hands the first step to the coder only once
the user approves the plan and says to start.

**During implementation (phase 5):** work the plan step by step, in order. After each step, verify it as
the plan specifies, record the result in the step's *Result*, and mark it done in the progress table —
nothing else changes. Do not batch several steps and verify at the end, and do not improvise work that
is not in the plan — if the plan is wrong, say so and amend it. In multi-agent mode the loop in
`references/multi-agent.md` does this.

**Review (phase 6)** may be run by any agent the user chooses — the spec author, the implementer, or a
fresh one — in multi-agent mode, one working in the lead role. Write it so it works for a reviewer with
no context: it reads the files and the code. Findings are recorded to files, not just reported in chat,
so the loop survives a new session.

**Close (phase 7):** after the review is closed and the user has accepted the change, merge it into the
living specs and archive its folder (`references/changes.md`).

**From phase 5 on, "the next gate"** is the board's "Waiting on the user" list in multi-agent mode, or
the next step report in single-agent mode. **A phase the user skips** is recorded in `AGENTS.md` or the
change's proposal, and the checks that cite its ids are dropped for that work — never filled with
invented ids.

## Amending an approved spec

Specs drift. When implementation reveals the spec is wrong, that is a **finding against the spec**, not
a licence to diverge.

1. Stop and say what the spec got wrong, and propose the amendment.
2. With the user's yes, amend the document, keeping the superseded decision visible with the reason it
   changed — a superseding ADR where it was an ADR's decision. Do not quietly overwrite history; the
   rejected reason is what stops it being re-proposed.
3. Then continue.

Code that silently disagrees with an approved spec is the worst outcome of this method, because the
document is now actively misleading — worse than having no document.

## Anti-patterns

| Symptom | What it means |
|---|---|
| Spec full of `TBD` | Decisions deferred to whoever is least equipped to make them |
| One 900-line spec file | Every task pays to load all of it; split it by topic |
| The full pipeline on a weekend tool | The weight gets the method abandoned; propose the small track |
| Ten scenarios on one requirement | The spec enumerating what the tests should; keep the examples to the edges |
| A monolith chopped into parts afterwards | Fragments that cut across topics; design files for how they are loaded |
| `AGENTS.md` importing specs, or restating the directory tree | Everything loads at startup, and the tree was derivable anyway |
| A step that says "see the tech spec" | The implementer reads everything; name the files |
| A step that copies spec text, or a result copied into a second table | Two sources of truth; the copy drifts |
| Tech spec naming no versions | "Latest" is not reproducible |
| Decision rationale in the tech spec as well as the ADR | Two places to update; one will be stale |
| An accepted ADR edited in place | The rejected reasoning is lost; supersede it instead |
| A proposal that is already implemented when presented | Scope taken, not asked |
| Living specs describing a feature not yet built | Readers can no longer trust them; that is what the change folder is for |
| A change closed without merging its deltas | The living specs now lie about the system |
| The lead writing code, or the coder editing specs | Ownership broken; neither file can be trusted |
| A review round that adds new requirements | Moving goalposts; the loop never ends |
| Flow with only a happy path | The failure behaviour will be invented under pressure |
| Integration test against an in-memory substitute | Passes exactly where production fails |
| Plan step verified by "it builds" | Not a verification |
| Plan step that touches "wherever needed" | The component inventory is incomplete |
| Product spec naming a database | Solution chosen before the problem was stated |
| A step whose result is checked three steps later | Wrong step boundaries |
| Findings reported only in chat | Lost at the end of the session |
| "The implementer can decide" | Either specify it or record it as a question — escalate, do not guess |
| NFR with no number | A wish; it will be declared met by whoever is asked |
| A `Must` requirement with no plan step | Unimplemented, and invisible without the matrix |
| Requirement with no product-spec source | Invented scope, or an incomplete product spec |
| An NFR category left silent | Not "not applicable" — just undiscovered until production |
| "Verified" on an NFR whose mechanism was checked but outcome was not | Two different claims |
