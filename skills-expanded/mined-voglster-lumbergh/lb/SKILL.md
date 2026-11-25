---
name: lb
description: >
  Observe and coordinate the other AI coding sessions Lumbergh is supervising, using the
  `lb` CLI: list sessions and their state, read a peer's transcript, wait for a session to
  reach a state, send it a prompt, spawn a new worker in its own worktree, or supervise the
  whole fleet at once. Use when you need to check on, wait for, hand work to, or create a
  peer Lumbergh session. Do NOT use for spawning background terminals, general shell tasks,
  or when you are not running alongside other Lumbergh sessions.
---

# lb — drive Lumbergh sessions

Run `lb` (no args) for a live dashboard of every session and its state
(`working`/`idle`/`blocked`/`error`, and whether it finished unseen). The binary is the
authority on syntax — run `lb <command> --help` when unsure.

## Commands

- `lb read --session <name> [--last N] [--source transcript|pane|detection] [--full]` —
  what a session is doing. Default `transcript` (messages + tool calls); `pane` = raw
  terminal (e.g. a permission prompt); `detection` = what the state classifier sees.
- `lb state --session <name>` — current state, unseen flag, time in state.
- `lb wait --session <name> --until idle|working|blocked|error|rest [--timeout <s>]` —
  block until a session reaches a state (e.g. `--until blocked`, then step in).
- `lb wait-output --session <name> --match "<text>" [--regex <re>] [--timeout <s>]` —
  block until the terminal shows text / matches a regex; the current screen is checked
  first, so output that already appeared still matches.
- `lb prompt --session <name> "<text>" [--wait]` — send input to a peer; this drives
  another agent, so use it deliberately. `--wait` blocks until its state changes.
- `lb fleet [--wait] [--timeout <s>] [--origin bill] [--json] [--heal]` — every task under
  way: task, repo, branch, kind, state, time in state, whether it `needs` you, its `dirty`
  and `commits` counts, its OUTCOME
  column (the worker's own final `DELIVERED:`/`FAILED:` line, once written), and the repo
  and worktree paths. Take a path from a row rather than typing one — `repo_path` is what
  `lb spawn --repo` wants, `path` is what `lb worktree reap` wants.
  `dirty` counts a worker's uncommitted files and `commits` what it has committed since it
  started. An **idle worker with `dirty` above 0 is holding work that exists nowhere else**
  — it looks finished, and tearing it down destroys that work. Ask it to commit; never reap
  it. `-` is "git could not answer", which is not `0`.
  `--wait` blocks until a task needs you (`blocked`, `error`, `undelivered`, `dead`, a
  worker gone idle holding uncommitted work, or a
  report of yours that finished a chunk — the `needs` column) or
  the timeout elapses — a timeout is a normal return (exit 0), not a failure, so re-run it
  to keep waiting.
  `undelivered` is a worker that was stood up but never took its brief: no context consumed
  and an untouched HEAD. It is not idle and not working — it is doing nothing. `--heal`
  re-sends the recorded brief to every such worker, which is the whole repair.
- `lb spawn --repo <path> --branch <b> --kind ship|scout --brief <file> [--new] [--base <b>]
  [--name <n>] [--agent <provider>] [--intent "..."]` — create an isolated worktree, start a
  worker in it, and deliver the brief. Any stage failing (bad kind/brief/repo/name, the
  worktree, the session, recording it, or delivering the brief after retries) unwinds
  everything already created, so a failed spawn never leaves a half-built task behind.
  The output names the `base` it branched from (ref + sha). `--base <b>` resolves against
  the branch's upstream when the local copy is behind it — `lb land --push` leaves local
  branches stale — and prints a `base_note` whenever local and upstream disagree.

## Bill's files, when you can't reach his filesystem

The briefs you dispatch and the user's standing preferences live in Bill's home, on the
machine running the Lumbergh server. If you are occupying the Bill role from another host
you can reach the server but not that directory — use these instead of file tools:

- `lb brief write --name <slug> [--file <path>|-]` — write `briefs/<slug>.md` from a file or
  from stdin. You send a slug, never a path: the server resolves it against its own home and
  prints the resulting path, which is exactly what `lb spawn --brief` wants (spawn sends the
  path and the *server* opens it, so a path from your own filesystem would mean nothing).
- `lb brief read <slug>` / `lb brief list [--json]` — read a brief back. Do this rather than
  trust your memory of what you asked for: a babysat session is `/clear`ed every refresh
  cycle, a fresh session per wake is deliberate, and a fleet row carries only slug, kind,
  state and outcome.
- `lb report read <slug> [--json]` / `lb report list [--json]` — a scout's findings. Its
  `DELIVERED: report <slug>` line names the slug. The header answers *is there work here*
  (`actionable`), *what finishing looks like* (`done_when`), *how sure it is*
  (`confidence`), and *what it needed and could not determine* (`open_questions`) — so
  `lb report list` triages a whole directory without fetching a single body. `--json`
  returns `{frontmatter, body}`.
  **`open_questions` is what you put to the user.** A scout that has read the code knows
  precisely which detail is missing; ask that, verbatim, rather than inventing a question
  of your own.
- `lb prefs read` — the user's standing preferences. Read them before answering a worker's
  question; the answer is often already there.
- `lb prefs add "<text>" --reason "<why>"` — append one dated bullet when the user states a
  standing preference or corrects you. The server stamps the date and formats the bullet.
  Append-only by design: nothing here can rewrite or reorder the file, which is the user's.

## Worktrees

`lb worktree` manages the isolated repo copies workers run in. `lb spawn` already creates
one per task, so reach for these when adopting or cleaning up.

- `lb worktree ls --repo <path> [--json]` — every worktree of a repo, with the session (if
  any) attached to each.
- `lb worktree create --repo <path> --branch <b> [--new] [--base <b>] [--session <name>]
  [--intent "..."]` — a fresh worktree with the project's configured links applied. `--new`
  creates the branch; `--base` says off what.
- `lb worktree reap <path> [--force] [--rm-branch]` — remove a worktree once its work has
  landed. It **refuses** while the worktree has uncommitted changes (`dirty`), commits that
  are in no base branch and on no remote (`unlanded`), or no base to compare against at all
  (`unknown`); that refusal means work would be lost, so report it rather than reaching for
  `--force`. Landed-ness is patch identity against the base branch, not push state: work
  that landed by rebase or cherry-pick counts, and so does a batch the overseer landed onto
  the local base but has not pushed — which is the normal end state under `commit` delivery.
  A refusal after a green batch is therefore a real finding, not noise. On a real reap it
  also kills anything still running inside the worktree — a test server left up would
  otherwise outlive its own tree, holding a port and a database connection — and names
  every process it killed.
- `lb worktree deps <path> [--base <ref>]` — does this worktree's gate test what its code
  declares? Exits non-zero when it changed a dependency manifest while `.venv`/
  `node_modules` still points at the shared checkout, which makes lint and tests pass
  against versions the branch no longer uses.
- `lb worktree adopt <path> [--session <name>]` — start tracking a worktree that git already
  knows about but Lumbergh doesn't.
- `lb worktree link <path>` / `lb worktree unlink <path>` — re-apply or remove the project's
  configured shared files (env files, caches) in an existing worktree.

Targets `$LUMBERGH_SESSION` by default; pass `--session` for another.
