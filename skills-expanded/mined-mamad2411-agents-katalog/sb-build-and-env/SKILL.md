---
name: sb-build-and-env
description: >-
  Recreates the second-brain plugin development environment from scratch and explains
  its build system. Load when: setting up a fresh clone (node/npm/jq/Git-Bash
  prerequisites); npm ci / tsc / esbuild / vitest problems; tests/test-bundle-current.sh
  reports a STALE bundle; deciding whether mcp/dist must be rebuilt for a src change;
  installing or debugging the optional vector-deps tier (bm25-only or text-only degraded
  search, install-vector-deps.sh exit codes); Windows Git-Bash environment weirdness —
  CRLF from jq, "C:/" vs "/c/" path forms, "Cannot connect to C:", ln -s copying instead
  of linking, WSL bash.exe hijacking spawns, directory junctions; a root .mcp.json
  breaking the MCP server; the macOS bash-3.2 portability floor. NOT for: operating or
  installing the shipped plugin (auth modes, drainer, upgrades, data geography) — use
  sb-run-and-operate; test-suite mechanics, CI lanes, add-a-test — use
  sb-validation-and-qa; release gating and versioning policy — use sb-change-control;
  triaging live runtime failures — use sb-debugging-playbook.
---

# sb-build-and-env — recreate the dev environment + the build system

Repo: the `second-brain` Claude Code plugin at the repo root (the former `cost-router`
sub-plugin was absorbed and removed in 0.35.x). All Node work lives under `mcp/` — there is **no root `package.json`**
and no git submodules. Facts below verified against the working tree, **as of 0.33.31
(2026-07-05; the 0.33.31 batch is uncommitted on top of HEAD `6fba312` = 0.33.30).**

Terms used here (defined once):

| Term | Meaning |
|---|---|
| BRAIN_DIR | `~/.second-brain` — private runtime state dir (env override `BRAIN_DIR`). Full data geography: sb-run-and-operate. |
| KNOWLEDGE_DIR | `~/knowledge` — wiki + graph dir (override `CLAUDE_PLUGIN_OPTION_KNOWLEDGE_DIR` / `KNOWLEDGE_DIR`). |
| bundle | a single-file esbuild output `mcp/dist/**/*.bundle.js`, **committed to git** |
| vector-deps tier | optional shared install of `@huggingface/transformers` + native deps that enables embedding search (§5) |
| SessionStart banner | plugin hook output at session start that surfaces degradations; details: sb-run-and-operate |

## 1. Prerequisites

| Tool | Floor | Why | Check |
|---|---|---|---|
| git | any recent | clone; exec-bit + LF handling matter (§3) | `git --version` |
| Node.js | **>= 22** (`mcp/package.json` engines; CI pins `'22'`; every bundle targets `node22`) | MCP server, all CLIs, esbuild | `node --version` |
| npm | ships with Node | `npm ci` against `mcp/package-lock.json` | `npm --version` |
| jq | hard dependency | used pervasively by hooks/scripts and by the shell tests (`README.md:239`: tests require `jq`, `mktemp`, `bash` — all bundled with Git Bash) | `jq --version` (1.8.1 observed on the Windows dev box) |
| bash | macOS stock **3.2** is the floor (§6 T6); Windows: **Git Bash from Git for Windows** | every hook and shell test is bash | `bash --version` |
| make | optional — **Git Bash does NOT ship it** (`command -v make` → empty on the Windows dev box, verified 2026-07-05) | only the `Makefile` conveniences (`make test`, `make hook-install`, `make release-check`); every target is a one-line wrapper with a direct-command equivalent (§2 step 6, §7) | `command -v make` |

Platform notes:
- **Windows**: dev happens under Git Bash (MINGW/MSYS). Native cmd/PowerShell is not
  supported for hooks/tests (`README.md:237`). Do NOT develop under WSL: repo paths use
  MSYS `/c/...` form, and the codebase specifically defends against WSL's
  `System32\bash.exe` being resolved instead of git-bash (§6 T4).
- **macOS**: optional `brew install coreutils` provides `gtimeout` for bounded
  extraction; without it extraction runs unbounded (`README.md:236`).

## 2. From-zero setup (all platforms; run from repo root, git-bash on Windows)

