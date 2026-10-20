---
name: sb-change-control
description: >-
  How a change ships in the second-brain plugin repo (claude-code-plugin). Load this skill when the
  task involves: cutting or preparing a release; bumping the plugin version; deciding whether a
  change needs a version bump, a plan doc, a design spec, or is a straight fix; a "surface budget
  exceeded" failure from validate-plugin.sh; adding a new script/test/skill/agent file; writing
  commit messages or release-commit bodies for this repo; pre-push gate failures (tsc, vitest,
  bundle-current, run-all, validate-plugin, version-bump tripwire, portability guards); branch/PR
  policy questions; review-before-release process; or checking a proposed change against the repo's
  non-negotiable rules (fail-loud vs guard-fail-safe, cross-platform bash, no native deps, jq/CRLF
  discipline, no ln -s on MSYS, canonical wiki, prose-promises-need-machine-locks, autonomy).
  Do NOT load for: triaging a live runtime failure (use sb-debugging-playbook), authoring tests or
  understanding suite mechanics (use sb-validation-and-qa), recreating the dev environment or the
  build/bundle toolchain (use sb-build-and-env), or the history behind an incident in depth (use
  sb-failure-archaeology).
user-invocable: true
disable-model-invocation: false
---

# sb-change-control — how a change ships here

> **PRE-1.0 DIET (2026-07-24): `docs/plans/`, `docs/specs/`, `docs/superpowers/` and
> `CHANGELOG.md` were REMOVED from main** — the repo ships as a plugin and no longer carries
> internal planning docs. All existing citations below resolve via the `archive/docs` branch
> (`git show archive/docs:<path>`). Release records now live in release-commit bodies
> (`release: X.Y.Z — thesis` + bullets + gates line). New plans/specs go to the second-brain
> wiki, NOT the repo. The surface-budget baseline moved from `docs/` to
> `.claude-plugin/surface-budget.json` (validate-plugin.sh R8 reads the new path;
> references below already updated).

