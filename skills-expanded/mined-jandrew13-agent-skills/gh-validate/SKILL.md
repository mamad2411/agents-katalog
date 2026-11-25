---
name: gh-validate
description: Behaviorally validate exactly one GitHub pull request before merge — pull its branch into an isolated worktree, run the ticket's acceptance criteria as literal behavior through the real entry point (not by reading the diff), post a pass/fail verdict comment, and set the board Status. Use when a PR in the dev-workflow pipeline is at status Awaiting Validation (review findings clean/addressed, CI green — Codex not required) and needs its pre-merge validation stage. Verifies the feature works through the real path — never strategy profitability. Never fixes, never merges.
---

# GH Validate

**Session shape:** spawned subagent, one per PR; pulls the PR branch into its own
isolated worktree — never the operator's main worktree.
**Conventions scope:** read only §§3, 4, 5, 8, 9 of
the pipeline CONVENTIONS.md — resolve it at `gh-workflow/CONVENTIONS.md`
alongside this installed skill set, else `agents/gh-workflow/CONVENTIONS.md` in
the skill source repo (github.com/JAndrew13/agent-skills); it is NOT in the
target repo. `grep -n "^## "` it for section offsets and read just those
ranges; open any other section only at the moment a step cites it.

## Overview

Validate **exactly one PR** per invocation, as the pipeline's standalone
pre-merge behavioral-proof stage:
`(Awaiting Validation) → gh-validate → (In Validation) → (Validated) | (Reviewed)`.

Review (`gh-review`) reads diffs; CI runs tests. Neither behaviorally exercises
the feature. This skill closes that gap: it checks the PR branch out into its
own isolated worktree and **runs** the ticket's acceptance criteria as literal
behavior — driving the real CLI/MCP/preview surface the change reaches, the
same evidentiary discipline as the `verify` skill (runtime observation over
diff-reading, no import-and-call, capture what the app itself produced).

**Content sources (extraction, not new logic):** the dev-workflow brainstorm's
Validator description (FABLE_09 §3 gh-validate row) and the `verify` skill's
patterns (surface identification, drive-it, push-on-it, capture, verdict
format) — adapted here to a fixed pipeline contract (worktree, PYTHONPATH,
verdict-comment format, board Status) rather than `verify`'s free-form report.

**Taxonomy, statuses, the state machine, the review gate, and the
version/cadence policy are owned by
[`agents/gh-workflow/CONVENTIONS.md`](../../agents/gh-workflow/CONVENTIONS.md).** This
skill **references** those sections and **never restates** their tables.

## Scope (single-purpose)

- Input: one PR (number or URL) whose board Status is `Awaiting Validation`
  (CI green, review findings clean/addressed — Codex not required, CONVENTIONS.md §4).
- If asked to validate several PRs, run this skill once per PR — do not batch.
- Read the linked **issue** end to end: its acceptance criteria, its
  `## Refinement` block, and its Validation section (if it has one) before
  touching a worktree. Validation measures the change against *that ticket's*
  acceptance criteria — nothing more, nothing less.

## Scope honesty (non-negotiable)

**gh-validate verifies that the feature works through the real path — it is
never a strategy-profitability or live-promotion signal.** Board Status
`Validated` means "the code change does what the ticket says, observed at
runtime." It does not mean a strategy is profitable, a backtest beat a
baseline, or the change is ready for live capital (memory:
`verify-feature-not-perfect-strategy`). If a ticket's acceptance criteria are
themselves about strategy P/L, validate that the *mechanism* fires as
specified (e.g. a gate blocks/allows the cases it's supposed to) — do not turn
this into a profitability-maximizing exercise.

## Non-negotiables (read first — the two memorialized traps)

These are encoded here **verbatim** because they have each already corrupted a
validation pass once, silently:

1. **Worktree PYTHONPATH trap.** The PR branch is tested in an **isolated
   worktree**, and the skill MUST **set `PYTHONPATH=<worktree>\src`** — worker
   and reviewer worktrees share main's `.venv`, whose editable install points
   at **main's** `src`, so without this the tests silently run against main's
   code, not the PR's (memory: `worktree-venv-pythonpath-trap`; bit PR #441
   twice). Set it before any Python invocation in this validation.
2. **Preview-server stop.** If validation starts a preview/dashboard server,
   the skill MUST **stop it when done** (`ks server stop` / `ks_server_stop`)
   — never leave a server running (memory: `close-preview-process`).

Also carried from the sibling skills' operating discipline:

- **Never `gh pr checkout` / `git switch` in the operator's main worktree**
  (memory: `worktree-review-isolation`) — always work inside the dedicated
  validation worktree created below.
