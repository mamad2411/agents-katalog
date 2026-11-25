---
name: git-github-auth-fallback
description: Industrial protocol for recovering from git push / fetch authentication failures against GitHub (HTTP 401 / 403) when credentials are missing, stale, or bound to the wrong identity — covers Credential Manager reset, Personal Access Token re-issue, SSH remote swap, and gh CLI re-authentication.
category: Git-Auth
---

# Git / GitHub Auth Fallback Skill (v1)

This skill defines the recovery protocol when a Git operation against a GitHub remote fails with an
authentication or authorization error — typically `remote: Permission to <owner>/<repo>.git denied to <user>`
or `fatal: ... The requested URL returned error: 403` on `git push`, `git fetch`, or `git ls-remote`.

The root cause is almost never "the repo is wrong"; it is one of:

1. No credentials cached for the remote at all (401).
2. Credentials cached for the **wrong GitHub identity** (the most common cause on shared / work machines —
   surfaces as 403 even though the URL is correct).
3. PAT scope insufficient or PAT expired / revoked.
4. SSH key not loaded into the agent or not associated with the active GitHub account.
5. `gh` CLI authenticated under a different account than the credential helper.

***

## 1. Environment & Dependencies

```powershell
git --version
git config --get credential.helper
git config --global --get user.email
```

Identify the credential helper in use:

- **`manager-core` / `manager`** — Git Credential Manager (default on Windows; also on macOS / Linux via install).
- **`osxkeychain`** — macOS native keychain.
- **`libsecret`** / **`store`** / **`cache`** — Linux options.
- **(empty)** — No helper; Git will prompt every time or fail in non-TTY contexts (e.g., VS Code tasks per
  [Terminal Fallback via VS Code Tasks](../terminal-fallback-via-vscode-tasks/SKILL.md) §4.4).

If the helper is empty AND the agent is running inside a VS Code task (no TTY), the agent MUST stop and surface
the situation to the user — auth fixes for `manager-core` / `osxkeychain` REQUIRE an interactive UI.

Check whether path-based credential isolation is already enabled:

```bash
git config --global --get credential.useHttpPath
# Expected: "true" for multi-account setups, empty otherwise.
```

- **`credential.useHttpPath true`** — Git stores credentials keyed by the full remote URL
  (`https://github.com/owner/repo.git`) instead of by hostname alone. **Required** on macOS when
  two GitHub accounts (personal + company) share the same machine via HTTPS without SSH.
  The macOS `osxkeychain` helper has a known limitation where it may serve the same cached
  credential for all `github.com` paths regardless of this setting — see §3.6 Path F for
  the flush-and-verify workflow and §3.7 Path G for the `.netrc` fallback.

***

## 2. Diagnosis (MUST run before any fix)

Before attempting any remediation, classify the failure exactly:

### 2.1 Capture the remote and the exact error

```powershell
git -C <repo> remote -v
git -C <repo> push <remote> <branch> 2>&1 | Out-File .auth_probe.txt -Encoding utf8
```

Inspect `.auth_probe.txt` for one of these signatures:

| Signature | Classification |
| :--- | :--- |
| `fatal: Authentication failed` | 401 — no credentials, or credentials rejected. |
| `remote: Permission to <owner>/<repo>.git denied to <other-user>` | 403 — wrong identity cached. **Most common on work machines.** |
| `remote: Write access to repository not granted` | 403 — correct identity, missing write scope or collaborator role. |
| `ERROR: Repository not found` (with SSH) | SSH key not associated with the account, OR repo is private and the key has no access. |
| `Could not resolve host: github.com` | Not auth — network / proxy. Out of scope for this skill. |

### 2.2 Identify which GitHub identity Git is offering

For HTTPS remotes via Credential Manager:

```powershell
# Credential Manager GUI on Windows — list stored entries:
git credential-manager get
# Paste the following on stdin, then hit Enter twice:
#   protocol=https
#   host=github.com
# The helper returns the username it would use.
```

For SSH remotes, ask the SSH agent which key would be offered:

```bash
ssh -T git@github.com -v 2>&1 | head -40
```

The verbose output includes `Hi <username>! You've successfully authenticated...` if a key is found, or
`Permission denied (publickey)` if not.

### 2.3 Check credential isolation config (multi-account macOS / Linux)

For HTTPS remotes with multiple GitHub accounts on the same host, verify that Git will
keep credentials separate per repo path:

