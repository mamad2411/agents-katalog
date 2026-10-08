---
name: broccoli-oss-gcp-deploy
description: Deploy this repository to a new Google Cloud project using the repo's existing Cloud Run, Cloud Run Jobs, Cloud SQL, Secret Manager, and Artifact Registry scripts. Use when Codex needs to interpret a generic repo setup request as a deploy, discover the active gcloud operator/account/org/billing context, fail early on missing gcloud permissions or local prerequisites, or perform the actual Broccoli OSS GCP deployment behind an explicit apply step.
---

# Broccoli OSS GCP Deploy

## Overview

Use this skill to deploy this repo into a fresh GCP project without guessing operator-specific values. Discover the active `gcloud` context first, stop on missing prerequisites or permissions, and only mutate cloud state when the user has clearly asked you to deploy or set this repo up. Assume the operator may be doing this for the first time and may not yet have a project ID or know where secrets belong in GCP.

Intent rule: if the user says things like "set this up for me", "deploy this repo", or shares this repository URL and asks you to get it running, treat that as a deployment request for Broccoli. If they only provided the GitHub repo URL, clone the repo first, then use this skill from the repo checkout.

Authentication boundary: if `gcloud` requires interactive login or reauthentication, direct the user to complete that flow locally in their own terminal. Never ask the user to paste OAuth verification codes, one-time codes, tokens, private keys, API keys, database passwords, webhook secrets, PEM contents, or any other secret value into chat.

Project boundary: never read, copy, or infer secret values or operator inputs from a different GCP project in order to satisfy this deployment. Treat every target project as isolated unless the user explicitly instructs otherwise for a specific non-secret value. In particular, do not read Secret Manager values from another project to obtain `--github-app-id`, webhook secrets, API keys, database passwords, PEM contents, or similar deployment inputs.

Missing-input rule: if a required deployment input was not provided in the original prompt and cannot be discovered safely from the target project or active non-secret `gcloud` context, stop and ask the user for it before proceeding. For non-secret identifiers such as `--github-app-id`, asking in chat is allowed. For secrets, do not ask the user to send the value in chat; instead, instruct them to populate the target project's Secret Manager secret version themselves out of band and continue only after they confirm it is done. Do not keep going by guessing, reusing another project's values, or silently choosing substitutes.

Auto-discovery rule: once the target project contains the needed Secret Manager values, prefer using those target-project values directly instead of asking the operator to run helper commands themselves. Examples:

- retrieve generated webhook secrets from the target project's Secret Manager when you need them for setup guidance
- use the target project's `broccoli-oss-linear-api-key` to query Linear for `viewer.id` and candidate team ids
- use the target project's `broccoli-oss-db-password` to construct a local TCP `DATABASE_URL` for operator commands via Cloud SQL Auth Proxy

Only ask the operator for values that are not safely discoverable or that require a human choice, such as the target GitHub repository, the default branch to seed, or which GitHub App installation to use when more than one installation exists.

First-time-operator rule: if the operator does not already have a target GCP project, does not know the final project ID, or does not know where to add secrets, ask whether they want you to create the project first. If they say yes, you may run the apply step even before `--github-app-id` or operator-managed secret values are present. In that case the wrapper should create the project, attach billing, enable APIs, ensure Artifact Registry and Secret Manager containers exist, then stop with explicit README references for the manual GitHub/Linear/Secret Manager work.

## Required Workflow

Follow these steps in order. Do not skip discovery.

### 1. Discover the operator context

Run the discovery script first:

```bash
python .agents/skills/broccoli-oss-gcp-deploy/scripts/discover.py
```

The script checks:

- local discovery prerequisite: `gcloud`
- active `gcloud` account and current project
- visible organizations, folders, and open billing accounts
- recommended parent and billing defaults
- relevant org policies that may block public Cloud Run webhooks

If discovery fails, stop and fix the reported problem before doing anything else.

If the failure is an auth or reauth error, instruct the user to run `gcloud auth login <account> --no-launch-browser` locally in their own terminal when the operator account is known. Continue only after they confirm it is complete. Do not relay browser login links or ask for the returned verification code in chat.

Local apply requirements are checked when they are actually needed:

- `docker` + `docker buildx` only when building images locally
- `envsubst` only when running `deploy/bootstrap.sh`
- `uv` for the post-deploy migration/seed/preflight steps, not for discovery
- all `gcloud` subprocesses must run in non-interactive mode so the wrapper fails fast instead of hanging on prompts
- for the default Cloud Build path, ensure `roles/cloudbuild.builds.builder` on the default build executor service account(s) present in the target project before invoking the image build; if `iam.serviceAccounts.get` is denied, the wrapper should still attempt the binding directly instead of treating that lookup failure as fatal

For exact discovery commands and how to interpret failures, read [references/gcloud-discovery.md](./references/gcloud-discovery.md).

