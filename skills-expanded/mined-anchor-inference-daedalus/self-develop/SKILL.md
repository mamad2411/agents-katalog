---
name: self-develop
description: How to change your own code (host or core) safely: worktree, tests, then a pull request or an apply-and-restart.
requires: self_development
---
# Self-development workflow

This installation runs in one of three modes (`[self_change] mode`, shown by `GET /api/capabilities`
and by the doctor). The tools you actually have say which one you are in:

- **server** — all four `Self*` tools: the full workflow below, ending in a pull request.
- **local** — `SelfWorkspace` and `SelfApply`: there is no fork, no remote and no pull request here. Work
  through steps 1-4, then call `SelfApply` instead of `SelfPropose` (step 5L). Never push.
- **off** — no `Self*` tool exists. This installation does not change its own code; do not look for
  a way around that.

1. `SelfWorkspace(repo, branch)` — get a worktree on `agent/<branch>`, from `origin/main` in server mode
   and from the branch the checkout has open in local mode (there is no remote to branch from there).
   `repo` is `bot` (host: tools, providers, transport, Mini App, skills) or `core` (agent loop).
2. Edit inside the worktree only. Layout of the host repository:
   - `daedalus/tools/<name>.py` — one tool per module, exported in `TOOLS`; use `@tool` from the core.
   - `daedalus/providers/` — OpenAI-compatible adapter; a new endpoint is usually just config.
   - `daedalus/transport/telegram/` — chat surface. `daedalus/extensions/` — scheduler, self-dev, API.
   - `skills/<id>/SKILL.md` — skills (front matter: name, description).
   - `tests/unit`, `tests/smoke` — smoke tests are the supervisor's preflight gate; keep them fast.
3. Run the gates in the worktree **through Verify**, so the receipts land on the proposal card:
   `Verify("unit suite passes", "uv sync --extra dev && uv run pytest -q", cwd=<worktree>)` (host) or
   `uv run pytest -q` (core, ~3k tests; run the subset you touched first, then the whole suite).
   A proposal whose card says "nothing was checked with Verify" is asking the operator to trust prose.
   Before proposing, walk this checklist and say in the summary what you found:
   - every reader of a field or threshold you changed (`grep` the name across the repo) agrees with
     the new rule — a check added in one place and an older check elsewhere must not disagree;
   - the new path behaves when the object is missing, not linked, expired, or restarted mid-way;
   - a fast path you add does not repeat work already done by the slow path it precedes;
   - the full suite and `ruff check` pass, not only the tests you wrote.
4. Commit with a message that describes the change on its own terms. In server mode the repositories are
   public:
   no session or run ids, no board-thread, review-round or defect-catalogue references (SelfPropose
   refuses a branch whose commits carry them), no model or tool names as authors — your own
   `Co-authored-by: Daedalus <daedalus@localhost>` trailer is fine — and
   nothing about the operator (addresses, hostnames, paths, accounts, workloads, circumstances) in
   commits, pull requests, code comments or docs. What you know about the operator stays in the session.
5. `SelfPropose(repo, title, summary)` — opens the pull request and a decision card for the operator.
   Server mode only.
5L. `SelfApply(repo, summary, execution_path)` — local mode. It runs the same gates as a proposal (the
   Verify receipts, the execution path, the size rule), fast-forwards your commits onto the checkout's own
   branch, and puts "Changes are ready — restart to apply" in front of the operator with your summary on
   it. Write that summary as one sentence they can act on. What happens next is not yours to do: the
   restart preflights your commit on a copy of itself and keeps the running version if it fails, and a
   change that boots three times and dies is put back automatically. Your worktree and branch stay where
   they are, so a refused change is still there to fix. If you changed `deploy/Dockerfile` or the system
   packages, say so — a restart cannot deliver those and the operator has to build a new image.
6. After the merge, `SelfRebuild(reason)`. The supervisor pulls main, runs preflight and restarts;
   a failing preflight rolls back automatically and reports why. A rebuild asked for while one runs
   is queued and starts right after it — no need to ask again.

In local mode nothing is published, so your commit messages are your own — but what describes the operator
still has no place in code or comments, because a local checkout can become a pull request later.

What describes the machine is private and the proposal gate refuses it: the LAN address your
services are reached at (ServiceList shows it), hostnames, the operator's paths and accounts.
Write "the host's address" in a test or a comment, never the value.

Rules: never edit the running checkout, never push to main, keep changes small and tested.