```bash
git config --global --get credential.useHttpPath
# If empty or "false", Git serves the first credential found for github.com
# to ALL repos — the root cause of cross-account 403 errors.
```

On macOS, also probe which identities are currently stored in the keychain for `github.com`:

```bash
# List every stored github.com credential (username is returned for each entry):
git credential-osxkeychain get <<EOF | grep -E '^(username|password)='
protocol=https
host=github.com
EOF
```

If multiple entries exist with different usernames, the keychain already has mixed
identities — a flush-and-re-auth cycle is needed (see §3.1 Path A for the generic flush,
§3.6 Path F for the `useHttpPath` workflow).

***

## 3. Remediation Paths (Pick One)

Each path is a complete, standalone fix. The agent MUST present the options to the user, recommend one based on
the diagnosis, and proceed only after the user confirms.

### 3.1 Path A — Reset Credential Manager and re-authenticate (RECOMMENDED for "wrong identity" 403)

> [!CAUTION]
> This path is interactive — it requires the user to run the commands in a real terminal, not inside a VS Code
> task. The agent MUST surface the commands and wait for confirmation.

```powershell
# Windows
git credential-manager erase
# Paste on stdin:
#   protocol=https
#   host=github.com
# (Enter twice)

# Then trigger the next push, which will open the GCM browser prompt:
git -C <repo> push <remote> <branch>
# Sign in as the correct account in the browser window that opens.
```

```bash
# macOS (osxkeychain helper)
git credential-osxkeychain erase <<EOF
protocol=https
host=github.com
EOF

# Linux (libsecret / store)
git credential-libsecret erase <<EOF
protocol=https
host=github.com
EOF
```

After re-auth, re-probe with `git push` and verify the captured output shows success.

### 3.2 Path B — Personal Access Token in the remote URL (NON-INTERACTIVE)

When the agent must complete the push inside a non-TTY environment (e.g., CI, VS Code task), embed a PAT
directly. The token MUST come from an environment variable and MUST NEVER be committed.

**Preferred form — temporary `remote set-url` with immediate revert:**

```powershell
$env:GITHUB_PAT = '<user-paste-pat-here>'
git -C <repo> remote set-url <remote> "https://$env:GITHUB_PAT@github.com/<owner>/<repo>.git"
git -C <repo> push <remote> <branch>
# IMMEDIATELY revert the URL so the PAT does not persist in .git/config:
git -C <repo> remote set-url <remote> "https://github.com/<owner>/<repo>.git"
```

> [!CAUTION]
> The PAT lives in `.git/config` between the `set-url` and the revert. The agent MUST execute the revert in the
> same task / same shell session as the push to minimize exposure. NEVER capture the URL form with the PAT
> embedded into a log file, commit message, or session note — this is a Tier-A redaction violation per
> [Redaction & Portability](../redaction-portability/SKILL.md) §1.

#### 3.2.1 FORBIDDEN — `git push -u <embedded-PAT-URL>` form

DO NOT use this shape when establishing upstream tracking for a brand-new branch:

```powershell
# ❌ ANTI-PATTERN — leaks PAT into TWO places:
git -C <repo> push -u "https://user:$env:GITHUB_PAT@github.com/<owner>/<repo>.git" <branch>:<branch>
```

**Why it's worse than §3.2:** The `-u` flag writes the full URL (with embedded PAT) into `.git/config` as the
branch's upstream tracking metadata — specifically:

```ini
[branch "<branch>"]
    remote = https://user:ghp_xxx...@github.com/<owner>/<repo>.git
    merge = refs/heads/<branch>
```

This is **separate** from `[remote]` URL config and is **not** cleaned up by `git remote set-url`. The PAT
persists in `.git/config` indefinitely until the user notices.

**Correct two-step pattern when the named remote does not yet exist or you want to push to an ad-hoc URL:**

```powershell
# 1. Push WITHOUT -u (no upstream tracking written)
$AdHocUrl = "https://user:$env:GITHUB_PAT@github.com/<owner>/<repo>.git"
git -C <repo> push $AdHocUrl <branch>:<branch>

# 2. Add the named remote with the CLEAN URL (no PAT) and set tracking via fetch
git -C <repo> remote add <remote-name> "https://github.com/<owner>/<repo>.git"
git -C <repo> fetch <remote-name>
git -C <repo> branch --set-upstream-to=<remote-name>/<branch> <branch>

# 3. Verify tracking points to the named remote, NOT a URL
git -C <repo> branch -vv     # Output should show [<remote-name>/<branch>], no http://
git -C <repo> config --get branch.<branch>.remote   # Should print the remote name, not a URL
```

