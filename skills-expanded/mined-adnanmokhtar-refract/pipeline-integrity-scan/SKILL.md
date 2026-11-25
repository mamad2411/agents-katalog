---
name: pipeline-integrity-scan
description: "CI lets a red build merge or deploy: masked gates, lost exits, skip-satisfied checks, ungated deploys."
kind: skill
pack: devops
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: pipeline-integrity-scan

## Premise

A pipeline is a promise that a red build stops. The promise breaks silently, and CI stays green while it does:
- a scan step with `exit-code: 0`;
- a smoke test under `continue-on-error: true`;
- `trivy … | tee scan.txt` under a shell with no pipefail;
- a required check that a path filter leaves Pending, or a job `if:` turns into a "success";
- a prod deploy with `if: always()`;
- a free-text dispatch `ref` that ships an unreviewed branch.

No tool in the ledger catches these. Measured on the research fixture, actionlint 1.7.12 caught only a misspelt `needs:`, and zizmor 1.30.1 (`--persona=auditor`) caught none of the masking classes. These are joins across files, settings and platform semantics, not lint rules.

This skill finds those defects on **six platforms**: GitHub Actions, GitLab CI, CircleCI, Bitbucket Pipelines, Azure Pipelines and Jenkins. It decides structural facts with `ci-graph.py`, and proves each finding with the seeded-failure, shell-probe, required-check or settings-read oracle at its tier. It owns `ownership.json` row `ci-pipeline-integrity` (§1–§8). `@ci-reviewer` (this pack) judges its rows.

**Every finding cites the line `<file:line>` + the gate it neutralises (which job, which command) + why that gate matters (required, or an ancestor of a deploy or publish job) + the platform row it rests on + the oracle and its tier + the fix in the project's own CI syntax.** A grep hit is a candidate, and a `ci-graph.py` row is a structural fact about the files; neither is a finding. "CI looks fine" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/devops.md`](../../../../snippets/precedents/devops.md). Platform facts come from [`ci-platform-semantics.md`](../../../../snippets/ci-platform-semantics.md); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § DevOps, V209–V216.

## The rule

A candidate is a finding when all four hold. They are the protocol's gates as `precedents/devops.md` § Reading the seven gates applies them to pipelines.

1. **The gate matters.** The job is in the required set (`ci-graph.py --required --online`, or `--contexts=` from a rules snapshot), or it is an ancestor of a deploy or publish job (`--deploy-ancestors`), or it is that deploy or publish job. Unknown required-ness (no token) is `UNREADABLE`: the row stays `[report-flagged]` and is never cleared (precedents § 7).
2. **The platform does what the candidate claims.** The verdict names its row in `ci-platform-semantics.md`. Examples: S1 for a GitHub pipe, R1/R2 for a skip, R8 for GitLab `when: manual`. A `[K?]` row (S3, S6, R7) keeps the finding Unconfirmed until its sandbox run (V210 probe, V209 seed).
3. **No control already catches it.** These all count as controls:
   - an aggregator that fails on `needs.*.result` (precedents § 8, § 10);
   - a later step that re-checks `PIPESTATUS`;
   - CircleCI's `-eo pipefail` default;
   - an environment rule or ruleset;
   - the same gate enforced in another required job.
4. **The oracle fired, or both ends are cited.** The seeded failure turns the gate red and the run stays green (V209, V212). Or the shell probe exits 0 (V210). Or the graph row is present before the fix and gone after it (T). Without a run, cite both ends: the masking line, and the required context or deploy job it feeds. The row is then `[report-flagged]`.

## Boundaries

- **Attacker-path classes are security's.** That covers expression injection, privileged triggers with untrusted code, pins × privilege, cache poisoning, OIDC width and secret exposure. They go to `ci-security-scan` when the security pack is installed (until that skill ships, `iac-scan` § 5, *CI workflows*). Without it, § Security fallback lane runs here, tagged (`precedents/devops.md` § 1).
- **Masking on a test job, zero tests, test retries** → testing `suite-execution-scan` §4/§6, when that pack is installed. **A masked lint step** → code-quality `suppression-scan` §3. **The a11y gate** → frontend `a11y-scan` §7. Each owner reads `ci-graph.py --required --online` from here for severity (precedents § 2). Without the owner pack, the row prints `<class> (owner pack <x> not installed)` at this skill's severity.
- **The observability rules gate** (promtool/pint) → observability `alert-rule-lint` owns its content. The CI-level mask on that job is §1 here.
- **Deploy concurrency, environment protection, rollout gating, migration topology** → `deploy-safety-scan` (this pack). **Cache keys and affected detection** → `pipeline-cache-scan`. **Rebuild-after-scan, release refs, retention** → `release-integrity-scan`. This skill owns whether a red build can **reach** a merge or a deploy, not how the deploy behaves.

## Adapt to the codebase — the platform lanes

Discover every CI file (pre-flight 0a); never assume `.github/`. Print the lanes you ran in the header. Facts tagged `[V]` were verified on the date in `ci-platform-semantics.md`; `[K?]` rows are settled by their oracle before a fix relies on them.

