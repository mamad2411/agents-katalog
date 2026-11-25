---
name: implement
description: Build ready pieces. Typed alone, take one free or ask which. Given a piece, request or "auto", follow its route; it does not shape.
---

# Implement

Read `masterplan.md` (risk record first) and refresh the plan with
`sh .agents/tools/plan-refresh.sh`. See `records/references/pieces.md`.
Run `maintain/scripts/upgrade-check.py` from the project root and keep
only its exit code. Exit 1 means `/maintain` must finish the update; say so
and carry on.

In Codex, on `unable to get password from user`, run the installed setup
skill's `templates/foundation/codex-github-check.py` with python3 and
`--message`. Give its sentence and stop. Do not retry or sign in.

## Choose work

A ready repair comes first. Otherwise take the only free ready piece. If several are ready, show them and their blockers, then
ask which to take. Unattended, take the lowest-numbered.

A piece must be ready, have `## Done when`, and wait on no question. A piece with open parts is a container; build its parts. Send an unready piece to
`/shape` with the reason; it does not settle the question. A plain
request must match a ready piece or goes to `/shape`. For a live break, follow
`live-copy`'s rollback route.

Skip questions, missing `Done when`, `## Waiting on you`, unmet dependencies,
another person's assignment or a recorded block. Say why; take the next
eligible piece. Closed blockers make `blocked` stale; say so. Mutual blockers
go to `/shape`.

For several ready pieces, show **Ready now** and **Waiting**, counts and dependencies. Omit questions; an unmarked piece needs
`/shape`. Showing a list builds nothing. A green pull request waits for merge;
follow `merge` only when asked. Ask which merge when told only "put it live".

## Build and save

Build one piece per pass with `build-piece`, through updated records. After
green checks and records in the pull request, use `merge`. By default, approval
naming the merge is required. Unattended, leave it ready for review unless the
automatic merge option is on.

`auto` needs approval and `references/running-longer.md`. An unattended run merges only through `--auto` when the setting is on, never otherwise. Each piece must be
self-sufficient enough to build without a person present. Load the reference
first. In an unattended run nobody is there to say yes, so never merge except
through `--auto` when its recorded option and every hold allow it, and never
accept a risk for the person.

## Done when

Evidence, review, records and save route are complete, with any available
machine check run and green; or report a safe block, its caution and other
work. Never call blocked work ready or live.
