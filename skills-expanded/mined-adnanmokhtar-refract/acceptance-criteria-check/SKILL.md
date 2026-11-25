---
name: acceptance-criteria-check
description: "Acceptance criteria: falsifiable and EARS-shaped (ears-lint), each id named by a test, no stale ids, no undefined Gherkin steps."
kind: skill
pack: product
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: acceptance-criteria-check

## Premise

A criterion is verifiable when someone who was not in the room can observe whether it holds. The test is mechanical and gives every reviewer the same answer: **name the observation that would prove this criterion FAILED**. If no such observation exists, the criterion cannot be verified, and the argument about "done" is scheduled for after delivery instead of now. A verifiable criterion that no test names is the same promise one step later: it is found by the first user, not by the suite.

This skill runs two lanes over every criterion in scope:

- **The shape lane** (§4): the four tests (falsifiable, observable, bounded, singular), the seven failure classes and the numeric-bound check, by hand on any spec, and mechanically by `ears-lint.py` when the spec is in the run-ledger format.
- **The trace lane** (§1–§3): criterion ids joined against the tests that cite them, in both directions, and Gherkin scenarios against their step definitions by the runner's own dry run.

**Every criterion in scope gets a row.** No sampling: an unchecked criterion has been silently accepted. **Traceability is id-anchored only**: an id in a spec, the same id in a test. An inferred link ("this test looks like it covers that criterion") is never a trace; model-inferred trace links over-link and trail plain retrieval baselines ([`precedents/product.md`](../../../../snippets/precedents/product.md) § 31).

## The rule

A criterion is a finding when one of these holds, after the read step:

1. **It cannot fail** (§4): no observation refutes it, or its bound is an adjective, or it joins two independently testable claims.
2. **No test names it** (§1): its id appears in no test title, tag, annotation or name, or appears only in a comment. A test that names it but does not assert it is a link, not proof (§ 31).
3. **A test cites an id no spec holds** (§2): the trace is stale, and the gap it hides is invisible.
4. **Its scenario cannot run** (§3): a Gherkin step with no definition, or an ambiguous one. An unused step definition is dead glue.

## Boundaries

- **Inside a delivery run** (`ai/runs/<run_id>/`), the AC → task → test matrix is repo-baseline `trace-matrix.py`, owned by `@verifier`. This skill calls it and reports its orphans; it never re-derives them.
- **Whether a requirement is the right requirement** (ambiguity with two readings, solution in the problem, the coverage grid, non-functional bounds, metric linkage) is `@requirements-reviewer` (delivery pack, the single owner; product dispatches it). This skill supplies its criteria ledger and its falsifiability column; it does not issue the spec verdict.
- **Whether the requirement should exist** is `evidence-trace`; unsourced requirements become ranked tests in `assumption-ledger`.
- **Whether the test is strong** (assertion strength, skipped or never-collected suites, doubles) is the testing pack (`suite-execution-scan`, when installed). A criterion whose only test is skipped is reported here as untested, with the testing row named as corroboration.
- GitHub Spec Kit's `analyze` coverage table is model-judged and traces requirement → task, not requirement → test; it is read as a list of ids, never as evidence of coverage.

## Lanes

| Spec format | Criterion ids | Shape lane | Trace lane |
|---|---|---|---|
| run-ledger `ai/runs/<run_id>/requirements.md` (`### REQ-###`, `- AC-###: …`) | `REQ-###`, `AC-###` | `python3 -I .claude/scripts/ears-lint.py <requirements.md>` (exit 0 clean · 2 findings) | `python3 -I .claude/scripts/trace-matrix.py <run_id>` |
| a spec or ticket in Markdown (`ai/specs/`, `specs/`, `docs/requirements/`) with ids | `AC-12`, `REQ-7`, a project prefix (pre-flight 0b) | the four manual tests (§4) | the id join (pre-flight 1–2) |
| GitHub Spec Kit (`specs/<feature>/spec.md`, `.specify/`) | `FR-###`, `SC-###` | the four manual tests | the id join |
| Kiro (`.kiro/specs/<feature>/requirements.md`) | numbered requirements in EARS form | the four manual tests (EARS shape read by hand) | the id join, when tests cite the numbers |
| Gherkin (`*.feature`) | scenario tags (`@AC-12`) | the four manual tests per `Then` | cucumber-js / behave dry run (§3) |
| a spec with no ids | none | the four manual tests | `N/A (no criterion ids)`: say so; never infer links |

