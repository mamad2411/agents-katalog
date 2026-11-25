---
name: vibe-ssh
description: Operate the user's own servers over SSH through the Vibe-SSH app - run commands, upload project files, deploy and troubleshoot - while the user watches and can take over. Use it whenever a task needs a remote server the user has added to Vibe-SSH, instead of calling ssh or scp directly.
metadata:
  bootstrap: "true"
---

# vibe-ssh

Read one version-matched guide for the task. For an Nginx static-site deployment,
run `vibe-ssh skill static-site && vibe-ssh hosts` in the same tool call.
For Compose use `vibe-ssh skill compose`; for other SSH tasks use `vibe-ssh skill`.
The guide ends with a line starting `[vibe-ssh:skill] end of guide`. Read the
missing lines if output is truncated.

For a known deployment, use `vibe-ssh batch` with one explicit plan for related
commands and uploads. Each step is a separate application job. Inspect the step
results before submitting anything else when the outcome is `stopped`.

If `vibe-ssh` is not on PATH, run `"$HOME/.local/bin/vibe-ssh" skill`.
Opening the installed Vibe-SSH app automatically configures the version-matched
Skill and command. If neither command exists, ask the user to open the app and
check its integration warning; never overwrite unrelated skills or fall back
to plain `ssh` with the user's keys.
