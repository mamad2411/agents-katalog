---
name: proven-code-review
description: Reviews a pull request, branch, diff or staged changes like a senior engineer who reads beyond the diff, tries to refute every suspected bug before reporting it, and proves the serious ones by running a failing test, so the review contains real bugs with evidence instead of noise. Use when asked to review code, a PR, a branch or AI-generated changes, before merging, or when you want a second opinion that catches what green tests and quick reviews miss.
argument-hint: "[PR number | branch | commit range | files] [quick | deep]"
---

# Proven code review

Report only real problems, each with evidence, and prove the serious ones. A review with two
proven bugs is worth more than one with fifteen guesses. "No material issues" is a valid outcome
when you show what you checked.

Modes: default proves every Critical and High finding; `quick` traces only (no proofs); `deep`
also proves Medium findings and runs the full test suite.

## 1. Scope the change and its intent

- **Target.** What the user names; otherwise the current branch against its base
  (`git merge-base HEAD <default branch>`), else staged, else working-tree changes. For a PR
  number use `gh pr diff <n>` and `gh pr view <n>` if `gh` is available. Pasted code is reviewed as is.
- **Intent.** Read the PR title and description, commit messages and any linked ticket or spec.
  The review checks the code against what its author claims it does.
- **Test command.** Find it in the CI workflow, `package.json` scripts, `pyproject.toml`/`tox.ini`,
  `Makefile`, `go.mod`, `pom.xml`/`build.gradle`. You will need it to prove findings.
- **Size.** Above ~1,500 changed lines, review the riskiest files first (auth, money, data
  writes, concurrency, public APIs) and say which files you did not cover.

## 2. Map the change before judging it

Read whole files, not just hunks. For every changed function, endpoint, query or config:

- what it did before and what it does now (`git diff`, `git show <base>:<path>`);
- **who calls it**: search the repository for every caller and import, including files outside
  the diff. Most expensive bugs live in an unchanged caller that relied on the old behaviour;
- the contract callers rely on: exceptions raised, return shape, `null`/`None` semantics, units,
  time zones, ordering, idempotency;
- what it touches: database writes, money, auth, files, network, caches, shared state;
- which tests cover it, and whether they exercise the new behaviour or only its happy path.

## 3. Hunt in passes

Run each pass against the map. `references/hunting-guide.md` lists concrete patterns per pass
and per language; `references/ai-code-failure-modes.md` lists what coding agents typically get
wrong. Use them.

1. **Intent:** does the change do what the PR says? Try the exact example the PR mentions.
2. **Contracts beyond the diff:** changed signatures, return values, exceptions, defaults and
   schemas against every caller and every consumer.
3. **Correctness:** boundaries, rounding, empty and null paths, error paths, async and await,
   units, time zones, encodings.
4. **Concurrency and state:** check-then-act, lost updates, idempotency, transactions, side
   effects that happen before the state that guards them is written.
5. **Security:** authorization on every new entry point (compare with its sibling routes),
   injection, path traversal, secrets, unbounded input.
6. **Tests:** do the new tests test the change? Look for weakened or deleted assertions, mocks
   that replace the behaviour under test, and fixtures that cannot occur in production.

Skip style, naming and architecture opinions unless they hide a defect.

## 4. Try to refute every candidate

Before a suspicion becomes a finding, try to prove yourself wrong:

- Is it already prevented elsewhere: middleware, a caller's validation, a database constraint,
  the type system, a framework default? Search for it.
- Can the triggering input reach this code? Trace it from a real entry point.
- Is the behaviour intended, according to a comment, a test, the spec or the PR text? A behaviour
  that a test explicitly asserts is intended unless the PR text or spec contradicts it; at most
  ask about it.
- Would a user, the data or the business actually be harmed?

Refuted → drop it silently. Undecidable → a **question for the author** (three at most), never a
finding.

## 5. Prove the serious ones

For every Critical and High finding (and Medium in `deep` mode), show it happening:

1. **Preferred: a failing test.** Write the smallest test that fails because of the bug, in the
   project's own framework, in a **new** file (for example `tests/test_review_proof_<slug>.py` or
   `test/review-proof-<slug>.test.js`). Never edit existing tests or code to do this.
2. **Otherwise: a one-off command** (`python -c`, `node -e`, a REPL snippet) that prints the
   wrong result.
3. Run it with the project's test command and capture the failing output.
4. **Races and ordering bugs:** force the bad interleaving (a barrier, a slowed side effect, two
   connections) instead of hoping a loop hits it. `references/proof-recipes.md` has recipes for
   the common classes.
5. Delete the proof files you created once you have the output, unless the user asked to keep
   them, and include the test code in the report so the author can add it.

Stay local and harmless: never install packages, call external services, use production
credentials or data, or run migrations against a real database. If a proof needs any of that,
report the finding as **Traced** and say what would prove it.

Evidence tiers in the report:
- **Proven**: a command you ran in this session shows the wrong behaviour.
- **Traced**: you followed the path through the code; quote the decisive lines.

Also run the existing test suite once (default and `deep` modes, if it finishes in about two
minutes) and report any failure as a Proven finding.

## 6. Write the report

Use `assets/report-template.md`. Order findings by severity, then by evidence (Proven first).

- **Verdict:** `BLOCK` (any Critical) · `REQUEST CHANGES` (any High) · `APPROVE WITH NOTES` (only
  Medium/Low) · `APPROVE` (nothing material).
- **Severity:** Critical = security breach, data loss or corruption, wrong money, outage of a
  main path · High = wrong behaviour or crash on a realistic path, broken caller contract ·
  Medium = real but narrow edge case · Low = minor, cheap to fix. When torn between two levels,
  pick the lower one: inflated severity costs the reader's trust in the rest of the review.
- Every finding names `file:line`, the concrete trigger (input or interleaving), the
  consequence, the evidence, and a minimal fix as code.
- **Checked and fine:** list what you examined and found correct. It shows coverage and makes a
  short review trustworthy.
- At most three nits, only if each is worth the author's time. No generic advice: never write
  "consider adding tests" without the exact test.

Post to a pull request only if the user asks (`gh pr review <n> --comment --body-file <file>`).
Never approve or merge on the user's behalf.

`examples/example-review.md` shows a complete review of a realistic change.