| Test carrier | How an id is cited |
|---|---|
| Jest, Vitest, Mocha, node:test | the id in the `test` / `it` / `describe` title |
| Playwright | `@AC-12` in the title, or `{ tag: '@AC-12' }`, or an annotation; `npx --no playwright test --list --grep @AC-12` lists them |
| pytest | the id in the test name or a marker (`@pytest.mark.ac("AC-12")`) |
| RSpec, JUnit 5, Kotest, Go | the id in the description, `@DisplayName` / `@Tag`, or `func TestAC12…` |
| Gherkin | a scenario tag `@AC-12` |

## Pre-flight

Run as **one** script from the repo root (bash 3.2). Every `rg` names its path; its stderr goes to `$O/rg.err`, and a non-empty file prints `BLOCKED`: the lane it feeds is `blocked (rg exit 2)`, never zero hits. Ids are normalised (`AC-007` = `AC-7`) before the join. Output goes under `${TMPDIR}`, cleared first.

```bash
X=(-g '!**/node_modules/**' -g '!**/{dist,build,.next,vendor,.venv,coverage,target}/**')
O="${TMPDIR:-/tmp}/ac-trace"; rm -rf "$O"; mkdir -p "$O"      # cleared first: a stale id list poisons the join
PFX="${PFX:-AC|REQ|FR|SC|NFR|US}"     # add the project's own prefixes from 0b, e.g. PFX='AC|REQ|PAY'
SPEC_ROOTS=(); for d in ai/specs ai/runs ai/product specs spec docs/specs docs/requirements requirements .kiro/specs .specify; do [ -d "$d" ] && SPEC_ROOTS+=("$d"); done
[ ${#SPEC_ROOTS[@]} -gt 0 ] || SPEC_ROOTS=(/dev/null)        # never an empty path list: rg would read stdin
TG=(-g '**/*.{test,spec}.{js,jsx,ts,tsx,mjs,cjs}' -g '**/{test,tests,__tests__,spec,e2e,features}/**' -g '**/test_*.py' -g '**/*_test.{py,go}'
    -g '**/*_spec.rb' -g '**/*{Test,Tests,IT}.{java,kt,cs}' -g '**/*.feature')
echo "0a spec roots: ${SPEC_ROOTS[*]}"
# 0b. id prefixes the specs actually define (an id opening a heading, a list item or a table cell)
rg -o --no-filename --pcre2 -g '*.{md,mdx,txt}' '^\s*(?:#{1,6}\s+|[-*+]\s+(?:\*\*)?|\|\s*(?:\*\*)?)\K[A-Z][A-Z0-9]{0,9}-\d{1,5}\b' "${SPEC_ROOTS[@]}" 2>>"$O/rg.err" | sed -E 's/-[0-9]+$//' | sort | uniq -c | sort -rn | head -10
# 1. criterion ids defined, with their spec line (the TR-1 side of the join)
#    a heading id inside a run ledger (`### REQ-010` in ai/runs/*/requirements.md) is a STORY, not a criterion: dropped
rg -n --pcre2 -g '*.{md,mdx,txt}' "^\s*(?:#{1,6}\s+|[-*+]\s+(?:\*\*)?|\|\s*(?:\*\*)?)\K(?:$PFX)-\d{1,5}\b" "${SPEC_ROOTS[@]}" 2>>"$O/rg.err" \
  | grep -vE '^ai/runs/[^:]+/requirements\.md:[0-9]+:[[:space:]]*#{1,6}[[:space:]]' > "$O/defined.lines"
