---
name: ship
description: Take a finished local change through verification, UI checks, pull-request publication, CI and review follow-up, and the user-authorized merge outcome. Use when implementation is complete and the user says "ship it" or "get this merged," or as the final stage of $build. Do not use to implement new feature scope.
---

# Ship

Read the applicable `AGENTS.md`. Require a finished, cleaned diff or commits ahead of the intended base. If there is nothing to ship, ask for the missing scope.

1. Run `$verify` to prove the behavior end to end and sweep relevant edge cases.
2. Run `$design` when the diff touches a user-facing surface.
3. Run `$docs` first when an externally produced change altered architecture, interfaces, commands, configuration, or documented workflows.
4. Run `$pr` to stage the confirmed scope, commit, push, and open the PR through the GitHub-backed publishing workflow.
5. Run `$babysit` to monitor CI and review feedback through the terminal condition authorized by the user.

A blocking finding stops the pipeline. Fix it only when the requested scope authorizes that work, re-run the failed stage, and continue. Never carry a known-broken change forward.

- If `$verify` finds a required behavior missing during `$build`, return to `$implement` with a failing test and the no-commit constraint established by `$build`. In standalone `$ship`, report the missing implementation instead of expanding feature scope.
- Re-run relevant tests after any stage changes code.
- Use collaboration subagents for noisy independent verification or monitoring work when available, and pass concise reports between stages.
- A request limited to opening a PR does not authorize merge. Enable auto-merge or merge directly only under `$babysit`'s explicit authorization rules.
