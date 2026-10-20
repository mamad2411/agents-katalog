---
name: gcp-secrets-iam
description: Manage secrets with Secret Manager and design least-privilege IAM bindings, service accounts, and org policies on Google Cloud. Use when the user is handling credentials, granting access, or auditing permissions.
---

# Secret Manager and Least-Privilege IAM

## Secret Manager basics

```bash
gcloud services enable secretmanager.googleapis.com
printf 'postgres://...' | gcloud secrets create db-url \
  --replication-policy automatic --data-file=-
printf 'new-value' | gcloud secrets versions add db-url --data-file=-
gcloud secrets versions access latest --secret db-url
gcloud secrets versions list db-url
gcloud secrets versions disable 1 --secret db-url   # revoke without delete
```

- Secrets are versioned; consumers should pin a version in config and roll
  forward deliberately. `latest` is convenient and is also how a bad value
  ships everywhere at once.
- Use `--data-file=-` with a pipe, never `--data-file=secret.txt` left on
  disk, and never pass secret values as command-line args (shell history).
- Rotation: set `--next-rotation-time`/`--rotation-period` to get Pub/Sub
  reminders; the rotation itself is your job (Cloud Run job or Cloud
  Function subscribed to the topic).
- Access from code: ADC + the client library
  (`SecretManagerServiceClient.access_secret_version`), or platform
  integration (Cloud Run `--set-secrets`, GKE Secret Manager add-on with
  Workload Identity). Do not copy secrets into plain Kubernetes Secrets or
  `.env` files in images.

## Grant access at the secret, not the project

```bash
gcloud secrets add-iam-policy-binding db-url \
  --member serviceAccount:app-sa@PROJ.iam.gserviceaccount.com \
  --role roles/secretmanager.secretAccessor
```

`secretAccessor` reads values; `secretVersionManager` adds/disables
versions; `roles/secretmanager.admin` is for humans running ops, not
runtimes. Granting `secretAccessor` on the whole project gives every
secret to that identity: per-secret bindings are the point.

## Least-privilege IAM playbook

- **Never basic roles** (`roles/owner`, `roles/editor`, `roles/viewer`) on
  service accounts or in prod projects. Use predefined roles
  (`roles/run.invoker`, `roles/storage.objectViewer`, ...); browse with
  `gcloud iam roles describe` or the roles reference.
- One service account per workload, named for it (`myapp-run-sa`), granted
  only what that workload calls.
- Bind at the narrowest resource that supports it: bucket
  (`gcloud storage buckets add-iam-policy-binding`), secret, topic,
  service, dataset; project-level bindings are the fallback, folder/org
  the exception.
- **IAM Conditions** for time-boxed or resource-name-scoped grants:

```bash
gcloud projects add-iam-policy-binding PROJ \
  --member user:dev@example.com --role roles/cloudsql.client \
  --condition 'expression=request.time < timestamp("2026-08-01T00:00:00Z"),title=temp-access'
```

- Separate projects per environment; project boundaries are the strongest
  isolation you get.

## Audit and tighten

```bash
gcloud projects get-iam-policy PROJ \
  --flatten="bindings[].members" \
  --format="table(bindings.role,bindings.members)" \
  --filter="bindings.members:serviceAccount"
gcloud policy-intelligence query-activity --activity-type serviceAccountLastAuthentication --project PROJ
```

- IAM Recommender (Console > IAM, or `gcloud recommender recommendations
  list --recommender=google.iam.policy.Recommender`) flags over-granted
  roles from 90-day usage; act on it quarterly.
- Enable Data Access audit logs for Secret Manager so
  `AccessSecretVersion` calls are logged with caller identity.
- Disable service account key creation org-wide
  (`iam.disableServiceAccountKeyCreation` org policy) and keyless auth
  everywhere (see the gcloud-cli-auth skill); audit stragglers with
  `gcloud iam service-accounts keys list`.

## Incident quick path

Leaked secret: `gcloud secrets versions add` the replacement, redeploy
consumers, `versions disable` (then destroy) the leaked version, check
audit logs for `AccessSecretVersion` by unexpected principals. Leaked SA
key: `gcloud iam service-accounts keys delete` immediately, then rotate
whatever that SA could reach.
