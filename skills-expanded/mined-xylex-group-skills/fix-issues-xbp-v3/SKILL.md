---
name: fix-issues-xbp-v3
description: >
  Global CLI-only fix workflow extending fix-pr-comments-xbp-v2. Accepts GitHub
  issue URLs (/issues/N), PR discussion_r / issuecomment / pullrequestreview
  links, bare PR URLs, and review paste. Groups by owner/repo#issue-N or
  #pr-N and fans out parallel isolated worktrees. One agent per target
  (red→green + ship). No MCP.
---

# fix-issues-xbp-v3 — issues + PR reviews (extends v2)

| Path | `~/.grok/workflows/fix-issues-xbp-v3.rhai` |
| Base | `fix-pr-comments-xbp-v2` (PR path preserved) |

## What it accepts

| Input | Group key | Agent path |
|-------|-----------|------------|
| `https://github.com/{o}/{r}/issues/{N}` | `o/r#issue-N` | Issue fix (body + comments → branch → red→green → PR + issue comment) |
| `…/issues/{N}#issuecomment-{ID}` | `o/r#issue-N` | Same + MUST_FIX that comment |
| `…/pull/{N}#discussion_r{ID}` | `o/r#pr-N` | v2 PR thread fix |
| `…/pull/{N}#issuecomment-{ID}` | `o/r#pr-N` | v2 issuecomment fix |
| `…/pull/{N}#pullrequestreview-{ID}` | `o/r#pr-N` | Review-body findings |
| Bare `…/pull/{N}` | `o/r#pr-N` | Unscoped unresolved threads |
| Review paste (P0–P3 / Codex) | PR group(s) | paste / mixed |
| `issue=231` + `repo=owner/repo` | issue group | Issue fix |

Mixed issues + PRs + repos in **one** invocation → **parallel** agents (one per group).

## Contract

- **Every** listed issue, `discussion_r`, `issuecomment`, and `pullrequestreview` is a MUST_FIX target.
- Mixed classes never drop a class.
- Issuecomment / review bodies: fix **every** P0–P3 (or acceptance-criteria bullet) inside.
- Optional `max_comments` is a soft ceiling; listed IDs are never skipped.
- Empty invocation (no URL / issue / PR / paste) **aborts** — no agents.
- Opt-in empty: `allow_unscoped=true` or `allow_empty=true`.

## Concurrent isolation

| Resource | Isolation |
|----------|-----------|
| PR edits | `%USERPROFILE%\.xbp\worktrees\<owner>-<repo>\pr-<N>` |
| Issue edits | `%USERPROFILE%\.xbp\worktrees\<owner>-<repo>\issue-<N>` |
| Foreign repo base | `%USERPROFILE%\.xbp\repos\<owner>-<repo>` |
| Logs | `%USERPROFILE%\.xbp\logs\fix-issues-xbp-v3\<owner>-<repo>\{pr\|issue}-<N>\` |
| Shared session workspace | **Never** switch branch here |

## Issue agent rules

1. `xbp github show` / `gh issue view` + comments  
2. Isolate worktree from default branch → `fix/issue-N-…`  
3. Extract body + comment requirements (checklists, bugs, P0–P3)  
4. RED (failing focused test) → implement → GREEN  
5. Allowlist commit once; push; `gh pr create` with `Fixes #N` when `push` true  
6. `xbp github comment N -m …` with SHA + proof (+ PR URL)  
7. Close only if `close_issue: true` and fully done (default **false**)

## PR agent rules (same as v2)

- Focused test only — never whole monorepo suite  
- Allowlist commit once per PR group  
- `reply --if-not-fixed` + `resolve` for review threads  
- Prefer `xbp … -m` / `--body-file -`; logs under `~/.xbp/logs/`  
- Avoid `*tmp*` worktree artifacts; gitignore if unavoidable  
- `proof-table` once per PR at end  

## Invoke

```text
/workflow fix-issues-xbp-v3 https://github.com/xylex-group/xbp/issues/231
/workflow fix-issues-xbp-v3 https://github.com/xylex-group/xbp/issues/231 https://github.com/xylex-group/xbp/pull/500#discussion_r123
/workflow fix-issues-xbp-v3 issue=231 repo=xylex-group/xbp
/workflow fix-issues-xbp-v3 dry_run=true urls=[...]
```

### Args

| Arg | Default | Meaning |
|-----|---------|---------|
| `paste` / `query` / `urls` / `issue_urls` / `issues` / `issue` | — | Scope input |
| `discussion_urls` / `review_urls` / `reviews` | — | Extra URL lists |
| `pr` / `repo` | — | Bare PR / owner/repo |
| `dry_run` | false | Inventory only → `scratch/dry.json` |
| `push` | true | git push (+ issue PR create) |
| `reply` | true | GitHub replies / issue comments |
| `close_issue` | false | Allow closing fully fixed issues |
| `use_worktree` | true | Isolated worktrees |
| `max_comments` | uncapped | Soft ceiling |
| `max_concurrency` / `concurrency` | **4** | Parallel agent batch size (v3.1). `0` = uncapped legacy |
| `force_wide` | false | Force wide inventory path for PRs |
| `allow_unscoped` | false | Allow empty → invent unscoped run |

### Cost controls (v3.1)

- **Batched fan-out** — multi-target runs use `max_concurrency` (default 4) instead of launching every group at once (20 parallel cold worktrees burned ~26M tokens / 36 min wall on a full issue batch).
- **Slim `run_schema`** — fewer required fields; `tool_trace` optional (≤12).
- **Short isolation + LEAN caps** — `MAX_SEARCH=8`, no monorepo suite, shared `CARGO_TARGET_DIR=%USERPROFILE%\.xbp\cache\cargo-target\<slug>`.
- **Tighter INPUT caps** — paste/context ~3–4k chars per agent.
- Legacy full-blast: `max_concurrency=0`.

## Auto-run suggestion

When the user pastes several `github.com/.../issues/N` and/or mixed PR discussion URLs and asks to fix them, launch:

```text
name: fix-issues-xbp-v3
args: { paste: "<full message>", urls: [...deduped...], pr?: N, issue?: N }
agent_budget: 48+   # ≈1 agent per target group
```

Prefer this over `fix-pr-comments-xbp-v2` when **any** `/issues/` URL is present; otherwise v2 remains fine for pure PR reviews.

## Telemetry

`scratch/telemetry.json` (schema_version 4), `run.log`, `performance.md`,  
`scratch/fix-issues-xbp-v3-report.md`. Multi: one section per group.
