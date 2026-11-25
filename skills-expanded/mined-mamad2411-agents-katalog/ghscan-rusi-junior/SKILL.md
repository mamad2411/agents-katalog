# Junior Rule 09: Code or Skill

## Core Rule

**Encode in code what must *not* be judged. Encode in a skill what must be.**

Code is a guarantee. It runs the same way whether or not anyone is watching, and it cannot
be reasoned out of. A skill is an instruction. It is read by something that decides, in the
moment and under pressure, whether this is a case it applies to.

Choose by which of those two properties the behavior actually needs.

## Placement Guide

| Requirement | Home | Reason |
| --- | --- | --- |
| Complete audit of actions | Code at the action boundary | A missing self-reported entry cannot be detected later |
| A limit with known enforcement points | Code at those points | Every applicable operation must pass the check |
| Interpreting context or choosing an approach | Skill | Correctness depends on the situation |
| A constraint whose applicability requires judgment | Skill, explicitly described as a norm | Prose cannot guarantee compliance |
| Both judgment and an enforceable limit | Skill chooses; code bounds and records | Each layer handles the part it can reliably provide |

Use the distinctions below when a requirement spans more than one row.

## The Test

**Would I trust this if the agent had a stake in the answer?**

- **No, I would want it guaranteed** → **code.** The agent is a party to the outcome, so its
  own compliance cannot be the thing that guarantees the outcome.
- **There is nothing to trust, only something to work out** → **skill.** No fixed right
  answer exists to hold anything to, so there is nothing to enforce.

That answers where the behavior *should* live. Whether it *can* is the second question, and
**Constraints** below is where it gets asked. A guarantee with nowhere to run is a norm, and
it has to be labeled one.

## Belongs in Code

Two cases live here, and only one of them is absolute.

### Records - No Exception

Anything that records or audits what the agent did:

- Logs, journals, ledgers, any append-only record of actions taken
- Anything a later reader will rely on without checking it

**The agent is the party being audited.** An append-only record an agent writes freehand is
not an audit trail, it is a statement. The absolutism here is structural rather than a matter
of degree: an entry the agent never wrote leaves nothing behind to notice it is missing. A
record cannot be relied on for what it does not contain, so its completeness has to be
guaranteed by something other than the party it describes.

**Not this:** that clause is about a mechanism whose output is **relied on** as a record. It
is not about the documents the work itself produces. Specs, findings, progress tracking,
decision records, anything written for a reader who will weigh it against the work: that is
work product. It is read and judged, not trusted blind, and prose is its right home.

### Constraints - Enumerable, or Judged

Budgets, quotas, limits, gates that must hold on every path, including the paths nobody
anticipated. Code is strictly stronger here, so prefer it. But the split is not
records-versus-constraints, it is **enumerable versus judged**:

- The moments the constraint applies to can be enumerated → enforce it in code
- Recognizing those moments takes reading the situation → prose is the honest home, because
  a program would have to guess which situations count

Most real constraints are part one and part the other. Mechanize the part that enumerates
and leave the rest in prose, rather than approximating the judgment with a proxy or
abandoning the enforceable half because the whole cannot be enforced.

**When a constraint stays in prose, say that is what it is.** It is a norm, not a guarantee.
A norm someone has to uphold and a limit that cannot be exceeded are different objects, and
only one of them survives pressure. Calling the first one enforced is the failure this rule
exists to prevent.

## Belongs in a Skill

Anything that requires:

- Reading context and working out what it means
- Weighing trade-offs where no option dominates
- Choosing what to try, and in what order
- Deciding when the work is finished, or when to stop and ask

**A program has no judgment.** Asked for one, it will encode a proxy - a threshold, a keyword
list, a pattern match - and that proxy will be wrong in exactly the cases that needed
judgment in the first place.

## Triggers (stop and re-place the work)

- About to write a program that **decides** something → probably belongs in a skill
- About to write a skill instruction that must hold **every single time** → code if the
  moments it applies to can be enumerated; otherwise prose, named as a norm
- Building a mechanism whose output is **relied on** as a record of what the agent did →
  code, without exception
- Reaching for grep, regex, thresholds, or keyword lists to approximate **understanding** the
  content → the judgment is being proxied; hand it to the agent instead
- Writing "always..." or "never skip..." into prose → ask what actually enforces it

## Why Both Directions Are Easy

Neither failure looks wrong while you are doing it.

- **Judgment encoded as a program** looks rigorous. It produces brittle heuristics:
  thresholds and pattern matches standing in for actually reading the thing. It fails
  quietly, on the inputs the heuristic never anticipated.
- **An integrity constraint encoded as prose** looks flexible. It produces a rule the agent
  can skip under pressure - precisely when it matters most, because pressure is when a
  constraint is the only thing doing any work.

The first is caught when the heuristic returns an absurd answer. The second is caught late or
never: a record that cannot answer the question put to it, or a limit discovered only once
something has already gone past it.

## Anti-Patterns

| Anti-Pattern | Instead |
|---|---|
| Program that pattern-matches content to classify it | Hand the content to the agent and let it read |
| Threshold standing in for "is this significant?" | Judgment call - put it in a skill |
| Prose instructing the agent to log every action it takes | Make the logging the mechanism, not the instruction |
| Prose instructing the agent to stop at a limit that has a counter behind it | Enforce it where it cannot be reasoned past |
| Calling a prose constraint enforced | Name it a norm, and mechanize whatever part of it enumerates |
| Program choosing which approach to take | Skill chooses; code bounds what it may choose from |

## The Two Compose

Most durable designs use both: **the skill decides, the code records and bounds.** Neither
layer is a weaker form of the other, and a behavior placed in the wrong one is not "close
enough" - it fails in the specific way that layer fails.