| Lane | Files | Shell and exit (row) | Skip / failure tolerance (row) | Graph | Tool |
|---|---|---|---|---|---|
| **GitHub Actions** | `.github/workflows/*`, `action.yml`, reusable `workflow_call` | `run:` = `bash -e` **no pipefail**; `shell: bash` adds it (S1, S2; precedents § 43) | `if:` skip = success (R1); needs-skip not a failure (R2); path filter = Pending (R3); `merge_group` (R5) | `ci-graph.py` | actionlint 1.7.12 |
| **GitLab CI** | `.gitlab-ci.yml`, local `include:`, `extends:` | bash executor `set -eo pipefail` (S3 `[K?]`) | `when: manual` ⇒ `allow_failure: true` (R8); `retry:when` default `always` (R9); `rules:changes` true on non-push pipelines (R10); `needs:optional` (R11) | not modelled: grep + read | `glab ci lint --dry-run` `[K?]` |
| **CircleCI** | `.circleci/config.yml` (+ `setup: true` continuation) | `/bin/bash -eo pipefail` (S4) | a workflow job with no `requires:` starts at once | not modelled | `circleci config process` (expands orbs) |
| **Bitbucket** | `bitbucket-pipelines.yml` | `set -e`, **no pipefail** (S5) | `after-script` never fails the step | not modelled | — |
| **Azure Pipelines** | `azure-pipelines*.yml`, templates | multi-line `script:` = **last command wins** (S6 `[K?]`) | `continueOnError`, `condition: always()`, `dependsOn: []` | not modelled | REST preview run `[K]` |
| **Jenkins** | `Jenkinsfile*`, `vars/*.groovy` | `sh` = `sh -xe`, no pipefail (S7) | `catchError(buildResult: 'SUCCESS')`, unchecked `returnStatus: true`, `propagate: false`, `post { always }` | not modelled | `declarative-linter` (needs a controller) |

A GitLab template, `extends:` base, reusable workflow or composite action is **one finding with N call sites** (precedents § 5).

## Tool lane and ledger

`ci-graph.py` ships in the repo baseline (`.claude/scripts/ci-graph.py`, fallback `$HOME/.claude/templates/repo-baseline/.claude/scripts/ci-graph.py`). It parses with PyYAML, else Ruby psych, else `uv run --with pyyaml`. It remaps the `on:` key that YAML 1.1 reads as `true` (precedents § 44). Exit 0 is clean, 1 means rows, and 2 is NOT-RUN (no loader, a parse error, no workflow, the settings API unreadable). Exit 2 is **never** a clean result (precedents § 41).

| Lane | Command | Trap that makes a clean result false |
|---|---|---|
| Graph | `python3 "$G" . --all`; `--contexts=<a,b> [--merge-queue]` or `--settings-dir=<dir>` (offline, from saved `gh api` responses; 0b passes `$SETTINGS_DIR` when the caller sets it) or `--required --online [--repo=o/r --branch=b]` (`gh` + token; without `--online` it prints `NOT-RUN OFFLINE` and exits 2); `--deploy-ancestors`; `--job-of=F:L`, `--shell-of=F:L` | No YAML loader → exit 2; GitHub only; a job that pushes through `docker/build-push-action` `outputs: …push=true` with no `push:` input is not counted as a publish (read it) |
| Settings | `gh api repos/{o}/{r}/rules/branches/{b}` **and** legacy `…/branches/{b}/protection/required_status_checks`; `…/actions/workflows`; GitLab `glab api projects/:id` | 403/404 = `UNREADABLE(gh api …: 403)`, never "absent" (precedents § 6); rulesets in evaluate mode are not returned `[K]` |
| GHA lint | `actionlint -format '{{json .}}'` 1.7.12, or, when the image is local, `docker run --pull=never --rm -i rhysd/actionlint:1.7.12 - < <file>` per file `[K]` (neither present → NOT-RUN; to enable: `docker pull rhysd/actionlint:1.7.12`) | exit 3 = no project (a bind-mount trap) → NOT-RUN; it checks that `needs:` exists, not that it is sufficient |
| Shell probe | the four lines of V210 (below) | none: runs with no CI access |
| Expansion | `circleci config process`, `glab ci lint --dry-run --ref <b>` | needs the CLI or a token → `blocked (<cli> absent)`; then the raw file is grepped and the row says so |

## Pre-flight greps

Run as **one** script from the repo root; shell state does not survive between tool calls. Grep **N** feeds **§N**; 0 is the inventory and the graph, F is the security fallback lane. Every `rg` names its path (`.`): given no path, rg reads stdin under an agent's shell and reports a silent zero. An rg exit 2 is a failed grep, never zero hits. File-level greps use `--files-without-match`, never `rg -L` (that is `--follow`). `--hidden` is required: `.github`, `.gitlab` and `.circleci` are dot-directories.

