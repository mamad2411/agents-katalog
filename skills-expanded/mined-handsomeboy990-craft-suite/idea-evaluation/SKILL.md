---
name: idea-evaluation
description: Converges a set of ideas to a ranked, defensible few: pressure-tests each idea's premise against reality, scores on feasibility, value, fit, cost and risk for the real actor, identifies the assumption each idea most depends on and the cheapest way to test it, and recommends with reasoning and next steps. The convergent half of ideation; ideation-engine is the divergent half. Use to choose among ideas, to kill weak ones early, and to define the validation that de-risks the survivors.
license: MIT
metadata:
  category: ideation
  version: 1.0.0
  depends_on: [opportunity-core]
  outputs: [evaluation-matrix, ranked-ideas, riskiest-assumptions, validation-plan]
---

# Idea Evaluation

Ideas are cheap; choosing well among them is the work. Evaluation converges a
generated set to a few defensible recommendations, kills the weak ones before
they cost effort, and names for each survivor the one assumption it most depends
on and the cheapest way to find out if it holds. It is the convergent half;
`ideation-engine` is the divergent half.

## 1. Pressure-test the premise

Each idea rests on a premise: a real audience has this need and would use or pay
for this. Test the premise before the idea.

```
premise     restate the idea's core premise as a falsifiable claim
challenge   what would have to be true for it to work, and is it
reality     confront the premise with what is actually known: does the audience
            exist, is the need real, do they currently solve it another way, would
            they switch
kill early  a premise that fails here kills the idea now, cheaply, which is a
            success of evaluation, not a failure of the idea
```

Killing a doomed idea in evaluation is worth more than building it and learning
the same thing in six months.

## 2. Score against the criteria, for the real actor

```
criteria    feasibility, value to the audience, fit to the actor, cost, risk, per
            opportunity-core, with the binding constraint weighted highest
reason      each score carries its one-line reasoning; a bare number is a guess
actor       scored for this actor's real skills, resources and time, not in the
            abstract; an idea that needs what the actor lacks scores down for them
compare     the scores rank the ideas against each other, surfacing the real
            trade-offs, not a single winner declared prematurely
```

## 3. The riskiest assumption

Every idea has one assumption that, if wrong, sinks it. Find it.

```
identify    the single assumption the idea most depends on and is least sure of:
            usually about demand, willingness to pay, or a technical unknown
test        the cheapest, fastest way to find out if it holds: a landing page, ten
            customer conversations, a spike, a search of existing solutions and
            their reviews; a test measured in days, not months
order       test the riskiest assumption first; there is no point de-risking the
            easy parts of an idea whose hard part is unproven
```

## 4. Recommend with reasoning and validation

```
shortlist   the ranked few, each with why it survived and what it would demand
rejected    the ideas killed and the premise or score that killed them, so the
            actor sees the reasoning, not just the survivors
validate    for each survivor, the validation plan: the riskiest assumption and the
            cheap test for it, as the immediate next step
honest      when no idea survives the pressure test, say so; that is a real, useful
            finding that saves the actor from building the least-bad option
```

## 5. Prohibitions

- Never score an idea without confronting its premise with reality first.
- Never give a score without its reasoning.
- Never evaluate in the abstract when a real actor will pursue it.
- Never rank without naming each survivor's riskiest assumption and its test.
- Never recommend building before the riskiest assumption is cheaply testable.
- Never manufacture a winner from a set that all failed the premise test.
- Never treat killing an idea as a failure; killing a doomed idea early is the job.

## 6. Protocol

1. For each idea, restate and pressure-test its premise against reality; kill
   what fails.
2. Score the survivors on the criteria for the real actor, with reasoning.
3. Rank them, surfacing the trade-offs.
4. For each survivor, identify the riskiest assumption and the cheapest test.
5. Recommend the ranked few with reasoning; show the rejects and why.
6. Give each survivor a validation plan led by its riskiest-assumption test.
7. If none survives, report that honestly with the reasoning.

## 7. Auto-critique

Score from 0 to 5: premises pressure-tested against reality before scoring, weak
ideas killed early, scores carry reasoning, evaluation is for the real actor,
each survivor's riskiest assumption named with a cheap test, recommendation ranked
with rejects shown, validation plan concrete, an all-fail result reported honestly.

Threshold: no axis below 3, average at least 4. A recommendation to build before
the riskiest assumption is identified and testable, or a manufactured winner from
a failed set, caps the score until fixed.

## 8. Interfaces

- Upstream: `opportunity-core` for the criteria, `ideation-engine` supplies the
  set to converge.
- Downstream: `project-brief` and `delivery-orchestrator` take the chosen idea to
  execution; `hackathon-strategy` uses it to pick a hackathon project;
  `technology-selection` when the survivor becomes a build.
- Lateral: `market-research` and `client-discovery` to test a demand assumption
  with real evidence; `self-critique` for the skeptic role.

## 9. The validation mindset

The output of evaluation is not "build this"; it is "this is the most promising,
and here is the cheapest way to find out if it is real before committing." An idea
that survives evaluation still carries an untested riskiest assumption, and the
recommendation's first action is always to test it, not to build. This is what
separates evaluation from endorsement: it hands the actor a de-risking step, not
a green light.

## 10. Note on killing ideas

The most valuable evaluation often ends with fewer survivors than the actor hoped,
or none. A clear, reasoned "none of these survive contact with reality, and here
is why" saves months. Delivering it requires resisting the pressure to recommend
the least-bad option as if it were good. Rank honestly, and when the field is
weak, say so and point back to `ideation-engine` with what the failures taught.
