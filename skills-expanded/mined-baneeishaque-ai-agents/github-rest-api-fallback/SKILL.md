---
name: github-rest-api-fallback
description: Industrial fallback protocol for querying and mutating GitHub resources via the REST API (api.github.com) when the gh CLI is unavailable, using PowerShell Invoke-RestMethod or curl with optional Personal Access Token authentication.
category: GitHub-Automation
---

# GitHub REST API Fallback Skill (v1)

This skill defines the operational fallback when the **`gh` CLI** is not installed, not on `PATH`, or not
authenticated, but the agent still needs to perform GitHub operations such as repo inspection, fork discovery,
PR listing, or secret management.

It treats the **GitHub REST API** at `https://api.github.com` as the SSOT and provides a portable invocation
pattern using `Invoke-RestMethod` (PowerShell) and `curl` (POSIX).

***

## 1. Environment & Dependencies

The agent MUST verify the fallback path is necessary, AND that the underlying HTTP client works.

### 1.1 Detect `gh` absence

```powershell
# PowerShell
where.exe gh 2>&1
gh --version 2>&1
```

```bash
# POSIX
which gh
gh --version
```

If both return "not found" / non-zero exit, the fallback is justified. Before engaging, consider whether
installing `gh` via [System-Wide Tool Management](../system-wide-tool-management/SKILL.md) is more appropriate
for the current task — this skill is the short-term workaround.

### 1.2 Verify HTTP client

```powershell
# PowerShell — built into Windows PowerShell 5.1+ and PowerShell Core 7+
Get-Command Invoke-RestMethod
```

```bash
# POSIX
which curl && curl --version | head -1
```

### 1.3 Authentication decision

| Need | Token required? | Notes |
| :--- | :--- | :--- |
| Public repo metadata, forks list, branches, public PRs, public files | No | Unauthenticated rate limit: 60 req/hr per IP. |
| Private repo data, write operations, user-scoped lists, higher rate | Yes | Personal Access Token (classic or fine-grained) with appropriate scope. |
| Secrets, releases, workflow dispatches | Yes | Scope: `repo`, plus `workflow` or specific resource scope. |
| **Any operation on a GitHub Enterprise Server (GHE)** | **Yes** | GHE rejects unauthenticated requests with `401 Unauthorized` even for endpoints public on `api.github.com`. See §1.4. |

If a token is required, the agent MUST instruct the user to generate one at
`https://github.com/settings/tokens` (or `https://<ghe-host>/settings/tokens` for GHE) and surface it via an
environment variable — NEVER hard-code it in scripts, URLs, commit messages, or session logs (Tier-A per
[Redaction & Portability](../redaction-portability/SKILL.md) §1).

### 1.4 GitHub Enterprise Server (GHE) base URL

When the target host is **not** `github.com` (e.g., a corporate GitHub Enterprise instance at
`github.<corp-cloud-domain>` or `github.<corp-domain>`), the API base is **NOT** `https://api.github.com` —
it is `https://<ghe-host>/api/v3` (REST v3) or `https://<ghe-host>/api/graphql` (GraphQL).

| Hosted GitHub.com | GitHub Enterprise Server |
| :--- | :--- |
| `https://api.github.com/repos/<o>/<r>` | `https://<ghe-host>/api/v3/repos/<o>/<r>` |
| `https://api.github.com/user/repos` | `https://<ghe-host>/api/v3/user/repos` |
| `https://api.github.com/repos/<o>/<r>/forks` | `https://<ghe-host>/api/v3/repos/<o>/<r>/forks` |

**Detection heuristic:** Inspect `git remote -v` in the target repo. If the remote host is anything other
than `github.com`, treat it as GHE and prepend `/api/v3` to every endpoint path.

**Tokens are NOT portable across instances.** A PAT issued at `github.com/settings/tokens` is rejected by
`<ghe-host>/api/v3` with `401 Bad credentials`. Generate the token at the matching host's
`/settings/tokens` page.

All subsequent examples in §2–§4 use `api.github.com` for readability; substitute `<ghe-host>/api/v3`
verbatim when targeting an Enterprise instance.

***

## 2. The Canonical Invocation Pattern

When this skill is engaged via `create_and_run_task` (because `run_in_terminal` is also unavailable), use the
file-mediated output-capture pattern from
[Terminal Fallback via VS Code Tasks](../terminal-fallback-via-vscode-tasks/SKILL.md) §3.

