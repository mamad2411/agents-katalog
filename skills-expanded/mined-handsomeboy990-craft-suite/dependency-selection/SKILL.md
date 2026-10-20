---
name: dependency-selection
description: Decides whether to add, replace, upgrade or refuse a library through a twelve point evaluation covering existing solutions, platform capabilities, maintenance, security, licence, size, transitive tree, types, accessibility and migration cost. Use before any dependency change.
license: MIT
metadata:
  category: dev-skills
  version: 1.0.0
  depends_on: [engineering-core, project-exploration]
  outputs: [dependency-decision, evaluation-record, migration-plan]
---

# Dependency Selection

A dependency is a permanent liability accepted for a temporary convenience.
Sometimes that trade is excellent. It is never free, and it is never reversed
casually.

## 1. The three questions before the evaluation

Asked in order. Two of them end the discussion most of the time.

1. **Does the project already solve this?** Search the codebase and the
   installed tree. Adding a second date library, a second HTTP client, a
   second validation library or a second state manager is a defect.
2. **Does the platform solve this?** Standard library, runtime API, framework
   feature. Many dependencies exist because they predate a platform feature
   that now ships everywhere the project runs.
3. **Is the problem small enough to own?** Fifty lines the team understands
   beat a package with nine transitive dependencies for a formatting helper.
   The inverse is also true: cryptography, date arithmetic across timezones,
   parsers and accessibility primitives are not written by hand.

## 2. The twelve point evaluation

Applied only to candidates that survive section 1.

| # | Criterion | Reject when |
|---|---|---|
| 1 | solves the actual need | it solves a superset and the excess is most of the cost |
| 2 | framework and runtime compatibility | it needs a version the project cannot adopt |
| 3 | maintenance | no release or no answered issue in a long period, single maintainer with no succession |
| 4 | security | known unfixed advisories, or a history of slow response |
| 5 | licence | incompatible with the project's distribution |
| 6 | size | the bundle or runtime cost exceeds the benefit, measured |
| 7 | transitive tree | it pulls in a large tree, or a package with a poor reputation |
| 8 | types | no types, or types that lie, in a typed project |
| 9 | accessibility | a UI library whose components are not keyboard operable |
| 10 | documentation | the answer to a normal question requires reading the source |
| 11 | escape cost | it captures the data model or the API surface so deeply that leaving is a rewrite |
| 12 | alternatives | a smaller or already present option covers the need |

Each criterion is answered with evidence: a version number, a date, a
measured size, a licence identifier. Not an impression.

## 3. Measuring the cost

Never estimated when it can be measured.

```
Bundle impact     build before and after, compare the output size
Install impact    count the added packages in the lockfile diff
Runtime impact    the operation timed with and without, where it matters
Transitive risk   read the lockfile diff, not the manifest line
```

A single manifest line that adds ninety packages is ninety packages of
maintenance, audit surface and install time.

## 4. The decision record

```
Need           what the project cannot currently do
Existing       what was searched, and why it does not cover the need
Platform       what the platform offers, and why it is insufficient
Candidates     two or three, with the twelve points answered
Decision       chosen, with the deciding criterion named
Cost           packages added, bundle delta, licence
Escape         what leaving costs, in one sentence
```

Recorded where the project keeps decisions, or in the continuity notes when it
has no such place.

## 5. Upgrades

| Kind | Approach |
|---|---|
| patch | apply, run the suite, ship |
| minor | read the release notes, apply, run the suite, check the touched paths |
| major | read the migration guide, plan, apply in its own commit, test the changed behaviour explicitly |
| security | apply promptly, judge the reachability of the advisory, do not assume it applies |

Rules: one dependency change per commit, so a regression can be bisected.
Never upgrade a major version inside a feature commit. Never apply a bulk
update across a whole tree without reading what changed.

## 6. Removal

A dependency that is no longer used is removed in its own commit. Check the
lockfile, not the manifest, to confirm nothing else pulls it in. Removing a
package that another package depends on transitively changes nothing except
the manifest, and pretending otherwise is a false cleanup.

## 7. Refusals

Refuse, with the reason stated once:

- a second library for a problem already solved in the project;
- a package for a task the platform performs in a few lines;
- an unmaintained package chosen because it is familiar;
- a UI library whose components fail keyboard operation;
- a package whose licence conflicts with the project's distribution;
- a heavy library imported for one function that can be imported alone;
- a framework adopted inside a feature commit.

## 8. Protocol

1. Ask the three questions of section 1. Stop if answered.
2. Identify two or three candidates.
3. Answer the twelve points for each, with evidence.
4. Measure the cost, section 3.
5. Decide, naming the deciding criterion.
6. Install with the project's package manager, exactly.
7. Read the lockfile diff before committing it.
8. Run the security audit command and the test suite.
9. Record the decision.
10. Commit the dependency change alone.

## 9. Auto-critique

Score from 0 to 5: existing solution genuinely searched, platform capability
considered, evidence behind each criterion, cost measured rather than
estimated, alternatives real rather than straw men, escape cost stated,
commit isolated.

Threshold: no axis below 3, average at least 4. A decision with no measured
cost and no named alternative is not a decision, it is a preference.

## 10. Interfaces

- Upstream: `architecture-design`, `project-exploration`,
  `ui-ux-engineering` for UI libraries.
- Downstream: `security-audit` for the advisory check,
  `performance-engineering` for the size impact, `testing-quality`,
  `git-workflow` for the isolated commit, `technical-documentation`.
