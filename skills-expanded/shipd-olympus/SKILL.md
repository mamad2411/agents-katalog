---
name: shipd-olympus
description: Use when creating or reviewing a shipd.ai Olympus quest submission — picking a candidate GitHub repo, designing a challenge task hard enough for the ≤50% pass-rate bar, writing the test patch, solution patch, test.sh, or Dockerfile, or when a platform check fails (naming collisions, Dockerfile warnings, description request_changes, test fairness).
---

# Shipd Olympus Submissions

## Overview

An Olympus submission = repo@commit + problem description + hidden tests + golden solution + Dockerfile. Tasks must be HARD enough that state-of-the-art agents fail at least half their runs — a one-file fix is an instant rejection. The approved shape: a new "family" of related functionality mirroring something the repo already has, 200+ effective solution LOC, 40+ deterministic tests.

## 1. Repo eligibility (check ALL before investing)

```bash
gh repo view OWNER/REPO --json stargazerCount,licenseInfo,pushedAt,primaryLanguage
```

- **License**: permissive only (MIT/Apache/BSD). GitHub API `"other"` ≠ fail — read the LICENSE file (some repos show "other" but are Apache-2.0; others show "other" but are GPL → disqualified).
- **Stars**: 500+. **Activity**: commit within 12 months (verify `pushedAt` arithmetic — "3 months ago" passes, don't confuse with a 3-month rule).
- **Language**: TS/JS/Python/Go/Rust/C++/Java. Pin commit = head of default branch.
- In the platform form, paste the exact `https://github.com/owner/repo` URL — its search surfaces forks (0 stars) and some repos are blocked outright.

## 2. Task design — aim below the 50% bar

The platform rejects tasks agents pass more than half the time. **Design for failure up front; don't hope the batch comes back hard.**

Hard is *designed*, not *found*. Searching issue trackers for "hard problems" mostly surfaces chores (docs, typings, build config). Instead: pick a complex subsystem in an eligible repo (parser, type dispatcher, scheduler, query planner) and design a feature family that must integrate with it correctly.

Difficulty archetypes, ranked by difficulty gained per spec word spent:

1. **Convention traps** — the spec picks ONE of several plausible conventions and agents implement a neighboring one. Quantile interpolation has ~9 textbook variants; rounding modes, date arithmetic, and string collation are similar minefields. One sentence of spec, an entire wrong-implementation class of failures.
2. **Exact-boundary rules** — one sentence with several failure seams (e.g. weighted median: exact-half cumulative weight averages with the next larger *distinct* value; duplicates merge; fractional weights break expand-and-recount tricks).
3. **Non-inferable semantic substitution** — the new function differs from its obvious sibling in one deliberate way (divisor uses total weight, not element count). Agents copy the sibling and fail.
4. **Cross-cutting invariants** — one rule enforced at N call sites; agents patch two of four.
5. **Long wiring chains** — the feature must register in 5+ places (factory list, type definitions, docs registry, parser exposure); missing one fails a test non-obviously. Also lifts the LOC and file-count medians the platform requires.
6. **Parser/compiler surface** — grammar, precedence, round-trip printing. Hardest per run, but the spec cost is high; use when the repo's parser is the complex subsystem.

Stack 2–3 archetypes in one task. Difficulty that is really *ambiguity* doesn't count: 0% pass usually means one misreadable sentence or an unfair test, not a hard task — read the failing agent logs before celebrating.

Issue-graveyard mining (inspiration only, never copy an issue verbatim — originality sweep still applies):

```bash
# old, open, high-reaction feature issues with no PR ever = hard by natural selection
gh api "repos/O/R/issues?state=open&per_page=30" \
  --jq '.[] | select(.pull_request == null) | "\(.reactions.total_count) #\(.number) \(.title) (\(.created_at[:4]))"' | sort -rn
```

Other selection rules:

- Pure-logic surface only: parsers, statistics, schedulers, query engines. Clipboard/audio/UI/network features are untestable under `--network none`.
- Avoid mega-popular quest-farm repos (es-toolkit, dayjs, zod) — similarity-check collisions.

## 3. Originality sweep (the #1 rejection reason)

Any PR — open, merged, or **closed** — that implements the idea kills it. Sweep all four:

```bash
gh search prs --repo O/R "keyword"          # all states
gh search issues --repo O/R "keyword"
gh api "search/issues?q=repo:O/R+exact+name"   # per exact function name
gh api graphql -f query='query{search(query:"repo:O/R keyword",type:DISCUSSION,first:10){nodes{... on Discussion{title,url}}}}'
```

Also find how a similar past feature was wired: `git log --diff-filter=A -- path/to/analogous.file` then `git show --stat` — that commit is the wiring checklist for the solution.

## 4. Description rules

Maintainer-issue prose. Opens with the ask ("Add X…"). No headings, bullets, code, file names, or internal helpers. Name only contract essentials: function names, option strings, error-vs-result behavior.

Every function named in the ask needs its own defining clause — a sibling defined only implicitly (std as "sqrt of variance") draws a sanity WARNING for unstated parameters/defaults. Properties the tests rely on that *follow* from a stated rule get stated as a consequence clause attached to that rule ("…in each divisor, so that integer weights act as repetition counts") — explicit enough for the test checker, nothing itemized for the trim checker to cut.

**Two AI checkers pull in opposite directions — expect oscillation:**

- The *description-trim* checker demands removing "discoverable" clauses over multiple rounds (`request_changes` at 3+ suggestions).
- The *test-quality* checker flags tests that "enforce repository conventions not stated in the problem" and demands they be explicit.

**The checkers never converge — use the priority rule instead**: the trim checker emits blocking `request_changes`; the test-quality checker emits non-blocking WARNINGs. When they conflict, obey the blocker. A compact conventions sentence ("Like the existing X functions, the new ones accept the same containers and types and are exposed the same way") buys a round, but the trim checker eventually HIGH-flags it as discoverable — and it's right: repo conventions are repo-discoverable, so fairness rules keep the hidden tests fair without stating them. Delete on demand; accept the residual WARNING. Only *non-inferable* contract facts (semantic substitutions, boundary rules, skip semantics) are worth defending against a `request_changes`.

Don't chase checker convergence: warnings are non-blocking, and each rerun costs tokens and marks results stale. Batch all edits before rerunning checks — one rerun per batch, never per tweak.

## 5. Tests (hidden from agents)

- **Random-hash filenames, always**: `openssl rand -hex 3` → `name.a3f9b2.test.js` (or `test_name_a3f9b2.py`, `name_a3f9b2_test.go`). Predictable names fail the collision check. Never use "shipd"/"datacurve"/"quest"/"olympus"/"challenge" anywhere in patches.
- **T1**: 100% fail at base, 100% pass with solution. For throws/raises tests, first assert the function *exists* (`assert.strictEqual(typeof math.fn, 'function')`, `assert callable(mod.fn)`) — otherwise "fn is not defined" satisfies the throws assertion and the test passes at base.
- **T7**: never assert error messages or error types — bare `assert.throws(fn)` / `pytest.raises(Exception)`.
- Strongest tests: property equivalence against existing sibling functions (weighted-with-integer-weights ≡ sibling on expanded data, across all option values).
- Only test what's in the description or repo-discoverable. If the repo itself lacks a capability, don't test it even if a checker suggests it.
- **Fairness bar for exact return types**: pinning a type's exact return (deep-equal on a Fraction/Decimal/custom type) is only fair if *sibling* functions' tests or docs demonstrate it — lower-level evidence (arithmetic ops supporting the type) doesn't count. Audit each typed assertion against sibling tests before submitting; unfair ones FAIL the fairness check outright.
- test.sh: two modes; `base` runs the real unit suite ignoring a **broad glob** that matches both your hashed files AND predictable names an agent might create; `new` runs your hashed files; JUnit via `--output_path`; no fail-fast flags.

## 6. Dockerfile

```dockerfile
FROM public.ecr.aws/d3j8x8q7/olympus-base-typescript:latest   # or -python / -go / …
WORKDIR /app
COPY . .
RUN npm ci --include=dev
RUN npm install --no-save --include=dev mocha-junit-reporter@2.2.1
CMD ["/bin/bash"]
```

- **JS/TS trap**: the base image sets `NODE_ENV=production` → plain `npm ci` silently skips devDependencies (no test runner; `npx` then hits the network and dies offline). `--include=dev` is mandatory.
- Pin ad-hoc installs (`pkg@x.y.z`); `--no-save` is correct and unavoidable — patches apply AFTER build, so manifests can't be edited before install. Lockfile/"non-reproducible" warnings are non-blocking; justify and move on.
- No tests in build. Runtime is `--network none` — every dependency must be installed at build time.

## 7. Local verify loop (do before spending platform tokens)

Build from a **fresh clone** — a working tree with `node_modules`/`.venv`/build artifacts gets COPY'd in and corrupts the image (`git clean -fd` doesn't remove ignored dirs; need `-x` or a fresh clone).

