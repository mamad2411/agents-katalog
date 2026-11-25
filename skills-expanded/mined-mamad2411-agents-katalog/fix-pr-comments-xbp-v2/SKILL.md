---
name: fix-pr-comments-xbp-v2
description: >
  Blazing-fast CLI-only PR review fixes. Auto-detects discussion_r / issuecomment /
  paste from any args. Fixes ALL provided discussion + issue comments (mixed never
  drops either). Multi-PR / multi-repo: groups every GitHub URL by owner/repo#pr and
  fans out parallel agents with isolated worktrees so different PRs, branches, and
  repositories can run simultaneously in one invocation. Concurrent-safe log dirs.
  ONE agent per PR end-to-end (red→green + ship). No MCP, no multi-phase ceremony.
---

# fix-pr-comments-xbp-v2 — FAST + FIX ALL + MULTI-PR PARALLEL

| Path | `~/.grok/workflows/fix-pr-comments-xbp-v2.rhai` |

## Contract

- **Every** `#discussion_r` and **every** `#issuecomment-` in the input is a MUST_FIX target.
- Mixed input (`discussion_r` + `issuecomment`) does **not** drop issue comments.
- Issuecomment bodies: fix **every** P0–P3 block inside each body.
- Unscoped: fix **all** unresolved review threads (soft max only if inventory is huge).
- Optional `max_comments` is a soft ceiling; listed IDs are never skipped.

## Multi-PR / multi-repo (single invocation)

URLs from **different PRs**, **different branches**, or **different repositories** in one
paste / `discussion_urls` list are **grouped by `owner/repo#pr`** and fixed **in parallel**:

| Input mix | Behavior |
|-----------|----------|
| One PR (any number of discussion_r + issuecomment) | 1 agent, PR-scoped worktree |
| Same repo, PR #512 + #513 | 2 parallel agents, `…/pr-512` + `…/pr-513` worktrees |
| `xylex-group/athena#512` + `other-org/foo#99` | 2 parallel agents; foreign repo cloned to `~/.xbp/repos/<owner>-<repo>` then worktree |
| Bare PR URLs only | Unscoped fix-all per PR, still parallel |

Grouping sources:

- `https://github.com/{owner}/{repo}/pull/{N}#discussion_r{ID}`
- `https://github.com/{owner}/{repo}/pull/{N}#issuecomment-{ID}`
- Bare pull / files / review URLs (`…/pull/N`, `…/pull/N/files`, …)
- `discussion_urls`, `urls`, `links`, `paste`, `query`, …

Bare `discussion_r` / `issuecomment-` ids without a full URL attach to the only group, or
to `args.pr` / the first group when multi.

Each agent uses **full PR URLs** with xbp (`xbp github pr view https://github.com/…/pull/N`)
so cross-repo network ops never depend on the session cwd remote.

## Concurrent isolation

| Resource | Isolation |
|----------|-----------|
| Code edits / commit / push | `git worktree` at `%USERPROFILE%\.xbp\worktrees\<owner>-<repo>\pr-<N>` |
| Foreign repo base | `%USERPROFILE%\.xbp\repos\<owner>-<repo>` (`gh repo clone` if missing) |
| Logs / proof / last-agent | `%USERPROFILE%\.xbp\logs\fix-pr-comments-xbp-v2\<owner>-<repo>\pr-<N>\` |
| Shared session workspace | **Never** `gh pr checkout` / stash / reset here |

Also safe across **separate** workflow runs (e.g. two `/workflow` launches).

Args: `use_worktree` (default true), `worktree_path` (single-PR override only),
`skip_checkout` (exceptional), `repo` (`owner/repo` when URLs omit host).

## Speed model

| Input | Agents |
|-------|--------|
| Single PR (any mix of discussion_r / issuecomment / paste) | **1** |
| N distinct `owner/repo#pr` groups | **N** (parallel) |
| Unscoped full inventory (1 PR) | **1** |
| `force_wide` + multi groups | **N** wide agents |

No bootstrap / fix / verify / ship fan-out.

## Auto-detect

Reads `query`, `objective`, `paste`, `discussion_urls`, `url`, …  
Classifies per group: `mixed` | `discussion_r` | `issuecomment` | `paste` | unscoped.  
`dry_run: true` writes `scratch/dry.json` with `groups[]` + `multi` for inventory without agents.

## Invoke

```text
/workflow fix-pr-comments-xbp-v2 https://github.com/…/pull/N#discussion_rID https://github.com/…/pull/N#issuecomment-ID
/workflow fix-pr-comments-xbp-v2 https://github.com/org/a/pull/1#discussion_r1 https://github.com/org/b/pull/2#issuecomment-9
agent_budget: 48   # raise when multi-PR (≈1 agent per PR group)
```

### Empty invocation aborts

Bare `/fix-pr-comments-xbp-v2` (no URL, no `pr=N`, no discussion/issuecomment ids, no review paste)
**aborts immediately** — it does **not** invent an unscoped “fix everything on the current branch” run.

| Input | Result |
|-------|--------|
| No links / no PR / no paste | `aborted: true`, `scratch/abort.json`, no agents |
| PR number only (`pr: 518` or `…/pull/518`) | Unscoped fix-all on that PR (allowed) |
| `discussion_r` / `issuecomment` / paste | Scoped fix (normal) |
| Empty + `allow_unscoped: true` | Opt-in unscoped (detect PR yourself; rare) |
## Agent rules (baked in)

- Focused test only — never whole monorepo suite  
- Allowlist commit once per PR group  
- `reply --if-not-fixed` + `resolve` for each review thread  
- Prefer `xbp … -m BODY` or `--body-file -` (stdin); keep logs under `%USERPROFILE%\.xbp\logs\`  
- **Avoid `*tmp*` worktree artifacts**  
- If any in-repo file basename matches `*tmp*`: append `**/<exact-basename>` to `.gitignore`, ensure prefix catch-all (`**/tmp*`, `**/.tmp*`), never stage/commit the tmp file  
- Top-level `pr comment` summarizing issuecomment findings  
- `proof-table` once per PR at end (payload outside repo)  
- `results[]` must cover every MUST_FIX target for that PR  

## Telemetry

`scratch/telemetry.json` (schema_version 4), `run.log`, `performance.md`.  
Multi runs: aggregated report with one section per `owner/repo#pr`.
