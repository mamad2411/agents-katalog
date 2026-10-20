<!-- BEGIN AGENT-BOX workflow sha256=92395bc8ed359eb4df1606ec6a97757e1ee9c2ef82532f1c2614f912651942a4 -->
Read the tracked task before work; .agent-box.json binds this repository to its tracker project.
Use agent-box tracker for task state, progress and dependencies; read related history when context is missing.
Use ab-interview, ab-plan, ab-work, ab-sync, ab-review, ab-pr, and ab-land as needed. ab-setup maintains this binding and ab-adopt brings an existing project in line with the workflow; ab-normalize processes unmarked tasks in a bound project.
The coordinator owns branches, commits, lifecycle, dependencies, and GitHub actions. Delegate implementation sequentially and research to scouts, which may run in parallel, when their model lists are configured; with an empty list the coordinator does that work itself.
A worker changes project files and answers; scouts and a fresh reviewer only read. Plan sync reads the repository and updates tracker descriptions and comments through agent-box tracker; it never changes project files, Git or lifecycle. The coordinator verifies answers and findings and commits what it accepts.
Tracker comments are a human journal. Branch, base branch, and pull request come from Git and GitHub; lifecycle comes from the tracker's own fields, never from comment text.
Use the user's language for all coordinator messages to them: progress updates, questions, option explanations and final answers. Literal project labels may stay quoted in the project language. Write tracker text, GitHub text, commit messages, code comments and documentation in the `language` that `agent-box tracker status` and `workflow inspect` report; when it is null, use the task's language in the tracker and English for implementation. Agent-to-agent handoffs and reports stay English; agent-box CLI output, errors and help stay English.
Complete subtasks only after validation and integration into the parent branch; complete parents only after merge into the base branch.
<!-- END AGENT-BOX workflow -->

# agent-box — notes for agents working on this repository

## What this is

A launcher. `agent-box` runs Claude Code and Codex CLI inside rootless Podman
workspace boxes. Python standard library at runtime, packaged as `agent-box-tool` with no
runtime dependencies. Install editable for development; uv/pipx or pacman own the public
`agent-box` command and package updates.

```text
pyproject.toml         package metadata and agent-box -> agent_box.cli:main
agent_box/cli.py       argument parsing and command dispatch
agent_box/config_menu.py stdlib curses configuration menu
agent_box/tracker/     portable task contract and product adapters
agent_box/workflow.py  deterministic workflow boundaries; skills orchestrate
agent_box/runtime.py   container lifecycle, mounts, launches, doctor
agent_box/config.py    the whole config schema; flat dataclasses, no framework
agent_box/paths.py     every host-side path; nothing else may hardcode a home layout
agent_box/runtime_bundle.py immutable package copies for running boxes
agent_box/skills/      skills agent-box ships and installs (owned, checked in)
agent_box/Containerfile the workspace image, with optional tool groups
tests/                 unittest, no plugins
```

## Rules that are not negotiable

**Semantic Versioning from 1.0.0.** Use SemVer: PATCH fixes bugs compatibly,
MINOR adds backward-compatible functionality, and breaking changes to the
documented public contract require MAJOR. Describe breaking changes and their
upgrade path in release notes. Package versions and persisted schema versions
are separate; see `docs/compatibility.md` for the public surface and formats.

**Every public version upgrades directly to every later version.** Keep forward
migrations, including across major releases; users never install intermediate
packages. Before changing a persisted format or owned integration layout, assess
migration impact, retain published fixtures, add the required conversion and
test skipped versions, failure/retry and data preservation. Reject future schemas
before parsing or writing; preserve the original before migration commits. Do
not invent migrations for unpublished layouts. Running workspace runtimes stay
immutable; adopting a new runtime may require an explicit stop/relaunch.

**Paths come from `paths.py`.** Use `HOST_HOME` (passwd-derived), never
`Path.home()`, `os.path.expanduser`, or `$HOME`. A poisoned environment must not
be able to move a bind mount, a state directory or the container's home.

**Off by default.** Anything that exposes a credential or widens what an agent
can reach starts disabled. The exceptions are documented in the dataclass that
defines them, with the reason.

**Apply once after a package update.** `runtime.apply_config` is the single
integration writer. Configuration commands apply explicit changes; the first
host launch after a package update automatically migrates data and refreshes
already configured integrations under a lock, recording the package identity
only after success. Unchanged launches and read-only commands do not reapply.
Rendered sessions never infer or rewrite unavailable host settings. Preserve
user-owned content and opt-ins; keep `config apply` for manual edits and retry,
and `uninstall` for removing owned integrations.

On-demand Claude usage may renew and atomically save its OAuth credentials;
this is authentication maintenance, not integration application. Status-line
reads never renew tokens. Coordinate credential writes with Claude's locks.

**Installation belongs to the installer.** uv/pipx or pacman own installed
commands and package updates; uv/pipx also own their shell PATH setup. agent-box never edits shell startup files or installer entry points.
After upgrading the package, the next host launch refreshes integrations;
run `agent-box uninstall` before removing the package through its installer.

