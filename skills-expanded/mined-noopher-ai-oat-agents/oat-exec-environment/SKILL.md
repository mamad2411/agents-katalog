---
name: oat-exec-environment
description: Run build, test, install, and artifact-producing commands inside the Dispatch's execution environment through oat-agents env exec, and report the image they ran under.
---

# oat-agents Exec Environment

Load this skill whenever your Dispatch has an execution environment. The launch tells you so in an `<execution-environment>` block naming the environment id and the image id.

## What goes inside

Run inside the environment every command that compiles, tests, installs, generates, or otherwise produces something:

```
oat-agents env exec -- cargo test
oat-agents env exec -- npm run build
oat-agents env exec -- pytest -q tests/
```

Everything after `--` is handed over unparsed, and the command's own exit status comes back as the exit status of `env exec`. Run it from inside the worktree; the working directory maps straight through, so paths in the output are paths you can open.

## What stays outside

Reading files, `git status`, `git diff`, `git log`, and writing your report stay on the host. The environment exists to make execution reproducible, not to move your whole turn into a container.

## When it is unavailable

Run `oat-agents env doctor` and report its output as a blocker through the channel your role owns.

Do not run the work on the host instead. A result produced where nothing recorded it is not evidence, and a report that presents it as evidence is worse than a report that says the environment was down. The same holds for a command that fails with `env_outside_workspace` or `env_not_ready`: find out why, or report it — never route around it.

## When the environment is missing a package

Installing it inside the container is not a fix. That installation lives in one running container, is gone the moment it is replaced, and is absent from any other role's — so it produces a result only you can reproduce, which is the opposite of what the environment is for.

What the environment has comes from the repository's `.devcontainer/`. Decide first whether this task owns that file. If it does: add what is missing to `.devcontainer/`, then rebuild, from anywhere inside the worktree:

```
oat-agents env rebuild
```

It takes no arguments on purpose. The run, the role, the profile and the worktree all come from the environment already bound to where you are, because naming one of them wrongly would not fail — it would leave a second environment running beside the first.

The result gives the new `image_id` and whether anything `changed`. Editing `.devcontainer/` on its own changes nothing: until the rebuild, every command still runs in the old container.

Then say so in your report: the image id you finished on, that it differs from the one the launch named, and what you added. Anything you verified before the rebuild was verified somewhere else, so re-run what the result depends on.

If the task does not own `.devcontainer/`, report the missing capability as a blocker with the exact command and error. Do not install it inside the container to get past it.

## When a command fails because the environment lacks something

A command that fails because the image has no binary, browser, library or service it needs verified nothing. It is not a pass, not a skip and not "known": the part of the work it covers is unproven, and a report that reads green because of it misstates the Run to everyone who acts on it.

Call a failure known, pre-existing or environmental only by citing where the Run recorded it — a `decision` or `note` in the workflow log, or something the task you were given names. Without that it is a new finding, and you report it as one.

Then take one of the two paths above. If the task owns `.devcontainer/`, add what is missing, rebuild, re-run what the result depends on, and report the old and the new `image_id`. If it does not, report it as a blocker through the channel your role owns — `dispatch ask` for a role — with the exact command, its exit status and the error line, and keep working on whatever that does not block. Do not install it inside the container, do not run the command on the host, and do not drop the failing part from the command so that the rest passes.

Either way, the report lists what stayed unverified: each command that failed for the environment's sake, and which part of what you were asked to verify it leaves unproven. The meta-agent can then decide about it instead of discovering it later.

## Long commands

A build that outlives its own stream is not lost. When a command passes a `--timeout`, the error names the `exec_id` it is still running under; reattach with:

```
oat-agents env exec --attach <exec-id>
```

The command keeps running inside the environment whether or not anything is watching, and the attach returns its real exit status when it ends.

## What the report must carry

- The `image_id` from the `<execution-environment>` block, stated verbatim.
- Verification commands exactly as you ran them, so they can be matched against the environment's ledger.

Every command run through `env exec` is recorded with its argv, exit status, and duration. A report claiming verification that the ledger does not show is a discrepancy anyone reading the Run will see — so report what you ran, including what you ran and abandoned.

## For a role checking another's work

Your environment is a new one built from the same image. Check it:

```
oat-agents env status
```

If your `image_id` matches the one reported earlier in this worktree, you are verifying under the conditions it verified under.

If it differs, find out why before concluding anything. A rebuild that changed the image is one honest reason: the Run log carries an `env_image_built` row, and the newer id is the right one. A difference nobody accounts for is the other kind: the two results were not produced under the same conditions, and that is a finding, not something to reconcile yourself.

The worktree, unlike the environment, is not new — it is the same one, mounted from the same path — and the ledger records what each command ran against:

```
oat-agents env evidence
```

Every entry says whether it ran against the tree as it stands, in the image you are running, and lists under `reuse_blocked_by` any mechanical reason it cannot stand in for a re-run — the code changed after it, or during it, the image differs, it exited non-zero, it never came back. An empty list means none of those apply. It does not mean the command is worth reusing; that depends on whether the command is reproducible, which the ledger cannot see and you can.

A fresh environment is not by itself a reason to re-establish a fact the ledger already holds.

A report you are checking that calls a failure environmental, known or pre-existing without citing where the Run recorded it is a finding, not context: whatever that failure covered was not verified.

## What the fingerprint covers

Tracked files, whatever is staged or unstaged against `HEAD`, untracked files git does not ignore, and the exclude configuration that decides which files those are. A mode change to executable counts; other permission bits do not.

What it cannot see is anything git was told to ignore — `.env`, a generated config, an artifact under a build directory. A command whose result depends on one of those is a command whose prior run proves less than the fingerprint suggests. That is a reason to run it again, and a reason to say why in the report.

A repository with submodules has no fingerprint at all: a submodule's own dirty state does not reach `git diff`, so rather than hash most of the tree and imply it was all of it, the ledger records that it could not tell. So does a tree too large to hash, and a git that would not answer. None of them ever match, including against each other.
