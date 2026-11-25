---
name: llm-claims
description: "Conversational claim ledger -- the in-chat notation. Agent MUST load on `claim *` marker commands, or when a conversation's claims churn (reversals, contested points, retractions). For a ledger kept as files, load Skill(llm-claims-kb)."
---

<!-- Core: verbatim-shared with the user's claude.ai preferences.
     Merge improvements in either direction by copy-pasting this block. -->

## Claim Ledger

When claims churn, label them. A label names the locus; a trailing
sigil signs the judge -- `!` the user's call, `+` the agent's (veto
invited), `?` no one's yet -- and bare means no judge is needed: a
checkable fact, or it follows from its premises. `<-` names what a
claim rests on:

* PARSER: the crash is in the parser, reproduced on a minimal input
* MULTIBYTE+: it fires only on multibyte input (three samples, no counterexample)
* DECODER <- PARSER MULTIBYTE+: so the fix belongs in the decoder, not the parser

Policy:

1. Claim set: union over chat, last wins.
2. Every claim, both parties: sound, open, or retracted. Open claims are debt, priced by what rests on them.
3. Governance is one line over labels: `claim accept MULTIBYTE` re-signs it `MULTIBYTE!`
4. Every render is a patch: restating a claim supersedes it, unmentioned claims stand. List what changed and stop.

<!-- /Core -->

The core block alone runs in chat-only environments; typed claim kernels
and proof-transport systems are harder rungs of the same ladder, and the
invariant holds at every rung -- every claim sound, open, or retracted.

The rest of this file is what it takes to read a ledger and to name an
operation on one. What each operation *obliges* is a file apiece in
`skill.kb/must-read.kb/`.

> **IMPERATIVE:**
>
> Your FIRST action when this skill loads MUST be:
> `Bash("ls -RF skill.kb/must-read.kb/")`
>
> That listing is an index of triggers: each filename names the occasion to
> read it. Walk it while planning, before ANY action, and read every entry
> whose trigger matches the work at hand — `before/` entries must be read
> *before* the action they name, not alongside it.

## Sigils

The sigil trails the label, so the label stays a greppable word: `grep -w
XY` finds `XY`, `XY?`, `XY!`, and every reference, and not `XY_Z`. Labels
are distinct as whole words and no more; a family sharing a head
(`CONFLICT`, `CONFLICT_ARITY`) is found by `grep '\<CONFLICT'`.

A claim therefore has two renderings of its name. Its **definition
site** -- the line stating it -- is fully qualified: label, sigil, and
any `(todo)`. Everywhere else the bare label is licensed and usually
reads better. An arrow clause may still carry sigils where the
warrant-mix is the point (`XY <- AB! CD?`), at the price of a copy that
goes stale when the claim is re-signed.

Four marks exhaust the space. A signature records *residual choice*: if
accepting every premise settles the claim, nothing was left to decide and
it stays bare, standing on its premises. Unsure whether a judgment crept
in? Sign `+` -- a needless signature invites a needless veto, but a false
bare hides a judge.

`?` and `+` both want the user's eye, for opposite things -- an answer, a
veto. One scan finds both: `grep -nE '[A-Z_][?+]'`.

## Arrows

`<-` names what a claim rests on. It is motivation, not entailment: it
says the writer had those claims in view, and nothing checks that the
conclusion follows. A closed ring -- `AB <- CD` and `CD <- AB` -- is
mutual support, which is no support at all; nothing rejects it at entry,
and the ring stays `?` until something outside it lands.

## Statuses and retraction

A sigil sometimes needs one more word; suffix the line:

    * XY: claim text                  -- certified(CHECK)

`certified(CHECK)` names the re-runnable check that discharged the claim.
A certified claim goes **bare** -- the check made it a fact -- and keeps
the note so anyone can re-run CHECK. Retraction withdraws with nothing in
its place and stays visible where it stood: `~~XY~~: claim text`, so `grep
XY` still finds it. The signatures need no verbose form; the sigil is the
record.

A claim decided but not yet built takes a `(todo)` on its label:

    * XY! (todo) <- AB!: the island rule is ***

