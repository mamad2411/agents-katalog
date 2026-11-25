---
name: guardrails
description: "Guard of the irreversible: cancels a call that would switch off the protection itself — the guard's wiring and the project registry — install a new dependency, or wipe the working tree. Forbids weakening the checks that constrain the agent itself; runs as a PreToolUse hook and judges only Bash, while the project's protected paths are held by the harness `deny`."
disable-model-invocation: true
---

# The guard

## Why it exists

The regulation, the gate, import contracts, linter concessions — rules that CONSTRAIN the agent.
The agent also has write access to them. The moment a rule gets in the way, the cheapest exit is not
to solve the task honestly but to **weaken the rule**: add an ignore, drop a step from the gate,
soften a contract. This is not a hypothesis — it has already happened.

**Protection cannot be built on self-checking.** A hash-lock inside the gate the agent lifts with
the same motion as the rule. Only a ban enforced by **NOT the agent** works: the PreToolUse hook is
run by Claude Code itself BEFORE the call reaches the file; exiting with code 2 cancels the call.

## What it protects

Not "important files" but exactly those that **constrain the agent** — editing any of them weakens a
check that would otherwise catch sloppiness. The list is in `<project>/.retainer/config.toml` (the
`protected` field). Typically: linter configs, import contracts, the gate script, git hooks, CI
workflows, the regulation, agent instructions, the guard itself and its config.

## What is closed

- **Edit / Write / NotebookEdit** on protected paths — shut tight, but exactly where there is an
  `Edit` rule under the path in the harness registry. The native `deny` does this, not the guard:
  the guard does not judge write tools at all, and whether the two registries agree is checked by
  the gate step `deny_sync`. A rule names a path: a second worktree or a clone of the same
  repository in another directory is open until a rule names that path. And git is not a write
  tool — `checkout`, `pull` or `merge` change a protected file, and a commit carries whatever edit
  lies in the tree.
- **Bash into the guard's own wiring** — writing to `~/.claude/settings.json`, `~/.claude/hooks` and
  the managed-repo registry: editing them disables protection silently. Reading is allowed, changing
  is not.
- **A config the guard cannot read** (always on): when `.retainer/config.toml` leaves an array or a
  multiline value unclosed, or is not UTF-8, every key after the break is lost, and so is every
  `guard_*` flag among them. Every Bash command in that repository is then refused until the owner
  fixes the file or issues the key. A broken single line (an unclosed quote) is not refused: the
  other keys are read, and the broken value keeps its gate on.
- **The new-dependency gate** (on by default, turned off by `guard_dependency = false`): a command
  that ADDS a package via a language manager (`pip install X`, `poetry add`, `uv add`, `uv pip
  install X`, `npm i X` — including `-g`) is blocked without a key: a new dependency is the owner's
  decision. The manager registry is closed: others are not judged until their form is met live.
  Restoring the declared (`npm ci`, `pip install -r`, `poetry install`, `uv sync`), installing your
  own project (`pip install -e .`), bootstrapping the manager (`pip install -U pip`) and system
  managers (`brew`) are not touched.
- **The destructive gate** (opt-in, `guard_destructive = true`, legacy `guard_git`): `reset --hard`,
  `clean -f`, `branch -D`, `checkout .`, `restore .`, force-push (also by a `+ref` refspec), a push
  that deletes remote refs (`:ref`, `--delete`, `-d`, `--mirror`), **`rm -rf`**, `find -delete` and
  `find -exec rm`, `dd`, `shutdown`/`reboot`/`poweroff`, `chmod -R` — blocked without a key. A
  heredoc piped into a shell (`cat <<EOF | bash`) is judged by its body. An ordinary `git push`, a
  single `rm file`, `chmod +x` are not touched. Commands are tied to position (not to text in
  quotes) — a mention in a commit message/`echo` is not cut. (The list was vetted against, among
  others, Roo deniedCommands.) An exception by TARGET: `rm -rf` passes when ALL targets are
  recoverable by definition — a system temp directory (including one made by `mktemp -d` in the same
  command) or a run cache (`__pycache__`, `.pytest_cache`). The target is normalized before the
  check, so climbing out of a temp directory with dots stays a block, and a managed repository
  inside a temp directory is work, not trash. `find` has no such exception: `find <temp> -delete`
  is refused too.

## An honest boundary

The Bash check is a string heuristic. An elaborate bypass (assembling a file name from pieces) it
does not catch and should not: the goal is not "stop an attacker" but to remove the easy path.
Protected project paths are held by the harness `deny` — one rule for all editing tools; the guard's
Bash layer closes its own wiring, and there a quoted launcher argument (`sh -c …`) is parsed as a
command. A write into a project's `protected` the guard does not cancel at all — measured with a
live hook: `sed -i`, `echo >` and `cp` on a protected path pass — and a script lying as a file is
invisible to it: it does not read its text. The rest requires a deliberate multi-step sabotage,
visible in the diff + at code-reviewer + at the owner's "ok".

