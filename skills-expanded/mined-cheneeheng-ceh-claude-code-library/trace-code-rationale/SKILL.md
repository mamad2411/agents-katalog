---
name: trace-code-rationale
description: >-
  Load this skill when the question is why code is the way it is, not what it does: trace it
  through git log, blame, PRs, and issues, citing each claim. Trigger on "why is it like this", "why
  was this added", "is this safe to remove".
argument-hint: "<file>[:<line>-<line>] | <symbol>"
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Requires the git CLI on PATH and a git working tree with full history; a shallow clone truncates
  the answer. The PR and review-comment lookup also needs the GitHub CLI (`gh`) authenticated via
  `gh auth login` and network access. Without `gh` the skill answers from commits alone and says
  so.
license: Apache-2.0
---

# Trace code rationale

Answer "why is it like this" from the project's history, not from the current code. Done when
every claim in the answer cites a commit, PR, issue, or file, and every part of the question the
history does not answer is named as not recorded.

The current code shows what it does, never why. A reason guessed from the code reads as plausible
and is often wrong, and someone who deletes a guard on a guessed reason brings back the bug it was
added for.

## Procedure

1. **Pin the target.** Name the file and line range, or the symbol, and restate the question as
   "why does `<target>` do `<behavior>`". Read the current code only to find the lines.
2. **Check the history is whole.** `git rev-parse --is-shallow-repository` printing `true` means
   older commits are missing. Say so, and fetch them with `git fetch --unshallow` before going on.
3. **Find the commits that shaped it.** Start with the line history, then use blame and pickaxe for
   what it misses:

   ```bash
   git log -L <start>,<end>:<file>                 # every commit that touched these lines
   git blame -w -C -C -M -L <start>,<end> <file>   # skips whitespace, follows moves and copies
   git log -S'<distinctive string>' --follow -- <file>   # when a string appeared or vanished
   ```

   If `.git-blame-ignore-revs` exists, pass `--ignore-revs-file .git-blame-ignore-revs`. Blame
   names the last commit to touch a line, which is often a reformat or a move. Keep going back
   until you reach the commit that introduced the behavior, not just the text.

4. **Read the introducing commit whole.** `git show <sha>` gives the message and the full diff,
   including the other files it changed. The reason often sits in a test or config file next to
   the line you care about.
5. **Find the PR and issue.** Squash merges keep the discussion in the PR, not the commit:

   ```bash
   gh api repos/{owner}/{repo}/commits/<sha>/pulls --jq '.[].number'
   gh pr view <N> --comments            # description and review discussion
   ```

   Follow every `#NNN`, `Fixes`, or ticket id in the commit or PR to its issue. Check the repo's
   decision records, ADRs, and `CHANGELOG.md` entries from the same dates.

6. **Answer.** Use the shape under Output.

## Rules

- **Cite every claim.** Each sentence of the answer names its source: a short sha, `#PR`, `#issue`,
  or `path:line`. A claim with no source is a guess, and a guess goes under Not recorded.
- **Stated beats inferred, and the answer says which is which.** "The PR says X" is stated.
  "The diff adds a retry right after an outage issue, so likely X" is inferred, labelled as such,
  with both sources.
- **The diff outranks the message.** When a commit message says one thing and the diff does
  another, report both and trust the diff for what changed.
- **"Not recorded" is a valid answer.** When the history gives no reason, say so and list where
  you looked. Never fill the gap with a reason that sounds right.
- **Read only.** This skill changes no files and no history. A fix or deletion the answer suggests
  is a separate task.

## Output

Reply in chat, no files:

```markdown
**Question:** why does `<target>` do `<behavior>`?

**Answer:** <two or three sentences, each with its citation>.

| Date       | Commit    | PR / issue | What changed           | Why, as recorded                    |
| ---------- | --------- | ---------- | ---------------------- | ----------------------------------- |
| 2024-03-02 | `a1b2c3d` | #412, #398 | added the retry on 503 | "upstream drops 1 in 50 under load" |

**Not recorded:** <each part of the question the history does not answer, and where you looked>.
```

When the question was "is this safe to remove", end with the condition under which removing it
would bring the original problem back, cited to the commit or issue that describes the problem.

## Stop conditions

- Not a git repository → say so. With no history there is nothing to trace from.
- The history is shallow and cannot be fetched (no remote, no network) → answer from what exists
  and say where the history stops.
