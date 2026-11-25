---
name: feature-forge
description: >
  Plan and land a feature that integrates an external service across
  several repos you already own. Pins the cross-repo contract before any
  repo codes against a guess of it, grills that contract against
  money-and-trust failure modes, builds the verification harness before
  the handler, and blast-radiuses the seams instead of the diffs.
  Generates a per-feature EXECUTION-STEPS.md with resolved absolute
  paths. Use for "integrate <provider> across our repos", "plan this
  feature end to end", "coordinate this across N repos", or
  /feature-forge.
---

# Feature forge

For integrating an external service (payments, auth, messaging,
analytics) into an existing multi-repo system, where several repos must
agree on one contract.

Not for greenfield platform work (a fresh PRD-to-build pipeline); use
`platform-pipeline` for that. This
skill assumes the repos exist, the domain is known, and the hard part is
the seam between them.

## What actually makes this work

Three moves carry the whole workflow. The stage list is scaffolding
around them. If you skip one of these, the stages will not save you.

1. **Contract before code, grilled before committed.** Stages 3-4. The
   failure this prevents is four repos independently guessing at a
   shared shape and reconciling later, after the guesses are load
   bearing.
2. **Verification harness before the build, not after.** Stage 8. You
   cannot retrofit proof of idempotency. The ability to fire duplicate
   and out-of-order events has to exist before anyone writes the
   handler, or "it works" means "it worked once, in order".
3. **Blast-radius at seams, not at diffs.** Stage 10. Cross-repo
   breakage is exactly the class grep cannot see: a status enum
   remapped in one repo, a field read by another, a wire shape a third
   parses loosely.

## The deliverable

The first output is not code. It is
`<plan-root>/EXECUTION-STEPS.md`: a per-feature step sheet with every
path resolved absolute, one copy-pasteable prompt per stage, and a
skill-availability table for the tools in play.

Generate it from `references/stage-prompts.md`, filling every
placeholder from the interview in stage 0. A sheet with an unresolved
`<repo>` in it is a draft, not a deliverable. Paths must be absolute so
the sheet works from any working directory and from either tool.

See `references/worked-example.md` for a completed sheet.

## Stage 0 — Interview, then resolve

Answer from the filesystem. Ask the user only what you cannot observe.

- **Repos.** Which repos are in play, at what absolute paths, and what
  does each own in this feature? Name the one that owns privileged
  mutations; it is usually where the contract's hard half lives.
- **Prior art.** Is there an existing plan, spec, ADR, or issue set
  covering this? Read it before writing anything. A plan written
  provider-agnostic often survives a provider decision almost intact,
  and resuming it beats restarting.
- **Provider.** Which external service, and is it decided or still
  open? If open, stage 2 is a comparison, not a fact-gather.
- **Store or platform constraints.** Does any surface fall under app
  store rules, regulated payments, or data residency? These constrain
  the design before it exists, not at review.
- **Skill availability.** Which skills exist in which tool (Claude Code,
  Codex, others). Record it in the sheet. A prompt naming a skill the tool
  lacks wastes a turn: use the fallback from the table below instead.

## Dependencies and fallbacks

Each stage names a skill. None ships with this pack, and the workflow
works without them: the fallback is what the stage must still produce.

| Stage | Skill | Where to get it | Fallback when it is missing |
|---|---|---|---|
| 2 | `research` | mattpocock/skills | Web research from the provider's own docs, API reference and changelog, with citations, written to a file |
| 3 | `codebase-design`, `domain-modeling` | mattpocock/skills | Write the contract by hand, covering every item listed in stage 3 |
| 4 | `grilling` | mattpocock/skills | Answer each failure mode in stage 4 yourself, in writing, with a named state and owning repo |
| 5 | `to-tickets` | mattpocock/skills | Write the tickets by hand with the fields listed in stage 5 |
| 6 | `design`, `prototype` | a design skill or tool of your choice; `prototype` from mattpocock/skills | Wireframes or screenshots of the affected surfaces. Backend-only features skip with a reason |
| 8 | `create-verification-skill` | cursor/plugins | A script that fires duplicate, out-of-order and badly signed events at the handler and prints stored state before and after |
| 10 | `blast-radius` | cursor/plugins | Trace each seam by hand and run real code to prove the safety fact |
| 11 | `security-review` | built into Claude Code | Work through the stage 11 checklist by hand |
| 12 | `code-review`, `simplify` | mattpocock/skills; `simplify` is built into Claude Code | Any careful review pass per repo |