This repo is a Claude Code plugin ("second-brain") that ships as version-locked release batches.
Change control is unusually strict because the plugin's own history proves what happens without it:
releases shipped with core features broken before the gate existed (RELEASING.md:19-22), a release
once shipped with no version bump at all (0.30.2, PR #79), and stale `mcp/dist` bundles shipped
reviewed-source-but-old-code twice (0.24.7/0.24.8). Every rule below carries the incident that
created it.

Terms used throughout (defined once):

| Term | Meaning |
|---|---|
| BRAIN_DIR | Runtime state dir, default `~/.second-brain` (logs, transcripts, dreams, persona state) |
| KNOWLEDGE_DIR | Wiki/cold-tier dir, default `~/knowledge` (plugin.json `userConfig.knowledge_dir`) |
| surface budget | `.claude-plugin/surface-budget.json` — caps on live counts of skills/agents/scripts/shell-tests, enforced by `scripts/validate-plugin.sh` |
| tripwire | `tests/test-release-version-bump.sh` — shipped-source-changed ⇒ version strictly bumped vs `origin/main` |
| bundle-current | `tests/test-bundle-current.sh` — committed `mcp/dist/*.bundle.js` must byte-match a rebuild of committed `mcp/src` |
| MSYS / git-bash | The Windows bash environment this plugin is developed on (Windows is the dev platform; there is NO Windows CI lane) |
| dream / drainer | Background consolidation machinery — see sb-run-and-operate; only their change-control implications appear here |

## 1. Classify the change first

| Change type | Version bump? | Budget bump? | Docs needed | Example |
|---|---|---|---|---|
| Test-only or docs-only (`tests/`, `docs/`) | NO (tripwire excludes them) | Only if a new `tests/test-*.sh` file | none | new regression test |
| Bug fix in shipped surface | YES (patch) | only if new files | release-commit-body bullet; regression test expected | guard fix |
| Bug fix requiring user action | YES — as a MINOR, not patch (RELEASING.md:90-93) | — | release-commit body + `skills/upgrade/migrations/<ver>.md` | data-layout repair |
| New feature (multi-task) | YES | usually | plan doc in `docs/plans/` | new hook |
| New workstream / design decision | YES eventually | — | design note in the second-brain wiki (`decisions/`) FIRST, then a plan in `docs/plans/`, then code | P2/P3a/P6 |
| Anything touching autonomy, security boundaries, or data layout | YES | — | spec + plan; check CONSTITUTION.md hard constraints | quarantine work |

"Shipped surface" = the tripwire TRIGGERS list (`tests/test-release-version-bump.sh`):
`mcp/src mcp/dist mcp/package.json model-ladder.json scripts hooks skills agents bin systemd
.claude-plugin/plugin.json .claude-plugin/mcp.json` (`model-ladder.json` is behaviour-defining
data — editing a rung changes shipped behaviour like a `scripts/` edit). Deliberately excluded:
`tests/`, `docs/`, `.claude/`, `package-lock.json`, `marketplace.json` (its entry mirrors
plugin.json, which is already a trigger).

The fixed per-feature pipeline (observed across the whole history, e.g. the SP-4 sequence):
`docs(spec)` → `docs(plan)` → TDD `feat(...)` task commits → `fix(review): apply deep-review
findings` (adversarial review is a NAMED step, see §7) → `release: X.Y.Z — …` batch commit.
Every plan opens with a "Constitution compliance" section and carries Global Constraints restating
the portability bans and "Fail loud, never silent." The convention was set by the constitution-era
plans, removed from main in 0.34.0 — exemplar:
`git show archive/docs:docs/superpowers/plans/2026-06-30-p2-learning-to-guardrail.md`.
Plan/spec templates and house doc style are owned by sb-docs-and-writing.

Constitution check: every change is measured against `CONSTITUTION.md` (repo root, 66 lines) —
mission triad, "If a saved item does not actively guide a future decision, it does not belong,"
and three hard constraints (fully autonomous, untrusted-content isolation, cross-platform).
CLOSED (0.43.0): CONSTITUTION.md used to name a phantom `tests/test-surface-budget.sh` as the
budget gate; it now points at `scripts/validate-plugin.sh` R8 (lines 190-217), matching its own
Governance section. Do not re-open.

## 2. The surface budget — AT CAP (bump-with-justification required)

As of 0.49.0 (re-verified 2026-09-05) the budget and the live counts are EQUAL on all four axes:

```json
{ "skills": 16, "agents": 4, "scripts": 53, "tests": 162, "upgrade_skill_max_bytes": 8192 }
```

Verified live: `skills` dirs 16, `agents/*.md` 4, `scripts/*.sh` (top-level) 53,
`tests/test-*.sh` (top-level) 162, `skills/upgrade/SKILL.md` 4561 B. Consequence: ANY new
top-level file in `skills/`, `agents/`, `scripts/`, or a new `tests/test-*.sh` makes
`validate-plugin.sh` FAIL ("surface budget exceeded — …") unless `.claude-plugin/surface-budget.json`
is bumped IN THE SAME COMMIT. That is by design: "Growth must be a deliberate, git-blameable
choice. Ratchet DOWN freely." (`.claude-plugin/surface-budget.json` `_comment`). House convention: record
the delta in the release-commit body ("Surface budget: tests 158 -> 159", the 0.45.0 release).

Not budgeted: vitest `.test.ts` files (any count), `scripts/` subdirectories,
files under `.claude/` (the counter anchors at repo-root `skills/` etc.). Before adding a file,
prefer folding into an existing one — the ratchet exists because surface accretion was the
root cause the Constitution names ("accretion with no forcing function for simplicity").

Counting rules (exact, from `scripts/validate-plugin.sh:196-199`): top-level only, `-maxdepth 1`;
skills counts DIRECTORIES under `skills/`, agents counts `*.md`, scripts counts `*.sh`, tests
counts `test-*.sh`.

## 3. The release protocol — version lockstep in ONE commit

A release is one commit on `main` that stamps everything together. Anatomy, verified against the
real release commit `6fba312` (0.33.30, `git show 6fba312 --stat`):

1. `.claude-plugin/plugin.json` — `"version"` bumped.
2. `.claude-plugin/marketplace.json` — the `second-brain` plugin entry's `version` bumped to
   match (single entry since cost-router was removed in 0.35.x).
   `validate-plugin.sh` FAILS on any plugin.json↔marketplace.json drift.
3. **The release commit body is the release record** (until 1.0 — RELEASING.md "The
   checklist"): `release: X.Y.Z — thesis` subject, evidence-dense bullets naming
   files/env-defaults/tests, and the gates line. CHANGELOG.md left the tree in 0.34.0;
   pre-1.0 history lives on `archive/docs` — do NOT recreate the file.
4. Rebuilt `mcp/dist/*.bundle.js` — if ANY `mcp/src` file changed: `cd mcp && npm run bundle`
   (deps must be lockfile-exact first: `npm ci --prefix mcp`), commit the bundles. NEVER
   hand-edit anything under `mcp/dist/` — the bundle-current gate byte-compares dist against a
   rebuild of src, so a hand edit both fails the gate and signals routing around review.
5. `.claude-plugin/surface-budget.json` — bumped iff counts grew (§2).
6. `skills/upgrade/migrations/X.Y.Z.md` — ONLY when a real user precondition/action exists
   (18 files exist for ~200 releases; sparse by design). `skills/upgrade/SKILL.md` stays a lean
   runner ≤ 8192 bytes (machine-enforced).
7. Commit subject: `release: X.Y.Z — <thesis>`. Body: bullets — the body IS the release record,
   then the gates line: `Gates green locally: tsc, vitest (N pass, offline), bundle-current,
   run-all bash suite, validate-plugin, release version-bump tripwire, portability static
   guards.` Then the `Co-Authored-By: Claude <model> <noreply@anthropic.com>` trailer.

Version rules: informal SemVer (RELEASING.md:82-93) — patch = bug fixes with no behavior change
for healthy installs; a patch that requires user action SHOULD be a minor; major = on-disk
layout or user-visible CLI break. The new version must be STRICTLY greater than
`origin/main`'s, compared semver-numerically, never lexicographically (string compare says
`0.24.9 > 0.24.18` — the tripwire uses a BSD-safe dotted-numeric compare, no `sort -V`).
Queued plan docs may carry stale version targets — recompute at implementation time.

Tag contract: releases bind to the MERGE/push, not git tags — nothing has been tagged since
v0.22.1. The release record is the version-locked manifest pair + the release-commit body, with the
local suite green and the `ci` workflow green server-side (RELEASING.md:8-15).

(The old "CHANGELOG editing trap" warning that stood here is MOOT: CHANGELOG.md was removed from
main in 0.34.0, so no release edits it. The orphaned `## 0.33.19` heading survives on `archive/docs`.)

The full copy-paste release runsheet is in
[references/release-runsheet.md](references/release-runsheet.md).

## 4. The local gate list — every gate a change must pass BEFORE push

Ground truth is the release-commit gates line (e.g. `git log -1 --format=%B 6fba312`). Run from
repo root; all commands are git-bash/Linux/macOS-safe:

| # | Gate | Command | What a FAIL means |
|---|---|---|---|
| 0 | Deps (prereq) | `npm ci --prefix mcp` | lockfile drift / missing esbuild (gate 3 silently SKIPs without it) |
| 1 | Typecheck | `cd mcp && npx tsc --noEmit` | vitest transpiles per-file and will NOT catch tsc errors (0.24.10 incident) |
| 2 | Vitest, offline | `cd mcp && SECOND_BRAIN_DISABLE_EMBEDDINGS=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 npm test` | offline env replicates CI (CI has no HuggingFace network; a model fetch HANGS past test timeout) |
| 3 | Bundle-current | `bash tests/test-bundle-current.sh` | committed `mcp/dist` is STALE vs committed src → `cd mcp && npm run bundle` and commit |
| 4 | Shell suite | `bash tests/run-all.sh` (CI-equivalent when vitest already ran: `SB_RUN_ALL_VITEST=0 bash tests/run-all.sh`) | exit 0 + `ALL GREEN` is the release contract; suite mechanics owned by sb-validation-and-qa |
| 5 | Plugin validator | `bash scripts/validate-plugin.sh` | manifests, hooks.json shape, SKILL.md frontmatter (SKAG-6), version drift, SURFACE BUDGET, mcp.json path form |
| 6 | Version tripwire | `bash tests/test-release-version-bump.sh` | shipped source changed but version not strictly bumped vs `origin/main` (needs `origin/main` fetched, or set `SB_RELEASE_BASE_REF`) |
| 7 | Portability guards | `bash tests/test-script-portability.sh` | a bash-4-ism / GNU-only construct in `scripts/` (13 static checks as of 2026-09-05 — details owned by sb-validation-and-qa) |

Wrappers: `make test` = gate 4 incl. vitest; `make release-check` = vector-deps import smoke +
full suite; `make hook-install` wires `.githooks/pre-push` to re-run the suite on every push.

Bypass policy (RELEASING.md:68-80, verbatim doctrine): `SB_SKIP_PREPUSH=1 git push` or
`git push --no-verify` are OK only for a genuinely broken test with the fix already open in the
same session — never routine. "If you find yourself using a bypass twice in a row on different
commits, the gate is wrong, not your work. Open an issue, fix the test, then resume." Never
suggest bypassing a gate as a workflow; fix the gate or the change.

Cross-platform caveat (load-bearing): Windows is the dev platform but has NO CI lane — a
Windows-only green run is NOT release evidence for the BSD/macOS/Linux surface. CI runs a Linux
job (ubuntu, the 8 steps above) and a macOS job on real Apple bash 3.2 + BSD coreutils (4 tests
only, not the full suite). Conversely, the run-all false-green class (fixed 0.33.31) hit
hardest on Windows precisely because the local suite IS the Windows release gate. Practice:
run all gates locally, push, then confirm the `ci` workflow is green server-side before calling
the release done. Subagent verification on Windows alone has missed BSD/Linux CI failures.

## 5. Branch policy

Four delivery eras (from `git log`; corrected 2026-09-05 — the "direct-to-main since 0.33.17" era
below never actually closed out the PR requirement, it just had a lull):

1. 2026-04-24 → 05-25 — direct-to-main with occasional PRs (#1–#5).
2. 2026-05-26 → 06-24 — PR-per-release era (PRs #6–#83; branch names like
   `feat/0.29.0-surface-collapse-and-cap`). Last PR before the lull: #83, squashed as `f4856e5`
   (0.33.16, 2026-06-24).
3. 2026-06-26 → 07-23 — a direct-to-main lull (no merge commits landed in this window).
4. Since RELEASING.md's 2026-07-24 amendment — **current policy: every release lands via a PR**,
   gated on `tests/run-all.sh` green locally AND the `ci` workflow green server-side (RELEASING.md
   "Tag contract amendment"). Verified 2026-09-05: 15 `Merge pull request` commits land between
   `f4856e5` and HEAD (PRs up to #102), and HEAD itself is typically a merge commit.

Work on a feature/fix branch and open a PR; do not push release commits straight to `main`. CI's
version-bump tripwire compares against the PR base branch automatically (`SB_RELEASE_BASE_REF`
from `github.base_ref`).

## 6. Commit message conventions

- Prefixes: `feat` / `fix` / `docs` / `chore` / `test` / `refactor` / `release` / `plan`;
  distribution over the last 300 subjects: fix 95, feat 63, release 35, chore 15, test 14.
- Scope = subsystem: `(mcp) (kb) (dream) (capture) (extract) (drain) (search) (graph)
  (persona) (maintainer) (security) (review) (slug) (session-load) (cross-os) (ci) (tests)
  (portability) (release)`.
- Subject: imperative, em-dash-separated context, and the workstream ID when one exists —
  `feat(security): scope consolidation agents' node grant to bundled CLIs + source-scan guard (P6a)`.
  Workstream IDs: P0–P8 (constitution/diet), R1–R9 (deep-dive waves), SP-0–SP-5, task numbers.
- Release subjects: `release: X.Y.Z — <thesis>` (no `v`, em-dash).
- Bodies: dense prose mirroring the release bullets — exact env vars with defaults, arrow
  notation (`51->52`), the failure mode closed, what adversarial review caught, and (releases)
  the "Gates green locally: …" line.
- Trailer: `Co-Authored-By: Claude <actual model used> <noreply@anthropic.com>` — the
  convention is the REAL model name, not a fixed string.
- Self-correction is loud: a wrong claim in a prior commit gets a commit that says so
  (`6b1535a` "… — CORRECTS false claim in 9a03a26"). Never quietly fix history.

## 7. Review discipline — adversarial review is a named step

- Before a release batch lands, an adversarial/deep review pass runs against the change set;
  its findings land as dedicated commits: `fix(review): apply deep-review findings`,
  `62e1c42 fix(security): P6a follow-up — close field/read-path gaps + honest claims
  (adversarial review)`, `177d088 docs+log: scope P6b claims honestly + fix degraded-path log
  (adversarial review)`. Release bodies routinely state "Adversarial review (no critical)
  drove N … must-fixes".
- The repo's former in-house review tooling, `skills/code-review-deep/`, was removed in 0.44.0
  as out-of-scope (served none of the content classes); the fresh-context critic role
  moved to `persona_think` (`skills/doubt` step 4, `stop-verify-gate.sh` critic offer).
- Review scope this repo actually enforces, beyond bugs: HONESTY of claims (bullets like
  "scope P6b claims honestly" — overclaiming is a review finding), grants/least-privilege
  (agent frontmatter is product code, test-locked), and "does the gate test the real
  capability?" (presence-vs-effect, the 0.33.9/0.33.11 audit class — standing review question).
- Review learned the hard way to check REAL environments: the 0.24.29→0.24.30 slug-precedence
  miss shipped because all tests ran in sandboxes and "a test regression was 'fixed' by
  reverting precedence — green tests over real-env correctness." A live-env verification is
  part of review for env-dependent behavior (see the `verify` doctrine in sb-validation-and-qa).

## 8. The undo convention — forward-fix, never revert

There are ZERO `git revert` commits in 780+ commits. Undoing here means: a forward commit whose
body carries the rationale, frequently with an explicit "Supersedes"/"CORRECTS" marker, PLUS an
inverted or new machine guard so the reverted shape cannot come back. Canonical example: the
0.24.5 `.mcp.json` `${CLAUDE_PLUGIN_ROOT:-.}` form broke MCP startup for every installed user;
0.24.35 reverted it AND INVERTED the validator guard — `validate-plugin.sh` now FAILS on the
`:-` form, on a root `.mcp.json`, and on missing `mcpServers` wiring. When you back something
out, ask: "what guard makes the old shape a hard failure?"

## 9. The non-negotiables

Each rule below has a real incident behind it. One-line stories here; full archaeology is owned
by sb-failure-archaeology. A change violating one of these gets blocked in review regardless of
green gates.

| # | Rule | The incident behind it | Machine enforcement |
|---|---|---|---|
| 1 | **Fail LOUD everywhere — EXCEPT PreToolUse guards, which fail SAFE.** Errors route through `sb_log_error` (lib.sh); no `2>/dev/null` silent-exit patterns. But the three PreToolUse guards (`symlink-guard.sh`, `persona-tool-guard.sh`, `wiki-write-guard.sh`) always exit 0, convey verdicts via hookSpecificOutput JSON, and must STAY ARMED (emit deny) even when helpers/lib.sh are missing. No single doc states this split — it is enforced by history. | Swallowed tar stderr "hid this bug for several releases" (0.33.10 dream_accept); conversely a crashing guard would block every session, so guards fail-soft on their own errors but fail-CLOSED on missing tools (0.24.4: symlink-guard denies when `realpath` is absent) | Guard tests assert the inline-fallback deny with lib.sh unsourceable (`tests/test-symlink-guard.sh:249-264`); plans restate "Fail loud, never silent" as a Global Constraint |
| 2 | **Cross-platform bash: macOS bash 3.2 + BSD coreutils + git-bash/MSYS + Linux.** No `mapfile`, `declare -A`, `${x^^}`, `grep -P`, GNU `date -d` without a BSD fallback, no `case` inside `$(...)`, no GNU regex escapes (`\b \w \s \d`) in sed/grep, no `awk -v` for backslash data. | 0.24.33: a `case` in a comsub was a LOAD-TIME parse error on bash 3.2 — every macOS `dream_accept` broke; parses fine on bash 4+, so it shipped through green Linux CI. 0.28.2: GNU-only escapes silently matched NOTHING on BSD | `tests/test-script-portability.sh` (13 static checks over `scripts/` as of 2026-09-05, count drifts — re-verify with `grep -cE '^# [0-9]+\.' tests/test-script-portability.sh`) + the macOS CI job on real `/bin/bash` 3.2 |
| 3 | **No native (node-gyp) dependencies.** Pure-JS default; heavy deps only as an opt-in vetted tier (the vector-deps pattern: staged install, graceful degrade, junction links). | The vector-deps saga: 4.7 GB cache (0.20.0), installer that could destroy a working install (0.20.1); CONSTITUTION.md hard constraint 3; P3a plan explicitly REJECTS node-tree-sitter for this reason | Constitution + plan fences; no automated gate — reviewers block it (flag any new `dependencies` entry in `mcp/package.json`) |
| 4 | **jq discipline: `-c` for anything line-oriented; `tr -d '\r'` after every `jq -r` capture.** Windows git-bash jq 1.8.1 emits CRLF even on clean LF input and pretty-prints by default. | 0.30.1: 121 CR-contaminated `$(jq -r …)` captures across 29 scripts (config booleans read as `"true\r"`); 0.33.31: `jq` without `-c` pretty-printed projects.jsonl records across ~8 lines → the MCP registry reader went blind EVERY session | `tests/test-jq-crlf-windows.sh` (Windows-jq stub on Linux CI); the projects.jsonl membership test asserts one-compact-object-per-line |
| 5 | **Never `ln -s` a directory on MSYS; use `fs.symlinkSync(target, link, "junction")` from node.** On git-bash, `ln -s` silently DEEP-COPIES. | 0.33.7: each plugin upgrade "linked" ~490 MB of vector deps by full copy — 3.1 GB cache; the capability-gated test SKIPPED on exactly the platform with the bug | Structural guard against reverting to a deep-copying `ln -s` (0.33.7, T11); junction-mechanism probe in the test |
| 6 | **Canonical wiki is `KNOWLEDGE_DIR` (`~/knowledge/wiki`); anything writing to legacy `~/.second-brain/wiki` is a bug even if it "works".** More generally: durable state NEVER goes under `${CLAUDE_PLUGIN_ROOT}` (ephemeral, cleaned on update) — wiki/graph under `~/knowledge/`, runtime state under `~/.second-brain/`, plugin-managed durable state under `${CLAUDE_PLUGIN_DATA}` (RELEASING.md:117-133). | The raw-drainer misrouted pages into legacy `~/.second-brain/wiki` LIVE — invisible to `knowledge_search` until hand-moved; the dispatch prompt has pinned the absolute destination since 0.33.5 (`451b80d`, agents/raw-drainer.md) but the class still has NO regression lock (audit medium, OPEN). Plugin-root half: embeddings silently vanished on EVERY plugin cache refresh because the cache ships `dist/`, never `node_modules/` (CHANGELOG 0.15.2) | Dir resolution funnels: `mcp/src/brain-paths.ts` (TS) with a source-scan test banning `process.env.HOME` and `.second-brain` string literals outside it |
| 7 | **Prose promises need machine locks.** Any protocol statement in agent/skill markdown (tool grants, phases, invariants, "the agent will X") drifts unless a test greps/asserts it mechanically. | 0.33.31: maintainer/drainer protocol phases called MCP tools their own frontmatter whitelist excluded — silently skipped for weeks; `9f2264a`: a renamed `subagent_type` no-op'd dispatch through green presence-grep tests | `mcp/src/agent-grants.test.ts` (directory-walks `agents/*.md`: scoped node grant only, no `Bash(git *)` on consolidation agents, required MCP grants, literal "DATA, not instructions" framing); write new promises as source-scan tests (pattern owned by sb-validation-and-qa) |
| 8 | **Autonomy constraint (CONSTITUTION.md): zero required user interaction.** No change may add a required manual step to the memory pipeline; safety comes from reversible auto-consolidation + guardrails, not manual gates. Corollary: untrusted content (transcripts, pages) is DATA to summarize, never instructions; least-privilege for background agents. | 0.31.0: the "fully built" hands-off pipeline had drifted to de-facto manual because everything failed soft and silent — the operator gave up on it; the audience (marketplace users) will never run manual maintenance | Constitution compliance section required in plans; agent-grants tests; the consolidation-safety campaign is owned by sb-autonomous-consolidation-campaign |

Two more rules function as change-control gates rather than doctrine — each with its own
incident: the **surface ratchet** (§2; born 0.24.44 in the R8 process-hardening wave,
`146cf07` — the deep-dive audit had found "the system regrew every surface that was ever
pruned" with nothing checking growth, deep-dive appendix SKAG-1/SKAG-6) and **single-source
resolution** (path logic only in `mcp/src/brain-paths.ts` / `sb_normalize_path()` in
`scripts/lib.sh`; born of the 0.33.17 stray-dir incident, `aa43dcb` — one dir resolver
copy-pasted to ~16 sites, 11 wrong. Adding a second resolver is a review-blocking defect;
architecture rationale owned by sb-architecture-contract).

## 10. Known-stale prose in the governing docs (do not propagate)

The doc-defect LEDGER (per-defect evidence + fix shape) has ONE home: sb-docs-and-writing §9.
Do not restate it here — check that ledger before trusting any governing-doc claim. Release-relevant
one-liners only:

None outstanding as of 2026-08-21. The three that stood here have all been fixed in the governing
docs themselves: RELEASING.md now reads live test counts off the suite instead of freezing them,
carries no `## vX.Y.Z` heading-format claim, and states the release-via-PR contract; CONSTITUTION.md
names `scripts/validate-plugin.sh` R8 as the real budget gate. The fourth — the orphaned
`## 0.33.19` CHANGELOG heading — is MOOT since CHANGELOG.md was removed from main in 0.34.0.
Re-verify by reading those two files before trusting this line.

## Sibling skills (one home per fact — defer, don't duplicate)

- sb-debugging-playbook — symptom→triage for live failures (a gate failing for environmental reasons).
- sb-validation-and-qa — test-suite mechanics, run-all env knobs/SKIP semantics, house test patterns, CI lane details, add-a-test checklist.
- sb-build-and-env — dev-env recreation, esbuild/bundle model internals, vector-deps install.
- sb-failure-archaeology — the full incident chronicle behind every rule in §9.
- sb-architecture-contract — WHY the invariants (funnels, tiers) are shaped this way; also owns
  the add-a-hook and add-an-MCP-tool authoring recipes (its references/extending-the-plugin.md).
- sb-docs-and-writing — CHANGELOG/plan/spec/migration templates and voice; owns the doc-defect ledger (§9).
- sb-config-and-flags — every env knob (`SB_*`) with defaults and kill switches.
- sb-run-and-operate — install/upgrade/operate; data geography beyond the invariant stated here.

## Provenance and maintenance

Derived from repo evidence read/run on 2026-07-05 against the working tree (HEAD `6fba312` =
0.33.30 + the uncommitted 0.33.31 batch; `plugin.json` already says 0.33.31): RELEASING.md,
CONSTITUTION.md, archive/docs:CHANGELOG.md (head), `.claude-plugin/surface-budget.json`, `scripts/validate-plugin.sh`,
`tests/test-release-version-bump.sh`, `tests/run-all.sh`, Makefile, `.githooks/pre-push`,
`scripts/lib.sh` (:1-51), `scripts/symlink-guard.sh` / `scripts/wiki-write-guard.sh` headers,
`mcp/src/agent-grants.test.ts`, `mcp/package.json`, `.github/workflows/ci.yml`, and git history
(`git show 6fba312 --stat`, PR-merge census, `f4856e5`, revert census). Authored 2026-07-05 at
version 0.33.31 (uncommitted working tree).

Volatile facts — re-verify before trusting:

```bash
jq -r .version .claude-plugin/plugin.json                      # current version (was 0.33.31)
cat .claude-plugin/surface-budget.json                                    # budget caps (re-verified 2026-09-05: 16/4/53/162/8192)
echo "skills:$(find skills -mindepth 1 -maxdepth 1 -type d|wc -l) agents:$(find agents -maxdepth 1 -name '*.md'|wc -l) scripts:$(find scripts -maxdepth 1 -name '*.sh'|wc -l) tests:$(find tests -maxdepth 1 -name 'test-*.sh'|wc -l)"  # live counts vs caps (were AT CAP)
git log -1 --format=%B $(git log --format=%h --grep='^release:' -1)  # latest release body = current gates line
git log --oneline --grep="Merge pull request" -1               # branch policy is PR-merge-gated since 2026-07-24 (re-verified 2026-09-05: #102 last merge commit)
grep -n 'TRIGGERS=' tests/test-release-version-bump.sh         # tripwire trigger list
ls skills/upgrade/migrations/ | wc -l                          # migration-file count (was 18)
grep -n 'validate-plugin.sh' CONSTITUTION.md                   # budget gate ref (must NOT say test-surface-budget)
```