```bash
CI=(--hidden -g '.github/workflows/*.{yml,yaml}' -g '**/.gitlab-ci*.yml' -g '.gitlab/**/*.{yml,yaml}' -g '.circleci/*.{yml,yaml}'
    -g '**/bitbucket-pipelines.yml' -g '**/azure-pipelines*.yml' -g '**/*.azure-pipelines.yml' -g '**/Jenkinsfile*' -g '**/*.jenkinsfile'
    -g '**/vars/*.groovy' -g '**/action.{yml,yaml}' -g '!**/{node_modules,vendor,dist,build,test,tests,__tests__,spec,e2e,fixtures,__fixtures__,testdata}/**')
GH=(--hidden -g '.github/workflows/*.{yml,yaml}' -g '**/action.{yml,yaml}' -g '!**/{node_modules,vendor,fixtures,__fixtures__,testdata}/**')
GL=(--hidden -g '**/.gitlab-ci*.yml' -g '.gitlab/**/*.{yml,yaml}' -g '!**/{node_modules,vendor,fixtures,__fixtures__,testdata}/**')
AZ=(-g '**/azure-pipelines*.yml' -g '**/*.azure-pipelines.yml' -g '!**/{node_modules,vendor,fixtures,__fixtures__,testdata}/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(#|//)')   # drops YAML and Groovy comment-only lines
MUT='\b(kubectl\b[^\n|;&]*?\s(apply|set\s+image|replace|rollout\s+restart)|kustomize\s+edit\s+set\s+image|helm\s+(upgrade|install|rollback)|terraform\s+apply|tofu\s+apply|pulumi\s+up|fly\s+deploy|railway\s+up|vercel\b[^\n]*--prod|netlify\s+deploy[^\n]*--prod|npm\s+publish|pnpm\s+publish|yarn\s+npm\s+publish|twine\s+upload|cargo\s+publish|gem\s+push|docker\s+(push|buildx\s+imagetools\s+create)|crane\s+(copy|tag)|gh\s+release\s+(create|upload)|aws\s+(ecs\s+update-service|lambda\s+update-function-code|s3\s+sync)|gcloud\s+run\s+deploy|az\s+webapp\s+deploy|serverless\s+deploy|cdk\s+deploy|argocd\s+app\s+sync)\b'
G=.claude/scripts/ci-graph.py; [ -f "$G" ] || G="$HOME/.claude/templates/repo-baseline/.claude/scripts/ci-graph.py"
echo '# 0a lanes: every CI file, by platform'; rg --files "${CI[@]}" . | sort
echo '# 0b graph (GitHub Actions only): structural rows; exit 2 = NOT-RUN, never clean'
if [ -n "$(rg --files "${GH[@]}" -g '!**/action.{yml,yaml}' .)" ]; then python3 "$G" . --all ${SETTINGS_DIR:+--settings-dir="$SETTINGS_DIR"}; echo "ci-graph exit=$?"; else echo 'ci-graph: N/A (no GitHub workflow)'; fi
echo '# 1a masking: continue-on-error / allow_failure / continueOnError / || true / set +e / Jenkins catchError, returnStatus, propagate'
rg -n --pcre2 "${CI[@]}" '^\s*-?\s*(continue-on-error|allow_failure|continueOnError)\s*:\s*(true\b|\$\{\{|\{?\s*exit_codes)|\|\|\s*(true|:|exit\s+0|echo)\b|^\s*-?\s*set\s+\+e\b|\bcatchError\s*\(|\breturnStatus\s*:\s*true|\bpropagate\s*:\s*false|\bunstable\s*\(|\btrap\s+[\x27"]exit 0[\x27"]\s+ERR|\bmake\s+-k\b|--if-present\b' . | "${NC[@]}"
echo '# 1b scanner flags that zero the exit; GitLab when: manual (allow_failure defaults true)'
rg -n --pcre2 "${CI[@]}" '\bexit-code\s*:\s*[\x27"]?0\b|--exit-code[ =]0\b|--soft-fail\b|--no-fail\b|--no-exit-codes?\b|\bzizmor\b[^\n]*--format[ =]sarif|\bpoutine\b(?![^\n]*--fail-on-violation)' . | "${NC[@]}"
rg -n --pcre2 "${GL[@]}" '^\s{2,6}when\s*:\s*manual\b' . | "${NC[@]}"
echo '# 2a pipes into a filter (the producer exit is lost without pipefail); 2b risky shell overrides; 2c Azure multi-line scripts'
rg -n --pcre2 "${CI[@]}" '(?<![|>])\|(?!\|)\s*(tee|grep|head|tail|sed|awk|jq|sort|uniq|cut|xargs)\b' . | "${NC[@]}"
rg -n --pcre2 "${CI[@]}" '^\s*-?\s*shell\s*:\s*(sh|bash\s+\{0\}|bash\s+-e\s+\{0\}|sh\s+-e\s+\{0\})\s*$' . | "${NC[@]}"
rg -n --pcre2 "${AZ[@]}" '^\s*-?\s*(script|bash)\s*:\s*[|>]' .
echo '# 3 required-check skips: workflow path/branch filters, job if: on actor/label/draft/event, merge_group; GitLab rules:changes, needs:optional'
rg -n --pcre2 "${GH[@]}" '^\s{4}(paths|paths-ignore|branches-ignore)\s*:|^\s{4}if\s*:.*\b(github\.actor|labels|draft|github\.event_name|github\.head_ref)\b|^\s{2}merge_group\s*:' . | "${NC[@]}"
rg -n --pcre2 "${GL[@]}" '^\s*-?\s*changes\s*:|\bcompare_to\s*:|\boptional\s*:\s*true\b' . | "${NC[@]}"
echo '# 4a deploy / publish verbs; 4b gate bypasses (empty needs, status functions, always-run, workflow_run, Jenkins post blocks)'
rg -n --pcre2 "${CI[@]}" "$MUT" . | "${NC[@]}"
rg -n --pcre2 "${CI[@]}" '\b(needs|dependsOn)\s*:\s*\[\s*\]|\boptional\s*:\s*true\b|\bif\s*:[^\n]*(always\(\)|!\s*cancelled\(\)|success\(\)\s*\|\|\s*failure\(\))|\bcondition\s*:\s*(always\(\)|succeededOrFailed\(\))|^\s*-?\s*when\s*:\s*always\b|^\s{2}workflow_run\s*:' . | "${NC[@]}"
rg -n --pcre2 -g '**/Jenkinsfile*' -g '**/*.jenkinsfile' -g '!**/{node_modules,vendor,fixtures,__fixtures__,testdata}/**' '^\s*(always|cleanup|unstable|changed)\s*\{' . | "${NC[@]}"
echo '# 5 refs from inputs; deploy workflows on any branch; free-text dispatch inputs'
rg -n --pcre2 "${CI[@]}" '\bref\s*:\s*\$\{\{\s*(github\.event\.)?inputs\.|\bbranches\s*:\s*\[?\s*[\x27"]\*\*?[\x27"]|^\s{6,8}(ref|branch|sha|tag|version|image)\s*:\s*$' . | "${NC[@]}"
echo '# 6 unbounded deploy waits; non-GitHub CI files with no timeout key at all'
rg -n --pcre2 "${CI[@]}" '\b(kubectl\b[^\n|;&]*?\srollout\s+status|(kubectl\s+)?argo\s+rollouts\s+status|helm\s+(upgrade|install)\b[^\n]*--wait)\b(?![^\n]*--timeout)' . | "${NC[@]}"
rg --files-without-match --pcre2 "${CI[@]}" -g '!.github/**' -g '!**/action.{yml,yaml}' '^\s*-?\s*(timeout|timeoutInMinutes|no_output_timeout|max-time)\s*:|\btimeout\s*\(' .
echo '# 7 matrix exclude lists and dynamic matrices (the graph checks them against .nvmrc / engines / requires-python)'
rg -n --pcre2 "${CI[@]}" '^\s*exclude\s*:|\bfromJSON\(\s*needs\.' . | "${NC[@]}"
echo '# 8 schedules'
rg -n --pcre2 "${CI[@]}" '^\s*-?\s*cron\s*:|\bcron\s*\(\s*[\x27"]|^\s*schedules\s*:' . | "${NC[@]}"
```

