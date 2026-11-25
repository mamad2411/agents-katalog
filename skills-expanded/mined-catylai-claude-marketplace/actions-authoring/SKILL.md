---
name: actions-authoring
description: "Writes, reviews and debugs GitHub Actions workflows to house policy: pinned actions, least-privilege tokens, safe fork triggers, OIDC. Use when editing .github/workflows/ or a run fails. Not for GitLab CI (use gitlab-workflow:gitlab-ci-authoring); not for a PR's failing checks (use pr-lifecycle)."
when_to_use: "write a GitHub Actions workflow, add CI, pin actions to a SHA, workflow permissions, pull_request_target, OIDC from Actions, why is my workflow failing"
allowed-tools: Read, Grep, Glob, Edit(.github/**), Bash(gh run list *), Bash(gh run view *), Bash(gh run watch *), Bash(actionlint *)
license: MIT
---

# actions-authoring

Treat a workflow file as production code that holds a credential. It runs on a machine you do not
own, with a token that can write to the repository, and outside contributors can trigger it. The
rules below are the house policy. `code-review-core`'s `deps.sh` detector enforces the pinning rule
as written here, so a change to that rule needs a matching change there.

To add Claude itself to a repository's CI, use Claude Code's built-in `/install-github-app` rather
than hand-writing that workflow.

## Baseline

```yaml
name: ci
on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read            # workflow-level floor; jobs ask for more only when they need it

concurrency:                # a PR shares a group per branch; each push to main gets its own
  group: ${{ github.workflow }}-${{ github.event_name == 'pull_request' && github.ref || github.sha }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}

jobs:
  test:
    name: test
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@<40-char-sha>  # vX.Y.Z
      - uses: actions/setup-python@<40-char-sha>  # vX.Y.Z
        with:
          python-version-file: .python-version
      - run: pip install -e '.[test]'
      - run: pytest -q
```

Workflows live directly in `.github/workflows/`; a file in a subdirectory never runs. Give every job
a `timeout-minutes`, since the default is six hours of a held runner, and give every workflow an
explicit `permissions` block.

## Pin every remote `uses:` to a full commit SHA

A tag such as `@v4` is a pointer in someone else's repository, and anyone with write access there
can move it. The next run then executes code nobody reviewed, with this job's secrets. Pin to the
40-character commit SHA and keep the version in a trailing comment:

```yaml
- uses: some-org/some-action@<40-char-sha>  # vX.Y.Z
- uses: some-org/shared/.github/workflows/build.yml@<40-char-sha>  # vX.Y.Z   (reusable workflow)
```

The same applies to actions under `actions/` and `github/`, and to remote reusable workflows. Two
cases are exempt. A local action or workflow referenced by path (`./.github/actions/setup`) is pinned
by your own commit. A `docker://` image has no git ref; pin it by digest instead.

Resolve the SHA for the exact version you reviewed. Never copy one from an example:

```bash
gh api repos/<owner>/<repo>/commits/<tag> --jq '.sha'
```

The `commits/<ref>` endpoint always returns the commit. `git/ref/tags/<tag>` returns the tag
*object* for an annotated tag, which is the wrong SHA to pin. To keep pins current, enable Dependabot
with the `github-actions` ecosystem in `.github/dependabot.yml`: it bumps the SHA and the comment
together and links the release notes.

## Permissions

With no `permissions` block, the `GITHUB_TOKEN` gets whatever default the repository or organisation
is set to, and that can change without the file changing. Declare it. A job-level block **replaces**
the workflow-level one, and any scope it leaves out is set to `none`:

```yaml
permissions: {}                  # strictest floor: every job lists what it needs
jobs:
  comment:
    permissions:
      contents: read
      pull-requests: write       # only this job can comment
  release:
    permissions:
      contents: write            # pushes a tag
      id-token: write            # mints an OIDC token
```

Put jobs that run untrusted code in a different job from any write scope. A job that builds a
fork's code while holding `contents: write` is one malicious install script away from a push to
your repository.

## `pull_request` vs `pull_request_target`

| Trigger | Workflow file and code | Token on a fork PR | Secrets on a fork PR |
| --- | --- | --- | --- |
| `pull_request` | the PR's merge commit, so the PR can change the workflow | read-only | none |
| `pull_request_target` | the base branch | write, as configured | **available** |

`pull_request_target` exists so a workflow can label or comment on a fork's PR. Because it holds
secrets, a `pull_request_target` job works only with PR metadata (number, labels, title passed
through `env:`). Keep it from checking out, installing, building or running anything from the PR
head, including `ref: ${{ github.event.pull_request.head.sha }}` and actions that read the PR's
files. A single `postinstall` script is enough to exfiltrate every secret.

When fork code has to be built *and* a result posted, split the work. A `pull_request` workflow
builds with no secrets and uploads an artifact. A separate `workflow_run` workflow with the write
scope downloads that artifact and posts it. Treat the artifact as untrusted input: parse it as data,
never execute it, and look up the PR number through the API rather than trusting a number the
artifact contains.

Pass event data to a shell through `env:` and quote it as `"$TITLE"`. A `${{ github.event.* }}`
expression inside `run:` is substituted before the shell parses the line, so a PR title containing
`$(...)` would run as a command.

## Secrets and cloud credentials

Prefer `secrets.GITHUB_TOKEN`, which is scoped per job and expires with it, over a personal access
token for anything inside the repository. For cloud access, use OIDC in place of a stored key: the
job needs `id-token: write`, and the cloud-side trust policy decides which repository, branch or
environment may assume the role.

```yaml
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: aws-actions/configure-aws-credentials@<40-char-sha>  # vX.Y.Z
        with:
          role-to-assume: arn:aws:iam::<account-id>:role/<ci-role>
          aws-region: <region>
```

For the AWS trust policy (the `sub` and `aud` conditions that make this safe), follow
`terraform-aws:aws-iam-boundaries`. Log masking catches a secret only when it appears verbatim, so a
base64-encoded or line-split secret prints in clear text. Fork PRs receive no secrets, so a step that
quietly skips when a secret is empty behaves differently for contributors than for you.

## Concurrency

A `concurrency` group runs one job or workflow at a time. By default (`queue: single`) it also holds
at most one pending run: a newer run cancels the pending one and takes its place, even with
`cancel-in-progress: false`. `cancel-in-progress: true` cancels the running one as well. The
consequences:

- Group pull requests on `${{ github.workflow }}-${{ github.ref }}` so different branches do not
  cancel each other, and cancel in-progress runs there: only the newest commit matters.
- Keep pushes to `main` out of a shared group, because a pending run would be replaced and that
  commit would never get a result. The baseline groups a push by `github.sha`, so each push has its
  own group.
- For deployments that must run one at a time and in order, add `queue: max`: up to 100 runs wait
  instead of replacing each other, and further runs are cancelled once it is full. It cannot be
  combined with `cancel-in-progress: true`. Leave the default when only the newest deploy matters.

```yaml
concurrency:
  group: production-deploy
  queue: max
```

`queue` is recent; check that your GitHub Enterprise Server version documents it before relying on it.

## Required checks

Branch protection matches a required check by the name the job reports: its `name:`, or
`name (a, b)` for a matrix cell. Renaming a job silently orphans the requirement. For a matrix,
require one aggregate job instead (see [references/patterns.md](references/patterns.md)). Read what
is required before renaming anything, checking both classic protection and rulesets:

```bash
gh api "repos/{owner}/{repo}/branches/main/protection/required_status_checks" --jq '.contexts'
gh api "repos/{owner}/{repo}/rules/branches/main" --jq '.[] | select(.type == "required_status_checks")'
```

Caching, matrices, reusable workflows and composite actions each have a cost; the trade-offs and
worked examples are in [references/patterns.md](references/patterns.md).

## Debugging a run

```bash
gh run list --branch <branch> --limit 5
gh run view <run-id> --log-failed             # only the failing steps
gh run view <run-id> --job <job-id> --log     # one job's full log
gh run rerun <run-id> --failed                # only with a stated reason to suspect flakiness
```

When a workflow did not run at all, check in this order:

1. The YAML did not parse.
2. The `on:` filters (`branches`, `paths`, types) excluded the event.
3. For `schedule` and `workflow_dispatch`, the file is not on the default branch.

For step tracing, set the repository variable `ACTIONS_STEP_DEBUG=true`, re-run, then remove it,
since debug logs print more than you meant to keep.

## Verify

Before a workflow change is done, check it against this list:

- [ ] `actionlint .github/workflows/<file>.yml` passes. Without actionlint, at least confirm the file
      parses as YAML.
- [ ] Every remote `uses:` is `@<40-char-sha>  # vX.Y.Z`.
- [ ] A workflow-level `permissions` block exists, and each job grants only what it uses.
- [ ] No `pull_request_target` job touches PR-head code; no `${{ github.event.* }}` inside `run:`.
- [ ] Every job has `timeout-minutes`.
- [ ] Cloud auth uses OIDC.
- [ ] No required check's job name changed.

## Without gh

Writing and reviewing YAML needs only the files, or YAML pasted into the conversation. For run
history and logs without a shell, use the GitHub MCP server's `actions_list`, `actions_get` and
`get_job_logs`. If neither is available, ask the user to paste the failing step's log.