The body already states the future state, so the mark grades the tense
rather than restating it. It sits on the label and ahead of the arrows:
past them it would read as a modifier of the last prior, whose tense is
its own business. It touches neither the label -- which must survive the
day the state ships -- nor the sigil, spent on the judge. When the state
lands, drop the token; the line is already the descriptive sentence.
Undecided stays plain `?` (an-open-question-needs-no-new-mark); in files
the tense is `todo: true` (`Skill(llm-claims-kb)`).

## Theories

`<-` tracks support -- what a claim rests on. Theories track **sense** --
what a claim cannot be read without. The two are independent: a claim can
rest on another without borrowing a word from it, and can borrow a word
without resting on it.

A **theory** is a stipulated word list -- its **ontology** -- together
with the claims confined to that list. It is no second kind of thing: it
is a claim, whose text states the ontology and whose `<-` names the
**priors**, the theories whose words it also admits. What is confined to
it is written **under** it, indented:

* DESIGN+: what this skill commits to -- ontology: skill, manual, design
  * STANCE+: a regress stops at an act -- ontology: regress, act, author, judgment
    * AUTHOR_ACTS+: authority is a property of acts, not of propositions
  * PURPOSE+ <- STANCE+: one invariant, at a cost a chat will pay -- ontology: ledger, claim, cost
    * CHEAP+: the ledger competes with keeping no ledger, not with a better notation

Indentation is sense; `<-` is support. A claim reads in every word
stipulated above it, so containment needs no arrow to say so, and a prior
is what you cite when the words you need are *beside* you rather than
above. The shape repeats at every depth and nests without limit -- the
flat list is just the case where nothing nests.

A theory lists only the words it coins -- those it fixes a meaning for
that a reader could not have brought; topic vocabulary stays off the
list however central to the subject. The grouping follows: a claim
belongs to the outermost theory that coins every coined word its text
needs. A theory's standing is its defining claim's standing, and
widening the ontology is a revision to it.

- **Confinement** -- an ontology excludes: a listed word is that
  theory's, and its siblings may not use it. It greps for a sibling
  saying an owned word -- the word was no coinage and gets culled, the
  claim is misfiled and moves, the speaker genuinely depends on the
  owner and imports it (an import asserts support too -- take it only
  where that holds), the two mean different things by it and
  one uniquifies, or the speaker is the owner's own prior and the word
  wants a shared theory upstream of both.
- **Conservativity** -- a later theory never lowers a prior's standing.
  Where it seems to, the prior was wrong; fix it there.

You want a new theory when more than one theory leans on the same
subsection of an existing one -- break that subsection out as their
shared prior -- or when the split would leave most parts easier to
read and reason about: shorter ontology, shorter arrows, claims
arguing in one vocabulary instead of two. Never because the list of
claims got long.

Auxiliary theories, naming, and words that recur across theories:
`skill.kb/theories.md`.

## Commentary

The claim line is the artifact; anything you want to say *about* it goes
in a sub-bullet beneath it, opened with `//`. Marginal notes take no
label and no sigil, and they do not travel with the claim when it is
re-rendered, filed, or flushed.

* XY!: the claim, stated for a reader who was not there
  * // why I read the antecedent this way; veto if I picked wrong

The mark keeps indentation unambiguous -- a labelled child is
containment, a `//` child is commentary -- and it greps: `grep -n '\* //'`
finds every note in a render.

## Commands

Marker commands (`Skill(llm-subtask)`); also act on your own initiative --
the core's "when claims churn" is the trigger, not a user request.

- `claim list` -- render the surviving ledger
- `claim add XY: TEXT` -- add a claim; the colon survives here alone,
  because what follows it *is* the claim line
- `claim accept XY` -- the user's ruling; re-sign `XY!`, with a clause of
  grounds -- also how a `+` graduates
- `claim contest XY` -- reopen; mark `XY?`
- `claim retract XY` -- retract and propagate
- `claim certify XY` -- name an executable check, run it; on success the
  claim goes bare, suffixed `-- certified(CHECK)`
- `claim flush` -- end-of-context extraction

Render a ledger as one nested list, one claim per line, in ASCII (`<-`).
The last three commands each carry a rule in the bank; `ls` it rather
than guessing.

A ledger kept as files -- one claim per file, standing in frontmatter --
is `Skill(llm-claims-kb)`. Why the notation is shaped this way, and
where to argue with it: `design.claims.md`.
