---
name: llm-design-kb
description: "A project's design record, kept as a claim ledger -- mission, goals, requirements, architecture, components, deliverables. Agent MUST load when starting or extending a project's design documentation, when writing down what a system is for or must do, when deciding which rung a design statement belongs on, when recording a design decision together with the options it beat, or when meeting a numbered design tower (010-mission.kb/ and siblings)."
---

# Design Knowledge Bases

A design record is a claim ledger whose theories are the rungs of a
why/how chain. The notation is `Skill(llm-claims)`; persisting it to
disk is `Skill(llm-claims-kb)`. This skill adds one thing to them: the
stratification, and the discipline of keeping a design statement on
the rung whose question it answers.

> **IMPERATIVE:**
>
> Your FIRST action when this skill loads MUST be:
> `Bash("ls -RF skill.kb/must-read.kb/")`
>
> Each filename names the occasion to read it. Walk the listing while
> planning and read every entry whose trigger matches the work.

## The rungs

Six theories, each answering a question that motivates the next:

| Rung | The question it answers |
|---|---|
| `mission` | What problem are we solving? Who benefits? |
| `goals` | How do we accomplish the mission? |
| `requirements` | How do we validate the goals are achieved? |
| `architecture` | How do we satisfy the requirements? |
| `components` | How do we implement the architecture? |
| `deliverables` | How do we build the components? |

They are a **default the skeleton seeds, not a law this skill
enforces**. A project drops a rung it does not argue about and adds
one it does, by revising its own `design.md` -- the rung set is that
claim's `ontology:`, so restratifying is an ordinary edit under
ordinary governance, and it takes the standing of whoever ruled it.

Two consequences of rungs being theories rather than folders:

- **Priors are a DAG.** A claim's `why:` names whatever claims it
  would be revisited over -- one rung up, four rungs up, or sideways.
  The ladder is the common shape, not a constraint, so a design claim
  citing a goal directly is an ordinary long edge, not an error.
  Content the design assumes but does not argue -- background, prior
  art, use cases -- is an auxiliary theory beside the rungs.
- **No numeric prefixes.** Order lives once, in the `why:` arrows; a
  digit in the filename is a second copy that drifts, and inserting a
  rung between two numbers would rename every reference on file.

The discipline the rungs buy is **confinement**: a word a rung
stipulates is that rung's, and its siblings may not use it.
`llm-claims-kb-ownership --trespass` reports a mechanism word coined
in `architecture` and spoken in `requirements` -- which is the
state-properties-not-mechanisms rule, mechanized.

## Encode: draft the design as a ledger

Render the design in chat as `Skill(llm-claims)` notation before
writing any file -- rungs as theories, claims nested under the rung
whose question they answer, `<-` for what each rests on, a sigil on
every line. What the user ruled signs `!`; what you inferred signs
`+`; what nobody has settled signs `?` and says what would settle it.

Design records lead implementation as often as they trail it, so
**every claim declares its tense**. Mission, goals, and requirements
are aspirational by nature and take no mark. From architecture down, a
claim describing something not yet built takes a `(todo)`:

    * CACHE! (todo) <- SPEED!: the resolver caches by content hash, not by path

Write it as declarative future-state prose, never as an imperative
task: when the state lands, dropping the token leaves a sentence that
is already true. A claim with no `(todo)` is a claim about what is, and
a mismatch with the code is a bug in the claim.

## Review: rung by rung

Present each rung as you finish it rather than the whole tower at the
end -- a mission the user would have redirected is a tower built on
sand, and the cost of finding out is one message.

Review is a veto point, not a gate: silence persists every claim at
its honest sigil. Integrate what comes back, keeping each ruling's
words attached to its label -- at the persist beat they become the
claim's `authority:`.

A rejected option is not deleted. It stays as a struck claim carrying
`verdict:` and its ground, filed beside the winner: without it the
next session re-proposes the dead idea and re-pays the whole argument.
At the **second contending answer** the question takes the
decision-point shape (`Skill(llm-kb)`): `$ITEM.md` poses the question,
`$ITEM.kb/` holds one file per candidate, chosen and declined alike.

## Persist: copy the skeleton, then file

The default home is `docs/dev/claims.kb/`, which leaves room for the
several ledgers a project accumulates. Bootstrap it by copying this
skill's `skeleton/` wholesale:

```bash
cp -r <this-skill>/skeleton/docs/dev/claims.kb docs/dev/
```

That lands `design.md` beside `design.kb/`, the six rung theories with
their questions and `why:` arrows, a `technical-policy.kb/` for
cross-cutting imperatives, and a bound schema for each collection. The
rungs arrive `standing: open` -- they are the questions, not answers,
and answering them is the first act. Each empty collection holds a
`.keepme` explaining itself; delete it when the first claim lands, and
delete any rung the project does not want.

Then file the reviewed ledger per `Skill(llm-claims-kb)`: one claim
per file, standing in frontmatter, arrows as `why:`. The operation
ends at a commit.

## Maintenance

After a session that changed the code or the design understanding,
hold the record to what is now true:

- **Descriptive claims are checked against ground truth and fixed
  directly.** A claim carrying `todo:` is exempt -- it is normative,
  and a mismatch is the point; drop the token instead, if the state
  landed this session.
- **New understanding enters at the standing it earned.** What the
  user ruled is a signed claim; what you inferred is `+`; what surfaced
  and stayed unsettled is `?`. Enacting an inference as settled rule is
  the failure this skill exists to prevent.
- **`why:` arrows are traced, not assumed.** A new claim needs its
  arrows; a claim that gained a responsibility needs them updated.
  `skill://llm-claims-kb/bin/llm-claims-kb-graph` finds the arrow that
  points nowhere, the claim that never joined the graph, and the
  citation cycle.
- **Confinement is a grep.** `llm-claims-kb-ownership --trespass`
  reports a rung speaking another rung's stipulated word -- usually a
  misfiled claim, sometimes a missing import.

## In unledgered prose

Documents outside the ledger -- READMEs, contracts, synthesis files --
carry the same tense distinction as callouts: `> [!TODO]` for decided
but unbuilt, `> [!QUESTION]` for undecided, undecorated prose for what
ships today. Never implement a `[!QUESTION]`: an agent that builds an
open question has shipped an unratified guess.

They are the ledger's poor relation, and a churning callout is the
signal to promote the document's claims into the ledger, where they
gain a judge and a ground.
