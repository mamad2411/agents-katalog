---
name: pipeline-cache-scan
description: "CI caches serving stale deps: keys, restore-keys, buildx scopes."
kind: skill
pack: devops
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: pipeline-cache-scan

## Premise

A cache is an optimisation: deleting it must never change what a build produces, only how long it takes. These keep CI green while they break that promise:
- `key: ${{ runner.os }}-node` over `node_modules`: keys are immutable, so the first save wins and every later lockfile change restores the old tree (`ci-platform-semantics.md` C6);
- `restore-keys` that bring back an install directory from another lockfile, then an install step guarded by `cache-hit` compared to anything but `'true'` (`cache-hit` is `'true'` only on an exact key match);
- one key for x64 and arm64 runners over a directory holding native addons; a key that ignores the Node or Python major;
- `cache-to: type=gha` with no `mode=` (`min`, the default) — measured on 2026-10-10 with buildx 0.37.1: after a change in the final stage, the builder stage **re-ran** (2.0 s) under `min` and was **CACHED** under `max`;
- several images on the default `scope` (`buildkit`), each overwriting the others' cache; the old `${{ runner.os }}-buildx-${{ github.sha }}` pattern, a new key every run that crowds out the dependency caches;
- `nx affected` or `turbo --filter=...[origin/main]` on the default `fetch-depth: 1`, where the base is missing and "affected" becomes everything or nothing.

`ci-graph.py --check=cache-keys` finds three GitHub shapes (`CACHE-KEY-NO-HASH`, `CACHE-NODE-MODULES`, `CACHE-PREFIX-SKIP-INSTALL`). This skill adds the lockfile, architecture and runtime joins, the other platforms, the Docker layer cache and the affected-detection join, and proves each finding with the cache probe.

It owns `ownership.json` row `ci-cache` (§1–§4). `@ci-reviewer` (this pack) judges its rows.

**Every finding cites `<file:line>` + the job and what the cache holds (a download cache or an installed tree) + the key and what it fails to vary on + the install guard after it + the oracle and its tier + the fix in the platform's own syntax.** A grep hit is a candidate, and a `ci-graph.py` row is a structural fact; neither is a finding. "Caching looks fine" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/devops.md`](../../../../snippets/precedents/devops.md) (pipeline § 7–16, tools § 41–46). Platform facts come from [`ci-platform-semantics.md`](../../../../snippets/ci-platform-semantics.md) (C6 caches, C1 concurrency); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § DevOps, V217–V219.

## The rule

A candidate is a finding when all four hold (the seven gates as `precedents/devops.md` § Reading the seven gates applies them to caches):

1. **The cache changes what the job runs** (gates 1, 5). It restores an **installed tree** (`node_modules`, `.venv`, `vendor/bundle`, `target/`, a build output) that a later step uses without reinstalling, or it decides which tests run (§3). A **download cache** (`~/.npm`, the pnpm store, `~/.cache/pip`, `~/.m2`, the Go module cache) is re-verified by a lockfile install, so a wrong key there costs time only: L, report-only.
2. **The event happens** (gate 2). A lockfile change, a runtime major bump, an arm64 leg, a PR that touches one package, a second image build in the same run.
3. **No control already covers it** (gate 4). The install runs on every non-exact hit (a `!= 'true'` guard, or no guard); the key hashes the lockfile and names the arch and runtime; `actions/setup-*` builds the key (setup-node: OS, arch, package manager and the lockfile hash; setup-python adds the Python version — action sources read 2026-10-10).
4. **The oracle fired, or both ends are cited** (gate 6). The cache probe (V217) on a sandbox repo, the affected probe (V218), or the graph row present before the fix and gone after it (T). Without a run, cite the key line and the step that consumes the restore; the row is `[report-flagged]`.

## Boundaries

- **Cache poisoning is security's, when the security pack is installed** — `ci-security-scan` §5 (CI-CACHE-POISON, CI-CACHE-RELEASE): a cache written by an outsider-startable workflow (`pull_request_target`, `workflow_run`, `issue_comment`) and restored by a publish or deploy job, and caches restored in tag or release workflows. Pre-flight R lists those lines and never posts them. Without the security pack they print `security-class (owner pack not installed)` at this skill's severity (precedents § 1). This skill owns **staleness and collision without an attacker**.
- **Job timeouts, masking, required checks** → `pipeline-integrity-scan` (this pack). It owns whether a red build reaches a merge; this skill owns whether a green build ran on the dependencies the lockfile names.
- **Layer order inside the Dockerfile** (`COPY . .` before the install) → `container-build-scan` §3. §2 here owns only how CI exports and imports the BuildKit cache.
- **Test retries and flaky quarantine** → testing `suite-execution-scan` §6, when that pack is installed.

## Adapt to the codebase — the platform lanes

Discover every CI file (pre-flight 0a); never assume `.github/`. Print the lanes you ran in the header.

