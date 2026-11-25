---
name: opportunity-core
description: Constitution of the opportunity family: the shared discover-then-evaluate method behind ideation, hackathons and business research, the rule that an opportunity (an idea's premise, a hackathon, a lead, a market) is grounded in reality and never fabricated, the evaluation discipline that ranks before it recommends, and the refusal to mistake a long list for a good answer. Load before generating ideas, finding hackathons, or researching clients and markets.
license: MIT
metadata:
  category: ideation
  version: 1.0.0
  depends_on: []
  outputs: [opportunity-method, grounding-standard, evaluation-discipline, shortlist]
---

# Opportunity Core

The rules the opportunity skills share and none restates. Ideation, hackathon
work and business research look different and run the same method: discover a
field of possibilities, then evaluate them against reality, then recommend a
few, never dump a hundred. This constitution holds that method and the honesty
that keeps it useful.

Loaded first, depends on nothing, usable alone.

## 1. Discover, then evaluate, then recommend

A long list is the easy half and the useless half. The value is in the second and
third steps, which most idea generation skips.

```
discover    generate or find the field of possibilities: ideas, hackathons, leads,
            market segments; broad, divergent, without premature judgement
evaluate    test each against reality: feasibility, fit, constraint, value, risk;
            convergent, honest, ranked
recommend   a few, with the reasoning; the point of the work is the shortlist and
            why, not the long list it came from
```

A skill in this tree that stops at discovery has done a third of its job. The
discipline is finishing the other two thirds.

## 2. Grounded in reality, never fabricated

Each category has a thing that must be real, and the rule is the same: it is
grounded in something verifiable, or it is marked as a hypothesis, never
presented as fact.

```
ideation    an idea rests on a real problem a real audience has, not an invented
            need; the premise is stated as a hypothesis to test, not a certainty
hackathons  a hackathon is a real event with a real link, deadline and eligibility,
            from a live source; never an invented event
business    a lead, a client, a competitor, a market figure is real and sourced;
            never a fabricated company or a made-up statistic
```

This is the opportunity form of the evidence rule. A fabricated opportunity costs
someone real time and real effort chasing something that is not there.

## 3. Evaluate against stated criteria

```
criteria    the axes that decide, named before scoring: feasibility, fit to the
            person or team, value to the intended audience, cost, risk, and the
            constraint that actually binds (time, budget, eligibility, skill)
score       each possibility against the criteria, with the reasoning, not a bare
            number; a score whose reasoning cannot be stated is a guess
weight      the criteria are not equal; the binding constraint dominates, and an
            idea that fails it is out regardless of how appealing it is elsewhere
```

## 4. Fit to the actor

An opportunity is good only relative to who pursues it. The same idea is excellent
for one team and wrong for another.

```
who         the real person or team: their skills, resources, time, constraints,
            and goals, from the configuration or the brief
match       an opportunity is evaluated for this actor, not in the abstract; a
            brilliant idea that needs skills the team does not have is a bad
            recommendation for that team
honest      a recommendation names why it fits this actor, and what pursuing it
            would demand of them
```

## 5. The shortlist, with reasoning

```
few         a small number of strong possibilities, ranked, each with why it made
            the cut and what it would take
rejected    the notable possibilities that did not make it, and why, so the actor
            sees the space was explored, not just the survivors
next        for each shortlisted possibility, the concrete next step: the test to
            run, the application to file, the outreach to make
honest      when nothing scores well, say so; a weak field honestly reported beats
            a strong-sounding recommendation the evidence does not support
```

## 6. Prohibitions

- Never stop at a long list; evaluate and recommend.
- Never present an ungrounded premise, an invented event, or a fabricated lead as
  real; mark a hypothesis as a hypothesis.
- Never invent a hackathon, a deadline, a company, or a market statistic.
- Never score without stating the reasoning behind the score.
- Never evaluate an opportunity in the abstract when a real actor pursues it.
- Never recommend an opportunity that fails the binding constraint.
- Never manufacture a strong recommendation from a weak field.

## 7. Protocol

1. Establish the actor: skills, resources, time, constraints, goals.
2. Discover the field broadly, without premature judgement.
3. Ground each possibility in something real, or mark it a hypothesis.
4. Name the evaluation criteria and the binding constraint before scoring.
5. Score each against the criteria for this actor, with reasoning.
6. Recommend a ranked shortlist, with why each made it and the notable rejects.
7. Give each shortlisted possibility a concrete next step.

## 8. Auto-critique

Score from 0 to 5: the work goes past discovery to evaluation and recommendation,
every possibility grounded or marked hypothesis, criteria and binding constraint
named before scoring, scores carry reasoning, evaluation is for the real actor,
shortlist ranked with rejects shown, next steps concrete, a weak field reported
honestly.

Threshold: no axis below 3, average at least 4. A fabricated opportunity (an
invented event, lead, or statistic), or a long list with no evaluation, is an
automatic zero regardless of the average.

## 9. Interfaces

- Downstream, this tree: `ideation-engine`, `idea-evaluation`,
  `hackathon-discovery`, `hackathon-strategy`, `pitch-and-demo`,
  `client-discovery`, `lead-research`, `market-research` refer to this
  constitution and do not restate it.
- Other trees: `research-core` in `research/` supplies the source discipline the
  business skills apply; `delivery-orchestrator` and `project-brief` take a chosen
  opportunity into execution; `technology-selection` when an idea becomes a build.
- Lateral: `self-critique` for the skeptic and target-audience role passes.

## 10. The two halves

Discovery and evaluation are different cognitive acts, and the common failure is
doing only the first because it is generative and fun. This tree treats the long
list as raw material, not output. The deliverable is always the ranked few with
their reasoning and their next steps, and the honest statement when the field is
thin. A hundred ideas is not an answer; three evaluated ones are.
