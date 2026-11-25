---
name: git-submodule-dead-upstream-audit
description: Diagnose unreachable submodule upstreams (404, deleted, renamed, private), check for local cached history, and search GitHub for surviving forks or mirrors of the recorded SHA before deciding to remove the submodule.
category: Git & Repository Management
---

# Git Submodule Dead Upstream Audit Skill (v1)

This skill provides a deterministic, evidence-based protocol for auditing a Git submodule whose upstream URL appears
to be unreachable. It answers three questions in order — **(1) Is the upstream really gone?** **(2) Do we have any
local copy of its history?** **(3) Does any public fork or mirror still hold the recorded commit SHA?** — so the
agent can recommend removal, re-pointing, or recovery on the basis of evidence rather than assumption.

> [!IMPORTANT]
> This skill is **non-destructive**. It produces an audit verdict only. Removal MUST be performed by the
> [`git-submodule-removal`](../git-submodule-removal/SKILL.md) skill, and re-pointing MUST be performed by
> [`git-submodule-fork-reconfigure`](../git-submodule-fork-reconfigure/SKILL.md), each with explicit user authorization.

***

## 1. Environment & Dependencies

Before execution, the agent MUST verify each tool. Missing tools MUST be installed via the
[`system-wide-tool-management`](../system-wide-tool-management/SKILL.md) skill.

- **git**: Submodule introspection.
    - Check: `which git && git --version`
- **curl**: Upstream reachability and authenticated GitHub API queries. The `curl` invocations in §3 and §4 follow the
  same canonical pattern documented in [GitHub REST API Fallback](../github-rest-api-fallback/SKILL.md) §2.4
  (mandatory `User-Agent` header, `-fsSL` flags, PAT via `$GITHUB_TOKEN` env var) — that skill is the SSOT for
  GitHub REST invocations and SHOULD be consulted when adapting any call here.
    - Check: `which curl && curl --version`
- **PowerShell alternative**: On Windows without `curl`, every call below can be rewritten with
  `Invoke-RestMethod` per [GitHub REST API Fallback](../github-rest-api-fallback/SKILL.md) §2.1.
- **python3**: JSON parsing for GitHub API responses.
    - Check: `which python3 && python3 --version`
- **PAGER Environment**: Export `PAGER=cat` for all Git commands to prevent terminal hangs.
- **No direct-shell tool**: When `run_in_terminal` is unavailable, route every shell invocation through
  [Terminal Fallback via VS Code Tasks](../terminal-fallback-via-vscode-tasks/SKILL.md) §3.

### 1.1 GitHub Token (Required for Code Search)

The unauthenticated GitHub API rejects code search with HTTP 401. The agent MUST resolve a personal access token
**without printing it to the terminal**:

```bash
GH_TOKEN=$(awk '$1=="GitHub"{print $2; exit}' "<KEYS_FILE>")
```

- `<KEYS_FILE>`: A space-separated `keyword value` file under the user's private configuration directory (the agent
  MUST ask the user for the path; it is **never** committed or echoed).
- The agent MUST verify only the prefix (e.g., `printf '%s' "$GH_TOKEN" | head -c 8`) to confirm the token loaded —
  full-value echo is **FORBIDDEN**.

***

## 2. Pre-Audit Discovery

1. **Read the submodule registration**:

    ```bash
    PAGER=cat git config --file .gitmodules --get-regexp "^submodule\.<PATH>\."
    ```

    Extract the configured `url` and any `branch`.

2. **Resolve the recorded pointer SHA** from the parent index:

    ```bash
    PAGER=cat git ls-tree HEAD <PATH> | awk '{print $3}'
    ```

    The output is a 40-character commit SHA (the "recorded pointer").

3. **Inspect the working tree state**:

    ```bash
    ls -la <PATH> 2>&1 | head
    ls -la .git/modules/<PATH> 2>&1 | head
    ```

    - **Empty `<PATH>` directory + missing `.git/modules/<PATH>`** ⇒ submodule was never initialized; **no local
      history exists**.
    - **Populated `.git/modules/<PATH>`** ⇒ a local clone exists; the recorded SHA may be recoverable from local
      objects via `git -C .git/modules/<PATH> cat-file -t <SHA>`.