**agent-box owns its integrations.** An integration configured somewhere else,
that the user has to assemble first, is not an integration. Settings live in
`config.json`; skills are shipped in `agent_box/skills/` and installed by
agent-box; the container gets a rendered, minimal artifact, never `config.json`
itself.

**Derived, not stored.** A fact that Git, GitHub or the tracker already owns is
read back from there. Branch names come from the task's `ab/<id>-` namespace,
the base branch from origin's default, the pull request from a head/base lookup,
the lifecycle from the board's own columns. `.agent-box.json` names the tracker
project and holds the allowed project configuration overrides. Nothing machine-readable is written into a tracker
comment: a comment is a human journal, and lifecycle is read from the tracker's
own fields.

**Role ownership.** Plan sync may update tracker descriptions and comments through
`agent-box tracker`, reading project files without changing them. The coordinator
owns Git, lifecycle, dependencies and GitHub. Other roles keep their existing limits.

**The coordinator accepts implementation.** A delegated worker reads its brief and
the code, changes project files in the working tree, and answers in Markdown;
a reviewer or scout reads and reports, changing nothing at all. The
coordinator decides from that answer what to commit and what to record in the
tracker and on GitHub. This is a contract, not credential isolation: a
delegation runs either as a native subagent of the coordinator's own session or
as a managed `codex exec` / `claude -p`, the first of which inherits the
coordinator's workspace, `.git` and credentials, so the two backends
deliberately share one contract rather than one of them acquiring private
restrictions. Workers and scouts are therefore only launched (`workflow
delegate`), never tracked: guards that only existed because the contract was
wide belong deleted, not tightened. A reviewer round is still bound to its
repository, project, task and scope by the descriptor workflow keeps beside the
round's input, which is plain readable JSON and is deliberately not treated as
unforgeable; a native reviewer's model and context are taken on trust.

**Secrets travel by name.** `--env=NAME` (Podman inherits the value) for
anything secret; `--env=NAME=VALUE` puts the value in an argv that `/proc`
exposes to other processes. `notify.sync_credentials` and
`runtime.sync_tracker_runtime` are the pattern for rendered credential files.

**Never overwrite what a user owns.** Skill directories carry a marker; ones
without it are the user's. Claude's `statusLine` slot is filled only when empty.
Hook removal only ever touches agent-box's own commands.

## Working in the code

- **All text an agent may read must be functionally compact.** Skills, instructions,
  handoffs, messages, errors, hints, CLI help and command output need enough context,
  exact commands and necessary constraints to act without guessing; remove filler
  and repetition without cryptic compression.
- **Comments explain why, not what.** The existing docstrings state the decision
  and the alternative that was rejected. Match that; do not add narration.
- **Tests are the specification.** Every test's name and docstring says what
  behaviour is being protected and why it would be wrong otherwise. A test that
  restates the implementation is noise.
- **Structural vs per-exec.** Anything in `container_lifetime_args` is part of
  the box's identity: changing it recreates the box. Per-invocation values go
  through `invocation_env`. Choose deliberately.
- **Diagnostics are returned, not printed**, so both the launch path and
  `agent-box config` can render them (`tracker_warnings` is the pattern).

## Commands

```bash
python3 tests/run_suite.py              # full suite; isolated paths, no outer PTY
python3 -m agent_box selftest                     # fast, no Podman
uvx ruff check --select E4,E9,F agent_box/ tests/   # what CI lints
python3 -m agent_box config show                  # inspect the live config, tokens redacted
```

The runner uses unittest discovery, temporary state/integration paths and piped
stdio. For focused runs: `python3 tests/run_suite.py discover -s tests -p test_browser.py`.
Test modules import each other by bare name, so keep discovery.

## Gotchas

- `tests/` must never touch the developer's real `~/.claude` or `~/.agents`.
  Anything that calls `config_interactive` or `apply_config` has to patch
  `runtime.CLAUDE_HOME`, `runtime.CODEX_HOME`, `runtime.AGENT_SKILLS_DIR`, `runtime.MANAGED_SKILLS_SOURCE`
  and the credential paths. This has bitten before.
- Module-level constants derived from `paths.py` (`AGENTS_DIR`, `TRACKER_RUNTIME_DIR`,
  `CONTAINER_TRACKER_RUNTIME_DIR`) are resolved at import; tests patch them on `runtime`,
  not on `paths`.
- `tests/run_suite.py` and `selftest` drop every inherited `AGENT_BOX_*` variable,
  so they pass inside a workspace box as is; a bare `python3 -m unittest` does not,
  and reads the session's `AGENT_BOX_RUNTIME_CONFIG` instead of its fixtures.
- The image label `io.agent-box.tools` records the built tool groups. A missing
  label means *unknown*, not *empty* — never report it as drift.
- Inside a workspace box the saved configuration is not mounted: `config apply`
  then applies only the skills and profiles the rendered session snapshot
  describes and leaves host-only sections (notifications, hooks, status line,
  credentials, Claude links) alone; the global `agent-box config` menu
  refuses because it edits a file that is not there.
- `agent_box/skills/` contains short owned `ab-*` skills. Maintain them directly
  and keep their command/role contracts consistent with the Python helpers.
- `.gitignore` ignores `/skills/` at the repo root only — `agent_box/skills/` is
  checked in on purpose.