- **venv version fragility.** A fresh worktree's ambient `python` can resolve
  to system Python (observed: 3.14) rather than the project's 3.11 venv, and a
  system Python lacks `pytest`/project deps entirely. Use the project's `.venv`
  interpreter (`<main-repo>\.venv\Scripts\python.exe`, or `py -3.11`) inside
  the validation worktree, not whatever `python`/`python3` resolves to on
  `PATH` (memory: `venv-version-fragility`).

## Where this sits in the pipeline

Per the state machine (CONVENTIONS.md §4), validation is the gate between
review and merge:

```
(Awaiting Validation) --CI green--> --gh-validate: PR branch in isolated worktree,
      behavioral test (UI via preview tools when relevant)--> (In Validation) -->
      pass --> (Validated)               fail --> (Reviewed) + PR comments
```

You own the transition **into** `In Validation` and **out of** it
(CONVENTIONS.md §5 ownership table): pass sets `Validated`; fail kicks back to
`Reviewed` — **never** silently to `Open` or `Awaiting Review`, so the PR and
its review history stay attached (CONVENTIONS.md §4 kick-backs rule).

## Workflow

### 1. Confirm scope and preconditions

- Identify the repository (the profile's `<repo>`), the single PR, and its
  linked issue. Confirm the PR's board Status is `Awaiting Validation`; if it
  is earlier in the pipeline (still `Awaiting Review` / `Reviewed`), stop —
  it isn't yours yet.
- Confirm CI is green on the PR (`gh pr checks <n>`). CI is a *precondition*
  here, not something you re-run wholesale — CONVENTIONS.md §9 gives targeted
  runs to development/review; this skill adds the one thing neither reads nor
  CI provide: **runtime behavior**.
- Read the issue's acceptance criteria and Validation section verbatim. These
  are the literal checklist you will prove true or false — not a paraphrase.
- Resolve the PR's board item id up front so the step-6 status transition is one
  command, following the **board-economy contract** (CONVENTIONS.md §3): **use the
  board item-id the dispatcher injected** — a lead/sweeper that already resolved the
  board map passes it down — and do **not** call `item-list`. **Only if no item-id
  was injected** (a standalone/human invocation) fall back to resolving it yourself
  by matching `items[].content.number == <issue#>` from `gh project item-list
  <board-number> --owner <board-owner> --limit 300 --format json` (ids from
  PROFILE.md; mechanics in CONVENTIONS.md §3).

### 2. Create the isolated validation worktree

Never validate in the operator's main worktree or any other session's
worktree. Create your own, off the PR's head:

```sh
git -C <operator-main-repo> fetch origin
git -C <operator-main-repo> worktree add --detach <validate-worktree> origin/main
cd <validate-worktree>
gh pr checkout <pr-number>          # now on the PR's actual head commit
```

Then, **before any Python invocation**, apply the two non-negotiables:

```sh
export PYTHONPATH=<validate-worktree>/src      # trap #1 — see Non-negotiables
cp <operator-main-repo>/.env <validate-worktree>/.env   # gitignored; needed for Settings()
```

Use the project's `.venv` interpreter explicitly rather than ambient `python`
(the venv-fragility note above):

```sh
<operator-main-repo>/.venv/Scripts/python.exe -m pytest --version
# or: py -3.11 -m pytest --version
```

### 3. Identify the real surface per acceptance criterion

For each acceptance criterion, find the surface it reaches — the same
surface/handle framing as the `verify` skill:

| Change reaches | Surface | You |
|---|---|---|
| CLI (`ks ...`) | terminal | run the command, capture stdout/exit code |
| MCP tool | the tool call | invoke it, capture the structured response |
| Server / API endpoint | socket | request it, capture the response body |
| Dashboard / web UI | pixels | **rebuild + launch the preview**, drive it, screenshot (step 4) |
| Library / internal function | its caller's surface above | follow the call site to where a CLI/MCP/UI actually invokes it — an internal function alone is not a surface |

**Read-only where possible; write only what the ticket claims.** If an
acceptance criterion is about a destructive/live path (an order, a send, a
delete) with no dry-run or preview equivalent, do not drive it live — validate
what you safely can and say explicitly which path was not exercised and why
(mirrors `verify`'s destructive-path rule; also never
`ks server --live` / `ks_server_live` / any live buy/sell/order tool from this
skill — preview/backtest surfaces only).

**Tests in the diff are the author's evidence, not your surface.** CI already
ran them. Reading a test to learn what to check is fine (it's a spec) — but
then go run the app. A diff with no runtime surface at all (docs-only,
type-only, tests-only) has nothing for this skill to add: say so and defer
to CI + gh-review's judgment rather than inventing a run.

### 4. Dashboard / UI work — rebuild before you judge

**`dist` is gitignored, so a `git pull`/checkout of the PR branch alone never
updates the running dashboard** (memory: `dashboard-rebuild-after-pull`) —
without the rebuild you are looking at the *previous* build, not the PR's.
For any PR touching `dashboard/client` or `src/dashboard/server`:

1. **Rebuild the client** inside the validation worktree:
   `cd <validate-worktree>/dashboard/client && npm run build` (run `npm ci`
   first only if `package.json`/`package-lock.json` changed in this PR).
2. **Start the dashboard rooted at the validation worktree** so both the rebuilt
   `dist` and any server-side Python change are the PR's, not main's. Run the
   **CLI from the worktree** with `PYTHONPATH=<validate-worktree>/src` (project
   venv), holding the pid: `ks dashboard --host 127.0.0.1 --port <port>
   --no-browser`. **Do not** use `ks_dashboard_start` on the default (main-rooted)
   MCP server — it would serve the operator's main checkout, not the PR (see the
   P1 ⚠️ in Tool guidance). Stop any prior worktree instance you started by pid
   first.
3. **Hard-refresh** the browser/preview view (Ctrl+Shift+R) — a cached
   `index.html` can still point at the previous build's hashed assets.
4. **Confirm the served build is the new one** before judging anything:
   `curl -s http://127.0.0.1:7311/ | grep -o 'assets/index-[^"]*\.js'` should
   show a hash that matches this rebuild, or a new endpoint the PR added
   should return 200, not 404.
5. Drive the feature through the actual preview UI (click, fill, navigate —
   the preview tools), not by curling the API underneath, unless the ticket's
   acceptance criterion is itself about the API.
6. **Stop the server when this step is done** — see step 6's cleanup; do not
   wait until the very end if you started it only for this sub-check.

### 5. Drive each criterion, then push on it

For each acceptance criterion: **drive** the smallest real path that makes the
changed behavior execute, capture the app's own output as evidence, then
**push on it** the way `verify` does — probe one adjacent case per criterion
(a boundary value, a conflicting flag, a repeat-with-stale-state, a malformed
input) to make sure the pass is not a happy-path coincidence. This is not a
second full test sweep; it is one adversarial nudge per criterion, at the same
surface you just drove.

- **Capture real evidence**: command + stdout/exit code, MCP tool response
  JSON, screenshot + accessibility snapshot for UI, or the response body for
  an API — not your paraphrase of what you expect it to show.
- **Ambiguous output is a fail, not an interpretation call.** When in doubt,
  fail with the raw capture attached rather than reading a favorable
  interpretation into it.
- Note anything else you saw that a reviewer would want to know — friction,
  a surprising default, an error message that didn't name the bad input —
  even if it isn't itself a failing criterion. These ride in the verdict
  comment's findings, not as a separate channel.

### 6. Post the verdict comment

**Post on the PR — never chat-only** (same rule as `gh-review`: the submitter
and the next actor must see it there). Format, one line per criterion plus a
findings section:

```markdown
## Validation verdict: PASS | FAIL

**Scope:** validated PR #<n> against issue #<m>'s acceptance criteria, in an
isolated worktree at `<validate-worktree>` (PR head `<sha>`).

### Per-criterion results

1. ✅/❌ <acceptance criterion, verbatim or lightly trimmed>
   - Command/observation: `<exact command or tool call>`
   - Evidence: <the app's own output — trimmed stdout, response snippet,
     screenshot reference>
2. ✅/❌ <next criterion>
   ...

### Findings
<Anything noticed while driving the app that the ticket didn't ask about —
friction, a surprising default, an unhelpful error, a probe that held. Empty
is fine if nothing stuck out.>

### Verdict rationale
<One paragraph: why PASS or FAIL follows from the per-criterion table above.
Any criterion marked ❌ makes the overall verdict FAIL — no partial pass.>
```

No partial pass: **one failing criterion fails the whole verdict** — same
standard as `verify` ("3 of 4 passed" is FAIL until 4 pass or the gap is
explained away and re-scoped with the operator, not silently waived here).

Then set the board Status via `gh project item-edit` (never a label —
mechanics and IDs in CONVENTIONS.md §3; ownership in §5):

- **All criteria pass → `Validated`.** `gh-merge` picks it up next.
- **Any criterion fails → `Reviewed`**, with the verdict comment already
  posted explaining the failure. This is the fixer loop
  (`gh-fixer` → `gh-review` → back here) — **never** kick back to `Open`; the
  PR and its history stay attached (CONVENTIONS.md §4).

Set Status to `In Validation` at the **start** of step 2 (before you begin
driving anything), not retroactively at the end — it marks the PR as claimed
for validation for the duration of this run.

### 7. Clean up — always, pass or fail

- **Stop every server this run started** (the trap #2 non-negotiable), for
  anything launched in steps 3–4. The stop tools **require explicit
  confirmation** — `ks_server_stop` / `ks_dashboard_stop` default
  `confirm_stop=false` and **raise** unless you pass `confirm_stop=true`, so a
  bare call FAILS and leaves the server running (violating this non-negotiable).
  Use the confirmed form, and target the pid you started:
  - `ks_dashboard_stop(confirm_stop=true, pid=<pid>)` /
    `ks_server_stop(confirm_stop=true, pids=[<pid>])` — these reap by process
    role/pid via `taskkill /T /F`, so they stop a worktree-launched server
    regardless of the MCP server's own root (they match on the process, not cwd).
  - There is **no** `ks dashboard stop` / `ks server stop` CLI subcommand — a
    CLI server you launched foreground is stopped with Ctrl-C; a backgrounded one
    is stopped by its pid (the confirmed MCP stop above, or `taskkill /PID <pid>
    /T /F`).

  Confirm via `ks_project_processes` that nothing tagged `server`/`dashboard`
  from this run remains before ending the turn — do not end "assuming it shut
  down."
- **Remove the validation worktree**:
  `git -C <operator-main-repo> worktree remove <validate-worktree>` (add
  `--force` only if it refuses due to an untracked file you intentionally
  left, e.g. a copied `.env` — never force-remove over uncommitted work you
  don't recognize). Confirm with `git -C <operator-main-repo> worktree list`
  that it is gone.
- Run the profile's `<artifacts-gate>` from the main repo if this run
  wrote anything under `tmp/`/`.tmp-*`/`evidence-outputs/` during validation,
  to confirm nothing tracked leaked out.

## Boundaries

- **Behavioral, advisory-on-failure only.** Never edit code, never push
  commits, never resolve review threads. A failing criterion goes back via the
  verdict comment for the fixer loop (`gh-fixer`), same handoff shape as
  `gh-review`'s findings.
- **Never merges.** Only `gh-merge` merges (CONVENTIONS.md §5, §8).
- **One PR per invocation.** Re-invoke for the next PR.
- **Verifies the feature, not the strategy.** Per Scope honesty above — resist
  any pull toward judging profitability, backtest superiority, or live
  readiness; those are separate, later decisions outside this pipeline stage.
- **Isolation.** All git ops run in the dedicated validation worktree from
  step 2; nothing touches the operator's main worktree or another session's
  worktree (memory: `worktree-review-isolation`).
- **Leave nothing running or lying around.** Step 7 is not optional cleanup —
  it is part of the acceptance bar for this skill's own use (see
  Worked example below).

## Tool guidance

- Use `gh pr checkout <n>` **only inside the dedicated validation worktree**
  created in step 2 — never in the operator's main worktree or a shared
  session tree.
- **⚠️ The project's default MCP server (`<project-mcp-server>`, PROFILE.md) is
  MAIN-ROOTED — never use it to
  validate a PR worktree.** This is the P1 trap and the twin of the PYTHONPATH
  trap above: the running MCP server resolves its project root from **its own**
  process (its project-root env override, else it walks up from the MCP process's
  cwd to the first `<version-file>`), and every server/dashboard it
  launches is a **subprocess of the MCP process**. Those subprocesses inherit
  the **MCP process's** cwd/env — **not** your shell's `cd <validate-worktree>`
  and **not** your exported `PYTHONPATH`. So calling the MCP server-launch tools
  (dashboard/preview starters) on the default MCP server starts and inspects the
  **operator's MAIN checkout**, recreating the exact false-validation trap this
  skill exists to prevent — you'd render a green verdict against code that isn't
  the PR's. Therefore, to exercise a server/dashboard/preview surface, do **one**
  of these two, never the main-rooted MCP tools:
  - **(Preferred) Run the CLI from inside the validation worktree** with
    `PYTHONPATH=<validate-worktree>/src` set, using the project venv interpreter
    (Non-negotiables): e.g. `ks server --preview --config <toml> --once`, or
    `ks dashboard --host 127.0.0.1 --port <port> --no-browser` — a process
    **you** own, whose cwd/PYTHONPATH are the worktree's. (Foreground, or launch
    it as a background process you hold the pid for — the CLI has no `stop`
    subcommand; you stop it by pid, step 7.)
  - **OR (re)start the MCP server rooted at the validation worktree first** —
    launch it with its project-root env override set to `<validate-worktree>`
    (PROFILE.md validation notes name the variable; here `KS_PROJECT_ROOT`) and
    worktree `src` on `PYTHONPATH` **before any MCP call**, and confirm it is
    worktree-rooted; only then are its server/dashboard launch tools operating
    on the PR's code. Do not point MCP tools at a PR worktree without this.
  Read-only, root-agnostic MCP tools that only *inspect* by process role or hit
  a URL you started (`ks_project_processes`, `ks_strategy_validate` against an
  explicit worktree path, a plain `curl` to the port you launched) are fine
  either way — the trap is specifically the tools that **launch** a server in the
  MCP process's root.
- Use `gh project item-edit` for the board Status write; call `gh project item-list`
  **only** as the no-injected-id fallback (the §3 board-economy contract), never to
  re-fetch the full board map when the dispatcher already supplied the item-id
  (commands and IDs: CONVENTIONS.md §3).
- Run only the **targeted** tests/scripts the acceptance criteria point at —
  never a full-suite `pytest -q` here (that is `gh-merge`'s job at the
  merge-to-`main` boundary, CONVENTIONS.md §9); this skill's value is runtime
  observation CI doesn't give you, not re-running CI.

## Worked example — validating a passing and a failing fixture (illustrative)

**Purpose:** show the full loop end to end, including the kick-back path, on
a small illustrative fixture — a `[TASK] CONFIG` PR that adds a volatility
entry gate CLI flag. (The commands below use THIS project's PROFILE.md instance
values — CLI module, venv path, strategy fixture; substitute your profile's.)

**Fixture A (passing):** PR #950 for issue #849, AC: "`ks backtest --config
<toml> --vol-floor 4` rejects entries below the floor; without the flag,
behavior is unchanged."

```sh
git -C <main-repo> fetch origin
git -C <main-repo> worktree add --detach <validate-worktree-950> origin/main
cd <validate-worktree-950> && gh pr checkout 950
export PYTHONPATH=<validate-worktree-950>/src
cp <main-repo>/.env <validate-worktree-950>/.env

# Step 5 — drive it:
<main-repo>/.venv/Scripts/python.exe -m kalshi_socket.cli backtest \
  --config strategies/testing/simple.toml --vol-floor 4 --no-rerun-prompt
#   -> report shows 0 entries below the floor (evidence: report JSON summary)
# push on it: run again WITHOUT --vol-floor -> confirm entries below floor
#   now DO occur (regression check: unflagged behavior unchanged)
```

Verdict comment: both criteria ✅ → board Status `Validated`. Cleanup: nothing
to stop here (backtest is a one-shot CLI run, no server started), remove
`<validate-worktree-950>`, confirm `git worktree list` clean.

**Fixture B (failing):** PR #951 for issue #850, AC: "the dashboard's new
`/positions` panel shows live position P/L; refreshing the page keeps the
panel visible."

```sh
git -C <main-repo> worktree add --detach <validate-worktree-951> origin/main
cd <validate-worktree-951> && gh pr checkout 951
export PYTHONPATH=<validate-worktree-951>/src
cd dashboard/client && npm run build          # step 4 — dist is gitignored
# start the dashboard via the CLI FROM THE WORKTREE (NOT ks_dashboard_start on
# the main-rooted MCP server — see the P1 warning); hold the pid to stop it:
<main-repo>/.venv/Scripts/python.exe -m kalshi_socket.cli \
  dashboard --host 127.0.0.1 --port 7311 --no-browser &   # $! = the pid
# hard-refresh, confirm the served build hash is this rebuild, drive /positions
```

Observed: the panel renders on first load but **disappears on refresh**
(evidence: accessibility snapshot before/after F5 shows the panel present,
then absent). One criterion ❌.

Verdict comment posted on #951: criterion 1 ✅ (panel shows live P/L),
criterion 2 ❌ (does not survive refresh — capture attached) → **FAIL**. Board
Status → `Reviewed` (never `Open`) with the comment explaining exactly what
broke and the repro. Cleanup regardless of the fail: stop the dashboard by pid
— `ks_dashboard_stop(confirm_stop=true, pid=<pid>)` (the confirmed form; a bare
call raises), confirm via `ks_project_processes` no dashboard process remains,
remove `<validate-worktree-951>`, confirm `git worktree list` clean.

**Post-run check (both fixtures):** `git worktree list` shows neither
`<validate-worktree-950>` nor `<validate-worktree-951>`; `ks_project_processes`
shows no server/dashboard process attributable to this run.
