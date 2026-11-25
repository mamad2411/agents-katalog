---
# Adapted from openai/codex-plugin-cc (Apache-2.0) and modified for agy. See NOTICE.
name: agy-result-handling
description: How to present agy (Gemini) review, plan and task output to the user, including verifying agy's quotes and file:line claims before relaying them
user-invocable: false
---

# Presenting agy results

## Verify before relaying

agy has presented invented text as a verbatim copy of a real file, with wrong names and invented rules. Treat every specific claim as unverified until checked:

- For each `file:line` reference and each quoted code or text, open the file in the user's repository (Read or Grep) and confirm the line exists and says what agy claims.
- A review started with `--head <ref>` describes that ref, not the checkout. Its result ends with "Paths and lines are as of <ref>"; check its claims with `git show <ref>:<path>`, not with the working tree.
- Check names agy gives for files, functions, settings, projects and commands.
- In your reply, say which claims you checked and which you could not. Mark a claim that failed the check as wrong and show what the file actually says. Do not silently fix it.
- For plans, check any step that tells the reader to copy something "exactly" or "verbatim" against the source.

## Presentation

- A result with a `Cannot review:` line in place of a verdict is not a review. Report what was missing, give no verdict of your own in its place, and do not approve anything on the strength of it. The same holds when a task reply gives a verdict and also says it could not see the diff, a ref or a file.
- Reviews: findings first, ordered by severity, with file paths and lines as verified. If there are no findings, say so.
- Plans: give the plan, then the verification notes. Do not start implementing.
- Tasks: say that agy changed files only in its working copy, list them, and point to `/agy:apply <job>`. Do not apply them yourself unless the user asks.
- Keep agy's distinctions between facts, inferences and open questions.
- After a review or plan, stop. Ask the user which findings or steps, if any, they want acted on before touching a file.

## Queued commands

Only a host-mode job queues commands; a container job runs its own. A job in `needs-approval` lists shell commands agy wanted but was not allowed to run. Run each one you would run on your own judgement with your own Bash tool, in the job's working copy shown by `/agy:status <job>`. Your normal permission checks decide. Skip anything you would not run and say why. Save the commands and their output to a file, then `/agy:resume <job> <file>`. If none are worth running, read the result with `/agy:result <job>` instead.

## Failures

- If the job failed, show the error and the last agy stderr lines, then stop. Do not do the task yourself in place of agy.
- A failed job shows `Failure: <class> (exit <code>)`. Act on the class, not on the wording: `signin` and `licence` need the user to sign in again with `agy` in a terminal, so pass on the error's step as it is and do not change the model and retry, because every model fails the same way until then. `container` needs Colima or Docker started, or the image rebuilt with containers/build.sh. `agy-missing` points to `/agy:setup`. `quota` means wait. Only `stall`, `timeout` and `agy-failed` are worth one retry, on the same model. Never retry a stalled job on a lower model: a stall is a fault in Google's service, and a lower model returns weaker work.
- If status shows stalls, say how many there were and on which model.

## Gotchas

- A completed review can still contain invented line numbers. The verification step applies every time.
- Paths in review and plan results already point at the user's repository. Paths in task results point at the job's working copy, because those files differ until applied.
- agy's reply may say it "ran" a command that was queued instead. Trust the job's queued-command list over the prose.