| Lane | Cache primitive | Key semantics | Restore fallback | Source |
|---|---|---|---|---|
| **GitHub Actions** | `actions/cache` (v4+; the legacy service was shut down 2025), `setup-*` `cache:` | immutable; scope = own branch, default branch, PR base; PR caches on `refs/pull/N/merge`; 7-day idle eviction, 10 GB (C6) | `restore-keys` prefixes, newest match; `cache-hit` = `'true'` only on the exact key | C6 [V]; *Dependency caching reference* and actions/cache README, fetched 2026-10-10 (the README disagrees with itself on the non-exact value: compare to `'true'` only) |
| **GitLab CI** | `cache:` with `key:` / `key: files:` | protected and unprotected pipelines get separate caches (`-protected` / `-non_protected` suffix, a project setting); caching is best-effort | `fallback_keys` (up to 5), then `CACHE_FALLBACK_KEY` | GitLab Docs, *Caching in GitLab CI/CD*, fetched 2026-10-10 |
| **CircleCI** | `restore_cache` / `save_cache` | immutable, first write wins (a later save is silently discarded); `{{ checksum "f" }}`, `{{ arch }}`; `{{ epoch }}` is a new key every run; 15-day retention | each listed key is a prefix; the most recent match wins | CircleCI Docs, *Caching dependencies*, fetched 2026-10-10 |
| **Azure Pipelines** | `Cache@2` (`key: 'npm \| "$(Agent.OS)" \| package-lock.json'`) | file segments are hashed | `restoreKeys` | `[K]` |
| **Bitbucket** | `caches:` (predefined or custom `key: files:`) | predefined caches are not keyed on the lockfile `[K?]` | — | `[K?]` |
| **BuildKit (any CI)** | `cache-from` / `cache-to` (`type=gha`, `registry`, `local`, `inline`) | `mode=min` default exports final-stage layers only; `type=gha` `scope` defaults to `buildkit` and builds sharing a scope overwrite each other; `inline` supports `min` only; `type=gha` needs Buildx ≥ 0.21.0 / BuildKit ≥ 0.20.0 after the 2025-04-15 cache API change | — | Docker Docs, *Cache storage backends*, *GitHub Actions cache*, fetched 2026-10-10; min vs max measured |

A reusable workflow or composite action that builds the key is **one finding with N call sites** (precedents § 5).

## Tool lane and ledger

| Lane | Command | Trap that makes a clean result false |
|---|---|---|
| Graph | `python3 "$G" . --check=cache-keys` (`ci-graph.py`, repo baseline; PyYAML, else Ruby psych, else `uv run --with pyyaml`) | exit 2 (no YAML loader, a parse error) is NOT-RUN, never clean (precedents § 41); it reads `actions/cache` only, not `setup-*`, other platforms, or buildx |
| Settings (A) | `gh cache list --json key,ref,sizeInBytes,lastAccessedAt -L 100`; `gh api repos/{o}/{r}/actions/cache/usage` | 403/404 = `UNREADABLE`, never "no caches" (precedents § 6) |
| Timing (A) | `gh api repos/{o}/{r}/actions/runs?per_page=100`, `…/runs/{id}/jobs` | a token is required; without one §4 prints `UNREADABLE` |
| Cache probe (R) | a sandbox repo the user names: a lockfile bump PR, then `gh cache delete --all` and a re-run | `act` does not reproduce the cache service scopes (precedents § 45) |

## Pre-flight greps

Run as **one** script from the repo root; bash 3.2, bash 5 and zsh print identical output. Grep **N** feeds **§N**; 0 is the inventory and the graph; R lists the security-routed rows. Every `rg` names its path; an rg exit 2 is a failed grep, never zero hits; in every rg call the include globs come first and the exclusion array last, because ripgrep lets the later `-g` win. File-level checks use `rg -l` / `rg -q`, never `rg -L` (that is `--follow`). `--hidden` is required for `.github`, `.gitlab` and `.circleci`.

