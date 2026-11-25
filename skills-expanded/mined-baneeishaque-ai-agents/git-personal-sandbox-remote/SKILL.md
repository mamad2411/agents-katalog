---
name: git-personal-sandbox-remote
description: Industrial protocol for backing up personal-only files (build configs, IDE artifacts, experiments) to an independent personal Git repository alongside the team's origin remote, without polluting the team repo via commits or forks.
category: Git & Repository Management
---

# Git Personal Sandbox Remote Skill (v1)

> **Skill ID:** `git-personal-sandbox-remote`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

You have files in a clone of a team repository that:

- MUST be tracked in Git (you want history + remote backup), AND
- MUST NOT reach the team's `origin` (build configs only relevant to you, IDE
  artifacts the team has chosen not to track, personal experiments, sandbox
  patches), AND
- SHOULD NOT appear on the team's upstream as a personal **fork** (forks are
  visible in the upstream's "forks" network list and may surface in team
  notifications / dashboards — some teams find these noisy).

This skill orchestrates the dual-remote workflow that solves all three:

1. Create a brand-new **independent** personal repository (not a fork).
2. Add it as a `personal` remote alongside `origin`.
3. Commit your personal-only files on a dedicated `personal/<purpose>` branch.
4. Push to `personal` ONLY — `origin` is never touched.
5. Maintain the two streams in parallel over time (team work on the team
   branch, personal work on the personal branch).

## When to Apply

Apply this skill when ALL of the following hold:

- The working tree contains tracked or untracked files you want under version
  control with remote backup.
- The team's `origin` should NOT receive those files (team policy, social
  noise, scope hygiene).
- A **fork** is undesirable because it would appear in the team upstream's
  fork network or trigger collaboration features (issues, PRs, notifications).
- The platform is GitHub (`github.com` or GitHub Enterprise Server) where you
  have permission to create a personal repository.

Do NOT apply when:

- The files are intended for upstream eventually — use a **fork + PR** flow
  instead. See [`git-submodule-fork-reconfigure`](../git-submodule-fork-reconfigure/SKILL.md)
  for the fork mechanics.
- The files are throwaway / machine-local only — use `.gitignore` plus the
  [`gitignore-rules`](../gitignore-rules/SKILL.md) skill instead.
- No remote backup is needed — a **local-only branch** (never pushed) is
  simpler than provisioning a personal repository.
- The platform is not GitHub-flavored (GitLab, Bitbucket, Azure DevOps require
  analogous but platform-specific endpoints; this skill's REST examples are
  GitHub-only).

## Composition Rationale

This skill is an **atomic composer** — it orchestrates the following primitives
without re-implementing them:

| Composed Skill | Used for |
|---|---|
| [`github-rest-api-fallback`](../github-rest-api-fallback/SKILL.md) §1.4, §3 | `POST /user/repos` (create) and `DELETE /repos/{o}/{r}` (teardown) when `gh` CLI is unavailable, plus the GHE base-URL `/api/v3/` substitution |
| [`git-github-auth-fallback`](../git-github-auth-fallback/SKILL.md) §3.2.1 | The push-without-`-u` two-step pattern that avoids leaking the PAT into branch tracking config |
| [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md) | The actual commit on the `personal/<purpose>` branch (logical grouping, atomic principle, message quality) |
| [`redaction-portability`](../redaction-portability/SKILL.md) | Sanitizing any conversation log / case study produced from this workflow |

## Related Skills

- [`git-submodule-fork-reconfigure`](../git-submodule-fork-reconfigure/SKILL.md)
  — sibling skill for when a **fork** IS desired (e.g., upstream contribution).
- [`gitignore-rules`](../gitignore-rules/SKILL.md) — alternative for files that
  do not need version control at all.
- [`git-remote-origin-repoint`](../git/repo/git-remote-origin-repoint/SKILL.md) — batch repoint of clone
  remotes (including the `personal` remote) after a repository moves owners, with `git ls-remote`
  verification.
