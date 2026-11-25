---
name: ci-security-scan
description: CI workflows as attack surface on six platforms — untrusted code in privileged jobs, expression injection, unpinned deps by token scope, secrets, runners.
kind: skill
pack: security
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: ci-security-scan

## Premise

A CI job runs with credentials: a token that can push, a secret that can publish, an OIDC role that can deploy. When someone outside the trust boundary can steer what that job executes, the token, the secret or the published artifact is theirs. That someone can be a fork author, a commenter, an issue author, or whoever controls an upstream action, image or tool. This skill is the security pack's static review of the files that define those jobs. It reads them as the maintainer's own code, the way `injection-scan` reads a request handler. It is the same class of review that zizmor, poutine and GitHub's own hardening guide describe.

**Scope is static.** It reads workflow files, the actions they call and repository settings through read-only `gh api` GETs. It runs offline analyzers into a ledger. It never sends an event, opens a fork PR or triggers a workflow, and it carries no exploit payloads. Gate 5 of [`finding-verification.md`](../../../../snippets/finding-verification.md) is met by the cited trace (who can start the job → the line that executes their input → what the job's token can do) plus the re-detect oracle each detector names.

**Every finding cites `<file:line>` + the trigger and who can fire it + the sink line + what the job's token, secrets or OIDC role can do + the fix + severity.** A grep hit or a scanner rule id is never a finding by itself, and "no CI findings" is never printed without the class-coverage block (§ Output).

## Boundaries

The claim shape decides the owner (`precedents/devops.md` § "The claim, restated"):
- **Attacker path → here.** An actor outside the trust boundary reaches code execution in a privileged job, a write token, a secret, an OIDC role or the published artifact.
- **No attacker → the devops pack.** A red build merges, what ships is not what was tested, or a deploy half-applies or races. When the devops pack is installed, `pipeline-integrity-scan` owns those rows and `@ci-reviewer` judges them. Signing, attestation and verification breadth stay with `release-security`. Without the pack, the ledger says `delivery integrity: not reviewed (devops pack not installed)`.
- **One line, both claims:** one finding per `<file:line>`, credited to the more severe claim, with the other listed as corroboration.
- `iac-scan` § 5 dispatches here and keeps its grep 6 as the candidate list. The value of a leaked secret is `secret-scan-method`'s (rotation first). The OIDC trust policy on the cloud side is IaC: `iac-scan` § 4, and the infrastructure pack when it is installed.

## Adapt to the codebase

Grep 0 inventories the platforms. Run the rows for the platforms present and **print the lanes you ran** in the output header. The column that decides most verdicts is the third one: **when** untrusted text becomes shell. Text substituted into the script before the shell parses it is code. Text expanded by the shell from a quoted variable is data.

| Lane | Files | Untrusted text → shell | Privileged contexts | Scanner lane | Safe primitive the fix names |
|---|---|---|---|---|---|
| **GitHub Actions** | `.github/workflows/*.y*ml`, `action.y*ml`, `.github/dependabot.yml` | `${{ }}` is substituted before the shell runs | `pull_request_target`, `workflow_run`, `issue_comment`, `issues`, `discussion*`, `labeled`; `permissions:` writes, `secrets.*`, `id-token: write` | zizmor (regular + auditor) ∪ poutine ∪ octoscan per file ∪ actionlint; `ci-graph.py` for the job graph | `env:` + `"$VAR"`; 40-hex SHA pins + a bot; per-job `permissions:`; `persist-credentials: false` |
| **GitLab CI** | `.gitlab-ci.yml`, `*.gitlab-ci.yml`, `.gitlab/**`, includes | `$VAR` is shell-expanded (quoted = data); `$[[ inputs.x ]]` is substituted first | MR pipelines run in the parent project; protected variables; `CI_JOB_TOKEN` | **grep + read**: checkov and poutine found nothing on the seeds | quoted `"$CI_…"`; `spec:inputs` with `options:` / `regex:`; include `ref:` 40-hex or `integrity:` |
| **CircleCI** | `.circleci/config.yml` | `<< pipeline.* >>` / `<< parameters.* >>` are substituted into config | fork-PR secrets setting, contexts | grep + read; checkov image ids | `"$CIRCLE_BRANCH"`; orbs at full semver; image digests; restricted contexts |
| **Bitbucket** | `bitbucket-pipelines.yml` | shell-expanded `$VAR` | `pull-requests:` pipelines, deployment variables | grep + read; checkov image id | pipes at full version; deployment environments with restrictions; `oidc: true` |
| **Azure Pipelines** | `azure-pipelines*.y*ml`, templates | `$(macro)` is substituted before the script runs; `##vso[` logging commands set variables | fork-PR builds with secrets, `persistCredentials`, `resources.repositories` | poutine (the only tool that caught the seeds) + grep | `env:` mapping + `"$VAR"`; `target.settableVariables`; repository `ref:` as a tag or SHA; required-template check |
| **Jenkins** | `Jenkinsfile*`, `*.jenkinsfile`, `vars/*.groovy`, JCasC | Groovy interpolates a double-quoted `sh "…${x}…"` before the shell | fork-PR trust policy; global libraries run outside the sandbox; executors on the controller | **none**: grep + read | single-quoted `sh '… $VAR'`; `@Library('lib@<tag or sha>')`; `TrustPermission`; zero controller executors |

## Tool ledger

Each tool is **RAN** (version, exit code, files parsed, hits, output path), **SKIPPED** (`n/a` only when grep 0 proves the platform is absent), or **NOT-INSTALLED** (the ledger prints the install command below for the user; an audit never runs a one-shot download). Write output to a scratch directory, never into the repo. A tool that parsed nothing is **NOT-RUN, never PASS** (`precedents/devops.md` § 41). Behaviour below is from the devops research notes (A § 0, § 3; measured 2026-10-10):

| Tool | Command | Trap that makes a clean result false |
|---|---|---|
| zizmor 1.30.1 (floor 1.28: 1.27.0 logged GitHub credentials, GHSA-f42p-wjw5-97qh) | `zizmor --offline --persona=regular --format=json .`, then `--persona=auditor` (installed only; to enable: `pipx install zizmor==1.30.1`) | exit **3** = no inputs collected; `--format=sarif` and `--no-exit-codes` force exit 0; 11–14 = highest severity found. Read stderr for `failed to parse input`. 1.30.1 misses the `issue_comment` PR checkout, `GITHUB_ENV` writes under `issues:`, AI-agent prompts and artifact execution, and flags every `workflow_run` (false positive). Docs describe unreleased 1.31 — do not cite it |
| poutine 1.1.6 | `poutine analyze_local . --format json -q --fail-on-violation` | exit 0 **with findings** unless `--fail-on-violation` (exit 10); needs a git repo. The only tool that caught the `issue_comment` checkout and the Azure injection |
| octoscan 0.1.7 (GPL-3.0: run, never vendor) | `octoscan scan <file> --oneline`, **one file per run** (linux/amd64 glibc) | `scan .` or a directory → 0 findings, exit 0. Catches `GITHUB_ENV`/`GITHUB_OUTPUT` writes under any trigger and expressions in `with:` (an agent `prompt:`) |
| actionlint 1.7.12 | `actionlint -format '{{json .}}'`; or, when the image is already local, per file on stdin: `docker run --pull=never --rm -i "rhysd/actionlint:1.7.12@$ACTIONLINT_DIGEST" -format '{{json .}}' - < <workflow>` (to enable: `docker pull rhysd/actionlint:1.7.12@$ACTIONLINT_DIGEST`) | exit 3 = no project found (a bind mount of `/private/tmp` is empty on Docker Desktop — stdin avoids it); it trusts `inputs.*`. A correctness and `if:` lane, not a security superset |
| checkov 3.3.26 | `checkov -d . --framework circleci_pipelines bitbucket_pipelines azure_pipelines -o json --compact` (installed only; to enable: `pipx install checkov==3.3.26`) | images only; GitLab and GitHub found ~nothing; a top-level `steps:` Azure file is not parsed (0 resources = NOT-RUN) |
| `ci-graph.py` | grep 4a (`--check=pin-priv`) | exit 2 = NOT-RUN (no YAML loader, a parse error, no workflow) |

Pin every scanner image by version **and** digest: the 2026-03 trivy-action compromise force-moved 76 of 77 tags. Record each digest once (`crane digest <image>:<version>`) and keep it in the ledger. A different digest under the same version is a stop, not an update. scorecard's Dangerous-Workflow check scored 10/10 on a fixture full of dangerous workflows, so it is not an oracle here. gato-x is an offensive tool: never use its attack modes, and enumerate only an org the user owns, with their consent.

## Pre-flight greps

Run as **one** script from the repo root, so the shell arrays survive. Grep **N** feeds detector **§ N**. Every `rg` names its path (`.`): with no path and a piped stdin, rg reads stdin and returns nothing. That is a false clean, and this skill exists to prevent it. A platform's absence comes from grep 0, **never from a quiet grep**. `CIG` points at the job-graph script the baseline installs.

```bash
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{fixtures,__fixtures__,testdata,examples}/**' -g '!.git/**')
W=(--hidden -g '**/.github/workflows/*.y*ml' -g '**/action.y*ml' "${X[@]}")
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*#')
G=(--hidden -g '.gitlab-ci.yml' -g '*.gitlab-ci.yml' -g '**/.gitlab/**/*.y*ml' "${X[@]}")
CIG="${CIG:-.claude/scripts/ci-graph.py}"
TRIG='^(on:\s*\[?[^\n#]*?\b|\s{2}-?\s*)(pull_request_target|workflow_run|issue_comment|pull_request_review_comment|pull_request_review|discussion_comment|discussion|issues|workflow_dispatch|repository_dispatch|workflow_call)\b(?!\s*:\s*(write|read|none)\b)'
EXT='^(on:\s*\[?[^\n#]*?\b|\s{2}-?\s*)(pull_request_target|workflow_run|issue_comment|pull_request_review_comment|pull_request_review|discussion_comment|discussion|issues)\b(?!\s*:\s*(write|read|none)\b)'

echo '## 0'
# 0. Inventory per platform (decides every N/A), then the files a privileged trigger starts.
rg --files --hidden "${X[@]}" . | rg --pcre2 '(^|/)(\.github/workflows/[^/]+\.ya?ml|action\.ya?ml|\.github/dependabot\.ya?ml|renovate\.json5?|\.?gitlab-ci\.yml|[^/]+\.gitlab-ci\.yml|\.circleci/config\.ya?ml|bitbucket-pipelines\.yml|azure-pipelines[^/]*\.ya?ml|Jenkinsfile[^/]*|[^/]+\.jenkinsfile|vars/[^/]+\.groovy)$'
rg -n --pcre2 "${W[@]}" "$TRIG" . | "${NC[@]}"

echo '## 1a'
# 1. Privileged trigger × untrusted code. 1a every way PR code reaches the runner, in privileged-trigger files only;
#    1b comment triggers with no author check in the file; 1c label gates, artifact sinks and dispatch chains to read.
rg -l --null --pcre2 "${W[@]}" "$EXT" . | xargs -0 -r rg -H -n --pcre2 'ref:\s*[\x22\x27]?\$\{\{\s*github\.(event\.pull_request\.head\.(sha|ref)|head_ref|event\.workflow_run\.head_(sha|branch))|refs/pull/|\bpull/\$\{\{|allow-unsafe-pr-checkout:\s*true|\bgh\s+pr\s+checkout\b|\bgit\s+fetch\b[^\n]*\bpull/|\bmerge_commit_sha\b|repository:\s*[\x22\x27]?\$\{\{\s*github\.event\.(pull_request\.head\.repo|workflow_run\.head_repository)\.full_name' | "${NC[@]}"
echo '## 1b'
rg -l --null --pcre2 "${W[@]}" '^(on:\s*\[?[^\n#]*?\b|\s{2}-?\s*)(issue_comment|pull_request_review_comment|discussion_comment)\b' . | xargs -0 -r rg --files-without-match 'author_association|getCollaboratorPermissionLevel|/collaborators/[^\s/]+/permission'
echo '## 1c'
rg -n --pcre2 "${W[@]}" 'types:\s*\[[^\]\n]*\blabeled\b|\b(download-artifact|action-download-artifact)@|\bgh\s+run\s+download\b|\bgh\s+workflow\s+run\b|\bcreateWorkflowDispatch\b|\bactions:\s*write\b|\bgit\s+push\b[^\n]*(--tags|\borigin\s+v\d)' . | "${NC[@]}"

echo '## 2a'
# 2. Expression injection. 2a every tainted context, ONE MATCH PER LINE OF OUTPUT (-o), so an integer beside a title no
#    longer hides it; the filter then drops matches that are only an integer/enum/boolean field (finding-verification § 4 CIP1).
INJ='\$\{\{(?:(?!\}\}).)*?(?:\bgithub\.event\s*\[|\bgithub\.event\.(?:issue|pull_request|comment|review|review_comment|discussion|discussion_comment|head_commit|commits|pages|workflow_run|inputs|release|merge_group|check_run|check_suite|deployment|client_payload)\b|\bgithub\.head_ref\b|(?<![\w.])inputs\.|(?<![\w.])env\.|\bsteps\.[\w-]+\.outputs\.|\bneeds\.[\w-]+\.outputs\.|(?<![\w.])matrix\.)(?:(?!\}\}).)*\}\}'
rg -n -o --pcre2 "${W[@]}" "$INJ" . | rg -v --pcre2 ':\$\{\{\s*github\.event\.[\w.]+\.(?:number|id|run_number|run_attempt|conclusion|fork|draft|merged)\s*\}\}$|:\$\{\{(?:(?!&&|\|\|)[^}])*(?:==|!=)(?:(?!&&|\|\|)[^}])*\}\}$'
echo '## 2b'
#    2b values written to GITHUB_ENV / GITHUB_PATH / GITHUB_OUTPUT, and loader variables set from an expression;
#    2c the units a caller feeds (composite actions, reusable workflows, local `uses: ./`) and matrices built from outputs.
rg -n --pcre2 "${W[@]}" '>>\s*[\x22\x27]?\$\{?(GITHUB_ENV|GITHUB_PATH|GITHUB_OUTPUT)\b|^\s*(LD_PRELOAD|LD_LIBRARY_PATH|BASH_ENV|NODE_OPTIONS|PYTHONPATH|PERL5OPT|RUBYOPT|GIT_SSH_COMMAND|GIT_ASKPASS)\s*:[^\n]*\$\{\{' . | "${NC[@]}"
echo '## 2c'
rg -n --pcre2 "${W[@]}" '^\s*using:\s*[\x22\x27]?composite|^\s{2}workflow_call\s*:|^\s*-?\s*uses:\s*[\x22\x27]?\./|fromJSON\(\s*(needs|steps)\.|\boutputs\.(all_)?(changed|modified|added|deleted|renamed)_files\b' . | "${NC[@]}"

echo '## 3'
# 3. AI agents in CI: the agent step, its tool and user allow-lists, CLIs driven from run:.
rg -n --pcre2 "${W[@]}" 'uses:\s*[\x22\x27]?(anthropics/claude-code-(base-)?action|google-github-actions/run-gemini-cli|openai/codex-action|actions/ai-inference|[\w-]+/[\w-]*(claude|gemini|codex|copilot|llm|gpt|openai|ai-agent)[\w-]*)@|\b(claude|gemini|codex|aider|opencode)\b\s+(-p|--print|exec|run)\b|--dangerously-skip-permissions|--yolo\b|\ballowed_?[tT]ools\b|\bclaude_args\s*:|\ballowed_non_write_users\s*:|\ballow-users\s*:' . | "${NC[@]}"

echo '## 4a'
# 4. Pinning × privilege. 4a the graded rows (job permissions, secrets, environment joined to each mutable uses:);
#    4b every non-SHA uses: (ledger); 4c images with no digest (IR-S6); 4d tools fetched at a moving version;
#    4e actions with a known compromise or archived upstream; 4f Dependabot that runs external code, no actions bot.
[ -n "$(rg --files "${W[@]}" .)" ] && { python3 "$CIG" . --check=pin-priv; echo "ci-graph exit $? (0 clean, 1 rows, 2 NOT-RUN)"; }
echo '## 4b'
rg -n --pcre2 "${W[@]}" '^\s*-?\s*uses:\s*[\x22\x27]?(?!\./|docker://)[^@\s]+@(?![0-9a-f]{40}\b)\S+' . | "${NC[@]}"
echo '## 4c'
rg -n --pcre2 "${W[@]}" '^\s*(container|image)\s*:\s*[\x22\x27]?(?!\$\{\{)(?![^\n]*@sha256:)[\w./-]+(:[\w.-]+)?[\x22\x27]?\s*$|\buses\s*:\s*[\x22\x27]?docker://(?![^\n]*@sha256:)' . | "${NC[@]}"
echo '## 4d'
rg -n --pcre2 "${W[@]}" '\b(curl|wget)\b[^\n|]*\|\s*(sudo\s+)?(ba|z|da)?sh\b|\b((ba|z)?sh|source)\s+<\(\s*(curl|wget)\b|\bnpx\s+(-y\s+)?(@[\w.-]+/)?[\w.-]+@latest\b|\bversion\s*:\s*[\x22\x27]?latest\b' . | "${NC[@]}"
echo '## 4e'
rg -n --pcre2 "${W[@]}" 'uses:\s*[\x22\x27]?(tj-actions/changed-files|reviewdog/action-setup|aquasecurity/(trivy-action|setup-trivy)|actions-cool/(issues-helper|maintain-one-comment)|actions/(create-release|upload-release-asset)|actions-rs/[\w-]+)@' . | "${NC[@]}"
echo '## 4f'
rg -n --hidden -g '**/.github/dependabot.y*ml' "${X[@]}" 'insecure-external-code-execution:\s*allow' . ; rg -q --hidden -g '**/.github/dependabot.y*ml' -g '**/renovate.json*' -g '**/.github/renovate.json*' "${X[@]}" 'github-actions|pinGitHubActionDigests|config:best-practices' . || echo 'no bot keeps action pins fresh (dependabot github-actions / renovate)'

echo '## 5a'
# 5. Cache and artifact trust. 5a cache writers in privileged-trigger files (they save into the default-branch scope);
#    5b cache readers in release/tag workflows; 5c the workspace or hidden files uploaded as an artifact.
CACHE='\bactions/cache(/save)?@|^\s*cache\s*:\s*[\x22\x27]?\w|\bcache-to\s*:[^\n]*type=gha|\benable-cache\s*:\s*true|\brust-cache@|\bbundler-cache\s*:\s*true|\bsetup-gradle@'
rg -l --null --pcre2 "${W[@]}" "$EXT" . | xargs -0 -r rg -H -n --pcre2 "$CACHE" | "${NC[@]}"
echo '## 5b'
rg -l --null --pcre2 "${W[@]}" '^\s{2}(release|registry_package)\s*:|^\s{4}tags\s*:' . | xargs -0 -r rg -H -n --pcre2 "$CACHE" | "${NC[@]}"
echo '## 5c'
rg -n -U --pcre2 "${W[@]}" 'upload-artifact@[^\n]*\n(?:[^\n]*\n){0,6}?\s+path:\s*[\x22\x27]?(\.|\./|\$\{\{\s*github\.workspace\s*\}\})[\x22\x27]?\s*$|include-hidden-files:\s*true' .

echo '## 6a'
# 6. Credentials and OIDC. 6a the whole secrets context, derived (unmasked) values, inherit; 6b long-lived publish
#    and cloud tokens; 6c secrets on argv, echoed or traced; 6d write scopes, any form (IR-S4) and files with no
#    permissions block; 6e workflow-level id-token; 6f checkouts that keep their token (awk).
rg -n --pcre2 "${W[@]}" 'toJSON\(\s*secrets\s*\)|\bsecrets\s*\[|fromJSON\(\s*secrets\.|\bsecrets:\s*inherit\b' . | "${NC[@]}"
echo '## 6b'
rg -n --pcre2 "${W[@]}" '\b(NPM_TOKEN|NODE_AUTH_TOKEN|PYPI_(API_)?TOKEN|TWINE_PASSWORD|CARGO_REGISTRY_TOKEN|GEM_HOST_API_KEY|NUGET_API_KEY|AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|AZURE_CREDENTIALS|GCP_SA_KEY|GOOGLE_CREDENTIALS)\b\s*:\s*[\x22\x27]?\$\{\{\s*secrets\.|\bpassword\s*:\s*[\x22\x27]?\$\{\{\s*secrets\.(?!GITHUB_TOKEN\b)' . | "${NC[@]}"
echo '## 6c'
rg -n --pcre2 "${W[@]}" '\b(echo|printf|cat)\b[^\n]*\$\{\{\s*secrets\.|\s(--password|--token|-p)\s+[\x22\x27]?\$\{\{\s*secrets\.|\bset\s+-[a-z]*x|ACTIONS_(STEP|RUNNER)_DEBUG|\bprintenv\b' . | "${NC[@]}"
echo '## 6d'
rg -n --pcre2 "${W[@]}" 'permissions:\s*write-all|\b(contents|packages|id-token|actions|pull-requests|deployments|security-events|statuses|checks|issues|attestations|pages|discussions|repository-projects)\s*:\s*write\b' . | "${NC[@]}"
rg --files-without-match --hidden -g '**/.github/workflows/*.y*ml' "${X[@]}" '^\s*permissions\s*:' .
echo '## 6e'
rg -n -U --pcre2 "${W[@]}" '^permissions:\s*(\{[^}\n]*\bid-token:\s*write|\n(?:[ \t]+[\w-]+:[^\n]*\n)*?[ \t]+id-token:\s*write)' .
echo '## 6f'
rg -l "${W[@]}" 'actions/checkout@' . | xargs -r awk 'function f() { if (c && !k) print cf ":" c ": checkout keeps its token in .git/config"; c = 0 } FNR == 1 { f() }
  /^ *[^ #]/ { match($0, /^ */); if (c && (RLENGTH < i || (RLENGTH == i && /^ *- /))) f() } /persist-credentials: *false/ { k = 1 }
  /uses: *actions\/checkout@/ { f(); c = FNR; cf = FILENAME; k = 0; match($0, /^ */); i = /^ *- / ? RLENGTH : RLENGTH - 2 } END { f() }'

echo '## 7'
# 7. Gates an attacker can pass: actor bot checks, string contains(), always-true if:, workflows that merge or approve.
rg -n --pcre2 "${W[@]}" '\bgithub\.(actor|triggering_actor)\s*[!=]=|contains\(\s*[\x22\x27][^\x22\x27]*[\x22\x27]\s*,\s*github\.|^\s*if:\s*[|>]|^\s*if:\s*[\x22\x27]?\$\{\{(?:(?!\}\}).)*\}\}\s*\S|\bgh\s+pr\s+(merge\b[^\n]*--auto|review\b[^\n]*--approve)|enable-pull-request-automerge@|dependabot/fetch-metadata@' . | "${NC[@]}"

echo '## 8'
# 8. Runners and rogue workflows: non-GitHub-hosted labels, exfiltration shapes, discussion triggers, workflow history.
rg -n --pcre2 "${W[@]}" '^\s*runs-on\s*:\s*\[?\s*[\x22\x27]?(?!ubuntu-|windows-|macos-|\$\{\{)[\w-]+|curl[^\n]*\s(-d|--data[\w-]*|-F|-T)\s[^\n]*\$\{\{\s*(secrets\.|toJSON\(\s*secrets)|webhook\.site|requestbin|pipedream\.net|ngrok(-free)?\.(io|app)|discord(app)?\.com/api/webhooks|base64[^\n]*\$\{\{\s*secrets\.|^\s{2}discussion\s*:|^on:\s*[^\n]*\bdiscussion\b' . | "${NC[@]}"
git log --format='%h %ad %an <%ae> %s' --date=short -n 40 -- .github/workflows .github/actions 2>/dev/null

echo '## 9a'
# 9. Other platforms (no scanner covers them; grep + read owns them). 9a GitLab: eval / sh -c of MR and commit text,
#    pre-templated inputs, includes with no pinned ref or integrity, images, shared caches, public artifacts, forwarded
#    variables; 9b CircleCI; 9c Bitbucket; 9d Azure; 9e Jenkins.
rg -n --pcre2 "${G[@]}" '\b(eval|sh\s+-c|bash\s+-c)\b[^\n]*\$\{?CI_(MERGE_REQUEST_\w+|COMMIT_(MESSAGE|TITLE|DESCRIPTION|BRANCH|REF_NAME|TAG_MESSAGE)|EXTERNAL_PULL_REQUEST_\w+)|(?<![\x22\w])\$\{?CI_(MERGE_REQUEST_(TITLE|DESCRIPTION|SOURCE_BRANCH_NAME)|COMMIT_(MESSAGE|TITLE|DESCRIPTION|BRANCH|REF_NAME))\b(?![\w}]*\x22)|\$\[\[\s*inputs\.[\w-]+' . | "${NC[@]}"
rg -n -A3 --pcre2 "${G[@]}" '^\s*-?\s*(project|remote|component|template)\s*:|^\s*(image|name)\s*:\s*[\x22\x27]?(?![^\n]*@sha256:)[\w./-]+(:[\w.-]+)?[\x22\x27]?\s*$|\bunprotect\s*:\s*true|\bfallback_keys\s*:|^\s*public\s*:\s*true|\baccess\s*:\s*[\x22\x27]?all\b|\bpipeline_variables\s*:\s*true' . | "${NC[@]}"
echo '## 9b'
rg -n --pcre2 --hidden -g '**/.circleci/*.y*ml' "${X[@]}" '^\s+[\w-]+:\s*[\w-]+/[\w-]+@(volatile|dev:\S+|\d+(\.\d+)?)\s*$|<<\s*(pipeline\.(git\.(branch|tag|revision)|trigger_parameters\.[\w.]+)|parameters\.[\w-]+)\s*>>|^\s*-?\s*image\s*:\s*(?![^\n]*@sha256:)\S+' . | "${NC[@]}"
echo '## 9c'
rg -n --pcre2 --hidden -g '**/bitbucket-pipelines.yml' "${X[@]}" '^\s*-?\s*pipe\s*:\s*\S+:(\d+|latest)\s*$|^\s*image\s*:\s*(?![^\n]*@sha256:)\S+|^\s{2}pull-requests\s*:|\becho\b[^\n]*\$\{?\w*(SECRET|TOKEN|PASSWORD|KEY)\w*' . | "${NC[@]}"
echo '## 9d'
rg -n -A4 --pcre2 --hidden -g '**/azure-pipelines*.y*ml' -g '**/.azure*/**/*.y*ml' "${X[@]}" '##vso\[task\.(setvariable|prependpath)|^\s*-?\s*(script|bash|pwsh|powershell)\s*:[^\n]*\$\((System\.PullRequest\.\w+|Build\.SourceVersionMessage|Build\.SourceBranch(Name)?|Build\.RequestedFor)\)|persistCredentials\s*:\s*true|^\s*-?\s*repository\s*:\s*\w|^\s*(container|image)\s*:\s*(?![^\n]*@sha256:)[\w./-]+(:[\w.-]+)?\s*$' . | "${NC[@]}"
echo '## 9e'
rg -n --pcre2 --hidden -g 'Jenkinsfile*' -g '*.jenkinsfile' -g '**/vars/*.groovy' "${X[@]}" '\b(sh|bat|powershell|pwsh)\s*\(?\s*(script:\s*)?"[^"\n]*\$\{?(env\.(CHANGE_\w+|BRANCH_NAME|TAG_NAME|GIT_\w+)|params\.\w+|\w*(TOKEN|PASS\w*|SECRET|KEY)\b)|@Library\(\s*[\x27\x22][^\x27\x22]+@(master|main|develop|[a-z][\w/-]*)[\x27\x22]|\blibrary\s*\(?\s*[\x27\x22][^\x27\x22]+@(master|main)|\btrust(Everybody|Everyone|Contributors)\b|^\s*agent\s+any\b' . | "${NC[@]}"
```

A finding is a grep hit **plus** a read of the whole job: its trigger, its `if:`, its `permissions:`, its secrets, its `environment:` and every step before the sink. The greps narrow; they do not decide. Three blind spots are structural:
- **Grep 2a sees one expression, not the step.** A match inside `with:` is data unless the action evaluates it (CIP3). A match inside `env:` is the fix unless the variable later reaches `eval`, `bash -c`, `GITHUB_ENV` or an unquoted position (CIP4). Grep 2b finds the second half.
- **Links across files are reads.** A caller's `with:` feeds a composite `run:`, a PR job's cache save feeds a release job's restore, workflow A's artifact is executed by `workflow_run` B. Greps 2c, 5a, 5b and 1c list each end; link them by reading.
- **Settings are invisible in YAML:** the default token permission, fork-PR approval, "Actions can approve PRs", environment reviewers, rulesets on `.github/workflows/**` and the OIDC subject format. Read them with `gh api` GETs (§ 8) before a severity rests on them. A 403 or 404 means unreadable, not absent.

**No-network mode (`gh api` never called).** An offline audit, a missing `gh` login or a read-only rule on the target still runs every grep and the offline lanes: zizmor `--offline`, actionlint, and `ci-graph.py`, which is offline by default (`--required` without `--online` prints `NOT-RUN OFFLINE(…)` and exits 2, which means required-ness unknown, never "not required"). What only the API can answer is named and never assumed. § 8's settings pass and § 7's can-approve read become `blocked (offline: settings unread)`. CIP8 (immutable tag) and CIP10 (private, forking off) cannot apply, so a pin row stays `[report-flagged]` with the immutability link unproven, and fork classes are rated as on a public repo. A job with no `permissions:` block is graded write-capable, because the repo default is unread. The owner can export the settings once (`gh api … > DIR/<name>.json`), and `ci-graph.py --settings-dir=DIR` reads them with no token. Print `mode: offline (gh api not called)` in the output header and list the unread settings under PROVE.

## Scans for

Severity is **reach × capability**. *Reach* is who can start the job: anyone with an account (`pull_request_target`, `issue_comment`, `issues`, `discussion`, a fork PR), a write collaborator (`push`, `workflow_dispatch`), or maintainers only. *Capability* is what the job's token, secrets or OIDC role can do: push code or tags, publish or deploy, mint a prod cloud role, or read deploy secrets; comment and label only; or read-only with no secrets. Each default below assumes anyone-reach and a write-capable job. Drop one step for collaborator-only reach or a comment/label-only token. A read-only job with no secrets is Hardening unless it saves a cache that a privileged job restores (§ 5). A private repo with forking disabled moves fork classes to insider severity (CIP10).

| § | Class | OWASP CI/CD Top 10 | CWE | Default |
|---|---|---|---|---|
| 1 | Privileged trigger runs untrusted code | CICD-SEC-4 | CWE-829 | critical |
| 2 | Expression injection (every substitution form) | CICD-SEC-4 | CWE-94, CWE-78 | critical |
| 3 | AI agent fed untrusted text, holding tools or tokens | CICD-SEC-4 | CWE-77 | critical with shell + secrets, else high |
| 4 | Pinning × privilege | CICD-SEC-3, CICD-SEC-8 | CWE-829, CWE-494 | high in a privileged job; low first-party in a read-only one |
| 5 | Cache and artifact trust | CICD-SEC-9 | CWE-345 | high (critical feeding a publish) |
| 6 | Credentials and OIDC | CICD-SEC-6, CICD-SEC-2 | CWE-522, CWE-532, CWE-250 | medium–high |
| 7 | Gates an attacker can pass | CICD-SEC-1 | CWE-290, CWE-697 | high on an auth or deploy gate |
| 8 | Runners and repository settings | CICD-SEC-7, CICD-SEC-5 | CWE-668 | critical for a self-hosted runner on a public trigger |
| 9 | GitLab, CircleCI, Bitbucket, Azure, Jenkins | as the GitHub analogue | as above | as the GitHub analogue |

### 1. Privileged trigger runs untrusted code

Classes: CI-PWN-REQ(-REFS), CI-COMMENT-OPS, CI-LABEL-TOCTOU, CI-WF-RUN-ARTIFACT-EXEC, CI-DISPATCH-TOKEN-CHAIN, CI-PRT-* verdict changes.

```
BAD:   on: pull_request_target  →  checkout ref: ${{ github.event.pull_request.head.sha }}  →  run: npm ci && npm test
       on: issue_comment (no author check)  →  checkout ref: refs/pull/${{ github.event.issue.number }}/head  →  run: ./deploy.sh
       on: workflow_run  →  download-artifact from the PR run  →  run: bash ./post.sh   ·   types: [labeled] then checkout head.ref
GOOD:  build and test on pull_request (fork PRs get a read-only token and no secrets); a privileged follow-up job reads
       the result as data only — a number checked against ^[0-9]+$ in $RUNNER_TEMP, never a script, never `uses: ./`
       comment-ops: if: contains(fromJSON('["OWNER","MEMBER","COLLABORATOR"]'), github.event.comment.author_association)
```
Grep 1a lists every way PR code reaches the runner in a privileged-trigger file: head/merge refs, `refs/pull/`, the head repository, `gh pr checkout`, `git fetch … pull/` and `allow-unsafe-pr-checkout: true`. **Read the code:** Does a later step execute the checked-out tree (install, build, test, `make`, `./script`, `uses: ./`)? Which `actions/checkout` does it resolve to? v7.0.0, and the 2026-07-20 backports v6.1.0 / v5.1.0 / v4.4.0 / v3.7.0 / v2.8.0, refuse a fork-PR ref under `pull_request_target` / `workflow_run` unless `allow-unsafe-pr-checkout: true` (CIP6). A floating `@v4` now gets the block; an older SHA pin keeps the hole. The block never covers `issue_comment`, same-repo PR branches, `gh pr checkout` or `git fetch`. Grep 1b lists comment-triggered files with no `author_association` or permission check. Grep 1c lists `labeled` gates, artifact downloads and dispatch chains (`actions: write` → `gh workflow run` → a privileged workflow). **Finding:** an untrusted actor can start the job, their content executes, and the job holds a capability. **Severity:** critical; high when the only capability is commenting or labelling. **PROOF:** re-detect. Grep 1 shows no PR-code sink in a privileged-trigger file. poutine `untrusted_checkout_exec` and zizmor `dangerous-triggers` are clean on the file. `ci-graph.py . --diff-guard=<base>` is clean outside the job.

### 2. Expression injection

Classes: CI-INJ, CI-ENV-INJECT, CI-COMPOSITE-INJECT, CI-REUSABLE-INPUT, CI-DISPATCH-INJECT, CI-MATRIX-TAINT, CI-OBFUSCATED-INJECT.

```
BAD:   run: echo "${{ github.event.issue.title }}"   ·   ${{ github.event['comment'].body }}   ·   ${{ format('{0}', github.event.issue.title) }}
       env: { T: ${{ github.event.issue.title }} } run: echo "${{ env.T }}"          # env. re-expanded into the script
       run: echo "X=$T" >> "$GITHUB_ENV"                                             # tainted → every later step's environment
       composite action.yml run: echo ${{ inputs.who }}  ←  caller with: who: ${{ github.event.issue.title }}
       matrix: ${{ fromJSON(needs.plan.outputs.files) }} → run: wc -l ${{ matrix.f }}  # file names are attacker-chosen
GOOD:  env: { TITLE: ${{ github.event.issue.title }} }  run: printf '%s\n' "$TITLE"
       inputs of type boolean / number / choice; GITHUB_ENV written only with constants, SHAs or integers
```
Grep 2a prints **each** tainted expression on its own line, so an integer beside a title no longer hides it. It covers the bracket form, `format()`, `toJSON()`, `github.event.inputs`, `env.`, `matrix.`, and step and job outputs. Its filter drops integer, enum, boolean and pure-comparison expressions (CIP1). Grep 2b lists `GITHUB_ENV` / `GITHUB_PATH` / `GITHUB_OUTPUT` writes and loader variables (`NODE_OPTIONS`, `LD_PRELOAD`, `BASH_ENV`) set from an expression. Grep 2c lists composite actions, reusable workflows, local `uses: ./` and matrices built from outputs. **Read the code:** Is the expression inside `run:`, a github-script `script:`, or a composite `run:` (code), or inside `with:` / `env:` (data, CIP3, CIP4)? Trace `env.X`, `steps.*.outputs` and `needs.*.outputs` back to their definition. A literal, a SHA or `github.repository_owner` is not a source. For `inputs.*`, read the input's `type:` and who can dispatch or call it. **Finding:** attacker-controlled text is substituted into a script, or written to `GITHUB_ENV` / `PATH`. **Severity:** critical on anyone-reach with a write token or secrets; high for comment/label-only or collaborator-only reach (`workflow_dispatch`); medium for a reusable input every caller passes as a constant. **PROOF:** re-detect. Grep 2a / 2b show no tainted expression in a script position. zizmor `template-injection` and `github-env`, and octoscan `expression-injection` and `dangerous-write`, are clean on every file.

### 3. AI agent fed untrusted text

Class: CI-AI-AGENT-PROMPT-INJECT. No offline tool flags it: zizmor treats `with:` as data, and octoscan hits it only incidentally.

```
BAD:   on: issues · uses: <agent-action>@v1 · with: { prompt: "Triage: ${{ github.event.issue.body }}", claude_args: --allowedTools "Bash(*)",
       allowed_non_write_users: "*" } · permissions: { contents: write, pull-requests: write } · secrets in env
GOOD:  trigger restricted to write-access users (the action's default — keep it); read-only token; no shell or git-push tools;
       the agent's output posted as a comment, never executed by a later step
```
Grep 3 lists agent steps, agent CLIs driven from `run:`, tool allow-lists and user allow-lists. **Read the code:** (1) Can a non-collaborator start the job (`issues`, `issue_comment`, `pull_request_target`, `discussion`), or does `allowed_non_write_users` / `allow-users` widen it? (2) Does untrusted text reach the prompt, or can the agent read it through `gh` or an MCP tool? (3) What can the agent do: shell (`Bash(*)`, `--yolo`, `--dangerously-skip-permissions`), push, comment; and which token and secrets sit in its environment? (4) Does a later step execute the agent's output? Read the input names on the **pinned** version of the action before relying on a default. **Finding:** untrusted reach × untrusted text × a capability. **Severity:** critical with shell tools and secrets or a write token; high otherwise. Hand the model-side judgment to `@llm-security-reviewer` § "LLM01 Prompt Injection (direct, indirect, cross-modal)". **PROOF:** re-read. The trigger, the allow-list and the token scope each show the restriction at `<file:line>`.

### 4. Pinning × privilege

Classes: CI-PIN, CI-IMAGE-UNPINNED, CI-REUSABLE-UNPINNED, CI-COMPOSITE-INNER-UNPINNED, CI-UNPINNED-TOOL, CI-KNOWN-VULN-ACTION, CI-IMPOSTOR-COMMIT, CI-REF-CONFUSION, CI-TYPOSQUAT, CI-ARCHIVED-ACTION, CI-DEPENDABOT-EXEC.

```
BAD:   permissions: { packages: write, id-token: write } · uses: docker/build-push-action@v6 · uses: org/wf/.github/workflows/x.yml@main
       container: node:22 · uses: docker://alpine:3.20 · run: curl -fsSL https://x/install.sh | sh · npx tool@latest
GOOD:  uses: docker/build-push-action@<40-hex sha>  # v6.x.y  + dependabot package-ecosystem: github-actions and docker
       container: node:22@sha256:<digest> · tools at an exact version with a checksum
```
Grep 4a is the graded list. `ci-graph.py --check=pin-priv` joins every mutable `uses:` to its job's effective permissions, secrets and environment. It prints `PIN×PRIV job=… uses=… perms=…` and tags `actions/*` and `github/*` as first-party. Grep 4b is the full ledger of unpinned `uses:`. Grep 4c lists images with no digest in `container:`, `services:` and `docker://`. A flow-map `container: { image: x }` is a read. 4d lists tools fetched at a moving version. 4e lists actions with a published compromise (tj-actions/changed-files, reviewdog/action-setup, trivy-action, actions-cool) or an archived upstream. 4f lists Dependabot executing external code, and the absence of a bot that keeps pins fresh. **Read the code:** Is the tag an exact release with `immutable: true` (`gh api repos/O/R/releases/tags/<tag> --jq .immutable`, CIP8)? Is the SHA reachable from the upstream's branches and tags, or only from a fork (impostor)? Does a SHA-pinned composite action use `@main` inside it (`gh api repos/O/R/contents/<path>/action.yml?ref=<sha>`)? **Finding:** a mutable reference executes inside a job with a capability. **Severity:** high for a third-party mutable reference in a job with write scopes, secrets, `environment:` or `id-token`. High–critical for a known-compromised range. Medium for an image without a digest in a privileged job. Low for first-party actions, or any pin in a read-only job with no secrets. A SHA pin with no bot is rot (CIP9), reported once per repo. **PROOF:** re-detect. `ci-graph.py --check=pin-priv` prints no row for the job, `pinact run --check` exits 0, and grep 4f shows a bot covering `github-actions` and `docker`.

### 5. Cache and artifact trust

Classes: CI-CACHE-POISON, CI-CACHE-RELEASE, CI-ARTIFACT-SECRET-LEAK.

```
BAD:   on: pull_request_target · setup-node with cache: npm        # saves into the default-branch cache scope
       on: push tags v* · restores any cache → npm publish          # restores what an untrusted job saved
       upload-artifact with path: .                                 # .git/config with the token, .env
GOOD:  untrusted jobs: actions/cache/restore only, lookup-only, or setup-gradle cache-read-only: true
       release jobs: no cache restore (or a key prefix no untrusted job can write) · upload only the build output directory
```
A run restores caches from its own ref, the default branch and the PR base. `pull_request_target`, `workflow_run`, `issue_comment` and `schedule` run in the default-branch scope (`ci-platform-semantics.md` row C6), so a cache they save is restorable by every release job. Saving happens in a post step with a runner-internal token, which `permissions: contents: read` does not stop. Grep 5a lists cache writers in outsider-startable files, 5b cache readers in release and tag workflows, and 5c workspace or hidden-file uploads. **Read the code:** Is the 5a writer reached by an outsider, and does a 5b job restore the same key family? Is the artifact the whole tree, with `persist-credentials` left on? **Finding:** an outsider-written cache reaches a publish or deploy job; or an artifact carries a credential, which on a public repo anyone with read access can download. **Severity:** critical when the cache feeds a publish; high otherwise; high for a credential artifact. **PROOF:** re-detect. Greps 5a–5c are clean, and zizmor `cache-poisoning` and `artipacked` are clean. A read-only cache inventory: `gh cache list --json key,ref,createdAt` shows no key on the default branch created by a PR-triggered run.

### 6. Credentials and OIDC

Classes: CI-SECRETS-ALL, CI-UNREDACTED, CI-SECRETS-NO-ENV, CI-REUSABLE-INHERIT, CI-OIDC-WIDE, CI-TRUSTED-PUB-MISSING, persisted checkout credentials, secrets on argv or in logs.

```
BAD:   ${{ toJSON(secrets) }} · ${{ fromJSON(secrets.SA).private_key }} (derived, not masked) · secrets: inherit to @main
       permissions: { id-token: write } at workflow level · NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }} · --password ${{ secrets.X }}
       actions/checkout with no persist-credentials: false · Azure checkout persistCredentials: true
GOOD:  one named secret per step, from an environment with reviewers · id-token: write on the publish job only
       trusted publishing (OIDC) bound to the workflow file and environment · docker/login-action with password: from env
```
Grep 6a lists the whole secrets context, derived values and `inherit`. 6b lists long-lived publish and cloud tokens (it skips `secrets.GITHUB_TOKEN`). 6c lists secrets on argv, echoed or traced. 6d lists write scopes in any form, including flow-map and `write-all`, plus files with no `permissions:` block. 6e lists workflow-level `id-token: write`. 6f lists checkouts that keep their token in `.git/config`. Checkout ≥ v6.0.0 stores it under `$RUNNER_TEMP`, which zizmor rates lower. **Read the code:** Which job runs untrusted or third-party code while the secret or OIDC permission is in scope? Code in the job can read the token from runner memory. With no `permissions:` block, is the repo default read or write (`gh api repos/O/R/actions/permissions/workflow`)? Does trusted publishing exist for this registry? **Finding:** a credential is exposed beyond the step that needs it, to a party the job runs. **Severity:** high for workflow-level `id-token` or secrets in a job that runs dependencies or third-party code; medium for a long-lived token where OIDC exists (acceptable at ≤ 90 days and environment-scoped where unsupported); medium for no `permissions:` with a write default. Hand the leaked value to `secret-scan-method` to rotate first. **PROOF:** re-detect. Greps 6a–6f are clean for the job. zizmor `excessive-permissions`, `overprovisioned-secrets`, `unredacted-secrets`, `secrets-inherit` and `artipacked` are clean.

### 7. Gates an attacker can pass

Classes: CI-BOT-SPOOF, CI-AUTOMERGE, CI-UNSOUND-CONTAINS, CI-UNSOUND-TERNARY, CI-IF-ALWAYS-TRUE.

```
BAD:   if: github.actor == 'dependabot[bot]' → gh pr merge --auto      # actor = whoever fired the latest event
       if: contains('refs/heads/main refs/heads/prod', github.head_ref) # substring: a branch named "ain" passes
       if: |  ${{ … }}   · if: ${{ a }} && ${{ b }}                     # a non-empty string is always true
GOOD:  if: github.event.pull_request.user.login == 'dependabot[bot]' && github.event.pull_request.head.repo.full_name == github.repository
       contains(fromJSON('["refs/heads/main","refs/heads/prod"]'), github.ref) · one bare expression per if:
```
Grep 7 lists actor checks, string `contains()`, block-scalar and fenced `if:`, and workflows that merge or approve. **Read the code:** Does the gate guard a privileged action (merge, deploy, secrets)? Is "Allow GitHub Actions to create and approve pull requests" on (`gh api repos/O/R/actions/permissions/workflow --jq .can_approve_pull_request_reviews`)? `github.repository_owner == 'org'` stops runs in forks of the workflow, not fork PRs. **Finding:** the gate passes for an actor it means to exclude, in front of a capability. **Severity:** high on an auth or deploy gate (CIP11); low elsewhere. **PROOF:** re-detect. zizmor `bot-conditions`, `unsound-contains` and `unsound-condition`, and actionlint `if-cond`, are clean on the file.

### 8. Runners and repository settings

Classes: CI-SELFHOSTED-UNTRUSTED, CI-SELFHOSTED-PERSIST, CI-ROGUE-WORKFLOW, CI-FORK-GATE-WEAK, settings.

Grep 8 lists non-GitHub-hosted `runs-on` labels, exfiltration shapes (secrets posted with `curl`, webhook collectors, base64 of secrets), `discussion` triggers, and the last 40 commits that touched workflows. **Read the code:** Is a self-hosted runner reachable from a fork PR, a comment or a discussion? Is it ephemeral (JIT or a scale set)? Is the repo public (`gh api repos/O/R --jq '{private,visibility,allow_forking}'`)? Then do a read-only settings pass: `actions/permissions` (allowed actions, `sha_pinning_required`), `actions/permissions/workflow`, `actions/permissions/fork-pr-contributor-approval`, `environments` (reviewers, branch policies, admin bypass), `rulesets` (code-owner review on `.github/workflows/**`), `actions/runners`, and `actions/oidc/customization/sub`. A workflow committed by an unusual author, or one that posts secrets anywhere, is a stop: report it at once and hand rotation to `secret-scan-method`. **Severity:** critical for a self-hosted runner on an anyone-reach trigger in a public repo; medium when fork approval is "all outside contributors"; high for no protection on `.github/workflows/**` with secrets of publish scope. **PROOF:** a settings read. Each verdict cites the `gh api` line it rests on.

### 9. Other platforms

Grep 9a–9e; the tools are near-blind here, so grep + read is the lane of record.
- **GitLab** (9a). Flag: `eval` / `sh -c` / an unquoted `$CI_MERGE_REQUEST_*` / `$CI_COMMIT_*` (expanded by the shell, so quoted is data); `$[[ inputs.x ]]` substituted with no `options:` / `regex:`; `include: project` with no 40-hex `ref:`; `remote` with no `integrity:`; a component `@main` / `@~latest`; `image:` with no digest; `cache: unprotect: true` and `fallback_keys`; `artifacts: public: true`, or no `access:` on a public project; `trigger: forward: pipeline_variables: true`. A `project:` under `trigger:` is a downstream, not an include.
- **CircleCI** (9b). Flag: `<< pipeline.git.branch >>` / `<< parameters.x >>` in `command:` (substituted into config); orbs at `@volatile`, `@dev:*` or a major only; images with no digest. The fork-PR secrets setting is a settings read.
- **Bitbucket** (9c). Flag: `pipe: …:1` / `:latest`; `image:` with no digest; `pull-requests:` pipelines that use secured variables; an echoed secret.
- **Azure** (9d). Flag: `##vso[task.setvariable|prependpath]` fed from `$(System.PullRequest.*)` / `$(Build.SourceVersionMessage)`; `$(macro)` of that text in `script:` (substituted first); `persistCredentials: true`; `resources.repositories` with no tag or SHA `ref:`; container images with no digest. `env:` + `"$VAR"` is data.
- **Jenkins** (9e). Flag: a double-quoted `sh "…${env.CHANGE_TITLE}…"` / `${params.X}` (Groovy interpolates first); `"${TOKEN}"` inside `withCredentials` (the secret lands on argv); `@Library('x@master')` (global libraries run outside the sandbox); `trustEverybody` / `TrustContributors` in JCasC; `agent any` with executors on the controller.

**Severity** follows the GitHub analogue: injection and untrusted-code rows are critical with deploy credentials in scope; pinning, images and public artifacts are medium; variable and runner scope are high. **PROOF:** re-detect with the platform's 9x grep, plus the settings read the row names.

## Verification

Every critical or high row passes [`finding-verification.md`](../../../../snippets/finding-verification.md) before it is confirmed. Restate the claim with CI values: *an actor who can [open a fork PR / comment / open an issue / push a branch] fires [trigger], whose job at [file:line] executes [their text or code] while holding [token scope / secret / OIDC role], and gains [push / publish / deploy / secret]*. Then apply:
- **§ 4 CI precedents CIP1–CIP11.** These are settled verdicts: integer contexts, the SHA-by-sink rule, `with:` as data, `env:` indirection, `pull_request_target` with only `uses:` steps, the checkout v7 block and its backports, the post-2025-12-08 default-branch rule, immutable tags, the SHA pin with no bot, a private repo with no forks, and sound bot checks. A precedent applies only when its condition is shown at `<file:line>` or by a `gh api` line.
- **The job graph.** `ci-graph.py --check=pin-priv` gives each job's effective permissions, secrets and environment as structural facts (`proof-oracles.md` § DevOps, "Graph assertion (`ci-graph.py`)"). The verifier still reads the job.
- **Platform facts and dates.** [`ci-platform-semantics.md`](../../../../snippets/ci-platform-semantics.md) rows C3 (environment protection) and C6 (cache scope), and § "Dated changes that flip verdicts". A verdict that rests on a platform behaviour names the row.
- **Fix guard.** A fix that changes `on:`, `if:`, `needs:`, `concurrency:`, `permissions:` or `environment:` outside the finding's job is rejected. `ci-graph.py --diff-guard=<base>` proves it.

## Output

```
ci-security-scan — <repo>@<sha>   lanes: github-actions (14 workflows, 1 composite), gitlab-ci; circleci, bitbucket, azure, jenkins absent
Tool ledger
  zizmor 1.30.1   RAN  exit 14 · regular + auditor · 15 of 15 files parsed · 31 hits → 9 merged, 6 FP (workflow_run)
  poutine 1.1.6   RAN  --fail-on-violation · exit 10 · 4 hits → 3 merged
  octoscan 0.1.7  NOT-INSTALLED  linux/amd64 only — `octoscan scan <file> --oneline` per file in a debian container
  ci-graph.py     RAN  --check=pin-priv · exit 1 · 7 PIN×PRIV rows

Findings: 3

1. .github/workflows/ci-comment.yml:15,16                          [report-with-fix]  critical
   §1 comment-ops — on: issue_comment, no author_association check; checks out refs/pull/<n>/head, then ./deploy.sh
   on a self-hosted runner with deployments: write. Reach: any account. checkout v7 does not cover issue_comment (CIP6).
   Fix: gate on author_association ∈ OWNER/MEMBER/COLLABORATOR; run PR code on pull_request with a read-only token. CICD-SEC-4 · CWE-829
2. .github/workflows/triage.yml:13                                 [report-with-fix]  critical
   §2 injection — ${{ github.event.issue.title }} inside run: (issues: opened, issues: write).
   Fix: env: { TITLE: … } and "$TITLE". CICD-SEC-4 · CWE-94
3. .github/workflows/publish.yml:17                                [report-flagged]   high
   §4 pin × privilege — pnpm/action-setup@v4 in a job with contents: write, id-token: write and NPM_TOKEN (ci-graph PIN×PRIV).
   Unproven link: whether the v4 tag is an immutable release (gh api unreadable: 404). Fix: SHA pin + dependabot github-actions. CICD-SEC-3 · CWE-829

Class coverage:
  §1 privileged trigger × untrusted code   checked (6 hits → 1 finding; 2 refuted by CIP6, 1 by CIP5)
  §2 expression injection                  checked (21 hits → 1 finding; 9 with: data, 6 env-indirected, 4 constants)
  §3 AI agents                             N/A (no agent action or CLI in any workflow)
  §4 pinning × privilege                   checked (7 PIN×PRIV rows → 1 finding, 6 first-party low, grouped)
  §5 cache and artifact trust              checked (2 hits → 0 findings: no release job restores a cache)
  §6 credentials and OIDC                  checked (9 hits → 0 findings; 6 checkouts persist credentials → Hardening)
  §7 gates                                 checked (0 hits)
  §8 runners and settings                  blocked (gh api 403 on actions/permissions — settings unread)
  §9 other platforms                       checked gitlab (3 hits → 0); circleci, bitbucket, azure, jenkins N/A (no files)
```

`[report-with-fix]`: the trace from trigger to capability is complete and the fix is concrete. `[report-flagged]`: one link is unproven (a settings read, a pinned action's inner `uses:`, the immutability of a tag), and the row names it. The coverage block lists **all nine** classes on every run: `checked (k hits → m findings)` only when the grep ran on a present platform; `N/A (<reason>)` only when grep 0 proves the surface absent; `blocked (<reason>)` when a grep, a tool or a settings read could not run.

**Bulk triage** for a 3,000-hit run (a monorepo with hundreds of workflows). Group before reading:
- Group grep 2a by expression (`cut -d: -f3- | sort | uniq -c | sort -rn`). Close an expression once, with a cited reason, for every occurrence: a workflow-level `env:` literal, a literal matrix, `github.repository_owner`.
- Group grep 4b by `action@ref`. Grade it through 4a's rows only. Rows with no privileged job close as one "unpinned in read-only jobs → low" line per action, with one fix (`pinact run`).
- Group grep 6f per workflow.

Count every class in the coverage line (`3,112 hits: 41 read, 2,904 grouped into 37 expressions, 167 first-party pins in read-only jobs`). Nothing in a privileged-trigger file (grep 0's second list) is ever closed in bulk.

## False positives / gotchas

- **Measured** on a seeded six-platform sample (15 workflows, 1 composite action, a decoy beside each class), 2026-10-10. Grep 2a keeps all 10 injection seeds, including the bracket form, `format()`, `toJSON()`, `env.` re-expansion, a composite input and a matrix from outputs; the old `iac-scan` grep missed 5. Grep 1a finds 8 of 8 PR-code checkouts (the old ref grep found 2). Grep 6d finds 15 write-scope lines, including a flow-map block and the scopes the old grep never listed (it found 10), plus the 2 files with no `permissions:` block. Grep 4c finds 3 of 3 undigested images and 0 of 2 digest decoys.
- **Measured** on `benchmarks/fixtures/vuln-fullstack`. Both CI seeds surface, one through 2a and one through 1a, plus 5a `cache: npm` under `pull_request_target`. That seed's `actions/checkout@v4` now resolves to v4.4.0, which refuses the fork-PR ref (CIP6). The same-repo-branch path and the cache write keep the finding.
- **Measured** on a real application monorepo (one 500-line workflow, all actions SHA-pinned, 2026-10). 2a went 12 → 9 after the comparison filter; all 9 are constants or a literal matrix, closed by the read. 4a printed 0 rows (`ci-graph` exit 0). 4c found 3 service images by tag. 4d found 1 `bash <(curl …)` installer pinned by URL tag. 6f found 6 checkouts. Two noise fixes held there: cache writers keyed on outsider-startable triggers only (8 → 0), and 6b skipping `secrets.GITHUB_TOKEN` (1 → 0).
- **Measured offline** on a real NestJS + React monorepo (2026-10-15, no network): `ci-graph.py --check=pin-priv` ran with 0 rows; § 8, CIP8 and CIP10 were `blocked (offline)`. The two CI rows that rested on settings (a `pull-requests: write` token persisted during dependency code, an image push on same-repo branches) stayed Unconfirmed with the `gh api` read that settles each.
- **`tags:` and `project:` collide.** docker/metadata-action has a `tags:` input, and GitLab `trigger:` has a `project:` key. Confirm 5b's match is under `on:`, and 9a's is under `include:`.
- **YAML 1.1 reads `on:` as `true`** (`precedents/devops.md` § 44). Any YAML reader other than `ci-graph.py` must remap it, or it sees no triggers.
- **`workflow_run` alone is not a finding.** zizmor flags every one. The signal is an artifact, cache or head checkout in it (CIP5).

## When to run

- On any diff touching a CI definition on any of the six platforms, a composite action, `dependabot.yml` or a Renovate config. `/security-audit` dispatches it on that signal, and on every whole-repo run that holds a CI file. `iac-scan` § 5 points here.
- Before making a repo public (self-hosted runners, fork reach), after adding an AI agent to CI, and after an upstream action's compromise is announced (grep 4e).

## Halt conditions

- Do not report a critical or high row as confirmed until a verifier other than the run that found it has passed it through [`finding-verification.md`](../../../../snippets/finding-verification.md). That protocol is security's reading of [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/security-audit` this happens in Phase 4. Run standalone, it applies the protocol as a separate second pass, tags those rows `self-verified`, and lists the rest as Unconfirmed, Hardening or Refuted — never drops them.
- Halt on a finding without `<file:line>`, the trigger and who can fire it, the sink line, the job's capability, the fix and a severity.
- Halt on a ledger row marked RAN with no parsed-file count, or on a clean result from a tool in a known false-clean mode. That row is NOT-RUN.
- Do not send events, open PRs, dispatch workflows, run an offensive tool or call a write API against any repository. Settings are `gh api` GETs on a repo the user owns.
- Do not print, decode or rotate a secret value; hand it to `secret-scan-method`.

## Related

- `/security-audit`: dispatches here and takes the coverage block as its "CI pipelines" ledger row. `/security-fix` closes the findings.
- `iac-scan` § 5: the dispatch line and grep 6 candidates. `secret-scan-method`: leaked values. `@llm-security-reviewer` § "LLM01 Prompt Injection (direct, indirect, cross-modal)": the model side of § 3.
- [`ci-platform-semantics.md`](../../../../snippets/ci-platform-semantics.md), `precedents/devops.md` § 41 and § 44 (tool and loader traps), and `.claude/scripts/ci-graph.py` (`--check=pin-priv`, `--diff-guard`).
- devops pack, when installed: `pipeline-integrity-scan` and `@ci-reviewer` for delivery integrity; `release-security` for signing and provenance. Without it, those claims are listed as not reviewed.