### 2.1 PowerShell — Unauthenticated GET

```powershell
Invoke-RestMethod `
  -Uri 'https://api.github.com/repos/<owner>/<repo>' `
  -Headers @{ 'User-Agent' = 'copilot-agent' } `
  | ConvertTo-Json -Depth 5 `
  | Out-File .gh_response.txt -Encoding utf8
```

**Flag-by-flag breakdown:**

- **`-Uri`** — Full REST endpoint. Always single-quoted to prevent PowerShell variable expansion inside the URL.
- **`-Headers @{ 'User-Agent' = '...' }`** — The GitHub API rejects requests without a `User-Agent` header
  (HTTP 403 with "Request forbidden by administrative rules"). Any non-empty identifier is acceptable.
- **`ConvertTo-Json -Depth 5`** — Serializes the deserialized response object back to JSON for inspection.
  Depth 5 covers most GitHub schemas; raise to 8 for deeply nested objects (e.g., PR with commits and reviews).
- **`Out-File .gh_response.txt -Encoding utf8`** — Captures the response into the workspace per the terminal
  fallback pattern. `utf8` is mandatory; the PowerShell default (`utf8 with BOM`) breaks `read_file`'s parsing
  in some configurations.

### 2.2 PowerShell — Authenticated GET (with PAT)

```powershell
$Headers = @{
  'User-Agent'    = 'copilot-agent'
  'Accept'        = 'application/vnd.github+json'
  'Authorization' = "Bearer $env:GITHUB_TOKEN"
}
Invoke-RestMethod -Uri 'https://api.github.com/user/repos?per_page=100&type=owner' -Headers $Headers `
  | ConvertTo-Json -Depth 5 `
  | Out-File .gh_repos.txt -Encoding utf8
```

**Additional headers:**

- **`Accept: application/vnd.github+json`** — Pins the response schema to the current stable GitHub API.
  Recommended for all authenticated calls.
- **`Authorization: Bearer <token>`** — Token-based auth. The token MUST be supplied from `$env:GITHUB_TOKEN`
  (or any other env var); embedding it in the command body is a Tier-A redaction violation.

### 2.3 PowerShell — Mutating POST / PATCH / DELETE

```powershell
$Body = @{ name = 'new-repo'; private = $false } | ConvertTo-Json
Invoke-RestMethod `
  -Method Post `
  -Uri 'https://api.github.com/user/repos' `
  -Headers $Headers `
  -ContentType 'application/json' `
  -Body $Body `
  | ConvertTo-Json -Depth 5 | Out-File .gh_create.txt -Encoding utf8
```

For DELETE, omit `-Body` and pass `-Method Delete`. For PATCH, use `-Method Patch` and include the partial body.

### 2.4 POSIX — `curl` equivalents

```bash
# Unauthenticated GET
curl -fsSL -H 'User-Agent: copilot-agent' \
     'https://api.github.com/repos/<owner>/<repo>' \
     -o .gh_response.json

# Authenticated GET
curl -fsSL \
     -H 'User-Agent: copilot-agent' \
     -H 'Accept: application/vnd.github+json' \
     -H "Authorization: Bearer ${GITHUB_TOKEN}" \
     'https://api.github.com/user/repos?per_page=100&type=owner' \
     -o .gh_repos.json
```

**Flag-by-flag breakdown:**

- **`-f`** — Fail (non-zero exit) on HTTP ≥ 400. Without it, `curl` writes the error body to stdout and exits 0.
- **`-s`** — Silent; suppress progress meter.
- **`-S`** — Show errors even with `-s`.
- **`-L`** — Follow redirects (the GitHub API occasionally 301-redirects renamed resources).
- **`-o <file>`** — Capture response to the workspace per the terminal fallback pattern.

***

## 3. Canonical Endpoint Cookbook

This section maps the most common `gh` CLI commands to their REST equivalents. All endpoints are documented at
<https://docs.github.com/en/rest>.

