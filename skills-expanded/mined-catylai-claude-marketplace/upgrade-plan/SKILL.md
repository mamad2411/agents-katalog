---
name: upgrade-plan
description: "Turns the upgrade-research table into an ordered, conflict-checked upgrade plan in .upgrade/plan.md, gated on whether the test suite can detect a regression and backed by a recorded baseline. Use when asked what order to upgrade dependencies or runtimes in, whether an upgrade is safe, or after upgrade-research has produced its table. Not for finding versions or EOL dates (use upgrade-research); not for applying the plan (use upgrade-execute)."
argument-hint: "[path to the research table; blank uses the table in this conversation]"
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Edit(.upgrade/**), Bash(git status *), Bash(git rev-parse *), Bash(mkdir -p .upgrade/*), Bash(npm ls *), Bash(npm install --dry-run *), Bash(go mod graph *), Bash(go mod why *), Bash(cargo tree --locked *), Bash(pipdeptree *), Bash(terraform providers)
license: MIT
---

# upgrade-plan

Stage 3 of the upgrade pipeline. Input: the research table from `upgrade-research`
(`$ARGUMENTS` names a file holding it; blank means the table earlier in this conversation). Output:
`.upgrade/plan.md` and a recorded baseline in `.upgrade/baseline/`, both in the format defined in
[references/plan-format.md](references/plan-format.md), which `upgrade-execute` reads.

Run from the repository root. This skill changes no manifest, lockfile or commit; the only source
edit it makes is the falsification probe in step 3, which it reverts before moving on.

## Handoff contract: what this skill reads

Two tables, both from earlier in the pipeline, joined on `ID`:

- **The research table**, exactly as `upgrade-research` defines it in its Handoff contract:
  `ID | Name | Kind | Current | Latest stable | In-major latest | Ceiling | Ceiling source |
  Recommended | Bound by | Support | EOL | Advisories | Rank | Sources`, followed by its `Unknowns`
  list. `Rank` (1–5, the ladder `upgrade-research` owns) orders independent steps here.
- **The inventory table** from `dependency-inventory`, for the columns research does not carry:
  `Ecosystem`, `Manifest`, `Declared`, `Lockfile` and `Pin`.

How research values map into the plan:

| Research value | Plan treatment |
| --- | --- |
| `Recommended` = `keep` | `Not in this plan`, reason `already-current` |
| `Recommended` = `needs-ceiling`, or `Ceiling` = `unknown` on a `runtime` or `base-image` row | `Not in this plan`, reason `needs-ceiling` |
| `Bound by` = `breaking` and `Latest stable` is a newer major | An in-major step to `Recommended` now; the major is either its own later step (same `ID`, `Depends on` the in-major step) with located breaking changes, or `Not in this plan` as `deferred-major` |
| `Advisories` = `not-checked`, `EOL` = `unknown`, a query in `Unknowns` | Listed under `Input gaps`, with the effect on ordering |
| `T…` rows (transitive advisories) | Moved by upgrading the direct dependency that pulls them, found with the probes in step 4 |

When a column is missing, record it under `Input gaps` and plan conservatively; without `Rank`,
independent rows keep table order and the plan says so. When there is no research table at all,
stop and suggest running `upgrade-research` first, because a plan built on remembered version
numbers is the failure this pipeline exists to prevent.

## Workflow

Copy this checklist and tick it off as you go:

```
- [ ] 1. Preflight: clean tree, .upgrade/ created, HEAD recorded
- [ ] 2. Baseline: gates found, run, recorded
- [ ] 3. Adequacy: coupling checked, falsification probe run and reverted, verdict set
- [ ] 4. Conflicts found
- [ ] 5. Steps ordered, grouped and typed
- [ ] 6. Breaking changes located for every major
- [ ] 7. Plan written and verified
```

### 1. Preflight

Run `git status --porcelain`. The baseline must describe a commit, so if the tree is dirty, show
the user the list and ask them to commit or stash it; their uncommitted work is theirs to move.
Then run `mkdir -p .upgrade/baseline`, because the gate logs are written into it by shell
redirection, which does not create directories. Create `.upgrade/.gitignore` containing the single
line `*`, which keeps everything under `.upgrade/` out of `git status` and out of every commit.
Record `git rev-parse HEAD` for the plan header.

### 2. Baseline

A red suite validates nothing, and a failure that already existed gets blamed on the first upgrade
after it. So the baseline is captured, and read, before any version moves.

1. Find the gates the project itself runs: read the CI workflow files, `package.json` scripts,
   `Makefile`, `tox.ini`/`noxfile.py`, `pyproject.toml`. Use those exact commands; a gate the
   project does not run is not part of its baseline.
2. Run each gate from the repo root, sending output to its log, for example
   `npm test > .upgrade/baseline/test.log 2>&1; echo "exit=$?"`. Suites that take longer than the
   Bash tool's default timeout need an explicit `timeout`, or `run_in_background` if they exceed its
   maximum.
3. Write `.upgrade/baseline/summary.md` in the gate-run format: command, exit code, tests run and
   the failing test identifiers, per gate.

When no test gate exists, record that; it is a finding that sets the verdict, not a reason to stop.
When the project has no gate of any kind (no test, typecheck, lint or build command), write no
summary and set the plan header to `Baseline: none (no gates)`.

### 3. Adequacy

The question is specific: *if this dependency started misbehaving, would a test go red?* Coverage
percentage does not answer it; a suite that mocks the HTTP client will not notice an HTTP client
upgrade.

1. For each row ranked 1–3, each major and each runtime, Grep for the package's imports and check
   whether the tests that reach it use the real thing or a mock.
2. Run the falsification probe on the highest-risk rows: break the integration in one place (a wrong
   argument at a call site, a client pointed at a dead address), run the relevant test gate, then
   restore the file with `git restore -- <file>` and confirm `git status --porcelain` is empty
   again. A suite that stays green with the integration broken will stay green when the upgrade
   breaks it, so that row's steps are `unverifiable`.
3. Judge the suite against the written standards: load `dev-standards:test-structure` (and read
   its Python or TypeScript reference, whichever applies) and `dev-standards:zero-tolerance-testing`
   with the Skill tool. If `dev-standards` is not
   installed, judge from the evidence gathered in 1 and 2 and write "standards not available" in the
   `Adequacy` section.
4. Set the verdict:

| Verdict | When | Decision |
| --- | --- | --- |
| `adequate` | Baseline green; the suite exercises the upgraded code; the falsification probe went red | `proceed`, by the gate |
| `partial` | Baseline green; some rows have no meaningful test | The user chooses `proceed`, `add-tests-first` or `stop`; the plan lists the unverifiable steps by number and name |
| `inadequate` | No test gate, a red baseline, or the probe stayed green | The user chooses: `fix-baseline-first`, `add-tests-first`, `proceed-unverified` or `stop` |

For `partial` and `inadequate`, present the evidence and ask with AskUserQuestion before writing any
step, so the user knows what kind of verification they are getting before the first version moves.
Record the answer as `Decision` with `Decided by: user`. A red baseline is fixed as its own change
before any upgrade, or explicitly accepted as `proceed-unverified`.

### 4. Conflicts

Versions do not move independently. Use the read-only probes in
[references/conflict-probes.md](references/conflict-probes.md) for peer conflicts, shared
transitives, runtime-to-toolchain coupling, native modules and Terraform constraints. When a
resolver refuses, quote its output verbatim in `Conflicts`; that refusal is the finding. Plans never
contain `--force`, `--legacy-peer-deps`, `--no-verify` or a hand-edited lockfile, because each yields
a tree no future install reproduces.

### 5. Order, group and type

Derive the order from the constraint graph:

1. **Prerequisites first.** If A's target requires B at some minimum, B moves first and A lists it in
   `Depends on`.
2. **Runtime first when it is the floor** (a library's new version requires a newer runtime), and
   only as far as the ceiling allows.
3. **Dependencies first when they block the runtime** (a native module with no build for the new
   runtime).
4. **Independent rows by `Rank`**, lowest number first.
5. **Riskiest verifiable steps before unverifiable ones**, so failures surface while the suite can
   still explain them.

Write the derivation into each step's `Why`: "CLI before provider, because the provider's target
requires a newer CLI than the one pinned" is reviewable; "runtime first, as usual" is not.

Keep changes unbatched. Each step is one independently verifiable change. When two changes cannot be
verified apart, group them as `atomic`, name each member and the reason it cannot move alone, and
record the coupling in `Conflicts`. Keep atomic groups as small as the constraints require, because
a group's failure cannot be bisected. Rows that cannot move in this plan go to `Not in this plan`
with their reason.

### 6. Breaking changes for every major

Cross a major only with its call sites located in this codebase. For each major:

1. Read the project's upgrade guide and the release notes for that major (WebFetch, or ask the user
   to paste them when web access is unavailable).
2. List the removed, renamed and behaviour-changed APIs and options.
3. Grep this repository for each one, excluding vendored and installed directories.

Record the result in `Breaking changes` as `file:line` entries, or as `none found (searched: ...)`,
which is a materially different claim from not having searched. Changes that keep an API's signature
but alter its behaviour are invisible to grep; put them in `Behaviour changes` with the code path
they affect. A major whose notes could not be read goes to `Not in this plan` as `needs-research`.

### 7. Write and verify the plan

Write `.upgrade/plan.md` exactly in the format in
[references/plan-format.md](references/plan-format.md). Then check it:

- every header field and step field is present, with a value from its enum;
- every `Depends on` number refers to an earlier step;
- every research `ID` appears once, in one step's `Rows` or in `Not in this plan`, except that a
  row with both an in-major step and a major step appears in exactly those two steps;
- `git status --porcelain` is empty (the probe was reverted and nothing outside `.upgrade/` changed).

Fix and re-check until all four hold. Then show the user the plan's header, step titles and
`Not in this plan`, and tell them that executing it is a separate, user-started command:
`/dependency-upgrades:upgrade-execute`.

## Without a checkout

On a surface with no shell or repository, build the plan from the research table and whatever test
output, CI configuration and manifests the user pastes. Set `Adequacy: not-assessed` unless pasted
baseline output supports a verdict, write `Baseline: none (no checkout)`, and return the plan in the
conversation instead of writing files.
