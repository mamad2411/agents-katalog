---
name: fork-and-decide
description: Decide a project one fork at a time before anything is built. Two files and a
  log carry the state; every answer propagates through the remaining questions — options
  re-weight, die, or collapse, and the user stays the only judge. Use when an idea, a doc,
  or an old repo must become a decided spec. Not for tasks you could describe in one sentence.
---

# Fork & Decide — decision propagation for turning ideas into decided specs

One project, decided one fork at a time. Two working files and a log carry the whole state,
and every answer the user gives is amplified through the remaining question space — the fork
count falls faster than one per answer. That amplification, not automation of judgment, is
the point: deduction may act alone; inference must show itself.

## The files

**FORKS.md** — open questions only. A fork:

```
### FR7 · Payments provider — one-way · closed kind
UK+EU cards, no monthly fee. (definitions its options lean on live here — no close on an un-grounded term)
- Stripe — 1.5% + 20p, native Apple Pay · leading ← recommend: fees at this volume
- Paddle — merchant of record, 5% + 50p · live
- invoice by hand — possible, buried by "zero-ops" motivation · dead
next: your call        (or: research · experiment · expand)
```

**DECIDED.md** — closed decisions, current truth only, no corpses (history is git). Lens-scoped
permanent IDs. One bullet each: statement · reason · basis tail — `_constraint_` (someone said
so) · `_evidence → file_` (checked) · `_assumption (door) · reopen-if …_`. Plus three sections:
**Principles** (graduated motivations that govern every gap the agent fills alone), **Conflicts**
(`not X with Y · learned <date>`), **Rejected** (killed options with their reasons and traces — guard-rails, not residue).

**log.md** — provenance, keyed by ID: when · who/what · source — direct word · artifact
(file, "quote", speaker, timestamp) · derived (the forcing trace).

## The rules

1. **Every close propagates — full sweep.** Every open fork is re-read against the new decision
   AND its motivation; no edge filter decides what gets looked at. Backward too: every prior
   decision is checked for contradiction. The sweep is a READ: effects land only where the
   decision or motivation actually bites — re-reading every fork is never a license to
   re-label every fork.
2. **Two payloads, one mandatory.** The decision carries hard effects — what is now impossible
   or forced; the motivation, when given, carries soft effects — state moves and steering.
   A bare decision is legal; a motivation is never demanded.
3. **Allowed effects:** re-weight · kill/add option · rewrite question · spawn fork · kill fork ·
   collapse to one survivor.
4. **Admission:** a question earns a fork iff its answer would change other answers or is
   expensive to reverse; the rest the agent does alone under the Principles.
5. **Contact:** forks reach the user most-influential-first, top-3 per turn, recommendations
   marked, free-text answers — free text carries motivation, and motivation is fuel. Definitions
   travel with the fork.
6. **Authority:** the user closes on judgment. The system closes only entailment — every sibling
   option *killed* by hard effects — as a derived decision, logged with its trace, shown in the
   receipt. Options merely at *dead* never trigger it. A derived close is logged as **derived**;
   writing it as the user's word is laundering, and inventing a decision the user never voiced —
   however sensible — is the same violation. The turn does what the message licenses, nothing
   beyond it. The user's words carry authority, not truth: an evidence collision is surfaced,
   neither silently obeyed nor silently corrected. When a **one-way** door closes on an
   assumption, the receipt names the irreversibility and carries the experiment that would
   settle it — the decision still stands; the gate is the blocking check, not this. A
   passage the user retracts in-message
   ("disregard that…") voids everything in it — nothing from it enters the ledger as a
   decision, option, note, or reason.
7. **States, not numbers:** every option sits at leading / live / fading / dead; propagation
   moves options between states. *Killed* is not a state — it is removal by fact, with a trace.
8. **Cascade guards:** any fork touched twice in one cascade stops the chain and goes to
   the user.
9. **Conflict memory:** an incompatibility no rejected option can carry — two standing
   decisions that collide only in combination — writes one standing line.
10. **Expansion:** option lists are samples. Forks carry a kind (closed / open); the sweep
    maintains a saturation read; a ripe fork (open kind, few options, nothing leading, or the
    recommendation keeps being refused) gets `next: expand` proposed — the divergence research
    runs only on the user's word. A sweep-spawned fork arrives MINIMAL — the question, its
    door, one line on what raised it; options, figures, and a recommendation are expansion
    work and wait for the word. Evidence-carried options land automatically — and evidence
    means evidence: an invented figure is never written anywhere, an option carries a source
    or carries no number.
11. **Principles:** recurring user-given (or endorsed) motivations graduate into the Principles
    section and govern every gap filled alone; agent reasoning never self-graduates.
12. **Ledger hygiene:** current truth only; IDs permanent, holes allowed, renumbering forbidden;
    every decision gets a log row. Decided text states what IS — never a diff against a
    baseline, named or unnamed: "has no X (unlike …)" is a diff; a list of what stands is
    the fact.
13. **The receipt:** every turn that changes the ledger ends by showing the change itself —
    what closed, what moved state, what was derived, what the sweep touched — plus the status
    line. Every new ledger entry's receipt line names its lens and the one-line why of that
    placement — unconditionally, obvious cases included; any other call the user didn't make
    (a scope reading, a derived number) is surfaced the same way. "Updated the file" without
    the delta is a violation.

## The gate

Ready to build means: no open one-way doors · no one-way door closed on an assumption ·
conflicts quiet. Then the handoff is written — `constitution.md`, one page: the constraints
and decisions the builder must never undo, one line each with its ID — and handed over
together with DECIDED.md itself, which is already current truth and carries its own
provenance. A fresh session builds from those two alone.

Before it, ask for a **lens read** if you want one: one isolated reviewer per professional
lens, each seeing only the decided spec, none seeing another's output. What comes back is a
report — you promote what earns a fork; nothing lands on its own.

## Running it

Say *"fork and decide this: \<one paragraph of the idea\>"* — or just *"fork and
decide"* in a folder that already holds a dossier. The session creates `spec/FORKS.md`,
`spec/DECIDED.md`, `spec/log.md` and runs the loop: most-influential-first, top-3 per turn,
receipts on every change. Then talk: *"decide FR3: …"* · *"expand FR7"* · *"park FR9 until
we play"* · *"run a lens read"* · *"I'm closing this session — what's unlanded?"*

