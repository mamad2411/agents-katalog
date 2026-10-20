---
name: sb-validation-and-qa
description: >-
  Test-suite mechanics and the evidence bar for the second-brain plugin repo
  (claude-code-plugin). Load this when you are about to run tests, add a shell
  or vitest test, interpret tests/run-all.sh output (PASS/FAIL/SKIP semantics,
  the false-green trap), answer "will CI reject my bash?" (the 13 bash-3.2/BSD
  portability static guards), write a test that exercises Windows-only branches
  on Linux (PATH-stubbed cygpath/realpath), run vitest offline, lock a prose
  promise with a source-scan test, bump the surface budget for a new test, or
  judge whether a claim ("fixed", "passing", "done") has sufficient evidence.
  Keywords: run-all, SKIP, false green, vitest offline, portability guard,
  surface budget exceeded, exec bit, test-the-test, tautological test,
  fallback branch, mktemp sandbox. NOT for: the release gating sequence,
  version-bump tripwire policy, or gate-bypass rules (use sb-change-control);
  triaging a live failure (sb-debugging-playbook); proof methods beyond
  testing such as measurements and ablations (sb-proof-and-analysis-toolkit).
---

# Validation and QA — what counts as evidence, and how the suite works

This repo is a Claude Code plugin ("second-brain") with two test lanes: a bash
suite (`tests/test-*.sh`, run by `tests/run-all.sh`) and a vitest suite under
`mcp/` (TypeScript MCP server + CLIs). The runner's own header states the
contract: "a release tag is valid ONLY when this script exits 0 with all
green" (`tests/run-all.sh:7-9`).

Terms used below, defined once:

- **BRAIN_DIR** — runtime state dir, default `~/.second-brain`.
- **KNOWLEDGE_DIR** — wiki home, default `~/knowledge`. Both derive from
  `$HOME` when unset (that derivation is load-bearing for test isolation).
- **guard** — a PreToolUse hook script under `scripts/` (e.g.
  `symlink-guard.sh`) that emits an allow/deny JSON decision.
- **surface budget** — `.claude-plugin/surface-budget.json`, the growth ratchet
  enforced by `scripts/validate-plugin.sh` (details in sb-change-control;
  the `tests` key is enforced here in the add-a-test checklist).

## The evidence bar

These rules are enforced by history, not by any single doc. Each one exists
because its absence shipped a bug.

