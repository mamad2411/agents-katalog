---
name: finish-work
description: >-
  Use when a change is ready ("finish", "wrap up", "we're done", "open the PR"). Checks the docs moved with the
  change, runs the full gate and, for the extension, the client or a tool, the live suites where a Kit app runs,
  commits, opens a draft PR, reviews it with review-code until it is clean, and asks the maintainer to mark it ready
  or merge it; the maintainer squash-merges.
---

# Finish a change

Done means `uv run tools/gate.py full` passed, `REVIEW.md` is answered and `review-code` is clean, not that the work
feels complete. `main` takes PRs only, and the maintainer squash-merges them (`AGENTS.md`, How a change lands).

## Steps

1. **Docs in the same change.** Check each thing that describes the change moved with it: `docs/TOOLS.md` for a
   tool, `docs/ARCHITECTURE.md` for a route, the protocol or the token, the extension's `docs/README.md` for its
   settings, `README.md`, `CHANGELOG.md` under Unreleased when users notice it, `AGENTS.md` for a changed path, command
   or rule, and the plan when the work departed from it (where and why). A plan with a progress log gets the step's
   row. Write them the way `AGENTS.md` asks.
2. **The gate:** `uv run tools/gate.py full`. Fix every failure; never weaken a test, a check or a baseline to pass.
3. **The live suites,** for a change to the extension, the client or a tool, when a Kit app runs `ovmcp.bridge`:
   `OMNIVERSE_MCP_SIM=1 uv run pytest tests/test_integration.py tests/test_scenarios.py` (PowerShell:
   `$env:OMNIVERSE_MCP_SIM = "1"`, then `uv run pytest ...`). Note the Kit app and its version, what passed, and which
   failures `main` has too on the same Kit. A headless Isaac Sim starts only if the person who accepts NVIDIA's EULA
   set `OMNI_KIT_ACCEPT_EULA=YES`. No Kit app: say so; the PR says they did not run. A change to a tool's
   description, the server's instructions or a plugin skill also runs the AI scenario phases that use them
   (`run-scenarios`) when a Kit app runs on 8212, and the PR says whether it did: for a tool, the phases of
   `test_project/scenarios.md` whose text names it; for the instructions or a skill, every phase.
4. **Commit:** a plain imperative subject that says what changed, a body that says why, `Refs #<n>`. No tool
   attribution: `commit-msg` refuses it.
5. **Open a draft PR.** Write the body to `.local/pr-body.md`, from `.github/pull_request_template.md` when there is
   one, else with: what and why; the plan, or `Trivial: <why>`; how it was tested (the gate, the live suites or why
   not); the review; the one-way doors it touches, or "none"; `Closes #<n>`. Push with `git push -u origin HEAD`
   (`pre-push` runs gate quick), then `gh pr create --draft --title "<plain imperative sentence>" --body-file
   .local/pr-body.md`. The title becomes the commit subject on `main`. Say it's open and how to see it all: the PR's
   Files tab, or `git diff origin/main...HEAD`.
6. **Review** with `review-code` until it is `clean`. Commit each round's fixes with gate quick passing, and the
   record in `docs/reviews/`. Put the verdict and the record's path in the body's Review section:
   `gh pr edit <n> --body-file .local/pr-body.md`.
7. **CI,** where the repo runs it, on the head commit: `gh pr checks <n> --watch`. A red check is fixed, never
   skipped.
8. **Ask the maintainer,** as one question with a recommendation: mark it ready (`gh pr ready <n>`), merge it, or
   leave it a draft.
   - If `main` moved: `git fetch origin`, `git rebase origin/main`, `git push --force-with-lease`. A rebase that
     changes code needs the gate again.
   - Merge only on the maintainer's word: `gh pr merge <n> --squash --delete-branch --subject "<title> (#<n>)"
     --body-file .local/squash.md`, a body that says what and why and ends `Refs #<issue>` or `Closes #<issue>`. No
     HTML comments, no tool attribution.
9. **Clean up** after the merge: `git switch main` and `git pull`; a worktree goes with `git worktree remove <path>`
   from the main checkout. Work that turned up on the way becomes an issue (`gh issue create`).

## Done means

- `gate full` passed on the head commit, `review-code` is clean for exactly this code, and the PR says whether the
  live suites ran.
- The PR is ready for the maintainer, merged on their word, or left a draft by their choice.

## Never

- Open, mark ready or merge a PR with a failing gate or CI, or with a review of different code.
- Mark a `REVIEW.md` question yes without its evidence.
- Add AI co-author trailers, "Generated with" lines or session links: commits, PR titles, PR bodies.
- Push to `main`, merge without the maintainer's word, or push to someone else's branch.
- Set `OMNI_KIT_ACCEPT_EULA` for anyone: accepting NVIDIA's EULA is the person's own.

## Traps

| What broke | When | The guard |
|---|---|---|
| Live tests turned a refused token into a skip, so a run with every test skipped looked green | issue #2, plan review | `OMNIVERSE_MCP_SIM=1` makes them fail instead of skipping |
| The first capture after Kit started went past the client's timeout | PRs #3 and #8, live runs | Rerun once on a warm Kit before calling it a regression |
| Scenario failures on Isaac Sim 6.2 that `main` has too (#5, #6) | PR #3, live run | Run `main`'s suite on the same Kit and compare |
