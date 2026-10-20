---
name: gcloud-cli-auth
description: Set up the gcloud CLI, Application Default Credentials, projects, and keyless service-account auth. Use when the user needs to install, configure, or debug Google Cloud authentication.
---

# gcloud CLI and Auth Setup

## Install and initialize

```bash
brew install google-cloud-sdk        # macOS; Linux: apt/yum repo or tarball
gcloud init                          # login + pick project + default region
gcloud components update             # keep current; some tools are components
gcloud auth list                     # active CLI account
gcloud config list                   # project, region, account in effect
```

Project targeting: `gcloud config set project my-project`, or per-command
`--project my-project`. Multiple contexts (work/personal, prod/dev):

```bash
gcloud config configurations create work
gcloud config configurations activate work
```

## The two logins (do not confuse them)

- `gcloud auth login`: credentials for **the gcloud CLI itself**.
- `gcloud auth application-default login`: writes **Application Default
  Credentials (ADC)** to
  `~/.config/gcloud/application_default_credentials.json`, which is what
  **your code and SDKs** read.

Client libraries failing with `Could not automatically determine
credentials` while gcloud works fine means ADC was never set up. They are
independent stores.

ADC resolution order: `GOOGLE_APPLICATION_CREDENTIALS` env var (path to a
credential config file) -> the ADC file above -> the attached service
account (Cloud Run, GKE, GCE metadata server).

Quota project: user ADC needs a project to bill API quota against. On
`Quota exceeded` or `API not enabled` errors right after login:

```bash
gcloud auth application-default set-quota-project my-project
```

## Service accounts, keyless

The golden rule: never download service account keys if avoidable.

- **On Google Cloud** (Cloud Run, GKE, GCE): attach the service account to
  the workload; ADC finds it ambiently. GKE uses Workload Identity (see
  the gke skill).
- **Local dev as a service account**: impersonation, no key file:

```bash
gcloud auth application-default login \
  --impersonate-service-account=app-sa@my-project.iam.gserviceaccount.com
# caller needs roles/iam.serviceAccountTokenCreator on that SA
```

- **External CI (GitHub Actions, other clouds)**: Workload Identity
  Federation. The generated credential config JSON contains no private key
  and is safe to store. gcloud accepts it directly:

```bash
gcloud auth login --cred-file=wif-credential-config.json
```

- Print a token for raw HTTP debugging:
  `curl -H "Authorization: Bearer $(gcloud auth print-access-token)" ...`
  (use `print-identity-token` for Cloud Run invoker auth).

If keys are truly unavoidable, disable them by default at the org with the
`iam.disableServiceAccountKeyCreation` org policy and exempt per project.

## Service account management

```bash
gcloud iam service-accounts create app-sa --display-name "App runtime"
gcloud projects add-iam-policy-binding my-project \
  --member serviceAccount:app-sa@my-project.iam.gserviceaccount.com \
  --role roles/secretmanager.secretAccessor
gcloud iam service-accounts list
```

Grant narrow predefined roles per service (see the gcp-secrets-iam skill);
never `roles/editor` on a runtime SA.

## Debug ladder

1. `gcloud auth list` and `gcloud config get-value project`: right account,
   right project?
2. Code failing but CLI working: ADC missing or stale, re-run
   `gcloud auth application-default login`.
3. `PERMISSION_DENIED`: check WHICH identity called (error names it), then
   its roles: `gcloud projects get-iam-policy my-project
   --flatten=bindings --filter="bindings.members:app-sa@*"`.
4. `403 ... API has not been used`: `gcloud services enable
   run.googleapis.com` (per project, per API).

## In Caeros

Run `gcloud auth login` plus `gcloud auth application-default login` once
in your environment; Caeros shells and generated code inherit both, and
`--impersonate-service-account` keeps prod-shaped testing keyless.