#### 3.2.2 Recovery — cleaning up a leaked PAT in branch tracking config

If the `-u <embedded-PAT-URL>` form was already executed, surface and scrub:

```powershell
# Detect: any branch config that has a full URL (instead of a remote name) as its remote target
git -C <repo> config --list --local | Select-String 'branch\..*\.remote=https?://'

# Scrub by re-pointing the branch to a named remote
git -C <repo> fetch <remote-name>
git -C <repo> branch --set-upstream-to=<remote-name>/<branch> <branch>

# Verify the URL form is gone
git -C <repo> config --list --local | Select-String 'branch\..*\.remote='
```

The leaked PAT MUST also be **revoked at the issuing host** (`https://<host>/settings/tokens`) the moment it
is cleaned from disk — `.git/config` is plaintext and may have been backed up, indexed, or sync'd to cloud
storage in the meantime.

The PAT must have scope:

- **`repo`** — for write access to private repos and to public repos when you are not a collaborator.
- **`workflow`** — for pushing changes that modify `.github/workflows/*`.

#### 3.2.3 FORBIDDEN — embedded-PAT URL push to an LFS-enabled remote

Git LFS is GitHub Enterprise's default storage for binary assets. When the
target remote is LFS-enabled, `git-lfs` emits an informational stderr line
on every push:

```text
Locking support detected on remote "https://<user>:<PAT>@<host>/<owner>/<repo>.git".
Consider enabling it with:
  $ git config lfs.https://<user>:<PAT>@<host>/<owner>/<repo>.git/info/lfs.locksverify true
```

The line is written by `git-lfs` directly to the controlling terminal in
a way that bypasses parent-shell `2> $logFile` redirection on Windows /
PowerShell. The embedded PAT therefore leaks to:

1. The terminal scrollback (visible to anyone with desktop access)
2. The agent's tool-call transcript (which forwards terminal output as
   conversation context)
3. Any chat client rendering the transcript

Even with sanitization on the parent shell's captured output, the
unsanitized form reaches the chat client first.

**Detection** — assume the remote is LFS-enabled if ANY of the following hold:

- The repo contains a `.gitattributes` line with `filter=lfs`
- `git -C <repo> lfs ls-files --all` returns ≥ 1 row
- The remote hostname is a GitHub Enterprise instance with binary assets
  (most internal corp deployments)

**Mandate** — for LFS-enabled remotes, use **Git Credential Manager** (the
URL stays clean, the PAT lives in the OS keychain). See
[`git-personal-sandbox-remote`](../git-personal-sandbox-remote/SKILL.md)
§4a for the dialog-trigger sequence and the `git credential fill` pattern
for retrieving the stored PAT for one-shot REST calls.

**If a PAT leak via this path has already occurred:**

1. **Revoke immediately** at `https://<host>/settings/tokens` — the leaked
   PAT MUST be considered compromised regardless of how briefly it appeared.
2. Clear local exposures via §3.2.2.
3. Wipe terminal scrollback (`Clear-Host` is NOT sufficient — close the
   terminal entirely; some shells persist scrollback to disk).
4. Reissue a fresh PAT and bind via Credential Manager per
   [`git-personal-sandbox-remote`](../git-personal-sandbox-remote/SKILL.md)
   §4a — do NOT export the new PAT to any environment variable.

### 3.3 Path C — Switch the remote to SSH

When the user has an SSH key already associated with the correct GitHub account, swap the protocol:

```powershell
git -C <repo> remote set-url <remote> "git@github.com:<owner>/<repo>.git"
git -C <repo> push <remote> <branch>
```

Verify the key is loaded:

```bash
ssh-add -L                   # Lists keys currently held by the agent.
ssh -T git@github.com        # Prints "Hi <user>!" on success.
```

If `ssh-add -L` reports "The agent has no identities", load the key:

```bash
ssh-add ~/.ssh/id_ed25519
```

For permanent SSH key registration on GitHub, see <https://github.com/settings/keys>.

### 3.4 Path D — Re-authenticate via `gh` CLI

When `gh` is installed, it can manage credentials for both itself and for Git (via `gh auth setup-git`):

