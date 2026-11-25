---
name: openshift-safe-operations
description: How to authenticate to and safely operate an OpenShift/Kubernetes cluster through mcp-openshift — getting a token from the browser web console or via username/password (local IdP), the safe-by-default access model (modes, namespace allowlists, protected namespaces, apply/delete gates, dry-run), and the standard diagnose-before-change workflows. Use whenever connecting mcp-openshift, choosing an auth method, deciding what is safe to run, or triaging/operating workloads on the cluster.
---

# Operating OpenShift safely with mcp-openshift

`mcp-openshift` (`@dockndevai/mcp-openshift`) is a safe-by-default MCP server for an OpenShift /
Kubernetes cluster. This skill is the operating manual: how to authenticate (including from the
browser console you already use), the safety rules the agent must follow, and the common workflows.

## 1. Authentication — how to connect

You always need the **API server URL** plus a credential. The server auto-detects the auth method.

### A. Bearer token from the browser web console (recommended, quickest)
Because you use OpenShift in the browser, the easiest token comes straight from the console:

1. In the OpenShift web console, click your **username (top-right)** → **Copy login command**.
2. Re-authenticate if prompted, then click **Display Token**.
3. Copy the value after `--token=` (starts with `sha256~…`) and the URL after `--server=`.
4. Configure:
   - `OPENSHIFT_SERVER=https://api.<cluster>.<domain>:6443`
   - `OPENSHIFT_TOKEN=sha256~…`

Equivalent on the CLI: `oc whoami --show-server` and `oc whoami -t`.
Console tokens are **short-lived** (often 24h); when it expires, grab a fresh one, or use password
auth (below) which re-logins automatically.

### B. Username / password against the local identity provider
For HTPasswd / LDAP / any challenge-capable local IdP, give the credentials and the server runs the
same OAuth *request-token* flow `oc login -u … -p …` uses, caches the token, and re-logs in on expiry:
- `OPENSHIFT_SERVER=https://api.<cluster>:6443`
- `OPENSHIFT_USERNAME=<user>`
- `OPENSHIFT_PASSWORD=<password>`

The password is sent **only** to the cluster's own OAuth endpoint over TLS, is never logged, and is
never written to disk (only the resulting token is cached at `~/.mcp-openshift/token.json`, mode 0600).
If the IdP does not support direct password login (e.g. pure OIDC/SSO), use method A instead.

### TLS (private-CA clusters)
Most clusters use a private CA. Either trust it — `OPENSHIFT_CA_CERT=/path/to/ca.crt` — or, for a dev
cluster only, `OPENSHIFT_INSECURE_TLS=true` (this disables MITM protection; never use it against a
cluster that matters).

## 2. The safety model — what the agent may do

The cluster's **RBAC for your account is the real boundary**; these flags are defence in depth on top.

- **Access mode `OPENSHIFT_MODE`** — `read-only` (default) → `read-write` → `admin`. A tool is
  registered only if the mode allows its capability. Read-only exposes only observe tools.
- **Namespace scoping** — `OPENSHIFT_NAMESPACE_ALLOWLIST` confines writes/deletes to named
  namespaces; `OPENSHIFT_PROTECTED_NAMESPACES` (defaults to `kube-*`, `openshift`, `openshift-*`,
  `default`) may be **read but never mutated**.
- **Apply gate** — `apply_resource` (create/update) needs `OPENSHIFT_ALLOW_APPLY=true` on top of
  read-write, plus a human confirmation.
- **Delete gate** — `delete_resource` needs `admin` mode **and** `OPENSHIFT_ALLOW_DELETE=true`, plus
  a human confirmation. Deletes are not recoverable through the API.
- **Dry-run** — `OPENSHIFT_DRY_RUN=true` sends writes with Kubernetes `dryRun=All`: the API validates
  and admission-checks them but persists nothing.
- **Audit + redaction** — every guarded op emits a JSON audit line to stderr; Secret `data` values
  are always redacted from resource output; secret-named `env` values, ConfigMap entries and Route `tls.key` are masked on a best-effort basis (`OPENSHIFT_REDACT_OBJECTS`, on by default), and `pod_logs` output is scrubbed of credential-shaped text on a best-effort basis (`OPENSHIFT_REDACT_LOGS`, on by default). Both are heuristic, not a guarantee.

### Rules the agent should follow
1. **Start read-only and diagnose first.** Prefer `list_resources`, `get_resource`, `pod_logs`,
   `list_events` before proposing any change.
2. **Never mutate protected/system namespaces.** If asked to, explain that they're read-only here.
3. **Dry-run a write before doing it for real** when the change is non-trivial (`OPENSHIFT_DRY_RUN`
   or by proposing it and letting the human enable apply).
4. **Prefer the least drastic action** — `scale`/`rollout_restart` over deleting and recreating.
5. **Deleting is last resort.** It requires admin + the flag + confirmation for a reason.
6. **Report the audit trail.** When you change something, say exactly what, in which namespace.

## 3. Common workflows

**Triage a failing workload**
1. `list_projects` → pick the namespace.
2. `list_resources kind=pod namespace=<ns>` → find the unhealthy pod (Pending/CrashLoopBackOff).
3. `get_resource kind=pod name=<pod> namespace=<ns>` → read status/conditions.
4. `pod_logs namespace=<ns> name=<pod>` (add `previous=true` for a crashed instance).
5. `list_events namespace=<ns>` → scheduling / image-pull / quota errors.

**Roll a deployment**: `rollout_restart namespace=<ns> name=<deploy>`.
**Scale**: `scale namespace=<ns> name=<deploy> replicas=<n>` (scaling to 0 asks for confirmation).
**Ship a change**: build the manifest, then `apply_resource` with `OPENSHIFT_DRY_RUN=true` first to
validate, then apply for real (needs `OPENSHIFT_ALLOW_APPLY=true`).

## 4. Resource kinds you can name
Core: `pod`, `service`, `configmap`, `secret`, `pvc`, `serviceaccount`, `event`, `node`,
`namespace`. Apps: `deployment`, `replicaset`, `statefulset`, `daemonset`, `job`, `cronjob`.
OpenShift: `project`, `deploymentconfig`, `route`, `build`, `buildconfig`, `imagestream`. Singular or
plural is accepted. For anything else, `list_resources`/`get_resource` accept the kind directly.

## 5. Recommended starting posture
```
OPENSHIFT_SERVER=https://api.<cluster>:6443
OPENSHIFT_TOKEN=sha256~…            # or OPENSHIFT_USERNAME/OPENSHIFT_PASSWORD
OPENSHIFT_CA_CERT=/path/to/ca.crt   # if the cluster uses a private CA
OPENSHIFT_MODE=read-only            # raise to read-write / admin only when needed
# to enable changes later, add exactly what you need:
# OPENSHIFT_MODE=read-write OPENSHIFT_NAMESPACE_ALLOWLIST=my-app,my-app-staging
# OPENSHIFT_ALLOW_APPLY=true OPENSHIFT_DRY_RUN=true   # validate applies first
```