```bash
git clone https://github.com/Cain-Ish/claude-code-plugin
cd claude-code-plugin

# 1. Deps — lockfile-exact, same command CI uses (ci.yml "npm ci --prefix mcp").
#    Installs runtime deps INCLUDING @huggingface/transformers (~70MB native
#    onnxruntime-node/sharp pulled transitively) AND devDeps (esbuild, tsc, vitest).
npm ci --prefix mcp

# 2. Typecheck (vitest does NOT typecheck — see §4).
cd mcp && npx tsc --noEmit

# 3. Unit tests, offline mode (replicates CI: no HuggingFace network; a model fetch
#    HANGS past the 5s test timeout — ci.yml comment at the Vitest step).
SECOND_BRAIN_DISABLE_EMBEDDINGS=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 npm test
#    A plain `npm test` with network also works and additionally covers the
#    embedding/RRF path once the ~70MB model is cached.

# 4. Full build (typecheck + rebuild all 18 bundles into mcp/dist/).
npm run build
cd ..

# 5. Shell suite + bundle gate + manifest validator (prove the env can run the gates).
bash tests/run-all.sh            # shell tests + vitest lane; exit 0 == green
bash tests/test-bundle-current.sh
bash scripts/validate-plugin.sh

# 6. Wire the pre-push gate (once per clone).
make hook-install                # sets core.hooksPath=.githooks
#    No make (default Git Bash)? The target is just these two lines (Makefile):
git config core.hooksPath .githooks && chmod +x .githooks/pre-push
```

**Dev clone vs marketplace install — two different dependency models.** A dev clone
gets a full REAL `mcp/node_modules` from `npm ci` (dev tools included). A marketplace
install ships `mcp/dist/` but never `node_modules/`, and gets runtime deps via the
shared vector-deps link instead (§5) — that shared tree is `npm install --omit=dev`,
so it contains **no esbuild/tsc/vitest** and cannot build. If `mcp/node_modules` on
your machine is a link (`[ -L mcp/node_modules ] && readlink mcp/node_modules` →
`~/.second-brain/vector-deps/node_modules`), remove the LINK first with
`rm mcp/node_modules` before `npm ci` — on git-bash `rm -f` unlinks a junction without
deleting the shared target (verified in `bin/install-vector-deps.sh:82-84`).

## 3. Windows dev specifics

- **Line endings are locked to LF.** `.gitattributes` sets `* text=auto eol=lf` (plus
  explicit rules for `.sh/.json/.md/.js/.ts/.yml`) precisely because CRLF breaks bash
  shebangs and heredoc terminators (its own comment says so). Any `core.autocrlf`
  value is overridden for tracked text; the dev box observed uses `core.autocrlf=input`.
- **Exec bits are invisible on Windows** (`core.filemode=false`). New shell tests must
  be stored mode 100755 via `git update-index --chmod=+x tests/test-<x>.sh`;
  `tests/test-exec-bits.sh` enforces it. Mechanics: sb-validation-and-qa.
- **There is NO Windows CI lane.** `.github/workflows/ci.yml` has exactly two jobs,
  `linux` and `macos` (the macos job exists for bash 3.2 + BSD coreutils). Windows
  coverage exists only as PATH-stub tests that emulate Windows on Linux CI, plus YOUR
  local run. Consequence (non-negotiable): on the Windows dev box, run the full
  `bash tests/run-all.sh` locally before every push — the pre-push hook does this for
  you once `make hook-install` is run. Project direction: also cross-check bash
  changes against BSD/macOS semantics before push; a Windows-only green run is not
  evidence for the CI lanes (see sb-validation-and-qa for the CI matrix, and §6 T6).

## 4. The build system: 18 committed esbuild bundles

npm scripts (`mcp/package.json`):

| Command (from `mcp/`) | Does |
|---|---|
| `npm run typecheck` | `tsc --noEmit` |
| `npm run bundle` | 18 chained esbuild invocations (below) |
| `npm run build` | `tsc --noEmit && npm run bundle` |
| `npm test` | `vitest run` |
| `npm start` | `node dist/server.bundle.js` |

The `bundle` script is one ` && `-chained line of **18** esbuild invocations, each
`--bundle --platform=node --target=node22 --format=esm
--external:@huggingface/transformers`, producing 18 committed bundles:
`mcp/dist/server.bundle.js` (this one also gets a `createRequire` banner) +
15 `mcp/dist/tools/*.bundle.js` + 2 `mcp/dist/cli/*.bundle.js`.