***

## 3. Upstream Reachability Probe

Run both an HTML and an API probe; treat any **2xx** as alive, **3xx** as renamed/moved (follow it), **404/410** as
deleted, and **private** as inaccessible (the API returns `404` for private repos to anonymous callers).

```bash
# HTML probe (no auth required)
curl -sI "<URL_WITHOUT_DOT_GIT>" | head -3

# API probe (authenticated — distinguishes private vs deleted only with the right token scope)
curl -s -H "Authorization: Bearer $GH_TOKEN" -H "Accept: application/vnd.github+json" \
    "https://api.github.com/repos/<OWNER>/<REPO>" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('message') or d.get('full_name'))"
```

- **Pedagogical Breakdown**:
    - `curl -sI`: silent, headers-only — fast 404 detection without downloading the body.
    - `Authorization: Bearer $GH_TOKEN`: required for any API call beyond 60 req/h and for code search.
    - `Accept: application/vnd.github+json`: pins the API media type for forward-compatibility.
    - The `python3` filter prints either `Not Found` (deleted) or the canonical `full_name` (alive, possibly renamed).

***

## 4. Fork / Mirror Discovery (Authenticated)

When the upstream is gone, search public GitHub for any surviving copy of the recorded SHA. Each query MUST be
authenticated.

### 4.1 SHA Code Search (Strongest Signal)

```bash
curl -s -H "Authorization: Bearer $GH_TOKEN" -H "Accept: application/vnd.github+json" \
    "https://api.github.com/search/code?q=<RECORDED_SHA>" \
    | python3 -c "import sys,json;d=json.load(sys.stdin);print('total:',d.get('total_count'));[print(i['repository']['full_name'],i['path']) for i in d.get('items',[])[:20]]"
```

A non-zero `total_count` means at least one repository commits a file containing that exact SHA — usually a
submodule pointer in another super-project that still references the dead submodule. Each hit is a candidate mirror.

### 4.2 Repository Name Search

```bash
for q in "<OWNER>+<REPO>" "<REPO>+user:<OWNER>" "<REPO>+fork:true"; do
    echo "=== $q ==="
    curl -s -H "Authorization: Bearer $GH_TOKEN" -H "Accept: application/vnd.github+json" \
        "https://api.github.com/search/repositories?q=$q" \
        | python3 -c "import sys,json;d=json.load(sys.stdin);print('total:',d.get('total_count'));[print('-',i['full_name']) for i in d.get('items',[])[:10]]"
done
```

### 4.3 Owner Activity Sweep

```bash
curl -s -H "Authorization: Bearer $GH_TOKEN" \
    "https://api.github.com/users/<OWNER>/repos?per_page=100" \
    | python3 -c "import sys,json;[print(r['full_name']) for r in json.load(sys.stdin)]"

curl -s -H "Authorization: Bearer $GH_TOKEN" \
    "https://api.github.com/users/<OWNER>/events?per_page=100" \
    | python3 -c "import sys,json;print('\n'.join(sorted({e['repo']['name'] for e in json.load(sys.stdin)})))"
```

This catches renames (e.g., `<REPO>` → `<REPO>-archive`) and reveals related repos that may host a salvage branch.

### 4.4 Wayback Machine (Last-Resort)

```bash
curl -s "https://archive.org/wayback/available?url=github.com/<OWNER>/<REPO>" \
    | python3 -c "import sys,json;print(json.load(sys.stdin).get('archived_snapshots') or 'no snapshot')"
```

A snapshot only proves the repo *existed*, not that the SHA can be recovered, but it can yield the original
README and identify the project's purpose.

### 4.5 Candidate Validation

For every candidate `<CAND_OWNER>/<CAND_REPO>` returned by §4.1–§4.3, confirm that the recorded SHA is reachable:

