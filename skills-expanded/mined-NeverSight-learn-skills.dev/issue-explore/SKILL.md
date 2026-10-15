---
name: issue-explore
description: >
  Fetches a work item from GitLab, GitHub, Jira, or Plane (auto-detected from the reference
  format or URL) and starts opsx:explore with the issue context and code repository context
  pre-loaded. Use when a user mentions a ticket number, issue key, or issue URL and wants
  to explore the implementation before starting a change. Works correctly when the issue
  tracker and the code host are different systems (e.g. Jira issues + GitLab code).
compatibility: >
  Requires git. Fetch method is resolved in order: glab/gh/jira CLI → MCP server → API token env var.
metadata:
  author: pavan.katakam@senecaglobal.com
  providers: gitlab, github, jira, plane
---

# issue-explore

Fetch a work item from any supported issue tracker and load it into `opsx:explore`.
The issue tracker and the code host are treated **independently** — a Jira ticket in a
GitLab-backed repo, or a Plane issue with a GitHub codebase, is the normal case, not an edge case.

## Usage

```
# ✅ Always works — no setup needed:
/issue-explore https://gitlab.company.com/group/project/-/issues/123
/issue-explore https://github.com/owner/repo/issues/123
/issue-explore https://company.atlassian.net/browse/PROJ-123
/issue-explore PROJ-123                    # Jira key format — always auto-detected
/issue-explore https://app.plane.so/my-workspace/projects/proj-uuid/issues/issue-uuid/

# ⚙️  Needs GITHUB_TOKEN / GITLAB_TOKEN or a matching git remote:
/issue-explore owner/repo#123              # GitHub repo + number
/issue-explore group/project#123          # GitLab project + IID
/issue-explore 123                         # bare number — provider inferred from tokens/remote/git log

# Flags:
/issue-explore PROJ-123 --no-branch        # skip branch creation, exploration-only
```

## Provider registry

Provider detection, URL patterns, CLI tools, and token names are declared in **[references/providers.json](references/providers.json)** — adding a new tracker only requires a new entry there plus a reference file.

| Provider | Detected by | Reference file |
|----------|-------------|----------------|
| GitLab   | hostname matches `gitlab.com` / `*.gitlab.com` / `*gitlab*` | [references/gitlab.md](references/gitlab.md) |
| GitHub   | hostname matches `github.com` / `*.github.com` | [references/github.md](references/github.md) |
| Jira     | hostname matches `*.atlassian.net` / `jira.*` | [references/jira.md](references/jira.md) |
| Plane    | hostname matches `app.plane.so` / `*.plane.so` | [references/plane.md](references/plane.md) |

To add a new provider, see [references/adding-providers.md](references/adding-providers.md).

**Self-hosted / custom domains**: set `ISSUE_EXPLORE_HOSTS` in your shell profile:
```bash
export ISSUE_EXPLORE_HOSTS='{"git.corp.com":"gitlab","jira.corp.com":"jira"}'
```
Entries in this map use fnmatch wildcards and override all registry patterns.

---

## Steps

Follow Steps 1–6 in order. Steps 3–5 delegate to the provider's reference file.

---

### Step 1 — Detect provider and parse reference

Provider metadata is loaded from `references/providers.json`. Steps 1 and 2 iterate the registry instead of hardcoding per-provider logic — this is how new providers are added without touching SKILL.md.

```python
import re, os, json, fnmatch
from urllib.parse import urlparse

# Load provider registry
_reg_path = os.path.join(os.path.dirname(__file__), "references", "providers.json")
PROVIDERS  = json.load(open(_reg_path))["providers"]   # list of provider dicts

def _host_matches(host, patterns):
    """Return True if host matches any pattern (exact or fnmatch wildcard)."""
    for p in patterns:
        if fnmatch.fnmatch(host, p):
            return True
    return False

def _provider_for_host(host):
    # 1. User-defined overrides (ISSUE_EXPLORE_HOSTS env var)
    custom = json.loads(os.environ.get("ISSUE_EXPLORE_HOSTS", "{}"))
    for k, v in custom.items():
        if fnmatch.fnmatch(host, k) or host == k:
            return v
    # 2. GITLAB_URL legacy fallback
    gl = os.environ.get("GITLAB_URL","").rstrip("/")
    if gl and host in gl:
        return "gitlab"
    # 3. Registry patterns
    for prov in PROVIDERS:
        if _host_matches(host, prov["hostname_patterns"]):
            return prov["name"]
    return None
```