```
fresh clone @ commit → docker build → run --network none:
  apply test.patch → base PASS, new FAIL (exit = #tests)
  apply solution.patch → base PASS, new PASS
grep -inE "challenge|quest|olympus|shipd|mars|datacurve" *.patch   # only allowed hit: base image name
```

Patches: `git add -A && git diff --cached -- <paths>` (captures new files); paste verbatim including `diff --git` / `new file mode` headers — they ARE the format.

## 8. Platform endgame

Similarity check: read the close matches yourself; same task reworded = pivot, don't reword. Verify the exact bars in the form's "Submission criteria" panel (they change with product); known bars observed:

- **Pass rate ≤ 50%** across agent runs — the gate most tasks fail. 100% pass = too easy, must harden before submitting.
- **≥ 6 agent runs** completed.
- **Median LOC ≥ 150** across passing runs (only effective solution lines count — comments/blanks/tests don't).
- **Median files ≥ 2** across passing runs.
- Fair / solvable / no-cheating checks on the runs themselves.

Run a SMALL batch first to gauge before spending tokens on all 6+. 0% pass usually means one ambiguous sentence or unfair test — read the agent logs before assuming the task is hard.

**Hardening when pass rate is too high**: add a precision trap, not volume — pick the next archetype from §2 that your task doesn't use yet. Convention traps and exact-boundary rules give the most difficulty per spec word; dimension/axis-style generalizations give the most LOC. Each hardening edit stales the checks — batch description+tests+solution changes, reverify locally, then rerun checks once.

## Common mistakes

| Mistake | Fix |
|---|---|
| Picking a "good first issue" | Olympus wants SOTA-hard; invert instinct |
| Hoping the agent batch comes back hard | Design difficulty in from §2; batches cost tokens |
| Trusting GitHub license field | Read LICENSE file |
| Predictable test filenames | Hash suffix from `openssl rand -hex 3` |
| `npm ci` without `--include=dev` | NODE_ENV=production trap |
| bare throws-assertion at base | assert-the-function-exists first line |
| Pinning exact typed returns without sibling evidence | Fairness FAIL; audit vs sibling tests |
| Rerunning checks per tweak | Batch edits; checks go stale + cost tokens |
| Obeying every checker trim | Keep non-inferable contract facts |
