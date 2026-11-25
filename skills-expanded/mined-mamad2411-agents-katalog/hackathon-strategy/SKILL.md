---
name: hackathon-strategy
description: Plans a hackathon entry to win within its real constraints: reads the judging criteria and builds toward them, chooses a project scoped to the time and team rather than an ambitious one that will not finish, plans the build so a working demo exists early and improves, allocates the team, and protects the demo and the submission from the last-hour collapse that loses winnable hackathons. Use once a hackathon is chosen, to turn a weekend into a placing entry.
license: MIT
metadata:
  category: hackathons
  version: 1.0.0
  depends_on: [opportunity-core]
  outputs: [judging-strategy, scoped-project, build-plan, team-allocation]
---

# Hackathon Strategy

Most hackathon projects lose not to better ideas but to worse scoping: a team
builds something too ambitious, has nothing working at the deadline, and demos a
broken half. This skill plans an entry that wins within the real constraints, by
building toward the judging criteria with a project small enough to finish and
polished enough to place.

## 1. Build toward the judging criteria

```
read        the actual judging criteria, from the event; they are usually
            published and they decide everything
weight      criteria are weighted: if "impact" is 40% and "technical difficulty"
            is 10%, an impressive technical feat with a weak impact story loses to
            a simple project with a strong one
build for   scope the project so it scores on the heaviest criteria; a hackathon
            is optimised for the rubric, not for the team's idea of impressive
demo        most rubrics reward a working demo heavily; a project that demos beats
            a more sophisticated one that does not run
```

Ignoring the rubric is the most common strategic error. Read it first, and let it
shape the project.

## 2. Scope to the time and team, ruthlessly

```
constraint  the real hours available and the real team, per opportunity-core's
            binding constraint; a 24-hour hackathon is not a 24-hour workday
minimum     the smallest project that tells a complete story and scores on the
            heavy criteria; a whole, small thing beats a broken, big thing
cut early   decide before building what is core and what is optional; the optional
            is only touched if the core works and time remains
demo path   scope so that the demo, the thing judges see, is the part that works;
            never let the impressive-but-fragile feature be the one on stage
```

## 3. Plan for a working demo early

```
early       a working end-to-end skeleton, however thin, in the first third of the
            time; something that runs and can be demoed even if nothing else lands
improve     from the skeleton, deepen the parts that score, in priority order;
            every increment keeps the demo working
freeze      a hard stop before the deadline: no new features after it, only
            polish, demo rehearsal, and submission; the last hours are for landing,
            not reaching
buffer      time reserved for the demo recording, the submission form, and the
            things that always break at the end
```

A team with a working demo at the two-thirds mark and time to polish beats a team
still integrating at the deadline, every time.

## 4. Allocate the team

```
strengths   assign to strengths: the strong frontend person on the demo surface,
            the strong backend on the core, someone owning the pitch from the start
parallel    partition the work so people are not blocked on each other; a clean
            interface between parts lets them build in parallel
pitch       the pitch and demo are not an afterthought assigned at hour 23; one
            person shapes the story throughout, so the build serves it
solo        for a solo entry, the same discipline compressed: scope smaller, demo
            earlier, protect the submission time
```

## 5. Protect the submission

```
submission  the submission form, the demo video, the repository, the write-up: all
            take longer than expected and are done inside the reserved buffer, not
            in the final frantic minutes
rehearse    the live or recorded demo is rehearsed; a demo that works but is
            fumbled loses to a clear one
requirements   re-read the submission requirements before the deadline: a required
            field, a specific format, a theme statement; a disqualification on a
            technicality wastes the whole weekend
```

## 6. Prohibitions

- Never build without reading the judging criteria first.
- Never scope an ambitious project that will not finish; a whole small thing wins.
- Never let the fragile feature be the one demoed.
- Never leave the working demo to the last third of the time.
- Never treat the pitch and submission as an afterthought.
- Never skip re-reading the submission requirements before the deadline.
- Never add features after the freeze; the last hours are for landing and polish.

## 7. Protocol

1. Read the judging criteria and their weights; identify the heaviest.
2. With `ideation-engine` and `idea-evaluation`, choose a project scoped to the
   time and team that scores on the heavy criteria.
3. Plan the build: a working skeleton early, priority-ordered improvements, a
   feature freeze, and a submission buffer.
4. Allocate the team to strengths, in parallel, with the pitch owned throughout.
5. Build to a working demo early; improve the scoring parts; freeze on schedule.
6. Inside the buffer: polish, rehearse the demo, complete the submission, re-read
   the requirements.

## 8. Auto-critique

Score from 0 to 5: judging criteria read and built toward, project scoped to
finish, demo path is the working path, working demo planned early with a freeze,
team allocated to strengths in parallel, pitch owned throughout, submission and
requirements protected in a buffer.

Threshold: no axis below 3, average at least 4. A plan that builds an unfinishable
scope, or leaves the demo and submission to the final hour, caps the score until
fixed.

## 9. Interfaces

- Upstream: `opportunity-core` for the binding constraint, `hackathon-discovery`
  for the chosen event and its rules, `ideation-engine` and `idea-evaluation` for
  the project choice.
- Downstream: `pitch-and-demo` for the presentation; the engineering tree
  (`frontend-engineering`, `backend-engineering`, `fullstack-engineering`) builds
  the scoped project fast.
- Lateral: `project-brief` compressed to a weekend; `self-critique` for the judge
  role pass on the plan.

## 10. The scoping principle

The single lesson that wins more hackathons than any other: finish something
whole and small, then make it better, rather than build something big and demo it
broken. Judges reward a complete, working, well-told project over an ambitious
one that does not run. Every strategic decision, what to build, what to cut, when
to freeze, serves that principle. The team that internalises it beats more
talented teams that do not.
