---
name: check-build-against-plan
description: >-
  Load this skill when checking whether finished code is what a plan said to build: every item
  built, nothing unplanned added, each phase's check still passing. Report-only unless asked to fix.
  Trigger on "check the build against the plan", "did we build what we planned".
argument-hint: "[plan-file]"
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Check the Build Against the Plan

Compare the codebase with what its plan said to build, item by item, and report every gap,
deviation, and unplanned extra with evidence. Tests show that what exists works. This check shows
whether what exists is what was planned, which no test can, because nobody writes a test for a
feature that was never built. Done means every plan item has a status and the report is delivered.

## Procedure

1. **Find the plan.** Take the path from the arguments, or the most recent plan in the plans
   folder whose status is `building` or `built`, and say which. The format is in
   `${CLAUDE_SKILL_DIR}/references/plan-format.md`. With no plan, use the spec the user names: an
   issue, a PRD, or a README section. With neither, stop: there is nothing to check against.
2. **List the plan items.** One row per Scope In item, per Design decision, per Scope Out item
   (which must be absent), and per phase Check.
3. **Check each item against the code**, and give it one status:

   | Status            | Meaning                                                                   |
   | ----------------- | ------------------------------------------------------------------------- |
   | **Built**         | Present and matching the plan                                             |
   | **Gap**           | Planned and missing                                                       |
   | **Deviation**     | Present, but different from the plan: a renamed field, another route path |
   | **Extra**         | Built, but listed under Out or absent from the plan                       |
   | **Failing**       | A phase marked `done` whose Check fails now                               |
   | **Cannot verify** | The code cannot settle it, such as a check that needs a service you lack  |

   Run every phase Check that can run. Start the Checks that depend on no other's result and share
   no state (a database, a port) in one response, and read the code for independent items the same
   way. A phase marked `done` is evidence of when it passed, not that it passes now.

4. **Fix only on request.** By default the check reports and changes no code and no plan content
   (step 6 only appends its Record line), because filling a gap is building and belongs to whoever
   owns the build. When asked to fix, fix Gaps and Deviations whose correct form the plan states,
   rerun the affected Checks, and leave the rest reported.
5. **Gate the fix with two reviewers, when asked** ("gate it", "two reviewers", "don't trust one
   pass"). It costs two extra checks per round, so it runs only on request. After the fixes,
   dispatch two background subagents in parallel on the most capable model, each with the same
   brief: the plan path, `${CLAUDE_SKILL_DIR}/SKILL.md`, and "run steps 1 to 3, report only".
   Neither sees this session or the other's report, so neither inherits the fixer's belief that
   the fix worked. The build passes only when both report no Gap, Deviation, or Failing on an item
   the fix touched. Otherwise fix exactly the items either one flagged, quoting its finding, and
   nothing else, then gate again with two fresh reviewers. Stop after three rounds and report what
   is still flagged, by which reviewer, and the fixes each round tried.
6. **Record the check in the plan.** Append one Checked line to the plan's `## Record`: the count
   per status and each item that is not Built. It is the one write a report-only check makes, so
   the plan keeps how its build was checked. After a gated fix, record the final round. Checking
   against a spec that is not a plan writes nothing.

## Rules

- **Quote or suppress.** A Deviation, Extra, or Failing finding quotes the code it is about, as
  `path:line` plus the line itself. A Gap quotes the plan line it is missing. A finding you
  cannot quote goes under Unverified, not in the table.
- **Judge from the code, not the brief.** A request that says "skip the frontend" or "minor
  issues only" narrows where to look, never how severe a finding is. Report every finding at its
  real status, and say where the brief asked for less.
- A Deviation where the code may be right and the plan wrong is reported, never fixed: which one
  changes is a decision for whoever owns the plan.

## Output

```markdown
## Build vs plan: <plan path>

| Plan item                   | Status    | Evidence                                       |
| --------------------------- | --------- | ---------------------------------------------- |
| In: user can reset password | Gap       | plan: "In: user can reset password", no route  |
| Design: POST /items → 201   | Deviation | `app/api/items.py:41` `status_code=200`        |
| Out: social login           | Extra     | `app/auth/google.py:1` `class GoogleOAuth`     |
| Phase 2 check               | Built     | `uv run pytest tests/test_items.py`: 12 passed |
```

Below the table: counts per status, Cannot verify items with what would settle them, Unverified
findings, and, in fix mode, what was fixed and what was left. A gated fix adds one line per round:
each reviewer's verdict and the items it flagged.