### 2. Confirm the resolved deployment values

By default, this skill resolves:

- project display name: `besimple-broccoli-oss`
- preferred project ID: `besimple-broccoli-oss`
- region: `us-central1`
- Artifact Registry location: `us`
- Artifact Registry repository: `containers`
- Cloud SQL instance: `broccoli-oss-pg`

If the user supplies overrides, pass them to the scripts instead of hardcoding values.

Required user-provided inputs for the full bootstrap path:

- GitHub App ID (`--github-app-id`)
- secret values for operator-managed Secret Manager secrets listed below, unless those values already exist in the target project

The apply step may safely generate these deployment-owned secrets if a latest version is missing:

- `broccoli-oss-db-password`
- `broccoli-oss-gh-webhook-secret`
- `broccoli-oss-linear-webhook-secret`

If any operator-managed secret inputs are missing, abort before bootstrap. Ask the user to provide non-secret identifiers in chat if needed, but require secret values to be populated out of band in the target project and confirmed complete before continuing.

If the operator is first-time and asks you to create the project first, it is acceptable to run `--apply` before `--github-app-id` and operator-managed secrets are ready. The wrapper should pause after project setup and point them to the README.

### 3. Run a non-mutating deployment plan

Before applying, run the deployment wrapper without `--apply`:

```bash
python .agents/skills/broccoli-oss-gcp-deploy/scripts/deploy.py --github-app-id <app-id>
```

This prints the resolved configuration, the required secrets, the exact repo scripts that will be invoked, and the next apply command.

When `--github-app-id` is missing, use the dry-run output to explain that the operator must manually follow these README sections before full bootstrap:

- `README.md -> Deploy it on your GCP -> 1. Create a GitHub App`
- `README.md -> Deploy it on your GCP -> 3. Open Secret Manager in the right project`
- `README.md -> Deploy it on your GCP -> 4. Add the required secret values`

Important limitation: project ID availability cannot be proven non-mutating. The authoritative check is project creation. If Google reports that the preferred ID is already in use, the wrapper may reuse that exact project only when the active operator can successfully describe it. Otherwise it must stop, report that the preferred ID is unavailable, and ask the user to choose a different project ID. Do not auto-pick a suffixed fallback.

### 4. Apply the deployment only when explicitly requested

Run the same wrapper with `--apply` when the user explicitly wants cloud changes. There are two valid apply paths:

1. project-prep apply for a first-time operator who needs the GCP project created before they can add secrets
2. full deploy apply after the user has confirmed the target values, provided any missing non-secret IDs, and confirmed that any missing secret values were populated out of band in the target project

Full deploy example:

```bash
python .agents/skills/broccoli-oss-gcp-deploy/scripts/deploy.py \
  --github-app-id <app-id> \
  --apply
```

The wrapper will:

1. create the GCP project under the resolved org or folder
2. link billing and enable required APIs
3. ensure the Artifact Registry repo exists
4. ensure the required Secret Manager secret containers exist
5. stop with README-backed manual instructions if `--github-app-id` is missing
6. stop before bootstrap if required operator-managed secret versions are still missing
7. create Cloud SQL PostgreSQL 16 with explicit `--edition=enterprise`
8. for the default Cloud Build path, ensure `roles/cloudbuild.builds.builder` on the default build executor service account(s) that exist in the target project
9. call [deploy/build-and-push.sh](/home/ubuntu/git/besimple-broccoli-oss/deploy/build-and-push.sh) unless prebuilt images were supplied
10. call [deploy/bootstrap.sh](/home/ubuntu/git/besimple-broccoli-oss/deploy/bootstrap.sh)
11. make the Cloud Run ingress service public with `--no-invoker-iam-check`

When apply stops on missing `--github-app-id` or missing operator-managed secrets, clearly send the operator to these README sections:

- `README.md -> Deploy it on your GCP -> 0. Create or choose a GCP project`
- `README.md -> Deploy it on your GCP -> 1. Create a GitHub App`
- `README.md -> Deploy it on your GCP -> 2. Designate a Linear bot user`
- `README.md -> Deploy it on your GCP -> 3. Open Secret Manager in the right project`
- `README.md -> Deploy it on your GCP -> 4. Add the required secret values`

Also include the GCP Console Secret Manager link for the resolved project. Be explicit that these steps remain manual because the values live in third-party products and should not be pasted into chat.

### 5. Finish post-deploy setup

After bootstrap succeeds, complete the remaining GitHub App, Linear, migration, seed, preflight, and smoke-test steps from [references/post-deploy.md](./references/post-deploy.md).

Post-deploy execution rule:

