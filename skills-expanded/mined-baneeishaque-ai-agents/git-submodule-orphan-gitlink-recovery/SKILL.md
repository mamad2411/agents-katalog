---
name: git-submodule-orphan-gitlink-recovery
description: Industrial protocol for recovering orphan submodule gitlinks (recorded in a parent's tree but absent from `.gitmodules`) by SHA-based upstream discovery, fork reconfiguration, registration, and unrecoverable-pointer drop.
category: Git & Repository Management
---

# Git Submodule Orphan Gitlink Recovery Skill (v1)

This skill provides a surgical protocol for repairing **orphan gitlinks** — paths recorded as `mode 160000`
(submodule pointers) in a Git tree whose URLs are **missing from `.gitmodules`**. Such pointers cannot be
initialized via `git submodule update --init` because git has no URL to clone; they manifest as empty directories
and cause `fatal: no submodule mapping found in .gitmodules for path '<path>'` during `git submodule status`.
The skill orchestrates SHA-based upstream discovery, on-the-fly forking when the parent submodule is read-only,
selective registration of recoverable pointers, and explicit removal of unrecoverable ones.

***

## 1. Environment & Dependencies

Before execution, the agent **MUST** verify the industrial environment.

1. **Verify Git** (`>= 2.30`):

    ```bash
    git --version
    ```

2. **Verify GitHub CLI**:

    ```bash
    gh --version
    gh auth status
    ```

    *If `gh` is not logged in, the agent MUST instruct the user to run `gh auth login` manually.*

    **Fallback delegations** (each is independently optional but the agent MUST engage them when the named tool
    or capability is unavailable):

    - **No `gh` installed**: replace every `gh repo view` / `gh repo fork` / `gh auth token` call with the REST
      equivalent per [GitHub REST API Fallback](../github-rest-api-fallback/SKILL.md) §3 — specifically
      `GET /repos/{o}/{r}` for view, `POST /repos/{o}/{r}/forks` for fork, and a user-supplied PAT in
      `$env:GITHUB_TOKEN` instead of `gh auth token`.
    - **`gh auth status` fails / wrong identity cached**: defer to
      [Git / GitHub Auth Fallback](../git-github-auth-fallback/SKILL.md) §2 before attempting any write
      operation against GitHub.
    - **No `run_in_terminal`**: route every shell command via
      [Terminal Fallback via VS Code Tasks](../terminal-fallback-via-vscode-tasks/SKILL.md) §3.

3. **Verify `curl` + `python3`** (used for `Authorization: Bearer` token search and JSON parsing):

    ```bash
    curl --version | head -1
    python3 --version
    ```

4. **Load GitHub Token** (for authenticated commit-hash search; raises rate limit from 10/min to 30/min and unlocks
   `search/commits`). Prefer the `gh` token; fall back to a local keyword file:

    ```bash
    # Option A (preferred): reuse the gh CLI token.
    GH_TOKEN=$(gh auth token)

    # Option B (fallback): read from a redacted local keyword file.
    GH_TOKEN=$(awk '$1=="GitHub"{print $2; exit}' "<KEYS_FILE>")

    # Verify prefix only — NEVER print the full token.
    echo "token-prefix: ${GH_TOKEN:0:7}…"
    ```

***

## 2. Phase 1: Orphan Gitlink Detection

Identify the orphan pointers inside a submodule (or any Git repository).

1. **Enter the suspect submodule** (run from the parent repo root):

    ```bash
    cd <submodule-path>
    ```

2. **List all gitlinks in the working tree**:

    ```bash
    PAGER=cat git ls-tree -r HEAD | awk '$2=="commit"{print $4, $3}'
    ```

    * `ls-tree -r HEAD` — recursively walks the current commit's tree.
    * `awk '$2=="commit"'` — filters to entries whose object type is `commit` (mode `160000` = gitlink).
    * Output columns: **path**, **SHA**.

3. **Compare against `.gitmodules`**:

    ```bash
    [ -f .gitmodules ] && git config --file .gitmodules --get-regexp '\.path$' || echo "(no .gitmodules)"
    ```

    Any path appearing in step 2 but **not** in step 3 is an **orphan gitlink**.

4. **Confirm the runtime symptom** (proves the pointer is broken, not just lazily registered):

    ```bash
    PAGER=cat git submodule status 2>&1 | head
    ```

    Expect `fatal: no submodule mapping found in .gitmodules for path '<orphan>'`.

***

## 3. Phase 2: SHA-Based Upstream Discovery

For each orphan SHA, attempt to discover the canonical upstream repository on GitHub.

1. **Search the commits index** (returns up to 100 repos that contain the exact SHA):

    ```bash
    curl -s \
        -H "Authorization: Bearer $GH_TOKEN" \
        -H "Accept: application/vnd.github+json" \
        "https://api.github.com/search/commits?q=hash:<SHA>&per_page=30" \
      | python3 -c "import sys,json; d=json.load(sys.stdin); print('count',d.get('total_count')); [print(' ',i['repository']['full_name']) for i in d.get('items',[])]"
    ```

    * `q=hash:<SHA>` — GitHub's full-SHA commit search; partial prefixes are NOT supported.
    * `Accept: application/vnd.github+json` — current API media type. The legacy
      `application/vnd.github.cloak-preview+json` still works as a fallback.
    * `count` is the authoritative result tally; `items` holds the repositories.

2. **Identify the canonical upstream** when multiple repos contain the SHA:

    | Heuristic | Command | Rationale |
    | :--- | :--- | :--- |
    | Oldest `created_at` | `gh repo view <owner>/<repo> --json createdAt,name,parent,stargazerCount,isFork` | Forks are always younger than their source. |
    | Exact name match | (visual scan) | Forks usually keep the original name. |
    | Highest stars | `--json stargazerCount` | Tie-breaker for unrelated copies. |
    | `isFork: false` + no `parent` | `--json isFork,parent` | True ancestor will report no parent. |

    **Fidelity Mandate**: The agent MUST verify the chosen repo actually contains the SHA before proceeding:

    ```bash
    curl -s -H "Authorization: Bearer $GH_TOKEN" \
      "https://api.github.com/repos/<owner>/<repo>/commits/<SHA>" \
      | python3 -c "import sys,json; d=json.load(sys.stdin); print('sha:',d.get('sha')); print('msg:',(d.get('commit',{}).get('message') or '').splitlines()[0])"
    ```

3. **Verdict per orphan** (adapted from
   [git-submodule-dead-upstream-audit](../git-submodule-dead-upstream-audit/SKILL.md) §5):

    | `count` | Local cache (`git cat-file -t <SHA>`) | Verdict | Action |
    | :--- | :--- | :--- | :--- |
    | `>= 1` | n/a | **Recoverable** | Phase 4: register with discovered URL. |
    | `0` | object exists | **Salvageable** | Phase 4: push local objects to a new repo, then register. |
    | `0` | not found | **Unrecoverable** | Phase 4: drop the orphan gitlink. |

***

## 4. Phase 3: Write-Access Decision

Recovery requires committing changes to the parent submodule repository. Determine whether direct push is possible.

1. **Probe push permission**:

    ```bash
    curl -s -H "Authorization: Bearer $GH_TOKEN" \
        "https://api.github.com/repos/<owner>/<repo>" \
      | python3 -c "import sys,json; d=json.load(sys.stdin); print('permissions:',d.get('permissions')); print('default_branch:',d.get('default_branch'))"
    ```

    * `permissions.push: true` → proceed in-place; create branch on `origin`.
    * `permissions.push: false` (or `pull` only) → **MANDATORY** fork via
      [git-submodule-fork-reconfigure](../git-submodule-fork-reconfigure/SKILL.md).

2. **When forking is required**, execute the fork-reconfigure protocol:

    ```bash
    gh repo fork <owner>/<repo> --fork-name <repo> --clone=false
    git remote rename origin upstream
    git remote add origin https://github.com/<your-user>/<repo>.git
    ```

    * `--clone=false` — prevents `gh` from cloning a duplicate working tree (we are already inside it).
    * Renaming `origin → upstream` preserves the read-only ancestor for future fetches.

***

## 5. Phase 4: Recovery Commit

On a dedicated branch in the (possibly forked) submodule repo, atomically apply all recovery edits.

1. **Create the recovery branch**:

    ```bash
    git checkout -b fix/register-submodules
    ```

2. **Register every Recoverable orphan** in `.gitmodules`:

    ```bash
    [ ! -f .gitmodules ] && touch .gitmodules
    git config --file .gitmodules submodule.<path>.path <path>
    git config --file .gitmodules submodule.<path>.url  <discovered-url>
    git add .gitmodules
    ```

    * `git config --file .gitmodules` — writes the canonical INI section the way `git submodule` expects.
    * The `<path>` MUST exactly match the gitlink path from Phase 1.

3. **Drop every Unrecoverable orphan**:

    ```bash
    git rm --cached <path>
    ```

    * `--cached` — removes the gitlink from the index without touching the (empty) working-tree directory.

4. **Verify the staged change**:

    ```bash
    PAGER=cat git status -s
    ```

    Expect `A  .gitmodules` for additions and `D  <path>` for unrecoverable drops.

5. **Commit** (per
   [Git Commit Message Rules](../../../ai-agent-rules/git-commit-message-rules.md)):

    ```bash
    git commit -m "fix(submodules): register <recovered-list> and drop unrecoverable <dropped-list>

- Add .gitmodules entry mapping path '<path>' to <url> (matches recorded SHA <SHA>, the canonical upstream).
- Remove orphan gitlink at path '<path>' (recorded SHA <SHA>); SHA is not present on any public GitHub
    repository or in local cache, so the gitlink is unrecoverable.
- No upstream PR is opened by this protocol; this branch lives only on the personal fork and is consumed by
    the parent repository via fork-reconfigured submodule URL."
    ```

6. **Push the branch**:

    ```bash
    git push -u origin fix/register-submodules
    ```

***

## 6. Phase 5: Parent Repository Re-Point

Update the parent so that `git submodule update --init --recursive` now resolves the recovered nested submodules.

1. **Return to the parent root**:

    ```bash
    cd <parent-repo-root>
    ```

2. **Update `.gitmodules`** (only when the submodule was forked in §4.2):

    ```bash
    git config --file .gitmodules submodule.<sub-name>.url    <fork-url>
    git config --file .gitmodules submodule.<sub-name>.branch fix/register-submodules
    git submodule sync <sub-path>
    ```

    * `submodule sync` — propagates the new URL into `.git/config`; required so subsequent `init` uses the fork.
    * The `branch =` field tells future operators which branch contains the recovery commit.

3. **Advance the gitlink**:

    ```bash
    git add <sub-path> .gitmodules
    PAGER=cat git diff --submodule=log --cached <sub-path>
    ```

    * `--submodule=log` — renders the gitlink advance as a one-line commit summary, perfect for review.

4. **Commit the parent re-point**:

    ```bash
    git commit -m "chore(submodules): align <sub-name> with personal fork

- Update URL from <original-url> to <fork-url>.
- Track branch fix/register-submodules on the fork (contains the registration of nested submodule <X> and
    the removal of the unrecoverable <Y> orphan gitlink).
- Advance gitlink <old-sha>..<new-sha> to the fork commit.
- Enables full recursive init (recovers <X> from upstream <X-source-url>) without depending on the
    read-only <original-owner> upstream."
    ```

***

## 7. Verification

Confirm end-to-end recovery from a clean perspective.

1. **Recursive init**:

    ```bash
    PAGER=cat git submodule update --init --recursive 2>&1 | tail -10
    ```

2. **Zero uninitialized**:

    ```bash
    PAGER=cat git submodule status --recursive | grep '^-' && echo "FAIL: uninit pointers remain" || echo "OK"
    ```

    * Lines starting with `-` mean uninitialized; an empty result is the success signal.

3. **Zero empty submodule directories**:

    ```bash
    PAGER=cat git submodule foreach --recursive --quiet \
        'if [ ! -e .git ]; then echo "EMPTY: $displaypath"; fi'
    ```

***

## 8. Operational Safety

- **No Force Push**: This protocol NEVER force-pushes. The recovery branch is fresh; rebases against the upstream
  default branch are out of scope.
- **No Upstream PR by Default**: Opening a pull request to the original (read-only) upstream is **out of scope** for
  this skill. The agent MUST ask the user before creating any cross-org PR; the recovery is consumed locally via the
  parent's re-pointed `.gitmodules`.
- **Token Hygiene**: Print only the token prefix (`${GH_TOKEN:0:7}…`). The full token MUST never appear in command
  output, commit messages, or saved logs.
- **Unrecoverable Drop Justification**: Before `git rm --cached`-ing an orphan, the agent MUST present the empty
  `count`-from-search-and-cache evidence to the user and obtain explicit approval. A wrongly-dropped gitlink is
  recoverable from reflog only briefly.
- **Fork Naming Discipline**: When forking, `--fork-name` MUST equal the original repo name unless the user
  explicitly requests otherwise; mismatched fork names break the fork-sync protocol.

***

## 9. Composition Rationale

This skill is a **domain composer** that orchestrates two existing primitives plus a new domain-specific
discovery (orphan-gitlink detection):

```text
                ┌─ git-submodule-dead-upstream-audit  (SHA → repo search) ┐
git-submodule- ─┤                                                          ├─→ recovery commit + parent re-point
orphan-gitlink- │                                                          │
recovery        └─ git-submodule-fork-reconfigure     (write-access fix)  ─┘
```

* **SHA discovery primitive**: reused verbatim from
  [git-submodule-dead-upstream-audit](../git-submodule-dead-upstream-audit/SKILL.md) §4.
* **Fork + remote swap primitive**: reused verbatim from
  [git-submodule-fork-reconfigure](../git-submodule-fork-reconfigure/SKILL.md) §2–§3.
* **New primitive owned here**: orphan detection (§2), recovery-vs-drop verdict (§3.3), parent re-point with
  `branch =` field (§6).

Inlining either primitive into this skill is **FORBIDDEN** by the Layered Composition Mandate; if a fix lands in
either base skill it MUST flow through to this composer automatically.

***

## 10. Related Skills

- [Git Submodule Dead Upstream Audit](../git-submodule-dead-upstream-audit/SKILL.md) — SHA-to-repo discovery
  primitive; this skill reuses its `search/commits` protocol.
- [Git Submodule Fork Reconfigure](../git-submodule-fork-reconfigure/SKILL.md) — fork + remote swap primitive;
  this skill invokes it whenever the parent submodule is read-only.
- [Git Submodule Removal](../git-submodule-removal/SKILL.md) — invoked instead of this skill when the **entire**
  submodule (not a nested orphan) is dead.
- [Git Submodule Pointer Repair](../git-submodule-pointer-repair/SKILL.md) — invoked when the gitlink itself is
  invalid (points to a SHA that does not exist anywhere), as opposed to merely unregistered.

## Composition by Higher-Level Skills

| Composer | Role | Reuses From This Skill |
| :--- | :--- | :--- |
| [`git-submodule-uninitialized-handler`](../git-submodule-uninitialized-handler/SKILL.md) | Drives every uninitialized pointer to a fully-initialized state. | Phase 2 — invoked once per orphan-containing submodule to register recoverable orphans and drop unrecoverable ones. |

***

## 11. Traceability

- Origin session: **AI Suite Submodule Audit** (May 2026) — recovered
  `ljt-520_openclaw-backup/Star-Office-UI` from `ringhyacinth/Star-Office-UI` and dropped unrecoverable
  `ljt-520_openclaw-backup/thirdparty_bizs` via personal fork `Baneeishaque/openClaw-backup` on branch
  `fix/register-submodules`.
- Standard authority: [Skill Factory](../skill-factory/SKILL.md) §2.0 (Layered Composition).
- Compatibility: macOS, Linux, Windows (Git Bash / Zsh).
