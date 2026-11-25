---
name: gitlab-ci-authoring
description: "Writes and debugs .gitlab-ci.yml to house policy: pinned includes, rules:, protected variables, OIDC id_tokens. Use when editing .gitlab-ci.yml or a pipeline was not created. Not for a failing job on an MR (use mr-lifecycle); not for GitHub Actions (use github-workflow:actions-authoring)."
when_to_use: "write a gitlab ci pipeline, add CI to this repo, rules vs only except, duplicate pipelines, needs DAG, cache vs artifacts, OIDC to AWS from GitLab, id_tokens, protected variable, interruptible, why is my pipeline not running"
allowed-tools: Read, Grep, Glob, Edit(.gitlab-ci.yml), Edit(.gitlab/ci/**), Bash(glab ci lint *), Bash(glab ci lint), Bash(glab ci list *), Bash(git log *)
license: MIT
---

# gitlab-ci-authoring

Treat a pipeline file as production code that holds a credential. It runs on a machine you do not
own, with access to your registry and your cloud, and anyone who can push a branch can make it run.

## Step 1: read what exists

Read `.gitlab-ci.yml` and anything under `.gitlab/ci/`, then `git log --oneline -5 -- .gitlab-ci.yml`
and `glab ci list --per-page 5`. Without a checkout, ask the user to paste the file and the last few
pipeline results, and propose edits only to a file you have read.

## Pin every include

```yaml
include:
  - project: '<group>/ci-templates'
    file: '/templates/build.yml'
    ref: <40-char commit sha>          # vX.Y.Z
  - component: $CI_SERVER_FQDN/<group>/<component>/build@<40-char commit sha>
  - remote: 'https://example.com/ci/lint.yml'
    integrity: 'sha256-<base64 digest of the file>'
```

A branch is a mutable pointer, so whoever controls it controls your pipeline and its secrets. A tag
is only conventionally stable; a SHA is immutable, and is the only acceptable ref for a project you
do not control. Keep the human-readable version in a comment beside it. `include:remote` has no ref;
pin it with `integrity`, or prefer `project:` or `component:`. The same rule for GitHub Actions lives
in `github-workflow:actions-authoring`.

## `rules:`, and one pipeline per push

`only`/`except` is legacy; write `rules:`. Rules are evaluated top to bottom and the first match
wins, so the order is the logic. End a job's rules with an explicit `- when: never` so a reader does
not need to know the default.

Without `workflow:rules`, a push to a branch with an open MR can create two pipelines (a branch
pipeline and an MR pipeline) that race each other. Put this at the top of the file:

```yaml
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS && $CI_PIPELINE_SOURCE == "push"
      when: never
    - if: $CI_COMMIT_BRANCH
    - if: $CI_COMMIT_TAG
```

`rules:changes` is true on a new branch and on any pipeline without a push event (schedules,
triggers, the web UI), so it cannot gate an expensive job on its own there. On MR pipelines it
compares against the target branch; elsewhere set `rules:changes:compare_to` to a ref.

## `needs:`, artifacts and cache

- `needs: [build]` starts a job when `build` finishes rather than when its whole stage does;
  `needs: []` starts it at once. A job with `needs` downloads artifacts only from the jobs it
  needs; add `artifacts: false` inside a `needs` entry when it needs the ordering but not the files.
  Without `needs`, a job downloads artifacts from every job in earlier stages unless
  `dependencies: []` says otherwise.
- `cache` is for speed and may be missing; `artifacts` are outputs and must not be. A pipeline that
  is correct only with a warm cache is broken; test it cold.

## Variables and secrets

- **Protected** variables reach only pipelines on protected branches and tags. Mark every deploy
  credential protected; otherwise anyone who can push a branch can run a job that prints it. An MR
  pipeline from an unprotected source branch or a fork does not get protected variables, which is
  the point.
- **Masked** (or **masked and hidden**) keeps a value out of job logs. GitLab refuses to mask a
  value that does not meet its masking requirements. Masking is not secrecy: a script that sends
  the value somewhere, or transforms it (base64), is not stopped by it.

### OIDC instead of stored cloud keys

```yaml
deploy:
  id_tokens:
    AWS_ID_TOKEN:
      aud: <the audience the cloud's OIDC provider expects>
  variables:
    AWS_ROLE_ARN: arn:aws:iam::<account-id>:role/<deploy-role>
    AWS_WEB_IDENTITY_TOKEN_FILE: $CI_PROJECT_DIR/.aws-web-identity-token
  script:
    - printf '%s' "$AWS_ID_TOKEN" > "$AWS_WEB_IDENTITY_TOKEN_FILE"
    - aws sts get-caller-identity      # the SDK and CLI assume the role from the two variables
    - ./deploy.sh
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

GitLab's ID token carries the claims the cloud's trust policy conditions on. `sub` is
`project_path:<group>/<project>:ref_type:<branch|tag>:ref:<name>`; `ref_protected` is `"true"` on a
protected ref. Condition on the exact `sub`; on gitlab.com also pin `project_id` and `ref_protected`.
Self-managed supports only `sub` and `aud`. Never trust the group alone. Decode a real token from a
job to confirm the claim values before writing the policy.
The role and trust-policy side belongs to `terraform-aws:aws-iam-boundaries`.

## Superseded pipelines

```yaml
workflow:
  auto_cancel:
    on_new_commit: interruptible
default:
  interruptible: true
```

Merge this into the same `workflow:` block as the rules above. With auto-cancel on, a new push cancels the older pipeline for the same ref. The default mode
(`conservative`) cancels nothing once any job with `interruptible: false` has started; `interruptible`
cancels only the interruptible jobs. Set `interruptible: false` on anything that deploys or migrates,
so it is never killed halfway.

## When the bigger mechanisms earn their place

- `extends:` for three or more jobs sharing a shape; `!reference` to reuse one key's value. Both
  compose better than YAML anchors, which do not work across included files.
- Child pipelines (`trigger:include:`) for a monorepo whose components have real pipelines of their
  own, not for two jobs.
- Components for one pipeline shape across repositories; version and pin them as above.
- `parallel:matrix:` for a version or platform matrix; count the jobs it creates.

## Verify

```bash
glab ci lint
glab ci lint --dry-run --ref <branch>
```

`glab ci lint` validates against the server, which resolves every `include:`. `--dry-run` simulates
creating a pipeline on that ref, so it also shows whether `workflow:rules` lets one be created.

## When a pipeline misbehaves

- **No pipeline appeared.** `workflow:rules` or a YAML error; the two look identical from the MR.
  Run the lint above.
- **A job is missing.** Its `rules:` did not match; read them top to bottom for that pipeline source.
- **A job is pending forever.** No online runner has all of its `tags:`. It sits pending instead of
  failing, so check the runner before the job.
- **A job failed.** That is an MR problem: use `mr-lifecycle` to read the log.