The input is one of three forms — handle each differently.

**Case A — Full URL** (`http://` or `https://`): hostname identifies the provider; path is parsed by the registry's `url_path_patterns`.

```python
arg   = "ARG"          # substitute user's argument
parsed = urlparse(arg)
host   = parsed.hostname or ""
path   = parsed.path

provider = None; project_ref = None; issue_id = None; parse_failed = False

# A1 — provider from hostname (via registry + ISSUE_EXPLORE_HOSTS override)
provider = _provider_for_host(host)

# A2 — project + issue from registry url_path_patterns
#      (newest pattern first, never delete old ones — add to providers.json instead)
if provider:
    prov_def = next((p for p in PROVIDERS if p["name"] == provider), None)
    patterns = prov_def["url_path_patterns"] if prov_def else []
    for p in patterns:
        m = re.search(p, path)
        if m:
            if provider == "jira":
                issue_id = m.group(1); project_ref = issue_id.split("-")[0]
            else:
                project_ref, issue_id = (m.group(1).strip("/"), m.group(2)) if m.lastindex >= 2 else (None, m.group(1))
            break
    else:
        parse_failed = True
```

If `parse_failed`: ask the user for the issue ID (and project path if needed), then say:
> "The URL path format for [provider] may have changed. Add the new pattern to the provider's patterns list in `references/[provider].md` — newest first, never delete old ones."

If `provider` is None: ask "Which tracker is this URL from?" then say:
> "Set `GITLAB_URL=https://your-host` for self-hosted GitLab, or add a hostname rule to Step 1 Case A."

**Case B — String (non-numeric, no URL)**:

```python
import re, subprocess

def git_remote():
    try: return subprocess.check_output(["git","remote","get-url","origin"], stderr=subprocess.DEVNULL).decode().strip()
    except: return ""

if re.match(r'^[A-Z][A-Z0-9_]+-\d+$', arg):          # Jira key: PROJ-123
    provider = "jira"; issue_id = arg; project_ref = arg.split("-")[0]
elif "#" in arg:
    project_ref, issue_id = arg.split("#", 1)
    provider = "github" if "github.com" in git_remote() else "gitlab"
else:
    provider = None
```

If `provider` is None: ask which tracker, then say:
> "Use `PROJ-123` for Jira (always auto-detected) or `group/project#NNN` for GitLab/GitHub."

**Case C — Bare number**: resolve provider via heuristics in this order — do not prompt unless all heuristics fail.

```python
import os, re, subprocess

# git_remote() defined above in Case B — reuse it here.

def _parse_repo(remote):
    """Return repo path from a git remote URL, or None if unparseable."""
    if not remote:
        return None
    if remote.startswith("http"):
        path = re.sub(r'https?://[^/]+/', '', remote).rstrip('.git')
        return path or None
    m = re.search(r':(.+?)(?:\.git)?$', remote)
    return m.group(1) if m else None

def _recent_issue_key_provider():
    """Scan the last 100 commit messages for Jira/GitHub/GitLab issue keys.
    Returns the provider whose key format appears most recently, or None."""
    try:
        log = subprocess.check_output(
            ["git","log","--oneline","-100"], stderr=subprocess.DEVNULL).decode()
    except:
        return None
    if re.search(r'[A-Z][A-Z0-9_]+-\d+', log):   return "jira"
    if re.search(r'#\d+',                  log):   return "github_or_gitlab"
    return None

issue_id = arg; remote = git_remote()
has_gitlab = bool(os.environ.get("GITLAB_TOKEN"))
has_github = bool(os.environ.get("GITHUB_TOKEN"))
remote_provider = "github" if "github.com" in remote else ("gitlab" if remote else None)
log_hint = _recent_issue_key_provider()

# Resolution priority: remote+token → token only → git log hint
if   remote_provider == "github" and has_github: provider = "github"; project_ref = _parse_repo(remote)
elif remote_provider == "gitlab" and has_gitlab: provider = "gitlab"; project_ref = _parse_repo(remote)
elif has_gitlab and not has_github:              provider = "gitlab"; project_ref = _parse_repo(remote)
elif has_github and not has_gitlab:              provider = "github"; project_ref = _parse_repo(remote)
elif log_hint == "jira":                         provider = "jira";   project_ref = None   # jira key required — ask
else:                                            provider = None
```

