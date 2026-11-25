---
name: swarm-implement
description: Implementation phase — turn a validated design into dependency-ordered tickets, then work them as one of N parallel agents with atomic claims, model tiering, and tests-in-ticket definition of done. Use to plan tickets from a design, pick up/continue implementation work, coordinate parallel agents, or check what to build next.
---

# swarm-implement — implementation phase

Two roles. Check flow-state: no tickets yet → you're the **planner**; tickets exist →
you're a **worker**.

## Planner (strong model, once per milestone batch)

**Gate:** validated design. Read `docs/design.md` and the milestone's FR specs.

1. Emit tickets to `30 Plans/<P>/tickets/TK-NNN-<slug>.md` (template:
   `90 Templates/ticket.md`, machine lane): FR-ID trace, `requires:` edges (tracer-bullet
   order: thinnest end-to-end slice first), suggested `tier` (size) and `kind`
   (`design`/`planning`/`coding`/`review`/`docs` — lets orchestration route the right model),
   DoD checklist, and CONTEXT — the exact notes/design sections a worker needs (nothing more).
   **Also name the layers.** `requires:` orders tickets that exist; it cannot say whether the
   thing being ordered exists at all. Two tickets were once written as if a persistence layer
   were there — the engine belonged to one ticket, the tables to another, and the carrier
   between them to nobody, so both DoDs were unreachable as written and the gap was findable
   only by grepping for a repository and finding none. So every ticket carries:
   - `provides:` — the layers this ticket makes exist (`ledger repository`, `recurrence tables`)
   - `needs:` — the layers it builds on, in the same words
   Every `needs:` must match some ticket's `provides:`. `board` prints a **PLANNING GAPS**
   section and `doctor` fails the `ticket coverage` check when one does not, when a `requires:`
   names a ticket that was never written, or when two tickets claim the same layer. Run
   `doctor` before you hand the batch to workers — the gap is cheap now and a stalled worker
   later.
2. Ask the user ONCE (skip in auto mode if already answered at SRS validation):
   parallelism appetite, and is a browser/test environment available for UI verification?
3. Update flow-state (`phase: implement`, ticket count) — J1: state first, work second.

**Model tiers:** `top` — architecture-touching, complex logic, tricky concurrency;
`mid` — standard features, refactors; `small` — boilerplate, docs, simple UI. Workers on
the wrong tier for a ticket should say so rather than proceed on hard tickets.

## Worker loop (any agent, any platform, N in parallel)

1. **Pick:** next `status: open` ticket whose `requires:` are all `done`
   (`swarmvault.py query --project P --type ticket`). If orchestration is on, check
   `board --project P` first: a ticket listed **for this session** was routed to you by
   fit — take that one, on the model shown beside it (switch model if your platform lets
   you; say which model you want if it doesn't). Don't spawn an agent for work already
   routed here.
2. **Claim:** `swarmvault.py claim TK-NNN --project P --agent <you>` — claim won = yours;
   lost = pick another. Claims stale past the TTL: `--break-stale` (it logs the takeover).
3. **Read only the ticket's CONTEXT** — not the whole vault (token economy).
4. **Implement** to the DoD:
   - Acceptance criteria of the FR demonstrably met — no feature is complete until it
     fulfills its requirement.
   - Unit tests per function: happy path + edge cases + exception paths.
   - UI work: verify in the real browser/app when the env allows (Playwright); else mark
     the ticket `needs-ui-verify` honestly.
   - **Craft — write it for the next human** (a future teammate or agent):
     - *Simple:* the least code that does the job; delete before you add; no speculative
       generality. YAGNI outranks every principle below it.
     - *Reusable:* search first — call an existing function instead of a near-duplicate. Two
       occurrences are a coincidence, the third is a pattern; abstract only when the copies
       change together.
     - *Readable:* intention-revealing names, functions that do one nameable thing, early
       returns over deep nesting, match the file's existing idiom and vocabulary.
     - *Maintainable:* obvious data flow, no hidden globals/side effects, deep modules behind
       simple interfaces.
     - *Errors:* never swallow one. Catch only what you can actually handle, fail loudly with
       context (what was attempted, with what input), propagate the rest.
     - *Tests assert behavior, not implementation* — if a pure refactor breaks a test, the test
       was wrong. Happy path + boundaries + empty + failure, every time.
     - *Comment sparingly:* the code shows *what*; comments/docstrings only capture *why* —
       a constraint, a tradeoff, a non-obvious edge — never narrate lines. But "clean code
       needs no comments" is not the rule: an unexplained business rule is a defect too.
       Delete commented-out code.
     - **Don't follow a rule into a worse codebase.** Fragmented functions, one-implementation
       abstractions, patterns where a function would do, and SRP shrapnel are the documented
       failure modes of clean code applied without judgment — the next human's comprehension
       wins over any rule. Depth, the smell scan, and the tie-breakers:
       `references/clean-code.md`.
     - *Text a user will read* (UI strings, error copy, CLI output, README, release notes) is
       not code: route it through **swarm-write** and the project's `voice.md`. Placeholder
       copy shipped as final is a defect.
   - Deep reasoning that would bloat comments → code-note in
     `10 Projects/<P>/code-notes/` + one pointer line in the file header.
   - Commit: Conventional Commits with the FR in scope — `feat(FR-12): …`.
5. **Checkpoint as you go (J1):** significant progress or a blocker →
   `swarmvault.py checkpoint --project P --ticket TK-NNN --did … --next …`. That writes the
   full session note *and* appends the same compact line to the ticket, because a killed
   session must be resumable from the ticket alone — an agent that reads only the ticket, as
   this skill tells it to, has to find the handoffs there. `--ticket` defaults to whatever
   this agent has claimed; without either, the command says plainly that the ticket will not
   resume on its own.
6. **Close:** `swarmvault.py release TK-NNN --project P --done`; record commit + test
   refs in the ticket frontmatter; journal a session note (DID/NEXT/BLOCKED).
7. **Report at every boundary — without being asked.** `release --done` already prints the
   full board (pass `--platform`/`--model` so the burn estimate isn't guessed); relay it
   rather than swallowing it, and put its CHECK MY ASSUMPTIONS questions to the user. Same at
   a real blocker, a milestone, or a phase gate; when orchestration is enabled also
   `signal --event done|blocked` so other agents see it. Between boundaries use
   `board --project P --brief` (one line) — never a timer, never per heartbeat: monitoring
   must not cost more than the work (swarm-orchestrate has the cheap paths, including the
   status.md the supervisor keeps current for free).

**Scope discipline:** your change wants to cross into another ticket's files → note the
ticket link and stop; never expand scope silently.

**Milestone boundary:** last ticket of a milestone done → trigger swarm-review (auto
mode) or offer it (gated).

---
*Influences: superpowers subagent-driven-development, executing-plans &
dispatching-parallel-agents; Pocock's implement & to-tickets; euxx code-simplifier;
Martin's* Clean Code *and its documented failure modes; Ousterhout's deep modules;
Conventional Commits — see CREDITS.md.*
