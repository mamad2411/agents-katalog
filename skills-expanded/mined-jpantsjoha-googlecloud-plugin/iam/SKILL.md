---
name: iam
description: "Google Cloud IAM — identity, access management, service accounts, and policy authoring. Enforces least-privilege by default. Covers roles, conditions, service account patterns, Workload Identity Federation, and gcloud CLI. Never grants owner or editor roles. Use when the user mentions: iam policy, grant access, least privilege, IAM binding, who has access, iam conditions, gcloud iam. Use this to author or change IAM; use gcp-security instead to audit an existing posture against the security gate."
license: MIT
metadata:
  "googlecloud-plugin/version": "0.1"
  "googlecloud-plugin/triggers": "IAM, iam policy, grant access, service account, roles, least privilege, IAM binding, who has access, iam conditions, workload identity federation, gcloud iam"
  "googlecloud-plugin/required-scopes": "iam.roles.get, iam.roles.list, resourcemanager.projects.getIamPolicy, resourcemanager.projects.setIamPolicy"
  "googlecloud-plugin/mcp-servers": "google-iam"
---

# IAM — Identity and Access Management

Control who (identity) can do what (role) on which GCP resource. Always least-privilege.

## Principles

1. **Least privilege** — grant the minimum role needed. Prefer predefined roles over basic roles. Never grant `roles/owner` or `roles/editor` programmatically.
2. **Service accounts for workloads** — not user accounts. Use Workload Identity to avoid SA key files.
3. **IAM Conditions** — scope bindings by resource, time, or request attribute where possible.
4. **Audit regularly** — `gcloud projects get-iam-policy` to review bindings; remove stale grants.

## Core Patterns

### Grant a predefined role

```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SA@PROJECT.iam.gserviceaccount.com" \
  --role="roles/run.invoker"
```

### Create a service account

```bash
gcloud iam service-accounts create SA_NAME \
  --display-name="Description" \
  --project PROJECT_ID
```

### List effective permissions on a resource

```bash
gcloud projects get-iam-policy PROJECT_ID \
  --flatten="bindings[].members" \
  --format="table(bindings.role,bindings.members)"
```

### IAM Condition (time-bound access)

```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="user:USER@example.com" \
  --role="roles/viewer" \
  --condition="expression=request.time < timestamp('2026-12-31T00:00:00Z'),title=temp-access"
```

## Never Do

- Grant `roles/owner` or `roles/editor` to service accounts or automation
- Create SA key files when impersonation, an attached service account or Workload Identity Federation can do the job (see `shared/auth/README.md`)
- Share service account keys across environments

## References

- [IAM Overview](https://cloud.google.com/iam/docs/overview)
- [IAM Best Practices](https://cloud.google.com/iam/docs/using-iam-securely)
- [Service Account Overview](https://cloud.google.com/iam/docs/service-account-overview)
- [Predefined Roles Reference](https://cloud.google.com/iam/docs/understanding-roles)