```bash
gh auth status
gh auth login                # Interactive — browser or token paste.
gh auth setup-git            # Configures git's credential helper to defer to gh.
git -C <repo> push <remote> <branch>
```

If `gh` is absent, install it via [System-Wide Tool Management](../system-wide-tool-management/SKILL.md), or
fall back to Path A / B / C.

### 3.5 Path E — Validate a PAT without git (REST API probe)

Before retrying a push, the agent can validate a candidate PAT via the GitHub REST API:

```powershell
$Headers = @{
  'User-Agent'    = 'copilot-agent'
  'Authorization' = "Bearer $env:GITHUB_PAT"
}
Invoke-RestMethod -Uri 'https://api.github.com/user' -Headers $Headers `
  | ConvertTo-Json -Depth 3 | Out-File .pat_probe.txt -Encoding utf8
```

The response object's `login` field is the GitHub username the PAT belongs to. If `login` does NOT match the
account that owns / has write access to the target repo, the PAT is wrong — go back to step 1 of the chosen
path. For full REST patterns, defer to [GitHub REST API Fallback](../github-rest-api-fallback/SKILL.md).

### 3.6 Path F — macOS `credential.useHttpPath` for multi-account HTTPS (RECOMMENDED for macOS)

Use when: macOS, two or more GitHub accounts (personal + company), HTTPS remotes, no SSH,
and the user wants a clean credential-per-repo setup without embedding tokens in URLs or
switching to SSH.

> [!CAUTION]
> This path is partly interactive — the initial push after the flush opens a dialog or
> browser prompt to re-authenticate. The agent MUST surface the commands and wait for
> confirmation.

```bash
# 1. Enable path-keyed credential isolation
git config --global credential.useHttpPath true

# 2. Flush ALL stored credentials for github.com from the macOS keychain.
#    Without this step, the old (wrong-identity) credential is served for every path.
git credential-osxkeychain erase <<EOF
protocol=https
host=github.com
EOF

# 3. Push to the company repo — macOS prompts for fresh credentials.
#    Enter the COMPANY GitHub username and PAT (password field).
git -C <repo> push <remote> <branch>

# 4. On success, subsequent pushes to personal repos prompt separately
#    because the full URL path differs (credential.useHttpPath).
```

**How it works:** `credential.useHttpPath true` tells Git to key stored credentials by
the full remote URL (`https://github.com/org/repo.git`) instead of just the hostname
(`github.com`). After flushing the old hostname-keyed entry, each repo path gets its
own credential entry in the keychain — personal and company accounts never collide.

#### 3.6.1 Verification — per-path credential isolation

```bash
# Probe what credential the helper would serve for the company repo:
git credential-osxkeychain get <<EOF
protocol=https
host=github.com
path=org/company-repo.git
EOF
# Returns the company username

# Probe for a personal repo:
git credential-osxkeychain get <<EOF
protocol=https
host=github.com
path=personal/repo.git
EOF
# Returns the personal username (different)
```

#### 3.6.2 Recovery — if the old identity keeps being served