```bash
[ -n "${ZSH_VERSION:-}" ] && setopt shwordsplit nonomatch
X=(-g '!**/{node_modules,vendor,dist,build,out,target,.venv,venv,coverage,.next,.turbo,generated}/**'
   -g '!**/{test,tests,__tests__,spec,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,examples}/**' -g '!**/{docs,ai,.claude,.git}/**')
CI=(--sort path --hidden -g '.github/workflows/*.{yml,yaml}' -g '**/action.{yml,yaml}' -g '**/.gitlab-ci*.yml' -g '.gitlab/**/*.{yml,yaml}' -g '.circleci/*.{yml,yaml}'
    -g '**/bitbucket-pipelines.yml' -g '**/azure-pipelines*.yml' -g '**/Jenkinsfile*' "${X[@]}")
GH=(--sort path --hidden -g '.github/workflows/*.{yml,yaml}' -g '**/action.{yml,yaml}' "${X[@]}")
BLD=(--sort path --hidden -g '.github/workflows/*.{yml,yaml}' -g '**/.gitlab-ci*.yml' -g '.circleci/*.{yml,yaml}' -g '**/azure-pipelines*.yml' -g '**/Jenkinsfile*'
     -g '**/docker-bake.{hcl,json}' -g '**/Makefile' -g '*.sh' -g '*compose*.{yml,yaml}' "${X[@]}")
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*#')   # drops comment-only hit lines
SCAN="${SCAN:-$(mktemp -d "${TMPDIR:-/tmp}/pipeline-cache.XXXXXX")}"; echo "SCAN=$SCAN"
G=.claude/scripts/ci-graph.py; [ -f "$G" ] || G="$HOME/.claude/templates/repo-baseline/.claude/scripts/ci-graph.py"
echo '# 0a CI files by platform; lockfiles the keys must hash'
rg --files "${CI[@]}" . | tee "$SCAN/ci.txt"
rg --files --hidden -g '{package-lock.json,npm-shrinkwrap.json,pnpm-lock.yaml,yarn.lock,bun.lock,bun.lockb,poetry.lock,uv.lock,Pipfile.lock,requirements*.txt,Gemfile.lock,go.sum,Cargo.lock,composer.lock,gradle.lockfile,*.gradle*,pom.xml,packages.lock.json,mix.lock,pubspec.lock,Podfile.lock}' "${X[@]}" . | sort | head -20
echo '# 0b graph (GitHub Actions): CACHE-KEY-NO-HASH, CACHE-NODE-MODULES, CACHE-PREFIX-SKIP-INSTALL; exit 2 = NOT-RUN, never clean'
if rg -q '^\./\.github/workflows/' "$SCAN/ci.txt"; then python3 "$G" . --check=cache-keys; echo "ci-graph exit=$?"; else echo 'ci-graph: N/A (no GitHub workflow)'; fi
cat > "$SCAN/cache.awk" <<'AWK'
# §1 every actions/cache step: key, path, restore-keys, the install guard after it; LOCK = a lockfile in hashFiles(); ARCH = the key separates architectures
function out(c, m) { printf "%s:%d: %s %s\n", FILENAME, L, c, m }
function flush() { if (!L) return
  inst = (P ~ /node_modules|\.venv|(^|[ \/])venv|vendor\/bundle|(^|[ \/])target([ \/]|$)|\.gradle\/caches\/build|site-packages|\/build([ \/]|$)|dist([ \/]|$)/)
  if (K ~ /hashFiles\(/ && K !~ /lock|shrinkwrap|go\.sum|requirements[^*]*\.txt|\.gradle|pom\.xml|Pipfile|Gemfile|composer|pubspec|Podfile|mix|pre-commit|\.tool-versions|\.nvmrc/) out("KEY-NO-LOCK", "hashFiles() names no lockfile: " K)
  if (inst && K !~ /runner\.arch|\barch\b|ARCH/ && MIXED) out("KEY-NO-ARCH", "install dir " P " keyed without runner.arch in a workflow with mixed-arch runners")
  if (inst && K !~ /version|matrix\.(node|python|ruby|go|java)|steps\.[A-Za-z_-]+\.outputs/) out("KEY-NO-RUNTIME", "install dir " P ": the key does not change when the runtime major does (native addons, venv interpreter)")
  if (K ~ /github\.(sha|run_id|run_number)/) out("KEY-PER-RUN", "a new key every run: " K (R ? " (restore-keys " R ")" : ""))
  if (inst && R != "") out("PREFIX-RESTORE-INSTALL-DIR", "install dir " P " restored by prefix " R ": read the install guard")
  L = 0; K = P = R = ""; blk = "" }
FNR == 1 { flush(); MIXED = A = B = J = 0 }
/^jobs:/ { J = 1 }
J && /^  [A-Za-z0-9_.-]+:[ \t]*$/ { flush(); MIXED = A = B = 0 }
/runs-on:|^[ \t]*-?[ \t]*(os|runner|platform)[ \t]*:|^[ \t]*(os|runner)[ \t]*:[ \t]*\[/ { n = split(tolower($0), t, /[ ,\[\]"\x27]+/)
  for (i = 1; i <= n; i++) if (t[i] ~ /arm|aarch64|macos-1[4-9]|macos-latest|graviton/) A = 1; else if (t[i] ~ /ubuntu|windows|macos-13|x64|amd64/) B = 1
  if (A && B) MIXED = 1 }
/^[ \t]*-[ \t]/ { if (L) { match($0, /^[ \t]*/); if (RLENGTH <= D) flush() } }
/uses:[ \t]*actions\/cache(\/restore|\/save)?@/ { flush(); L = FNR; match($0, /^[ \t]*-?/); D = RLENGTH - 1; if ($0 !~ /^[ \t]*-/) { D = RLENGTH - 2 } next }
L && /^[ \t]*key:/ { K = $0; sub(/^[ \t]*key:[ \t]*/, "", K); blk = "" ; next }
L && /^[ \t]*path:/ { P = $0; sub(/^[ \t]*path:[ \t]*\|?[ \t]*/, "", P); blk = "path"; next }
L && /^[ \t]*restore-keys:/ { R = $0; sub(/^[ \t]*restore-keys:[ \t]*\|?[ \t]*/, "", R); blk = "rk"; next }
L && blk == "path" && /^[ \t]+[^ \t:]+[ \t]*$/ { x = $0; gsub(/^[ \t]+|[ \t]+$/, "", x); P = P " " x; next }
L && blk == "rk" && /^[ \t]+[^:]+$/ { x = $0; gsub(/^[ \t]+|[ \t]+$/, "", x); R = R " " x; next }
L && /^[ \t]*[a-z-]+:/ { blk = "" }
END { flush() }
AWK
echo '# 1a actions/cache steps (GitHub): lockfile in the key, arch on mixed runners, per-run keys, prefix restores of install dirs'
rg --files "${GH[@]}" . | while IFS= read -r f; do awk -f "$SCAN/cache.awk" "$f"; done
echo '# 1b install guards on cache-hit (only == / != '"'"'true'"'"' is exact-hit safe) and setup-* built-in caches (their keys hash the lockfile, OS and arch)'
rg -n --pcre2 "${GH[@]}" 'outputs\.cache-hit\b' . | rg -v --pcre2 "cache-hit\s*[!=]=\s*['\"]true['\"]" | "${NC[@]}"
rg -n --pcre2 "${GH[@]}" '(?<![\w-])(cache|package-manager-cache)\s*:\s*[\x27"]?(npm|pnpm|yarn|pip|pipenv|poetry|gradle|maven|sbt|true|false)\b' . | "${NC[@]}"
echo '# 1c other platforms: GitLab cache:key without files:, CircleCI keys without {{ checksum }}, Azure Cache@2, Bitbucket caches'
rg -n -A4 --pcre2 "${CI[@]}" -g '!.github/**' '^\s*cache:\s*$|^\s*-?\s*(restore_cache|save_cache)\s*:|^\s*-\s*task:\s*Cache@|^\s*caches:\s*$' . | rg --pcre2 '\bkey:|\bkeys:|^\S+-\d+-\s*-\s+\S|\bpaths?:|\bfiles:|\bpolicy:' \
  | awk '{ m = "" } /(key|keys):[ \t]*[^ \t]/ || /-[0-9]+-[ \t]+-[ \t]+[^ :]+[ \t]*$/ { if ($0 !~ /checksum|files|\$CI_JOB_NAME|\[[ \t]*\]/ && $0 !~ /paths?:/) m = "   <- NO-LOCKFILE-IN-KEY" } { print $0 m }'
echo '# 2 Docker layer cache: buildx cache-from/to, mode, scope, inline, local dirs; build steps per file (several images + no scope = one shared scope)'
rg -n --pcre2 "${BLD[@]}" '\bcache-(from|to)\s*[:=]|--cache-(from|to)\b|\bcache_(from|to)\s*:|\bmode=max\b|\bscope=|--no-cache(?![-\w])|\.buildx-cache\b' . | "${NC[@]}" > "$SCAN/bx.txt"
awk -F: '{ l = $0; sub(/^[^:]+:[0-9]+:/, "", l); m = ""
  if (l ~ /cache-to|cache_to/ && l ~ /type=(gha|registry|local|s3|azblob)/ && l !~ /mode=max/) m = m " MODE-MIN(default)"
  if (l ~ /type=gha/ && l !~ /scope=/) m = m " GHA-DEFAULT-SCOPE(buildkit)"
  if (l ~ /type=inline/ && l ~ /mode=max/) m = m " INLINE-MAX-IGNORED"
  if (l ~ /type=local/ && l ~ /cache-to/ && l ~ /\.buildx-cache([ ,"\x27]|$)/) m = m " LOCAL-SAME-DIR(grows)"
  print $0 (m != "" ? "   <-" m : "") }' "$SCAN/bx.txt"
rg -c --pcre2 "${BLD[@]}" 'docker/build-push-action@|\bdocker\s+(buildx\s+)?build\b|\bbake\b' . | awk -F: '$2 > 1 { print $1 ": " $2 " image builds (each needs its own scope=)" }'
echo '# 3 superseded runs (PR workflows with no concurrency) and affected detection x clone depth'
rg -l --pcre2 "${GH[@]}" '^\s{2}pull_request\s*:|^on:\s*\[?[^\n]*\bpull_request\b' . | while IFS= read -r f; do rg -q '^\s*concurrency\s*:' "$f" || echo "$f: PR workflow without concurrency"; done
rg -n --pcre2 "${CI[@]}" '\bnx\s+affected\b|nx-set-shas|\bturbo\b[^\n]*--filter=[^\n]*\[|--affected\b|\blerna\b[^\n]*--since\b|\bgit\s+diff\b[^\n]*\borigin/|tj-actions/changed-files|dorny/paths-filter' . | "${NC[@]}" > "$SCAN/aff.txt"
rg -N -o '^[^:]+' "$SCAN/aff.txt" | sort -u | while IFS= read -r f; do awk -v F="$f" '/^jobs:/ { J = 1 } J && /^  [A-Za-z0-9_.-]+:[ \t]*$/ { j = $1; sub(/:$/, "", j) }
  /fetch-depth:[ \t]*0([^0-9]|$)|GIT_DEPTH:[ \t]*["\x27]?0|git[ \t]+fetch.*(--unshallow|--depth|origin[ \t])/ { deep[j] = 1 }
  /nx[ \t]+affected|nx-set-shas|turbo.*--filter=.*\[|--affected|lerna.*--since|git[ \t]+diff.*origin\/|changed-files|paths-filter/ { n++; h[n] = FNR; hj[n] = j; ht[n] = $0 }
  END { for (i = 1; i <= n; i++) { t = ht[i]; sub(/^[ \t]+/, "", t); printf "%s:%d: job=%s deep-clone=%s :: %s\n", F, h[i], (hj[i] == "" ? "-" : hj[i]), (deep[hj[i]] ? "yes" : "NO (default fetch-depth 1)"), t } }' "$f"; done
echo '# 4 speed: static candidates (serial needs: chains with no hand-off; GitLab stage ladders with no needs:), then run timing (gh + a token)'
if rg -q '^\./\.github/workflows/' "$SCAN/ci.txt"; then python3 "$G" . --serial-chains; fi
rg '\.gitlab-ci[^/]*\.yml$|^\./\.gitlab/' "$SCAN/ci.txt" | while IFS= read -r f; do awk -v F="$f" 'function fl() { if (j != "" && !nd && !ev) nn[st == "" ? "test" : st] = 1; j = ""; st = ""; nd = ev = 0 }
  /^stages:/ { sl = FNR; s = $0; if (s ~ /\[/) { gsub(/^[^[]*\[|\].*$/, "", s); ns = split(s, o, /[ \t]*,[ \t]*/) } else il = 1; next }
  il && /^[ \t]+-[ \t]/ { x = $0; sub(/^[ \t]+-[ \t]+/, "", x); sub(/[ \t#].*/, "", x); o[++ns] = x; next }
  /^[^ \t#]/ { il = 0; fl(); if ($0 ~ /^[A-Za-z0-9_-][A-Za-z0-9_.-]*:[ \t]*$/ && $1 !~ /^(stages|variables|default|workflow|include|image|services|cache|before_script|after_script):$/) { j = $1 } }
  j != "" && /^  stage:/ { st = $2; gsub(/["\x27]/, "", st) }  j != "" && /^  needs:/ { nd = 1 }  j != "" && /^  environment:/ { ev = 1 }
  END { fl(); for (i = 1; i <= ns; i++) { gsub(/["\x27 ]/, "", o[i]); if (o[i] in nn) { c++; l = l (l == "" ? "" : ">") o[i] } }
    if (sl && c >= 3) printf "%s:%d: STAGE-LADDER stages=%d serial=%s (jobs with no needs: and no environment: wait for the whole previous stage)\n", F, sl, ns, l }' "$f"; done
if gh auth status >/dev/null 2>&1; then echo "4: gh api repos/{o}/{r}/actions/runs?per_page=100 (p50/p95 per workflow); …/runs/{id}/jobs (queue = started_at - created_at)"; else echo '4: UNREADABLE (gh not authenticated): gh api repos/{o}/{r}/actions/runs?per_page=100'; fi
echo '# R routed to security ci-security-scan §5 when installed: cache writers in outsider-startable workflows, cache restores in tag- or release-triggered workflows'
rg -l --pcre2 "${GH[@]}" '^\s{2}(pull_request_target|workflow_run|issue_comment)\s*:' . | while IFS= read -r f; do rg -n --pcre2 'actions/cache(/save)?@|(?<![\w-])cache\s*:\s*[\x27"]?(npm|pnpm|yarn|pip|pipenv|poetry|gradle|maven|sbt)\b|cache-to\s*:' "$f" | sed "s|^|$f:|"; done
rg -l --pcre2 "${GH[@]}" '^\s{4}tags\s*:|^\s{2}release\s*:|^on:\s*\[?[^\n]*\brelease\b' . | while IFS= read -r f; do rg -n --pcre2 'actions/cache(/restore)?@|(?<![\w-])cache\s*:\s*[\x27"]?(npm|pnpm|yarn|pip|pipenv|poetry|gradle|maven|sbt)\b|cache-from\s*:' "$f" | sed "s|^|$f:|"; done
```

