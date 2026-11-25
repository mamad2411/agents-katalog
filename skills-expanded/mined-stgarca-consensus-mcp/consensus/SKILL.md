---
name: consensus
description: Bootstrap or check consensus-mcp in this project. Trigger when the user says "consensus init", "bootstrap consensus", "set up consensus", "initialize consensus-mcp", or asks to install/enable the cross-AI consensus workflow in their current project.
---

# Consensus-mcp project bootstrap

This skill is the entry point for setting up the **consensus-mcp** cross-AI
consensus workflow in a project. It is invoked when the user expresses intent
to initialize consensus-mcp - typically by typing phrases like
"consensus init", "set up consensus", or "bootstrap consensus" without a
leading slash.

## First: which operation did the user ask for?

Inspect the FLAGS the user actually typed and run EXACTLY that command - never
silently substitute a different one, and never afterward offer to run a command
the user just typed.

- **`--install-claude-code`** -> the ONE-TIME, MACHINE-WIDE install (the README's
  "add a small Claude Code helper so you can type 'consensus init' in any
  project"): it copies the consensus skills + slash command + enforcement hooks
  into `~/.claude`. This is NOT the per-project bootstrap. Run
  `consensus-init --install-claude-code` (add `--force` only if the user did),
  surface its output, and on exit 0 tell the user to restart Claude Code (or
  `/mcp`); then OFFER to run the per-project bootstrap
  (`consensus-init --from-claude-code`) since the helper install does not set up
  the current project. On exit 5 relay the stale `SKIP:` files (`--force`
  updates); on exit 6 the install is INCOMPLETE (enforcement OFF) - relay the
  remedy from stderr (e.g. `pipx install --force consensus-mcp`). Do NOT offer
  `--install-claude-code` again - you just ran it.
- **`--uninstall-claude-code`** -> run `consensus-init --uninstall-claude-code`.
- **otherwise (the default, plain "consensus init")** -> the per-project bootstrap
  below.

## What it does (the per-project bootstrap)

1. Run the shell binary `consensus-init --from-claude-code` (installed by
   `pipx install consensus-mcp`), carrying through any other flags the user typed
   (e.g. `--reconfigure`, `--force`, `--repair`).
2. Surface the binary's stdout/stderr verbatim - `consensus-init` already
   prints the right next-step guidance, so don't paraphrase or summarize.
3. If `consensus-init` fails because the binary is not on PATH, tell the
   user to run `pipx install consensus-mcp` once globally.
4. After a successful bootstrap, point the user at the restart step
   (Claude Code must reload to pick up the new MCP server). The CLI output
   already says this; just confirm. If the binary's "Enforcement status" line
   reports ADVISORY mode (the one-time global step has not run on this machine),
   you MAY offer to run `consensus-init --install-claude-code` once to enable
   edit-gating - but only if the user did NOT already ask for it this turn.

## How to invoke

Use Bash to run `consensus-init --from-claude-code` from the current
working directory. The binary detects the project root automatically
(git rev-parse -> strong markers -> cwd, per iter-0031).

## Workflow modes the operator can pick (v1.14.4+)

The wizard will prompt for `--workflow`. Three modes plus advisory:

- **Workflow A** = `propose-converge` (DEFAULT) - all contributors
  propose blindly, then converge across reviewed rounds. Use for
  design questions where reasonable people could disagree.
- **Workflow B** = `post-review` - one AI implements, others audit.
  Lightweight; use for execution per a converged design or hot-patches.
- **Workflow C** = `autonomous-execute` (NEW) - runs to completion
  overnight without operator-in-the-loop, auto-approving emergent
  scope items within an operator-pre-declared `autonomy_contract`.
  v1.14.4 ships the CONTRACT (validators, scope_check, halt-set,
  audit-ledger); the multi-iteration engine is **UNIMPLEMENTED as
  of v1.15.2 - no committed target version**. Operators can stage
  and validate Workflow C goal_packets; running one raises a clear
  `NotImplementedError`. Status:
  `docs/workflows/workflow-c-autonomous.md`.
- **Advisory** - dispatches happen but no vote is load-bearing. Rare.

Numeric aliases (3, 4) still resolve at the CLI but emit a
`DeprecationWarning`; will be removed in a future minor release.

For the operating procedures (when to use which workflow, how to
dispatch peers, halt conditions, etc.) the bootstrap pack also
installs `~/.claude/skills/consensus-workflow/SKILL.md` - that
skill is the load-bearing reference and triggers automatically
on workflow-execution intent.

## If the project is already configured -> treat re-init as an UPGRADE

If `consensus-init` exits with code 4 AND the first line of its stdout is
exactly `STATUS: already-configured`, the project is already set up - this is the
normal RE-INIT case (e.g. after upgrading the package). Do NOT show a
leave/reconfigure/force menu, and do NOT surface the raw "Error" - re-running init
on an existing project should behave like an idempotent **upgrade**, not a prompt.

1. Consume (do not display) the `STATUS: already-configured` token line.
2. Run `consensus-init --from-claude-code --repair` once. This is the upgrade:
   it verifies + refreshes the consensus-managed pieces (`.mcp.json`, the
   `.gitignore` block, the agent files, the instruction managed-blocks) WITHOUT
   touching the user's panel/config, and reports the REAL enforcement state.
3. Relay its summary lines verbatim (`OK:` / `REPAIRED:` / `SKIP:` /
   `REPORT-GLOBAL:`). Tell the user the project is up to date.
   - If it exits 0: confirm everything is current; stop.
   - If a line is `SKIP:` (a managed file DIVERGED because the user hand-edited
     it), tell the user that re-running with `--force` overwrites those SPECIFIC
     files - but do NOT force automatically.
   - If a line is `REPORT-GLOBAL:` (the once-per-machine enforcement step hasn't
     run), relay that they can enable edit-gating with
     `consensus-init --install-claude-code`. Do NOT suggest this when no
     `REPORT-GLOBAL:` line is present - enforcement is already on.

This is a single, non-looping pass; never re-offer a command the user already ran.

## If it looks like a workspace folder (not a project)

If `consensus-init` exits with **code 8** AND the first line of its stdout is
exactly `STATUS: looks-like-workspace-umbrella`, the current directory is a
*workspace folder containing git projects*, not a project - bootstrapping it
would blanket every sub-project. Do NOT surface the raw error. Instead:

1. Consume (do not display) the token line; the stderr guidance names the child
   projects found.
2. Present these options via `AskUserQuestion`:
   - One option per child project found (enumerate them from the stderr list,
     **capped at ~10**) - "Initialize `<that project>`" -> re-run
     `consensus-init --from-claude-code` from inside that project directory.
   - **Initialize here anyway** -> re-run `consensus-init --from-claude-code --here`.
   - **Cancel** -> stop; nothing was written.
3. Act on the choice one-shot (the project dir / `--here` suppresses the token, so
   no loop).

## What NOT to do

- Don't reimplement any of `consensus-init`'s logic. It writes
  `.consensus/config.yaml`, `.mcp.json`, and a `.gitignore` managed
  block - let the binary handle all of that. (The ONE exception is the
  already-configured carve-out above: exit code 4 + the
  `STATUS: already-configured` token triggers the AskUserQuestion menu,
  and the workspace-umbrella carve-out (exit code 8 + the `STATUS: looks-like-workspace-umbrella` token).)
- Don't paraphrase the binary's output. Operators rely on the exact
  next-step text from the CLI.
- Don't run if the user is asking a conceptual question
  ("what is consensus-mcp?", "how does consensus work?") - that is
  not a bootstrap intent.

## Expected output flow

```text
$ consensus-init --from-claude-code
.mcp.json written: <project-root>/.mcp.json
.consensus/config.yaml written: <project-root>/.consensus/config.yaml
.gitignore managed block added.

Detected --from-claude-code: Claude Code must reload to activate the
consensus-mcp server. Either restart Claude Code in this project
(Ctrl-C, then `claude code`), or run `/mcp` to reload MCP servers
if your build supports it.
```

After running, confirm the message to the user and stop. Do not
attempt to invoke any consensus-mcp MCP tool in the same session -
they won't be available until Claude Code reloads.