Why it is shaped this way:
- **`dist/` is committed** so a marketplace install works with no build step
  (`README.md:204`); the MCP manifest launches
  `node ${CLAUDE_PLUGIN_ROOT}/mcp/dist/server.bundle.js` (`.claude-plugin/mcp.json`).
- **transformers is `--external`** because its native binaries (onnxruntime-node,
  sharp) cannot be statically bundled — hence the vector-deps tier (§5) for installs
  that have no `node_modules`.
- Policy behind it (project direction): pure-JS by default, no node-gyp/native deps in
  the required tier; native code only in the opt-in vector-deps tier.

**THE RULE: any `mcp/src` change requires `cd mcp && npm run build` and committing the
changed `mcp/dist/**` in the SAME commit.** Enforced by `tests/test-bundle-current.sh`:
it parses `scripts.bundle` into its ` && `-separated entries, re-runs each with the
outfile redirected to a temp dir, and **byte-compares** (`cmp -s`) against the
committed bundle — failing with "`mcp/dist/<x> is STALE`". It SKIPs (exit 0) when node
or `mcp/node_modules/.bin/esbuild` is absent — so on a fresh clone run `npm ci` first,
or the gate silently self-skips. Origin incident: 0.24.7/0.24.8 shipped a stale bundle
twice ("src reviewed, dist shipped stale" — the test's own header).

Corollaries:
- **Never hand-edit a `dist/` bundle.** The gate byte-compares against a rebuild of
  committed src, so a hand-edit both fails the gate and routes around review.
- **vitest is not a typecheck** — it transpiles per-file. A real `tsc` error shipped
  in two releases through a green suite (0.24.7 `EDGE_TYPES` cast) before
  `tests/test-mcp-typecheck.sh` made `tsc --noEmit` its own gate.
- Touching `mcp/src`/`mcp/dist`/`mcp/package.json` also trips the release version-bump
  tripwire — versioning policy: sb-change-control.
- **Adding a bundle**: append another esbuild invocation to `scripts.bundle` (keep the
  ` && ` separator — test-bundle-current splits on exactly that), run
  `npm run build`, commit the new `dist/` file. Adding a whole new MCP TOOL (module
  conventions, registration, ship set): sb-architecture-contract
  references/extending-the-plugin.md Recipe B.

Re-verify the count: `jq -r '.scripts.bundle' mcp/package.json | sed 's/ && /\n/g' |
grep -c '^esbuild'` → 18, and `find mcp/dist -name '*.bundle.js' | wc -l` → 18.

## 5. The optional vector-deps tier (`bin/install-vector-deps.sh`)

Purpose: install `@huggingface/transformers` + native deps ONCE into a **shared,
version-independent** dir — default `~/.second-brain/vector-deps` (override
`SB_VECTOR_DEPS_DIR`) — and link each plugin version's `mcp/node_modules` at it.
Per-version installs used to cost 519MB each, re-downloaded on every bump
(script header). Dev clones normally don't need this — `npm ci` already installs
transformers for real (§2).

```bash
bash "$CLAUDE_PLUGIN_ROOT/bin/install-vector-deps.sh"                # full install (~70MB download, one-time)
bash "$CLAUDE_PLUGIN_ROOT/bin/install-vector-deps.sh" --relink-only  # no-network heal; exit 3 = needs a real rebuild
```

Mechanics that matter when debugging it (all evidence: the script itself):

- **deps-key**: sha256 of the `dependencies` block of `mcp/package.json`, stored at
  `$SHARED/.deps-key` — the shared tree rebuilds only when the dep SET changes, not on
  version bumps (`sha256sum || shasum -a 256` dual-path).
- **Validators**: `deps_ok` (every dependency's own package.json present in the tree)
  and `import_ok` (`node --input-type=module -e 'await import("@huggingface/transformers")'`).
- **Staging + atomic swap**: builds in a private `mktemp -d "$SHARED/.staging.XXXXXX"`,
  validates (`deps_ok` AND `import_ok`) BEFORE touching the live tree or link; keeps
  the old tree as `node_modules.old` until the swap lands. A failed/offline npm can
  never destroy a working install. Orphaned `.staging.*` dirs (SIGKILL/power loss) are
  swept at start — they are ~500MB each.
- **Harvest path**: an existing REAL `mcp/node_modules` satisfying current deps is
  `mv`'d into staging instead of downloading.
- **Link = junction on Windows**: on MINGW/MSYS/CYGWIN the link is a Windows directory
  junction created via `node fs.symlinkSync(target, link, "junction")` (no admin
  privilege needed); plain `ln -s` on POSIX. NEVER `ln -s` on MSYS — see §6 T3.
- **`--relink-only` is a consent boundary**: it succeeds ONLY via the no-network path
  (shared tree present + key-current + `deps_ok` + `import_ok` → relink); anything
  needing staging/npm exits **3** untouched. SessionStart auto-heal relies on this
  NEVER downloading. Mutation-free on every failure path.
- **Key stamped only after the LINKED tree genuinely imports** — a broken tree is
  never trusted on the next run.

Exit codes: `0` ok · `1` bad `CLAUDE_PLUGIN_ROOT` / missing package.json / no sha256
tool · `2` npm not on PATH · `3` staged build invalid OR relink-only refusal ·
`4` import still failing after install+link.

**What degrades without it**: `knowledge_search` falls back to BM25-only,
`episodic_search` to text-only — no error, just empty embeddings; the SessionStart
banner flags it and MCP results carry `degraded:'bm25-only'` / `'text-only'`
(`README.md:206-212`). After a successful install, rebuild the episodic index:
`rm ~/.second-brain/episodic-index.json && node "$CLAUDE_PLUGIN_ROOT/mcp/dist/tools/episodic-index-cli.bundle.js"`
(printed by the installer). Smoke test (also step 1 of `make release-check`):
`cd mcp && node --input-type=module -e 'await import("@huggingface/transformers"); console.log("ok")'`.

## 6. Environment trap catalog (tell → fix)

Each trap: the symptom you will actually see, the fix, the guard that locks it, and
the incident version (full chronicle: sb-failure-archaeology).

| # | Trap | One-line tell |
|---|---|---|
| T1 | jq emits CRLF on Windows | `\r` contaminates every `$(jq -r …)`; "last record works, earlier ones don't" |
| T2 | Path forms `C:\` / `C:/` / `/c/` | guards fail-open; tar/rsync say "Cannot connect to C:" |
| T3 | `ln -s` deep-copies on MSYS | GBs of duplicated node_modules; "link" is a real dir |
| T4 | WSL bash shadows git-bash | Node-spawned bash fails "No such file" on `/c/...` paths |
| T5 | root `.mcp.json` / `${VAR:-default}` | MCP server dead outside the plugin dir |
| T6 | macOS bash 3.2 floor | script parses on Linux, load-time syntax error on macOS |
| T7 | Node `HOME` unset on Windows | stray `.second-brain/` dirs appear in unrelated repos |
| T8 | CRLF-tainted env path vars | misleading "No such file" on paths that clearly exist |

**T1 — jq CRLF text-mode stdout (Windows).** jq 1.8.1 on Windows emits CRLF even on
`-r` output over clean LF input, so captures, pipes-to-grep, comparisons, arithmetic,
and built paths silently break; jq also pretty-prints JSONL without `-c`, shredding
line-oriented registries (projects.jsonl went blind this way). Fix: `| tr -d '\r'`
after every `jq -r` capture; always `jq -c` when writing JSONL. Guard:
`tests/test-jq-crlf-windows.sh` (Windows-jq stub on Linux CI). Incidents: 0.30.1
(systemic), 0.33.31 (`jq -c` registry fix).

**T2 — path-form mismatch at the Windows↔POSIX boundary.** Hook payloads and
`realpath` output arrive as `C:\…`/`C:/…` while `$HOME`-derived prefixes are `/c/…`;
prefix compares then never match — this silently fail-OPENED all three PreToolUse
guards on Windows for months (G-HOOK-2 re-arm). Separately, GNU tar/rsync parse a
leading `C:` as a REMOTE `host:path` ("Cannot connect to C:"). Fix: normalize ONCE at
the boundary, never per-consumer — `sb_normalize_path()` in `scripts/lib.sh:29`
(backslash→`/`, `//?/` prefix strip, localhost-UNC rewrite, `cygpath -u` drive form;
idempotent) for guard comparisons (normalize realpath's OUTPUT too), and the lib.sh
source-time block (`scripts/lib.sh:5-12`) that `cygpath -u`-normalizes an inherited
`BRAIN_DIR`. Guards: `tests/test-normalize-path.sh`, `tests/test-symlink-guard.sh`
(stubbed cygpath/realpath reproduce Windows on Linux CI). Incidents: 0.33.10, 0.33.12,
0.33.31.

**T3 — `ln -s` silently DEEP-COPIES on git-bash/MSYS** (winsymlinks default): each
"link" was a full ~490MB copy of the vector deps per plugin version (3.1GB cache
observed). Fix: Windows directory junction via
`node fs.symlinkSync(target, link, "junction")` (`_link_dir` in
`bin/install-vector-deps.sh:85-96`); git-bash `test -L`/`readlink`/`rm -f` all treat
the junction like a link. Beware the sibling test trap: capability-gated tests that
probe `ln -s` silently SKIP on exactly the platform with the bug. Incident: 0.33.7.

**T4 — WSL bash shadow.** With WSL installed, a Node `exec("bash")` resolves
`System32\bash.exe` (WSL) via Machine-PATH before git-bash; WSL mounts drives at
`/mnt/c`, so MSYS `/c/...` script paths don't exist → "No such file or directory" from
spawns that work fine in your own terminal. Fix: probe Git-for-Windows bash explicitly
— `resolveBashExe()` in `mcp/src/tools/dream.ts:57-68` (candidates:
`Program Files\Git\bin\bash.exe`, x86 variant, `LOCALAPPDATA\Programs\Git`), and
`win_bash()` in `scripts/install-extract-timer.sh`. Incident: 0.33.1.

**T5 — MCP manifest placement is load-bearing.** Two sub-traps, both validator-FAILed
by `scripts/validate-plugin.sh:244-265`: (a) a repo-root `.mcp.json` is read a SECOND
time as a project-scoped MCP config when the repo is opened as a project, where
`${CLAUDE_PLUGIN_ROOT}` is unset → dead server. There is deliberately NO root
`.mcp.json` in this repo; never add one — the manifest lives ONLY at
`.claude-plugin/mcp.json`, wired via `plugin.json` `"mcpServers"`. (b) the bundle path
must be anchored by the bare `${CLAUDE_PLUGIN_ROOT}/` token — Claude Code does NOT
substitute the shell `${VAR:-default}` form, which collapsed the path to cwd-relative
and broke the server for every installed user (0.24.5 → fixed 0.24.35).

**T6 — bash 3.2 floor (macOS stock `/bin/bash`).** Banned in `scripts/`:
`mapfile`/`readarray`, `declare -A`/`local -A`,
`${x^^}`/`${x,,}`, `grep -P`, and — the nastiest — a `case` statement inside `$(...)`
command substitution, which is a LOAD-time parse error on 3.2 that `bash -n` on any
modern host cannot reproduce (broke every macOS `dream_accept`, 0.24.33). GNU
`stat -c` / `date -d` / `find -printf` need BSD fallbacks; GNU regex escapes
(`\b \w \s \d \xNN`) silently match NOTHING on BSD sed/grep. All statically enforced
by `tests/test-script-portability.sh` (11 checks); CI's macos job runs the real
`/bin/bash` 3.2. Full check list + test mechanics: sb-validation-and-qa.

**T7 — Node `HOME` unset on native Windows** (Windows uses `USERPROFILE`):
`process.env.HOME ?? ''` fallbacks collapse to CWD-relative paths and littered stray
`.second-brain/` dirs across unrelated repos (~16 call sites). Fix: ALL brain/knowledge
path resolution funnels through `mcp/src/brain-paths.ts` (`os.homedir()`); a
source-scan test bans `process.env.HOME` and `'.second-brain'` string literals
anywhere else in `mcp/src` (`mcp/src/brain-paths.test.ts`). Never re-implement the
resolver. Incident: 0.33.17. Architecture rationale: sb-architecture-contract.

**T8 — CRLF-tainted env vars.** A trailing `\r` on `CLAUDE_PLUGIN_ROOT` / `HOME` /
`BRAIN_DIR` / `KNOWLEDGE_DIR` makes `bash <path>` and `fs.stat` fail with a misleading
"No such file" on a path that looks perfect when printed. Fix: `cleanEnvPath` at every
env-path read on the TS side (`mcp/src/path-guard.ts`, applied in `server.ts`);
`tr -d '\r'` on the bash side. Incident: 0.30.0/0.30.1.

## 7. Pre-push gate + local dev loop

- `make hook-install` (once per clone) sets `core.hooksPath=.githooks`;
  `.githooks/pre-push` then runs `tests/run-all.sh` on every push and blocks on any
  failure. Bypass exists for recovery only (`SB_SKIP_PREPUSH=1 git push` or
  `git push --no-verify`) — the hook's own header: always follow up with a real fix.
  On Windows this local gate IS the release gate for Windows behavior (§3, no CI lane).
- `make test` = full suite; `make test-quiet` = verdicts only; `make release-check` =
  vector-deps import smoke + full suite (Makefile). Release gate policy and the full
  local gate sequence: sb-change-control.
- **Live-editing loop**: `claude --plugin-dir /path/to/claude-code-plugin`, then
  `/reload-plugins` inside the session after editing skills/agents/hooks (the bundled
  MCP server may still need a fresh session). **Never `--plugin-url`** for this loop —
  download-and-execute fails the supply-chain posture (`RELEASING.md:102-115`). The
  repo's `.claude/settings.json` also registers itself as a local plugin
  (`"second-brain@local": {"source":"local","path":"."}`), so opening the repo in
  Claude Code loads the working tree as the plugin.
- `${CLAUDE_PLUGIN_ROOT}` is **ephemeral** (replaced on every plugin update) — never
  write runtime state into the plugin root; durable state lives under `~/.second-brain`
  and `~/knowledge` (`RELEASING.md:117-133`). Invariant details: sb-architecture-contract.

## Provenance and maintenance

Derived entirely from repo evidence read/run on 2026-07-05 against the working tree at
0.33.31 (uncommitted batch on HEAD `6fba312` = 0.33.30): `mcp/package.json`,
`tests/test-bundle-current.sh`, `tests/test-mcp-typecheck.sh`,
`tests/test-script-portability.sh`, `bin/install-vector-deps.sh`, `scripts/lib.sh:1-51`,
`scripts/validate-plugin.sh:244-273`, `mcp/src/brain-paths.ts`,
`mcp/src/tools/dream.ts:57-68`, `.github/workflows/ci.yml`, `Makefile`,
`.githooks/pre-push`, `.gitattributes`, `.claude/settings.json`, `README.md:204-239`,
`RELEASING.md:102-133`, CHANGELOG version headings for the incident stamps. Items
marked "project direction" come from maintainer-accepted context, not a repo file.

Re-verify volatile facts (run from repo root):

| Fact | One-liner |
|---|---|
| Node engine floor | `jq -r .engines.node mcp/package.json` → `>=22` |
| Bundle count (18) | `jq -r '.scripts.bundle' mcp/package.json \| sed 's/ && /\n/g' \| grep -c '^esbuild'` |
| Committed bundles (18) | `find mcp/dist -name '*.bundle.js' \| wc -l` |
| esbuild flags (external/target) | `jq -r '.scripts.bundle' mcp/package.json \| grep -o -- '--external:[^ ]*' \| sort -u` |
| CI jobs (linux+macos, no Windows) | `sed -n '/^jobs:/,$p' .github/workflows/ci.yml \| grep -E '^  [a-z]+:$'` (unanchored grep also catches the `push:` trigger key) |
| No root .mcp.json | `ls .mcp.json` → must NOT exist (validator FAILs if it does) |
| vector-deps shared dir + exit codes | `grep -n 'SB_VECTOR_DEPS_DIR\|exit [1-4]' bin/install-vector-deps.sh` |
| Junction (not ln -s) on MSYS | `grep -n 'junction' bin/install-vector-deps.sh` |
| sb_normalize_path funnel exists | `grep -n 'sb_normalize_path()' scripts/lib.sh` |
| Offline vitest env names | `grep -n 'OFFLINE\|DISABLE_EMBEDDINGS' .github/workflows/ci.yml` |
| LF enforcement | `head -5 .gitattributes` |
| Pre-push runs run-all | `grep -n 'run-all.sh' .githooks/pre-push` |
