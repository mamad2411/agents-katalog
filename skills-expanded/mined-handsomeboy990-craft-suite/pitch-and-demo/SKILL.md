---
name: pitch-and-demo
description: Builds the pitch and demo that a hackathon, a demo day, or an investor meeting is actually judged on: a story that leads with the problem and the stakes, a demo that shows the working thing rather than describing it, a structure that fits the time limit, honest claims a judge can trust, and a rehearsed delivery that survives nerves and a failing wifi. Use to prepare a presentation of a built thing, and to turn a working project into a winning one.
license: MIT
metadata:
  category: hackathons
  version: 1.0.0
  depends_on: [opportunity-core]
  outputs: [pitch-narrative, demo-script, slide-outline, delivery-plan]
---

# Pitch And Demo

A project is judged on what the judges see and understand in a few minutes, not on
what was built. A strong build with a weak pitch loses to a modest build with a
strong one. This skill turns a working project into a presentation that lands: a
clear problem, a real demo, honest claims, and a delivery that survives the room.

## 1. Lead with the problem and the stakes

```
problem     open with the problem, concretely, so the judge feels it before they
            see the solution; a specific person with a specific pain beats an
            abstract market
stakes      why it matters: who is affected, how much, why now; the impact story
            that most rubrics weight heavily
solution    only then, the solution, as the answer to the problem just felt; the
            build serves the story, the story does not decorate the build
avoid       opening with the technology, the architecture, or the team's cleverness;
            the judge does not yet care, because they do not yet feel the problem
```

## 2. Show the working thing

```
demo        show it working, live or recorded; a demo that runs is the single most
            persuasive thing in the room, and most rubrics reward it heavily
real        the demo shows the actual product doing the actual thing, not slides
            describing it; "let me show you" beats "imagine if"
path        the demo follows the story: the problem, then the product solving it,
            in the order that makes the impact land
focus       demo the part that works and that scores; do not wander into the fragile
            feature or the settings screen; every second of the demo earns its place
```

## 3. Fit the time, ruthlessly

```
limit       the real time limit, respected; a pitch cut off at the buzzer before
            the demo is a loss, and judges enforce the clock
structure   problem, stakes, demo, what is next, in the time given; a two-minute
            pitch has no room for a team-history slide
cut         everything that does not serve the problem-to-demo arc; the technology
            deep-dive, the full roadmap, the acknowledgements
one thing   the judge should leave remembering one thing; name it, and build the
            pitch so that one thing lands
```

## 4. Honest claims

```
true        every claim is something the project actually does or the evidence
            actually supports, per opportunity-core; a judge who catches an
            overclaim discounts everything else
demo-real   the demo shows real behaviour, not a hardcoded happy path presented as
            general capability; if something is faked for the demo, it is not
            claimed as working
future      what is not built yet is framed as "next", not implied as done; the
            honest "here is what works today and where it goes" is more credible
            than a demo pretending to be a finished product
```

## 5. Rehearse and survive the room

```
rehearse    the pitch and demo are rehearsed against the clock, out loud, more than
            once; the first run is always too long and finds the fumbles
fallback    a recorded demo as backup for when the live one fails; wifi dies,
            laptops sleep, and the team that has a fallback keeps its score
handoffs    for a team, clean handoffs between speakers, rehearsed; a scramble over
            who talks next reads as unprepared
questions   anticipate the judges' questions (how does it scale, what is the
            business model, what did you build versus use) and prepare honest answers
```

## 6. Prohibitions

- Never open with the technology; open with the problem the judge must feel.
- Never describe the product when you could show it working.
- Never demo the fragile feature or wander off the story.
- Never overclaim; a caught overstatement discredits the whole pitch.
- Never present a hardcoded demo path as a general capability.
- Never run over the time limit; a cut-off pitch loses the demo.
- Never present without rehearsing against the clock and preparing a demo fallback.

## 7. Protocol

1. Write the narrative: problem, stakes, solution, in that order.
2. Script the demo to follow the story, showing the working, scoring part.
3. Structure the whole to the time limit; cut everything off the problem-to-demo arc.
4. Verify every claim is honest and the demo shows real behaviour.
5. Prepare the one thing the judge should remember.
6. Rehearse against the clock, prepare a recorded fallback, and ready answers to
   likely questions.

## 8. Auto-critique

Score from 0 to 5: opens with the problem and stakes not the technology, shows a
working demo of the scoring part, fits the time with everything off-arc cut, every
claim honest and the demo real, one memorable thing, rehearsed against the clock
with a fallback and prepared answers.

Threshold: no axis below 3, average at least 4. An overclaimed or faked-as-real
demo, or a pitch that opens on technology and never shows the working thing, caps
the score until fixed.

## 9. Interfaces

- Upstream: `opportunity-core` for honesty, `hackathon-strategy` for the project
  and the judging criteria the pitch scores on.
- Downstream: the same pitch adapts to a demo day, an investor meeting, or an
  internal review; `report-writing` in `documents/` for a written version.
- Lateral: `technical-writing` for a demo that needs an explainer;
  `self-critique` for the judge and skeptical-investor role passes.

## 10. Beyond hackathons

The same structure wins a demo day, an investor pitch, and an internal project
review: lead with the problem, show the working thing, claim only what is true,
fit the time, and rehearse. The audience and the weighting change (an investor
weights the market and the model more than a hackathon judge does), and the
problem-first, show-do-not-tell, honest-claims spine is constant. Adapt the
emphasis to the audience; keep the spine.