Then, for every GitHub hit in greps 1–2: `python3 "$G" . --job-of=<file:line> --shell-of=<file:line>`. That names the job and the effective shell. The shell row (`pipefail=yes|no`, `source=step|job|workflow|default`) is what decides §2. Once per run, `python3 "$G" . --required --online --deploy-ancestors` (or `--contexts=` from a rules snapshot) prints, for every job, `required=` and `ancestor-of=`. Rule 1 reads that column.

Blind spots, worked around rather than trusted:
- **A wrapper script.** `run: ./scripts/ci.sh` hides its `|| true` and pipes. Read every script a gate step runs: it either sets `set -euo pipefail`, or each pipe is checked.
- **Includes, orbs and templates** (GitLab `include: project:`, CircleCI orbs, Azure `template:`, Jenkins shared libraries) live outside the file. Expand them (§ Tool lane), or the row says `blocked (remote include not expanded)`.
- **A multi-line `if: |` block** around `${{ }}` is a string, so it is always true (zizmor `unsound-condition`). Grep 4b catches only the one-line form. Read every `if: |`.

### Measured (2026-10-10)

| Tree | Result |
|---|---|
| Seeded sample: GitHub Actions (5 workflows), GitLab, CircleCI, Bitbucket, Azure, Jenkins; 27 positives, 17 decoys, 5 routed | Whole script 0.5 s, 0 rg errors. **27/27 positives surface** in their § (with `--contexts=all-green --merge-queue` for the three §3 graph rows). 3 decoys never appear: prose in `docs/`, a workflow under `tests/fixtures/`, a Bitbucket `after-script`. 14 surface and are cleared on read, each by one precedent or one `--shell-of` row: cleanup `\|\| true` ×2 (precedents § 13), `if: always()` upload/notify/test-report ×3 (precedents § 8), a pipe under `shell: bash` and one on CircleCI (precedents § 14), advisory masks ×2 (precedents § 7), a PR preview (precedents § 24), a manual deploy, CircleCI `when: always`, a Slack `catchError`, a `\| cut` inside `$(…)` |
| `benchmarks/fixtures/*` (15) | 36 lines in 3 fixtures; 12 have no CI file. brittle-suite 12: 6 `NO-TIMEOUT`, 3 test-job masks (routed to testing), 1 services image (F lane). quality-mix 5: 3 `NO-TIMEOUT`. vuln-fullstack 19: the PR preview's graph rows (a precedents § 24 decoy) and the F lane's seeded issue-title injection plus a `head.sha` checkout ref. One FP class was fixed before shipping: grep 2b matched every `defaults:` key (3 → 0); the graph's `--shell-of` resolves defaults instead |
| Real NestJS + Fastify monorepo (one 488-line workflow, read-only, `git status` clean before and after) | 1.9 s. `ci-graph.py --all` exits 0: every action is SHA-pinned, the workflow cancels only off `main`, every job has a timeout. 1 candidate: §1, `continue-on-error: true` on an advisory runtime leg (`ancestor-of=-`, `required=unknown`). Without a token it stays `[report-flagged]` (precedents § 7). F lane: 12 expression candidates, all `matrix.*` constants or `with:` data on read; 2 write scopes; 3 services images without a digest |

## The 3,000-hit path

1. **Intersect** with `ci-graph.py --required --online --deploy-ancestors`. Keep the hits in a required job, an ancestor of a deploy or publish job, or that job itself. Dismiss the rest with one read each (precedents § 7), and name them in the coverage block.
2. **Group** by unit: reusable workflow, composite action, GitLab template or `extends:` base, CircleCI orb command, Jenkins shared-library step (precedents § 5).
3. **Rank:** prod deploy and publish paths first, then required checks, then the rest.
4. **Read the top 30 groups.**
5. **Run the bulk oracle once:**
   - `ci-graph.py --all` settles every GitHub structural row;
   - the V210 probe settles every §2 row of one platform;
   - one seeded-failure branch per platform (V209) settles every §1 row in that pipeline.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits — <continuing command>)`. Never mark it `checked`.

## Scans for

Severity follows rule 1: **C** on a required check or a deploy/publish ancestor (when the merge or the deploy is real), **H** otherwise on a gate, **M** for cost and hygiene. Never grade by job name.

| § | Classes | Default severity |
|---|---|---|
| 1 | PC-1 failure swallowed on a non-domain gate (scan, build, smoke, migration check, deploy, publish, aggregator, rules gate) | H; C on a required check or deploy ancestor |
| 2 | PC-2 exit status lost by the shell | H on a gate; M otherwise |
| 3 | PC-3 required check never reported, or satisfied by a skip | C |
| 4 | PC-4 / RL-3 deploy or publish not gated on tests | C |
| 5 | PC-8 unvalidated ref built or deployed | H |
| 6 | PC-6 job timeouts unset; unbounded deploy waits | M (H on self-hosted or larger runners) |
| 7 | PC-7 matrix hides signal | M |
| 8 | PC-9 scheduled job dead or racing | L/M (H when it is the only backup or security verification) |

### 1. Failure swallowed on a non-domain gate (PC-1)

```
BAD:   - uses: aquasecurity/trivy-action@<sha>  with: { exit-code: 0 }        # the scan can never fail
       - name: smoke  continue-on-error: true  run: ./scripts/smoke.sh       # in a job the aggregator needs
       container_scanning: { allow_failure: true }                           # GitLab
       catchError(buildResult: 'SUCCESS') { sh 'trivy image --exit-code 1 …' }   // Jenkins