If `provider` is None: **do not show a generic error**. Instead tell the user exactly what is missing and what to do:

> Couldn't auto-detect the issue tracker for **#[arg]**.
>
> The fastest fixes:
> | What you have | Do this |
> |---|---|
> | GitLab project | Set `GITLAB_TOKEN` and ensure `git remote get-url origin` returns a GitLab URL |
> | GitHub repo | Set `GITHUB_TOKEN` and ensure the remote points to `github.com` |
> | Jira | Use `PROJ-[arg]` — Jira keys always auto-detect |
> | Any | Pass the full issue URL instead: `/issue-explore https://...` |
>
> Once set, re-run `/issue-explore [arg]`.

If `provider == "jira"` but `log_hint == "jira"` and no Jira key format can be derived:
> Recent commits suggest this is a Jira project. Please use the full key format: `PROJ-[arg]` (replace `PROJ` with your project key).

```python
if not provider or not issue_id:
    raise SystemExit("BUG: provider/issue_id unresolved")
```

---

### Step 1b — Capture code repository context

Run unconditionally — independent of which issue provider was detected.

```bash
python3 - <<'PY'
import subprocess, re, os

def run(cmd):
    try: return subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip()
    except: return ""

remote  = run(["git","remote","get-url","origin"])
branch  = run(["git","rev-parse","--abbrev-ref","HEAD"])
commits = run(["git","log","--oneline","-10"])

code_host = "github" if "github.com" in remote else ("gitlab" if remote else "unknown")
if remote.startswith("http"):
    repo_path = re.sub(r'https?://[^/]+/','',remote).rstrip('.git')
else:
    m = re.search(r':(.+?)(?:\.git)?$', remote)
    repo_path = m.group(1) if m else ""

print(f"CODE_HOST={code_host}")
print(f"CODE_REPO={repo_path}")
print(f"CODE_REMOTE={remote}")
print(f"CODE_BRANCH={branch}")
print("CODE_COMMITS:")
for line in (commits.splitlines() or ["(none)"]): print(f"  {line}")
PY
```

If not in a git repo, set all to empty and continue.

**Carry forward**: keep `CODE_HOST`, `CODE_REPO`, `CODE_REMOTE`, `CODE_BRANCH`, and `CODE_COMMITS` in memory — they are substituted verbatim into Step 6's context block.

---

### Step 2 — Resolve fetch method

Resolve in this order — use the **first** method that is available:

1. **CLI** — check whether the provider CLI exists: `glab` (GitLab), `gh` (GitHub), `jira` (Jira).
2. **MCP** — scan the `system-reminder` tags in the current context for tool names that start with `mcp__gitlab__`, `mcp__github__`, or `mcp__jira__` (matching the detected provider). If any such tool is present, MCP is available.
3. **API token** — check env vars: `GITLAB_TOKEN`, `GITHUB_TOKEN`, or `JIRA_TOKEN`.
4. **none** — none of the above is available.

```python
import shutil, os, json

# Load registry (PROVIDERS already loaded in Step 1 — reuse it)
prov_def = next((p for p in PROVIDERS if p["name"] == PROVIDER), None)
cli_tool  = prov_def["cli_tool"]   if prov_def else ""
token_env = prov_def["token_env"]  if prov_def else ""
mcp_pfx   = prov_def["mcp_prefix"] if prov_def else f"mcp__{PROVIDER}__"

if shutil.which(cli_tool):
    FETCH_METHOD = "cli"
elif mcp_available_for(PROVIDER):   # scan system-reminder for tools starting with mcp_pfx
    FETCH_METHOD = "mcp"
elif os.environ.get(token_env):
    FETCH_METHOD = "api"
else:
    FETCH_METHOD = "none"
```

