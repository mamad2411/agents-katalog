# AGENTS.md — Rotaris

Scoped instructions — each owns its area and is not duplicated here:

| File | Owns |
| --- | --- |
| [apps/rotaris/AGENTS.md](apps/rotaris/AGENTS.md) | Rotaris desktop UX, accessibility, and Qt test standards |
| [.github/copilot-instructions.md](.github/copilot-instructions.md) | Copilot entry point (pointer + ReqToCode kernel) |

Canonical policy docs: [requirements/README.md](docs/requirements/README.md)
(requirement store format), [reqtocode-playbook.md](docs/reference/reqtocode-playbook.md)
(ReqToCode runbook), [terminology-glossary.md](docs/terminology-glossary.md).
For architecture detail start at [docs/architecture.md](docs/architecture.md),
especially [02-code-topology.md](docs/architecture/02-code-topology.md) and
[14-e2e-trace.md](docs/architecture/14-e2e-trace.md).

## Naming

The product is **Rotaris**.
Three surfaces share the name, and each has exactly one spelling:

| Surface | Distribution | Import package | Entry point |
| --- | --- | --- | --- |
| Rotaris desktop (primary UI) | `rotaris` | `rotaris` (`apps/rotaris/src/`) | `rotaris` |
| Rotaris engine (backend) | `rotaris-core` | `rotaris_core` (`src/`) | `rotaris-cli`, `rotaris-headless` |
| Rotaris TUI (secondary UI) | part of `rotaris-core` | `rotaris_core.tui` | `rotaris-cli run` |

State and identifiers follow from that: `<workspace>/.rotaris/`,
`~/.config/rotaris/`, `~/.local/share/rotaris/`, session worktree branches
`rotaris/session/<id>`, prompt placeholders `[[ROTARIS:TOKEN]]`, and classes
prefixed `Rotaris…` (`RotarisConfig`, `RotarisTuiApp`, `RotarisDelegateTool`).

## Architecture map

The code lives under `src/rotaris_core/`. The **Rotaris** desktop app (`apps/rotaris/`, PySide6) is the **primary** user interface; the Textual TUI is **secondary** — keep it working, but Rotaris takes priority (see `apps/rotaris/AGENTS.md`).

- `cli/`: CLI entry points, including interactive startup and `cli/background.py`
- `tui/`: Textual UI (secondary interface); `tui/app.py` is the stable `RotarisTuiApp` facade
- `ralph/`, `orchestrator/`, `improvement/`: run loop, scheduling, child lifecycle, delegation, improvement flow
- `agents/`: persona construction, prompts, tool wiring, agent-facing helpers
- `tools/`: concrete tool implementations exposed to agents
- `config/`: layered config loading, validation, MCP discovery/resolution
- `session/`: session snapshots, persistence, locking
- `haet/`: hash-anchored edit engine
- `auth/`, `providers/`, `models/`: auth, provider integration, model selection
- `core/`, `tracking/`, `mcp/`: shared runtime support, tracking, MCP shims
- `api/`: prompt/API-facing helpers

Runtime shape:

```text
Interactive CLI -> RotarisTuiApp -> MainScreen -> TuiRunController -> TuiRalphLoop
Background CLI  -> cli/background.py -> SessionManager + RalphLoop

RalphLoop -> Scheduler -> ChildManager -> asyncio.to_thread(LocalConversation.run)
```

## Rules that matter

### Runtime and orchestration

- `LocalConversation.run()` is synchronous OpenHands SDK code. Run it via `asyncio.to_thread`.
- Call `record.transition(new_state)`. Do not assign `record.state` directly.
- Pause conversations via `pause_with_daemon()` (`orchestrator/scheduler_conversation.py`), never `conversation.pause()` inline — a sync call from inside the conversation's own run-loop risks it waiting on itself.
- Never re-override `RalphLoop._run_iteration`; add a `RalphIterationObserver` hook instead.

### Imports and boundaries