sed -E 's/^[^:]+:[0-9]+://; s/^[^A-Z]*//; s/^([A-Z0-9]+-[0-9]+).*/\1/; s/-0*([0-9])/-\1/' "$O/defined.lines" | sort -u > "$O/defined"; echo "defined: $(wc -l < "$O/defined")"
# 2. ids cited by tests (the TR-2 side); then both joins
rg -o --no-filename --pcre2 "\b(?:$PFX)-\d{1,5}\b" "${TG[@]}" "${X[@]}" . 2>>"$O/rg.err" | sed -E 's/-0*([0-9])/-\1/' | sort -u > "$O/cited"; echo "cited: $(wc -l < "$O/cited")"
echo "TR-1 defined, never cited:"; comm -23 "$O/defined" "$O/cited"
echo "TR-2 cited, never defined:"; comm -13 "$O/defined" "$O/cited"
# 2b. where each cited id sits: a title / tag, or a comment only (a comment is not a trace)
rg -n --pcre2 "^\s*(?://|#|\*|/\*).*\b(?:$PFX)-\d{1,5}\b" "${TG[@]}" "${X[@]}" . 2>>"$O/rg.err"
# 3. Gherkin: feature files, and the runner that can dry-run them (installed only; never npx -y)
rg --files -g '*.feature' "${X[@]}" . 2>>"$O/rg.err" > "$O/features"; echo "features: $(wc -l < "$O/features")"
#    cucumber-js 12.x refuses Node 23 at start-up (measured 2026-10-19 on the launch-gaps fixture): that exit is NOT-RUN, never a §3 result
if [ -s "$O/features" ] && [ -x node_modules/.bin/cucumber-js ]; then
  DO_NOT_TRACK=1 CI=true node_modules/.bin/cucumber-js --dry-run --format usage-json:"$O/usage.json" >/dev/null 2>"$O/cucumber.err"
  rc=$?; if [ ! -s "$O/usage.json" ]; then echo "§3 NOT-RUN (cucumber-js exit $rc wrote no usage.json; node $(node -v 2>/dev/null): $(head -1 "$O/cucumber.err"))"
  else echo "cucumber-js dry run exit $rc — parse $O/usage.json; the exit code is never a PASS"; fi
elif [ -s "$O/features" ] && command -v behave >/dev/null 2>&1; then
  behave --dry-run -f steps.missing > "$O/behave-missing.txt" 2>&1; behave --dry-run -f steps.usage > "$O/behave-usage.txt" 2>&1
