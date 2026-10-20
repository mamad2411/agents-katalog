---
name: clarification-gate
description: Decides what must be asked before architecture and what can proceed on a recorded assumption, then asks it once in a single grouped batch. Prevents both expensive silent guessing and question spam. Run after requirements analysis, before technology and architecture work.
license: MIT
metadata:
  category: delivery-skills
  version: 1.0.0
  depends_on: [engineering-core, requirements-analysis]
  outputs: [question-batch, assumption-decisions, gate-verdict]
---

# Clarification Gate

Answers one question: which unknowns are worth a person's attention, and which
are worth a recorded assumption.

Both errors are costly. Guessing on a blocking unknown rebuilds a subsystem.
Asking about every unknown makes the user do the analysis they hired the
system to do.

## 1. The blocking test

An unknown is blocking when at least one holds:

1. **Architecture depends on it.** The answer changes the data model, the
   boundaries, the deployment shape, or which external system is used.
2. **It is expensive to reverse.** Getting it wrong means a migration, a
   rewrite, or a change to already stored data.
3. **It carries legal, financial or safety consequence.** Money movement, who
   owns data, what may be deleted, who may see what.
4. **The readings are genuinely incompatible.** Not a detail with a sensible
   default, but two products wearing the same word.
5. **No defensible default exists.** Any choice is arbitrary and the source
   gives no direction.

An unknown that fails all five is not blocking. It becomes an assumption with
its cost written down, and the work continues.

## 2. Non blocking, by construction

These almost never justify stopping. They have defaults, and the default is
recorded rather than asked:

wording of interface copy, pagination page size, sort order defaults, date
display format, colour and spacing choices where a design system exists,
maximum lengths of free text fields, whether a list shows ten or twenty items,
naming of internal modules, log level thresholds, test framework choice inside
an already chosen ecosystem.

Each becomes a line in the assumption register. The user sees all of them at
the validation gate and can correct any that matter, at zero cost.

## 3. Question quality

A question is worth asking when the answer changes what gets built, and the
person can answer it without doing engineering.

| Bad question | Why | Better |
|---|---|---|
| What database should we use? | that is the system's job | none, decide it and justify it |
| Do you want it to be secure? | no real alternative | none |
| Should we use REST or GraphQL? | engineering decision | none, unless a client system forces it |
| What are your requirements? | the analysis was not done | ask the specific gap |
| Can you clarify the specification? | unactionable | quote the sentence and give the readings |
| Is this okay? | no decision content | present the choice with its consequence |

The shape that works: quote the source, name the readings, state what each
costs, and ask which one.

```
Your brief says trainees "follow courses". This can mean four different
products:
  a) read pages and mark them read      simple, 2 tables
  b) watch videos with progress saved   needs video hosting and playback state
  c) complete graded exercises          needs a grading subsystem
  d) attend live sessions               needs scheduling and attendance
Which one is closest to what you have in mind?
```

The user answers in one word. That is the standard.

## 4. Batching

All blocking questions go in one message, grouped by area, numbered.

```
Money
  1 ...
  2 ...

Roles and permissions
  3 ...

Data lifecycle
  4 ...
```

Never a drip of one question per message. A person answering nine grouped
questions once spends five minutes. The same nine spread over a week costs
them far more and stalls the project between each one.

Cap: if the batch exceeds roughly ten questions, the requirements are not
merely unclear, they are absent. Say that plainly and ask for a working
session instead of sending a survey.

## 5. Assumption records

Every non blocking unknown becomes:

```
A<n>  <what is assumed>
      Why needed:  <what could not proceed without it>
      Default:     <the value adopted>
      If wrong:    <what changes, and what it costs to change it>
```

The `If wrong` line is what makes the record useful. An assumption whose
reversal costs a line of CSS and one whose reversal costs a migration look
identical without it.

Assumptions are surfaced twice: in the architecture proposal, and at the
validation gate. They are never buried in a file nobody opens.

## 6. Proceeding without an answer

When a blocking question receives no answer and the project must move:

1. Choose the reading that is cheapest to reverse, not the one that is best if
   correct.
2. Isolate the decision behind a boundary so the reversal touches one module.
3. Record it as a blocking assumption, marked as such.
4. Do not build anything downstream that depends on it being right.
5. Raise it again at the validation gate, at the top.

This is a degraded mode, and it is labelled as one. It is not equivalent to
having asked.

## 7. Protocol

1. Take the unknown register from `requirements-analysis`.
2. Apply the blocking test, section 1, to each unknown.
3. Convert every non blocking unknown into an assumption record, section 5.
4. Group the blocking ones by area and write them per section 3.
5. Check the batch size against the cap in section 4.
6. Send once. Wait.
7. On answers: update the specification, move resolved assumptions into
   requirements, note any answer that contradicts an existing requirement.
8. On no answer, and only when the project must proceed: section 6.
9. Issue the gate verdict.

## 8. Gate verdict

```
Cleared            no blocking unknown remains
Cleared with risk  blocking assumptions adopted per section 6, each named
Blocked            a blocking unknown remains and the project cannot proceed
                   correctly, with the exact question restated
```

## 9. Auto-critique

Score from 0 to 5: blocking test applied rather than guessed, non blocking
unknowns genuinely defaulted instead of asked, question quality, single batch,
assumption records carrying a real cost of reversal, honesty of the verdict.

Threshold: no axis below 3, average at least 4. A question the system could
have answered from the source or the repository is an automatic failure, as is
a silent guess on a blocking unknown.

## 10. Interfaces

- Upstream: `requirements-analysis`.
- Downstream: `technology-selection`, `architecture-proposal`,
  `validation-gate`, which restates the surviving assumptions.
- Related: `delivery-orchestrator` owns the gate sequencing.
