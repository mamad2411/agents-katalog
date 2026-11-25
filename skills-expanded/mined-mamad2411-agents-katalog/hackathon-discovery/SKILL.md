---
name: hackathon-discovery
description: Finds real hackathons that match a person or team from live sources, never invented: builds the search from the participant's skills, eligibility, location, availability and interests, queries the reachable hackathon listings, and reports each event with its real link, dates, eligibility rules, prizes and theme, plus an honest fit assessment. Verifies deadlines and eligibility against the source, because a missed rule wastes the effort. Use to find hackathons worth entering.
license: MIT
metadata:
  category: hackathons
  version: 1.0.0
  depends_on: [opportunity-core]
  outputs: [search-profile, matched-hackathons, eligibility-check, entry-shortlist]
---

# Hackathon Discovery

A hackathon is a real event with a real deadline, real eligibility rules and a
real registration link. This skill finds the ones that fit a participant and
reports them from live sources, because an invented hackathon, or a real one with
a misremembered deadline or eligibility rule, sends someone to build for nothing.

## 1. Build the search from the participant

```
skills      what the person or team can build, which decides which themes and
            tracks they can realistically compete in
eligibility the hard filters: location or online, student or open, age, region,
            team size, first-timer status; an event the participant cannot enter is
            not a match however appealing
availability the real time window: the dates they are free, the hours they can
            commit; a hackathon during an unavailable week is out
interests   the domains and problem types that motivate them; motivation sustains
            a weekend build
goals       why they are entering: to win, to learn, to network, to build a
            portfolio piece; the goal changes which events fit
```

## 2. Query live sources only

```
sources     the hackathon aggregators, platform listings, and any connector the
            runtime can reach
real        every event exists at its source with a real registration link
dates       the registration deadline and the event dates as the source states them
eligibility the rules as the source states them, read carefully, not assumed from
            the event's name or reputation
unreachable if no live source can be reached, say so and give the participant the
            exact places to search, with the filters; never invent events
```

This is opportunity-core's grounding rule for hackathons: an event that cannot be
traced to a live source is not reported as an event.

## 3. Verify eligibility and deadline against the source

```
eligibility read the actual rules: a "global" hackathon may exclude certain
            regions for prizes; a "student" event may define student narrowly; a
            team event may have a size limit; verify against the source, not the
            summary
deadline    the registration deadline and the submission deadline are different
            dates; report both, from the source; a deadline is never invented or
            approximated when the source states it exactly
window       confirm the event fits the participant's stated availability
```

A missed eligibility rule or a wrong deadline wastes the entire effort, which is
why this step is verified against the source and not taken on trust.

## 4. Report and shortlist

```
event       the name, organiser, theme, and tracks, from the source
fit         honest assessment against the participant's skills, interests, and
            goals: strong, worth considering, or a stretch
eligibility confirmed, with any rule the participant must meet
dates       registration deadline and event dates
prizes      what is actually offered, from the source
link        the real registration link
shortlist   the few worth entering, ranked by fit and goal, with the effort
            guidance: one well-chosen hackathon entered fully beats three half-done
```

## 5. Prohibitions

- Never invent a hackathon, a deadline, an eligibility rule, a prize, or a link.
- Never report an event that cannot be traced to a live source.
- Never state an eligibility rule from the event's name or reputation without
  reading the actual rules.
- Never approximate a deadline the source states exactly.
- Never recommend an event the participant is ineligible for or unavailable during.
- Never oversell a stretch event as a strong fit.
- Never register on the participant's behalf without explicit confirmation.

## 6. Protocol

1. Build the search profile: skills, eligibility, availability, interests, goals.
2. Query the reachable live sources; if none, say so and hand over the search.
3. Confirm each event is real with a real link and stated dates.
4. Verify eligibility and both deadlines against the source; confirm the window.
5. Assess fit honestly against skills, interests, and goals.
6. Shortlist the few worth entering, ranked, with effort guidance.
7. Pass the chosen event to `hackathon-strategy`.

## 7. Auto-critique

Score from 0 to 5: search built from the participant's real profile, every event
from a live source with a real link, eligibility and both deadlines verified
against the source, availability confirmed, fit honest, shortlist ranked with
effort guidance, nothing invented.

Threshold: no axis below 3, average at least 4. A single invented event, deadline,
eligibility rule, or link is an automatic zero regardless of the average, per
opportunity-core.

## 8. Interfaces

- Upstream: `opportunity-core` for the grounding rule.
- Downstream: `hackathon-strategy` plans the chosen event, `ideation-engine` and
  `idea-evaluation` generate and choose the project, `pitch-and-demo` for the
  submission.
- Lateral: `source-verification` in `research/` when an event's legitimacy is in
  doubt; `career-core`'s configuration overlaps with the participant profile.

## 9. Live sources and connectors

This skill reads whatever hackathon and search sources the runtime exposes: an
aggregator, a platform connector, web search and retrieval. It reads and prepares;
it does not register on the participant's behalf without explicit confirmation.
When a source cannot be reached, it names the aggregators and filters the
participant should use themselves, rather than inventing events, because a
participant will commit a weekend on the strength of what it reports.

## 10. Note on the participant profile

The search profile overlaps with the career configuration (skills, location,
availability) and can be seeded from it, but the goals differ: a hackathon is
entered to win, learn, network, or build a portfolio piece, and that goal reshapes
which events fit. A learner is matched to beginner-friendly events; a competitor
to ones with a real prize and strong fit; a networker to ones with the right
community. The goal is asked if not stated, never assumed from the skills alone.