else [ -s "$O/features" ] && echo "§3 NOT-RUN (cucumber-js / behave not installed)"; fi
# 4. run-ledger specs: the ears-lint lane
EL=.claude/scripts/ears-lint.py; [ -f "$EL" ] || EL="$HOME/.claude/templates/repo-baseline/.claude/scripts/ears-lint.py"
for f in ai/runs/*/requirements.md; do [ -f "$f" ] || continue
  if [ -f "$EL" ]; then python3 -I "$EL" "$f"; else echo "§4 ears lane NOT-RUN (no ears-lint.py: repo-baseline not installed)"; break; fi; done
[ -s "$O/rg.err" ] && echo "BLOCKED (rg exit 2): $(head -3 "$O/rg.err")"
```

Read 4's result with its counts: `ears-lint: 0 stories, 0 criteria` on a file means the file is not in the run-ledger format and the lane is `N/A (not run-ledger format)`, never a pass (`precedents/product.md` § 34).

### Measured

On 2026-10-19 over the 23 `benchmarks/fixtures` roots: 0 rg exit 2. Only `reward-hack` defines criterion ids (5 `AC-###` in its one spec under `specs/`, prefix histogram `AC 5 · SPEC 1`); its tests cite the same 5, so TR-1 and TR-2 are 0, the correct answer. A scratch copy with one test file deleted and a test citing `AC-009` added returns exactly `AC-3` for TR-1 and `AC-9` for TR-2. No fixture has a `.feature` file. `ears-lint.py` on that spec prints `0 stories, 0 criteria` and exits 0: the spec writes `- **AC-001** WHEN …` without the run-ledger colon, so the lane is N/A there, the case the read rule above exists for. An earlier draft of this script kept the previous run's id list when two runs shared `${TMPDIR}` (every later root reported the first root's 5 ids); the output folder is now cleared first. The product eval measured the real NestJS + React monorepo read-only on the same day: 0 criterion ids in docs or tests, no `.feature` files, 220 ADR references — the trace lane prints `N/A (no criterion ids, no Gherkin)` there. On the `launch-gaps` fixture (integration pass, same day): 9 ids defined, 10 cited; TR-1 `AC-5`, TR-2 `AC-9` `AC-14`, 2b the comment-only `AC-003`; the run ledger's `### REQ-010` story heading, a false TR-1 row in the first version, is dropped by step 1's run-ledger filter; step 4 runs through the `$HOME/.claude/templates/repo-baseline` fallback in a copy with no `.claude/` and prints `AC-011 — vague word in the SHALL clause: quickly`; step 3 prints NOT-RUN (no installed runner).

## Scans for

Severity assumes the criterion is in the release's scope. One step up when the criterion is a primary outcome, the success metric's behaviour, or an authorization rule.

| § | Class | Default |
|---|---|---|
| 1 | PR-TR-1 criterion with no test naming it | medium; high on a primary outcome or an authorization rule |
| 2 | PR-TR-2 test cites an id no spec holds (stale trace) | low |
| 3 | PR-TR-3 undefined or ambiguous Gherkin step; unused step definition | medium (undefined, ambiguous) · low (unused) |
| 4 | PR-TR-4 criterion not falsifiable, not bounded, not singular, not EARS-shaped | medium; BLOCKER on a primary outcome (under `/audit-requirements --spec`) |

### 1. Untested criterion

```
BAD:   specs/refunds.md:14  - **AC-3** WHEN a refund is issued THE ledger SHALL deduct the awarded points
       tests/: no title, tag or name carries AC-3 (only `// see AC-3` in a helper)
GOOD:  test('AC-3 a refund takes back the points the purchase awarded', …) — asserting the deducted balance
```
**Read the code:** Does the test that names the id assert the criterion's observable outcome, or only exercise the path? Is the test collected and run (a `.skip`, an `xit`, a file outside the runner's glob)? Is the id in a title or tag, or in a comment only (2b)? Inside a run, what does `trace-matrix.py` say? **Finding when** no collected test names the id in a title, tag or name, or the only naming test does not assert the outcome. **PROOF:** V427 — the join prints the id under TR-1 before the fix and not after; the new test fails on the pre-fix code when the behaviour is missing.

### 2. Stale trace

```
BAD:   tests/legacy.test.js:1  test('AC-9 legacy discount', …)   — no spec defines AC-9
GOOD:  the id is restored to the spec it came from, or the test is retitled to the criterion it now asserts
```
**Read the code:** Is the prefix an external tracker's (`PROJ-123`), resolved against the tracker rather than the repo (`precedents/product.md` § 35)? Was the criterion renamed, merged or removed (git log of the spec)? **Finding when** the id is the spec's own prefix and no spec in the repo holds it. **PROOF:** V427.

### 3. Gherkin glue

```
BAD:   features/points.feature:9  Then the points balance is reduced     — undefined step
       steps/legacy.steps.ts:22   Given('a gold member', …)               — used by no scenario
GOOD:  every step resolves to one definition; every definition is used by a scenario that runs
```
**Read the code:** Parse the formatter output, never the exit code: `cucumber-js --dry-run` exits 0 with undefined steps (13.3.0 docs, 2026-10-05). Is the step used only under a tagged-out feature (`@wip`, `@manual`) (`precedents/product.md` § 32)? Is the runner installed? Without it the class is `NOT-RUN (cucumber-js / behave not installed)`, and the feature and step files are read by hand for the undefined steps only. **Finding when** the usage output lists an undefined or ambiguous step, or an unused definition outside tagged-out features. **PROOF:** V428.

### 4. Unverifiable criterion — the four tests

**Establish the prior behaviour first** for a criterion that changes an existing surface: locate the surface and record what it does today at `<file:line>` (its states, the errors it already returns, the limits it already enforces). "Loads faster than before" has no bound in prose and gets one the moment "before" is a measured value. Record `NOT APPLICABLE — new surface` where the surface does not exist yet.

**Enumerate** every criterion verbatim with its locator, including the ones embedded in prose ("it should also …" is a criterion wearing a narrative disguise). Then apply the four tests to each:

| Test | Question | Fails when |
|---|---|---|
| **Falsifiable** | what observation would prove this FAILED? | no observation could refute it |
| **Observable** | can it be checked without asking the author? | verification needs the author's intent |
| **Bounded** | are the numbers, volumes and conditions stated? | an adjective stands where a bound belongs |
| **Singular** | is this one criterion? | "and" joins independently testable claims |

Classify each failure:

| Class | Shape | Replacement |
|---|---|---|
| unbounded adjective | fast, responsive, intuitive, easy, robust | a number, a percentile, a measurement point, a load condition |
| deferred standard | properly, correctly, appropriately, as expected | name the standard, or state the behaviour |
| capability not behaviour | "should be able to" | the observable outcome |
| blanket error clause | "handles errors gracefully" | one criterion per named failure, each with its outcome |
| compound | two claims joined by "and" | split |
| intent-dependent | "the user understands that …" | an observable proxy, or move it out of the criteria |
| circular | "works as expected" | state the expectation |

**Check every number that is present.** A latency or throughput criterion needs a unit, a percentile where it is a distribution, a measurement point (server, client, end to end; cold or warm) and a load condition. A number missing the percentile and the measurement point is unbounded, and it is the commonest way an unverifiable criterion passes review.

```
BAD:   - AC-2: the export completes quickly for large accounts
GOOD:  - AC-2: WHEN an account with 50,000 orders requests a CSV export THE service SHALL deliver the file within
         120 s (p95, measured server-side from request to the last byte)
```
**Read the code:** Is a flagged word bounded by the text around it (`precedents/product.md` § 33)? Is the run-ledger file really in that format, or did `ears-lint.py` read 0 criteria (§ 34)? Were the criteria written after the code, restating what was built (check the authoring order)? **Finding when** a criterion fails a test with its class named and its refuting observation written as MISSING; `ears-lint.py` exit 2 rows are findings as printed (mechanical facts: cite them, do not re-judge them). **PROOF:** V429.

## The 3,000-hit path

A backlog can hold thousands of criteria. Triage in this order and record each step in the coverage block:

1. **Scope first.** The release's specs (the ones a run, a ticket or `--spec` names), then the rest.
2. **Run the mechanical lanes on everything** (the id join, `ears-lint.py`, the Gherkin dry run): they cost seconds and need no reading.
3. **Group TR-1 rows by spec**: one decision per spec when the whole spec has no tests yet (one finding, N ids).
4. **Read the four tests by hand** for the release's criteria in full, then the top 30 criteria of the rest by priority (primary outcomes, authorization rules, money).
5. **Ledger the rest** as `Live, unreviewed (k specs / n criteria)`, never `checked`.

## Output

```
acceptance-criteria-check — specs: specs/refunds.md (12 criteria), ai/runs/20261018-refunds/requirements.md (9)
Lanes: ears-lint (run-ledger, 9 criteria) · id join (prefixes AC, REQ) · cucumber-js 13.3.0 dry run (2 features)

Criteria ledger:
| #    | Criterion (verbatim)                               | Falsifiable | Observable | Bounded | Singular | Refuting observation              | Test           | Class |
| AC-2 | "the export completes quickly for large accounts"  | no          | yes        | no      | yes      | MISSING — no bound on size or time | —              | unbounded adjective |
| AC-3 | "WHEN a refund is issued THE ledger SHALL deduct…" | yes         | yes        | yes     | yes      | balance unchanged after a refund  | none (TR-1)    | — |

Findings: 3

1. specs/refunds.md:14  AC-3                                       [report-with-fix]   high
   §1 untested criterion — no collected test names AC-3; tests/helpers/points.ts:40 cites it in a comment only.
   Fix: a test titled `AC-3 …` asserting the deducted balance. Proof: V427 (the join lists AC-3 under TR-1).

2. features/points.feature:9                                        [report-with-fix]   medium
   §3 undefined step "Then the points balance is reduced" (cucumber-js usage-json; dry-run exit 0).
   Fix: a step definition in steps/refund.steps.ts. Proof: V428.

3. specs/refunds.md:9  AC-2                                        [report-flagged]    medium
   §4 unbounded adjective "quickly"; "large accounts" has no size. The prior behaviour is unread (the export
   endpoint was not located). Settle: locate the export route and record today's p95; propose the bound.

Totals: 21 criteria · pass 17 · fail 4 · embedded in prose 1 · numeric criteria missing a bound part 1 (AC-2)
Verification: 5 candidates → 3 findings · 0 unconfirmed · 1 hardening · 0 pre-existing · 1 refuted

Class coverage:
  §1 untested criterion   checked (21 ids defined, 19 cited → 1 finding; 1 comment-only)
  §2 stale trace          checked (1 cited-never-defined → 0 findings: PROJ-88 is a tracker id)
  §3 Gherkin glue         checked (2 features, cucumber-js usage-json → 1 finding)
  §4 shape                checked (ears-lint 9 → 0; manual 12 → 1 finding)
Verdict: PARTIALLY VERIFIABLE (4 failing)
```

`[report-with-fix]`: the lane ran (the join, the lint, the dry run) or both ends were read, and the fix is a test, a step or a rewritten criterion. `[report-flagged]`: one link is unproven (the prior behaviour unread, a runner not installed, an id prefix not resolved); the row names what would settle it. The coverage block lists **all four** classes on every run: `checked (k → m findings)`, `N/A (<reason>)` (no criterion ids, no Gherkin, not run-ledger format), `NOT-RUN (<runner> not installed)`, `blocked (rg exit 2)`, or `Live, unreviewed (k / n)`. Verdict: `VERIFIABLE | PARTIALLY VERIFIABLE (<n> failing) | NOT VERIFIABLE`. The criteria ledger is pasted verbatim into `/audit-requirements --spec`, where it is the only source for the falsifiability column; replacement proposals go in a separate section marked as proposals.

## Precedents

The verifier reads [`precedents/product.md`](../../../../snippets/precedents/product.md) § 31–35 and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4 and § 10. The ones this skill meets most:

- **A bounded adjective is bounded** (§ 33). "Fast (p95 under 300 ms server-side at 500 concurrent requests)" passes. Read the surrounding text before flagging on a keyword.
- **A behaviour needs no number.** "The list shows the ten most recent" needs no percentile.
- **A reachable standard bounds a criterion.** A cross-reference to a documented standard is bounded if the standard is reachable; record `DEFERRED — standard not available` only if it is not.
- **An atomic "and".** "Saves and returns to the list" may be one user-visible outcome; split only when the halves are independently testable and could diverge.
- **An id in a comment or a title is a link** (§ 31); tagged-out features make steps look unused (§ 32); a tracker prefix resolves against the tracker (§ 35).
- **Criteria written after the code** pass every test here and are worthless as a contract: check the authoring order and say so.

## When to run

- Before estimation, so ambiguity is priced out rather than in; before build, as the last gate on the spec.
- Under `/audit-requirements --spec` (the criteria ledger) and `/audit-requirements --repo` (the trace lane across every spec and the scorecard's PRR-TR-1 row).
- After a dispute about whether something was done, to name the criterion that caused it; on an inherited backlog, to size the requirement debt.

## Halt conditions

- Every finding goes through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) (§ 10, correctness lens) with [`precedents/product.md`](../../../../snippets/precedents/product.md) before it is reported; under `/audit-requirements` that is its verification phase, standalone it is a separate second pass and the rows are tagged `self-verified`.
- **No acceptance criteria exist:** the spec has prose and nothing testable. That is the finding; report it and stop. Do not invent criteria: invented criteria become the contract.
- **The actor is unstated** across the criteria set: "the system shall" hides who, and the answer changes what is tested.
- **The surface cannot be located** for a criterion that modifies an existing surface. Where the repository is readable, go and read it (§4, prior behaviour); halt only when neither the criteria nor the code identifies what is being changed.
- **An external standard is unreachable:** record `DEFERRED — standard not available`, never a pass.
- Do not print a trace link the join did not produce, read a dry run's exit code as PASS, or count `ears-lint`'s `0 criteria` as clean. Do not rewrite a criterion in place: proposals go in their own section.

## Related

- `/audit-requirements` dispatches this skill: `--spec` takes the criteria ledger, `--repo` takes the trace lane and the PRR-TR-1 evidence row for `launch-readiness`. `/product-fix` closes TR rows test-first (V427–V429).
- `@requirements-reviewer` (delivery pack, the single owner) issues the spec verdict this ledger feeds; `evidence-trace` and `assumption-ledger` handle the unsourced requirements.
- `ears-lint.py` and `trace-matrix.py` (repo-baseline, `.claude/scripts/`) are the mechanical lanes for run-ledger specs; `@verifier` owns the run matrix.
- The testing pack's `suite-execution-scan` (when installed) owns whether the naming test is collected and run.
- `ai/patterns/acceptance-criteria.md` holds the project's criteria conventions.
