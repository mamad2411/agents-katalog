---
name: github-ecosystem-discovery
description: "Map a local GitHub repository ecosystem — discover all cloned repos, extract owner/purpose/status, cross-reference against GitHub, detect duplicates/stale repos, produce structured inventory"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Ecosystem, Inventory, Repository, Discovery, Auditing]
    triggers: [github ecosystem map, map my repos, repo inventory, ecosystem discovery, list all repos, portfolio audit, repo sprawl, duplicate clones, stale repos, audit repos]
    related_skills: [github, project-inventory]
prerequisites:
  commands: [git]
---

# GitHub Ecosystem Discovery

Systematically map ALL local repository clones into a structured inventory — discover repos, extract remotes, infer purpose from READMEs, categorize by owner/domain, and produce a comprehensive markdown output.

## When to Use

- User asks "map all my repos", "list my GitHub ecosystem", "how many repos do I have"
- User wants a categorized inventory of their cloned repositories
- User needs to audit what's checked out locally vs what's on GitHub
- User wants to know which repos are owned vs forked vs third-party
- General "what's in my github/ directory" questions
- Portfolio audit: user wants sprawl/duplicate/stale-repo analysis with evidence and prioritized recommendations (do not edit anything) — see `references/portfolio-audit-workflow.md`

## Workflow

### Phase 1: Discover

List all actual git repos under a parent directory. Skip non-repo directories and temp workspaces:

```bash
# Find all directories that are git repos in a parent folder
ls -d /path/to/parent/*/

# For each, check if it has a .git subdirectory and get the remote
for d in /path/to/parent/*/; do
  name=$(basename "$d")
  if [ -d "$d/.git" ]; then
    remote=$(cd "$d" && git remote -v 2>/dev/null | head -2)
    echo "=== $name === (GIT)"
    echo "$remote"
    echo
  fi
done
```

**Critical batching trick:** Run one shell loop over ALL directories instead of per-directory `git remote` calls. A single `for d in */; do ... done` loop handling 130+ directories completes in seconds.

### Phase 2: Extract Remotes

For each repo, extract:
- **Origin URL** — the primary remote (owner/repo parsed from it)
- **Other remotes** — upstream, fork, or legacy remotes (sometimes a repo has multiple remotes pointing to different forks)
- **Owner/Org** — parse from URL: `https://github.com/{owner}/{repo}.git`
- **No remote** — local-only directories that may be configs or WIP

```bash
# Fast batch extraction of all remotes across ALL repos
cd /path/to/parent
for d in */; do
  name=$(basename "$d")
  if [ -d "$d/.git" ]; then
    remote=$(cd "$d" && git remote -v 2>/dev/null | head -4)
    if [ -n "$remote" ]; then
      echo "=== $name ==="
      echo "$remote"
    else
      echo "=== $name === (no remote)"
    fi
  fi
done
```

### Phase 3: Infer Purpose

For every repo that has a remote, read the README to determine purpose:

```bash
# Quick skim of README for purpose
cd /path/to/repo
cat README.md 2>/dev/null | head -10

# For bigger repos, extract the h1-title and first paragraph
cat README.md 2>/dev/null | head -30 | grep -E '^#|^>' -A2 || echo "No README"
```

When a README has badge-heavy headers, skip the badges and read the paragraph after the first `>` block or after `---` separator.

### Phase 4: Cross-Reference & Categorize

Build the categorization:

