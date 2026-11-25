# Fixture: extract-codebase-overview (abridged)

## Step 2.5 -- Source census

Deterministic, runs before any prose. Denominator from `git ls-files`; `census_method: git-ls-files`
(or `find` with a named exclude list when the repo has no git). `walk_scope` records the dirs
the walk could enter, the depth cap, and `parallelism`.

Numerator is `files_cited` -- distinct paths appearing in `[found:]` citations. Never
`files_read`: it undercounts, and it is the only number a third party can audit from the
artifact alone.

**Persist as `## Coverage` section**, placed first in the body.

## Step 15 -- check 7 (coverage sweep)

`seen < present` with no `[SAMPLED: <seen>/<present> <unit>]` on the heading -> FAIL.
`seen == present` with the marker present -> FAIL. Never halts; flags only.