- [`github-repo-name-conflict-check`](../github/repo/github-repo-name-conflict-check/SKILL.md) — verify a
  candidate personal-repo name is available under the account before creating it.

## Composition by Higher-Level Skills

| Composer Skill | Role of this skill in the pipeline |
|---|---|
| [`git-parallel-branch-decommission`](../git-parallel-branch-decommission/SKILL.md) §3c | This skill owns sandbox creation, dual-remote setup, and push hygiene; the decommission composer adds the **rebuild-on-merge-base** fallback when the sandbox already contains the parallel branch's history from an earlier broad `--all` push. |
| [`git-personal-sandbox-restack`](../git-personal-sandbox-restack/SKILL.md) | This skill owns the dual-remote contract; the restack composer keeps the sandbox stacked on top of a moving team branch via `rebase --onto` and a six-axis equality audit before the gated `--force-with-lease` push. |
| [`git-personal-content-extraction`](../git-personal-content-extraction/SKILL.md) | **Prerequisite** for the extraction composer: the `personal` remote and `personal/sandbox` branch created by THIS skill are where the extracted personal commits are slot-inserted (at their original chronological position) at the end of each purification round. |
| [`git-personal-team-branch-workflow`](../git-personal-team-branch-workflow/SKILL.md) | **Prerequisite** for the proactive session-discipline composer — this skill owns the dual-remote setup (`personal` remote + `personal/<purpose>` branch) and guardrails that the team-branch-workflow skill assumes are already in place before the session workflow begins. |

---

## Prerequisites

| Requirement | Minimum |
|---|---|
| VCS | Git 2.x+ |
| Shell | PowerShell 5.1+ or POSIX shell |
| GitHub access | Permission to create repositories under your account on the target host (github.com or GHE) |
| Auth (Route A — preferred) | Git Credential Manager + PAT stored in OS keychain (Windows Vault / macOS Keychain / libsecret). MANDATORY for LFS-enabled remotes. |
| Auth (Route B — non-LFS only) | Personal Access Token (PAT) with `repo` (+ `delete_repo` for teardown) scope, exported via `$env:GITHUB_TOKEN` (process scope) or `[Environment]::SetEnvironmentVariable('GITHUB_TOKEN', ..., 'User')` (persistent) — NEVER pasted in chat |
| Auth (Route C) | `gh` CLI authenticated to the target host |

---

## Decision: Fork vs Independent Personal Repo

| Aspect | Fork | Independent Personal Repo |
|---|---|---|
| Appears in upstream's fork network | **Yes** (visible to every team member) | No |
| Can open PRs back to upstream | Yes (the intended use) | Only after manual `git remote add upstream` + push of upstream history |
| Inherits upstream branches/tags at creation | Yes | No (starts empty) |
| Inherits upstream issues / wiki / settings | Partial | No |
| Triggers "new fork" notifications | Sometimes | Never |
| Permission to create | Only if upstream allows forking | Always (your own namespace) |
| Suitable for "personal sandbox, not upstream-bound" | **No** (social noise) | **Yes** |

**This skill uses the independent personal repo path.** For the fork path, see
[`git-submodule-fork-reconfigure`](../git-submodule-fork-reconfigure/SKILL.md).

---

## Step-by-Step Procedure

### Phase 0 — Environment & Context

#### 0a — Inspect the team remote

```powershell
git -C <repo-path> remote -v
```

Record the host. Two cases:

- **`github.com`** → API base is `https://api.github.com`.
- **Anything else** (e.g., `github.<corp-cloud-domain>`) → GitHub Enterprise.
  API base is `https://<host>/api/v3`. See
  [`github-rest-api-fallback`](../github-rest-api-fallback/SKILL.md) §1.4.

#### 0b — Identify your personal namespace

```powershell
git -C <repo-path> config user.email
```