**The managed-repo registry.** Its contents the guard does not read. The registry drives the sweeps of managed projects — the
digest and the registry-vs-disk check — and the settings panel: they need to know which projects to
enter. The registry file itself is in the globally protected set, so without a key a write to it is
cancelled. The key needed here is the GLOBAL one (`~/.retainer/unlock`) — a project one does not open
the registry. **The owner registers a repo in THEIR OWN terminal.** What the guard judges instead is listed above:
a write into its own wiring, a new dependency, destruction and a secret leak.

## Unlocking — only by the owner

Rules sometimes must change (a new layer → a new contract). Then: **show the owner the exact diff and
explain why the old rule is wrong.** The key is issued only by them, in their terminal:

```bash
touch <project>/.retainer/unlock     # the path is from config.toml (unlock_file)
```

It lasts 30 minutes and rots on its own. The easy path to issuing it is closed: the common Bash
write forms aimed at the global key or at the project key of the repository the agent works in are
cancelled by the guard, and the owner's `touch` in their own terminal goes past the hook. The match
is a coarse string match, so a write after `cd` into the key's directory or through a writer outside
the verb list still passes — the same limit as for the wiring above. The same match refuses a command
that only names another tree's `.retainer/unlock` next to a write verb. A valid key may be touched again. A write tool on
the global key is held by the native `deny` the owner adds — the guard does not judge write tools.

**The key does NOT lift everything.** Under the guard — yes; under the harness native `deny`
(`.claude/settings.json`) — no: deny fires EARLIER than the hook, and the key does not open it. The
same path is sometimes closed both ways, and this is not visible in advance to the agent or the
owner.

| Closed by | Lifted by |
|---|---|
| the guard only | the owner's key (`touch …/unlock`), 30 minutes |
| also the native `deny` | nothing: the owner makes the edit themselves or removes the path from `deny` |

Which of the two rows is true the guard says itself — in the refusal text: under the native `deny` it
names the owner as the editor, not the key. Literally this reads where the rule is written in a form
the guard recognizes. The forms `//path` and `~/path` it does not recognize, and the registry is
written exactly in them — the protection check prints them for pasting — so the refusal calls for a
key where it will not help. While this holds, the `deny` row is verified by the reader.

## Rollout into the plugin cache — a separate step, not a consequence of a commit

The rules run from the **installed plugin's cache** (`~/.claude/plugins/installed_plugins.json` →
`installPath`), not from the working tree. Two consequences, both of which cost a whole run.

**A commit does not equal a rollout.** `claude plugin update` compares the version NUMBER, not the
content: the same number in the tree and the cache gives "already at the latest version", and the
cache freezes. A rule can be written, covered by tests and merged — and not run. The divergence is
caught by preflight (the "rollout" check), comparing the contents of the executable directories; it
also names what to roll out with.

**The cache the guard does not judge at all.** The installed-plugin directory is excluded from
managed repositories: there is nothing to protect — the cache contents are not a source but a copy,
and an edit in it is lost on the next install. So a write into the cache the guard does not cancel and
requires no key for it; the cost of error here is not a lost edit but the cache diverging from the
tree, and that is caught by preflight.

## The guard's disappearance must be loud

**A mechanism does not count as working until a gate checks it.** Checking "the file is in place" is
pointless — a dead backup hook was in place as a file (a real case: the config lay in a project
`.claude/` which does not load when the session root is `~`; 13 commits and hundreds of edits over a
day passed without a single snapshot, including a split of modules into packages — found by chance).
So the gate probes the guard with a **live command** and fails if it stopped blocking.

## There are NO snapshots or rollback

Protection holds by cancelling the call BEFORE the write, not by restoring what was written: a
snapshot before an edit and a rollback of the written are removed, the guard has no `PostToolUse`
event. So before a destructive operation that bypasses the write tools (a bulk `sed`, a script
writing to files directly, a migration with data loss) there is nothing to restore — the copy is made
by whoever undertakes the operation.

The implementation is `retainer/hooks/guard_discipline.py` (project-aware: one hook, the config from
the `.retainer/config.toml` of the repository the edit targets). Activation — `docs/guard.md`.

## When NOT to apply

- **The guard does not catch bugs in code.** It catches the weakening of rules. A logic defect, a
  forgotten case, a wrong algorithm — the subject of the gate, tests and review, and expecting them
  from the guard means treating as protected what is not.
- **Not a replacement for review and not a replacement for the gate.** It guards the checks, it does
  not check itself.
- **Not a tool against the human.** The owner lifts protection with their key by construction;
  building the guard into a ban for the owner means breaking the only legitimate exit.
- **Not for a foreign tree the engine has not reached.** The hook is run by the harness; where there
  is none, the rule is held by whatever held it before the guard — and that must be said aloud.