```bash
curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $GH_TOKEN" \
    "https://api.github.com/repos/<CAND_OWNER>/<CAND_REPO>/commits/<RECORDED_SHA>"
```

- `200` ⇒ the SHA exists in that repo; it is a valid recovery source.
- `404` ⇒ the SHA is not reachable from that repo's refs; the candidate is a false positive.
- `422` ⇒ the SHA is malformed; re-extract from §2 step 2.

***

## 5. Verdict Matrix

The agent MUST produce a verdict from the table below before recommending any next step. Any cell marked **HALT**
requires explicit user authorization to proceed.

| Upstream Probe | Local `.git/modules/<PATH>` | Fork/Mirror with SHA | Verdict | Recommended Next Skill |
| :--- | :--- | :--- | :--- | :--- |
| Alive (2xx) | irrelevant | irrelevant | **Healthy** — no action. | None. |
| Renamed (3xx → new URL) | irrelevant | irrelevant | **Re-point.** | [`git-submodule-fork-reconfigure`](../git-submodule-fork-reconfigure/SKILL.md) |
| Dead (404/410) | Present + SHA reachable locally | irrelevant | **Recoverable from local clone.** Push to a new origin, then re-point. | [`git-submodule-fork-reconfigure`](../git-submodule-fork-reconfigure/SKILL.md) |
| Dead (404/410) | Absent | ≥1 candidate validates (§4.5 = 200) | **Recoverable from public fork.** Re-point `.gitmodules` to the candidate. | [`git-submodule-fork-reconfigure`](../git-submodule-fork-reconfigure/SKILL.md) |
| Dead (404/410) | Absent | None validate | **Unrecoverable.** Recommend removal. | [`git-submodule-removal`](../git-submodule-removal/SKILL.md) (HALT for confirmation) |
| Private (401/404) | irrelevant | irrelevant | **Inaccessible.** Ask the user whether they hold credentials before deciding. | HALT |

***

## 6. Audit Report Template

The agent MUST present the verdict to the user using this exact structure (markdown table, not prose):

```markdown
**Submodule:** `<PATH>`
**Configured URL:** `<URL>`
**Recorded SHA:** `<RECORDED_SHA>`

| Probe | Result |
| :--- | :--- |
| Upstream HTML | <2xx | 3xx → <new-url> | 404 | 410> |
| Upstream API  | <Not Found | <full_name>> |
| Local `<PATH>/` | <empty | populated> |
| Local `.git/modules/<PATH>` | <missing | present (size)> |
| SHA reachable locally | <yes | no | n/a> |
| Code search hits for SHA | <count> |
| Validated forks (§4.5 = 200) | <list or none> |
| Wayback snapshot | <yes (date) | none> |

**Verdict:** <one of the §5 verdicts>
**Recommended next skill:** <link>
```

***

## 7. Operational Safety

- **Token Hygiene**: The agent MUST NEVER print the full token, log it, or commit any file containing it. Only the
  prefix may be displayed for verification.
- **Read-Only by Default**: This skill performs zero write operations on the parent repository, the submodule, or
  any remote. It produces a report and a recommendation only.
- **No Auto-Removal**: Even when the verdict is **Unrecoverable**, the agent MUST HALT and request explicit user
  confirmation before invoking the removal skill.
- **Rate-Limit Awareness**: Authenticated GitHub API allows 5,000 req/h; code search allows 30 req/min. The agent
  MUST batch queries and respect `X-RateLimit-Remaining` headers when auditing many submodules.

***

## 8. Upstream History Rewrite (Force-Push Recovery Mode)

A different failure mode from a dead URL: the remote responds, the URL is valid, but the pinned SHA is **not reachable** from any current branch on the remote — the upstream did a `push --force` that rewrote history out from under the pin.

**Trigger fingerprint**:

**Necessary signals (all three MUST hold):**

1. The remote is reachable (`git ls-remote <url>` succeeds).
2. `git -C <submodule> fetch origin` succeeds.
3. `git -C <submodule> merge-base --is-ancestor <pinned-sha> origin/<default>` returns **non-zero** — pinned SHA is not in the new default-branch history.