- do not stop at the service URL if the operator asked for a deploy and the remaining work is post-deploy setup you can continue safely
- prefer `--post-deploy-operator` so the wrapper runs `migrate`, `schema-version`, `seed`, and `preflight` inside GCP using a temporary Cloud Run Job instead of depending on local Cloud SQL Auth Proxy access
- print the exact follow-up commands for webhook-secret retrieval, Linear id discovery, Cloud SQL Auth Proxy, migrate, seed, and preflight
- if those commands only read from the target project's own secrets or APIs reached with those secrets, prefer running them yourself and reporting the results instead of telling the operator to do it manually
- treat GitHub App homepage/webhook settings and Linear webhook creation as manual admin tasks unless the operator explicitly provides credentials with that level of authority; a normal Linear bot API key is expected to be non-admin and is still sufficient for team/user discovery
- after deploy plus post-deploy setup, prefer a real Linear issue smoke over webhook-only canaries when the operator asks for end-to-end validation: assign a seeded issue to the configured bot, verify the queued/started/PR-opened/succeeded lifecycle comments, and verify a GitHub PR is actually published
- still leave the manual commands in the output and the README so operators can follow the same steps outside Codex if they want

## Script Interfaces

### `scripts/discover.py`

```bash
python .agents/skills/broccoli-oss-gcp-deploy/scripts/discover.py \
  [--project-id besimple-broccoli-oss] \
  [--display-name besimple-broccoli-oss] \
  [--organization <org-id>] \
  [--folder <folder-id>] \
  [--billing-account <billing-account-id>] \
  [--region us-central1] \
  [--format text|json]
```

Use `--format json` when the result needs to be piped or inspected programmatically.

### `scripts/deploy.py`

```bash
python .agents/skills/broccoli-oss-gcp-deploy/scripts/deploy.py \
  --github-app-id <app-id> \
  [--project-id besimple-broccoli-oss] \
  [--display-name besimple-broccoli-oss] \
  [--organization <org-id>] \
  [--folder <folder-id>] \
  [--billing-account <billing-account-id>] \
  [--region us-central1] \
  [--artifact-registry-location us] \
  [--artifact-repository containers] \
  [--tag latest] \
  [--service-image <image>] \
  [--runner-image <image>] \
  [--skip-build] \
  [--post-deploy-operator] \
  [--github-repo-full-name <owner/repo>] \
  [--git-clone-url <https-clone-url>] \
  [--default-branch <branch>] \
  [--github-installation-id <installation-id>] \
  [--linear-team-id <team-id>] \
  [--linear-bot-user-id <user-id>] \
  [--apply]
```

Behavior rules:

- `--apply` is required for any GCP mutation.
- Without `--apply`, the wrapper is a dry-run planner.
- `--skip-build` requires both `--service-image` and `--runner-image`.
- Missing operator-managed secret values are treated as blockers, not warnings.
- Missing required user inputs, including `--github-app-id`, are blockers for bootstrap. Stop and ask the user instead of sourcing them from another project or guessing.
- Never ask the user to paste secret values into chat. For missing secrets, instruct them to create or update the Secret Manager versions themselves and then confirm completion.
- When the operator needs a project created first, `--apply` may create the project and secret containers before stopping on missing `--github-app-id` or operator-managed secret values.
- `gcloud` calls must be non-interactive. If auth or reauth is required, stop with instructions for the operator to complete login locally and then resume.
- The wrapper should use Cloud Build by default and ensure the default build executor service account(s) that exist in the project have `roles/cloudbuild.builds.builder` before running the build. If `iam.serviceAccounts.get` is unavailable, attempt the IAM binding directly; only fail if no supported default executor identity exists or the binding itself fails.
- `--post-deploy-operator` requires `--github-repo-full-name`; the wrapper may auto-discover `--git-clone-url`, `--default-branch`, `--github-installation-id`, `--linear-team-id`, and `--linear-bot-user-id` from the target project's own secrets and third-party APIs reached with them.
- The temporary operator job created by `--post-deploy-operator` must be deleted after success or failure.

## Required Secrets

The apply step expects these operator-managed secrets to have a `latest` version before bootstrap:

- `broccoli-oss-github-app-private-key-pem`
- `broccoli-oss-linear-api-key`
- `broccoli-oss-openai-api-key`
- `broccoli-oss-anthropic-api-key`

The deploy wrapper can create missing secret containers safely. During `--apply`, it may also auto-generate `broccoli-oss-db-password`, `broccoli-oss-gh-webhook-secret`, and `broccoli-oss-linear-webhook-secret` if those latest versions are absent. It intentionally stops if any operator-managed secret values are still absent.

## Notes

- Keep this skill repo-local under `.agents/skills/`. Do not add it under `prompt-templates/skills/`; that directory is for runner prompt assets, not operator skills.
- Prefer the helper scripts over manually retyping long `gcloud` commands.
- If org policy blocks `--no-invoker-iam-check`, stop and surface that policy failure instead of trying to work around it silently.