GOOD:  exit-code: 1 on the gate; continue-on-error only on a declared-experimental leg (precedents § 12); cleanup keeps `|| true` (precedents § 13)
```
**Read the code:**
- Which job holds the hit (`--job-of`)? Is it required, or a deploy ancestor? Is the masked command the gate itself, or cleanup (`docker rm`, `pkill`)?
- Test, lint or a11y command? Route it (§ Boundaries).
- Does an aggregator check `needs.*.result` and fail on it? Does a later step re-run the gate?
- GitLab `when: manual` (R8): is the manual job a gate the pipeline waits on, or a deploy action?

**Finding when** a failing gate command leaves its job, or the required context, green. **Proof (V209):** seed `exit 1` as the gate's first line on a sandbox branch. Every required context and every deploy ancestor must conclude `failure`. Use the per-platform read in `proof-oracles.md` § *Seeded failure, per platform*.

### 2. Exit status lost by the shell (PC-2)

```
BAD:   run: pnpm build 2>&1 | tee build.log            # GitHub default `bash -e`: tee's 0 wins (S1)
       script: | ./scripts/smoke.sh \n echo done        # Azure multi-line: last command wins (S6 [K?])
       sh 'make build | tee build.log'                  // Jenkins `sh -xe` (S7)
GOOD:  shell: bash (adds -o pipefail) · set -o pipefail as the first line · test "${PIPESTATUS[0]}" -eq 0
```
**Read the code:**
- What is the effective shell (`--shell-of`, or the lane table)? Is the producer the gate (`trivy … | tee`)?
- Does the script set pipefail or check `PIPESTATUS`? Is it CircleCI (precedents § 14)?
- `grep -q` as an `if` condition is not a pipe that masks (precedents § 14). `head` in a pipe under pipefail is the opposite trap (SIGPIPE): note it, do not fix it blindly.

**Finding when** the row says the pipe masks and the producer is a gate. **Proof (V210):** `bash -e -c 'false | tee /dev/null'` → 0; `bash -eo pipefail -c 'false | tee /dev/null'` → 1; `bash -c $'false\necho done'` → 0; `sh -e -c 'false | cat'` → 0. Then seed the producer (V209) for the pipeline-level proof.

### 3. Required check never reported, or satisfied by a skip (PC-3)

```
BAD:   on: pull_request: paths-ignore: ['docs/**']   on the workflow holding a required job (R3: Pending forever)
       test: if: github.actor != 'dependabot[bot]'   (R1: skipped reports success)
       all-green: if: always() … test "${{ needs.build.result }}" != "failure"   (cancelled passes; precedents § 10)
GOOD:  path filtering inside the workflow behind an always() aggregator that fails unless every needs.*.result is success or skipped-by-design (precedents § 9)
```
**Read the code:**
- Which contexts are required? Use `--required --online`, or a rules snapshot via `--contexts=`. Read both the rulesets and the legacy protection, because they coexist.
- Does each context map to a job (`REQUIRED-UNMATCHED`, `DUP-NAME`)? A matrix job's context is `name (leg)`.
- Is the merge queue on? Then `merge_group:` is needed (R5).
- GitLab: are `only_allow_merge_if_pipeline_succeeds` and `allow_merge_on_skipped_pipeline` set (`glab api projects/:id`)? Does any `rules:changes` lack `compare_to:` (R10)?

**Finding when** a required context can end Pending-forever or `skipped` without a run. **Proof (V211):** open a docs-only PR, a bot PR and a merge-queue entry in a sandbox. Each required context must get a conclusion from a real run. Graph codes: `REQUIRED-PATH-FILTERED`, `REQUIRED-IF-SKIP`, `REQUIRED-NEEDS-SKIP`, `NO-MERGE-GROUP`, `AGGREGATOR-WEAK`, `DUP-NAME`, `REQUIRED-UNMATCHED`.

### 4. Deploy or publish not gated on tests (PC-4, RL-3)

```
BAD:   deploy-prod: needs: test  if: always()                (GitHub: runs after a failed test)
       deploy_prod: needs: []                                 (GitLab: starts before the test stage)
       - stage: deploy  dependsOn: []                         (Azure)    ·    post { always { sh 'kubectl apply …' } }   (Jenkins)
       workflows: main: jobs: [build, deploy]                  (CircleCI: no requires:)