| `gh` Command | REST Endpoint | Auth required? |
| :--- | :--- | :--- |
| `gh repo view <owner>/<repo>` | `GET /repos/{owner}/{repo}` | No (public) |
| `gh repo list <owner> --fork` | `GET /users/{user}/repos?type=owner` then filter `fork=true` | No (public list) |
| **List forks of an upstream** | `GET /repos/{owner}/{repo}/forks?per_page=100` | No (public list) |
| `gh repo fork <owner>/<repo>` | `POST /repos/{owner}/{repo}/forks` | Yes |
| `gh repo rename <new> --repo <owner>/<repo>` | `PATCH /repos/{owner}/{repo}` body `{ "name": "<new>" }` | Yes |
| `gh repo create <name>` | `POST /user/repos` body `{ "name": "<name>" }` | Yes |
| `gh pr list --repo <owner>/<repo>` | `GET /repos/{owner}/{repo}/pulls?state=open` | No (public) |
| `gh pr view <num> --repo <owner>/<repo>` | `GET /repos/{owner}/{repo}/pulls/{num}` | No (public) |
| `gh secret list --repo <owner>/<repo>` | `GET /repos/{owner}/{repo}/actions/secrets` | Yes |
| `gh secret set NAME --repo <owner>/<repo>` | Two-step: `GET /repos/{owner}/{repo}/actions/secrets/public-key` then `PUT /repos/{owner}/{repo}/actions/secrets/{name}` with libsodium-sealed value | Yes |
| `gh auth status` | `GET /user` (returns 200 if token valid, 401 if not) | Yes |

### 3.1 Fork-discovery example (the case that prompted this skill)

```powershell
Invoke-RestMethod `
  -Uri 'https://api.github.com/repos/<upstream-owner>/<repo>/forks?per_page=100' `
  -Headers @{ 'User-Agent' = 'copilot-agent' } `
  | ConvertTo-Json -Depth 4 `
  | Out-File .gh_forks.txt -Encoding utf8
```

The response is an array of fork objects; each has `full_name` (e.g., `someuser/repo`), `owner.login`,
`pushed_at`, `clone_url`. Identify the user's fork by matching `owner.login`, OR by ranking on recency
(`pushed_at`) when the user's account is unknown but a recent push is expected.

### 3.2 Pagination

The GitHub API returns at most 100 items per page. For multi-page resources (repos, forks, commits), iterate:

```powershell
$Page = 1
$All  = @()
while ($true) {
  $batch = Invoke-RestMethod -Uri "https://api.github.com/repos/<o>/<r>/forks?per_page=100&page=$Page" `
                             -Headers @{ 'User-Agent' = 'copilot-agent' }
  if ($batch.Count -eq 0) { break }
  $All += $batch
  $Page++
}
```

***

## 4. Rate Limits & Diagnostics

```powershell
Invoke-RestMethod -Uri 'https://api.github.com/rate_limit' `
                  -Headers @{ 'User-Agent' = 'copilot-agent' } `
  | ConvertTo-Json -Depth 3 | Out-File .gh_rate.txt -Encoding utf8
