---
# Adapted from openai/codex-plugin-cc (Apache-2.0) and modified for agy. See NOTICE.
name: gemini-prompting
description: Guidance for turning a user's request into a clear prompt for agy (Gemini 4) in the agy-rescue subagent
user-invocable: false
---

# Prompting agy

Use this skill only to tighten the request text that `agy-rescue` forwards. Do not inspect the repository or solve the task.

The companion already wraps the request in a template that tells agy it works in a separate copy, how commands are handled, to give no verdict on material it cannot reach, and how to report. Add only what the request is missing:

- **One task per job.** Split unrelated asks.
- **Done condition.** Say what finished looks like: "the failing test in tests/test_upload.py passes", not "fix uploads".
- **Scope.** Name the files or directories in play when the user did, and say what must not change.
- **Evidence.** For diagnosis, ask agy to separate what it observed in files from what it infers.
- **Material.** agy sees only the repository's files, and in container mode no git history or refs. A request that depends on a diff between refs, a pull request description or a file outside the repository must include that text. Do not write "run `git diff origin/main...pr/96`"; for a review of a ref the subagent uses `review --head`, and the rest of the request goes with it as the review's instructions.
- **No verdict without the material.** For a judgement on pasted material, add: "If anything you need is missing, say what and give no verdict."
- **Exact copies.** If the user wants text copied from a file, say "copy it from <path> character for character, or say you could not open it".

Keep the user's wording where it is already clear. Do not raise the model or add effort instructions unless the user asked.

## Gotchas

- In host mode agy cannot run tests itself: a test command is queued for Claude and costs a resume round. If the done condition needs a test run, name the exact command so it is queued once, not guessed at several times. In container mode agy runs its own commands.
- Long pasted context costs tokens on every resume, because a resumed conversation carries its history. Point agy at files in the repository instead of pasting them. Paste only what the job cannot reach: a diff between refs, or a file outside the repository.
- "Verbatim" in a prompt does not make agy copy; it has written invented text under that label. The result-handling skill's verification step is what catches it.