How to read it:
- **0b** and **1a** overlap on purpose: the graph proves the structural fact (T) on GitHub; 1a adds `KEY-NO-LOCK`, `KEY-NO-ARCH` (job-level: the job's `runs-on` or matrix mixes an arm label with an x64 one), `KEY-NO-RUNTIME` and `KEY-PER-RUN`.
- **1b** lists every `cache-hit` guard that is not an exact `'true'` comparison, and every `setup-*` cache (keys built by the action: decoys unless a privileged workflow uses them, which is R).
- **1c** marks GitLab and CircleCI keys with no lockfile (`NO-LOCKFILE-IN-KEY`); read the paths beside them to tell an installed tree from a download cache.
- **3** prints, per hit, the job and whether **that job** fetches deep history (`fetch-depth: 0`, `GIT_DEPTH: 0`, an explicit `git fetch`).

Blind spots, worked around rather than trusted:
- **A composite action or reusable workflow** that wraps `actions/cache` hides its key from 1a: read `.github/actions/*/action.yml` (1a includes them) and the caller's inputs.
- **Keys built in a script** (`echo "key=…" >> "$GITHUB_OUTPUT"`) appear as `${{ steps.x.outputs.key }}`: read the step.
- **Arch from a variable** (`runs-on: ${{ matrix.runner }}` with the matrix elsewhere, a self-hosted label): `KEY-NO-ARCH` needs the labels; read the matrix and `runs-on` before clearing.

### Measured (2026-10-10)

| Tree | Result |
|---|---|
| Seeded sample: 4 GitHub workflows (a mixed-arch matrix, a buildx image job, a legacy buildx job, PR, release, `pull_request_target`), GitLab, CircleCI; copies under `tests/fixtures/` and `docs/`; 13 positives, 8 decoys, 2 routed | 0.9 s, 0 rg or awk errors, `ci-graph.py` exit 1 (5 rows, Ruby psych loader); bash 3.2 and zsh identical. **13/13 positives surface** in their §. The copies never appear. Decoys clear on read: the lockfile + `runner.arch` + `!= 'true'` cache (its `KEY-NO-RUNTIME` row is Hardening: the Node major is pinned in the job), the pre-commit tool cache keyed on its config, `setup-node` `cache: npm`, a scoped `mode=max` image, `fetch-depth: 0` + `nx-set-shas`, GitLab `key: files:`, CircleCI `{{ arch }}-{{ checksum }}` |
| `benchmarks/fixtures/*` (16) | 3 fixtures hold GitHub workflows, 0 errors. brittle-suite: 4 `setup-*` caches (decoys) + 1 PR workflow with no concurrency; quality-mix: 1 + 1; vuln-fullstack: the PR preview's `cache: npm` in an outsider-startable workflow (R: security's seed). 13 have no CI file → `N/A`. Mobile-defects lists its lockfiles only |
| Real NestJS + Fastify monorepo (one 488-line workflow, read-only, `git status` clean before and after) | 1 s. 0 findings. `ci-graph.py` exit 0; 5 `setup-node` `cache: pnpm` (decoys: the action's key hashes the lockfile and arch); 3 image builds each with its own `scope=` and `mode=max` (the GOOD shape); concurrency present; no affected detection. Two FP classes fixed before shipping: `--no-cache\b` matched `--no-cache-filter` (a targeted rebuild); the R lane read build-push-action's `tags:` input as a tag trigger (now `on: push: tags` at its indent only) |

## The 3,000-hit path

1. **Intersect** with `ci-graph.py --required --online --deploy-ancestors`: keep caches in a required job, a deploy or publish ancestor, or the publish job itself. Dismiss the rest with one read each.
2. **Group** by key family (one key template across N jobs is one finding), then by reusable workflow or composite action (precedents § 5).
3. **Rank:** installed trees feeding a build or publish first; affected detection on required tests next; download caches and speed last.
4. **Read the top 30 groups.**
5. **Run the bulk oracle once:** one lockfile-bump PR plus one deleted-cache re-run on a sandbox repo settles every §1 row of that workflow (V217); one one-package PR and one shared-lib PR settle §3 (V218).
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits — <continuing command>)`. Never mark it `checked`.

## Scans for

| § | Classes | Default severity |
|---|---|---|
| 1 | FS-2 cache key wrong or stale: no lockfile in the key, no arch on mixed runners, no runtime, prefix restore of an installed tree, an inexact `cache-hit` guard | M (H when the tree feeds a release build; L for a download cache) |
| 2 | FS-3 Docker layer cache: `mode=min`, a shared default scope, a per-run key, an in-place local cache, `inline` + `mode=max` | L/M |
| 3 | FS-4 superseded PR runs; affected detection on a shallow clone | M (H when an empty affected set skips a required test) |
| 4 | FS-5 slow structure (run timing p50/p95, queue time) | L, report-only |

### 1. Cache key wrong or stale (FS-2)

```
BAD:   path: node_modules  key: ${{ runner.os }}-node            (immutable: the first tree is restored forever)
       key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}  on [ubuntu-latest, ubuntu-24.04-arm]   (x64 and arm64 share it)
       restore-keys: ${{ runner.os }}-node-  ·  - if: steps.deps.outputs.cache-hit == 'false'  run: npm ci      (a full miss skips the install)
       GitLab  cache: { key: $CI_COMMIT_REF_SLUG, paths: [node_modules/] }  ·  CircleCI  restore_cache: { keys: [deps-v1] }
