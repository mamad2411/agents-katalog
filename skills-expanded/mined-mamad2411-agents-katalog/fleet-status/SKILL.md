---
name: fleet-status
description: "One ranked snapshot of everything in flight — agent sessions that need an answer, open PRs with CI and review state, dirty or unpushed repos, background jobs, and the pending backlog. Use when the user asks what's going on, what needs them, what's still running, what's open, or is walking away and wants the state out of their head. Triggers on 'fleet status', 'what's running', 'what needs me', 'what's open', 'status of everything', 'where did I leave things'."
---

# Fleet status

Answers one question — **what is actually blocked on me right now** — and
answers it in under twenty lines, ranked, with the full detail one flag away.

The point is not to list everything. `AGENTS.md` already lists everything and
went unread for a week; a status-bar count (`9 fronts · 4 need you`) replaced it
and was worse, because a number with no referent says there is a fire without
saying where. This skill is the thing in between.

## Steps

1. **Run the collector.** It is read-only — no merges, no deletions, no session
   is touched.

   ```
   uv run --project "${CLAUDE_PLUGIN_ROOT}/scripts" "${CLAUDE_PLUGIN_ROOT}/scripts/fleet_status.py"
   ```

2. **Print the digest exactly as the script emitted it.** Do not re-narrate,
   re-sort or re-summarize it. The ranking is deliberate (see below) and
   re-writing it in prose is how the two views drift apart.

3. **Add the scheduled routines the script cannot see.** It prints
   `Scheduled: not tracked` because routines live server-side and only a live
   session can enumerate them. You are a live session: call `CronList` and, if
   there are any, add one line — `Scheduled: N routine(s) — <names>`. If the
   tool is unavailable, leave the line as printed.

4. **Offer two or three concrete next actions**, drawn from the ranked list and
   phrased as questions — "merge #118?", "kill `claude-work-01102909`, idle
   12d?". Wait for the user to pick. **Never act on your own**: no merging, no
   closing, no killing sessions, no deleting branches or worktrees. If they
   pick one, do that one thing and stop.

## Flags

| Flag | Use |
|---|---|
| *(none)* | Ranked digest. Refreshes `AGENTS.md` and `fleet.json`. |
| `--full` | Print the whole `AGENTS.md` report. Use when the user asks for everything, or for a specific session or repo. |
| `--json` | Print `fleet.json` — the same data for another program. |
| `--fresh` | Re-query GitHub, ignoring the 5-minute PR cache. Use after a merge. |
| `--offline` | Skip GitHub. Use when `gh` is unavailable or the network is down. |
| `--no-write` | Print without refreshing the cached files. |

## How the ranking works

Read this before you decide the digest is "wrong". The order is by *what is
blocked on a decision only the user can make*:

1. **Approved PR awaiting merge** — nothing else moves until they click.
2. **Red CI on a PR they own** — rotting, and blocking anything stacked on it.
3. **A stack of PRs** — collapsed to one line with its merge order, because
   four PRs that must land in sequence are one decision, not four.
4. **A session in `waiting_input`, under 12 hours old** — an agent asked a
   question. Past 12 hours it is an abandoned tab, and it moves to a
   `stale prompt(s)` count instead.
5. **Collisions** — two live sessions holding the same file.

The list is capped at 8. If there are more, the count is shown and the rest are
in `--full`. An unbounded urgent list is the same overwhelm in a new font.

Under the list, `IN FLIGHT (N)` is **every** agent still on the board — the
ones waiting on the user included, since they are running too. Do not read it
as a separate population from the ranked list; the same session appears in
both, and the breakdown after the total says which is which.

## Reading the output honestly

- **"not tracked" is not "none".** `Scheduled: not tracked` means the script
  cannot see server-side routines — never say there are none on that basis.
  Same for `PRs: gh unavailable`.
- **"not visible to this token"** is a standing fact about the GitHub
  credential (a repo in another org, or outside the App installation), not a
  failure. Do not offer to fix it unless asked.
- **"stale" on a background job is a guess.** The roster's pids belong to
  another container's process namespace, so nothing can confirm a death from
  here; staleness comes from the file's own clock.
- **A repo that timed out lowers the PR count.** When `N repo(s) unreachable`
  is non-zero, the totals are a floor, not a total. Say so if it matters.

## Requirements

- **`git`** — for repo state. Without it the repo section is empty.
- **`gh`, authenticated** — for pull requests. Without it the digest prints
  `PRs: gh unavailable — not read` and everything else still works. Install the
  GitHub CLI and run `gh auth login` to enable it.
- Neither is required for the skill to run. Every source degrades to "not
  collected" on its own, and never to a silent zero.

## Notes

- Outputs are **caches**: `AGENTS.md` and `fleet.json` under the plugin data
  directory. Delete them and the next run rebuilds them. Nothing reads either
  as state; the session registry and the checkpoints remain the only source of
  truth.
- The digest, `AGENTS.md` and `fleet.json` are three renderings of **one**
  collection, so they cannot disagree about the same fleet.
- Tidying up — deleting merged branches, removing dead worktrees, garbage
  collecting finished sessions — is deliberately **not** here. It is a separate
  follow-up, behind an explicit flag, because unreviewed deletion at the moment
  someone is most overloaded is how trust in a tool dies on its first false
  positive.
