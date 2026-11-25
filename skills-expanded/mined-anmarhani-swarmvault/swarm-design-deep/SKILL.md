---
name: swarm-design-deep
description: The developer-driven design lane — the user commits to each approach before anything is written, then the design goes to pseudocode, algorithms, invariants, sequence diagrams and test vectors in their chosen design language. Use when the user wants to own the system rather than receive it: "developer mode", deep/detailed design, designing algorithms or data structures, writing pseudocode or sequence diagrams during design, or human-driven planning after the SRS.
---

# swarm-design-deep — the developer-driven design lane

**Gate:** requires a validated SRS. This lane **replaces** swarm-design for the phase — do not
run both; one skill owns the design artifacts.

The standard lane (swarm-design) is agent-driven: it proposes an architecture and the user
validates it. That is the right trade for most projects. This lane exists for the other case —
a developer who must hold the system in their head afterwards. It is slower and costs more
tokens on purpose, and it pays for itself only if implementation comes out mechanical.

## The contract

Treat the design session as the agent, and apply six of the 12 factors to it:

| | applied here |
|---|---|
| **8** own your control flow | The user decides what is designed next. Never advance the unit list yourself. |
| **7** contact humans with tool calls | Every unresolved choice is an explicit question. No assumption reaches the doc silently. |
| **3** own your context window | Design lives in per-unit files, not the transcript. This is what makes the depth affordable. |
| **6** launch/pause/resume | One unit per session, closed and dropped. A cold session resumes from the unit table. |
| **12** stateless reducer | Each session = (files so far + one decision) → updated files. |
| **10** small, focused agents | One unit designed to the bottom beats the whole system designed halfway. |

**Awareness is caused by producing, not by reading.** Forty pages of excellent design gets a
rubber stamp. The commit step below is the whole point of the lane; without it this is just
swarm-design with more words.

## Setup — the design profile (ask once)

Write `docs/design/profile.md`, then never ask again:

- **design language** — what algorithms and signatures are written in. *Independent of the
  implementation language*: designing in Java and building in Python is normal. Language-neutral
  pseudocode is a valid answer. Say this out loud when asking, because users assume it's the
  build language.
- **granularity** — what one unit is here (module / service / endpoint / algorithm).
- **diagram formats** — see `references/diagrams.md`.
- **standing depth override**, if any.

## Units and depth triage

Decompose into units and give each a class. Propose the triage, get it confirmed. **Depth is
allocated, not applied** — this is the primary token control.

| class | signals | owes |
|---|---|---|
| **algorithmic** | novel logic, ordering/state/concurrency, performance-sensitive, non-obvious data structure | pseudocode, data structures, invariants, complexity, edge-case table, **test-vector table** |
| **integration** | crosses a boundary — network, process, third party, filesystem, user | sequence diagram, contract (types in/out), failure modes with timeout/retry/idempotency stance |
| **mechanical** | CRUD, config, glue, framework-shaped, fully determined by its contract | signature + one line of intent. **No pseudocode.** |

Level-0 units are the standard lane's deliverables — stack, decomposition, data model,
milestone boundaries — run through the same loop. Level-1 units are the modules themselves.

If the user asks for algorithmic depth on something mechanical: **say what it costs and what it
buys, once**, then do as they decide. Pseudocode for a CRUD handler is waterfall with extra
steps, and saying so is part of the job — arguing twice is not.

## The unit loop

Per unit, in order. Steps 1–2 are the lane; skip step 2 and you are running swarm-design.

1. **Frame.** What must this unit do (FR refs), what constrains it (NFR refs), what goes in and
   out, and 2–3 candidate approaches with real trade-offs. **Write no implementation detail
   yet.** Read the relevant FR spec, not the whole SRS.
2. **Commit.** The user states the approach in their own words, or picks one and says why. Wait
   for it. If they delegate — "you pick" — decide, and record `decided-by: agent (delegated)`.
   Do not treat silence, a "sounds good", or a question as a commitment.
3. **Draft.** Write the unit file against *their* approach, not your preferred one. Include
   whatever the depth class owes.
4. **Check.** Ask 2–3 questions about **consequences**, not content: "what happens if the queue
   is empty when the timer fires?" Aim them at the parts most likely to be wrong. A wrong answer
   means the design or the explanation is wrong — fix it, don't re-explain harder. This is not a
   quiz and must not read as one.
5. **Close.** Record status and attribution in the unit table, drop the unit from context, and
   **report units remaining**.

The user may write any part themselves — a signature, the control flow, the whole unit. Complete
and critique it rather than replacing it, and record that they wrote it.

**When a committed approach proves wrong while drafting:** stop, show the conflict with evidence,
and return to step 1 for that unit. Never quietly design something else.

## Ownership accounting

Each unit carries `decided-by: user | agent (delegated)`. At the exit summary, report the ratio.
If more than half were delegated, say it in one plain line — the lane was chosen for ownership,
and that is how much of it they hold. State it and move on; it does not block.

## Files

```
docs/design/
  profile.md              design language, granularity, diagram formats, depth policy
  overview.md             system map · unit table (class · status · decided-by) · FR traceability
  units/NN-<slug>.md      one file per unit  (template: references/unit-template.md)
  diagrams/               .drawio.svg / .excalidraw.md sources
```

ADRs still go to `50 Decisions/<P>/ADR-NNN-<slug>.md`. Sync mirrors everything. Per-unit files
are for context economy, not tidiness: load `overview.md` plus the one live unit, never the
closed ones.

Without a vault, write to `docs/design/` and skip the mirroring — the lane works standalone.

## Token economy

The lane is expensive by construction, so make the controls visible:

- Triage honestly. Most units are mechanical, and mechanical units cost a signature.
- One unit per session where practical; `checkpoint` and compact at unit boundaries — they are
  safe states by definition (see swarm-orchestrate).
- Report units remaining at every close, so the user can stop, downgrade the remaining triage,
  or switch lanes with real information.

## Exit gate

- Every Must-priority FR maps to ≥1 unit (traceability table in `overview.md`).
- Every unit closed, or deferred with a stated reason.
- Every algorithmic unit has a test-vector table.
- **The handoff test:** swarm-implement can write tickets from these units without asking
  *how* — only *in what order*. If it can't, the lane didn't pay for itself; name the units
  that fail and finish them.

Then flow-state → `phase: design-ui` (if the SRS declares an interface) or `phase: tickets`.
Record `design-lane: deep` so a cold session resumes here.

---
*Influences: humanlayer's 12-factor-agents (Apache-2.0) — factors 3, 6, 7, 8, 10, 12, applied to
the design session rather than a runtime agent. See CREDITS.md.*