Map the email to your GitHub username on the target host (you may need to ask
the user if it is non-obvious — corporate NTIDs rarely match the email local
part).

#### 0c — Choose the authentication path

| Path | Trigger | Reference |
|---|---|---|
| **A — `gh` CLI** | `gh --version` succeeds AND `gh auth status` shows the correct host | Phase 1A |
| **B — REST API + PAT** | `gh` unavailable OR not authenticated on the target host | Phase 1B |

For Path B, the user MUST generate a PAT at `https://<host>/settings/tokens`
with scope `repo` and export it as an environment variable — NEVER paste it
in chat. Use one of two methods:

**Method 1 — Process-scope (single shell, fastest):**

```powershell
# Use Read-Host -AsSecureString to avoid the value appearing in shell history
$secure = Read-Host -AsSecureString 'Paste PAT'
$env:GITHUB_TOKEN = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
  [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure))
```

**Method 2 — User-scope (persistent across shells, survives reboot):**

```powershell
$secure = Read-Host -AsSecureString 'Paste PAT'
$plain  = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
  [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure))
[Environment]::SetEnvironmentVariable('GITHUB_TOKEN', $plain, 'User')
```

> [!IMPORTANT]
> **Cross-shell visibility gotcha (Windows):** After `SetEnvironmentVariable
> (..., 'User')`, the variable is NOT visible in the current shell or in
> already-running child shells via `$env:GITHUB_TOKEN`. Only freshly-spawned
> processes inherit the new User-scope value. The agent's execution shell
> is often a long-lived child that does NOT see updates made from a
> different terminal. Two recovery paths:
>
> 1. **Restart the agent's shell** (close + reopen the integrated terminal), OR
> 2. **Read directly from the registry-backed User scope** without relying on
>    process inheritance:
>
>    ```powershell
>    $t = [Environment]::GetEnvironmentVariable('GITHUB_TOKEN','User')
>    # Use $t in subsequent commands instead of $env:GITHUB_TOKEN
>    ```
>
> The direct-read pattern is the agent's preferred fallback because it
> avoids the shell-restart round trip.

**Auth probe** — verify the PAT works against the correct host BEFORE
proceeding to Phase 1:

```powershell
$t = [Environment]::GetEnvironmentVariable('GITHUB_TOKEN','User')
if (-not $t) { $t = $env:GITHUB_TOKEN }
Invoke-RestMethod -Uri 'https://<api-base>/user' `
  -Headers @{ 'Authorization' = "Bearer $t"; 'User-Agent' = 'copilot-agent' } `
  | Select-Object login
```

The `login` field MUST equal `<user>` from Phase 0b. A mismatch means the PAT
belongs to a different identity — STOP and reissue.

> [!CAUTION]
> If a PAT is ever pasted into chat or any persisted artifact, it MUST be
> treated as compromised and revoked immediately at
> `https://<host>/settings/tokens`. See
> [`redaction-portability`](../redaction-portability/SKILL.md) §1 Tier-A.

---

### Phase 1 — Create the Personal Repository

#### 1A — Path A: `gh` CLI

```powershell
gh repo create <user>/<repo-name> --private --description "Personal sandbox: <purpose>"
```

Notes:

- `<repo-name>` MAY be the same as the team repo name (your namespace is
  separate). Same name keeps mental mapping simple.
- `--private` is the recommended default — personal sandboxes rarely need
  public visibility. Override only on explicit user request.
- DO NOT pass `--clone` or `--source` — this skill provisions an **empty**
  repo; you will push your existing local repo's branch into it.

#### 1B — Path B: REST API + PAT