```

- **Unauthenticated**: 60 requests/hour per IP.
- **Authenticated (classic PAT)**: 5,000 requests/hour.
- **Fine-grained PAT or GitHub App**: 5,000 requests/hour per token; 15,000 for paid orgs.

If `X-RateLimit-Remaining: 0` is observed, the agent MUST wait until `X-RateLimit-Reset` (Unix epoch) or
authenticate with a higher limit.

***

## 5. Failure Modes

| HTTP / Symptom | Cause | Resolution |
| :--- | :--- | :--- |
| `403 Request forbidden by administrative rules` | Missing `User-Agent` header | Add `'User-Agent' = '<any-identifier>'`. |
| `401 Bad credentials` | Invalid / expired PAT | Regenerate; re-export `$env:GITHUB_TOKEN`. |
| `404 Not Found` on a known repo | Repo is private and token lacks scope, OR the URL has a typo | Verify token scope (`repo` for private); double-check `owner/repo`. |
| `422 Validation Failed` on `POST` / `PATCH` | Body violates a GitHub constraint (e.g., reserved secret name prefix) | Inspect the `errors[]` array in the response body. |
| `Invoke-RestMethod : The remote server returned an error: (404)` | Same as above on PowerShell | The full response body is in `$_.ErrorDetails.Message`; capture it with a try/catch wrapper. |
| TLS errors in older Windows PowerShell | TLS 1.2 not enforced | `[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12` before the call. |

***

## 6. Composition by Higher-Level Skills

| Composer | Role | Reuses From This Skill |
| :--- | :--- | :--- |
| [`git-submodule-fork-reconfigure`](../git-submodule-fork-reconfigure/SKILL.md) | Discover an existing fork by listing upstream forks, when `gh` is unavailable. | §3.1 fork-discovery, §3 endpoint cookbook for `GET /repos/{o}/{r}/forks`. |
| [`git-submodule-fork-sync`](../git-submodule-fork-sync/SKILL.md) | Automated fork-conformance check (`gh repo view` / `gh repo rename`). | §3 endpoint cookbook — `GET /repos/{o}/{r}` and `PATCH /repos/{o}/{r}`. |
| [`git-submodule-orphan-gitlink-recovery`](../git-submodule-orphan-gitlink-recovery/SKILL.md) | SHA-based fork discovery for orphan gitlinks. | §3 endpoint cookbook for `GET /repos/{o}/{r}`, `POST /repos/{o}/{r}/forks`. |
| [`git-submodule-dead-upstream-audit`](../git-submodule-dead-upstream-audit/SKILL.md) | Detect 404 / private / deleted submodule upstreams. | §2.4 `curl` pattern and §3 `GET /repos/{o}/{r}`; §4 rate-limit awareness. |
| [`git-github-auth-fallback`](../git-github-auth-fallback/SKILL.md) | Validate that a PAT is still active by hitting `GET /user`. | §3 endpoint cookbook (`gh auth status` ↔ `GET /user`). |
| [`github-secrets-bulk-set`](../github-secrets-bulk-set/SKILL.md) | Set Actions secrets without `gh`. | §3 endpoint cookbook for the public-key + sealed-value workflow. |
| [`jira-acli-operations`](../jira-acli-operations/SKILL.md) | Create PRs when `gh` is unavailable. | §3 endpoint cookbook — `POST /repos/{o}/{r}/pulls`. |
| [`git-personal-sandbox-remote`](../git-personal-sandbox-remote/SKILL.md) | Create / delete an independent personal repository on GitHub (or GHE) when `gh` is unavailable. | §1.4 GHE base-URL substitution; §3 endpoint cookbook for `POST /user/repos` and `DELETE /repos/{o}/{r}`. |
| [`github-repo-commit-fetch`](../github-repo-commit-fetch/SKILL.md) | Read-only repo data fetch (commits, file at ref) when `gh` is unavailable. | §3 endpoint cookbook — `GET /repos/{o}/{r}/commits`, `GET /repos/{o}/{r}/commits/{sha}`, `GET /repos/{o}/{r}/contents/{p}?ref={sha}`. |
| [`github-actions-workflow-dispatch`](../github-actions-workflow-dispatch/SKILL.md) | Trigger a workflow when `gh` is unavailable. | §3 endpoint cookbook — `POST /repos/{o}/{r}/actions/workflows/{id}/dispatches`. |
| [`github-actions-run-audit`](../github-actions-run-audit/SKILL.md) | Audit workflow runs when `gh` is unavailable. | §3 endpoint cookbook — `GET /repos/{o}/{r}/actions/workflows/{id}/runs`, `GET /repos/{o}/{r}/actions/runs/{id}`. |

***

## 7. Related Skills

- [Terminal Fallback via VS Code Tasks](../terminal-fallback-via-vscode-tasks/SKILL.md) — Required when the
  agent runs REST calls through `create_and_run_task` (no direct shell tool). Provides the file-mediated
  output-capture pattern referenced throughout §2.
- [System-Wide Tool Management](../system-wide-tool-management/SKILL.md) — Use to install `gh` itself when the
  user prefers a one-time install over per-call REST workarounds.
- [Redaction & Portability](../redaction-portability/SKILL.md) — Mandatory: any captured response (`.gh_*.txt`)
  containing emails, internal hostnames, or org names MUST be redacted before being copied into a committed
  artifact.
- [`github-repo-name-conflict-check`](../github/repo/github-repo-name-conflict-check/SKILL.md) — destination
  name-availability checks; this skill's `GET /repos/{o}/{r}` cookbook is the no-`gh` alternative when the
  script's `gh api` path is unavailable.

***

## 8. Traceability

- Originating session: May 2026 — submodule fork discovery for `ai-agent-rules` had to be performed without
  `gh` installed; `GET /repos/<upstream>/forks?per_page=100` via `Invoke-RestMethod` resolved the lookup in a
  single call.