GOOD:  needs: [test, build] with no status function · workflow_run gated on conclusion == 'success' · requires: [build]
```
**Read the code:**
- Which jobs deploy or publish? Grep 4a, `environment:`, and the graph's `deploys=`/`publishes=` columns all say. Does `--deploy-ancestors` reach a test job?
- Is it a preview deploy per PR (precedents § 24), or a hotfix dispatch that re-runs the tests in the same workflow?
- Graph codes: `DEPLOY-UNGATED`, `DEPLOY-ALWAYS`, `WORKFLOW_RUN-NO-CONCLUSION`.

**Finding when** a failing test does not stop the deploy or publish. **Proof (V212):** seed a failure. The deploy job must be `skipped`, and `crane digest <ref>` / `npm view <pkg> versions` must be unchanged.

### 5. Unvalidated ref built or deployed (PC-8)

```
BAD:   workflow_dispatch: inputs: ref: { type: string }  →  actions/checkout with: ref: ${{ inputs.ref }}  →  kubectl apply
       on: push: branches: ['**']   on a deploy workflow
GOOD:  type: choice of release tags, or resolve the SHA and `git merge-base --is-ancestor <sha> origin/main`; environment deployment_branch_policy
```
**Read the code:**
- Is the input a `choice` of fixed tags, or checked before use?
- Does the target environment restrict branches? Read `gh api repos/{o}/{r}/environments/{env}`; `deployment_branch_policy: null` lets any branch deploy.
- GitLab: does the deploy job lack a `$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH` rule or a protected environment?

**Finding when** write access alone can ship an unreviewed branch to a protected environment. **Proof (V215):** a settings read (A), plus a dispatch from a feature branch that is refused (R). An injection reading of the same input is security's (F lane).

### 6. Timeouts unset; unbounded deploy waits (PC-6)

`ci-graph.py --check=timeout` prints `NO-TIMEOUT` (C4: 360 min; `THR-CI-JOB-TIMEOUT`) and `WAIT-NO-TIMEOUT` (`rollout status`, `argo rollouts status`, `helm --wait` with no `--timeout`). It skips `uses:` caller jobs, which cannot set a timeout (precedents § 11). Other platforms: grep 6 lists files with no timeout key at all, which fall back to the platform default `[K]` (GitLab project timeout, CircleCI `no_output_timeout`, Azure 60 min, Jenkins unbounded).

**Read:** is it a self-hosted or larger runner (cost ×)? Is the wait inside a deploy job? **Finding when** a job runs to the 360-minute default, or a deploy wait has no bound. **Proof (V213):** the graph row disappears after the fix.

### 7. Matrix hides signal (PC-7)

`ci-graph.py --check=matrix` prints two rows:
- `MATRIX-EXCLUDES-RUNTIME`: an `exclude:` that drops a runtime `.nvmrc`, `.node-version`, `engines` or `requires-python` declares;
- `MATRIX-DYNAMIC-UNGUARDED`: `fromJSON(needs.x.outputs.m)` with no non-empty guard. An empty matrix skips the job, and a skip is success (R1).

A required context named after one leg breaks when the matrix changes (§3).

**Read:** is the excluded leg declared unsupported, or experimental (precedents § 12)? **Finding when** a supported runtime goes untested while CI stays green. **Proof (V214):** the graph row disappears, and every declared runtime runs on a required leg.

### 8. Scheduled job dead or racing (PC-9)

Grep 8 lists the schedules. Then read `gh api repos/{o}/{r}/actions/workflows --jq '.workflows[]|[.path,.state]'` (`disabled_inactivity`; C5, public repos, 60 days) and the last run, `gh run list -w <file> -L 1`. GitLab schedules live in project settings (`glab api projects/:id/pipeline_schedules`). Without a token the row is `UNREADABLE` → Unconfirmed.

**Read:** is it a nightly security, backup-verify or dependency job, or two schedules writing one target? **Finding when** it has not run inside its period. **Proof (V216):** a settings read (A).

## Security fallback lane — when the security pack is not installed

Run only when neither `.claude/skills/ci-security-scan/` nor `.claude/skills/iac-scan/` exists. Detection is by the owning skill, not the pack: a partial security install with no CI skill still runs this lane. Every row prints `security-class (owner pack not installed)` at this skill's severity, never graded as security would grade it (precedents § 1). The read step applies the security precedents in outline: an integer field, a `with:` value read as data, an `env:` indirection read as `"$VAR"`, a SHA under `ref:`.

```bash
if [ ! -d .claude/skills/ci-security-scan ] && [ ! -d .claude/skills/iac-scan ]; then
W=(--hidden -g '.github/workflows/*.{yml,yaml}' -g '**/action.{yml,yaml}' -g '!**/{node_modules,vendor,fixtures,__fixtures__,testdata}/**')
INJ='\$\{\{(?:(?!\}\}).)*?(?:\bgithub\.event\s*\[|\bgithub\.event\.(?:issue|pull_request|comment|review|review_comment|discussion|discussion_comment|head_commit|commits|pages|workflow_run|inputs|release|merge_group|check_run|check_suite|deployment|client_payload)\b|\bgithub\.head_ref\b|(?<![\w.])inputs\.|(?<![\w.])env\.|\bsteps\.[\w-]+\.outputs\.|\bneeds\.[\w-]+\.outputs\.|(?<![\w.])matrix\.)(?:(?!\}\}).)*\}\}'
rg -n -o --pcre2 "${W[@]}" "$INJ" . | rg -v --pcre2 ':\$\{\{\s*github\.event\.[\w.]+\.(?:number|id)\s*\}\}$'   # F1 per match: an integer on the line no longer hides a title
rg -n --pcre2 "${W[@]}" 'permissions:\s*write-all|\b(contents|packages|id-token|actions|pull-requests|deployments|security-events|statuses|checks|issues|attestations|pages|discussions|repository-projects)\s*:\s*write\b' . | "${NC[@]}"
rg -n --pcre2 "${W[@]}" '^\s{2}(pull_request_target|workflow_run|issue_comment|pull_request_review_comment|discussion_comment)\s*:|refs/pull/|allow-unsafe-pr-checkout\s*:\s*true|\bgh\s+pr\s+checkout\b|\bgit\s+fetch\b[^\n]*\bpull/|merge_commit_sha|head\.repo\.full_name|github\.event\.pull_request\.head\.(sha|ref)\b' . | "${NC[@]}"
rg -n --pcre2 "${W[@]}" '^\s*(container|image)\s*:\s*[\x22\x27]?(?!\$\{\{)(?![^\n]*@sha256:)[\w./-]+(:[\w.-]+)?[\x22\x27]?\s*$|\buses\s*:\s*[\x22\x27]?docker://(?![^\n]*@sha256:)' . | "${NC[@]}"
[ -n "$(rg --files "${W[@]}" .)" ] && python3 "$G" . --check=pin-priv
else echo 'F: skipped (security pack installed: ci-security-scan / iac-scan § 5 own these classes)'; fi
```

The lane covers GitHub only. Attacker classes on GitLab, CircleCI, Bitbucket, Azure and Jenkins print `blocked (owner pack security not installed; no fallback for <platform>)`. The fallback is a floor, not the audit.

## Proof

The oracles, their tiers and the per-platform seeded-failure reads are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § DevOps. **Scope: a sandbox repository the user names, scratch branches and `${TMPDIR}` only, never the user's own branches.**

| § | Oracle | Tier | V |
|---|---|---|---|
| 1, 4 | Seeded failure: one `exit 1` per gate; required contexts and deploy ancestors conclude `failure`; deploy `skipped`; digest unchanged | R | V209, V212 |
| 2 | Shell-semantics probe (four lines) under the step's effective shell | T | V210 |
| 3 | Required-check join: docs-only PR, bot PR, merge-queue entry | A + R | V211 |
| 5, 8 | Settings read: environment branch policy; workflow `state` and last run | A | V215, V216 |
| 6, 7 | Graph assertion: `ci-graph.py --check=timeout,matrix` exits 0 after the fix, 1 before | T | V213, V214 |

`act` is a smoke check, never the proof (precedents § 45, § 46). A row whose oracle needs A with no token prints `UNREADABLE(gh api …: 403)` and stays Unconfirmed. A fix is checked with `ci-graph.py --diff-guard="$FIX_BASE" --allow-job=<file>:<job>` (the `=` forms: with a space, `--diff-guard` expects two files and exits 2; a workflow-level finding adds `--allow-workflow=<file>:<key>`): a fix that touches `on:`, `if:`, `needs:`, `concurrency:`, `permissions:`, `environment:`, `runs-on:` or `secrets:` outside the finding's job is rejected.

## Output

```
pipeline-integrity-scan — lanes: github-actions (5 workflows; ci-graph.py PyYAML), gitlab, circleci, bitbucket, azure, jenkins (grep + read)
Required set: --contexts=all-green (rules snapshot .refract/rules.json) · merge queue: on · security pack: not installed (F lane ran)

