---
name: persist-clarity
description: "Agent MUST load on /persist-clarity, when a session is ending that produced more understanding than diffs, when the user asks to wrap up without losing the clarity/context/understanding, or before /clear or a handoff following significant litigation, debugging, or design work."
---

# /persist-clarity [scope]

A session ends with two products: its **decisions** (diffs, conclusions,
rulings — usually persisted) and its **clarity** — the understanding
that produced them, which evaporates at the context boundary. Fluency
is not storable; its residues are. The operation has three beats, in
order: **encode** the clarity as a claim ledger; **review** — present
it, integrate rulings; **persist** — on the user's go — the reviewed
ledger into the project's homes.

## Encode: the ledger is the clarity

Render what this session now understands as a claim ledger —
`Skill(llm-claims)` notation: one claim per line, the sigil signing
the judge, `~~strikes~~` for what was killed, `<-` for what each
rests on. The render is a message, not a file: it mints nothing, so
no session is too small for it — two bare facts owe a two-line
ledger. If the session already kept a ledger, this is its final
patch, not a rival. Inventory the whole session, not the recent
tail — the early turns are the ones you've already half-forgotten,
which is the signal they need persisting.

Gate each line by the cold-reader test: could an agent with no memory
of this session reconstruct it from disk? What disk already holds
enters only as a premise; the ledger carries the delta.

The ledger is incomplete until it covers four residues:

1. **Results** — conclusions *with their standing*: the sigil names
   who ruled each one. A summary of conclusions is this ledger with
   the sigils stripped.
2. **Reversals** — why the losing alternatives lost: a struck claim
   apiece, with its ground, its revisit condition, the owner's veto
   verbatim. The most valuable residue and the first one lost:
   without it, the next session re-proposes the dead idea and re-pays
   the whole litigation.
3. **Lenses** — the ways-of-seeing that generated the decisions. Find
   them where the work *turned*: the question that made a hard choice
   easy; the razor applied more than once; the distinction the user
   drew that you didn't have at session start; the false fork someone
   dissolved. One claim per lens, phrased as a reusable rule.
4. **Opens** — what is *not* done, as `?` claims; clarity about it
   rots fastest of all.

The four appear whatever the session was: a debugging session's
reversals are its eliminated hypotheses, its lenses "check the X
before blaming the Y".

Spend first on reversals and lenses — the residues only you currently
hold. Anything already on disk can be sharpened later, by anyone.

## Review: standing is fixed here

The render *is* the ask — no ceremony around it.
`Skill(llm-claims)`'s presentation rules govern: a `?` comes with
what an answer would settle; a `+` is a standing offer to veto, never
a sign-off queue. Integrate what comes back — rulings re-sign,
contests reopen, corrections supersede — and keep each ruling's
words attached to its label: at the persist beat they become the
claim's `authority:`, never mined from the transcript after the
fact.

Review is a veto point, not a gate — a `+` stands without an answer,
vetoable forever; a `?` stays open — and it ends at the user's
satisfaction: integrate until the ledger reads back what they would
sign, or their silence leaves the render itself as the product.

## Persist: the user's call

A disk ledger past review is optional and recommended — offer it;
the user decides, and the operation may end at the chat render. On
go, read `skill.kb/persistence.md` and file the reviewed ledger into
the project's homes. It carries the per-ecosystem strategies; the two
residues no claim can hold — the **narrative address** (where the
full story can be re-mined) and the **re-entry path** (a cold agent's
reading order); and the filing anti-patterns. Elected, the filing
ends at a commit, not before.