When all three hold, you are looking at a force-rewrite (or a deleted-branch case), not a dead URL.

**Confidence amplifier (optional, raises probability when present):**

4. The remote shows a sibling branch named `origin/old-<default>`, `origin/<default>-old`, `origin/<default>-backup`, `origin/<default>-bak`, or a date-stamped variant — the upstream's own backup of the pre-rewrite tip. The upstream may or may not have kept such a backup; when it IS present, the force-rewrite hypothesis is near-certain AND the orphaned commits are likely recoverable (see [`git-submodule-missing-revision-recovery`](../git-submodule-missing-revision-recovery/SKILL.md)). Absence does NOT rule out a force-rewrite — it just means the upstream rewrote without preserving the old tip, and recovery from your own local clone or a third-party fork becomes the only path.

    **Probe command for signal 4** — run from inside the submodule working tree (or via `git -C <submodule>`):

    ```bash
    PAGER=cat git ls-remote origin \
        'refs/heads/*old*' \
        'refs/heads/*backup*' \
        'refs/heads/*bak*'
    ```

    - **One or more refs printed** ⇒ a backup branch is present; record each `<sha>  refs/heads/<name>` pair and feed it into the §8.1 remediation matrix.
    - **No output** ⇒ no backup branch matching the common naming patterns; treat signal 4 as **absent** (the necessary signals 1–3 alone still establish force-rewrite).
    - **Note**: The globs are case-sensitive against remote ref names. If the upstream uses unusual casing (e.g., `BACKUP`, `OLD`) or a non-English term, broaden the patterns or fall back to plain `PAGER=cat git ls-remote origin` and grep visually.

**Diagnostic only — remediation is out of scope for this skill version.**

The user has multiple options (fork-and-retarget, bump pin, cherry-pick orphaned commits, etc.) and the choice depends on whether your repo's orphaned commits carry unique work. Surface the diagnosis to the author and stop.

**Related skills for downstream remediation when the author decides**:

- [`git-submodule-fork-reconfigure`](../git-submodule-fork-reconfigure/SKILL.md) — if the choice is fork-and-retarget.
- [`git-submodule-missing-revision-recovery`](../git-submodule-missing-revision-recovery/SKILL.md) — if the choice is to recover the orphaned SHA from a backup branch.

***

## 9. Related Skills

- **Removal Engine** (post-verdict): [`git-submodule-removal`](../git-submodule-removal/SKILL.md)
- **Re-point Engine** (post-verdict): [`git-submodule-fork-reconfigure`](../git-submodule-fork-reconfigure/SKILL.md)
- **Pointer Repair** (when SHA is recoverable but parent history is wrong):
  [`git-submodule-pointer-repair`](../git-submodule-pointer-repair/SKILL.md)
- **Tool Bootstrap**: [`system-wide-tool-management`](../system-wide-tool-management/SKILL.md)
- **Parent Rules**: [`ai-agent-rules/git-submodule-rules.md`](../../../ai-agent-rules/git-submodule-rules.md)

### 9.1 Composition by Higher-Level Skills

| Composer | Role | Reuses From This Skill |
| :--- | :--- | :--- |
| [`git-submodule-orphan-gitlink-recovery`](../git-submodule-orphan-gitlink-recovery/SKILL.md) | Recovers orphan gitlinks (tree-recorded but absent from `.gitmodules`). | §4 SHA-to-repo `search/commits` protocol + §5 Verdict Matrix. |
| [`git-submodule-uninitialized-audit`](../git-submodule-uninitialized-audit/SKILL.md) | Recursive read-only audit of every uninitialized submodule pointer. | §4 SHA search invoked per Unreachable URL (HTTP 4xx/5xx). |

***

## 10. Traceability

- **Generated via**: [`skill-factory`](../skill-factory/SKILL.md)
- **Origin Conversation**: Audit of the dead `sammcgrail/seb` submodule in `lab-data/ai-suite` (`9 May 2026`).