If `osxkeychain` ignores `useHttpPath` (a known macOS limitation documented in
[git-credential-osxkeychain](https://github.com/git/git/blob/master/Documentation/git-credential-osxkeychain.txt)),
fall through to §3.7.

### 3.7 Path G — `.netrc` fallback when `osxkeychain` ignores `useHttpPath`

Use when: Path F was attempted but the macOS `osxkeychain` helper still returns the
wrong identity — the helper does not honour `credential.useHttpPath` on some macOS
versions. Switch the company repo to a repo-level `netrc` helper, bypassing the
keychain for that repo only:

```bash
# 1. Create ~/.netrc with strictly restricted permissions
touch ~/.netrc
chmod 600 ~/.netrc
```

Add the company credentials (replace placeholders):

```text
machine github.com
login <company-github-username>
password <company-pat>
```

```bash
# 2. Configure the company repo to use netrc instead of osxkeychain
git config --local credential.helper 'netrc -f ~/.netrc'

# 3. Push — netrc serves the company credentials; osxkeychain still serves personal repos
git -C <repo> push <remote> <branch>
```

> [!CAUTION]
> `.netrc` stores credentials in **plaintext**. The `chmod 600` restriction is mandatory.
> Do NOT use this path on shared or CI machines. Prefer Path F for all normal macOS
> workstations.

#### 3.7.1 Reverting to keychain

Once the keychain limitation is resolved (macOS update, credential helper change,
or the user prefers keychain-based auth), remove the repo-level override:

```bash
git config --local --unset credential.helper
```

### 3.8 Path H — `git credential fill` identity probe (RECOMMENDED before ANY other path)

Use when: any 401 / 403, on ANY helper (osxkeychain / manager-core / libsecret),
and the remote URL has been verified correct — the agent MUST establish which
identity the credential helper is about to offer BEFORE mutating anything.
This is the cheapest, least-destructive probe in the skill; run it first.

```bash
# Probe: what identity would Git offer for github.com right now?
printf 'protocol=https\nhost=github.com\n\n' | git credential fill
# Output: username=<identity> and password=<secret> lines if a credential exists,
# or the helper falls through / errors when nothing is stored.

# Path-scoped variant (multi-account setups, mirrors §3.6.1):
printf 'protocol=https\nhost=github.com\npath=%s/%s.git\n\n' '<owner>' '<repo>' | git credential fill
```

Interpretation:

| Probe result | Diagnosis | Next step |
| :--- | :--- | :--- |
| `username=<expected-identity>` | Helper state is correct; failure is scope / network / server-side. | Path E (PAT validation) then re-push. |
| `username=<other-identity>` | Wrong identity cached. | Path A (flush + re-auth) or Path F for useHttpPath setups. |
| Empty / helper error | No credential stored for this context. | Path A or Path D (re-auth); never Path B unless non-interactive is mandated. |

**Session-poisoning sub-case (the agent's OWN earlier work is the root cause):**
when the agent previously used Path B (PAT in an env var) or the bare
`git push -u <PAT-URL>` anti-pattern for ANOTHER repo in the same machine
session, the leftover `GITHUB_PAT` env var or a repo-local
`credential.helper` entry can serve the WRONG identity to every later repo
in the session — while the keychain itself is healthy.

```bash
# 1. Prove the poisoning source:
env | grep -iE '^(gh|git)_|_pat='          # session env carrying a token
git config --show-origin --get-all credential.helper
#    ^-- lines starting with file:<scope> show which scope set the helper

# 2. Neutralize the poisoned source:
export -n GITHUB_PAT GH_TOKEN              # zsh / bash: unset from THIS session
git config --local --unset credential.helper    # only if the local scope set one

# 3. Re-probe — the helper must now answer with the expected identity:
printf 'protocol=https\nhost=github.com\n\n' | git credential fill
```

> [!CAUTION]
> The `git credential fill` output includes the stored password/PAT on
> stdout. Treat the probe as Tier-A redaction material per
> [Redaction & Portability](../redaction-portability/SKILL.md) §1: capture
> ONLY the `username=` line into logs / notes, never the `password=` value.

***

## 4. Decision Matrix

| Scenario | Recommended Path | Rationale |
| :--- | :--- | :--- |
| Work laptop, Credential Manager cached a corp / coworker identity, push to personal repo → 403 | A (reset & re-auth) | Cleanest; future pushes auto-resolve. |
| CI / VS Code task / non-TTY environment, must push now | B (PAT in URL, immediately reverted) | Only non-interactive option. |
| User already has SSH keys, hates browser prompts | C (SSH remote) | No credentials in HTTPS layer at all. |
| User wants `gh`-managed flow for `pr create`, `issue`, etc. anyway | D (`gh auth login`) | Single helper for both git push and GitHub API. |
| Uncertain whether the PAT has the right scope | E first, then B or A | Cheap pre-flight check before mutating remote URL. |
| macOS + two GitHub accounts (personal + company) + HTTPS, no SSH | F (`useHttpPath`) | Keys credentials per repo path; cleanest non-SSH option. |
| macOS + `useHttpPath` still serves wrong identity after flush | G (`.netrc` fallback) | Bypass osxkeychain for the company repo only. |
| Any 401/403 on a verified-correct URL — probe before mutating | H (`git credential fill` probe) | Cheap, read-only; pinpoints the helper's identity and exposes session env-var poisoning from earlier Path-B work. |

***

## 5. Verification

After remediation, the push MUST produce visible success output:

```powershell
git -C <repo> push <remote> <branch> 2>&1 | Out-File .auth_verify.txt -Encoding utf8
# Inspect .auth_verify.txt for one of:
#   "Everything up-to-date"  (no commits to push but auth worked)
#   "To <url>"                followed by ref update lines
```

Additionally, confirm the working tree's tracking branch is in sync:

```powershell
git -C <repo> status -sb
# Expect: ## <branch>...<remote>/<branch>   (no [ahead N])
```

***

## 6. Composition by Higher-Level Skills

| Composer | Role | Reuses From This Skill |
| :--- | :--- | :--- |
| [`git-submodule-fork-reconfigure`](../git-submodule-fork-reconfigure/SKILL.md) | When `git push` to an upstream fails with 403, distinguish "needs forking" from "wrong identity cached". | §2 diagnosis matrix, §3 remediation paths. |
| [`git-submodule-fork-sync`](../git-submodule-fork-sync/SKILL.md) | Push to the realigned `origin` may surface a 401 / 403. | §2 classification before forking or reconfiguring further. |
| [`git-submodule-orphan-gitlink-recovery`](../git-submodule-orphan-gitlink-recovery/SKILL.md) | Auth failures while reconfiguring orphan gitlinks. | §2 classification, §3 remediation. |
| [`git-branch-promotion`](../git-branch-promotion/SKILL.md) | Force-push step blocked by auth. | §3 paths to restore push capability before §4 force-push. |
| [`github-secrets-bulk-set`](../github-secrets-bulk-set/SKILL.md) | `gh secret set` fails with 401 / 403. | §3.4 / §3.5 PAT validation. |
| [`jira-acli-operations`](../jira-acli-operations/SKILL.md) | `gh pr create` fails on the PR step. | §3.4 `gh auth login` flow. |
| [`git-personal-sandbox-remote`](../git-personal-sandbox-remote/SKILL.md) | Push a brand-new personal branch to a freshly-created `personal` remote without leaking the PAT into branch tracking config. | §3.2.1 push-without-`-u` two-step pattern; §3.2.2 leaked-PAT recovery. |
| [`git-submodule-history-removal`](../git/submodule/lifecycle/git-submodule-history-removal/SKILL.md) | Forced push (`--force-with-lease`) of a rewritten branch rejected with 401/403. | §3.8 Path H identity probe first (cheap, read-only), then §3 paths; §5 push verification. |

***

## 7. Related Skills

- [Terminal Fallback via VS Code Tasks](../terminal-fallback-via-vscode-tasks/SKILL.md) — §4.4 explicitly
  forbids running interactive credential-manager commands inside a task. This skill defers to that constraint
  by surfacing interactive paths back to the user.
- [GitHub REST API Fallback](../github-rest-api-fallback/SKILL.md) — Used for Path E (PAT validation) and any
  follow-up GitHub operation once auth is restored.
- [System-Wide Tool Management](../system-wide-tool-management/SKILL.md) — Use to install `gh`, `git`, or SSH
  key tooling if missing.
- [Redaction & Portability](../redaction-portability/SKILL.md) — Mandatory: PATs, account usernames, and
  internal-org email addresses are all Tier-A and MUST be redacted before any artifact is committed.
- [`github-repo-account-transfer`](../github/transfer/github-repo-account-transfer/SKILL.md) — the transfer
  pipeline resolves per-account tokens (`gh auth token --user`) and can surface 401/403 at the initiate or
  repoint stages; use this skill's §3 paths to restore the failing account's auth first.

***

## 8. Traceability

- Originating session: May 2026 — `git push` of `ai-agent-rules` failed with `HTTP 403` because Git Credential
  Manager on a work laptop was supplying credentials for the corp identity instead of the personal GitHub
  account that owns the fork. The resolution required identifying the cached identity, then switching to a
  fork-based remote (per [Git Submodule Fork Reconfigure](../git-submodule-fork-reconfigure/SKILL.md)) under
  the correct account.
- June 2026 — macOS HTTPS multi-account auth: `git push` to company repo returned 403 because macOS Keychain
  cached the personal GitHub identity while the company repo URL was correct. Resolution: set
  `credential.useHttpPath true`, flushed all `github.com` entries from the keychain, then pushed. Per-repo-path
  isolation (enabled by `useHttpPath`) kept personal and company credentials separate. Documented as §3.6
  Path F and §3.7 Path G.
- August 2026 — `git credential fill` probe added as §3.8 Path H: the read-only identity probe run before any
  destructive path, plus the session-poisoning sub-case (agent's own earlier Path-B work leaving `GITHUB_PAT`
  / a repo-local helper that serves the wrong identity to later repos in the same session). Introduced as the
  first probe for the `git-submodule-history-removal` push gate (401/403 on a forced push of a rewritten
  branch).