| # | Rule | The incident that made it law |
|---|------|-------------------------------|
| 1 | No completion claim without command output. "Fixed"/"passing" means you ran the command and can quote the summary line (`pass:/fail:/skip:` + `ALL GREEN`, or vitest's `Tests N passed`). | "Until v2.11.0, version numbers were aspirational. Each `fix(...)` commit was hopeful, not proven." (`RELEASING.md:19-20`) |
| 2 | Green CI does not prove Windows. There is NO Windows CI lane — a Windows-local `bash tests/run-all.sh` is mandatory evidence for any change touching bash/hooks/paths. | All three PreToolUse guards were silently inert on Windows (the dev platform) for months; every one of those releases had green CI (CHANGELOG 0.33.31 bullet 1; `scripts/lib.sh:14-29` comment). |
| 3 | A Windows-only pass does not prove CI. macOS bash 3.2 + BSD coreutils are real CI targets; run the CI-equivalent gates locally before push. | 0.33.15: `OUT=$(cmd); RC=$?` under `set -e` aborts on bash 4/5 but not bash 3.2 — macOS passed, Linux CI failed (CHANGELOG 0.33.15). |
| 4 | Test EFFECT, not PRESENCE. A test that greps a source/prompt file for a string proves nothing; run the behavior and assert its result. | "506 green tests missed 14 bugs … an audit found 53 tautological tests" (CHANGELOG 0.24.50, ~line 1106); 16 presence-vs-effect gaps closed in 0.33.9/0.33.11. |
| 5 | Fallback/default branches are part of the contract. Test with the tool ABSENT (`PATH=""`), the lib unreachable (`CLAUDE_PLUGIN_ROOT=/nonexistent`), and kill switches BOTH ways. | Stated as "the house rule" in `tests/test-normalize-path.sh:64-65`; the 0.33.7 `ln -s` deep-copy bug hid behind a capability probe that silently SKIPPED on exactly the platform with the bug. |
| 6 | Test-the-test: a new regression lock must be shown to FAIL on pre-fix code before you trust it (recipe R6 below). | 0.30.2 shipped unversioned because the drift check compared two files that were both stale — it agreed with itself (CHANGELOG 0.30.2). |
| 7 | SKIP is a verdict to audit, not a pass. A whole file counts SKIP if it prints one `SKIP:` line, even when everything else passed; check the `skipped:` list in the summary. | The 0.33.31 run-all false-green fix (next section) and the 0.33.7 skip-hid-the-bug case. |
| 8 | Sandbox green does not prove the real environment. When behavior depends on ambient env (`CLAUDE_PROJECT_DIR`, pins), verify live at least once. | 0.24.30: every test sandbox set the var the real env lacked; a regression was "fixed" by reverting to wrong precedence — "green tests over real-env correctness" (CHANGELOG, ~line 1310). |
| 9 | Assert independent oracles — filesystem/git facts, never the script's own claims. | `tests/test-dream-accept-guards.sh:1-5`: "ORACLE: the real live-wiki page count on disk BEFORE vs AFTER … not a re-read of the script's own claim". |

## Golden inventory — as of 0.33.31, working tree, 2026-07-05; re-verified 2026-09-05 at 0.49.0

Counts drift with every release. Trust these commands, not stale prose. `RELEASING.md`'s
2026-07-24 amendment already dropped the old frozen "24 shell + 59 vitest = 83 checks" line in
favor of "read the live counts off the suite output" — do not reintroduce a frozen number there.

| Fact | Value | Re-verify (repo root) |
|------|-------|-----------------------|
| Shell tests | 162 files | `ls tests/test-*.sh \| wc -l` |
| Budget cap for tests | 162 | `jq .tests .claude-plugin/surface-budget.json` |
| Vitest files | 66, all under `mcp/src/**` — the old `mcp/test/` tree no longer exists; `vitest.config.ts` `include` is `src/**/*.test.ts` only | `find mcp/src -name '*.test.ts' \| wc -l` |
| Vitest cases (offline) | 509 total: 496 pass, 13 skipped | `cd mcp && SECOND_BRAIN_DISABLE_EMBEDDINGS=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 npx vitest run 2>&1 \| grep -E '^\s*Tests'` |
| Golden retrieval fixture | 12 queries over `tests/fixtures/eval-wiki`; acceptance: recall@2 = 1.0 (`SB_EVAL_MIN_RECALL`, default 1.0 — a SINGLE missed query fails the release gate; the old 0.8 gate stayed green through the hub-boost bug) | `awk 'END{print NR}' tests/fixtures/eval-queries.jsonl`; `bash tests/test-knowledge-eval.sh` → `PASS: recall+token gate` |
| Full-suite wall baseline | ~156 s (Pi 5, recorded) | `tests/run-all.sh:157-159` comment; compare your `wall:` summary line |

## tests/run-all.sh — the aggregate runner

Run it: `bash tests/run-all.sh` (or `make test`). Every single test is also
standalone-runnable: `bash tests/test-<name>.sh`.

**Discovery and invocation.** Globs `tests/test-*.sh` (top-level only —
subdirectories are invisible) and runs each via `bash "$script"`, so the exec
bit is not needed at runtime — but it IS enforced in git: `tests/test-exec-bits.sh`
walks `git ls-files 'tests/test-*.sh'` and fails any file not stored as mode
100755 (fix: `git update-index --chmod=+x <file>`). If `mcp/package.json`
exists, one extra suite entry named `vitest (mcp)` runs
`npx vitest run` in `mcp/` and is counted as a single PASS/FAIL.

**Env knobs** (defaults from `tests/run-all.sh:12-25`):

| Var | Default | Effect |
|-----|---------|--------|
| `SB_RUN_ALL_QUIET` | `0` | `1` = suppress per-test stdout echo; FAIL output (last 40 log lines) always prints |
| `SB_RUN_ALL_VITEST` | `1` | `0` = skip the vitest lane (CI sets `0` — vitest already ran as its own step) |
| `SB_RUN_ALL_TIMEOUT` | `120` (s) | per-test timeout via `timeout N bash <script>`; applied only when a `timeout` binary resolves. The SAME single value also caps the ENTIRE vitest run |
| `SB_RUN_ALL_TESTS_DIR` | `<repo>/tests` | fixture-dir override, used only to test the runner itself (recipe R6) |

**Per-test HOME isolation.** Every test — and the vitest lane — runs with
`HOME` set to a fresh per-test dir under a suite-level `mktemp -d` sandbox
(`tests/run-all.sh:28-36,71-76,129-137`), so a test that forgets its own
sandbox cannot touch the real knowledge base (the 0.24.32 leak class: 4 tests
polluted the real `~/.second-brain` on every suite run). The real HOME passes
through as `SB_SUITE_REAL_HOME_PATH`, which arms lib.sh's G3 suite guard: a script whose brain or
knowledge dir still resolves to the real one gets a quarantine dir instead (it never exits: that
killed PreToolUse guards), the trip is appended to `SB_SUITE_GUARD_MARKER`, and run-all fails the
whole run when that marker exists. BRAIN_DIR/KNOWLEDGE_DIR are deliberately
NOT preset — they derive from `$HOME`, and presetting them broke 5 tests that
sandbox HOME and rely on the derivation (comment at `tests/run-all.sh:28-34`).

**SKIP semantics (exact — post-0.33.31 fix).** A test counts as SKIP only when
BOTH hold (`tests/run-all.sh:84-99`):

1. exit code == 0, AND
2. its output contains a line matching ERE `^SKIP[: ]`.

The exit-code gate deliberately comes first. The pre-fix runner grepped for
SKIP before checking the exit code, so a test that printed a mid-run `SKIP:`
line for one optional subtest and then FAILED a real assertion was silently
reclassified as SKIP — the suite reported ALL GREEN on real failures. Double
bug: the old ERE class `[:\s]` is the literal set `{':','\','s'}` and never
matched a space. Worst on Windows, where the local suite IS the release gate
(no CI lane). Fixed as of 0.33.31; regression-locked by
`tests/test-run-all-skip-semantics.sh`. Corollary: a file that prints one
`SKIP:` subtest line and otherwise fully passes (exit 0) is counted SKIP for
the WHOLE file — the suite still exits 0 and lists it under `skipped:`.

**Summary format** (parse-stable, `tests/run-all.sh:153-172`):

```
--- summary ---
  pass: <N>
  fail: <N>
  skip: <N>
  wall: <N>s
```

then `FAILED:` + `exit 1` if any fail; else an optional `skipped:` list, then
`ALL GREEN` + `exit 0`. Per-test lines: `PASS|FAIL|SKIP <name> <elapsed>s`
(FAIL adds `(ec=N)` + the last 40 log lines).

**Wrappers.** `make test`, `make test-quiet`, `make release-check`
(vector-deps smoke + suite). `.githooks/pre-push` runs the suite on every push
once wired via `make hook-install`; bypasses (`SB_SKIP_PREPUSH=1`,
`--no-verify`) and when they are legitimate are sb-change-control's topic.

## CI lanes (.github/workflows/ci.yml)

Two jobs; triggers: `pull_request` + push to `main`. Only SHA-pinned official
actions, read-only token.

**Job `linux`** (ubuntu-latest, node 22, 20-min timeout), steps in order:

| Step | Command |
|------|---------|
| deps (lockfile-exact) | `npm ci --prefix mcp` |
| typecheck | `cd mcp && npx tsc --noEmit` |
| vitest (offline) | `cd mcp && npm test` with `SECOND_BRAIN_DISABLE_EMBEDDINGS=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1` |
| bundle-current gate | `bash tests/test-bundle-current.sh` (byte-compares committed `mcp/dist` vs a rebuild — mechanics in sb-change-control) |
| bash suite | `bash tests/run-all.sh` with `SB_RUN_ALL_VITEST=0` |
| plugin validator | `bash scripts/validate-plugin.sh` (includes the surface budget) |
| version-bump tripwire | `bash tests/test-release-version-bump.sh` (policy in sb-change-control) |

Why offline vitest: CI has no HuggingFace network; a model fetch HANGS past
the 5s default test timeout, so CI never downloads a model. The embedding/RRF
path is covered only where the model exists locally.

**Job `macos`** (macos-latest — the bash-3.2/BSD lane). Every step runs under
`/bin/bash` (Apple bash 3.2.57), NOT the runner default, and it does NOT run
the full suite — only these five (re-verified 2026-09-05, `.github/workflows/ci.yml`
macOS job):
`tests/test-dream-lifecycle.sh`, `tests/test-script-portability.sh`,
`tests/test-stop-extract.sh`, `tests/test-dream-autostage.sh`, `tests/test-loop-smoke.sh`.

**There is NO Windows CI lane.** Windows coverage = the PATH-stub tests
(recipe R3) + your local run. This is why evidence-bar rules 2 and 3 exist.

**Local CI parity** (what "I ran the gates" means as test evidence; the
release process around it is sb-change-control's):

```bash
npm ci --prefix mcp
cd mcp && npx tsc --noEmit && \
  SECOND_BRAIN_DISABLE_EMBEDDINGS=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 npm test
cd .. && bash tests/test-bundle-current.sh && \
  SB_RUN_ALL_VITEST=0 bash tests/run-all.sh && \
  bash scripts/validate-plugin.sh && \
  bash tests/test-script-portability.sh && \
  bash tests/test-release-version-bump.sh   # CI's last linux step; needs `git fetch origin main`
                                            # first (or SB_RELEASE_BASE_REF) — policy: sb-change-control
```

## The 13 portability static guards ("will CI reject my bash?")

`tests/test-script-portability.sh` statically scans all `*.sh` under
`scripts/` (comment-only matches excluded; it also covered `cost-router/scripts/`
until that subplugin was removed in 0.35.x). It runs
in the normal suite AND on real bash 3.2/BSD in the macOS lane. Run it before
pushing any bash change: `bash tests/test-script-portability.sh`.

| # | Banned / required | Why (incident) | Portable fix |
|---|-------------------|----------------|--------------|
| 1 | No `mapfile`/`readarray` | bash-4 builtins; macOS `/bin/bash` is 3.2 | `while IFS= read -r` loop |
| 2 | No `declare -A`/`local -A`; no `${x^^}`/`${x,,}` | bash-4 features | indexed arrays / `tr` |
| 3 | No `grep -P` | PCRE absent on BSD/macOS grep | `grep -E` or `-F` |
| 4 | GNU `stat -c` needs a BSD `stat -f` fallback on the SAME line | BSD stat has no `-c` | `stat -f … 2>/dev/null \|\| stat -c …` |
| 5 | GNU `date -d`/`--date` (incl. `-u -d`) needs a BSD form (`-v`, `-r <epoch>`, or `-j -f`) in the same file | BSD date has no `-d` | pair both forms |
| 6 | `find -printf` needs a `stat (-f\|-c)` fallback, or a literal `NOT GNU` marker | BSD find has no `-printf` | stat-based fallback |
| 7 | Every `command -v timeout` must also resolve `gtimeout` | stock macOS has no `timeout`; brew coreutils ships `gtimeout` | probe both |
| 8 | No `case` inside `$(...)` command substitution | bash 3.2's parser miscounts the `)` closing each case pattern → hard syntax error at LOAD time for the whole script; NOT reproducible by `bash -n` on bash 4+/5 (0.24.33: every `dream_accept` broken on macOS) | `[[ "$x" == pat* ]]` glob inside the comsub, or lift the case out |
| 9 | No bare `"${ARR[@]}"`/`"${ARR[*]}"` of an array initialized empty (`NAME=()`) | "unbound variable" under `set -u` on bash < 4.4 | `${ARR[@]+"${ARR[@]}"}` on the line, or a `${#ARR[@]}` length check in the file |
| 10 | No duplicate top-level function definitions in one script | second def silently shadows the first, last-def-wins (0.24.48 `sb_validate_wiki`: the active def returned nothing, telemetry dead, all tests green) | rename or merge |
| 11 | No GNU-only regex escapes (`\b \w \s \d`, `\xNN`) inside a sed/grep program | BSD sed/grep treat them as literal chars — the pattern silently matches NOTHING (0.28.2: ANSI never stripped, verify-gates never fired) | `$'\xNN'` literal bytes, POSIX classes (`[[:alnum:]_]`, `[[:space:]]`, `[[:digit:]]`), or `grep -w` |
| 12 | No `$(basename …)`/`$(dirname …)` inside a `while … read` loop body in a HOT-PATH script (every script wired into `hooks/hooks.json`, derived live from the file, plus the drainer-tick chain) | Each spawn costs ~30-60ms on MSYS vs ~1ms on Linux; per-item spawns in a hot loop made `test-transcript-archive` take 258s on Windows vs 8s on Linux (2026-08-23) | `"${x##*/}"` / `"${x%/*}"` builtins instead |
| 13 | jq must never append DIRECTLY to a `*.jsonl` file via `>>` (the D120 class) | Native jq.exe on Windows inherits a plain end-of-file handle, not `O_APPEND`; two concurrent writers race at the same offset and tear the JSONL | build the line with `jq -c` into a var, then `printf`/`echo` it with `>>` |

Checks 8, 9, 12 and 13 are documented heuristics (depth/pattern tripwires, not a bash
parser) — keep command substitutions and loop bodies matching the documented shape and they stay
sound.

## House test patterns (recipes, each with a real in-repo example)

### R1 — Skeleton

Every shell test follows this shape (e.g. `tests/test-normalize-path.sh:1-13`):

```bash
#!/bin/bash
# <what is under test + the bug/finding/spec this locks>
set -u                                          # NOT set -e — exit codes checked per assertion
ROOT="$(cd "$(dirname "$0")"/.. && pwd)"        # repo root from the test's own location
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT     # sandbox, always cleaned
fail() { echo "FAIL: $1"; exit 1; }
pass() { echo "PASS: $1"; }
# ... assertions ...
echo; echo "ALL PASS"    # convention; the runner keys off exit code + SKIP grep, not this line
```

Helper variants in the wild: `aeq EXPECTED ACTUAL LABEL`
(`test-normalize-path.sh:12-13`); `assert_allow`/`assert_deny` jq-decoding
helpers for guard hook-JSON, where deny also greps
`permissionDecisionReason` for a needle (`test-symlink-guard.sh:39-56`).

### R2 — Environment sandboxing

- `export HOME="$TMP/home"` + mkdir exactly the dirs the code checks
  (`test-symlink-guard.sh:10-12`). Sandbox even though run-all isolates HOME —
  every test must be standalone-runnable.
- Export `BRAIN_DIR`, `KNOWLEDGE_DIR`, `CLAUDE_PLUGIN_OPTION_KNOWLEDGE_DIR`
  when the script under test reads them (`test-dream-accept-guards.sh:18-38`,
  a per-case `setup()` function).
- Unset hostile ambient env up front:
  `unset CLAUDECODE ANTHROPIC_API_KEY SB_EXTRACTOR_LOCAL_URL 2>/dev/null || true`
  (`test-dream-accept-guards.sh:7`).
- `export CLAUDE_PLUGIN_ROOT="$ROOT"` when the script resolves siblings
  through it (`test-graph-cluster-shim.sh:14`).

### R3 — PATH-stubbing: Windows branches run on Linux/BSD CI

The suite's signature move: write tiny `#!/bin/sh` stub executables into
`$TMP/bin`, `chmod +x`, prepend to `PATH` — so Git-Bash/Windows-only branches
are exercised deterministically on any OS.

- Stub `cygpath` emulating `cygpath -u 'C:/x/y'` → `/c/x/y`
  (`test-normalize-path.sh:20-32`). Ordering discipline: source `lib.sh`
  BEFORE the stub goes on PATH, so lib.sh's own load-time normalization runs
  against the real environment (`:34-39`).
- Stub pair `cygpath` + `realpath` reproducing the exact Windows failure shape
  (realpath re-emitting `C:/…` drive form) so the guard-inert-on-Windows bug
  is asserted on Linux CI — including case-varied `.SSH` (NTFS
  case-insensitivity bypass) and `\\?\C:\` extended-length forms
  (`test-symlink-guard.sh:191-247`, tests 20-22).
- Stub `realpath` that just `exit 127`s → proves the guard fails CLOSED when
  the binary is absent, AND that a normal project write is still allowed (no
  over-blocking) (`test-symlink-guard.sh:152-163`, test 17).
- Inverse capability probes for genuinely platform-bound subtests:
  `supports_symlinks()` — is `ln -s` a REAL symlink here or an MSYS file copy?
  (`test-symlink-guard.sh:17-25`); `supports_chmod_restrict()`
  (`test-dream-accept-guards.sh`); `command -v rsync` gating. When absent:
  `echo "SKIP: <subtest> — <reason>"` + a `pass "... (skipped)"` placeholder,
  keep going, exit 0.

### R4 — The fallback-branch rule

"Exercising this branch is the house rule: test the resolution path with the
tool ABSENT, not only the fixture-forced present case"
(`test-normalize-path.sh:64-65`). The three shapes:

- `got=$( PATH=""; sb_normalize_path 'C:\Users\me\x' )` — no cygpath anywhere;
  assert the degraded-but-correct result (`test-normalize-path.sh:66-67`).
- `CLAUDE_PLUGIN_ROOT=/nonexistent` — bundle unreachable → shim must emit `[]`
  and exit 0 (`test-graph-cluster-shim.sh:49-52`); lib.sh unsourceable → the
  guard's minimal INLINE fallback normalizer must still deny
  (`test-symlink-guard.sh:249-264`, test 23).
- Kill switches asserted BOTH ways, including independence between switches:
  `SB_SYMLINK_GUARD=off` → empty output (`test-symlink-guard.sh:111-114`);
  `SB_DREAM_REFLECT=off` gates `--gate reflect` to `[]` but must NOT gate the
  default consumer, and symmetrically for `SB_DREAM_SUMMARIZE`
  (`test-graph-cluster-shim.sh:69-81`).

### R5 — Independent oracle + regression-lock comment

Assert filesystem/git facts, never the script's own claims: live-wiki page
count on disk before vs after a refused accept
(`test-dream-accept-guards.sh:1-5`); a backup verified by a tar ROUND-TRIP
that reproduces the pre-accept snapshot, "not merely 'a file exists'".

Every regression test carries a comment naming the one-line source mutation
that flips it to FAIL: "drop the RESOLVED normalization in symlink-guard.sh
and this test flips to a silent allow (FAIL)" (`test-symlink-guard.sh:196-197`);
"drop the generated:true filter in graph-cluster-cli.ts and members gain
'reflection-a' (FAIL)" (`test-graph-cluster-shim.sh:87-88`). Write this
comment — it is the test's spec.

### R6 — Test-the-test

Prove a new regression lock fails on pre-fix code before trusting it.

For a fix already in your working tree, the stash method (keep the new test,
stash ONLY the fixed source):

```bash
git stash push -- scripts/<fixed-file>.sh   # fix gone; test stays
bash tests/test-<topic>.sh                  # EXPECT FAIL — a pass here means the lock is tautological
git stash pop                               # restore the fix; test goes green
```

(Path-scoped `stash push --` touches only the named file — safe in a dirty
tree, but double-check `git stash show` before popping.)

For test infrastructure itself, drive the real runner at throwaway fixtures:
`tests/test-run-all-skip-semantics.sh` generates fixture tests under `$TMP`,
runs `SB_RUN_ALL_TESTS_DIR="$D" SB_RUN_ALL_VITEST=0 SB_RUN_ALL_QUIET=1 bash
tests/run-all.sh`, and asserts the aggregate exit code + verdict counters
(mid-run SKIP + exit 1 → FAIL/exit 1; pure SKIP + exit 0 → SKIP/exit 0).

### R7 — Source-scan machine locks (vitest): prose promises get greps

Any protocol statement living in markdown or a doc comment (grants, phases,
invariants) drifts unless a test mechanically asserts it. Pattern: glob the
source tree, assert the invariant, list exemptions explicitly, and
directory-walk rather than hardcoding file lists so future additions are
auto-covered.

- `mcp/src/brain-paths.test.ts:90-114` — no non-test source file may contain
  `process.env.HOME` (the Windows CWD-relative `.second-brain` footgun) or a
  string literal starting `.second-brain` (re-implementing the resolver
  outside `brain-paths.ts`); test files + `brain-paths.ts` itself exempt.
- `mcp/src/agent-grants.test.ts` — walks `agents/*.md` ("not a hardcoded
  list, so a NEW agent added later with an over-broad grant is caught too")
  and enforces: only node grant allowed is exactly
  `Bash(node ${CLAUDE_PLUGIN_ROOT}/mcp/dist/*)`; no `Bash(*)`/bare `Bash`;
  body-runs-node ⇒ frontmatter carries the scoped grant; maintainer/drainer
  grant every `knowledge_*` MCP tool their protocol calls; the three
  consolidation agents carry the literal `DATA, not instructions` framing and
  no `Bash(git *)` grant.

The shell lane's analogue is `tests/test-script-portability.sh` (above).

### R8 — Misc conventions worth copying

- Build JSON with `printf` + manual escaping, NOT `jq --arg`, when the payload
  carries POSIX paths — Windows/Git-Bash jq translates POSIX paths to `C:\`
  form and breaks HOME-prefix checks (`test-symlink-guard.sh:28-29`).
- Windows jq emits CRLF even on `-r` output — strip with `tr -d '\r'` in any
  capture a comparison depends on.
- Prerequisite probes fail loud with an actionable message:
  `[ -f "$BUNDLE" ] || fail "build mcp first: cd mcp && npm run build (missing $BUNDLE)"`
  (`test-graph-cluster-shim.sh:11-13`).
- Assert determinism explicitly when the contract requires it: identical
  output across two runs (`test-graph-cluster-shim.sh:39-41`).

## Checklist: add a shell test

1. Create `tests/test-<topic>.sh` — the name MUST match `tests/test-*.sh` and
   stay top-level (subdirs are neither discovered nor budget-counted).
2. Start from the R1 skeleton; the doc header names the script under test and
   the bug/finding it locks.
3. Sandbox everything the code touches (R2). Standalone-runnable is required.
4. Exercise the Windows-only branches via PATH stubs (R3) AND the fallback
   branches (R4).
5. Assert independent oracles + write the regression-lock comment (R5).
6. Prove the test fails on pre-fix code (R6).
7. Any `scripts/*.sh` you add alongside MUST pass all 13 portability guards.
   Caveat: the static guard scans only `scripts/`
   (`tests/test-script-portability.sh`; it dropped `cost-router/scripts/` when that
   subplugin was removed) — your TEST file is never
   scanned, the linux CI lane runs it on bash 5, and the macOS lane runs only
   its four fixed tests. A bash-4-ism in a new test therefore sails through
   CI green and breaks only for macOS contributors running the suite locally
   — keep test files to the same portable subset by hand.
8. SKIP rules: whole-file skip = `echo "SKIP: <reason>"; exit 0`.
   Optional-subtest skip = `echo "SKIP: …"` + a `pass "(skipped)"`
   placeholder, keep exit 0 — knowing the whole file then counts SKIP.
   NEVER print a `^SKIP[: ]` line and deliberately exit non-zero.
9. Keep runtime well under 120 s (`SB_RUN_ALL_TIMEOUT` default).
10. Commit with the exec bit: `git update-index --chmod=+x tests/test-<topic>.sh`
    (else `test-exec-bits.sh` fails the suite).
11. **Budget bump, same commit (mandatory):** raise `"tests"` in
    `.claude-plugin/surface-budget.json` by +1, or `validate-plugin.sh` fails with
    "surface budget exceeded — tests=N > budget <cap> (bump
    .claude-plugin/surface-budget.json in the same commit to grow deliberately)".
    The counter is `find tests -maxdepth 1 -name 'test-*.sh' -type f | wc -l`
    — shell tests only; `.test.ts` files are not budgeted. House convention:
    record the delta in the release-commit bullet ("Surface budget: tests
    151→153").
12. Version bump: NOT required for a purely `tests/` + `docs/` change; if the
    same commit touches shipped paths, sb-change-control's tripwire rules
    apply.
13. Verify: `bash tests/test-<topic>.sh` → `bash tests/run-all.sh` →
    `bash scripts/validate-plugin.sh`.

## Checklist: add a vitest test

1. Create `<name>.test.ts` in `mcp/src/**` (co-located unit / source-scan
   tests — the old separate `mcp/test/` tree was folded into `src/**` and no
   longer exists), matching the `include: 'src/**/*.test.ts'` in
   `mcp/vitest.config.ts`. Never rely on `dist/` copies: the config excludes
   them because vitest's default glob once picked up stale COMPILED
   `dist/**/*.test.js` and CI ran an old copy of a fixed test.
2. Hermetic by construction: mkdtemp fixtures, never the real `~`. run-all
   sandboxes HOME for the vitest lane, but a direct `npm test` does NOT.
   Save/restore any `process.env` you mutate
   (pattern: `mcp/src/brain-paths.test.ts:24-36`).
3. If the test guards a prose promise, write it as a source-scan (R7).
4. Must pass OFFLINE:
   `cd mcp && SECOND_BRAIN_DISABLE_EMBEDDINGS=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 npm test`
   — CI has no HuggingFace network and a model fetch hangs past the 5 s
   default test timeout.
5. Typecheck: `cd mcp && npx tsc --noEmit` (CI runs it on tests too; vitest
   alone transpiles per-file and never typechecks — a real tsc error once
   shipped through two green releases, 0.24.10).
6. If you touched any non-test `mcp/src` source: rebuild + commit bundles
   (`cd mcp && npm run bundle`) or the bundle-current gate fails, and the
   version-bump tripwire applies — both sb-change-control.
7. **Budget: none.** No surface-budget key counts `.test.ts` files. Do not
   bump the budget for a vitest-only addition.
8. Verify the full local CI parity block (above) — a Windows-only pass misses
   BSD/Linux failures and vice versa.

## When NOT to use this skill

- Release sequence, version-bump/tripwire policy, gate bypass rules, bundle
  staleness mechanics → **sb-change-control**.
- A live failure to triage (symptom → cause) → **sb-debugging-playbook**.
- Evidence beyond tests — measurements, benchmarks, ablations, "prove it,
  don't just install it" → **sb-proof-and-analysis-toolkit**.
- Full incident narratives behind the rules here → **sb-failure-archaeology**.
- Setting up node/npm/the dev environment at all → **sb-build-and-env**.

## Provenance and maintenance

Derived from the working tree at commit `6fba312` (release 0.33.30) plus the
uncommitted 0.33.31 batch, read 2026-07-05: `tests/run-all.sh`,
`tests/test-script-portability.sh`, `.github/workflows/ci.yml`,
`tests/test-normalize-path.sh`, `tests/test-symlink-guard.sh`,
`tests/test-run-all-skip-semantics.sh`, `tests/test-graph-cluster-shim.sh`,
`tests/test-dream-accept-guards.sh`, `tests/test-exec-bits.sh`,
`mcp/src/brain-paths.test.ts`, `mcp/src/agent-grants.test.ts`,
`mcp/vitest.config.ts`, `scripts/validate-plugin.sh` (budget section),
`.claude-plugin/surface-budget.json`, `Makefile`, `.githooks/pre-push`, `RELEASING.md`,
and archive/docs:CHANGELOG.md incident entries (0.24.30, 0.24.50, 0.30.2, 0.33.7, 0.33.9,
0.33.15, 0.33.31). Vitest case count is from a live offline run on
2026-07-05. Authored 2026-07-05 against version 0.33.31.

Facts that drift, and their one-line re-checks (repo root):

| Fact class | Re-verify |
|------------|-----------|
| Shell-test count + budget | `ls tests/test-*.sh \| wc -l && jq .tests .claude-plugin/surface-budget.json` |
| Vitest file/case counts | `find mcp/src -name '*.test.ts' \| wc -l`; `cd mcp && SECOND_BRAIN_DISABLE_EMBEDDINGS=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 npx vitest run 2>&1 \| grep -E '^\s*Tests'` |
| Golden retrieval fixture count + gate | `awk 'END{print NR}' tests/fixtures/eval-queries.jsonl` (12); `grep -n SB_EVAL_MIN_RECALL tests/test-knowledge-eval.sh` (default 1.0) |
| run-all env knobs / SKIP semantics | `sed -n '11,25p;84,99p' tests/run-all.sh` |
| CI steps + lanes | `grep -n 'name:\|run:' .github/workflows/ci.yml` |
| Portability guard list (currently 13, re-verified 2026-09-05 — drifts every release) | `grep -nE '^# [0-9]+\.' tests/test-script-portability.sh` |
| Budget counting rules + fail message | `sed -n '190,220p' scripts/validate-plugin.sh` |
| Vitest offline env vars | `sed -n '32,44p' .github/workflows/ci.yml` |
| Exec-bit enforcement | `sed -n '1,30p' tests/test-exec-bits.sh` |