Findings: 2 · Unconfirmed: 4

1. .github/workflows/cd.yml:26                                             [report-with-fix]   critical
   §4 PC-4 — deploy-prod `needs: test` with `if: always()` (DEPLOY-ALWAYS): a failed test still deploys prod
   (R2). Proof: seeded `exit 1` in test on sandbox branch → deploy-prod ran, digest moved (V212, fails).
   Fix: drop `if: always()` from deploy-prod; keep `always()` only on the notify job (precedents § 8).

2. .github/workflows/ci.yml:41                                             [report-with-fix]   high
   §2 PC-2 — `pnpm build 2>&1 | tee build.log` in job build (ancestor-of=image-scan → all-green, required);
   --shell-of: "bash -e {0}" pipefail=no source=default (S1). Proof: V210 probe exits 0. Fix: `shell: bash`
   on the step, or `defaults: run: shell: bash` on the job.

3. .gitlab-ci.yml:16                                                       [report-flagged]    high
   §1 PC-1 — `allow_failure: true` on container_scanning: a HIGH CVE leaves the pipeline green.
   Unproven link: no GitLab sandbox run; deploy_prod has `needs: []`, so the scan gates nothing (see §4).
   Settling test: seeded `exit 1` → pipeline `failed` (proof-oracles § Seeded failure, GitLab row).

Verification: 41 candidates → 2 findings · 4 unconfirmed · 1 hardening · 0 pre-existing · 20 refuted (self-verified) · 14 routed

Class coverage:
  §1  masking on non-domain gates        checked (16 hits → 1 finding · 1 unconfirmed; 2 routed: lint → code-quality, test → testing)
  §2  shell exit semantics               checked (9 hits → 1 finding; 1 refuted by shell: bash, 1 by CircleCI pipefail)
  §3  required-check join                checked (contexts from snapshot: 3 graph rows → 1 unconfirmed, AGGREGATOR-WEAK awaiting V211)
  §4  deploy / publish gating            checked (6 deploy jobs → 1 finding; preview refuted by precedents § 24)
  §5  unvalidated refs                   checked (3 hits → 1 unconfirmed: environment policy UNREADABLE(gh api …: 403))
  §6  timeouts                           checked (graph: 1 NO-TIMEOUT, 2 WAIT-NO-TIMEOUT → hardening)
  §7  matrix                             checked (1 MATRIX-EXCLUDES-RUNTIME → refuted: leg declared experimental, precedents § 12)
  §8  schedules                          Unconfirmed (1 cron; workflow state UNREADABLE)
  F   security fallback                  4 rows tagged security-class (owner pack not installed)
