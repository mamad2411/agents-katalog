---
name: catchup
description: Deep-recovery resume. Rebuild a project's working state from the
  brain when the automatic SessionStart brief is missing, flagged STALE, or
  contradicts the repo. Spawns one subagent that reads the state note, recalls
  digests and episodes, cross-checks against the real repo, and returns a short
  distilled brief. Use when asked to "catch up", "/catchup", "deep resume",
  "reconstruct state", or when the injected state note carries a STALE banner.
---

# catchup

Reconstruct a project's working state from the hosted brain and hand the main
session one distilled brief to act on, without spending the main window on
the retrieval.

This is the DEEP path. The routine path is automatic: the
`brain-remote-session-start` SessionStart hook injects the project's state
note at session start, stamped with freshness. Reach for /catchup only when
that brief is missing (no state note yet), carries the STALE banner, or
visibly disagrees with the repo.

All the legwork happens inside ONE subagent; the main window only holds the
brief.

## 1. Resolve the project

- Use the `/catchup <project>` argument if given.
- Else infer from the conversation topic or cwd (basename of the repo).
- If ambiguous (no arg, no clear cwd or topic), ask once, then proceed.
  Never silently guess between two live candidates.
- Headless (`claude -p`, no user to ask): infer from cwd, proceed, and record
  the inference in the brief's Staleness warnings.

## 2. Spawn ONE subagent (model: opus) with this exact brief

Give the subagent this brief verbatim, substituting `<project>`:

> You are reconstructing the working state of the `<project>` project from
> the hosted brain (MCP server `brain`). Load the tools with ToolSearch
> `select:mcp__brain__state_get,mcp__brain__recall,mcp__brain__get_episode`
> if they are deferred. If any brain tool fails with an auth error, stop and
> report "brain sign-in expired: run /mcp and sign in again". Run, in order:
>
> 1. If `brain-push` is on PATH, run `brain-push` once (best-effort; it
>    records this machine's latest sessions). On failure note "latest
>    sessions may not be recorded" and continue.
> 2. `state_get("<project>")`: the rolling state note. `found: false` means
>    no note yet; say so and fall back to digests and episodes.
> 3. `recall("<project> state decisions next steps")`, then
>    `recall("<project>", scope="summaries")`. Fetch the full text of the
>    top 1 to 3 hits with `get_episode(id)`; snippets are too thin to brief
>    from.
> 4. Cross-check freshness against the target repo's own `git log -5
>    --oneline` and `git status`. The brain is only current through the last
>    checkpoint or reflect; if the repo moved past it, **trust the repo** and
>    flag the drift.
> 5. Verify every file path and command you are about to cite still exists.
>
> Return ONLY a distilled brief, about 400 words at most, in exactly this
> structure:
>
> - **Task**: what this project is and what we were doing.
> - **State**: done, in progress, blocked, each with evidence (commit
>   hashes, verdicts, test results).
> - **Decisions already made**: calls not to re-litigate.
> - **Single next action**: the one concrete first step.
> - **Verified pointers**: exact file paths and commands, each confirmed to
>   exist.
> - **Staleness warnings**: only if the brain lagged reality, the state note
>   was missing, sessions may be unrecorded, or a pointer failed to verify.
>   Omit if clean.
>
> Do not return raw recall output, transcripts, or file dumps; only the brief.

## 3. Relay and act

- Relay the subagent's brief, then act on the **Single next action**.
- Do NOT re-run recall or re-read anything the subagent already distilled.
  If the brief is over length or missing a section, send it back with a
  sharper brief; never fill the gap by reading in the main window.
- If a staleness warning changes the plan, surface it before acting.

## Degradation

- Brain tools unavailable or signed out: the subagent reports it and briefs
  from the repo alone, flagged.
- No state note for this project: fall back to digests and episodes; note it.