`mcp_available_for(provider)` is not a real function — it means: scan the `system-reminder` section of your context for any tool whose name starts with `mcp_pfx` (from the registry). If found, the result is `True`.

If `FETCH_METHOD=none`: ask the user for the token, set `FETCH_METHOD=api`, then show this table:

| Provider | Fastest permanent fix |
|----------|-----------------------|
| GitLab | `glab auth login` (installs `glab`) |
| GitHub | `gh auth login` (installs `gh`) |
| Jira | `jira init` (installs `jira-cli`) |
| Plane | `export PLANE_API_TOKEN=<token>` — get token at [app.plane.so/profile/api-tokens/](https://app.plane.so/profile/api-tokens/) |
| Any | Configure provider MCP server in Claude Code |
| Fallback | `export GITLAB_TOKEN / GITHUB_TOKEN / JIRA_TOKEN / PLANE_API_TOKEN` in shell profile |

**Carry forward**: keep `FETCH_METHOD` in memory — pass it explicitly to `references/[provider].md` in Step 3 so the provider file knows which fetch path to use.

---

### Step 3 — Fetch and normalize

> **Tell the user before starting this step:**
> ```
> Fetching [issue.provider] issue [issue.id]…
> ```
> After each sub-step completes, emit a one-line status so the user knows progress:
> - After Step A: `✓ Issue loaded: "[title]"`
> - After Step B: `✓ [N] comment(s) loaded`
> - After Step C (if run): `✓ [N] linked issue(s) loaded`
> - After Normalize: `✓ Normalised → /tmp/ii_normalized.json`

Load `references/[provider].md` and execute, in order:
1. **Interface Step A** — fetch raw issue → `/tmp/ii_raw_issue.json`
2. **Interface Step B** — fetch raw comments → `/tmp/ii_raw_comments.json`
3. **Interface Step C** — fetch raw linked issues → `/tmp/ii_raw_linked.json` (only if description is insufficient: < 150 chars, empty, or contains only cross-refs with no prose)
4. **Normalize** — map raw files to [`references/schema.json`](references/schema.json) → `/tmp/ii_normalized.json`

After this step `/tmp/ii_normalized.json` is the only file consumers read.

---

### Step 3b — Rank and trim comments

Before Step 4, post-process `comments` in `/tmp/ii_normalized.json` to surface the most relevant ones when the issue has many comments. This prevents context-window exhaustion on busy issues.

```python
import json, re

data     = json.load(open('/tmp/ii_normalized.json'))
comments = data.get("comments") or []

if len(comments) <= 10:
    # Small enough — use as-is, no ranking needed
    data["priority_comments"] = comments
else:
    author      = data.get("author", "")
    assignees   = set(data.get("assignees") or [])
    code_re     = re.compile(
        r'https?://\S+/-/(?:merge_requests|pull)/\d+'
        r'|`[^`]{4,}`'
        r'|(?:branch|commit|pr|mr)\b',
        re.IGNORECASE)
    bot_re      = re.compile(r'\[bot\]|^(github-actions|dependabot|renovate)$', re.IGNORECASE)

    def score(c):
        s = 0
        if c.get("author") == author:            s += 3   # reporter comment
        if c.get("author") in assignees:         s += 3   # assignee comment
        if bot_re.search(c.get("author", "")):   s -= 5   # penalise bots
        if code_re.search(c.get("body", "")):    s += 2   # contains code refs
        if len(c.get("body", "")) > 100:         s += 1   # substantive length
        return s

    ranked = sorted(comments, key=score, reverse=True)
    # Always include last 3 comments (most recent activity) + top-scored
    recents  = comments[-3:]
    top      = [c for c in ranked if c not in recents][:7]
    priority = top + recents
    # Remove duplicates, preserve order
    seen = set(); deduped = []
    for c in priority:
        cid = c.get("id") or c.get("body","")[:40]
        if cid not in seen: seen.add(cid); deduped.append(c)
    data["priority_comments"] = deduped

    data["comments_total"]    = len(comments)
    data["comments_shown"]    = len(deduped)

with open('/tmp/ii_normalized.json', 'w') as f:
    json.dump(data, f)
```

In Step 6's context block, render `priority_comments` instead of `comments`. If `comments_total > comments_shown`, add a note:
```
--- Comments ([comments_shown] of [comments_total] shown — ranked by relevance) ---
```

---

### Step 4 — Scan for code host cross-references

Read `/tmp/ii_normalized.json` and scan `description` + `comments[].body` for references pointing at the code repository:

```python
import json, re

issue     = json.load(open('/tmp/ii_normalized.json'))
full_text = (issue.get("description") or "") + "\n" + \
            "\n".join(c.get("body", "") for c in (issue.get("comments") or []))

code_refs = []
code_refs += re.findall(r'https?://\S+/-/merge_requests/\d+', full_text)
code_refs += re.findall(r'https?://github\.com/\S+/pull/\d+', full_text)
code_refs += re.findall(r'(?:branch[:\s]+|`)([\w./-]{4,80})(?:`|)', full_text, re.IGNORECASE)
code_refs += re.findall(r'(?<!\w)([0-9a-f]{7,40})(?!\w)', full_text)

seen = set(); CODE_REFS = []
for r in code_refs:
    if r not in seen: seen.add(r); CODE_REFS.append(r)
CODE_REFS = CODE_REFS[:10]
```

---

### Step 5 — Detect branching strategy, then optionally create branch

> **Branch creation is opt-in.** Steps 5a–5b detect the strategy and build the name.
> Step 5c asks the user for confirmation **before** touching git.
> Pass `--no-branch` (or the user replies "n" at the prompt) to skip branch creation entirely
> and continue to Step 6 as an exploration-only session.

#### Step 5a — Detect or ask for branching strategy

```bash
python3 - <<'PY'
import subprocess

# Detect whether repo has any commits at all
has_commits = subprocess.run(["git","rev-parse","HEAD"],
                              capture_output=True).returncode == 0

if not has_commits:
    print("BRANCH_STRATEGY=new-repo")
    print("BASE_BRANCH=none")
else:
    def branches():
        try: return subprocess.check_output(["git","branch","-a","--format=%(refname:short)"],
                                            stderr=subprocess.DEVNULL).decode().splitlines()
        except: return []

    all_b = set(branches())
    norm  = {b.replace("origin/","") for b in all_b}

    def has(*names): return any(n in norm for n in names)

    # Detect strategy from branch topology — most specific first
    if has("develop","dev") and has("release") and has("hotfix"):
        print("BRANCH_STRATEGY=gitflow")
        print("BASE_BRANCH=develop")
    elif has("develop","dev") and has("release"):
        print("BRANCH_STRATEGY=gitflow-lite")   # gitflow without hotfix convention
        print("BASE_BRANCH=develop")
    elif has("develop","dev","development"):
        print("BRANCH_STRATEGY=three-branch")
        print("BASE_BRANCH=" + next(n for n in ("develop","dev","development") if n in norm))
    else:
        try:
            default = subprocess.check_output(
                ["git","symbolic-ref","refs/remotes/origin/HEAD"],
                stderr=subprocess.DEVNULL).decode().strip().split("/")[-1]
        except:
            default = "main"
        # Trunk-based: main/master only, check if short-lived release/* branches exist
        if any(b.startswith("release/") or b.startswith("origin/release/") for b in all_b):
            print("BRANCH_STRATEGY=trunk-release")
        else:
            print("BRANCH_STRATEGY=single-branch")
        print(f"BASE_BRANCH={default}")
PY
```

**If `BRANCH_STRATEGY=new-repo`** — no commits exist yet. Ask the user:

> This looks like a new project with no commits yet. Which branching strategy will you use?
>
> | # | Strategy | New branches from | Promotion flow |
> |---|----------|-------------------|----------------|
> | 1 | **Gitflow** (feature/develop/release/hotfix/main) | `develop` | feature → develop → release → main |
> | 2 | **Three-branch** (dev / stg / main) | `dev` | feature → dev → stg → main |
> | 3 | **Single-branch** / trunk-based | `main` | feature → main directly |
>
> Reply `1`, `2`, or `3`. The branch will be created as an orphan.

Set `BASE_BRANCH` accordingly (`develop`, `dev`, `main`). Set `HAS_COMMITS=false`.

**If auto-detected** — tell the user which strategy was found and what base branch will be used:

| Detected strategy | Message |
|---|---|
| `gitflow` | "Detected Gitflow — branching from `develop`." |
| `gitflow-lite` | "Detected Gitflow (no hotfix convention) — branching from `develop`." |
| `three-branch` | "Detected three-branch strategy — branching from `[BASE_BRANCH]`." |
| `trunk-release` | "Detected trunk-based with release branches — branching from `[BASE_BRANCH]`." |
| `single-branch` | "Detected single-branch strategy — branching from `[BASE_BRANCH]`." |

Set `HAS_COMMITS=true`. Once confirmed, set `BASE_BRANCH` and `BRANCH_STRATEGY`.

**Carry forward**: keep `BASE_BRANCH`, `HAS_COMMITS`, and `BRANCH_STRATEGY` in memory — Steps 5b and 5c read them directly (they are not shell environment variables).

---

#### Step 5b — Build branch name

Derive the slug by reasoning over the issue title and (if present) the first 300 characters of the description. **Do not use hardcoded word lists.**

Apply this prompt to yourself:

```
You are generating a git branch name slug.

Issue title:       {issue["title"]}
Issue description: {issue["description"][:300] if issue.get("description") else "(none)"}

Rules:
1. Output ONLY the slug — no explanation, no quotes, no punctuation other than hyphens.
2. 2–4 lowercase words joined by hyphens.
3. Choose the most identifying domain/technical words that distinguish THIS issue
   from all others (e.g. "oauth-token-refresh", "null-ptr-save", "redis-cache-invalidation").
4. One optional short action verb (fix, add, migrate…) is allowed only when it
   meaningfully narrows scope; drop it if the noun words alone are clear.
5. Omit filler words (the, a, an, is, to, for, in, on, with, of, and, or, …).
6. Use the description only when the title is ambiguous or too generic on its own.

Slug:
```

Substitute the slug you just generated into the `raw_slug` line below, then run the block:

```python
import json, re

issue   = json.load(open('/tmp/ii_normalized.json'))
itype    = issue.get("issue_type", "unknown")
strategy = BRANCH_STRATEGY  # carry-forward from Step 5a

# Gitflow uses hotfix/ for bugs on main; all other strategies use bug/
_bug_prefix = "hotfix/" if strategy in ("gitflow","gitflow-lite") else "bug/"
prefix = {"bug": _bug_prefix, "feature": "feature/", "task": "task/", "hotfix": "hotfix/"}.get(itype, "feature/")

# ← Replace with the slug you generated (e.g. "oauth-token-refresh")
raw_slug = "YOUR-SLUG-HERE"

# Sanitize: lowercase, keep only alphanumeric and hyphens, collapse runs, cap length
slug   = re.sub(r'[^a-z0-9]+', '-', raw_slug.lower()).strip('-')[:50] or "untitled"
branch = f"{prefix}{issue['id']}-{slug}"
# Examples:
# "Add OAuth login support"                       → feature/PROJ-42-oauth-login-support
# "Fix null pointer exception on save"            → bug/317-fix-null-ptr-save
# "Implement Redis cache invalidation on logout"  → feature/88-redis-cache-invalidation
# "Row-level progress showing 0 during migration" → bug/4-row-progress-zero
print(f"BRANCH_NAME={branch}")
```

**Carry forward**: keep `BRANCH_NAME` in memory — Step 5c reads it directly.

---

#### Step 5b-confirm — Ask the user before touching git

**If `--no-branch` was passed**, skip to Step 6. Set `BRANCH_SKIPPED=true`.

**Otherwise**, ask:

> Ready to create branch:
> ```
> [BRANCH_NAME]  (from [BASE_BRANCH])
> ```
> Create it now? **[Y/n]** — or type a different name to override.

- If **Y** (or Enter): proceed to Step 5c with `BRANCH_NAME` as-is.
- If the user types a **custom name**: sanitize it (`re.sub(r'[^a-z0-9/._-]', '-', name.lower()).strip('-')`) and update `BRANCH_NAME`, then proceed to Step 5c.
- If **n**: set `BRANCH_SKIPPED=true` and skip Step 5c. Tell the user:
  > "Skipping branch creation — continuing in exploration mode. Run `/issue-explore [id]` again and choose Y when you're ready to implement."

---

#### Step 5c — Create the branch

Always branch from `origin/{base_branch}` so the new branch starts from the latest remote state, not from whatever the local copy happens to be at.

> **Tell the user before running this step:**
> ```
> Creating branch [BRANCH_NAME] from [BASE_BRANCH]…
> ```

```bash
python3 - <<'PY'
import subprocess, sys

# Values carried forward from Steps 5a and 5b — substitute directly before running:
branch      = BRANCH_NAME             # from Step 5b  (e.g. "bug/317-fix-null-ptr-save")
base_branch = BASE_BRANCH             # from Step 5a  (e.g. "dev" or "main")
has_commits = (HAS_COMMITS == "true") # from Step 5a  ("true" or "false")

# Check if branch already exists locally
existing = subprocess.run(["git","branch","--list", branch],
                          capture_output=True, text=True).stdout.strip()
if existing:
    print(f"BRANCH_EXISTS={branch}")

elif not has_commits:
    # New repo — no history yet; no base needed
    r = subprocess.run(["git","checkout","-b", branch], capture_output=True, text=True)
    if r.returncode == 0:
        print(f"BRANCH_CREATED={branch}")
        print("NOTE=new repo, branch will attach on first commit")
    else:
        print(f"BRANCH_ERROR={r.stderr.strip()}")
        sys.exit(1)

else:
    # Step 1: switch to source branch
    co = subprocess.run(["git","checkout", base_branch], capture_output=True, text=True)
    if co.returncode != 0:
        # Source branch may not exist locally yet — fetch and track it
        subprocess.run(["git","fetch","origin", base_branch], capture_output=True)
        co = subprocess.run(["git","checkout","--track", f"origin/{base_branch}"],
                            capture_output=True, text=True)
        if co.returncode != 0:
            print(f"BRANCH_ERROR=could not checkout source branch '{base_branch}': {co.stderr.strip()}")
            sys.exit(1)

    # Step 2: pull latest from remote so source branch is up to date
    pull = subprocess.run(["git","pull","origin", base_branch], capture_output=True, text=True)
    if pull.returncode != 0:
        print(f"PULL_WARN=pull failed on '{base_branch}': {pull.stderr.strip()}")
        # Non-fatal — continue with whatever local state we have

    # Step 3: create new branch off the now-updated source branch
    r = subprocess.run(["git","checkout","-b", branch], capture_output=True, text=True)
    if r.returncode == 0:
        print(f"BRANCH_CREATED={branch}")
        print(f"BASE={base_branch}")
    else:
        print(f"BRANCH_ERROR={r.stderr.strip()}")
        sys.exit(1)
PY
```

- **`BRANCH_EXISTS`**: tell the user the branch already exists and you switched to it: `Switched to existing branch: {branch}`. Continue to Step 6.
- **`BRANCH_CREATED`** (new repo): tell the user `Branch set to: {branch} — it will be created on your first commit.`
- **`BRANCH_CREATED`** (existing repo): tell the user `✓ Created and switched to: {branch}  (from {base_branch}, pulled latest)`.
- **`PULL_WARN`**: tell the user the pull failed, but name the fix: `⚠ Could not pull latest {base_branch} (no network or upstream not set). Branch created from local state — run 'git pull origin {base_branch}' when connectivity is restored.`
- **`BRANCH_ERROR`**: map the raw git error to an actionable message before showing it:

  | If stderr contains | Tell the user |
  |---|---|
  | `not a valid object name` | "Base branch `{base_branch}` doesn't exist locally. Run `git fetch origin` then retry." |
  | `already exists` | "Branch `{branch}` already exists. Switching to it — no new branch created." (then `git checkout {branch}`) |
  | `lock file` | "Another git operation is in progress. Wait for it to finish, then retry." |
  | `detached HEAD` | "Repository is in detached HEAD state. Run `git checkout {base_branch}` first, then retry." |
  | `Permission denied` | "Git cannot write to this repository. Check file permissions on `.git/`." |
  | *(anything else)* | Show the raw error prefixed with: "Branch creation failed. If `git fetch origin && git status` doesn't help, create the branch manually: `git checkout -b {branch} origin/{base_branch}`" |

  Continue to Step 6 without a branch in all error cases.

---

### Step 6 — Assemble context and invoke spec/exploration skill

Read `/tmp/ii_normalized.json` for all issue fields. Combine with code repo context from Step 1b.

```python
import json
issue = json.load(open('/tmp/ii_normalized.json'))
```

Context block:

```
=== [issue.provider] Issue: [issue.id] ===
URL:        [issue.url]
Title:      [issue.title]
State:      [issue.state]
Type:       [issue.issue_type]
Labels:     [issue.labels joined by ", "]
Author:     [issue.author]
Assignees:  [issue.assignees joined by ", "]

--- Description ---
[issue.description, up to 3000 chars]

--- Comments [if comments_total > comments_shown: "([comments_shown] of [comments_total] — ranked by relevance)"] ---
[issue.priority_comments, each as "[author]: body"]

--- Linked Issues ---
[issue.linked_issues, each as "  ID [state] title\n  summary", or "(none)"]

--- Provider Fields ---
[For each key-value pair in issue.custom_fields (if non-empty), render as "  key: value".
 Examples: "  Sprint: Sprint 12", "  Story Points: 5", "  Epic: PROJ-100 – Auth Overhaul"
 If issue.custom_fields is empty or absent, omit this section entirely.]

--- Code References in Issue ---
[CODE_REFS, or "(none found)"]

=== Code Repository ===
Host:    [CODE_HOST]  [NOTE if differs from issue.provider]
Repo:    [CODE_REPO]
Branch:  [CODE_BRANCH]

Recent commits:
[CODE_COMMITS]
```

If `CODE_HOST != issue["provider"]`, add inline note:
```
NOTE: Issue tracker ([issue.provider]) and code host ([CODE_HOST]) are different systems.
```

#### Step 6a — Detect available spec/exploration skill

Scan system-reminder tags for loaded skills. Check in this priority order — use the first match:

| Priority | Skill name | Invocation |
|----------|-----------|-----------|
| 1 | `opsx:explore` | `opsx:explore` |
| 2 | `spec-kit` | `spec-kit` |
| 3 | `explore` | `explore` |
| 4 | `spec` | `spec` |
| 5 | any skill whose name contains `explore` or `spec` | use that name |

Save result as `SPEC_SKILL` (the matched skill name), or `none` if nothing matched.

To add support for a new spec skill: add a row to the table above, newest priority first.

---

#### Step 6b — Invoke or present

**If `SPEC_SKILL` is found** — tell the user:
```
Loaded [issue.provider] issue [issue.id]: "[issue.title]"
Code repo: [CODE_HOST] — [CODE_REPO]
Branch:    [BRANCH_NAME if not BRANCH_SKIPPED else "(none — exploration mode)"]
Starting [SPEC_SKILL]...
```

Invoke `[SPEC_SKILL]` with:
```
I want to explore the implementation for this work item before starting a change:

<full context block>

Let's think through: requirements, ambiguities, edge cases, and which parts of the codebase are likely involved. Any branches or MRs already linked to the issue are under "Code References in Issue".
```

**If `SPEC_SKILL=none`** — present the full context block directly to the user, then offer concrete next steps:

```
No spec skill loaded — but the issue context above is ready.

What would you like to do?
  1. Find files in this repo likely affected by this issue
  2. List open questions, ambiguities, and edge cases
  3. Check for existing branches or MRs related to this issue
  4. Summarise what needs to be implemented
  5. Start implementing now

Reply with a number, or ask anything about the issue.

──────────────────────────────────────────────────
For richer structured exploration, install a spec skill:
  • opsx:explore — https://agentskills.io
  • spec-kit     — https://github.com/dailydotdev/spec-kit
──────────────────────────────────────────────────
```

Then wait for the user's reply and act on it directly (do not invoke a skill — you are the exploration layer).

**Always run this cleanup — even if Step 6b or the spec skill invocation fails:**
```bash
rm -f /tmp/ii_raw_issue.json /tmp/ii_raw_comments.json /tmp/ii_raw_linked.json \
      /tmp/ii_normalized.json
```
