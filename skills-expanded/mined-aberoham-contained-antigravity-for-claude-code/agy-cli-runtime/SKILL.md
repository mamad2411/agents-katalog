---
# Adapted from openai/codex-plugin-cc (Apache-2.0) and modified for agy. See NOTICE.
name: agy-cli-runtime
description: Internal contract for calling the agy companion script from the agy-rescue subagent
user-invocable: false
---

# agy runtime contract

Use only inside the `agy:agy-rescue` subagent.

Helpers, all through `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/agy_companion.py"`:

- `task [--background] [--model <level|family|family-level|model ID>] [--read-only] [--read-dir <directory>] [--resume-last] "<request>"`
- `review [--base <ref>] [--head <ref>] [--scope auto|working-tree|branch] [--model <level|family|family-level|model ID>] [--instructions-file <path>] ["<instructions>"]`
- `adversarial-review` with the same flags and instructions as `review`

`--caller-model "<Claude model ID>"` is accepted by all three; pass it on, quoted, when the request carries it. IDs such as `claude-opus-5-5[1m]` contain brackets that zsh would otherwise expand.

Rules:

- One `task`, `review` or `adversarial-review` call per handoff. The only other call is `result <job> --wait-seconds 590`, to wait for that same job when it is still running. Do not call `plan`, `status`, `cancel`, `resume` or `apply`.
- A request to review a diff, a branch, a ref or a pull request goes to `review`, never to `task`. `review` collects the diff on the host and puts it in the prompt; `task` carries only the request text.
- A review carries the caller's instructions to agy beside the diff: the pull request's title and description, the things to check, the report wanted. Give them as the last argument or with `--instructions-file <path>`. The file is read on the host, so it may be outside the repository. A request for something outside the copy, such as a comparison with another pull request, comes back listed under next steps as not done.
- `--head <ref>` reviews that ref against `--base` without checking it out. The job's copy is built from the ref's tree, without the user's uncommitted changes and without the ref's `.agents` directory, so a pull request's own agy hooks do not run. The ref must already be in the user's repository, for example fetched as `refs/remotes/pr/96`.
- `--background` returns a job id at once. Without it the companion waits up to 100 seconds, or `--wait-seconds <n>`, then reports that the job is still running and prints the `result <job> --wait-seconds 590` command that waits for it.
- For read-only work (`review`, `adversarial-review`, `task --read-only`) pass `--wait-seconds 590` and give the Bash call `timeout: 600000`. A review rarely finishes inside 100 seconds, and often takes 15 minutes or more, so wait again with the printed `result` command until it finishes, for at most six follow-up waits.
- A job id works from any directory for `result`, `status` and `cancel`, which find the job in the checkout that ran it. `apply` runs only in that checkout and says where it is.

## What the job can see

- Container mode (the default when Docker is available): a copy of the repository holding one commit. It has no history, no remotes and no refs such as `origin/main` or `pr/96`, so `git diff a...b` cannot work there. Nothing of the user's outside the repository is mounted in the container except a `--read-dir` directory.
- Host mode: a detached worktree, where agy may read files in the repository and in a `--read-dir` directory, and most shell commands are queued.
- A `task` request must therefore carry any diff, or any text from a file outside the repository, inline, or name the file's directory with `--read-dir`. When a request names a ref or an outside path, the companion prints a `Note:` line before the result.
- When agy lacks the material, a review's result has a line that starts with `Cannot review:` where the verdict would be, and no `Verdict:` line. Treat that as no review, never as an approval.
- A task job edits its own working copy under the plugin's state directory: a self-contained copy in container mode, a detached git worktree in host mode. The user's checkout changes only when they run `/agy:apply`.
- `--resume-last` continues the newest finished task this Claude session started in this repository, in the same working copy and agy conversation. With `--read-only` that round cannot edit, but the task's earlier edits stay applicable.

## Gotchas

- Never call `agy` directly. In some shells `agy` is a shell function that the Bash tool cannot see, and the companion is what adds the worktree, the tool policy hook, the write sandbox and stall recovery.
- Never pass `--dangerously-skip-permissions`. Only the companion's container backend adds it, inside the container; in host mode the companion refuses it.
- In host mode, shell commands that are not read-only are not run by agy: the job ends as `needs-approval` with the commands listed. That is expected, not a failure. In container mode agy runs its own commands.