## Stages

Copy these into the todo list verbatim. A stage you skip stays listed
with `skip: <reason>`.

1. **Frame against prior art.** Read the existing plan and every issue
   file in full. Classify each as still-valid, needs-revision, or
   already-answered by the decision now made. Name any standing
   decision the new provider actually invalidates. Rewrite nothing yet.
2. **Provider facts.** The `research` skill, primary sources only, with
   citations. Always cover: the provider's own state enum and its
   transitions, its webhook event set and delivery guarantees
   (ordering, duplication, retry, signature scheme), what custom data
   can ride a request so a callback maps back to your entity, what the
   provider's own portal self-serves, and where its responsibility
   ends. Write it to a file; later stages cite it.
3. **The contract.** The `codebase-design` skill. This is the stage
   that pays for the rest. Decide and write, as one authoritative doc:
   the document or table shape that is truth; your internal status enum
   and the exact mapping from the provider's, naming every state with
   no clean mapping; how a request binds to your entity before the
   external system knows about it, and how the callback resolves back
   with no ambiguity; the idempotency scheme (what the key is, where it
   lives, what happens on duplicate and out-of-order); how downstream
   surfaces read the resulting state, server-authorized; and per repo,
   what it owns and what it is forbidden from writing. Use
   `domain-modeling` first if the vocabulary is not yet pinned.
4. **Grill the contract.** The `grilling` skill, against the contract
   doc. Aim at failure modes that cost money or trust, not at style.
   The generic set: callback arrives twice, out of order, or never
   despite success; user abandons mid-flow then appears on another
   surface; renewal or retry fails; a human acts directly in the
   provider dashboard, outside your flow; two actors act on the same
   entity concurrently; an entity drops to a lower tier while over the
   lower tier's limits; someone replays a captured payload; your write
   fails after the external system already committed. Every answer
   needs a named state and a named owning repo. "We would handle that"
   is not an answer.
5. **Contract to tickets.** The `to-tickets` skill. Vertical slices, one
   per repo where possible. Each names its repo absolute path, the
   contract section it implements, its acceptance evidence, and its
   dependencies. Sequence so each ends in something verifiable alone.
6. **Design.** The `design` skill. Artboards for every surface the
   feature touches, including how it appears on surfaces that only
   consume the result. Reuse the existing design language rather than
   introducing primitives. Use `prototype` for cross-surface UX
   questions the artboards cannot settle.
7. **Approval gate. Hard stop, every time.** Explicit sign-off on the
   specific artboards before any repo is touched. An ambiguous reply is
   not approval. Everything after this point runs without asking again.
8. **Verification harness, privileged-mutation repo first.** The
   `create-verification-skill` skill. The capability that matters:
   drive the real integration against real local state and prove the
   properties the contract claims. Cover the adversarial paths
   explicitly (duplicate delivery, out-of-order delivery, signature or
   auth failure), not the happy path. Evidence is state before and
   after, never a 200.
9. **Build, one delegate per repo.** If the user works with a
   build-discipline skill (for example `poteto-mode`), invoke it only when
   they ask for it; some such skills are explicit-invocation only. Hardest judgment
   (idempotency, state transitions, reconciliation) goes to the
   strongest tier. Each delegate gets its repo path, the contract
   sections it owns, the sections it must not write, and its repo's
   verification skill. Review every diff. Never accept a delegate's own
   "done".
10. **Blast-radius the seams.** The `blast-radius` skill. At minimum:
    the enum mapping, anything touching money, currency, or precision,
    and the state read path consumed by surfaces that did not write it.
    Prove the safety fact by running real code. A writeup alone fails
    this stage.
11. **Security review.** Non-negotiable, not a formality. Signature or
    token verification actually present and correct, provider secrets
    absent from every client bundle, no client-writable path to the
    fields that carry authority, and access rules audited against the
    contract's ownership table.
12. **Close out.** `code-review` and `simplify`, per repo.

## Loop

The next feature re-enters at stage 0. Stages 3-4 rerun only if it
touches the contract; a feature that consumes the existing contract
without changing it starts at 5.
