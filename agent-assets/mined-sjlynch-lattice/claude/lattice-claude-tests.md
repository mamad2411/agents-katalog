# backend/src/__tests__

Backend tests use Node's built-in `node:test` runner with `tsx` (`npm test`
from `backend/`, which collects `src/__tests__/*.test.ts` — one level only).
The `test` script `--import`s `helpers/isolateHome.mjs` first: it points
`HOME`/`USERPROFILE` at a throwaway temp dir so the suite never writes into the
real `~/.lattice` (task DBs, `projects.json`, snapshots), inside a per-process
`TEMP`/`TMP` root it removes at exit (so a test's leaked temp dirs go too —
still clean up your own). It must load before
any test imports the task cache, whose home path binds once at module load. It
also points `TERMINAL_PORT` at a closed port (unless set), so code under test
never reaches the developer's live executor on :5185, and sets
`LATTICE_TEST_HOME_ISOLATED`; a test that writes under `~/.lattice`
(`opengrepScan`, `opengrepInstall`) throws at import without that marker, so a
bare `node --test <file>` can't land fixtures in your real home. Run one file
(or every file of a module) from the repo root with
`npm run test:file -- <path or module name>` — it adds the preloads and the
compact reporter (`scripts/testReporter.mjs`: failures + one summary line).

## Conventions

- Import assertions from `node:assert/strict` and test APIs from `node:test`.
- Prefer focused pure-unit coverage; for filesystem tests use temp dirs from
  `helpers/tempDir.ts` and clean them in `t.after`/`finally`.
- Every file runs in one Node process against source: no global mutable state
  leaks, no real dev-server dependencies, no long-lived timers. Don't call code
  that patches the global console or registers process handlers (e.g.
  `installCrashLogging()`) — test the pieces it composes.
- Test route handlers by building the router/app in-process, never by starting
  the backend server.
- HOME is isolated, so `~/.gitconfig` is invisible: a temp repo that commits
  passes its identity with `-c user.name=… -c user.email=…` (or a local config
  on that temp repo).
- Keep tests as flat `.test.ts` files here; shared code goes in `helpers/`.
- Each file's header comment carries its regression story — read it before
  weakening an assertion.

## Finding a test

Tests are named after the module they cover (`crashLog.test.ts`), with dotted
suffixes for a sub-area (`worktree.merge.branchState.test.ts`,
`health.analyze.test.ts`) — grep the module name in this directory. A module
whose suite outgrew one file is split by scenario (`<module>.<area>.test.ts`,
each ≤ ~15 KB) with its shared harness in `helpers/<module>.ts` — reuse that
harness, never copy it into a new split file. Tests for
the dev runner scripts (`backend/scripts/dev/`, root `scripts/`) live here too,
importing them by relative path.

- `helpers/isolateHome.mjs` — the HOME-isolation preload above.
- `helpers/tempDir.ts` — `withTempDir` / `writeLayout` filesystem fixtures.
- `helpers/health.ts` — shared `HealthMetrics` fixtures for the split `health.*` suites.
- `helpers/hangAnalyzeFixture.mjs` — plain-JS analyzer the real health worker
  loads to hang on its own thread (worker-timeout tests).
- `fixtures/opengrep-scan.json` — recorded engine output for the Opengrep digest/scan tests.
- `opengrepTriageReview` — native/local/Settings dispositions, expiry and corrupt
  store protection; metadata-only review persistence, per-turn completion without
  cleanup/board writes, waiting conversation recovery, route scope validation
  and queued cancellation. All HOME writes and task fixtures are isolated;
  injected launch/cleanup seams never run a coding harness or live board action.
- `opengrepCache` — incremental replacement/reuse of findings and clean coverage,
  deletion/rename, rule/ignore/git-selection invalidation, mid-scan edits and
  cancellation. `opengrepRealCache` optionally runs a tiny authored rule against
  `LATTICE_TEST_OPENGREP_BINARY` in an isolated git project/HOME (Windows child
  profile override: `LATTICE_TEST_OPENGREP_USERPROFILE`); no downloads or live scans.

## Cross-cutting guards (hard to find by name)

- `opengrepNoVendoredAssets` — no Opengrep binary, signature or third-party rule file may be tracked (the MIT licence boundary).
- `projectGit`, `cleanupSafety`, `pruneReparsePoints` — `.git`-deletion defences: the git subcommand whitelist, worktree-path / reparse-point throw-guards.
- `repoIntegrity` — the merge-run circuit breaker (defence #6): fires on a vanished `.git` or non-forward HEAD, never on a fast-forward.
- `gitIdentityUntouched` — no shipped source writes the host's git identity; every commit-instructing brief keeps the per-commit `-c` recovery.
- `latticeApiDocsDrift` — the API doc templates and `routes/ROUTES.md` vs the live router; a new route fails until it has a ROUTES.md row and is documented for agents or added to `UNDOCUMENTED_ROUTES`.
- `latticeApiDocs` — the generated `LATTICE_API.md` index (read whole on every Lattice question) must stay under 5 KB, even for a long project path.
- `defaultPromptMigrations` — backend built-in step prompts must match the frontend `prompts/*.md` bytes.
- `regExpTemplateEscapes` — no ``new RegExp(`…`)`` template in `backend/src`/`frontend/src` may use a single-backslash escape (`\.` is lost to `.` in a template literal).
- `rawGitAllowlist` — only the listed modules launch `git` directly; all other project-repo git goes through `projectGit`.
- `terminalFingerprint` — every module in the executor's import graph is in `FINGERPRINT_FILES`, and the executor never imports `latticeApiDocs` / `memDiag/browser` (fingerprint churn).
- `sharedFolderBoundary` — everything reachable from `shared/` imports only relative paths (the frontend bundles it).
- `deadExports` — an export of `backend/src`/`frontend/src` that nothing references fails; delete it rather than allowlisting.
- `moduleLayout` — no `x/index.ts` facades (a domain's facade is the root `x.ts`).
- `importCycles` — no runtime import cycle in `backend/src` / `frontend/src` beyond its short known list (a cycle dies at boot with "Cannot access X before initialization" once top-level code reads a binding). Break new ones with a leaf module or `import()`.
- `docBudget` — auto-loaded `CLAUDE.md` budgets (root 9 KB, the package / components indexes 5 KB, every other 12 KB) and 20 KB for on-demand `MAP.md` / `docs/*.md`.
- `docPaths` — every backtick-quoted file path in a `CLAUDE.md`, `MAP.md` or `docs/*.md` exists (suffix match), or is a name the code writes at runtime. Move a file → fix the docs that name it.