```

`[report-with-fix]`: the gate, its required or deploy reach, the platform row and the oracle are all in hand, and the fix is local to the job. `[report-flagged]`: one link is unproven. That may be required-ness unreadable, a `[K?]` platform row, a remote include not expanded, or no sandbox run. The row names the link and the settling test.

The coverage block lists **all eight** §s and the F lane on every run:
- `checked (k hits → m findings)` only when the grep ran on a lane that is present;
- `N/A (no CI file)` or `N/A (<platform> absent)`;
- `blocked (<reason>)` when a grep, the graph or an expansion failed. A `ci-graph.py` exit 2 makes every GitHub structural row `blocked (ci-graph NOT-RUN: <reason>)`;
- `Unconfirmed (… UNREADABLE …)` when only a settings read can decide;
- `Live, unreviewed (k groups / n hits)` for a partial review, never `checked`.

## False positives / precedents

The verifier reads [`precedents/devops.md`](../../../../snippets/precedents/devops.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- **§ 7** Masking on a job that is neither required nor a deploy ancestor. Precondition: the rules API was read. Unreadable → `[report-flagged]`, never cleared.
- **§ 8** `always()` / `failure()` / `!cancelled()` on cleanup, artifact-on-failure and notify steps, and on an aggregator that reads `needs.*.result`.
- **§ 9** Job-level path filtering behind an `always()` aggregator. **§ 10** names the aggregator's own required shape.
- **§ 11** No `timeout-minutes` on a `uses:` caller. **§ 12** `continue-on-error: ${{ matrix.experimental }}` with `fail-fast: false`.
- **§ 13** `|| true` on idempotent cleanup. **§ 14** A pipe on CircleCI, a `PIPESTATUS` check, `grep -q` as a condition.
- **§ 16** Retries scoped to infrastructure failure classes. **§ 24** Preview environments.
- **§ 41** A tool that errored or parsed nothing is NOT-RUN. **§ 43** The GitHub default shell. **§ 44** The `on:` remap.

Rationalizations to reject:
- "CI is green, so the gate works": seed a failure.
- "The deploy has `needs:`": with `if: always()` it runs anyway.
- "That job is advisory": who says so? The rules API or the aggregator, not the job name.
- "actionlint is clean": it checks that `needs:` exists, not that it is sufficient.

## When to run

- On any diff touching a CI file, a script a gate step runs, branch protection or rulesets (when exported), or `.nvmrc`/`engines`/`requires-python` (§7).
- After `/add-ci` (its Phase 6 runs this on the emitted file) and after a `/devops-fix` on a pipeline row.
- On every whole-repo `/devops-audit`, reporting all eight §s; the F lane when the security pack is absent.

## Halt conditions

- **Do not report a critical or high row as confirmed until a separate verifier has refuted it.** That verifier must not be the run that found it; it applies [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with `precedents/devops.md`.
  - Under `/devops-audit`, that happens in its verification phase.
  - Run standalone, apply the protocol as a second pass and tag those rows `self-verified`.
  - List the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- **Halt on any finding missing its anchors:** the line, the job, the required-or-deploy reach (or `UNREADABLE`), the platform row and the fix.
- **No severity from a job's name.** Rule 1's column decides it, from the graph, the rules API or a snapshot.
- **No `checked` on a lane whose tool failed.** `ci-graph.py` exit 2, an unexpanded remote include and an rg exit 2 are `blocked`.
- **Never run a seeded failure, a dispatch or a merge-queue entry on the user's own repository or branches.** Use a sandbox the user names; otherwise the row is Unconfirmed with the settling command written out.
- **No proposed fix may weaken a gate to make the row disappear.** That means no added `continue-on-error`, no `|| true`, no deleted required job, and no path filter on the required workflow. The `--diff-guard` must be clean outside the finding's job.
- **Do not print "CI looks fine" without the coverage block.** **Do not re-derive a class another skill owns** (§ Boundaries); cross-link it.

## Related

- `/devops-audit` dispatches this skill and folds its coverage block into the pipeline ledger row. `/devops-fix` closes the findings with the seeded-failure proof and `--diff-guard`. `/add-ci` (Phase 6) runs it on the workflow it emitted.
- `@ci-reviewer` judges these rows in refute mode. `@devops-architect` designs pipelines this skill then judges.
- `pipeline-cache-scan`, `deploy-safety-scan` and `release-integrity-scan` (this pack) own the neighbouring classes (§ Boundaries).
- `suite-execution-scan` (testing), `suppression-scan` (code-quality) and `a11y-scan` §7 (frontend) own gate masking on their own jobs, each when its pack is installed. `ci-security-scan` / `iac-scan` § 5 (security) owns the attacker paths.
- `ai/patterns/cicd-pipeline.md` is the pipeline shape the fixes follow.

## Sources

The platform rows in [`ci-platform-semantics.md`](../../../../snippets/ci-platform-semantics.md) were verified on 2026-10-10. They cite GitHub Docs *Workflow syntax*, *Troubleshooting required status checks*, *Disabling and enabling workflows* and *Dependency caching reference*; the GitLab *CI/CD YAML syntax reference*; CircleCI support; and the Atlassian KB. Tool behaviour comes from the devops research catalog's platform-semantics, pipeline-correctness and precedent notes (measured 2026-10-10): actionlint 1.7.12 and zizmor 1.30.1 on the green-theater fixture, and the four-line shell probe. The fallback greps come from the batch-4 devops eval (the security-boundary corrections it verified). Paraphrased; no text reproduced beyond identifiers.