| Category | Signal | Examples |
|----------|--------|---------|
| **Owned (pmb2/*)** | URL contains `github.com/{username}/` | `pmb2/hermes-config`, `pmb2/agent-fleet` |
| **Forked** | URL contains upstream org (not user) | `NousResearch/hermes-agent` |
| **Third-party/Starred** | Any other org | `langchain-ai/langchain`, `microsoft/playwright-mcp` |
| **Local-only** | No remote or no origin | `councilOS`, `scripts/` |

Categorization hints from directory contents:
- If a directory has only a README.md, it's likely WIP or a documentation stub
- If a directory has subdirectories like `agents/`, `teams/`, configs — it's likely a multi-agent workspace
- If a directory has `Dockerfile`, `docker-compose.yml` — infrastructure/project
- If the git log shows recent commits — it's active; old commits — inactive/archived

### Phase 5: Output

Write structured markdown:

```markdown
## 🔷 CATEGORY

| # | Name | URL | Purpose | Status |
|---|------|-----|---------|--------|
| N | **repo-name** | `https://github.com/owner/repo` | One-line purpose from README | Active / Inactive |

```

**Status heuristics:**
- **Active** — git log shows commits in last 30 days OR user is actively using it
- **Inactive** — no recent commits, or repo is a one-time checkout
- Use judgment: a frequently-referenced MCP server with old commits is still "Active" if it's part of the running toolset

### Phase 6: Add Summary Tables

End with aggregate stats so the user can immediately assess scale:

```markdown
| Owner | Count | Key Projects |
|-------|-------|-------------|
| **pmb2** | N | project1, project2, project3... |
| **Third-party** | N | Various starred/exploratory forks |

Total: **NNN** repositories catalogued.
```

## Portfolio Audit Mode (sprawl / duplicates / staleness)

The above phases map a single parent dir. For a full portfolio audit, extend across ALL clone roots and cross-reference against GitHub. A working, tested recipe with exact commands lives in `references/portfolio-audit-workflow.md`.

### Multi-root discovery + duplicate detection

1. Scan every clone root (e.g. `C:/Users/<user>`, `C:/Users/<user>/Documents/github`, `C:/Users/<user>/Projects`, `C:/Users/<user>/PycharmProjects`, `${MY_REPOS}/Documents/github`) for dirs containing `.git`.
2. For each repo, capture: `last-commit-date | origin-remote | dirty-file-count | branch | path` (one line per repo, written to a file for later processing).
3. **Duplicate clones** = the same normalized remote (`owner/repo`, case-insensitive, strip `https://github.com/`, `.git`) appearing in >1 path. Report each clone's age and dirty count so the user can pick the canonical one (keep newest + canonical location; flag dirty clones for commit/push before deletion).
4. **Local-only dirs** = repos with no origin remote (config/WIP/backups) — e.g. a `BookEnds_bak/` that is not even a git repo (just stale docs).

### GitHub-side cross-reference

```bash
gh repo list <owner> --limit 200 --json name,updatedAt,pushedAt,isArchived,primaryLanguage,description \
  --jq '.[] | select(.isArchived==true) | .name'
```

- **Stale** = pushedAt >270d (archive candidates); flag >1yr separately.
- **Missing descriptions** = `description==null` — bulk professionalization via `gh repo edit <name> --description "..."`
- **GH-only repos** = GitHub repos with no matching local clone (case-insensitive match on name!).
- **Skill/reference drift** — cross-check any existing inventory skill's claims (repo count, archived set) against the live API; inventories go stale fast and the skill should carry a "verified against API on <date>" note.

## Pitfalls

1. **Git remote ambiguity** — A repo can have multiple remotes (origin + legacy + upstream). Always check all remotes with `git remote -v`, not just `git config --get remote.origin.url`.
2. **Non-repo directories** — Not every directory under `github/` is a repo. Some are local config folders, temp checkouts, or documentation mounts that happen to have `git remote` output from another scope. Check `.git` exists.
3. **Name collision across skill stores** — Skills with the same relative path in `AppData\Local\hermes\skills\` and an external `hermes-config\skills\` collide on load. When this happens, note it for the curator. The collision blocks `skill_view` and `skill_manage` from loading or patching the skill.
4. **Private repos in README** — Some READMEs have "Proprietary and confidential" headers. Respect the license and note the repo as closed-source rather than inferring fine-grained functionality.
5. **README extraction** — For large repos, default `cat README.md | head -10` may skip past auto-generated badges and not reach the actual description. Scan for the first paragraph after `---` or the first `>` block line.
6. **Performance at scale** — Running 130+ `cd path && git remote -v` calls sequentially in a shell loop is fast (seconds). Avoid per-repo `git clone --bare` or full `git fetch` — those are overkill.
7. **Detached HEAD repos** — Some repos may be on a detached HEAD (no branch checked out). `git remote -v` still works for these.
8. **Symlinked repos** — If the parent directory has symlinks to repos elsewhere, `ls -d */` shows them but `cd $d` may break. Use `find -L` to follow symlinks when needed.
9. **`git -C` fails on MSYS paths (Windows/git-bash)** — `git -C ${MY_REPOS}/.../repo` errors with `cannot change to ...: No such file or directory` even though the path exists. Workaround: `( cd "$d" && git ... )` in a subshell — `cd` resolves the MSYS path to a native Windows path that git accepts. This bit the whole scan once; always use `cd`+subshell, never `git -C`, when paths are MSYS-style.
10. **Native Python may not resolve MSYS paths** — `execute_code`/Python `open()`/`os.path.isdir` on `/c/...` or `/e/...` paths can FileNotFoundError or silently miss dirs. Bash (git-bash) handles them fine. Do the filesystem scan in bash, emit a `|`-delimited file, then post-process in Python with the file's contents — not MSYS paths.
11. **Case-insensitive name matching for GH cross-reference** — GitHub repo names are case-preserved but lookups should compare lowercase on both sides (`CsFloat` local remote vs `csfloat` GH name). Case-sensitive comparison produces false "GH-only repo" positives.
12. **Slow secondary drives** — `du -sh` across a whole E: drive can time out (180s+). Use targeted `du` on specific dirs only, or rely on `git log`/file listings for age/size evidence.
13. **`.git` may be a file, not a dir** — submodules and worktrees have a `.git` file pointing elsewhere. `[ -d "$d/.git" ]` skips them; decide explicitly whether to include worktrees.

## Related Tools

- This skill produces a markdown inventory file that complements `project-inventory` (which tracks pmb2 GitHub projects specifically)
- `references/portfolio-audit-workflow.md` — tested end-to-end audit recipe (bash scan script, Python post-processing, staleness thresholds, 2026-08-07 baseline snapshot)
- For LOC/codebase size analysis of discovered repos, see `codebase-inspection` skill
- For extracting starred/owned repos from GitHub API, see `github-stars-extraction`