```powershell
$Headers = @{
  'User-Agent'    = 'copilot-agent'
  'Accept'        = 'application/vnd.github+json'
  'Authorization' = "Bearer $env:GITHUB_TOKEN"
}
$Body = @{
  name        = '<repo-name>'
  description = 'Personal sandbox: <purpose>'
  private     = $true
  auto_init   = $false
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri 'https://<api-base>/user/repos' `
  -Headers $Headers `
  -ContentType 'application/json' `
  -Body $Body `
  | ConvertTo-Json -Depth 4 `
  | Out-File .gh_create.txt -Encoding utf8
```

Substitute `<api-base>` per Phase 0a:

- `api.github.com` for github.com
- `<ghe-host>/api/v3` for GitHub Enterprise

`auto_init = $false` is critical — an auto-initialized README would conflict
with the branch you push from your existing repo.

#### 1c — Verify creation

```powershell
# Path A
gh repo view <user>/<repo-name>

# Path B
Invoke-RestMethod -Uri 'https://<api-base>/repos/<user>/<repo-name>' -Headers $Headers `
  | Select-Object full_name, private, clone_url, default_branch
```

---

### Phase 2 — Add the `personal` Remote

```powershell
git -C <repo-path> remote add personal https://<host>/<user>/<repo-name>.git
git -C <repo-path> remote -v
```

Expected output:

```text
origin    https://<host>/<team-org>/<repo>.git (fetch)
origin    https://<host>/<team-org>/<repo>.git (push)
personal  https://<host>/<user>/<repo>.git     (fetch)
personal  https://<host>/<user>/<repo>.git     (push)
```

> [!IMPORTANT]
> The `personal` remote URL MUST be the **clean** form — no embedded PAT.
> Embedding the PAT here would persist it in `.git/config` indefinitely.
> Authentication is handled at push time per Phase 4.

---

### Phase 3 — Create the Personal Branch and Commit

#### 3a — Create the branch

```powershell
git -C <repo-path> checkout -b personal/<purpose>
```

Naming convention: `personal/<purpose>` (e.g., `personal/build-config`,
`personal/ide-settings`, `personal/sandbox-experiment`). The `personal/`
prefix is a visual reminder that the branch must NOT be pushed to `origin`.

#### 3b — Stage and commit

Delegate to [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md)
for the full atomic-commit protocol (analysis, grouping, hunk-based staging,
commit message quality). The personal branch is the commit target instead
of the team branch.

Example:

```powershell
git -C <repo-path> add -- <personal-files>
git -C <repo-path> commit -m "<type>(<scope>): <subject>"
```

---

### Phase 4 — Push to `personal` (PAT-Safe)

> [!CAUTION]
> **LFS-enabled remotes leak embedded-PAT URLs UNCONDITIONALLY.**
> If the remote has Git LFS enabled (most GitHub Enterprise repos with binary
> assets do), `git-lfs` emits an informational stderr line on every push:
>
> ```text
> Locking support detected on remote "https://<user>:<PAT>@<host>/<user>/<repo>.git".
> ```
>
> This line contains the **full embedded-PAT URL** and is written BEFORE any
> stderr-to-file redirect can capture it in some shells (it leaks to the
> parent terminal regardless of `2> file`). Treat any embedded-PAT push to
> an LFS-enabled remote as a guaranteed PAT compromise.
>
> **Detection** — if Phase 0c's auth probe response indicates LFS, OR if
> `git -C <repo> lfs ls-files --all` returns ≥1 row, OR if the source repo
> uses LFS, MANDATE **Route A (Credential Manager)** below. Route B
> (embedded URL) is FORBIDDEN for LFS remotes.

#### 4a — Route A: Git Credential Manager (MANDATORY for LFS remotes; RECOMMENDED otherwise)

Credential Manager stores the PAT in the OS keychain (Windows Credential
Vault / macOS Keychain / `libsecret`), bound to the host. The git URL stays
clean (no `user:PAT@host` form), so no leak surface exists in stderr,
`.git/config`, terminal scrollback, or chat transcripts.

**Setup (once per host)**:

```powershell
# 1. Enable Credential Manager globally
git config --global credential.helper manager

# 2. Clear any prior cached credential for this host
cmdkey /list | Select-String <host>            # show current binding(s)
cmdkey /delete:git:https://<host>              # remove the old one if wrong

# 3. Clear any leaked PAT from environment (defense-in-depth)
[Environment]::SetEnvironmentVariable('GITHUB_TOKEN', $null, 'User')
Remove-Item Env:\GITHUB_TOKEN -ErrorAction SilentlyContinue

# 4. Trigger the credential dialog via a cheap authenticated op
git -C <repo-path> ls-remote personal
#   → Windows "Sign in" dialog appears
#   → Choose "Token" → paste fresh PAT → check "Save credential"
#   → PAT now lives in Credential Vault, bound to <host>

# 5. Verify storage
cmdkey /list | Select-String <host>
#   → must show: Target: git:https://<host>
```

**Push**:

```powershell
# -u is now SAFE because the URL contains no credentials
git -C <repo-path> push -u personal personal/<purpose>
```

**Retrieving the stored PAT for a one-shot REST API call** (e.g., to PATCH
repo settings) without re-prompting the user:

```powershell
$cred = (Write-Output "protocol=https`nhost=<host>`n`n" | git credential fill 2>$null)
$pat  = (($cred | Select-String '^password=').Line -replace '^password=', '')
# … use $pat in Invoke-RestMethod Authorization header …
$pat = $null; [GC]::Collect()    # discard immediately
```

#### 4b — Route B: Embedded-PAT URL (FORBIDDEN for LFS remotes; tolerated for non-LFS one-shots)

When the remote is **not** LFS-enabled and Credential Manager is unavailable
(headless CI, ephemeral environment), the embedded-PAT URL pattern is
tolerated with strict safeguards.

The `-u` flag is **FORBIDDEN** — it would write the embedded-PAT URL into
`.git/config` as the branch's upstream tracking metadata (a second PAT leak
surface beyond the `[remote]` URL). See
[`git-github-auth-fallback`](../git-github-auth-fallback/SKILL.md) §3.2.1.

The correct two-step pattern:

```powershell
# 1. Push WITHOUT -u using a one-shot URL with embedded PAT, stderr to file
$t = [Environment]::GetEnvironmentVariable('GITHUB_TOKEN','User')
$AdHocUrl = "https://<user>:$t@<host>/<user>/<repo>.git"
$log = "$env:TEMP\push_$([guid]::NewGuid()).log"
& git -C <repo-path> push $AdHocUrl personal/<purpose>:personal/<purpose> 2> $log
# Display sanitized stderr (PAT redacted), then delete the log
(Get-Content $log -Raw) -replace [regex]::Escape($t), '<PAT-REDACTED>'
Remove-Item $log
$t = $null; [GC]::Collect()

# 2. Set upstream tracking via the CLEAN named remote (no PAT)
git -C <repo-path> fetch personal
git -C <repo-path> branch --set-upstream-to=personal/personal/<purpose> personal/<purpose>

# 3. Verify tracking points to the named remote (NOT a URL)
git -C <repo-path> branch -vv
git -C <repo-path> config --get branch.personal/<purpose>.remote
```

The `config --get` output MUST be the literal string `personal` — NOT a URL.
If it shows a URL, recover per
[`git-github-auth-fallback`](../git-github-auth-fallback/SKILL.md) §3.2.2.

> [!WARNING]
> The stderr-redaction in step 1 only works for **non-LFS remotes**. For LFS
> remotes git-lfs writes its "Locking support detected" line to the parent
> terminal in a way that bypasses the `2> $log` redirect — the PAT will leak
> to the terminal regardless. Use Route A.

> [!CAUTION]
> PowerShell may render `git push`'s stderr as a red error block even when the
> push succeeded — look for `[new branch]` in the output to confirm success.
> Do not assume failure from the colored framing alone.

#### 4c — Mid-push Recovery: Default-Branch Lock

If you push more than one branch in a single `git push --all` (or push two
branches sequentially before configuring), the **first branch becomes the
remote's default branch** automatically. You then cannot delete it via
`git push --delete` — the remote rejects with:

```text
! [remote rejected]  <branch> (refusing to delete the current branch: refs/heads/<branch>)
```

**Recovery** — switch the default branch via REST PATCH first, then delete:

```powershell
# Pull PAT from Credential Manager (see Route A snippet above for the helper call)
$headers = @{ 'Accept'='application/vnd.github+json'; 'User-Agent'='copilot-agent'; 'Authorization'="Bearer $pat" }
$body    = @{ default_branch = 'personal/<purpose>' } | ConvertTo-Json

