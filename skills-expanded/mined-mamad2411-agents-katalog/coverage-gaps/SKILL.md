---
name: coverage-gaps
description: Analyze what a change leaves untested and propose the specific missing test cases. Use when the user asks what isn't covered, where the test gaps are, or whether a change is adequately tested.
---

# coverage-gaps — find what a change leaves untested

Analyze a change against its tests and name the specific behaviors that no test
protects, then propose the cases that would close the gaps.

## 1. Map the change surface

Collect the change yourself (`git diff`, `git show`) and read it. List every
behavior it introduces or alters: new branches, new inputs, new error paths,
new edge conditions. This is the set that SHOULD be covered.

## 2. Map what the tests actually exercise

Read the existing and new test files, and — when the repo supports it — dispatch
the runner (`purpose: explore` / `search`) to run the suite under coverage
(`pytest --cov`, `go test -cover`, `nyc`, etc.) and report which lines and
branches are hit. Coverage numbers show reached lines; you still judge whether
the behavior is actually ASSERTED, not just executed.

## 3. Name the gaps

For each behavior from step 1 with no meaningful test, write a gap:

    ### Gap: <behavior left untested>
    - **Location**: file:line (the code path)
    - **Missing case**: <the input / condition no test exercises>
    - **Proposed test**: <one-line arrange/act/assert to close it>

Rank by risk: error paths and edge cases that would fail silently first, cosmetic
gaps last.

## 4. Close or hand off

Author the missing tests yourself (see the write-tests skill), then dispatch the
runner to confirm they pass. If the analysis is the deliverable, present the
ranked gap list so the author knows exactly what to add.