- Use lazy imports in widely imported modules.
- Keep heavy imports inside functions or behind `TYPE_CHECKING`.
- Do not use `from rotaris_core import X` at module scope inside submodules.
- Keep `scheduler`, `child_manager`, and `delegate_tool` cross-imports local to functions.
- Keep `tui/app.py` thin; put behavior in helper modules unless the facade contract changes.

### Agents and tools

- `agents/factory.py` is the source of truth for persona construction and friendly tool names.
- `TOOL_NAME_MAP` in `agents/factory.py` is authoritative.
- `create_agent_for_persona()` returns a factory, not an instantiated agent.
- Personas exposing `"delegate"` use closure-based factories over `runtime_kwargs`; do not try to serialize that wiring.
- MCP servers belong under `mcp_servers:` in `agents.yaml`, not under `tools:`.
- Unavailable MCP servers are filtered at runtime and surfaced in the TUI.

Adding a tool: create `tools/my_tool.py` with `MyTool(ToolDefinition)` +
`MyToolExecutor`, map the friendly name to the SDK class name in
`agents/factory.py::TOOL_NAME_MAP`, re-export from `tools/__init__.py`, then
reference it by friendly name in the persona config `tools:` list.

### Config and persistence

- Config precedence is `~/.config/rotaris/` < `<workspace>/.rotaris/`.
- Config merges are field-wise overlays; list and dict fields replace rather than deep-merge.
- Keep `api_key` values as `SecretStr` and out of normal dumps.
- New `SessionState` fields need defaults for backward compatibility.
- Bump `SESSION_SCHEMA_VERSION` only for breaking snapshot changes.
- Sessions live under `<workspace>/.rotaris/sessions/<session_id>/` and writes must stay atomic.

### User-facing behavior and docs

- Surface user-visible errors with `self.notify(...)` at the correct severity.
- Bump `pyproject.toml` after every bug fix or feature addition.
- New or materially changed tests and product requirements follow the
  [Product-Centred Test Strategy](docs/testing/test_strategy.md): state productive
  use, model the unit/integration/E2E portfolio, and preserve a hermetic public-boundary
  user flow for every product SWR.

## Workflow — worktree, merge

**Every feature runs in its own worktree, on its own branch off `master` —
small, medium, or large.** A feature is anything that carries a requirement id
or changes behavior beyond a one-liner. Quick fixes may land directly on
`master` in the main checkout: a typo, a one-line fix, a doc tweak, a lint nit,
repairing the checkout, resolving a merge, editing this workflow.

The size of the change decides whether it gets a workspace, not the ceremony
around it. When in doubt — worktree. Sessions here run in parallel, so a branch
switch in the shared checkout is never private.

**The order is: implement → fast gate → merge.** An agent merges its own
finished work into `master` without asking anyone, resolving conflicts so that
both sides keep working.

### 1. Pick the workspace

**Worktree (default).** One worktree per feature, carrying that feature's
branch. The main checkout is shared — a live Rotaris session's agents write
uncommitted changes into it, parallel agents collide in one tree, and a
`checkout` in one session yanks the files out from under another. A worktree
gives the feature its own tree and its own branch while the main checkout stays
on whatever branch it already had.

Where the worktree comes from depends on which harness you are. Each harness
owns exactly one area, and none of them may write into another's:

| You are | Your worktree |
| --- | --- |
| an agent inside a Rotaris session | You are **already** in one: `.rotaris/worktrees/<session-id>`, branch `rotaris/session/<session-id>`, cut from the base checkout's current branch by `GitWorktreeService` (`rotaris … --isolate`). Work there. Do not create another, and do not `git checkout` — the harness owns this tree. |
| Claude Code | `.claude/worktrees/<name>` — mechanics in [CLAUDE.md](CLAUDE.md#worktrees-in-claude-code-sessions). |
| any other agent, or a background job that cannot change directory | `rtk git worktree add .tmp_wt/<name> -b <type>/<swr-id>-<slug> origin/<base>` |

**Ask which branch is your base — never assume `master`.** A requirement that
belongs to a [milestone](docs/milestones/README.md) branches from, and merges
back into, that milestone's branch. The answer is a command, not a document you
have to have read:

```bash
uv run python devtools/milestone.py branch-for SWR-<n>    # -> milestone/m1-… or master
```

`master` is the normal answer and means today's behaviour, unchanged: a bug fix
or a requirement in no milestone goes straight to `master`. Anything else is
`<base>` in the table above and in § 4 below.

Branches are `feat/…`, `fix/…`, or `chore/…` plus the requirement id when there
is one. Keep every worktree **inside** the repo — `.rotaris/worktrees/`,
`.claude/worktrees/` and `.tmp_wt/` are all gitignored, and untracked local
config is still found by walking up from there.

**`master` is checked out in the main repo root and nowhere else.** Never
`git worktree add … master`, never `git checkout master` inside a worktree, and
never cut a worktree whose branch *is* `master`. Every worktree carries a
`feat/…`, `fix/…`, `chore/…`, epic, or session branch. One tree owning `master`
is what keeps parallel runs from colliding: git only refuses a second checkout
of `master` while the first is on it, so the moment the main checkout sits on a
feature branch, a second tree can grab `master` and two sessions then merge into
two different working copies of the same branch. If you find `master` checked
out somewhere other than the repo root, that is a defect — move that tree off it
(`git checkout -b …` or remove the worktree) before doing anything else.

The same reasoning applies one level down: **a milestone or epic integration
branch is checked out in exactly one worktree.** Two trees on the same
integration branch is the same collision as two trees on `master` — each merge
lands in a different working copy of one branch.

Then give the worktree its own environment, once:

```bash
uv sync --all-packages       # ~25 s, ~1.2 GB, wheels come from the uv cache
```

That is what makes worktrees safe here: after it, `uv run` resolves
`rotaris_core` and `rotaris` to *this* worktree's `src`, not the main
checkout's.

**Branch in the main checkout (exception).** For a human-driven or Claude Code
session only — an agent inside a Rotaris session never takes it, since the
harness already gave it a tree. And only when nothing else is running in the
checkout and the work needs untracked state that lives only there — `.rotaris/`
(`agents.yaml`, `secrets.yaml`, sessions), a populated `.serena/`, a Rotaris run
driven from the workspace root:

```bash
rtk git checkout master            # in the main repo root — the only tree that
                                   # may sit on master (see the rule above)
rtk git checkout -b <type>/<swr-id>-<slug>
```

Check `rtk git worktree list` and `rtk git status` first; if a session owns the
checkout, take a worktree instead. To run Rotaris itself from a worktree, copy
the workspace config over rather than switching back:

```bash
mkdir -p .rotaris && cp "$(rtk proxy git rev-parse --path-format=absolute \
  --git-common-dir)/../.rotaris/agents.yaml" .rotaris/
```

### 2. Implement completely, on the branch

1. Implement the requirement **completely**: production code and
   `@traces`/`@verifies` annotations.
2. Stage explicit paths. Never `git add -A`: `snapshot_report.html` is tracked.
   Never `git stash` — the stash stack is shared across all worktrees, so a
   `pop` can restore a sibling's work into your tree.

### 3. Fast gate on the branch — seconds, not minutes

Once the slice is complete and committed, run **only the gates that finish in
seconds** — exact invocations in [Commands](#commands):

ReqToCode `check` → `ruff format` + `ruff check`.

Then run **one** focused test — the single test file covering the module you
changed — and nothing else. No full suite, no broader selection:

```bash
uv run pytest <test-file-for-the-module-you-changed> -q --timeout=30
```

### 4. Merge into your base branch yourself — no review, no waiting

**Merging is the agent's job, not a human's.** With § 3 green and the branch
fully committed, integrate it. Do not wait for approval or a review.

`<base>` throughout this section is what `milestone.py branch-for` answered in
§ 1 — the milestone branch when the requirement belongs to one, `master`
otherwise.

First bring `<base>` into the branch, inside your own worktree — that is where
conflicts get resolved, with the worktree's own environment behind you:

```bash
rtk git fetch origin
rtk git merge <base>               # in your worktree, on your branch
```

**Resolve conflicts by keeping both sides' behavior.** A conflict is two
features meeting, not a vote between them: read both sides, then write the
version that does both jobs. Taking `--ours` over a whole file, deleting a
sibling's feature, or reverting a hunk to make the markers go away are all
wrong — the sibling merged working behavior, and you are its only
guard. If two behaviors genuinely cannot coexist, keep both code paths alive
and say so plainly in your report.

- `swr.py` conflicts are expected when both sides added ids: take the incoming
  file, re-run `reqtocode check --fix`, commit the regenerated result.
- Requirement docs and epic indices: keep **both** ids, never drop the incoming
  one to make `diff --strict` quiet.

Then merge to `<base>` **in the one tree that holds it** (§ 1). Which tree that
is depends on the base, and the main checkout never leaves `master`:

```bash
rtk git status                     # untracked or uncommitted work you did not
                                   # create? Leave it alone — a live session may
                                   # own it, and never `git stash` it away.

# base is `master`: the main repo root, the only tree allowed to hold it.
rtk git checkout master            # only ever run in the main repo root
rtk git merge --no-ff <branch> -m "<type>: <summary> (SWR-<n>)"

# base is a milestone or epic branch: its own integration worktree, cut once
# when the branch was created. Never `git checkout` it in the main repo root —
# that frees `master` for a second tree to grab, which is what § 1 forbids.
rtk git worktree list              # find it; cut one if the branch has none:
                                   #   rtk git worktree add .tmp_wt/<base-slug> <base>
cd <that worktree> && rtk git merge --no-ff <branch> -m "<type>: <summary> (SWR-<n>)"
```

If that tree is busy — a live session owns it, or its owner still needs it — do
**not** spin up a second worktree on `<base>`. Two trees on one branch is
exactly the collision § 1 forbids. Instead, update the `<base>` ref without
checking it out anywhere, from your own worktree:

```bash
rtk proxy git push . <branch>:<base>   # fast-forward only; refuses otherwise
```

This is safe precisely because you just merged `<base>` into `<branch>` above,
so `<base>` is an ancestor and the update is a fast-forward. If git refuses,
`<base>` moved underneath you: `rtk git fetch origin && rtk git merge <base>` in
your worktree again, then retry. It costs the `--no-ff` merge commit, so prefer
the main checkout whenever it is free; when it is not, a fast-forwarded `master`
beats a second tree owning the branch.

Never merge from inside the worktree that holds the branch. Push only when
asked.

**The chain, in full.** Unit branches merge into their epic branch; epic
branches merge into their milestone branch; only a milestone branch — or a
requirement belonging to no milestone — merges into `master`. A milestone branch
reaches `master` when, and only when, its gate is green:

```bash
uv run python devtools/milestone.py gate M<n> --tests-passed
```

That is every member requirement `approved`, ReqToCode clean, no requirement
text drifted from its code, both manifests carrying the milestone's
`target-version`, `origin/master` already merged in, and the full suite green on
this head. Merging it is what cuts the release — see
[docs/milestones/README.md](docs/milestones/README.md).

### 5. Clean up the branch and worktree

After the merge, the branch is spent:

```bash
rtk git branch -d <branch>         # -d, not -D: it refuses if the merge failed
rtk git worktree remove <worktree-path>            # ~15 s
```

- `git worktree remove` refusing means uncommitted work is still in the tree.
  Look at it before deciding; do not reach for `--force` to make it quiet.
- `git worktree remove` failing with `Permission denied` is different: Windows
  still holds handles inside the worktree's `.venv`. Nothing is at stake there —
  `rm -rf <path> && rtk git worktree prune` finishes the job.
- `rtk git worktree repair` silently degrades to `git worktree list` — it exits 0
  printing a listing, having repaired nothing. Use `rtk proxy git worktree repair
  <path>`, which bypasses the filter and does the real work.

### Done means done

**Do not stop early.** Work is finished when *all* hold: the requirement is
implemented completely, ReqToCode is clean (`check` green, requirement
`status: approved`, epic index updated), and the branch is **merged into its
base branch** — the milestone branch when the requirement belongs to one,
`master` otherwise (§ 1). A partial implementation, an unresolved trace, or an
unmerged branch is not done — keep going until it is, or state plainly what is blocked
and why.

## Critical rules — ReqToCode (enforced, build-breaking)

**No orphan code, bidirectional or bust.** ALL production code and ALL tests trace to a requirement: implementations carry `@traces(SWR.SWR_<n>)`, tests carry `@verifies(SWR.SWR_<n>)` (`from rotaris_core.reqtocode import SWR, traces, verifies`). Code with no requirement is spec drift. Supplementary code (helpers, plumbing, refactors) with no product requirement → author a **technical requirement** (`type: technical`, `derived-from: SWR-<origin>`) and mirror the `Derived requirements:` link back on the origin. Full workflow: [.github/copilot-instructions.md](.github/copilot-instructions.md) and [docs/requirements/README.md](docs/requirements/README.md).

- Enforced by verifier, `tests/unit/reqtocode/` meta-tests, and CI. A broken trace is a broken build.
- After any edit under `docs/requirements/`, run `python -m rotaris_core.reqtocode diff` **first** — it lists the exact `@traces`/`@verifies` sites to update (`check` misses text-only edits; `diff --strict` gates them). Then `check --fix` → `check`.
- Every production module under `src/rotaris_core/` and `apps/rotaris/src/` needs ≥1 `@traces()` or an explicit `# reqtocode: exempt` (`__init__.py` + generated `swr.py` auto-excused). Orphan-test rule in [tests/AGENTS.md](tests/AGENTS.md).
- Implementing a requirement → set `status: approved` in its frontmatter in the same change + update epic index. Commit requirement docs + `swr.py` + code + tests as one unit, req id in the message.
- **Never** silence a violation by deleting annotations, weakening a requirement, or adding baseline entries (`orphan-baseline.txt` / `traceability-baseline.txt` are shrink-only). Never reuse/renumber an `SWR-<n>` id. On any ReqToCode failure: [docs/reference/reqtocode-playbook.md](docs/reference/reqtocode-playbook.md).

## Commands

All commands use `uv run` (cross-platform: Linux and Windows) — never activate
`.venv`, call `.venv/bin/*`, or invoke bare `ruff`/`mypy`. `make` targets
(`make lint`, …) are thin aliases over the same commands but require
`make`, which Windows lacks — prefer the `uv run` forms below.

```bash
uv sync --all-packages                # setup (apps/rotaris is a uv workspace member)
uv run ruff check src/ tests/ apps/rotaris/src/ apps/rotaris/tests/ --exclude 'tests/fixtures/files/large.py'    # lint (= make lint)
uv run ruff format src/ tests/ apps/rotaris/src/ apps/rotaris/tests/ --exclude 'tests/fixtures/files/large.py'   # format (= make format)
uv run mypy src/rotaris_core/ && uv run mypy apps/rotaris/src/rotaris/          # typecheck strict (= make typecheck)
uv run python -m rotaris_core.reqtocode check --fix                             # reqtocode fix (= make reqtocode-fix)
uv run python -m rotaris .            # run desktop app (--demo for demo data)
```

- ruff, mypy (`strict`), line length, target version: configured in `pyproject.toml` (source of truth).
- HAET edit engine, playbook prompt matrix, session persistence/diagnostics internals: [02-code-topology.md](docs/architecture/02-code-topology.md), [prompt-composition-matrix.md](docs/architecture/prompt-composition-matrix.md), [1500-sessions-diagnostics.md](docs/requirements/1500-sessions-diagnostics.md).

## OpenHands SDK

When touching SDK-adjacent code, verify current OpenHands SDK docs. Main integration points are `Agent`, `AgentContext`, `LLM`, `LocalConversation`, and the tool registry.