# GitHub Enterprise: <api-base> = <host>/api/v3
# github.com:        <api-base> = api.github.com
Invoke-RestMethod -Method Patch `
  -Uri "https://<api-base>/repos/<user>/<repo>" `
  -Headers $headers -ContentType 'application/json' -Body $body

# Now the delete succeeds
git -C <repo-path> push personal --delete <unwanted-branch>
```

This applies whenever `git push --all`, `git push --mirror`, or an accidental
multi-branch push contaminates the personal remote with team branches.
Always prefer **single-branch pushes** (`git push personal personal/<purpose>`)
to avoid this trap entirely.

#### 4d — LFS Object Completeness Pre-Push

A personal sandbox of an LFS-enabled team repo is incomplete (and effectively
read-only on the binary assets) unless all LFS objects are uploaded. The
clone may be a [git-lfs-selective-clone](../git-lfs-selective-clone/SKILL.md)
style pointer-only clone, so most objects are missing locally.

**Audit BEFORE the first push to personal**:

```powershell
# Total unique LFS pointers across all reachable history
git -C <repo-path> lfs ls-files --all | Measure-Object | Select-Object -ExpandProperty Count

# fsck the entire object graph
git -C <repo-path> lfs fsck
```

> [!IMPORTANT]
> The `*` vs `-` marker in `git lfs ls-files --all` indicates **working-tree
> presence at HEAD**, NOT object-store presence. A `-` does NOT mean the
> object is missing from `.git/lfs/objects/`. Use `git lfs fsck` (which
> walks the whole object graph) for ground truth.

**Fetch missing objects from team origin** (cheap, uses team-origin
credentials):

```powershell
git -C <repo-path> lfs fetch --all origin
```

**Verify on-disk storage** matches the expected count and size:

```powershell
$sz = (Get-ChildItem "<repo-path>\.git\lfs\objects" -Recurse -File | Measure-Object -Property Length -Sum)
"files: $($sz.Count)  size: $([math]::Round($sz.Sum/1MB,2)) MB"
```

Only after `lfs fsck` returns OK and all object versions are local should
you push to personal. Otherwise the push hits `(missing) <oid>` mid-upload
and aborts.

---

### Phase 5 — Daily Workflow

Once both branches exist, your day-to-day routine becomes:

| Scenario | Action |
|---|---|
| Personal-file work (build config, sandbox) | Stay on `personal/<purpose>` |
| Team-branch work | `git checkout <team-branch>` (your personal files vanish from the working tree — expected; they only exist on the personal branch) |
| Team commit complete | `git push origin <team-branch>` (NEVER `git push --all`) |
| Rebase personal branch onto latest team work | Delegate to the [`git-personal-sandbox-restack`](../git-personal-sandbox-restack/SKILL.md) composer — it runs `rebase --onto`, resolves DU conflicts, and audits content equality via six axes before the gated `--force-with-lease` push |

> [!WARNING]
> NEVER use `git push --all` or `git push --mirror` — both would push the
> `personal/<purpose>` branch to `origin` (the team repo), defeating the
> entire purpose of this skill. Always push branch-by-branch with explicit
> remote and refspec.

> [!IMPORTANT]
> **Personal-Repo Purity Principle.** The personal repo MUST contain ONLY
> branches that do not exist on the team origin. Pushing team branches to
> personal (via `--all`, `--mirror`, or by mistake) violates the skill's
> contract — the personal repo's `git log` should never duplicate what
> origin already preserves. If contamination happens, recover via Phase 4c
> (default-branch swap + `git push personal --delete <team-branch>`).
>
> **Tags follow the same rule.** Do NOT push team tags to personal
> (`git push personal --tags` is FORBIDDEN). Tags created from personal
> branches and unique to the personal workflow MAY be pushed individually:
> `git push personal <tag-name>`.

### 5a — Guardrail: Prevent accidental `personal/*` push to `origin`

Add a local push refspec that explicitly excludes the personal branches from
`origin`'s default push:

```powershell
# Restrict `origin`'s push behavior to non-personal branches
git -C <repo-path> config --local --add remote.origin.push 'refs/heads/*:refs/heads/*'
git -C <repo-path> config --local --add remote.origin.push '^refs/heads/personal/*'
```

The negation refspec `^refs/heads/personal/*` requires Git 2.29+.

---

### Phase 6 — Teardown (Delete the Personal Repo)

When the personal sandbox is no longer needed, remove the remote repo AND the
local remote.

#### 6a — Path A: `gh` CLI

```powershell
gh repo delete <user>/<repo-name> --yes
```

#### 6b — Path B: REST API

```powershell
Invoke-RestMethod -Method Delete `
  -Uri 'https://<api-base>/repos/<user>/<repo-name>' `
  -Headers $Headers
```

The PAT MUST have `delete_repo` scope (often a separate scope from `repo`).

#### 6c — Remove the local remote and personal branch

```powershell
git -C <repo-path> remote remove personal
git -C <repo-path> branch -D personal/<purpose>
```

---

## Failure Modes

| Symptom | Cause | Resolution |
|---|---|---|
| `git push` returns 401 / 403 against `personal` | Credential Manager has no creds for the new repo OR wrong-identity creds | [`git-github-auth-fallback`](../git-github-auth-fallback/SKILL.md) — choose Path A (helper reset) or Path B (PAT) |
| `git remote add personal …` says "remote personal already exists" | Earlier attempt left the remote | `git remote set-url personal <url>` to update, or `git remote remove personal` first |
| REST `POST /user/repos` returns `422 name already exists` | Personal repo with the same name already exists | Choose a different `<repo-name>`, OR confirm with the user it is the same logical sandbox and reuse it |
| `git branch --set-upstream-to=personal/…` fails: "the requested upstream branch does not exist" | `git fetch personal` was skipped | Run `git fetch personal` first, then re-issue `--set-upstream-to=` |
| `branch.personal/<purpose>.remote` shows a URL with `ghp_…` in it | Phase 4b was executed with `-u` instead of without | Recover per [`git-github-auth-fallback`](../git-github-auth-fallback/SKILL.md) §3.2.2 + revoke the leaked PAT immediately |
| After `git checkout <team-branch>`, personal files reappear as untracked | The personal-branch commit was never made — files were merely staged | Return to `personal/<purpose>` and commit per Phase 3b |

---

## Push Policy

This skill inherits the global push policy: the agent MUST NEVER execute
`git push` automatically. After any commit, the agent MAY offer to push
(e.g., "Push to personal?") but MUST WAIT for explicit user approval.

See [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md)
"Push Policy (GLOBAL)" for the canonical rule.

---

## Traceability

| Session | Topic |
|---|---|
| 2026-05-16 | Origin scenario — Eclipse PDE `build.xml` + `javaCompiler...args` files needed remote backup but team did not want them on `origin`; fork was rejected as socially noisy; resolved via independent personal repo on a GHE instance using REST API (no `gh`). |