GOOD:  cache the download cache (setup-node cache: npm, ~/.npm keyed on the lockfile) and always run npm ci
       or: key: nm-${{ runner.os }}-${{ runner.arch }}-node${{ steps.node.outputs.node-version }}-${{ hashFiles('package-lock.json') }}, no restore-keys, install if cache-hit != 'true'
       GitLab  key: { files: [package-lock.json] }  ·  CircleCI  deps-v2-{{ arch }}-{{ checksum "package-lock.json" }}
```
**Read the code:**
- What does the path hold: an installed tree or a download cache (rule 1)?
- Does a later step reinstall on every non-exact hit, or use the tree as restored?
- Is it a tool cache keyed on the tool's own config (`~/.cache/pre-commit` on `.pre-commit-config.yaml`, a Playwright browser cache on the Playwright version)? That is correct keying, not a missing lockfile.
- Do the job's runners mix architectures? Does the tree hold native code (`*.node`, wheels, a venv's interpreter link)?

**Finding when** a lockfile change or a runner or runtime change can leave the job running on a tree the lockfile does not describe, while CI stays green. The cross-arch collision rests on the docs naming only path and compression in the cache version (no architecture, fetched 2026-10-10) `[K?]`: settle it with V217 on an arm leg before a fix relies on it. **Proof (V217):** on a sandbox repo, a PR that bumps one dependency in the lockfile misses the exact key and reinstalls (the job log shows the install), and with every cache deleted (`gh cache delete --all`) the build is still green. Graph codes: `CACHE-KEY-NO-HASH`, `CACHE-NODE-MODULES`, `CACHE-PREFIX-SKIP-INSTALL`.

### 2. Docker layer cache (FS-3)

```
BAD:   cache-from: type=gha  cache-to: type=gha                 (mode=min: builder stages re-run every time; scope=buildkit shared)
       a second build-push-action with cache-from: type=gha       (reads the first image's scope; writes overwrite each other)
       actions/cache path: /tmp/.buildx-cache key: ${{ runner.os }}-buildx-${{ github.sha }}  +  --cache-to type=local,dest=/tmp/.buildx-cache   (the old pattern: a key per commit, a directory that only grows)
GOOD:  cache-from: type=gha,scope=api  cache-to: type=gha,mode=max,scope=api   (one scope per image)
       type=registry,ref=<repo>:buildcache,mode=max for cross-repo or long-lived caches (the ref differs from the image's tag)
```
**Read the code:** How many images build in this repo, and does each carry its own `scope=`? Is the Dockerfile multi-stage (only then does `mode=max` change anything)? Is the buildx version ≥ 0.21.0 for `type=gha` (`docker/setup-buildx-action` `version:` or the runner's)? Does the release build read a cache only the default branch writes (a `pull_request` run writes to its merge ref, which default-branch runs never restore — C6)? A cache written by an outsider-startable workflow is security's (§ Boundaries).

**Finding when** the declared cache cannot serve the build (builder stages never exported, scopes evicting each other, a key per run). **Proof (V217, buildx variant):** two runs of the image job on a sandbox repo with no source change: the second shows `CACHED` on every builder-stage step (`--progress=plain`); locally, `docker buildx build --cache-to type=local,dest=<d>,mode=max` then `--cache-from type=local,src=<d>` after a final-stage change shows the builder RUN `CACHED` (with `mode=min` it re-ran: measured).

### 3. Superseded runs and affected detection (FS-4)

```
BAD:   on: pull_request with no concurrency                     (every push runs the full suite again beside the stale run)
       - uses: actions/checkout@<sha>                            (fetch-depth: 1)
       - run: npx nx affected -t test                           (base main not in the clone: everything, or an error)
       - run: npx turbo run test --filter='...[origin/main]'     (origin/main never fetched)
GOOD:  concurrency: { group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}, cancel-in-progress: true }   (PR CI only: precedents § 15)
       fetch-depth: 0 + nrwl/nx-set-shas · or git fetch --depth=<n> origin ${{ github.base_ref }} before turbo/changed-files
```
**Read the code:** Does the tool fail on a missing base (red, visible) or fall back silently, and to what: everything (slow) or nothing (a required test skipped)? Is the job required (`ci-graph.py --required --online`)? Concurrency belongs on PR CI only; on a deploy it is `deploy-safety-scan` §2's finding, and `cancel-in-progress` on PR CI is fine (precedents § 15).

**Finding when** a PR's affected set is computed without the base ref, or superseded PR runs keep running. **Proof (V218):** on a sandbox repo, a PR touching one package runs only that package's tasks, a PR touching a shared library runs its dependents, and the empty set never skips a required test.

### 4. Slow structure (FS-5)

Two static candidates print without a token: `SERIAL-CHAIN` (`ci-graph.py --serial-chains`: three or more GitHub jobs, each needing only its parent and taking nothing from it — no `download-artifact`, no `needs.<parent>.*` read — and none a deploy, publish, environment or status-function job) and `STAGE-LADDER` (a GitLab `stages:` list where jobs with no `needs:` and no `environment:` sit in three or more stages, so each waits for the whole previous stage).

**Read the code:** Does the child reuse anything the parent made: an image pushed by SHA, a cache the parent warmed, a gate the team wants ordered (a smoke after a scan)? Could the chain run in parallel behind one filter or aggregator job, or the ladder become a `needs:` DAG?

Run timing is data, not a grep. With a token: p50/p95 per workflow from `gh api repos/{o}/{r}/actions/runs?per_page=100` (`…/runs/{id}/timing`) and queue time per job (`started_at - created_at`). There is no default threshold: compare against a budget the project declares. Without a token the timing half is `UNREADABLE` and a static candidate stays `[report-flagged]`. **Proof (V219):** the measured numbers, labelled measured. L, report-only.

## Proof

The oracles are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § DevOps. **Scope: a sandbox repository the user names, `${TMPDIR}` and scratch builders (removed afterwards) — never the user's branches or their cache store; `gh cache delete` runs only on the sandbox.**

| § | Oracle | Tier | V |
|---|---|---|---|
| 1 | Cache probe: a lockfile bump misses the exact key and reinstalls; a deleted cache stays green; the graph row is gone after the fix | R + T | V217 |
| 2 | Cache probe, buildx variant: builder stages `CACHED` on the second run | R | V217 |
| 3 | Affected probe: one-package PR → only it; shared-lib PR → dependents | R | V218 |
| 4 | Run timing from `gh api`, labelled measured | A | V219 |

## Output

```
pipeline-cache-scan — lanes: github-actions (4 workflows; ci-graph.py Ruby psych), gitlab, circleci · security: installed

1. .github/workflows/ci.yml:16                                       [report-with-fix]   medium
   §1 FS-2 — job build (matrix ubuntu-latest + ubuntu-24.04-arm) caches node_modules under
   `${{ runner.os }}-node-<lock hash>` with `restore-keys`; the install runs only on `cache-hit == 'false'`.
   An arm64 leg restores the x64 tree; a full miss skips `npm ci`. Proof: V217 on the sandbox — lock bump → exact
   miss, install skipped, build red on the arm leg (fails before the fix). Fix: cache ~/.npm via setup-node and
   always run `npm ci`; or add runner.arch and the Node version to the key and guard on `!= 'true'`.

2. .github/workflows/ci.yml:76                                       [report-flagged]    low
   §2 FS-3 — api and web share the default gha scope; api exports mode=min. Unproven link: no sandbox run.
   Settling test: V217 buildx variant, builder RUN `CACHED` on the second run.

Verification: 22 candidates → 1 finding · 6 unconfirmed · 4 hardening · 0 pre-existing · 9 refuted (self-verified) · 2 routed

Class coverage:
  §1  cache keys               checked (graph 5 rows + 1a 7 + 1c 3 → 1 finding, 3 unconfirmed; pre-commit cache refuted)
  §2  docker layer cache       checked (5 lines → 2 unconfirmed; scoped mode=max image refuted)
  §3  superseded / affected    checked (2 PR workflows without concurrency → hardening; 3 shallow affected → 1 unconfirmed)
  §4  speed                    checked (1 SERIAL-CHAIN + 1 STAGE-LADDER → 2 unconfirmed); timing UNREADABLE (gh not authenticated)
  R   routed                   triage.yml:10 (pull_request_target cache), publish.yml:14 (tag workflow restores) → security ci-security-scan §5
```

`[report-with-fix]`: what the cache holds, the key's missing dimension, the consuming step and the oracle are in hand, and the fix is local to the job. `[report-flagged]`: one link is unproven — the arch collision `[K?]`, a key built in a script, a composite action not read, no sandbox run. The row names the link and the settling test.

The coverage block lists **all four** §s and the R lane on every run: `checked (k hits → m findings)` only when the lane ran on a present surface; `N/A (no CI file)` or `N/A (no image build)`; `blocked (<reason>)` when the graph exits 2 or a grep fails; `UNREADABLE (<api>)` for §4's timing half without a token (its static candidates still run); `Live, unreviewed (k groups / n hits)` for a partial review.

## False positives / precedents

The verifier reads [`precedents/devops.md`](../../../../snippets/precedents/devops.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- **§ 5** One finding per key template, reusable workflow or composite action. **§ 6** A settings read that returns 403/404 is `UNREADABLE`.
- **§ 15** `cancel-in-progress` on PR CI is the intended behaviour (§3 recommends it; on a deploy it is `deploy-safety-scan` §2's).
- **§ 24** Preview environments. **§ 41** `ci-graph.py` exit 2 is NOT-RUN. **§ 44** The `on:` remap. **§ 45** `act` does not model the cache service.

Read-step rules measured or read on 2026-10-10, applied with a `file:line`: a download cache under a lockfile-verified install is speed, not correctness; a tool cache keyed on its own config or version is correctly keyed; `setup-node`/`setup-python` keys already hash the lockfile and arch; a `pull_request` run cannot write a cache the default branch restores (C6); `--no-cache-filter <stage>` is a targeted rebuild, not "no cache".

Rationalizations to reject:
- "It's only a cache": not when the job uses the restored tree without reinstalling.
- "The key has `runner.os`": x64 and arm64 Linux share it.
- "We use `mode=max`": on which scope, shared with which other image?
- "Affected keeps CI fast": on a shallow clone it may be testing nothing.

## When to run

- On any diff touching a CI file, a composite action, a lockfile's location, a Dockerfile's stage layout (§2), or a monorepo task-runner config (`nx.json`, `turbo.json`).
- After `/add-ci` (its Phase 6), after `/devops-fix` on a cache row.
- On every whole-repo `/devops-audit`, reporting all four §s and the R lane.

## Halt conditions

- **Do not report a critical or high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it; it applies [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with `precedents/devops.md`. Under `/devops-audit` that is its verification phase; standalone, run the protocol as a second pass and tag those rows `self-verified`. List the rest as Unconfirmed, Hardening, Pre-existing or Refuted; never drop them.
- **Halt on a finding missing its anchors:** the line, the job, what the cache holds, the key's missing dimension, the consuming step, and the fix.
- **No `checked` on a lane whose tool failed:** `ci-graph.py` exit 2, an rg exit 2, an unread composite action are `blocked`.
- **Never delete, list-and-purge or seed caches on the user's repository.** The cache and affected probes run on a sandbox repo the user names; otherwise the row is Unconfirmed with the settling command written out.
- **No proposed fix may trade correctness for speed:** no `restore-keys` added to an installed tree, no skipped install on a prefix hit, no `cache-mode: write` for an untrusted workflow (security's), no shallower clone under an affected run.
- **Do not print "caching looks fine" without the coverage block.** **Do not re-derive a class another skill owns** (§ Boundaries); cross-link it.

## Related

- `/devops-audit` dispatches this skill on a CI-file signal beside `pipeline-integrity-scan` and folds its coverage block into the cache rows; `/devops-fix` closes them with V217–V219. `/add-ci` (Phase 6) runs it on the workflow it emitted.
- `@ci-reviewer` judges these rows in refute mode.
- `pipeline-integrity-scan`, `deploy-safety-scan` §2 and `container-build-scan` §3 (this pack) own the neighbouring classes; `ci-security-scan` §5 (security) owns poisoning, when that pack is installed; `suite-execution-scan` §6 (testing) owns retries.

## Sources

GitHub cache scope, immutability and eviction: `ci-platform-semantics.md` C6 (GitHub Docs, *Dependency caching reference*, 2026-10-10). `cache-hit`, `restore-keys` order and `enableCrossOsArchive`: actions/cache README; the `setup-node` and `setup-python` key templates: their `src/` cache modules; GitLab *Caching in GitLab CI/CD*; CircleCI *Caching dependencies*; Docker Docs *Cache storage backends*, *GitHub Actions cache* and *Cache management with GitHub Actions* — all fetched 2026-10-10. Measured on 2026-10-10: buildx 0.37.1 `mode=min` vs `mode=max` builder-stage reuse with the local backend (a scratch `docker-container` builder, removed afterwards), and `ci-graph.py --check=cache-keys` on the seeded sample. Classes from the devops research catalog's release and pipeline notes (FS-2–FS-5) and the batch-4 devops eval (DV-2). Paraphrased; no text reproduced beyond identifiers.
