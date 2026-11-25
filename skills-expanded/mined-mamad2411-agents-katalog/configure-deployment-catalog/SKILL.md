---
name: configure-deployment-catalog
description: Help users configure how Opsphere knows their deployment sources — work context (Community) vs admin Cloud Catalog (Team). Use when deployment_status returns gaps, user asks about deployment sources, or latest-deploy queries fail for missing catalog config.
---

# Configure Deployment Catalog

Guide the user so **`deployment_status`** can resolve their stack. This is **catalog configuration**, not credential setup — use `configure-integration` for API keys.

## Tools

- `deployment_status(env?, target?, scope?)` — discover what's configured; read `gaps[]` for next steps
- `ops_my_usage()` — plan tier, **Catalog configuration** section (`plugin` vs `admin_portal`)
- `ops_set_work_context(context)` — **Community only** (prose description of stack)
- `ops_get_work_context()` — read saved context

**Never** store secrets in work context or chat. **Never** invent Vercel project names — use what the user or catalog provides.

## Decision tree

### 1. Check plan surface

Call `ops_my_usage` and read **Catalog configuration**:

| `catalog_config_surface` | Who configures structured sources |
|--------------------------|-------------------------------------|
| `plugin` | User via **`ops_set_work_context`** + integrations |
| `admin_portal` | Org **tenant_admin** at **https://admin.opsphere.io** → Cloud Catalog → Deployment sources |

If `work_context_editable_via_plugin: no`, **do not** call `ops_set_work_context` — Team/Enterprise returns `WorkContextForbiddenError`. Tell the user to contact their admin.

### 2. Community (plugin path)

1. Ask the user to describe their stack in prose (projects, envs, Vercel names, Bitbucket repos, S3 buckets, ECS services).
2. Call `ops_set_work_context(context: "<user text>")`.
3. Ensure integrations exist for providers they use:
   - Vercel → `configure-integration` skill → `VERCEL_TOKEN`
   - AWS (S3/ECS) → `configure-integration` → IAM keys
   - Bitbucket / GitHub → for CI correlation in `deployment_status`
4. Re-run `deployment_status(scope="auto")` to verify.

**Example prose:** _"Prod on Vercel project `acme-store-prod`. Static assets in S3 bucket `acme-static` + CloudFront. CI on Bitbucket workspace `acme`, repo `backend`."_

### 3. Team / Enterprise (admin portal path)

1. Explain that **Deployment sources** (JSON: Vercel, CI, GitOps, S3+CloudFront, ECS) are configured in **Cloud Catalog** by a tenant admin.
2. Share **`admin_portal_url`** from `ops_my_usage` (default **https://admin.opsphere.io**).
3. User action: admin adds sources per environment (PRD, TST, …) in the admin UI.
4. After admin updates catalog, retry `deployment_status`.

Do **not** tell Team users that `ops_set_work_context` will work — it will not.

### ArgoCD installations and GitOps destinations

When available, read **`opsphere://argocd/installations`** for the active workspace's resolution mode, installation identifiers and application associations. This is discovery, not evidence that Kubernetes credentials are ready.

- `legacy` / `shadow`: existing deployment sources still execute. Shadow compares the new selection without executing a second provider request. Do not claim a newly added association is active yet.
- `active`: use the association's exact `target` and `environment` with `deployment_status(target=..., env=..., scope="gitops")`. Multiple matching products require clarification; never choose the first or infer that `pre` means `nonprod`.
- For a direct ArgoCD tool, use the discovered installation slug in its existing `instance` parameter when that parameter is exposed. Do not invent a new parameter or an installation name.
- Configuration lives in **Admin → Cloud Catalog → + ArgoCD**, independently of the cloud-account capability checkbox. A workspace installation can serve multiple account environments or a standalone product/environment.
- The current connection method is Kubernetes through the existing AWS/SSO identity. Keep the management cluster's profile, Kubernetes context and namespace. An associated destination profile is **not** the management identity. Do not request an ArgoCD API token or bypass SSO.
- Association changes do not grant tool permissions or cross-workspace access. `valid_profiles` applies to explicit connection-profile overrides; adding a destination does not require adding that destination's profile to this list.
- An admin enables `active` only after reviewing associations and validating shadow results; configuration completeness alone does not prove connectivity. Do not change resolution mode as part of a read-only query.

If this resource is unavailable, use existing discovery and report that independent resolution cannot be verified. Do not assume the backend has been upgraded.

## When `deployment_status` returns gaps

| Gap theme | Community action | Team action |
|-----------|------------------|-------------|
| No Vercel source | Configure Vercel integration + mention project in work context | Admin adds `vercel` source in Cloud Catalog |
| No CI source | Describe repo/workspace in work context; configure Bitbucket/GitHub | Admin adds `ci_bitbucket` / `ci_ghe` source |
| No static web | Describe S3 bucket in work context; configure AWS | Admin adds `s3_cloudfront` source |
| capability off | Explain plan/tool not available; no `vercel_*` if vercel=false | Same — respect capabilities |

## Conversation script (Community, no sources)

> "Opsphere doesn't know your deployment stack yet. On the Community plan, describe what you deploy and where — Vercel project names, Bitbucket repos, S3 buckets, etc. I'll save that with `ops_set_work_context` (no API keys here). Then we'll connect any missing integrations like Vercel or AWS."

## Conversation script (Team, no sources)

> "Deployment sources for your org are managed in the **Opsphere admin portal** by your tenant admin. Ask them to add **Deployment sources** for your environment in **Cloud Catalog** at https://admin.opsphere.io. I can run `deployment_status` again once that's configured."

## Related skills

- **`set-work-context`** — Community prose only
- **`configure-integration`** — API credentials for Datadog, Vercel, AWS, etc.
