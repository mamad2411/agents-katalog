---
name: career-profile
description: Builds the candidate's foundational profile that every other career skill reads: the real inventory of skills with honest levels, the experience history with quantified results, the target roles and their requirements, the strengths and the genuine gaps, and the narrative that ties a non-linear history into a coherent direction. The source of truth a CV, a search and an interview all draw from. Use first in any career work, and when the candidate's direction changes.
license: MIT
metadata:
  category: career
  version: 1.0.0
  depends_on: [career-core]
  outputs: [skill-inventory, experience-history, target-definition, career-narrative]
---

# Career Profile

Every other career skill draws from one source: an honest, structured account of
who the candidate is and where they are going. Built once and maintained, it
stops the CV, the search and the interview prep from each inventing their own
version of the candidate. This skill builds that source.

## 1. The skill inventory, with honest levels

```
list       what the candidate can actually do, grouped by kind (technical,
           domain, interpersonal, tools)
level      an honest level for each: can do independently, can do with support,
           learning, aware of. A skill claimed above its real level surfaces at
           the interview, per career-core.
evidence   for each strong skill, the experience that proves it, so it is not a
           bare assertion
```

## 2. The experience history, quantified

```
role       title, organisation, dates, real and unembellished
results    what was achieved, quantified where honest numbers exist: a percentage,
           a count, a time, a scale; a real number beats a vague strong verb
scope      the size and stakes of the work, so a reader gauges the level
verb       the accurate action verb: led, built, coordinated, supported,
           contributed; not inflated past the real role
```

A result with a true number ("cut onboarding from three weeks to five days") is
worth more than any adjective, and it is the raw material the CV and interview
will both use.

## 3. Target roles and their requirements

```
targets    the roles the candidate is pursuing, from the configuration
require    what those roles actually ask for, from real listings, not assumption
map        the candidate's inventory against those requirements: met, partly,
           gap, so the search and the CV emphasise the met, and the prep and the
           learning plan address the gaps
```

## 4. Strengths and genuine gaps

```
strengths  the requirements the candidate meets strongly, which the CV leads with
           and the search filters on
gaps       the requirements the candidate does not meet, named honestly, not hidden
transfer   where a strength from one domain covers a requirement in another, the
           bridge is made explicit (the teaching-to-product case)
close      each real gap gets a path: a project, a course, a certification, or an
           honest "this role is a stretch and here is why it is still worth trying"
```

## 5. The narrative

A non-linear history reads as drift unless a narrative ties it together. The
narrative is true and it is chosen.

```
thread     the real through-line: the kind of problem the candidate keeps solving,
           the direction the moves have trended, the skill that compounds across roles
frame      each past role as a step toward the target, where that is honest;
           a genuine pivot is named as a pivot, not disguised as a straight line
own        a gap in dates or a short tenure is addressed, briefly and honestly,
           not left as a silent question the recruiter fills with the worst guess
```

## 6. Prohibitions

- Never record a skill above the level the candidate can support.
- Never inflate a title, a result, or a scope beyond the real role.
- Never invent a number; an honest range or a qualitative result beats a false figure.
- Never hide a genuine gap; name it and give it a path.
- Never assume a target role's requirements; take them from real listings.
- Never disguise a career pivot as a straight line; a true pivot is a strength
  when it is owned.

## 7. Protocol

1. Read the `career` configuration; ask once for what is missing (career-core).
2. Build the skill inventory with honest levels and the evidence for each.
3. Build the experience history with quantified, true results and accurate verbs.
4. Take the target roles' real requirements from actual listings.
5. Map the inventory against the requirements: met, partly, gap.
6. Name the strengths to lead with and the gaps to close, each with a path.
7. Write the narrative: the true through-line, pivots owned, gaps addressed.
8. Store the profile as the source the other career skills read.

## 8. Auto-critique

Score from 0 to 5: skills at honest levels with evidence, experience quantified
and un-inflated, target requirements from real listings, honest met/partly/gap
map, strengths and gaps both named, gaps given a path, narrative true with pivots
owned.

Threshold: no axis below 3, average at least 4. A skill or result recorded above
what the candidate can support caps the score until corrected, per career-core.

## 9. Interfaces

- Upstream: `career-core` sets the honesty standard and the configuration.
- Downstream: `cv-engineering` renders the profile as a CV, `job-search` filters
  on the strengths and targets, `cover-letter` draws the narrative,
  `interview-preparation` drills the gaps and rehearses the results.
- Lateral: `self-critique` for the recruiter role; `synthesis-reporting` when the
  target-role requirements come from a structured market scan.

## 10. Maintenance

The profile is the career equivalent of project continuity: built once, updated
when the candidate gains a skill, finishes a project, or changes direction. A
stale profile produces a CV that describes last year's candidate. It is refreshed
before a new search, not reconstructed from memory each time.
